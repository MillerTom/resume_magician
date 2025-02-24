from django.db import models
import uuid


class Scraper(models.Model):
    Name = models.CharField(max_length=50)
    ActorID = models.CharField(max_length=100)
    ActorName = models.CharField(max_length=500)
    IsActive = models.BooleanField(default=True)
    CreatedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Scraper'
        db_table = 'scrapers'


class ApiToken(models.Model):
    value = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'ApiTokens'
        db_table = 'ApiToken'


class configindeed(models.Model):   
    Skill = models.TextField()
    Url = models.TextField()
    Isactive = models.BooleanField()
    Priority = models.IntegerField(default=0)
    Donetoday  = models.TextField()

    class Meta:
        verbose_name = 'configindeed'
        verbose_name_plural = 'configindeeds'
        db_table = 'configindeed'

class configdice(models.Model):
    Skill  = models.TextField()
    Url  = models.TextField()
    Isactive  = models.BooleanField(default=True)
    Priority = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'configdice'
        verbose_name_plural = 'configdices'
        db_table = 'configdice'

class configlinkedin(models.Model):
    Skill  = models.TextField()
    Url  = models.TextField()
    Isactive  = models.BooleanField(default=True)
    Priority = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'configlinkedin'
        verbose_name_plural = 'configlinkedins'
        db_table = 'configlinkedin'

    
class configziprecruiter(models.Model):
    Skill  = models.TextField()
    Url  = models.TextField()
    Isactive  = models.BooleanField(default=True)
    Priority = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'configziprecruiter'
        verbose_name_plural = 'configziprecruiters'
        db_table = 'configziprecruiter'


class resumes (models.Model):
    Jobtitle  = models.TextField()
    Jobdescription  = models.TextField()
    Source  = models.TextField()
    Skill  = models.TextField()
    Priority = models.IntegerField(default=0),
    Dateresumecreated  = models.TextField()
    Scrapedat  = models.TextField()
    Runid  = models.TextField()
    Dateposted  = models.TextField()
    Salary  = models.TextField()
    Jobtype  = models.TextField()
    Company  = models.TextField()
    Location  = models.TextField()
    Joburl  = models.TextField()
    Customizedresume  = models.TextField()
    Appliedforby  = models.TextField()
    Appliedfordate  = models.TextField()
    Notes = models.FloatField()
    Requestregeneration = models.FloatField()
    Jobid  = models.TextField()
    JdIsmismatch = models.FloatField()
    WhoJdIsmismatch = models.FloatField()
    Iscomplexform = models.BooleanField()
    Iseasyapply  = models.TextField()
    Applystatus  = models.TextField()
    Failuresapplying = models.FloatField()
    Lock  = models.TextField()
    Applystartedat  = models.TextField()
    Date = models.DateTimeField()
    Datejobremovedfromsite = models.FloatField()
    Externalapplyurl = models.URLField()
    Problemapplying = models.FloatField()
    Index = models.BigIntegerField()

    class Meat:
        verbose_name = 'resume'
        verbose_name_plural = 'resumes'
        db_table = 'resumes'


class jobboardscrapehistory (models.Model):
    Datescrapestarted  = models.TextField()
    Datescrapeended  = models.TextField()
    Runid  = models.TextField()
    Scrapername  = models.TextField()
    Jobboard  = models.TextField()
    Url  = models.TextField()
    Days = models.IntegerField()
    Priority = models.IntegerField(default=0)
    Skill  = models.TextField()
    Beginningstate  = models.TextField()
    Endingstate  = models.TextField()
    Endingstatesetby  = models.TextField()
    Logdetails = models.TextField()
    Numberofjobsreturned = models.IntegerField()
    Rawjsonpassedtoscraper  = models.TextField()
    Rawjsonresponsefromapify  = models.TextField()
    Runtime = models.FloatField()
    Price = models.FloatField()

    class Meta:
        verbose_name = 'jobboardscrapehistory'
        verbose_name_plural = 'jobboardscrapehistorys'
        db_table = 'jobboardscrapehistory'


class jobboardscraperesults (models.Model):
    Jobtitle  = models.TextField()
    Jobdescription  = models.TextField()
    Source  = models.TextField()
    Skill  = models.TextField()
    # Priority = models.IntegerField(default=0),
    ResumeCreated  = models.TextField()
    Dateinserted  = models.TextField()
    ScrapedAt  = models.TextField()
    Runid  = models.TextField()
    PostedAt  = models.TextField()
    Salary  = models.TextField()
    JobType  = models.TextField()
    Company  = models.TextField()
    Location  = models.TextField()
    Joburl  = models.TextField()
    Jobid  = models.TextField()
    JdIsmismatch = models.FloatField()
    WhoJdIsmismatch = models.FloatField()
    Iscomplexform = models.FloatField()
    TodayDate  = models.TextField()
    ApplyType  = models.TextField()
    Externalapplyurl  = models.TextField(null=True)

    class Meta:
        verbose_name = 'jobboardscraperesult'
        verbose_name_plural = 'jobboardscraperesults'
        db_table = 'jobboardscraperesults'