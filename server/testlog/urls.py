from testlog.views import LogView
from django.urls import path

urlpatterns = [
    path('', LogView.as_view(), name='log'),

]