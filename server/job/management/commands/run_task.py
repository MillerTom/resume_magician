from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Q
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from job.utils import execute_gviz_query, logger
from scraper.models import JobBoardResult

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(settings.CREDENTIALS_PATH, scope)
client = gspread.authorize(creds)
service = build('sheets', 'v4', credentials=creds)
lockColumnIndex = settings.LOCK_COLUMN_INDEX
startedAtColumnIndex = settings.STARTED_AT_COLUMN_INDEX
UNLOCK_SECONDS = 3600

class Command(BaseCommand):
    help = 'Runs a task periodically'

    def handle(self, *args, **kwargs):
        # Check Google Sheet
        rows = []
        now = int(time.time())
        logger.info(f"*** Running task to check jobs ***")
        QUERY = (
            "SELECT AB, AG "
            "WHERE AA = 1"
        )
        data = execute_gviz_query(QUERY)

        rows.extend(data['table']['rows'])
        QUERY = (
            "SELECT AB, AG "
            "WHERE AA = '1'"
        )
        data = execute_gviz_query(QUERY)
        rows.extend(data['table']['rows'])
        logger.info(f'fetched {len(rows)}')

        sheet = client.open(settings.GOOGLE_SHEET_NAME).get_worksheet_by_id(settings.SHEET_ID)
        for row in data['table']['rows']:
            try:
                started_at = row['c'][0]['v']
                started_at = int(started_at)
                row_i = int(row['c'][1]['v'])
                logger.info(f'{started_at} {row_i}')
                if now - started_at > UNLOCK_SECONDS:
                    row_index = int(row['c'][1]['v']) + 1
                    sheet.update_cell(row_index, lockColumnIndex, '')
                    sheet.update_cell(row_index, startedAtColumnIndex, '')
                    time.sleep(1)
            except Exception as err:
                logger.error(f'error in google sheet: {str(err)}')

        # Check PostgreSQL database
        jobs = JobBoardResult.objects.filter(
            Q(date_applied_for=None),
            ~Q(date_apply_started=None)
        ).all()
        now = int(time.time())
        for job in jobs:
            try:
                if now - int(job.date_apply_started.timestamp()) > UNLOCK_SECONDS:
                    job.date_apply_started = None
                    job.lock_application = False
                    job.save()
                    logger.info(f'unlock job: {str(job.id)}')
            except Exception as err:
                logger.error(f'error in database: {str(err)}')