from django.contrib import admin

from scraper.models import (
    Scraper,
    ApifyKey,
    configdice,
    configindeed,
    configlinkedin,
    configziprecruiter,
    jobboardscrapehistory,
    jobboardscraperesults
)

class ApifyKeyAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'value' )
    ordering = ('id',)

class ScraperAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'actor_id', 'actor_name', 'is_active', 'created_at' )
    ordering = ('name',)

class configdiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'Skill', 'Url', 'Isactive', 'Priority')
    ordering = ('id',)

class configindeedAdmin(admin.ModelAdmin):
    list_display = ('id', 'Skill', 'Url', 'Isactive', 'Priority', 'Donetoday')
    ordering = ('id',)

class configlinkedinAdmin(admin.ModelAdmin):
    list_display = ('id', 'Skill', 'Url', 'Isactive', 'Priority')
    ordering = ('id',)

class configziprecruiterAdmin(admin.ModelAdmin):
    list_display = ('id', 'Skill', 'Url', 'Isactive', 'Priority')
    ordering = ('id',)

class jobboardscraperesultsAdmin(admin.ModelAdmin):
    list_display = ('Jobtitle', 'Jobdescription', 'Source', 'Skill', 'ResumeCreated','Dateinserted', 'ScrapedAt', 'Runid', 'PostedAt', 'Salary', 'JobType', 'Company', 'Location', 'Joburl', 'Jobid', 'JdIsmismatch', 'WhoJdIsmismatch', 'Iscomplexform',  'TodayDate', 'ApplyType', 'Externalapplyurl' )


class jobboardscrapehistoryAdmin(admin.ModelAdmin):
    list_display = ( 'Datescrapestarted', 'Datescrapeended', 'Runid', 'Scrapername', 'Jobboard', 'Url', 'Days', 'Priority', 'Skill', 'Beginningstate', 'Endingstate',  'Endingstatesetby', 'Logdetails', 'Numberofjobsreturned', 'Rawjsonpassedtoscraper', 'Rawjsonresponsefromapify', 'Runtime', 'Price' )

admin.site.register(Scraper, ScraperAdmin)
admin.site.register(ApifyKey, ApifyKeyAdmin)
admin.site.register(configdice, configdiceAdmin)
admin.site.register(configindeed, configindeedAdmin)
admin.site.register(configlinkedin, configlinkedinAdmin)
admin.site.register(configziprecruiter, configziprecruiterAdmin)
admin.site.register(jobboardscrapehistory, jobboardscrapehistoryAdmin)
admin.site.register(jobboardscraperesults, jobboardscraperesultsAdmin)