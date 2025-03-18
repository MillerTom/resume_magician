from django.core.management.base import BaseCommand
from scraper.models import Scraper
from scraper.tasks import run_actor

class Command(BaseCommand):
    help = 'Run Scrapers Based On Configurations'

    def handle(self, *args, **kwargs):
        print("*** Running Scrapers ***")
        scrapers = Scraper.objects.filter(is_active=True)
        for scraper in scrapers:
            configurations = scraper.scraper_configurations.filter(is_active=True)
            for configuration in configurations:
                print("* Running Configuration: ", configuration.url)
                run_actor(scraper, configuration)