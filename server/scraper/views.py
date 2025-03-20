from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet
from rest_framework import generics, status as http_status
from scraper.models import Scraper, JobBoardResult
from scraper.serializers import JobsSerializer, PullJobSerializer
from scraper.tasks import run_actor
from resume.utils import analyze_job

class ScraperStartView(generics.GenericAPIView):
    serializer_class = PullJobSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            scrapers = Scraper.objects.filter(is_active=True)
            for scraper in scrapers:
                configurations = scraper.scraper_configurations.filter(is_active=True)
                for configuration in configurations:
                    run_actor(scraper, configuration)
            return Response(
                {
                    "status": "success",
                    "message": "successfully scheduled tasks. Wait for a moment to get the results.",
                },
                status=http_status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)


class ScraperGetView(generics.GenericAPIView):
    def post(self, request):
        data = request.data
        run_id = data['runID']



class JobPagination(PageNumberPagination):
    page_size = 20


class JobBoardResultViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = JobBoardResult.objects.all()
    serializer_class = JobsSerializer
    pagination_class = JobPagination