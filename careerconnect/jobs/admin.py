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


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    actions = [duplicate_selected_jobs]
