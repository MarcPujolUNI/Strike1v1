from django.core.management.base import BaseCommand
from web.utils import clean_old_match_logs

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        clean_old_match_logs()
        self.stdout.write(self.style.SUCCESS("Old logs cleaned"))