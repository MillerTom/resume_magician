from rest_framework import serializers
from scraper.models import JobBoardResult


class PullJobSerializer(serializers.Serializer):
    numberOfDays = serializers.IntegerField(label="Number of days", min_value=1)
    appConsuming = serializers.CharField(label="App consuming", max_length=100)


class JobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobBoardResult
        fields = "__all__"
