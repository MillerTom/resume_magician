from django.db import models
import uuid


class Scraper(models.Model):
    name = models.CharField(max_length=50)
    actor_id = models.CharField(max_length=100)
    actor_name = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Scraper'
        db_table = 'scrapers'


class Configuration(models.Model):
    scraper = models.ForeignKey(Scraper, related_name='scraper_configurations', on_delete=models.CASCADE, null=True)
    skill = models.CharField(max_length=200)
    url = models.URLField()
    priority = models.IntegerField(default=0)
    days = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Configuration'
        db_table = 'configurations'


class JobBoardResult(models.Model):
    id=models.AutoField(primary_key=True)
    configuration = models.ForeignKey(Configuration, related_name='configuration_job_results', on_delete=models.CASCADE, null=True)
    job_title = models.CharField(max_length=220, default='')
    job_description = models.TextField()
    source = models.CharField(max_length=50, default='')
    skill = models.CharField(max_length=220, default='')
    date_resume_created = models.DateTimeField(null=True)
    date_scraped = models.DateTimeField(null=True)
    run_id = models.CharField(max_length=50, default='')
    date_job_posted = models.DateTimeField(null=True)
    salary = models.CharField(default=50)
    job_type = models.CharField(max_length=50, default='')
    company = models.CharField(max_length=100, default='')
    location = models.CharField(max_length=100, default='')
    job_url = models.URLField(max_length=500, null=True)
    customized_resume_url = models.URLField(max_length=500, null=True)
    applied_for_by = models.CharField(max_length=100, default='')
    date_applied_for = models.DateTimeField(null=True)
    general_notes = models.CharField(max_length=500, default='')
    is_request_regeneration = models.BooleanField(default=False)
    job_mismatch = models.BooleanField(default=False)
    who_jd_mismatch = models.CharField(max_length=100, default='')
    is_complex_form = models.BooleanField(default=False)
    is_easyapply = models.BooleanField(default=False)
    apply_status = models.CharField(max_length=100, default='')
    failure_applying = models.IntegerField(default=0)
    external_apply_url = models.URLField(max_length=500, null=True)
    lock_application = models.BooleanField(default=False)
    date_apply_started = models.DateTimeField(null=True)
    date_job_removed_from_site = models.DateTimeField(null=True)
    problem_applying_description = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'jobboard_results'


class ScrapeHistory(models.Model):
    configuration = models.ForeignKey(Configuration, related_name='configuration_history', on_delete=models.CASCADE, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    run_id = models.CharField(max_length=50, unique=True)
    dataset_id = models.CharField(max_length=50, blank=True, null=True)
    job_board = models.CharField(max_length=50)
    days = models.IntegerField(default=1)
    status = models.CharField(max_length=50)
    input_json = models.JSONField(blank=True, null=True)
    run_time = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    price = models.DecimalField(default=0.0, max_digits=8, decimal_places=4)
    is_done = models.BooleanField(default=False)
    number_of_jobs = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Scrape History'
        db_table = 'scrape_history'


class ApifyKey(models.Model):
    value = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Apify API Key'
        db_table = 'apify_key'
