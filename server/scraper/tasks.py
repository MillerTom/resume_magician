from django.conf import settings
from scraper.models import JobBoardResult, ScrapeHistory
from scraper.utils import CustomApifyClient


def run_actor(scraper, configuration, days=-1):
    actor_id = scraper.actor_id
    number_of_days = configuration.days if days == -1 else days
    url = configuration.url
    url = url.replace('days=1', 'days=%s' % number_of_days) if 'days' in url else url
    payload = {
        'startUrls': [{'url': url, 'method': 'GET'}],
        'maxItems': 100,
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
        apify_client = CustomApifyClient(settings.APIFY_API_KEY, actor_id)
        response = apify_client.start_actor(payload)
        print(f'DatasetId: {response["defaultDatasetId"]}')

        history = ScrapeHistory(
            configuration=configuration,
            finished_at=response['finishedAt'],
            run_id=response['id'],
            dataset_id=response['defaultDatasetId'],
            job_board=scraper.name,
            days=configuration.days if days == -1 else days,
            status=response['status'],
            input_json=payload,
            run_time=response['stats']['runTimeSecs'],
            price=response['usageTotalUsd'],
        )
        history.save()
    except Exception as err:
        print(f'=== run_actor error: {str(err)}')