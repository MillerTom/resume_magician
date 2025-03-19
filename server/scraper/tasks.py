from scraper.models import ApifyKey, ScrapeHistory
from scraper.utils import CustomApifyClient


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
        print("=== actor_id: ", actor_id)
        apify_key = ApifyKey.objects.first()
        APIFY_API_KEY = apify_key.value
        apify_client = CustomApifyClient(APIFY_API_KEY, actor_id)
        response = apify_client.start_actor(payload)
        print(f'DatasetId: {response["defaultDatasetId"]}')

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
            finished_at=response['finishedAt'],
            run_id=response['id'],
            dataset_id=response['defaultDatasetId'],
            job_board=scraper.name,
            days=configuration.days if days == -1 else days,
            status=response['status'],
            input_json=payload,
            run_time=response['stats']['runTimeSecs'],
            price=price,
        )
        history.save()
    except Exception as err:
        print(f'=== run_actor error: {str(err)}')