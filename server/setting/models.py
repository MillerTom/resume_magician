from django.db import models

class DataSource(models.Model):
    value = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Data Source'
        db_table = 'data_source'

class SupervisorStatus(models.Model):
    is_locked = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Supervisor Status'
        db_table = 'supervisor_status'

class LogEntry(models.Model):
    id=models.AutoField(primary_key=True)
    message=models.TextField()
    severity=models.CharField(max_length=20)
    source=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Log'
        db_table = 'setting_log'