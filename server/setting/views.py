from rest_framework.response import Response
from rest_framework import generics, status as http_status
from setting.models import DataSource

class GetDataSourceView(generics.GenericAPIView):
    def get(self, request):
        data_source = DataSource.objects.first()
        if not data_source:
            data_source = DataSource(value='google_sheet')
            data_source.save()
        return Response({'data_source': data_source.value}, status=http_status.HTTP_200_OK)
    
class UpdateDataSourceView(generics.GenericAPIView):
    def post(self, request):
        data = request.data
        data_source = DataSource.objects.first()
        if not data_source:
            data_source = DataSource(value=data['data_source'])
            data_source.save()
        data_source.value = data['data_source']
        data_source.save()
        return Response({'data_source': data['data_source']}, status=http_status.HTTP_200_OK)