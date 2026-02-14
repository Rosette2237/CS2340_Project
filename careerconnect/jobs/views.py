from django.shortcuts import render
from .models import Job
from .utils import calculate_match
from django.db.models import Q

def job_list(request):
    jobs = Job.objects.all()

    title_query = request.GET.get('title')
    location_query = request.GET.get('location')
    job_type_query = request.GET.get('job_type')
    visa_query = request.GET.get('visa_sponsorship')

    if title_query:
        jobs = jobs.filter(title__icontains=title_query)

    if location_query:
        jobs = jobs.filter(location__icontains=location_query)

    if job_type_query:
        jobs = jobs.filter(job_type=job_type_query)

    if visa_query == 'on':
        jobs = jobs.filter(visa_sponsorship=True)

    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            for job in jobs:
                job.match_percent = calculate_match(job.skills_required, profile.skills)
            jobs = sorted(jobs, key=lambda x: (-x.match_percent, -x.posted_at.timestamp()))
        except:
            pass

    context = {
        'jobs': jobs,
        'values': request.GET
    }
    return render(request, 'jobs/job_list.html', context)
