from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from jobs.models import Job


def index(request):
    locations = []
    for job in Job.objects.filter(location_lat__isnull=False, location_long__isnull=False):
        locations.append({
            'id': job.id,
            'title': job.title,
            'location': f"{job.city}, {job.state}",
            'location_lat': float(job.location_lat),
            'location_long': float(job.location_long),
        })

    template_data = {
        'title': 'Maps',
        'locations': locations,
    }
    return render(request, 'maps/index.html', {'template_data': template_data})


@login_required
def recruiter_map(request):
    if not getattr(getattr(request.user, 'profile', None), 'is_recruiter', False):
        return HttpResponseForbidden("Only recruiters can access this page.")

    from applications.models import Application

    recruiter_jobs = Job.objects.filter(recruiter=request.user).order_by('-posted_at')

    # Build sidebar job list and geocoded office pins
    jobs_sidebar = []
    job_locations = []
    for job in recruiter_jobs:
        applicant_count = Application.objects.filter(job=job).count()
        jobs_sidebar.append({
            'id': job.id,
            'title': job.title,
            'city': job.city,
            'state': job.state,
            'applicant_count': applicant_count,
            'has_location': bool(job.location_lat and job.location_long),
        })
        if job.location_lat and job.location_long:
            job_locations.append({
                'id': job.id,
                'title': job.title,
                'location': f"{job.city}, {job.state}",
                'lat': float(job.location_lat),
                'lng': float(job.location_long),
            })

    # Build applicant location pins (from applicants' profiles)
    applicant_locations = []
    for application in (Application.objects
                        .filter(job__recruiter=request.user)
                        .select_related('user__profile', 'job')):
        profile = getattr(application.user, 'profile', None)
        if profile and profile.location_lat and profile.location_long:
            applicant_locations.append({
                'job_title': application.job.title,
                'lat': float(profile.location_lat),
                'lng': float(profile.location_long),
            })

    return render(request, 'maps/recruiter_map.html', {
        'jobs': jobs_sidebar,
        'job_locations': job_locations,
        'applicant_locations': applicant_locations,
    })
