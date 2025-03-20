from django.contrib import admin
from scraper.models import (
    Scraper,
    Configuration,
    JobBoardResult,
    ScrapeHistory,
    ApifyKey,
)

admin.site.register(Scraper)
admin.site.register(Configuration)
admin.site.register(ApifyKey)

@admin.register(ScrapeHistory)
class ScrapeHistoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ScrapeHistory._meta.get_fields()]

@admin.register(JobBoardResult)
class JobBoardResultAdmin(admin.ModelAdmin):
    list_display = [field.name for field in JobBoardResult._meta.get_fields()]