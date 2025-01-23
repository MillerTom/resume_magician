from django.core.management.base import BaseCommand
import time
from django.conf import settings
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from job.utils import execute_gviz_query

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(settings.CREDENTIALS_PATH, scope)
client = gspread.authorize(creds)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = settings.SPREAD_SHEET_ID
jobUrlColumnIndex = settings.JOB_URL_COLUMN_INDEX
lockColumnIndex = settings.LOCK_COLUMN_INDEX
startedAtColumnIndex = settings.STARTED_AT_COLUMN_INDEX
appliedForDateColumnIndex = settings.APPLIED_FOR_DATE_COLUMN_INDEX

class Command(BaseCommand):
    help = 'Runs a task periodically'

    def handle(self, *args, **kwargs):
        # while True:
        now = int(time.time())
        print(f"Running task {str(now)}")
        QUERY = (
            "SELECT AB, AG "
            "WHERE AA = '1'"
        )
        data = execute_gviz_query(QUERY)
        sheet = client.open(settings.GOOGLE_SHEET_NAME).get_worksheet_by_id(settings.SHEET_ID)
        for row in data['table']['rows']:
            started_at = row['c'][0]['v']
            started_at = int(started_at)
            now = int(time.time())
            if now - int(row[lockColumnIndex - 1]) > 3600:
                row_index = int(row['c'][1]['v'])
                sheet.update_cell(row_index, lockColumnIndex, '')
                sheet.update_cell(row_index, startedAtColumnIndex, '')
            # time.sleep(1800)