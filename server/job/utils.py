import requests
import json
from django.conf import settings
from django.db.models import Q, F
from setting.utils import is_google_sheet
from scraper.models import JobBoardResume

def execute_gviz_query(query):
    SHEET_ID = settings.SPREAD_SHEET_ID
    WORKSHEET_ID = settings.SHEET_ID
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?"
    params = { 'tq': query, 'tqx': 'out:json', 'gid': WORKSHEET_ID }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        raw_data = response.text.lstrip("/*O_o*/\ngoogle.visualization.Query.setResponse(").rstrip(");")
        data = json.loads(raw_data)
        return data

    except Exception as e:
        print(f"Error executing gViz query: {e}")
        return None
    

def get_job():
    if is_google_sheet():
        QUERY = (
            "SELECT A, B, I, N, O "
            "WHERE (X IS NULL OR X != TRUE) AND "
            "N != '' AND "
            "(Q = '' OR Q IS NULL) AND "
            "(AA != 'locked' OR AA IS NULL) AND "
            "(AD = '' OR AD IS NULL) AND "
            "(AF = '' OR AF IS NULL) "
            "ORDER BY E "
            "LIMIT 1"
        )
        data = execute_gviz_query(QUERY)
        return {
            'jobTitle':         data['table']['rows'][0]['c'][0]['v'],
            'jobDescription':   data['table']['rows'][0]['c'][1]['v'],
            'datePosted':       data['table']['rows'][0]['c'][2]['v'],
            'jobUrl':           data['table']['rows'][0]['c'][3]['v'],
            'resume':           data['table']['rows'][0]['c'][4]['v'],
        }
    else:
        job_board_resume = JobBoardResume.objects.filter(
            Q(is_easyapply=False) &
            ~Q(job_url=None) &
            ~Q(customized_resume_url=None) &
            Q(date_applied_for=None) &
            Q(lock_application=False) &
            Q(date_job_removed_from_site=None) &
            Q(problem_applying_description='')
        ).annotate(
            config_priority=F('configuration__priority')
        ).order_by(
            'config_priority'
        ).first()
        return {
            'jobTitle':         job_board_resume.job_title,
            'jobDescription':   job_board_resume.job_description,
            'datePosted':       job_board_resume.date_job_posted,
            'jobUrl':           job_board_resume.job_url,
            'resume':           job_board_resume.customized_resume_url,
        }


def get_bot_jobs(source):
    jobs = []
    if is_google_sheet():
        QUERY = (
            "SELECT A, B, I, N, O, AG "
            "WHERE X = TRUE AND "
            f"C = '{source}' AND "
            "N != '' AND "
            "(Q = '' OR Q IS NULL) AND "
            "(AA != 'locked' OR AA IS NULL) AND "
            "(AD = '' OR AD IS NULL) AND "
            "(AF = '' OR AF IS NULL) "
            "ORDER BY E "
            "LIMIT 10"
        )
        data = execute_gviz_query(QUERY)
        for job_row in data['table']['rows']:
            jobs.append(
                {
                    'id':               job_row['c'][5]['v'],
                    'jobTitle':         job_row['c'][0]['v'],
                    'jobDescription':   job_row['c'][1]['v'],
                    'datePosted':       job_row['c'][2]['v'],
                    'jobUrl':           job_row['c'][3]['v'],
                    'resume':           job_row['c'][4]['v'],
                }
            )
    else:
        job_board_resumes = JobBoardResume.objects.filter(
            Q(is_easyapply=True) &
            ~Q(job_url=None) &
            ~Q(customized_resume_url=None) &
            Q(date_applied_for=None) &
            Q(lock_application=False) &
            Q(date_job_removed_from_site=None) &
            Q(problem_applying_description='') &
            Q(source=source)
        ).annotate(
            config_priority=F('configuration__priority')
        ).order_by(
            'config_priority'
        )[:10]
        print(job_board_resumes)
        for job_board_resume in job_board_resumes:
            jobs.append({
                'id':               job_board_resume.id,
                'jobTitle':         job_board_resume.job_title,
                'jobDescription':   job_board_resume.job_description,
                'datePosted':       job_board_resume.date_job_posted,
                'jobUrl':           job_board_resume.job_url,
                'resume':           job_board_resume.customized_resume_url,
            })
    return jobs