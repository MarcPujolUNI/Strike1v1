from datetime import timedelta
from django.utils import timezone
from web.models import Match

LOGS_DAYS = 30
def clean_old_match_logs():
    cutoff = timezone.now() - timedelta(days=LOGS_DAYS)
    matches = Match.objects.filter(date__lt=cutoff, log_file__isnull=False)

    for match in matches:
        if match.log_file:
            match.log_file.delete(save=False)
        match.log_file = None
        match.save()