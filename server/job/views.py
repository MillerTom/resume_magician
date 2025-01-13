from rest_framework.response import Response
from rest_framework import generics, status as http_status
from django.conf import settings
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from auth.utils import is_authenticated
from job.models import UserInfo, Job
from datetime import datetime
import time

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(settings.CREDENTIALS_PATH, scope)
client = gspread.authorize(creds)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = settings.SPREAD_SHEET_ID

jobUrlColumnIndex = settings.JOB_URL_COLUMN_INDEX
lockColumnIndex = settings.LOCK_COLUMN_INDEX
startedAtColumnIndex = settings.STARTED_AT_COLUMN_INDEX
appliedForDateColumnIndex = settings.APPLIED_FOR_DATE_COLUMN_INDEX


class GetJobRecordsView(generics.GenericAPIView):
    @is_authenticated
    def post(self, request):
        sheet = client.open(settings.GOOGLE_SHEET_NAME).get_worksheet_by_id(settings.SHEET_ID)
        data = sheet.get_all_values()
        df = pd.DataFrame(data[1:], columns=data[0])
        df = df.fillna('')
        df = df[(df['AppliedForDate'] == '') & (df['Lock'] == '') & (df['Easy Apply'] != 'TRUE')]

        backlog = {}
        skills = df['Skill'].tolist()
        skills = list(set(skills))
        for skill in skills:
            backlog[skill] = len(df[df['Skill'] == skill])
        df.sort_values(by='Priority', ascending=True, inplace=True)
        current_job = df.iloc[0].to_dict()
        job = {
            'jobTitle': current_job['JobTitle'],
            'jobUrl': current_job['URL to Apply'],
            'datePosted': current_job['Posted At'],
            'resume': current_job['Customized Resume']
        }

        # jobs = Job.objects.all()
        # for job in jobs:
        #     print(job.user)

        leaderboard = []
        userinfos = UserInfo.objects.all()
        for userinfo in userinfos:
            jobs = Job.objects.filter(user=userinfo).all()
            leaderboard.append({
                'name': userinfo.name,
                'email': userinfo.email,
                'num_applied_jobs': len(jobs),
            })

        # jobs = []
        # for index, row in df.iterrows():
        #     jobs.append({
        #         'id': index,
        #         'jobTitle': row['JobTitle'],
        #         'datePosted': row['Posted At'],
        #         'resume': row['Customized Resume'],
        #     })
        return Response({'job': job, 'backlog': backlog, 'leaderboard': leaderboard}, status=http_status.HTTP_200_OK)


class JobApplyStartView(generics.GenericAPIView):
    @is_authenticated
    def post(self, request):
        data = request.data
        job_url = data['jobUrl']
        now = int(time.time())

        sheet = client.open(settings.GOOGLE_SHEET_NAME).get_worksheet_by_id(settings.SHEET_ID)
        data = sheet.get_all_values()
        jobIndex = -1
        for row_index, row in enumerate(data, start=1):
            if row[jobUrlColumnIndex] == job_url:
                jobIndex = row_index
                if str(row[lockColumnIndex - 1]) == '1':
                    return Response({'msg': 'Job Locked'}, status=http_status.HTTP_403_FORBIDDEN)
                sheet.update_cell(row_index, lockColumnIndex, '1')
                sheet.update_cell(row_index, startedAtColumnIndex, str(now))
                break
        if jobIndex >= 0:
            return Response({'jobIndex': jobIndex}, status=http_status.HTTP_200_OK)
        else:
            return Response({'msg': 'Selected job not found'}, status=http_status.HTTP_404_NOT_FOUND)


class JobAppliedView(generics.GenericAPIView):
    @is_authenticated
    def post(self, request):
        data = request.data
        email = data['email']
        job_url = data['jobUrl']
        job_index = data['jobIndex']
        userinfo = UserInfo.objects.filter(email=email).first()
        job = Job.objects.filter(user=userinfo, url=job_url).first()
        if not job:
            job = Job(
                user=userinfo,
                url=job_url,
                applied_at=datetime.now()
            )
            job.save()
        sheet = client.open(settings.GOOGLE_SHEET_NAME).get_worksheet_by_id(settings.SHEET_ID)
        sheet.update_cell(job_index, lockColumnIndex, '')
        sheet.update_cell(job_index, startedAtColumnIndex, '')
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.update_cell(job_index, appliedForDateColumnIndex, now)
        return Response(status=http_status.HTTP_200_OK)