import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import Job


@admin.action(description="Duplicate selected jobs")
def duplicate_selected_jobs(modeladmin, request, queryset):
    duplicated = 0
    for job in queryset:
        Job.objects.create(
            recruiter=job.recruiter,
            title=job.title,
            description=job.description,
            location=job.location,
            salary_min=job.salary_min,
            salary_max=job.salary_max,
            skills_required=job.skills_required,
            job_type=job.job_type,
            visa_sponsorship=job.visa_sponsorship,
            location_lat=job.location_lat,
            location_long=job.location_long,
        )
        duplicated += 1
    modeladmin.message_user(request, f"Duplicated {duplicated} job(s).")


@admin.action(description="Export selected jobs as CSV")
def export_jobs_csv(modeladmin, request, queryset):
    from applications.models import Application

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="jobs_export.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Title', 'Recruiter', 'City', 'State',
        'Job Type', 'Salary Min', 'Salary Max',
        'Visa Sponsorship', 'Posted At', 'Application Count',
    ])

    for job in queryset.select_related('recruiter').order_by('-posted_at'):
        writer.writerow([
            job.id,
            job.title,
            job.recruiter.username,
            job.city,
            job.state,
            job.get_job_type_display(),
            job.salary_min,
            job.salary_max,
            'Yes' if job.visa_sponsorship else 'No',
            job.posted_at.strftime('%Y-%m-%d %H:%M'),
            Application.objects.filter(job=job).count(),
        ])

    return response


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    actions = [duplicate_selected_jobs, export_jobs_csv]  # ✨ export_jobs_csv added
    list_display  = ['title', 'recruiter', 'city', 'state', 'job_type', 'posted_at']
    list_filter   = ['job_type', 'visa_sponsorship']
    search_fields = ['title', 'recruiter__username']