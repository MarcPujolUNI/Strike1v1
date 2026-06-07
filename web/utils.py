from datetime import timedelta
from django.utils import timezone
from web.models import Match
from math import exp

LOGS_DAYS = 30
def clean_old_match_logs():
    cutoff = timezone.now() - timedelta(days=LOGS_DAYS)
    matches = Match.objects.filter(date__lt=cutoff, log_file__isnull=False)

    for match in matches:
        if match.log_file:
            match.log_file.delete(save=False)
    matches.update(log_file=None)

def score(winner_rating, loser_rating):
    diff = winner_rating - loser_rating
    surprise = 1 / (1 + exp(diff / 500))
    avg = (winner_rating + loser_rating) / 2
    progression = 3.0 / (1 + avg / 800)
    winner_gain = BASE * progression * (0.6 + 2.4 * surprise)
    loser_loss = BASE * progression * (0.4 + 2.8 * surprise)
    return round(winner_gain), -round(loser_loss)