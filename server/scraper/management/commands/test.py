from django.core.management.base import BaseCommand
from scraper.models import Scraper
from scraper.tasks import run_actor


class Command(BaseCommand):
    help = 'Scraper Tests'

    def handle(self, *args, **kwargs):
        print('========== Scraper Tests ==========')
        scrapers = Scraper.objects.filter(is_active=True)

        for i, scraper in enumerate(scrapers):
            print(f'{i + 1}. {scraper.name}')

            configurations = scraper.scraper_configurations.filter(is_active=True)
            for j, configuration in enumerate(configurations):
                print(f'{j + 1}) {configuration.skill}')

                run_actor(scraper, configuration)