from django.urls import path
from job.views import (
    GetJobRecordsView,
    JobApplyStartView,
    JobAppliedView,
    JobRejectView,
    DownloadResumeView,
    AsyncRunView,
)

urlpatterns = [
    path('get/records/', GetJobRecordsView.as_view(), name='get_records'),
    path('start/', JobApplyStartView.as_view(), name='job_apply_start'),
    path('applied/', JobAppliedView.as_view(), name='job_applied'),
    path('reject/', JobRejectView.as_view(), name='job_reject'),
    path('download/resume/', DownloadResumeView.as_view(), name='download_resume'),
    path('async/run/', AsyncRunView.as_view(), name='async_run'),
]