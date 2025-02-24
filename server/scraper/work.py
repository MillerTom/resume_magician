from scraper.models import ApifyKey, Scraper, configdice, configindeed, configlinkedin, configziprecruiter
from scraper.models import jobboardscraperesults, jobboardscrapehistory
from apify_client import ApifyClient
from datetime import datetime, timedelta
import pytz
from scraper.parse import Serializer, SerializerDice, SerializerIndeed, SerializerLinkedin, SerializerZipRecruiter
from scraper.apiscraper import ApiScraper
   
class WorkItem:
    def __init__(self, scraper, configurations, serializer):
        self.scraper = scraper
        self.configurations = configurations
        self.serializer = serializer

class ConfigurationItem:
    def __init__(self, name, instance, serializer):
        self.name = name
        self.instance = instance
        self.serializer = serializer  
        
configurationDictionary = [
    { "name": 'Dice',           "config": configdice,           "serializer": SerializerDice},
    { "name": 'Indeed',         "config": configindeed,         "serializer": SerializerIndeed},
    { "name": 'Linkedin',       "config": configlinkedin,       "serializer": SerializerLinkedin},
    { "name": 'ZipRecruiter',   "config": configziprecruiter,   "serializer": SerializerZipRecruiter}
]

class Worker:
    def __init__(self, name=None):
        print(f'Worker: init')
        self.name = name
        self.apiToken = ApifyKey.objects.first().value
        self.scrapers = Scraper.objects.filter(IsActive=True)
        self.configurationsInstances = []
        for configItem in configurationDictionary:
            configurationInstance = configItem['config'].objects.filter(Isactive=True)
            scraper = self.getScraperByName(configItem['name'])
            serializer = configItem['serializer'](scraper)

            if configurationInstance != None and scraper != None and serializer != None:
                configInstanceItem = ConfigurationItem(configItem['name'], configurationInstance, serializer)
                self.configurationsInstances.append(configInstanceItem)

        self.workerDictionary = self.makeWorkerDictionary()

    def getScraperByName(self, name):
        for scraper in self.scrapers:
            if scraper.Name == name:
                return scraper
        return None

    def getConfigurationInstanceByName(self, name):
        for instanceItem in self.configurationsInstances:
            if instanceItem.name == name:
                return instanceItem            
        return None

    def makeWorkerDictionary(self):        
        workerDictionary = []        
        for scraper in list(self.scrapers):
            worker = WorkItem(None, None, None)
            worker.scraper = scraper
            configInstance = self.getConfigurationInstanceByName(scraper.Name)
            if configInstance == None:
                worker = None
            else:
                worker.configurations = configInstance.instance
                worker.serializer = configInstance.serializer

            if worker != None:
                workerDictionary.append(worker)
        return workerDictionary

    def run(self):
        if self.name == 'all':
            self.scrapeAll()
            print(f'Worker: scrape-all-done--!')
        else:    
            self.scrapeSingle()
            print(f'Worker: scrape-{self.name}-done--!')

    
    def getWorker(self, name):
        for worker in self.workerDictionary:
            if worker.scraper.Name == name:
                return worker
        return None


    def scrapeAll(self):
        print(f'Worker: scrapeAll')
        for scraper in list(self.scrapers):
            worker = self.getWorker(scraper.Name)
            if worker != None:
                singleScraper = ApiScraper(worker=worker, apiToken=self.apiToken)
                singleScraper.run()
            else:
                print('Worker: scrapeAll Error getWorker == None')
    
    def scrapeSingle(self):
        print(f'Worker: scrapeSingle')
        worker = self.getWorker(self.name)
        if worker != None:
            singleScraper = ApiScraper(worker=worker, apiToken=self.apiToken)
            singleScraper.run()
        else:
            print('Worker: scrapeSingle Error getWorker == None')