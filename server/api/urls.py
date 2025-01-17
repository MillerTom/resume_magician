from django.urls import path

from api import endpoints

app_name = "api"

urlpatterns = [
    path(
        "scrape/ziprecruiter", 
        view=endpoints.ScrapeZipRecruiterEndpoint.as_view(), 
        name="scrape-ziprecruiter"
    )
]
