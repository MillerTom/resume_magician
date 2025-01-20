from django.db import models

class UserInfo(models.Model):
    email = models.CharField(max_length=200, default='')
    name = models.CharField(max_length=200, default='')
    created_at = models.DateTimeField(auto_now_add=True)

class Job(models.Model):
    user = models.ForeignKey(UserInfo, related_name='user_jobs', on_delete=models.CASCADE, null=True)
    url = models.CharField(max_length=1000, default='')
    index = models.IntegerField(default=-1)
    created_at = models.DateTimeField(auto_now_add=True)
    applied_at = models.DateTimeField(null=True)