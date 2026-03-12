from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Job
from accounts.models import Profile
from .forms import JobForm
from .utils import calculate_match
from .geocoding import geocode_job
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
        jobs = jobs.filter(
            Q(city__icontains=location_query) | Q(state__icontains=location_query)
        )

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
            jobs_list = list(jobs)
            for job in jobs_list:
                job.match_percent = calculate_match(job.skills_required, profile.skills)
            jobs = sorted(
                jobs_list,
                key=lambda j: (
                    -(getattr(j, "match_percent", 0) or 0),
                    -j.posted_at.timestamp(),
                ),
            )

    is_recruiter = False
    if request.user.is_authenticated:
        is_recruiter = getattr(getattr(request.user, 'profile', None), 'is_recruiter', False)

    context = {
        'jobs': jobs,
        'values': request.GET,
        'is_recruiter': is_recruiter,
    }
    return render(request, 'jobs/job_list.html', context)

@login_required
def create_job(request):
    if not getattr(request.user.profile, 'is_recruiter', False):
        return HttpResponseForbidden("Only recruiters can post jobs.")

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            lat, lng = geocode_job(job.address, job.city, job.state)
            job.location_lat = lat
            job.location_long = lng
            job.save()
            return redirect('jobs:index')
    else:
        form = JobForm()
    return render(request, 'jobs/job_form.html', {'form': form})

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.user != job.recruiter:
        return HttpResponseForbidden("You can only edit your own job postings.")

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            job = form.save(commit=False)
            lat, lng = geocode_job(job.address, job.city, job.state)
            job.location_lat = lat
            job.location_long = lng
            job.save()
            return redirect('jobs:index')
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/job_form.html', {'form': form})

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.user != job.recruiter:
        return HttpResponseForbidden("You can only delete your own job postings.")

    if request.method == 'POST':
        job.delete()
        return redirect('jobs:index')

    return render(request, 'jobs/delete_job.html', {'job': job})

@login_required
def recruiter_jobs(request):
    if not getattr(request.user.profile, 'is_recruiter', False):
        return HttpResponseForbidden("Only recruiters can view this page.")

    jobs = Job.objects.filter(recruiter=request.user).order_by('-posted_at')

    return render(request, 'jobs/recruiter_jobs.html', {'jobs': jobs})
