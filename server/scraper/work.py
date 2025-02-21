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
            number_of_days = 10
            number_of_jobs = len(jobs)
            print(f'SerializerDice: response jobs count = {len(jobs)}')
            # Save job
            if len(jobs) > 0: 
                for job in jobs:
                    job_title = job.get('title', '')
                    job_description = job.get('description', '')
                    salary = job.get('salaryRaw', '')
                    job_type = job.get('salaryRawUnit', '')
                    company = job.get('companyName', '')
                    location = job.get('location', '')
                       
                    job_posted_days_ago = job.get('datePosted', 0)
                    job_url = job.get('url', '')
                    external_apply_url = job.get('applyUrl', 0)
                    
                    new_job_result = jobboardscraperesults(
                        Jobtitle=job_title,
                        Jobdescription=job_description,
                        Source=self.scraper.actor_id,
                        Skill=configuration.Skill,
                        # Priority = configuration.Priority,
                        ResumeCreated = 'no',
                        Dateinserted = datetime.now(pytz.utc),
                        ScrapedAt = response["startedAt"],
                        Runid=response['id'],
                        PostedAt = job_posted_days_ago,
                        Salary = salary,
                        JobType = job_type,
                        Company=company,
                        Location=location,
                        Joburl=job_url,
                        Jobid = job.get('id', ''),
                        JdIsmismatch = 0,
                        WhoJdIsmismatch = 0,
                        Iscomplexform = 0,
                        TodayDate = datetime.now(pytz.utc),
                        ApplyType=job.get('contractType'),
                        Externalapplyurl=external_apply_url,                
                    )      
                    new_job_result.save()

            
            history = jobboardscrapehistory(
                Datescrapestarted = response['startedAt'],
                Datescrapeended = response['finishedAt'],
                Runid = response['id'],
                Scrapername  = self.scraper.name,
                Jobboard  = self.scraper.actor_name,
                Url  = configuration.Url,
                Days = number_of_days,
                Priority = configuration.Priority,
                Skill  = configuration.Skill,
                Beginningstate  = 'new task',
                Endingstate  = response['status'],
                Endingstatesetby  = response['actId'],
                Logdetails = response['statusMessage'],
                Numberofjobsreturned = number_of_jobs,
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
            number_of_days = 10
            number_of_jobs = len(jobs)
            print(f'SerializerIndeed: response jobs count = {len(jobs)}')
            # Save job
            if len(jobs) > 0: 
                for job in jobs:
                    job_title = job.get('positionName', '')
                    job_description = job.get('description', '')
                    salary = job.get('salary', '')
                    job_type = job.get('jobType', '')
                    company = job.get('company', '')
                    location = job.get('location', '')
                       
                    job_posted_days_ago = job.get('postingDateParsed', 0)
                    job_url = job.get('url', '')
                    external_apply_url = job.get('externalApplyLink', 0)
                    
                    new_job_result = jobboardscraperesults(
                        Jobtitle=job_title,
                        Jobdescription=job_description,
                        Source=self.scraper.actor_id,
                        Skill=configuration.Skill,
                        # Priority = configuration.Priority,
                        ResumeCreated = 'no',
                        Dateinserted = datetime.now(pytz.utc),
                        ScrapedAt = response["startedAt"],
                        Runid=response['id'],
                        PostedAt = job_posted_days_ago,
                        Salary = salary,
                        JobType = job_type,
                        Company=company,
                        Location=location,
                        Joburl=job_url,
                        Jobid = job.get('id', ''),
                        JdIsmismatch = 0,
                        WhoJdIsmismatch = 0,
                        Iscomplexform = 0,
                        TodayDate = datetime.now(pytz.utc),
                        ApplyType=job.get('applyType'),
                        Externalapplyurl=external_apply_url,                
                    )      
                    new_job_result.save()

            
            history = jobboardscrapehistory(
                Datescrapestarted = response['startedAt'],
                Datescrapeended = response['finishedAt'],
                Runid = response['id'],
                Scrapername  = self.scraper.name,
                Jobboard  = self.scraper.actor_name,
                Url  = configuration.Url,
                Days = number_of_days,
                Priority = configuration.Priority,
                Skill  = configuration.Skill,
                Beginningstate  = 'new task',
                Endingstate  = response['status'],
                Endingstatesetby  = response['actId'],
                Logdetails = response['statusMessage'],
                Numberofjobsreturned = number_of_jobs,
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
            number_of_days = 10
            number_of_jobs = len(jobs)
            print(f'SerializerLinkedin: response jobs count = {len(jobs)}')
            # Save job
            if len(jobs) > 0: 
                for job in jobs:
                    job_title = job.get('title', '')
                    job_description = job.get('description', '')
                    salary = job.get('salary', '')
                    job_type = job.get('contractType', '')
                    company = job.get('companyName', '')
                    location = job.get('location', '')
                       
                    job_posted_days_ago = job.get('postedTime', 0)
                    job_url = job.get('jobUrl', '')
                    external_apply_url = job.get('applyUrl', 0)
                    
                    new_job_result = jobboardscraperesults(
                        Jobtitle=job_title,
                        Jobdescription=job_description,
                        Source=self.scraper.actor_id,
                        Skill=configuration.Skill,
                        # Priority = configuration.Priority,
                        ResumeCreated = 'no',
                        Dateinserted = datetime.now(pytz.utc),
                        ScrapedAt = response["startedAt"],
                        Runid=response['id'],
                        PostedAt = job_posted_days_ago,
                        Salary = salary,
                        JobType = job_type,
                        Company=company,
                        Location=location,
                        Joburl=job_url,
                        Jobid = job.get('id', ''),
                        JdIsmismatch = 0,
                        WhoJdIsmismatch = 0,
                        Iscomplexform = 0,
                        TodayDate = datetime.now(pytz.utc),
                        ApplyType=job.get('applyType'),
                        Externalapplyurl=external_apply_url,                
                    )      
                    new_job_result.save()

            
            history = jobboardscrapehistory(
                Datescrapestarted = response['startedAt'],
                Datescrapeended = response['finishedAt'],
                Runid = response['id'],
                Scrapername  = self.scraper.name,
                Jobboard  = self.scraper.actor_name,
                Url  = configuration.Url,
                Days = number_of_days,
                Priority = configuration.Priority,
                Skill  = configuration.Skill,
                Beginningstate  = 'new task',
                Endingstate  = response['status'],
                Endingstatesetby  = response['actId'],
                Logdetails = response['statusMessage'],
                Numberofjobsreturned = number_of_jobs,
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
            number_of_days = 10
            number_of_jobs = len(jobs)
            print(f'SerializerZipRecruiter: response jobs count = {len(jobs)}')
            # Save job
            if len(jobs) > 0: 
                for job in jobs:
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

                    new_job_result = jobboardscraperesults(
                        Jobtitle=job_title,
                        Jobdescription=job_description,
                        Source=self.scraper.actor_id,
                        Skill=configuration.Skill,
                        # Priority = configuration.Priority,
                        ResumeCreated = 'no',
                        Dateinserted = datetime.now(pytz.utc),
                        ScrapedAt = response["startedAt"],
                        Runid=response['id'],
                        PostedAt = job_posted_days_ago,
                        Salary = salary,
                        JobType = job_type,
                        Company=company,
                        Location=location,
                        Joburl=job_url,
                        Jobid = job.get('QuizID', ''),
                        JdIsmismatch = 0,
                        WhoJdIsmismatch = 0,
                        Iscomplexform = 0,
                        TodayDate = datetime.now(pytz.utc),
                        ApplyType=apply_params.get('isZipApply'),
                        Externalapplyurl=external_apply_url,                
                    )      
                    new_job_result.save()

            
            history = jobboardscrapehistory(
                Datescrapestarted = response['startedAt'],
                Datescrapeended = response['finishedAt'],
                Runid = response['id'],
                Scrapername  = self.scraper.name,
                Jobboard  = self.scraper.actor_name,
                Url  = configuration.Url,
                Days = number_of_days,
                Priority = configuration.Priority,
                Skill  = configuration.Skill,
                Beginningstate  = 'new task',
                Endingstate  = response['status'],
                Endingstatesetby  = response['actId'],
                Logdetails = response['statusMessage'],
                Numberofjobsreturned = number_of_jobs,
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
        number_of_days = 1
        url = configuration.Url
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

class Worker:
    def __init__(self, name=None):
        print(f'Worker: init')
        self.name = name
        self.apiToken = ApifyKey.objects.first().value
        self.scrapers = Scraper.objects.filter(is_active=True)
        self.configDice = configdice.objects.filter(Isactive=True)
        self.configIndeed = configindeed.objects.filter(Isactive=True)
        self.configLinkedin = configlinkedin.objects.filter(Isactive=True)
        self.configZipRecruiter = configziprecruiter.objects.filter(Isactive=True)

        self.workerDictionary = self.makeWorkerDictionary()

    def makeWorkerDictionary(self):        
        workerDictionary = []        
        for scraper in list(self.scrapers):
            worker = WorkItem(None, None, None)
            worker.scraper = scraper
            if scraper.name == 'Dice':
                worker.configurations = self.configDice
                worker.serializer = SerializerDice(scraper)
            elif scraper.name == 'Indeed':
                worker.configurations = self.configIndeed
                worker.serializer = SerializerIndeed(scraper)
            elif scraper.name == 'Linkedin':
                worker.configurations = self.configLinkedin
                worker.serializer = SerializerLinkedin(scraper)
            elif scraper.name == 'ZipRecruiter':
                worker.configurations = self.configZipRecruiter
                worker.serializer = SerializerZipRecruiter(scraper)
            else:
                worker = None

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