from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='jobs.index'),
]