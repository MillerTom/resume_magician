from rest_framework import serializers


from scrapping import models


class JobBoardScrapeResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JobBoardScrapeResults
        fields = "__all__"

