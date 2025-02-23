from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import jobboardscraperesultsViewSet, jobboardscrapehistoryViewSet, configdiceViewSet, configindeedViewSet, configlinkedinViewSet, configziprecruiterViewSet
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register(r'indeed', configindeedViewSet)
router.register(r'dice', configdiceViewSet)
router.register(r'linkedin', configlinkedinViewSet)
router.register(r'ziprecruiter', configziprecruiterViewSet)
router.register(r'history', jobboardscrapehistoryViewSet)
router.register(r'jobs', jobboardscraperesultsViewSet)

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    # path("jobs/", jobboardscraperesults_list_view, name="results"),
    path('', include(router.urls)),
]