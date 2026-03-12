import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import Application


@admin.action(description="Export selected applications as CSV")
def export_applications_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="applications_export.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Applicant Username', 'Applicant Email',
        'Job Title', 'Job City', 'Job State',
        'Status', 'Applied At', 'Note',
    ])

    for app in queryset.select_related('user', 'job').order_by('-applied_at'):
        writer.writerow([
            app.id,
            app.user.username,
            app.user.email,
            app.job.title,
            app.job.city,
            app.job.state,
            app.get_status_display(),
            app.applied_at.strftime('%Y-%m-%d %H:%M'),
            app.tailored_note or '',
        ])

    return response


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    actions       = [export_applications_csv]
    list_display  = ['id', 'user', 'job', 'status', 'applied_at']
    list_filter   = ['status', 'applied_at']
    search_fields = ['user__username', 'job__title']
    ordering      = ['-applied_at']