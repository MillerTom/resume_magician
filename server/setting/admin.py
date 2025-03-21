from django.contrib import admin
from setting.models import DataSource, SupervisorStatus, LogEntry

admin.site.register(DataSource)
admin.site.register(SupervisorStatus)
admin.site.register(LogEntry)