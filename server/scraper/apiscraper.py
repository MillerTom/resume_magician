
from apify_client import ApifyClient
from datetime import datetime, timedelta
import pytz

class ApiScraper:
    def __init__(self, worker=None, apiToken=None):
        print(f'ApiScraper: init')
        if worker != None:
            self.scraper = worker.scraper
            self.configurations = list(worker.configurations)        
            self.actorId = self.scraper.ActorID
            self.serializer = worker.serializer
        else:
            self.scraper = None
            self.configurations = None
            self.actorId = None
            self.serializer = None

        self.apifyClient = ApifyClient(apiToken)
        self.apiToken = apiToken

    def run(self):
        for configuration in self.configurations:
            self.runConfig(configuration)
        return

    def runConfig(self, configuration):
        numberOfDays = 1
        url = configuration.Url
        url = url.replace('days=1', 'days=%s' % numberOfDays) if 'days' in url else url
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
            print(f'ApiScraper: apifyClient.actor.call start time = {datetime.now(pytz.utc)}')
            print(f'ApiScraper: call url = {url}')
            response = self.apifyClient.actor(self.actorId).call(run_input=payload)
            print(f'ApiScraper: apifyClient.actor.call end time = {datetime.now(pytz.utc)}')
            print(f'ApiScraper: DatasetId = {response["defaultDatasetId"]}')
            
            jobs = list(self.apifyClient.dataset(response["defaultDatasetId"]).iterate_items())
            print(f'ApiScraper: response jobs count = {len(jobs)}')

            if self.serializer != None:
                self.serializer.save(configuration, response, jobs, payload)
            
        except Exception as err:
            print(f'ApiScraper: runConfig Exception error: {str(err)}')
            
            return
     