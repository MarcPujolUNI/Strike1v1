from django.core.management.base import BaseCommand
from web.models import Country

class Command(BaseCommand):
    help = "Populates missing flag images"

    def add_arguments(self, parser):
        parser.add_argument('--replace', action='store_true', help="Replace existing flags")
        parser.add_argument('--country', nargs='+', type=str, help="Only add specific countries' flag")

    def handle(self, *args, **kwargs):
        replace = kwargs.get('replace', None)
        countries = kwargs.get('country', None)
        if not countries:
            countries = Country.objects.all()
        else:
            countries = Country.objects.filter(name__in=countries)
        for country in countries:
            if replace or not country.flag_image:
                if country.flag_image: country.flag_image.delete(save=False)
                country.flag_image = None
                country.get_flag_image()
        self.stdout.write(self.style.SUCCESS("Flags populated"))