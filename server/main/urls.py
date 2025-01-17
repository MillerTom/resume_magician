from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

admin.site.site_header = "Apply Job Forever"
admin.site.site_title = "Apply Job Forever Admin Portal"
admin.site.index_title = "Apply Job Forever!"

schema_view = get_schema_view(
   openapi.Info(
      title="Apply Forever API",
      default_version='v1',
      description="Apply Forever API",
      terms_of_service="",
      contact=openapi.Contact(email="contact@applyjobs"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('auth/', include('auth.urls')),
    #path('job/', include('job.urls')),
    path('api/', include('api.urls', namespace='api')),
	path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
