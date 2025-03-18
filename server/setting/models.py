from django.db import models

class DataSource(models.Model):
    value = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Data Source'
        db_table = 'data_source'
