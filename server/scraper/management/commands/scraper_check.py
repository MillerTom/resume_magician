from django.core.management.base import BaseCommand
from django.db.models import Q
from scraper.models import ScrapeHistory
from scraper.tasks import run_checker, run_qualifier, run_resume_maker
from scraper.utils import logger
from setting.models import SupervisorStatus


SUCCEED_STATUS = 'SUCCEEDED'

class Command(BaseCommand):
    help = 'Check Scraper History Periodically'

    def handle(self, *args, **kwargs):
        logger.info('*** Running Scraper Check ***')
        supervisor_status = SupervisorStatus.objects.first()
        print("==========", supervisor_status.is_locked)
        if supervisor_status.is_locked: return
        supervisor_status.is_locked = True
        supervisor_status.save()

        histories = ScrapeHistory.objects.filter(~Q(status=SUCCEED_STATUS)).all()
        for history in histories:
            try:
                logger.info(f'* Scrape Check: {history.configuration.url} - {history.configuration.scraper.name}')
                run_checker(history)
            except Exception as err:
                logger.error(f'Run Scraper Records Error: {str(err)}')

        histories = ScrapeHistory.objects.filter(status=SUCCEED_STATUS, is_done=False).all()
        for history in histories:
            try:
                logger.info(f'* Qualification: {history.run_id}')
                run_qualifier(history.run_id)
                history.is_done = True
                history.save()
            except Exception as err:
                logger.error(f'Run Qualifications Error: {str(err)}')

        for history in histories:
            try:
                logger.info(f'* ResumeMaker: {history.run_id}')
                run_resume_maker(history.run_id)
            except Exception as err:
                logger.error(f'Run ResumeMaker Error: {str(err)}')

        supervisor_status.is_locked = False
        supervisor_status.save()