from django.contrib import admin


from scrapping import models



@admin.register(models.ConfigDice)
class AdminConfigDice(admin.ModelAdmin):
    list_display = ["url", "is_active", "skill"]


@admin.register(models.ConfigLinkedIn)
class AdminConfigLinkedIn(admin.ModelAdmin):
    list_display = ["url", "is_active", "skill"]


@admin.register(models.ConfigZipRecruiter)
class AdminConfigZipRecruiter(admin.ModelAdmin):
    list_display = ["skill", "pk", "url", "is_active", "priority", "created_at"]


@admin.register(models.ConfigIndeed)
class AdminConfigIndeed(admin.ModelAdmin):
    list_display = ["pk", "skill", "url", "is_active", "done_today"]


@admin.register(models.JobBoardScrapeHistory)
class AdminScrapeHistory(admin.ModelAdmin):
    list_display = [
        "pk",
        "job_board",
        "skill",
        "number_of_jobs_returned",
        "run_id",
        "runtime",
        "price",
    ]


@admin.register(models.JobBoardScrapeResults)
class JobBoardScrapeResults(admin.ModelAdmin):
    # TO DO
    pass
