from django.urls import path
from job.views import GetJobRecordsView, JobApplyStartView, JobAppliedView

urlpatterns = [
    path('get/records/', GetJobRecordsView.as_view(), name='get_records'),
    path('start/', JobApplyStartView.as_view(), name='job_apply_start'),
    path('applied/', JobAppliedView.as_view(), name='job_applied'),
]