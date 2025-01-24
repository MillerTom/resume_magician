from django.core.management.base import BaseCommand
from django.conf import settings
from scraper.models import ScrapeHistory, JobBoardResult
from scraper.utils import CustomApifyClient, get_datetime
from scraper.tasks import run_actor


class Command(BaseCommand):
    help = 'Check Scraper History Periodically'

    def handle(self, *args, **kwargs):
        histories = ScrapeHistory.objects.filter(is_done=False).all()
        for history in histories:
            try:
                configuration = history.configuration
                scraper = configuration.scraper
                actor_id = scraper.actor_id
                apify_client = CustomApifyClient(settings.APIFY_API_KEY, actor_id)

                # Retry with modified number_of_days
                jobs = apify_client.client.dataset(history.dataset_id).iterate_items()
                number_of_jobs = 0

                # Save job
                for job in jobs:
                    number_of_jobs += 1
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

                    new_job_result = JobBoardResult(
                        configuration=configuration,
                        job_title=job_title,
                        job_description=job_description,
                        source=history.job_board,
                        skill=configuration.skill,
                        date_scraped=history.started_at,
                        run_id=history.run_id,
                        date_job_posted = get_datetime(job_posted_days_ago),
                        salary=salary,
                        job_type=job_type,
                        company=company,
                        location=location,
                        job_url=job_url,
                        is_easyapply= True if apply_params.get('isZipApply') else False,
                        external_apply_url=external_apply_url,
                    )      
                    new_job_result.save()

                if history.status != 'SUCCEEDED' or number_of_jobs == 0:
                    print("Failed: ", history.id)
                    if history.days == history.configuration.days:
                        run_actor(scraper, configuration, configuration.days + 1)
                else:
                    history.number_of_jobs = number_of_jobs
                    print("Succeed: ", history.id)
                history.is_done = True
                history.save()
            except Exception as err:
                print(f'Error: {str(err)}')