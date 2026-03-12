from django.urls import path
from . import views

urlpatterns = [
    path('',                     views.reports_dashboard,       name='reports.dashboard'),
    path('export/jobs/',         views.export_jobs_csv,         name='reports.export_jobs'),
    path('export/applications/', views.export_applications_csv, name='reports.export_applications'),
    path('export/users/',        views.export_users_csv,        name='reports.export_users'),
    path('export/searches/',     views.export_searches_csv,     name='reports.export_searches'),
]