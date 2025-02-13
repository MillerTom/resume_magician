from django.core.management.base import BaseCommand
from scraper.work import Worker

class Command(BaseCommand):
    help = 'this is command to scrape'

    def add_arguments(self, parser):
        # Optional: Add any command-line arguments here
        parser.add_argument('name', type=str, help='scraper name')

    def handle(self, *args, **kwargs):
        # The main logic of your command goes here
        name = kwargs['name']
        self.stdout.write(self.style.SUCCESS(f'command = {name}!'))

        scrapeWork = Worker(name)
        scrapeWork.run()

