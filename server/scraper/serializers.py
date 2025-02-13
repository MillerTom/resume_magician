from rest_framework import serializers
from scraper.models import jobboardscrapehistory, jobboardscraperesults


class PullJobSerializer(serializers.Serializer):
    numberOfDays = serializers.IntegerField(label="Number of days", min_value=1)
    appConsuming = serializers.CharField(label="App consuming", max_length=100)

class jobboardscraperesultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = jobboardscraperesults
        fields = '__all__'  # Or specify the fields you want to include

class jobboardscrapehistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = jobboardscrapehistory
        fields = '__all__'  # Or specify the fields you want to include        