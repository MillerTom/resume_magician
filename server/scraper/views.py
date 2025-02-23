from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from rest_framework.permissions import DjangoObjectPermissions
from rest_framework import generics, status as http_status
from scraper.models import Scraper, jobboardscraperesults,jobboardscrapehistory, configdice, configindeed, configlinkedin, configziprecruiter
from scraper.serializers import jobboardscrapehistorySerializer, jobboardscraperesultsSerializer, PullJobSerializer,configdiceSerializer, configindeedSerializer, configlinkedinSerializer, configziprecruiterSerializer
from rest_framework.decorators import action
from django.views import generic

class IndexView(generic.ListView):
    template_name = "jobList.html"
    context_object_name = "jobList"
    
    def get_queryset(self):
        """Return the last five published questions."""
        return configdice.objects.all()
   
  
class JobPagination(PageNumberPagination):
    page_size = 1

class configziprecruiterViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = configziprecruiter.objects.all()
    pagination_class = JobPagination
    serializer_class = configziprecruiterSerializer

    @action(detail=False, methods=['get'])
    def list_view(self, request):
        """Renders a template with a list of items."""
        items = self.get_queryset()
        return render(request, 'admin/configziprecruiter.html', {'items': items})

class configlinkedinViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = configlinkedin.objects.all()
    pagination_class = JobPagination
    serializer_class = configlinkedinSerializer

    @action(detail=False, methods=['get'])
    def list_view(self, request):
        """Renders a template with a list of items."""
        items = self.get_queryset()
        return render(request, 'admin/configlinkedin.html', {'items': items})

class configindeedViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = configindeed.objects.all()
    pagination_class = JobPagination
    serializer_class = configindeedSerializer

    @action(detail=False, methods=['get'])
    def list_view(self, request):
        """Renders a template with a list of items."""
        items = self.get_queryset()
        return render(request, 'admin/configindeed.html', {'items': items})
    
class configdiceViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = configdice.objects.all()
    pagination_class = JobPagination
    serializer_class = configdiceSerializer

    @action(detail=False, methods=['get'])
    def list_view(self, request):
        """Renders a template with a list of items."""
        items = self.get_queryset()
        return render(request, 'admin/configdice.html', {'items': items})


class jobboardscrapehistoryViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = jobboardscrapehistory.objects.all()
    serializer_class = jobboardscrapehistorySerializer
    pagination_class = JobPagination

    @action(detail=False, methods=['get'])
    def list_view(self, request):
        """Renders a template with a list of items."""
        items = self.get_queryset()
        return render(request, 'admin/history.html', {'items': items})

class jobboardscraperesultsViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = jobboardscraperesults.objects.all()
    serializer_class = jobboardscraperesultsSerializer
    pagination_class = JobPagination

    @action(detail=False, methods=['get'])
    def list_view(self, request):
        """Renders a template with a list of items."""
        items = self.get_queryset()
        return render(request, 'admin/jobs.html', {'items': items})