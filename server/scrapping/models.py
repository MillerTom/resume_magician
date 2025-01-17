from django.db import models



class ConfigIndeed(models.Model):
    skill = models.TextField()
    url = models.TextField()
    is_active = models.BooleanField()
    priority = models.IntegerField()
    done_today = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    class Meta:
        verbose_name = "Indeed Configs"
        verbose_name_plural = "Indeed Configs"


class ConfigDice(models.Model):
    skill = models.TextField()
    url = models.TextField()
    is_active = models.BooleanField()
    priority = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    class Meta:
        verbose_name = "Dice Config"
        verbose_name_plural = "Dice Configs"


class ConfigLinkedIn(models.Model):
    skill = models.TextField()
    url = models.TextField()
    is_active = models.BooleanField()
    priority = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "LinkedIn Config"
        verbose_name_plural = "LinkedIn Configs"


class ConfigZipRecruiter(models.Model):
    skill = models.TextField()
    url = models.TextField()
    is_active = models.BooleanField()
    priority = models.IntegerField()
    done_today = models.BooleanField(default=False, null=True)
    run_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    meta_data = models.JSONField(default=dict, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "ZipRecruiter Config"
        verbose_name_plural = "ZipRecruiter Configs"
    
    def __str__(self):
        return "<ZipRecruiter Scrape Config |  Skill: %s>" % self.skill


class Resume(models.Model):
    job_title = models.TextField()
    job_description = models.TextField()
    source_job_board = models.TextField()
    skill = models.TextField()
    priority = models.IntegerField()
    date_resume_created = models.DateTimeField(null=True, blank=True)
    scraped_at = models.TextField(null=True, blank=True)
    run_id = models.TextField(null=True, blank=True)
    date_job_posted = models.DateTimeField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    job_type = models.TextField(null=True, blank=True)
    company = models.TextField(null=True, blank=True)
    job_location = models.TextField(null=True, blank=True)
    job_url = models.TextField(null=True, blank=True)
    customized_resume = models.TextField(null=True, blank=True)
    applied_for_by = models.TextField(null=True, blank=True)
    date_applied_for = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    request_regeneration = models.IntegerField(null=True, blank=True)
    job_id = models.TextField(null=True, blank=True)
    job_description_is_mismatch = models.BooleanField(default=False)
    who_flagged_job_description_is_mismatch = models.TextField(null=True, blank=True)
    is_complex_form = models.BooleanField(default=False)
    is_easy_apply = models.BooleanField(default=False)
    apply_status = models.TextField(null=True, blank=True)
    number_of_failures_applying = models.IntegerField(null=True, blank=True)
    is_locked = models.BooleanField(default=False)
    datetime_apply_started_at = models.DateTimeField(null=True, blank=True)
    date_today = models.DateTimeField(null=True, blank=True)
    date_job_removed_from_site = models.DateTimeField(null=True, blank=True)
    external_apply_url = models.TextField(null=True, blank=True)
    problem_applying = models.TextField(null=True, blank=True)
    index = models.IntegerField(null=True, blank=True)


class JobBoardScrapeHistory(models.Model):
    date_scrape_started = models.DateTimeField(auto_now_add=True, null=True)
    date_scrape_ended = models.DateTimeField(null=True, blank=True)
    run_id = models.CharField(max_length=255, null=True)
    scraper_name = models.CharField(max_length=255, null=True, default='apply-jobs-forever')
    job_board = models.TextField()
    url = models.TextField()
    days = models.IntegerField()
    priority = models.IntegerField()
    skill = models.TextField()
    beginning_state = models.TextField(null=True, blank=True)
    ending_state = models.TextField(null=True, blank=True)
    ending_state_set_by = models.TextField(null=True, blank=True)
    log_details = models.TextField(null=True, blank=True)
    number_of_jobs_returned = models.IntegerField(null=True, blank=True)
    raw_json_passed_to_scraper = models.JSONField(default=list, null=True, blank=True)
    raw_json_response_from_apify = models.JSONField(default=list, null=True, blank=True)
    runtime = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return "<JobBoardScrapeHistory | Job Board: %s>" % self.job_board


    class Meta:
        verbose_name = "Scrape History"
        verbose_name_plural = "Scrapes History"


class JobBoardScrapeResults(models.Model):
    job_board_scrape_history = models.ForeignKey(JobBoardScrapeHistory, on_delete=models.CASCADE, null=True)
    job_title = models.TextField()
    job_description = models.TextField()
    source_job_board = models.TextField()
    skill = models.TextField()
    priority = models.IntegerField()
    date_resume_created = models.DateTimeField(null=True, blank=True)
    date_scraped = models.DateTimeField(null=True, blank=True)
    run_id = models.TextField()
    date_job_posted = models.DateTimeField(null=True, blank=True)
    date_job_posted_human_form = models.CharField(max_length=255, null=True, blank=False)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_human_readable_form = models.CharField(max_length=255, null=True, blank=False)
    job_type = models.TextField()
    company = models.TextField()
    location = models.TextField()
    job_url = models.TextField()
    job_id = models.TextField()
    job_description_is_mismatch = models.BooleanField(default=False)
    who_flagged_job_description_is_mismatch = models.TextField(null=True, blank=True)
    is_complex_form = models.BooleanField(default=False)
    date_today = models.DateTimeField(null=True, blank=True)
    apply_type = models.TextField()
    external_apply_url = models.TextField(null=True, blank=True)
    raw_json_result = models.JSONField(default=dict, null=True, blank=True)
    raw_json_job_details = models.JSONField(default=dict, null=True, blank=True)


    class Meta:
        verbose_name = "Scrape Result"
        verbose_name_plural = "Scrape Results"


    def __str__(self):
        return "<JobBoardScrapeResults | Run ID: %s >" % self.job_board_scrape_history.run_id
