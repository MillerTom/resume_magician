from django.core.management.base import BaseCommand
from django.db.models import Q
from scraper.models import ScrapeHistory
from scraper.tasks import run_checker, run_qualifier, run_resume_maker
from resume.models import BaseResume


SUCCEED_STATUS = 'SUCCEEDED'

class Command(BaseCommand):
    help = 'Check Scraper History Periodically'

    def handle(self, *args, **kwargs):
        print('*** Running Scraper Check ***')
        histories = ScrapeHistory.objects.filter(~Q(status=SUCCEED_STATUS)).all()
        for history in histories:
            try:
                print(f'* Scrape Check: {history.configuration.url} - {history.configuration.scraper.name}')
                run_checker(history)
            except Exception as err:
                print(f'Run Scraper Records Error: {str(err)}')

        histories = ScrapeHistory.objects.filter(status=SUCCEED_STATUS, is_done=False).all()
        for history in histories:
            try:
                print(f'* Qualification: {history.run_id}')
                run_qualifier(history.run_id)
                history.is_done = True
                history.save()
            except Exception as err:
                print(f'Run Qualifications Error: {str(err)}')

        for history in histories:
            try:
                print(f'* ResumeMaker: {history.run_id}')
                run_resume_maker(history.run_id)
            except Exception as err:
                print(f'Run ResumeMaker Error: {str(err)}')