from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='index'),
    path('create/', views.create_job, name='create'),
    path('<int:job_id>/edit/', views.edit_job, name='edit'),
    path('<int:job_id>/delete/', views.delete_job, name='delete'),
    path('my-jobs/', views.recruiter_jobs, name='recruiter_jobs'),
]