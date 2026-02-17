from django.urls import path
from . import views

urlpatterns = [
    path('', views.application_list, name='applications.index'), 
    path('apply/<int:job_id>/', views.apply_to_job, name='applications.apply'), 
    path('<int:pk>/', views.application_detail, name='applications.detail'),
]