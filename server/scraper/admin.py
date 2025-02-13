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

admin.site.register(Scraper)
admin.site.register(ApifyKey)
admin.site.register(configdice)
admin.site.register(configindeed)
admin.site.register(configlinkedin)
admin.site.register(configziprecruiter)
admin.site.register(jobboardscrapehistory)
admin.site.register(jobboardscraperesults)