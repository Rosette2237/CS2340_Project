from django.shortcuts import render
from .models import Job
from .utils import calculate_match
from django.db.models import Q, Exists, OuterRef

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

    jobs = jobs.order_by("-posted_at")

    if request.user.is_authenticated:
        from applications.models import Application
        jobs = jobs.annotate(
            user_has_applied=Exists(
                Application.objects.filter(
                    job=OuterRef('pk'),
                    user=request.user
                )
            )
        )
    
        profile = getattr(request.user, "profile", None)
        if profile is not None:
            jobs_list = list(jobs)  # evaluate queryset once
            for job in jobs_list:
                job.match_percent = calculate_match(job.skills_required, profile.skills)
            jobs = sorted(
                jobs_list,
                key=lambda j: (
                    -(getattr(j, "match_percent", 0) or 0),
                    -j.posted_at.timestamp(),
                ),
            )

    context = {
        'jobs': jobs,
        'values': request.GET
    }
    return render(request, 'jobs/job_list.html', context)
