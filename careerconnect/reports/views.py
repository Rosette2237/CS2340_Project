import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def reports_dashboard(request):
    from applications.models import Application
    from jobs.models import Job
    from accounts.models import Profile

    stats = {
        'total_jobs':         Job.objects.count(),
        'total_applications': Application.objects.count(),
        'total_candidates':   Profile.objects.filter(is_recruiter=False).count(),
        'total_recruiters':   Profile.objects.filter(is_recruiter=True).count(),
    }

    status_counts = []
    for key, label in Application.STATUS_CHOICES:
        status_counts.append({
            'label': label,
            'count': Application.objects.filter(status=key).count(),
        })

    top_jobs = []
    for job in Job.objects.select_related('recruiter').order_by('-posted_at')[:20]:
        top_jobs.append({
            'title':     job.title,
            'recruiter': job.recruiter.username,
            'count':     Application.objects.filter(job=job).count(),
        })
    top_jobs = sorted(top_jobs, key=lambda j: j['count'], reverse=True)[:5]

    return render(request, 'reports/dashboard.html', {
        'stats':         stats,
        'status_counts': status_counts,
        'top_jobs':      top_jobs,
    })


@staff_member_required
def export_jobs_csv(request):
    from jobs.models import Job
    from applications.models import Application

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="jobs_export.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Title', 'Recruiter Username', 'Recruiter Email',
        'City', 'State', 'Job Type', 'Salary Min', 'Salary Max',
        'Visa Sponsorship', 'Skills Required', 'Posted At', 'Application Count',
    ])

    for job in Job.objects.select_related('recruiter').order_by('-posted_at'):
        writer.writerow([
            job.id, job.title, job.recruiter.username, job.recruiter.email,
            job.city, job.state, job.get_job_type_display(),
            job.salary_min, job.salary_max,
            'Yes' if job.visa_sponsorship else 'No',
            job.skills_required,
            job.posted_at.strftime('%Y-%m-%d %H:%M'),
            Application.objects.filter(job=job).count(),
        ])

    return response


@staff_member_required
def export_applications_csv(request):
    from applications.models import Application

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="applications_export.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Applicant Username', 'Applicant Email',
        'Job ID', 'Job Title', 'Recruiter Username',
        'Job City', 'Job State', 'Status',
        'Applied At', 'Last Updated', 'Note',
    ])

    qs = (Application.objects
          .select_related('user', 'job', 'job__recruiter')
          .order_by('-applied_at'))

    for app in qs:
        writer.writerow([
            app.id, app.user.username, app.user.email,
            app.job.id, app.job.title, app.job.recruiter.username,
            app.job.city, app.job.state,
            app.get_status_display(),
            app.applied_at.strftime('%Y-%m-%d %H:%M'),
            app.updated_at.strftime('%Y-%m-%d %H:%M'),
            app.tailored_note or '',
        ])

    return response


@staff_member_required
def export_users_csv(request):
    from accounts.models import Profile

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users_export.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'User ID', 'Username', 'Email', 'Role',
        'City', 'State', 'Headline', 'Skills',
        'Has LinkedIn', 'Has Portfolio', 'Public Profile', 'Date Joined',
    ])

    for profile in Profile.objects.select_related('user').order_by('user__date_joined'):
        writer.writerow([
            profile.user.id, profile.user.username, profile.user.email,
            'Recruiter' if profile.is_recruiter else 'Candidate',
            profile.city, profile.state, profile.headline, profile.skills,
            'Yes' if profile.linkedin_link else 'No',
            'Yes' if profile.portfolio_link else 'No',
            'Yes' if profile.is_public else 'No',
            profile.user.date_joined.strftime('%Y-%m-%d'),
        ])

    return response


@staff_member_required
def export_searches_csv(request):
    from accounts.models import SavedSearch

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="saved_searches_export.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Recruiter Username', 'Skills Filter',
        'City Filter', 'State Filter', 'Notifications Active', 'Created At',
    ])

    for s in SavedSearch.objects.select_related('recruiter').order_by('-creation_date'):
        writer.writerow([
            s.id, s.recruiter.username, s.skills,
            s.city, s.state,
            'Yes' if s.is_applicable else 'No',
            s.creation_date.strftime('%Y-%m-%d %H:%M'),
        ])

    return response