from django.urls import path
from setting.views import GetDataSourceView, UpdateDataSourceView

urlpatterns = [
    path('data_source/get/', GetDataSourceView.as_view(), name='get_data_source'),
    path('data_source/update/', UpdateDataSourceView.as_view(), name='update_data_source'),
]