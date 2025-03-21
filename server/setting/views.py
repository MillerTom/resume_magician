from rest_framework.response import Response
from rest_framework import generics, status as http_status
from setting.models import DataSource
from setting.utils import logger

class GetDataSourceView(generics.GenericAPIView):
    def get(self, request):
        logger.info('get data source')
        data_source = DataSource.objects.first()
        return Response({'data_source': data_source.value}, status=http_status.HTTP_200_OK)
    
class UpdateDataSourceView(generics.GenericAPIView):
    def post(self, request):
        logger.info('update data source')
        data = request.data
        data_source = DataSource.objects.first()
        data_source.value = data['data_source']
        data_source.save()
        return Response({'data_source': data['data_source']}, status=http_status.HTTP_200_OK)