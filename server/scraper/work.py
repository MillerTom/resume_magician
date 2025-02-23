from scraper.models import ApifyKey, Scraper, configdice, configindeed, configlinkedin, configziprecruiter
from scraper.models import jobboardscraperesults, jobboardscrapehistory
from apify_client import ApifyClient
from datetime import datetime, timedelta
import pytz


class Serializer:
    def __init__(self, scraper=None):
        self.scraper = scraper
    
    def save(self, configuration, response):
        return
    
class SerializerDice(Serializer):
    def save(self, configuration, response, jobs, payload):
        try:            
            numberOfDays = 10
            numberOfJobs = len(jobs)
            print(f'SerializerDice: response jobs count = {len(jobs)}')
            # Save job
            if len(jobs) > 0: 
                for job in jobs:
                    jobTitle = job.get('title', '')
                    Jobdescription = job.get('description', '')
                    salary = job.get('salaryRaw', '')
                    jobType = job.get('salaryRawUnit', '')
                    company = job.get('companyName', '')
                    location = job.get('location', '')
                       
                    jobPostedAt = job.get('datePosted', 0)
                    jobUrl = job.get('url', '')
                    externalApplyUrl = job.get('applyUrl', 0)
                    
                    jobResult = jobboardscraperesults(
                        Jobtitle=jobTitle,
                        Jobdescription=Jobdescription,
                        Source=self.scraper.actor_id,
                        Skill=configuration.Skill,
                        # Priority = configuration.Priority,
                        ResumeCreated = 'no',
                        Dateinserted = datetime.now(pytz.utc),
                        ScrapedAt = response["startedAt"],
                        Runid=response['id'],
                        PostedAt = jobPostedAt,
                        Salary = salary,
                        JobType = jobType,
                        Company=company,
                        Location=location,
                        Joburl=jobUrl,
                        Jobid = job.get('id', ''),
                        JdIsmismatch = 0,
                        WhoJdIsmismatch = 0,
                        Iscomplexform = 0,
                        TodayDate = datetime.now(pytz.utc),
                        ApplyType=job.get('contractType'),
                        Externalapplyurl=externalApplyUrl,                
                    )      
                    jobResult.save()

            
            history = jobboardscrapehistory(
                Datescrapestarted = response['startedAt'],
                Datescrapeended = response['finishedAt'],
                Runid = response['id'],
                Scrapername  = self.scraper.name,
                Jobboard  = self.scraper.actor_name,
                Url  = configuration.Url,
                Days = numberOfDays,
                Priority = configuration.Priority,
                Skill  = configuration.Skill,
                Beginningstate  = 'new task',
                Endingstate  = response['status'],
                Endingstatesetby  = response['actId'],
                Logdetails = response['statusMessage'],
                Numberofjobsreturned = numberOfJobs,
                Rawjsonpassedtoscraper  = payload,
                Rawjsonresponsefromapify  = response,
                Runtime = response['stats']['runTimeSecs'],
                Price = response['usageTotalUsd'],
            )

            history.save()
            
        except Exception as err:
            print(f'SerializerDice error: {str(err)}')            
            
        return
  
class SerializerIndeed(Serializer):
    def save(self, configuration, response, jobs, payload):
        try:            
            numberOfDays = 10
            numberOfJobs = len(jobs)
            print(f'SerializerIndeed: response jobs count = {len(jobs)}')
            # Save job
            if len(jobs) > 0: 
                for job in jobs:
                    jobTitle = job.get('positionName', '')
                    Jobdescription = job.get('description', '')
                    salary = job.get('salary', '')
                    jobType = job.get('jobType', '')
                    company = job.get('company', '')
                    location = job.get('location', '')
                       
                    jobPostedAt = job.get('postingDateParsed', 0)
                    jobUrl = job.get('url', '')
                    externalApplyUrl = job.get('externalApplyLink', 0)
                    
                    jobResult = jobboardscraperesults(
                        Jobtitle=jobTitle,
                        Jobdescription=Jobdescription,
                        Source=self.scraper.actor_id,
                        Skill=configuration.Skill,
                        # Priority = configuration.Priority,
                        ResumeCreated = 'no',
                        Dateinserted = datetime.now(pytz.utc),
                        ScrapedAt = response["startedAt"],
                        Runid=response['id'],
                        PostedAt = jobPostedAt,
                        Salary = salary,
                        JobType = jobType,
                        Company=company,
                        Location=location,
                        Joburl=jobUrl,
                        Jobid = job.get('id', ''),
                        JdIsmismatch = 0,
                        WhoJdIsmismatch = 0,
                        Iscomplexform = 0,
                        TodayDate = datetime.now(pytz.utc),
                        ApplyType=job.get('applyType'),
                        Externalapplyurl=externalApplyUrl,                
                    )      
                    jobResult.save()

            
            history = jobboardscrapehistory(
                Datescrapestarted = response['startedAt'],
                Datescrapeended = response['finishedAt'],
                Runid = response['id'],
                Scrapername  = self.scraper.name,
                Jobboard  = self.scraper.actor_name,
                Url  = configuration.Url,
                Days = numberOfDays,
                Priority = configuration.Priority,
                Skill  = configuration.Skill,
                Beginningstate  = 'new task',
                Endingstate  = response['status'],
                Endingstatesetby  = response['actId'],
                Logdetails = response['statusMessage'],
                Numberofjobsreturned = numberOfJobs,
                Rawjsonpassedtoscraper  = payload,
                Rawjsonresponsefromapify  = response,
                Runtime = response['stats']['runTimeSecs'],
                Price = response['usageTotalUsd'],
            )

            history.save()
            
        except Exception as err:
            print(f'SerializerIndeed error: {str(err)}')            
            
        return
   
class SerializerLinkedin(Serializer):
    def save(self, configuration, response, jobs, payload):
        try:            
            numberOfDays = 10
            numberOfJobs = len(jobs)
            print(f'SerializerLinkedin: response jobs count = {len(jobs)}')
            # Save job
            if len(jobs) > 0: 
                for job in jobs:
                    jobTitle = job.get('title', '')
                    Jobdescription = job.get('description', '')
                    salary = job.get('salary', '')
                    jobType = job.get('contractType', '')
                    company = job.get('companyName', '')
                    location = job.get('location', '')
                       
                    jobPostedAt = job.get('postedTime', 0)
                    jobUrl = job.get('jobUrl', '')
                    externalApplyUrl = job.get('applyUrl', 0)
                    
                    jobResult = jobboardscraperesults(
                        Jobtitle=jobTitle,
                        Jobdescription=Jobdescription,
                        Source=self.scraper.actor_id,
                        Skill=configuration.Skill,
                        # Priority = configuration.Priority,
                        ResumeCreated = 'no',
                        Dateinserted = datetime.now(pytz.utc),
                        ScrapedAt = response["startedAt"],
                        Runid=response['id'],
                        PostedAt = jobPostedAt,
                        Salary = salary,
                        JobType = jobType,
                        Company=company,
                        Location=location,
                        Joburl=jobUrl,
                        Jobid = job.get('id', ''),
                        JdIsmismatch = 0,
                        WhoJdIsmismatch = 0,
                        Iscomplexform = 0,
                        TodayDate = datetime.now(pytz.utc),
                        ApplyType=job.get('applyType'),
                        Externalapplyurl=externalApplyUrl,                
                    )      
                    jobResult.save()

            
            history = jobboardscrapehistory(
                Datescrapestarted = response['startedAt'],
                Datescrapeended = response['finishedAt'],
                Runid = response['id'],
                Scrapername  = self.scraper.name,
                Jobboard  = self.scraper.actor_name,
                Url  = configuration.Url,
                Days = numberOfDays,
                Priority = configuration.Priority,
                Skill  = configuration.Skill,
                Beginningstate  = 'new task',
                Endingstate  = response['status'],
                Endingstatesetby  = response['actId'],
                Logdetails = response['statusMessage'],
                Numberofjobsreturned = numberOfJobs,
                Rawjsonpassedtoscraper  = payload,
                Rawjsonresponsefromapify  = response,
                Runtime = response['stats']['runTimeSecs'],
                Price = response['usageTotalUsd'],
            )

            history.save()
            
        except Exception as err:
            print(f'SerializerLinkedin: error: {str(err)}')
            
        return
    
class SerializerZipRecruiter(Serializer):
    def save(self, configuration, response, jobs, payload):
        try:            
            numberOfDays = 10
            numberOfJobs = len(jobs)
            print(f'SerializerZipRecruiter: response jobs count = {len(jobs)}')
            # Save job
            if len(jobs) > 0: 
                for job in jobs:
                    jobTitle = job.get('Title', '')
                    Jobdescription = job.get('description', '')
                    salary = job.get('FormattedSalaryShort', '')
                    jobType = job.get('EmploymentType', '')
                    company = job.get('OrgName', '')
                    location = (
                        job.get('jobDetails', {})
                        .get('model', {})
                        .get('gtmData', {})
                        .get('JobLocation', '')
                    )
                    jobPostedAt = job.get('FirstSeenDaysAgo', 0)
                    jobUrl = job.get('Href', '')
                    applyParams = job.get('jobDetails', {}).get('model', {}).get('applyParams', {})
                    if applyParams.get('isExternalApply'):
                        externalApplyUrl = applyParams.get('externalApplyUrl')
                    else:
                        externalApplyUrl = None

                    jobResult = jobboardscraperesults(
                        Jobtitle=jobTitle,
                        Jobdescription=Jobdescription,
                        Source=self.scraper.actor_id,
                        Skill=configuration.Skill,
                        # Priority = configuration.Priority,
                        ResumeCreated = 'no',
                        Dateinserted = datetime.now(pytz.utc),
                        ScrapedAt = response["startedAt"],
                        Runid=response['id'],
                        PostedAt = jobPostedAt,
                        Salary = salary,
                        JobType = jobType,
                        Company=company,
                        Location=location,
                        Joburl=jobUrl,
                        Jobid = job.get('QuizID', ''),
                        JdIsmismatch = 0,
                        WhoJdIsmismatch = 0,
                        Iscomplexform = 0,
                        TodayDate = datetime.now(pytz.utc),
                        ApplyType=applyParams.get('isZipApply'),
                        Externalapplyurl=externalApplyUrl,                
                    )      
                    jobResult.save()

            
            history = jobboardscrapehistory(
                Datescrapestarted = response['startedAt'],
                Datescrapeended = response['finishedAt'],
                Runid = response['id'],
                Scrapername  = self.scraper.name,
                Jobboard  = self.scraper.actor_name,
                Url  = configuration.Url,
                Days = numberOfDays,
                Priority = configuration.Priority,
                Skill  = configuration.Skill,
                Beginningstate  = 'new task',
                Endingstate  = response['status'],
                Endingstatesetby  = response['actId'],
                Logdetails = response['statusMessage'],
                Numberofjobsreturned = numberOfJobs,
                Rawjsonpassedtoscraper  = payload,
                Rawjsonresponsefromapify  = response,
                Runtime = response['stats']['runTimeSecs'],
                Price = response['usageTotalUsd'],
            )

            history.save()
            
        except Exception as err:
            print(f'SerializerZipRecruiter: error: {str(err)}')            
            
        return
        

class ApiScraper:
    def __init__(self, worker=None, apiToken=None):
        print(f'ApiScraper: init')
        if worker != None:
            self.scraper = worker.scraper
            self.configurations = list(worker.configurations)        
            self.actorId = self.scraper.actor_id
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
        self.scrapers = Scraper.objects.filter(is_active=True)
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
            if scraper.name == name:
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
            configInstance = self.getConfigurationInstanceByName(scraper.name)
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
            if worker.scraper.name == name:
                return worker
        return None


    def scrapeAll(self):
        print(f'Worker: scrapeAll')
        for scraper in list(self.scrapers):
            worker = self.getWorker(scraper.name)
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