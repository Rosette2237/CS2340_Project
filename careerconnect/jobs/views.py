from django.shortcuts import render
from .models import Job
from django.db.models import Q, Exists, OuterRef

def job_list(request):
    jobs = Job.objects.all().order_by('-posted_at')

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
        from applications.models import Application
        jobs = jobs.annotate(
            user_has_applied=Exists(
                Application.objects.filter(
                    job=OuterRef('pk'),
                    user=request.user
                )
            )
        )

    context = {
        'jobs': jobs,
        'values': request.GET 
    }
    return render(request, 'jobs/job_list.html', context)