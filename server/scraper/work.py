from scraper.models import ApifyKey, Scraper, configdice, configindeed, configlinkedin, configziprecruiter
from scraper.models import jobboardscraperesults, jobboardscrapehistory
from apify_client import ApifyClient
from datetime import datetime, timedelta
import pytz


class ApiScraper:
    def __init__(self, configurations=None, apiToken=None, scraper=None):
        self.configurations = list(enumerate(configurations))
        self.apiToken = apiToken
        self.scrapers = list(scraper)
        self.scraper = self.scrapers[0]
        self.apifyClient = ApifyClient(self.apiToken)
        self.actorId = self.scraper.actor_id

    def run(self):
        for j, configuration in self.configurations:
            self.runConfig(configuration)
        return

    def runConfig(self, configuration):
        number_of_days = 10
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
            
            response = self.apifyClient.actor(self.actorId).call(run_input=payload)
            print(f'DatasetId: {response["defaultDatasetId"]}')
            # Retry with modified number_of_days
            jobs = list(self.apifyClient.dataset(response["defaultDatasetId"]).iterate_items())
            number_of_jobs = 0
            print(f'response jobs count = {len(jobs)}')
            # Save job
            if len(jobs) > 0: 
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

                    new_job_result = jobboardscraperesults(
                        Jobtitle=job_title,
                        Jobdescription=job_description,
                        Source=self.actorId,
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
            print(f'=== run_actor error: {str(err)}')
            
            return

class Worker:
    def __init__(self, name=None):
        self.name = name
        self.apiToken = ApifyKey.objects.first().value
        self.scrapers = Scraper.objects.filter(is_active=True)
        self.configDice = configdice.objects.filter(Isactive=True)
        self.configIndeed = configindeed.objects.filter(Isactive=True)
        self.configLinkedin = configlinkedin.objects.filter(Isactive=True)
        self.configZipRecruiter = configziprecruiter.objects.filter(Isactive=True)

    def run(self):
        if self.name == None:
            self.scrapeAll()
        else:    
            self.scrapeSingle()

    def getConfigbyName(self, name):
        if name == 'Dice':
            return self.configDice
        elif name == 'Indeed':
            return self.configIndeed
        elif name == 'Linkedin':
            return self.configLinkedin
        elif name == 'ZipRecruiter':
            return self.configZipRecruiter
        
        return None

    def scrapeAll(self):
        for i, scraper in list(enumerate(self.scrapers)):
            configurations = self.getConfigbyName(scraper.name)
            singleScraper = ApiScraper(configurations, apiToken=self.apiToken, scraper=scraper)
            singleScraper.run()
    
    def scrapeSingle(self):
        configurations = self.getConfigbyName(self.name)
        singleScraper = ApiScraper(configurations=configurations, apiToken=self.apiToken, scraper=self.scrapers.filter(name=self.name))
        singleScraper.run()