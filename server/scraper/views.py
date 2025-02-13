from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet
from rest_framework import generics, status as http_status
from scraper.models import Scraper, jobboardscraperesults,jobboardscrapehistory
from scraper.serializers import jobboardscrapehistorySerializer, jobboardscraperesultsSerializer, PullJobSerializer

class JobPagination(PageNumberPagination):
    page_size = 20


class jobboardscrapehistoryViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = jobboardscrapehistory.objects.all()
    serializer_class = jobboardscrapehistorySerializer
    pagination_class = JobPagination

class jobboardscraperesultsViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = jobboardscraperesults.objects.all()
    serializer_class = jobboardscraperesultsSerializer
    pagination_class = JobPagination