from django.urls import path
from auth.views import GetTokenView, GetUserView

urlpatterns = [
    path('get/token/', GetTokenView.as_view(), name='get_token'),
    path('get/user/', GetUserView.as_view(), name='get_user'),
]