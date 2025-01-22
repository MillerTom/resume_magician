from django.db import models


class UserInfo(models.Model):
    email = models.CharField(max_length=200, default='')
    name = models.CharField(max_length=200, default='')
    created_at = models.DateTimeField(auto_now_add=True)


class Job(models.Model):
    user = models.ForeignKey(UserInfo, related_name='user_jobs', on_delete=models.CASCADE, null=True)
    url = models.CharField(max_length=1000, default='')
    index = models.IntegerField(default=-1)
    created_at = models.DateTimeField(auto_now_add=True)
    applied_at = models.DateTimeField(null=True)


class ConfigIndeed(models.Model):
    skill = models.CharField(max_length=200)
    url = models.URLField()
    is_active = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    done_today = models.BooleanField()

    class Meta:
        verbose_name_plural = "Config Indeed"


class ConfigDice(models.Model):
    skill = models.CharField(max_length=200)
    url = models.URLField()
    is_active = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Config Dice"


class ConfigLinkedIn(models.Model):
    skill = models.CharField(max_length=200)
    url = models.URLField()
    is_active = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Config LinkedIn"


class ConfigZiprecruiter(models.Model):
    skill = models.CharField(max_length=200)
    url = models.URLField()
    is_active = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Config Ziprecruiter"


# create job apply type using choice field
class JobApplyType(models.TextChoices):
    EASY_APPLY = "EASY_APPLY"
    EXTERNAL_APPLY = "EXTERNAL_APPLY"


class JobBoardResult(models.Model):
    job_title = models.CharField(max_length=220)
    job_description = models.TextField()
    source = models.CharField(max_length=50)
    skill = models.CharField(max_length=220)
    priority = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    date_scraped = models.DateTimeField()
    run_id = models.CharField(max_length=50)
    date_job_posted = models.DateField()
    salary = models.CharField(max_length=100)
    job_type = models.CharField(max_length=50, null=True, blank=True)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100, null=True, blank=True)
    job_url = models.URLField(max_length=500)
    job_id = models.UUIDField(
        unique=True, primary_key=True, default=uuid.uuid4, editable=False
    )
    job_description_is_mismatch = models.BooleanField(default=False)
    who_flagged_job_description_is_mismatch = models.CharField(
        max_length=50, null=True, blank=True
    )
    is_complex_form = models.BooleanField(default=False)
    apply_type = models.CharField(
        max_length=50, choices=JobApplyType.choices, default=JobApplyType.EASY_APPLY
    )
    external_apply_url = models.URLField(max_length=500, null=True, blank=True)


class RunStatus(models.TextChoices):
    READY = "READY"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    TIMED_OUT = "TIMED_OUT"
    ABORTED = "ABORTED"


class ScrapeHistory(models.Model):
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    run_id = models.CharField(max_length=50, unique=True)
    dataset_id = models.CharField(max_length=50, blank=True, null=True)
    scraper_name = models.CharField(max_length=50)
    job_board = models.CharField(max_length=50)
    url = models.URLField()
    days = models.IntegerField(default=1)
    priority = models.IntegerField(default=1)
    skill = models.CharField(max_length=200)
    status = models.CharField(
        max_length=50, choices=RunStatus.choices, default=RunStatus.READY
    )
    input_json = models.JSONField(blank=True, null=True)
    output_json = models.JSONField(blank=True, null=True)
    run_time = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    price = models.DecimalField(default=0.0, max_digits=8, decimal_places=4)

    class Meta:
        verbose_name_plural = "Scrape Histories"
