import json

from celery import shared_task
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

from job.models import ConfigZiprecruiter, JobBoardResult, ScrapeHistory
from job.utils.api import ZiprecruiterClient
from job.utils.utils import get_datetime


@shared_task
def run_actor(config_pk, number_of_days):
    config = ConfigZiprecruiter.objects.get(pk=config_pk)
    url = config.url.replace("days=1", "days=%s" % number_of_days)
    ziprecruiter_input = {
        "startUrls": [{"url": url}],
        "maxItems": 100,
        "maxConcurrency": 10,
        "minConcurrency": 1,
        "maxRequestRetries": 10,
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"],
            "apifyProxyCountry": "US",
        },
    }
    ziprecruiter = ZiprecruiterClient(settings.APIFY_API_KEY)
    response = ziprecruiter.start_actor(ziprecruiter_input)
    print(response)
    # finished_at = response["finishedAt"].replace("Z", "+00:00")
    # finished_at = datetime.fromisoformat(finished_at)
    hisotry = ScrapeHistory(
        finished_at=response["finishedAt"],
        run_id=response["id"],
        dataset_id=response["defaultDatasetId"],
        scraper_name=ziprecruiter.actor_name,
        job_board=ziprecruiter.job_board,
        url=url,
        days=number_of_days,
        priority=config.priority,
        skill=config.skill,
        status=response["status"],
        input_json=ziprecruiter_input,
        output_json=json.dumps(
            response, sort_keys=True, indent=1, cls=DjangoJSONEncoder
        ),
        run_time=response["stats"]["runTimeSecs"],
        price=response["usageTotalUsd"],
    )
    hisotry.save()

    # saving jobs
    jobs = ziprecruiter.client.dataset(hisotry.dataset_id).iterate_items()
    for job in jobs:
        job_title = job.get("Title", "")
        job_description = job.get("description", "")
        salary = job.get("FormattedSalaryShort", "")
        company = job.get("OrgName", "")
        location = (
            job.get("jobDetails", {})
            .get("model", {})
            .get("gtmData", {})
            .get("JobLocation", "")
        )
        employment_type = job.get("EmploymentType", "")
        job_posted_days_ago = job.get("FirstSeenDaysAgo", 0)
        job_url = job.get("Href", "")
        apply_params = job.get("jobDetails", {}).get("model", {}).get("applyParams", {})
        if apply_params.get("isExternalApply"):
            external_apply_url = apply_params.get("externalApplyUrl")
        else:
            external_apply_url = None
        if apply_params.get("isZipApply"):
            apply_type = "EASY_APPLY"
        else:
            apply_type = "EXTERNAL_APPLY"

        new_job = {
            "job_title": job_title,
            "job_description": job_description,
            "source": hisotry.job_board,
            "skill": hisotry.skill,
            "priority": hisotry.priority,
            "date_scraped": hisotry.started_at,
            "run_id": hisotry.run_id,
            "date_job_posted": get_datetime(job_posted_days_ago),
            "salary": salary,
            "job_type": employment_type,
            "company": company,
            "location": location,
            "job_url": job_url,
            "apply_type": apply_type,
            "external_apply_url": external_apply_url,
        }
        print(new_job)
        JobBoardResult.objects.create(**new_job)
