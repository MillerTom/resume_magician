import logging
import pdb

import requests
from apify_client import ApifyClient
from django.conf import settings
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


from api.serializers import JobBoardScrapeResultsSerializer
from scrapping import models


logger = logging.getLogger(__name__)



class ScrapeZipRecruiterEndpoint(APIView):
    
    permission_classes = []
    authentication_classes = []

    @swagger_auto_schema(
        tags=["Scraping"],
        operation_description="Scrape ZipRecuriter for jobs data",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["NumberOfDays", "AppConsuming"],
            properties={
                "NumberOfDays": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="The number of days to scrape job data for"
                ),
                "AppConsuming": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The consuming app's identifier"
                ),
                "SingleSkill": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="If this parameter is set, only one skill url will be scrapped, otherwise, the system will scrape all other skills url"
                ),
            },
        )
    )
    def post(self, request):
        number_of_days = request.data.get("NumberOfDays")
        app_consuming = request.data.get("AppConsuming")
        single_skill = request.data.get("SingleSkill")

        if not number_of_days:
            return Response({"error": "NumberOfDays is required"}, status=400)
        
        if not app_consuming:
            return Response({"error" : "AppConsuming is required"}, status=status.HTTP_400_error)
        
        if single_skill is None:
            configs = models.ConfigZipRecruiter.objects.all()
        else:
            configs = models.ConfigZipRecruiter.objects.filter(
                skill__iexact=single_skill
            )
            if not configs.exists():
                return Response(
                    {"error" : "Skill %s does not exist" % single_skill}, status=status.HTTP_400_BAD_REQUEST
                )

        client = ApifyClient(settings.APIFY_KEYS.get("ziprecruiter_key"))

        results = []
        for config in configs:

            ############################################################
            # This marks the current config as being active on the DB
            ############################################################

            config.is_active = True
            config.save()

            #############################################################
            # Create the history first record for this scrape
            #############################################################

            scrape_url = config.url.replace("days=1", "days=%s" % number_of_days)
            priority = config.priority
            skill = config.skill
            scrape_history = models.JobBoardScrapeHistory.objects.create(
                url=scrape_url,
                days=number_of_days,
                job_board="ziprecruiter",
                skill=skill,
                priority=priority,
            )
            
            #############################################################
            # Run the scraper via apify
            #############################################################

            run_input = {
				"startUrls": [{ "url": scrape_url}],
				"proxy": {
					"useApifyProxy": True,
					"apifyProxyGroups": ["RESIDENTIAL"],
					"apifyProxyCountry": "US",
				},
			}
            result = client.actor("memo23/apify-ziprecruiter-scraper").call(run_input=run_input)           
            
            #############################################################
            # Store the results, and store the raw json so we can inspect
            # and see what we need from the response
            #############################################################

            # clean some values to timestamps
            for i in ["startedAt", "createdAt", "notifiedAboutChangeAt"]:
                result["pricingInfo"][i] = result["pricingInfo"][i].timestamp()
            result["finishedAt"] = result["finishedAt"].timestamp()
            result["startedAt"] = result["startedAt"].timestamp()

            run_price = result.get("usageTotalUsd")
            dataset_id = result.get("defaultDatasetId")
            dataset_results = [x for x in client.dataset(dataset_id).iterate_items()]

            scrape_history.date_scrape_ended = timezone.now()
            scrape_history.raw_json_response_from_apify = result
            scrape_history.run_id = dataset_id
            scrape_history.days = number_of_days
            scrape_history.ending_state = "ended"
            scrape_history.ending_state_set_by = "[APIView] - end of scrape"
            scrape_history.number_of_jobs_returned = len(dataset_results)
            scrape_history.price = run_price
            scrape_history.save()
            
            ###############################################
            # Store each result and CerEaLize the records 
            ###############################################
            
            store_status, to_serialize = self.store_results(scrape_history, dataset_results)
            if store_status and len(to_serialize) > 0:
                serializer = JobBoardScrapeResultsSerializer(to_serialize, many=True)
                serialized_results = serializer.data
            else:
                serialized_results = []

            results.append({
                "job_board" : "ziprecruiter",
                "app_consuming" : app_consuming,
                "skill" : skill,
                "url" : scrape_url,
                "results" : serialized_results,
                "run_metadata" : result,
            })

            ###############################################################
            # Indicate that the current Job Config is not active (finished)
            ###############################################################

            config.is_active = False
            config.save()


        return Response(
            {"message": "Scraping completed", "results": results},
            status=status.HTTP_200_OK
        )


    def store_results(self, scrape_history, results):
        try:
            record_batch = []
            for result in results:
                data = dict(
                    job_board_scrape_history=scrape_history,
                    job_title = result.get("Title", "-"),
                    job_description = result.get("description", "-"),
                    source_job_board=scrape_history.job_board,
                    skill=scrape_history.skill,
                    priority = scrape_history.priority,
                    date_scraped=scrape_history.date_scrape_started,
                    run_id = scrape_history.run_id,
                    date_job_posted_human_form=result.get("humanDate", "-"),
                    salary_human_readable_form=result.get("FormattedSalary", "-"),
                    job_type=result.get("EmploymentType", "-"),
                    company=result.get("OrgName", "-"),
                    location="%s, %s" % (result.get("City", "-"), result.get("State", "-")),
                    job_url=result.get("JobURL", "-"),
                    job_id="KEY-NOT-FOUND",
                    #job_description_is_mismatch=False, # default!
                    #who_flagged_job_description=None, # default!
                    #is_complex_form=False, # default!
                    apply_type='href',
                    external_apply_url=result.get("QuickApplyHref", "-"),
                    raw_json_result=result,
                    raw_json_job_details=result.get("jobDetails"),
                )
                
                #############################################
                # Get the results here
                #############################################
                
                record_batch.append(models.JobBoardScrapeResults(**data))
            
            ###############################################
            # Bulk Insert
            ###############################################

            to_serialize = models.JobBoardScrapeResults.objects.bulk_create(record_batch)

        except Exception as error:
            logger.error(str(error))
            return False, []
                
        return True, to_serialize
