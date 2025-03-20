from django.db import models

class BaseResume(models.Model):
    keyword = models.CharField(max_length=100)
    google_doc_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)