from django.core.management.base import BaseCommand
from dateutil import parser
from datetime import datetime
from scraper.models import ScrapeHistory, JobBoardResult, ApifyKey
from scraper.utils import CustomApifyClient, get_datetime, is_valid_email
from scraper.tasks import run_actor


class Command(BaseCommand):
    help = 'Check Scraper History Periodically'

    def handle(self, *args, **kwargs):
        print('*** Running Scraper Check ***')
        apify_key = ApifyKey.objects.first()
        APIFY_API_KEY = apify_key.value
        histories = ScrapeHistory.objects.filter(is_done=False).all()
        for history in histories:
            try:
                configuration = history.configuration
                scraper = configuration.scraper
                print(f'* Configuration: {configuration.url} - {scraper.name}')
                actor_id = scraper.actor_id
                apify_client = CustomApifyClient(APIFY_API_KEY, actor_id)

                # Retry with modified number_of_days
                jobs = apify_client.client.dataset(history.dataset_id).iterate_items()
                number_of_jobs = 0

                # Save job
                for job in jobs:
                    number_of_jobs += 1
                    if configuration.scraper.name.lower() == 'ziprecruiter':
                        job_title = job.get('Title', '')
                        job_description = job.get('description', '')
                        salary = job.get('FormattedSalaryShort', '')
                        job_type = job.get('EmploymentType', '')
                        company = job.get('OrgName', '')
                        location = (
                            job.get('jobDetails', {})
                            .get('model', {})
                            .get('gtmData', {})
                            .get('JobLocation', '')
                        )
                        job_posted_days_ago = job.get('FirstSeenDaysAgo', 0)
                        job_url = job.get('Href', '')
                        apply_params = job.get('jobDetails', {}).get('model', {}).get('applyParams', {})
                        if apply_params.get('isExternalApply'):
                            external_apply_url = apply_params.get('externalApplyUrl')
                        else:
                            external_apply_url = None
                        is_easyapply = True if apply_params.get('isZipApply') else False
                        date_job_posted = get_datetime(job_posted_days_ago)
                    elif configuration.scraper.name.lower() == 'indeed':
                        job_title = job.get('positionName', '')
                        job_description = job.get('description', '')
                        salary = job.get('salary', '')
                        job_type = ', '.join(job.get('jobType', []))
                        company = job.get('company', '')
                        location = job.get('location', '')
                        job_url = job.get('url', '')
                        external_apply_url = job.get('externalApplyLink', None)
                        is_easyapply = True if external_apply_url else False
                        postingDateParsed = job.get('postingDateParsed', '')
                        date_job_posted = parser.parse(postingDateParsed) if postingDateParsed else parser.parse(datetime.now())
                    elif configuration.scraper.name.lower() == 'dice':
                        job_title = job.get('title', '')
                        job_description = job.get('description', '')
                        salaryRaw = job.get('salaryRaw', '')
                        salaryRawUnit = job.get('salaryRawUnit', '')
                        salary = f'{salaryRaw} {salaryRawUnit}'
                        job_type = job.get('contractType', '')
                        company = job.get('companyName', '')
                        location = job.get('location', '')
                        job_url = job.get('url', '')
                        external_apply_url = job.get('applyUrl', None)
                        if external_apply_url and is_valid_email(external_apply_url):
                            is_easyapply = True
                        else:
                            is_easyapply = False
                        postingDateParsed = job.get('datePosted', '')
                        date_job_posted = parser.parse(postingDateParsed) if postingDateParsed else parser.parse(datetime.now())
                    elif configuration.scraper.name.lower() == 'linkedin':
                        job_title = job.get('title', '')
                        job_description = job.get('description', '')
                        salary = job.get('salary', '')
                        job_type = job.get('contractType', '')
                        company = job.get('companyName', '')
                        location = job.get('location', '')
                        job_url = job.get('jobUrl', '')
                        is_easyapply = True if job.get('applyType', '') == 'EASY_APPLY' else False
                        external_apply_url = job.get('applyUrl', None)
                        postingDateParsed = job.get('publishedAt', '')
                        date_job_posted = parser.parse(postingDateParsed) if postingDateParsed else parser.parse(datetime.now())

                    # Check if same job is already scraped and added to database.
                    new_job_result = JobBoardResult.objects.filter(job_url=job_url).first()
                    if new_job_result:
                        print('Job duplicated', job_url)
                        continue
                    new_job_result = JobBoardResult(
                        configuration=configuration,
                        job_title=job_title,
                        job_description=job_description,
                        source=history.job_board,
                        skill=configuration.skill,
                        date_scraped=history.started_at,
                        run_id=history.run_id,
                        date_job_posted=date_job_posted,
                        salary=salary,
                        job_type=job_type,
                        company=company,
                        location=location,
                        job_url=job_url,
                        is_easyapply=is_easyapply,
                        external_apply_url=external_apply_url,
                    )
                    new_job_result.save()

                if history.status != 'SUCCEEDED' or number_of_jobs == 0:
                    print('Failed: ', history.id)
                    if history.days == history.configuration.days:
                        run_actor(scraper, configuration, configuration.days + 1)
                else:
                    history.number_of_jobs = number_of_jobs
                    print('Succeed: ', history.id)
                history.is_done = True
                history.save()
            except Exception as err:
                print(f'Error: {str(err)}')