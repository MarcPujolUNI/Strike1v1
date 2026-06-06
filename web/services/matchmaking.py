import json
import time
import redis
from django.conf import settings

r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)

QUEUE_KEY = "matchmaking:queue"
MATCH_KEY_PREFIX = "matchmaking:match:"
ATTEMPTS_KEY_PREFIX = "matchmaking:attempts:"
LOCK_NAME = "matchmaking:lock"

BASE_RANGE = 100
RANGE_INCREMENT = 50

def join_queue(user_id, score):
    user_id = str(user_id)
    with r.lock(LOCK_NAME, timeout=5):
        # 1. Check if already matched
        match_data = r.get(f"{MATCH_KEY_PREFIX}{user_id}")
        if match_data:
            return json.loads(match_data)

        # 2. Get current attempts to calculate range
        attempts = int(r.get(f"{ATTEMPTS_KEY_PREFIX}{user_id}") or 0)
        effective_range = BASE_RANGE + (attempts * RANGE_INCREMENT)

        # 3. Search for compatible players in the queue
        # We look for players with score between [score - effective_range, score + effective_range]
        potential_matches = r.zrangebyscore(QUEUE_KEY, score - effective_range, score + effective_range)
        
        # Filter out self if somehow present
        potential_matches = [m for m in potential_matches if m != user_id]

        if potential_matches:
            # Found a match! (Take the first one)
            opponent_id = potential_matches[0]
            
            # Remove both from queue
            r.zrem(QUEUE_KEY, user_id, opponent_id)
            
            # Create match records
            match_info = {
                "opponent_id": opponent_id,
                "status": "matched",
                "timestamp": time.time()
            }
            
            # Opponent match info
            opponent_match_info = {
                "opponent_id": user_id,
                "status": "matched",
                "timestamp": time.time()
            }
            
            r.set(f"{MATCH_KEY_PREFIX}{user_id}", json.dumps(match_info), ex=60)
            r.set(f"{MATCH_KEY_PREFIX}{opponent_id}", json.dumps(opponent_match_info), ex=60)
            
            # Clear attempts
            r.delete(f"{ATTEMPTS_KEY_PREFIX}{user_id}")
            r.delete(f"{ATTEMPTS_KEY_PREFIX}{opponent_id}")
            
            return match_info
        
        # 4. No match found, add to queue
        r.zadd(QUEUE_KEY, {user_id: score})
        return {"status": "searching"}

def get_status(user_id):
    user_id = str(user_id)
    
    # 1. Check if matched
    match_data = r.get(f"{MATCH_KEY_PREFIX}{user_id}")
    if match_data:
        return json.loads(match_data)
    
    # 2. Check if in queue
    score = r.zscore(QUEUE_KEY, user_id)
    if score is not None:
        return {"status": "searching"}
    
    # 3. Not in queue and not matched -> maybe timed out or never joined
    return {"status": "idle"}

def cancel_queue(user_id):
    user_id = str(user_id)
    r.zrem(QUEUE_KEY, user_id)
    r.delete(f"{ATTEMPTS_KEY_PREFIX}{user_id}")

def update_match_url(user_id, match_url):
    user_id = str(user_id)
    match_data = r.get(f"{MATCH_KEY_PREFIX}{user_id}")
    if match_data:
        data = json.loads(match_data)
        data["match_url"] = match_url
        # Keep same expiry
        ttl = r.ttl(f"{MATCH_KEY_PREFIX}{user_id}")
        if ttl > 0:
            r.set(f"{MATCH_KEY_PREFIX}{user_id}", json.dumps(data), ex=ttl)
            
            # Also update for the opponent so they don't call the API again
            opponent_id = data.get("opponent_id")
            if opponent_id:
                opp_match_data = r.get(f"{MATCH_KEY_PREFIX}{opponent_id}")
                if opp_match_data:
                    opp_data = json.loads(opp_match_data)
                    opp_data["match_url"] = match_url
                    r.set(f"{MATCH_KEY_PREFIX}{opponent_id}", json.dumps(opp_data), ex=ttl)
