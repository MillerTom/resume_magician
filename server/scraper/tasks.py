from dateutil import parser
from datetime import datetime
import openai
import json
from scraper.models import ApifyKey, ScrapeHistory, JobBoardResult, JobBoardResume
from scraper.utils import CustomApifyClient, get_datetime, is_valid_email, logger
from resume.utils import analyze_job, determine_base_resume, create_new_doc
from resume.models import BaseResume


SUCCEED_STATUS = 'SUCCEEDED'


def run_actor(scraper, configuration, days=-1):
    actor_id = scraper.actor_id
    number_of_days = configuration.days if days == -1 else days
    url = configuration.url
    if url:
        url = url.replace('days=1', 'days=%s' % number_of_days) if 'days' in url else url
        payload = {
            'startUrls': [{'url': url, 'method': 'GET'}],
            'maxItems': 100,
            'rowNumber': 100,
            'maxConcurrency': 10,
            'minConcurrency': 1,
            'maxRequestRetries': 30,
            'proxy': {
                'useApifyProxy': True,
                'apifyProxyGroups': ['RESIDENTIAL'],
                'apifyProxyCountry': 'US',
            },
        }
    else:
        payload = {
            'title': configuration.skill,
            'location': 'United States',
            'workplaceType': ['remote'],
            'maxItems': 100,
            'rowNumber': 100,
            'maxConcurrency': 10,
            'minConcurrency': 1,
            'maxRequestRetries': 30,
            'proxy': {
                'useApifyProxy': True,
                'apifyProxyGroups': ['RESIDENTIAL'],
                'apifyProxyCountry': 'US',
            },
        }

    try:
        logger.info(f"actor_id: {actor_id}")
        apify_key = ApifyKey.objects.first()
        APIFY_API_KEY = apify_key.value
        apify_client = CustomApifyClient(APIFY_API_KEY, actor_id)
        response = apify_client.start_actor(payload)
        logger.info(f'DatasetId: {response["defaultDatasetId"]}')

        if scraper.name.lower() == 'ziprecruiter':
            price = response['usageTotalUsd']
        elif scraper.name.lower() == 'indeed':
            price = response['pricingInfo']['pricePerUnitUsd']
        elif scraper.name.lower() == 'dice':
            price = response['usageTotalUsd']
        elif scraper.name.lower() == 'linkedin':
            price = response['usageTotalUsd']

        history = ScrapeHistory(
            configuration=configuration,
            run_id=response['id'],
            job_board=scraper.name,
            days=configuration.days if days == -1 else days,
            status=response['status'],
            input_json=payload,
            price=price,
        )
        history.save()
    except Exception as err:
        logger.error(f'run_actor error: {str(err)}')


def run_checker(history):
    apify_key = ApifyKey.objects.first()
    APIFY_API_KEY = apify_key.value
    configuration = history.configuration
    scraper = configuration.scraper
    actor_id = scraper.actor_id
    apify_client = CustomApifyClient(APIFY_API_KEY, actor_id)

    run_status = apify_client.client.run(history.run_id).get()
    if run_status['status'] == SUCCEED_STATUS:
        history.status = run_status['status']
        history.finished_at=run_status['finishedAt']
        history.run_time=run_status['stats']['runTimeSecs']
        history.dataset_id=run_status['defaultDatasetId']
        history.save()
    else:
        return

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
            logger.info('Job duplicated', job_url)
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

    # if history.status != SUCCEED_STATUS or number_of_jobs == 0:
    if number_of_jobs == 0:
        logger.info(f'Failed: {history.id}')
        if history.days == history.configuration.days:
            # Retry with modified number_of_days
            run_actor(scraper, configuration, configuration.days + 1)
    else:
        history.number_of_jobs = number_of_jobs
        logger.error(f'Succeed: {history.id} with ({number_of_jobs}jobs)')


def run_qualifier(run_id):
    priority = 1
    while priority <= 20:
        job_board_results = JobBoardResult.objects.filter(run_id=run_id, configuration__priority=priority, is_qualified=None).all()
        history = ScrapeHistory.objects.filter(run_id=run_id).first()
        for job_board_result in job_board_results:
            try:
                is_qualified = analyze_job(job_board_result.job_title, job_board_result.job_description)
                job_board_result.is_qualified = is_qualified
                job_board_result.save()
                if is_qualified:
                    job_board_resume = JobBoardResume(
                        configuration=job_board_result.configuration,
                        job_title=job_board_result.job_title,
                        job_description=job_board_result.job_description,
                        source=history.job_board,
                        skill=job_board_result.configuration.skill,
                        date_scraped=history.started_at,
                        run_id=run_id,
                        date_job_posted=job_board_result.date_job_posted,
                        salary=job_board_result.salary,
                        job_type=job_board_result.job_type,
                        company=job_board_result.company,
                        location=job_board_result.location,
                        job_url=job_board_result.job_url,
                        is_easyapply=job_board_result.is_easyapply,
                        external_apply_url=job_board_result.external_apply_url,
                    )
                    job_board_resume.save()
            except Exception as err:
                logger.error(f'run_qualifier error: {str(err)}')
        priority += 1


def run_resume_maker(run_id):
    thread = openai.beta.threads.create()
    thread_id = thread.id
    job_board_resumes = JobBoardResume.objects.filter(run_id=run_id, customized_resume_url=None).all()
    for job_board_resume in job_board_resumes:
        try:
            # Run OpenAI Assistant based on Vector Store
            result = determine_base_resume(thread_id, job_board_resume.job_title, job_board_resume.job_description)
            job_board_resume.ai_response_job_analyzer = json.dumps(result)
            if not result: continue

            # Find Base Resume based on AI Response
            base_file_name = result['BaseResumeFilename']
            base_resume = BaseResume.objects.extra(
                where=["%s LIKE CONCAT('%%', keyword, '%%')"],
                params=[base_file_name]
            ).first()
            generated_title = result['JobTitle']
            generated_experience = result['ExperienceGenerated']

            # Recreate Resume using Base Resume
            customized_resume_url = create_new_doc(base_resume.google_doc_id, generated_title, generated_experience)
            job_board_resume.customized_resume_url = customized_resume_url
            job_board_resume.save()
        except Exception as err:
            logger.error(f'run_resume_maker error: {str(err)}')