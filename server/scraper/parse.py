
from scraper.models import jobboardscraperesults, jobboardscrapehistory
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
                        Source=self.scraper.ActorID,
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
                Scrapername  = self.scraper.Name,
                Jobboard  = self.scraper.ActorName,
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
                        Source=self.scraper.ActorID,
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
                Scrapername  = self.scraper.Name,
                Jobboard  = self.scraper.ActorName,
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
                        Source=self.scraper.ActorID,
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
                Scrapername  = self.scraper.Name,
                Jobboard  = self.scraper.ActorName,
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
                        Source=self.scraper.ActorID,
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
                Scrapername  = self.scraper.Name,
                Jobboard  = self.scraper.ActorName,
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
        
