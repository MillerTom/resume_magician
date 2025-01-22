from django.urls import path
from scraper.views import ScraperStartView

urlpatterns = [
    path('start/', ScraperStartView.as_view(), name='start_scraping'),
]