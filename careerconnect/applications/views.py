from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application
from jobs.models import Job

@login_required
def application_list(request):
    applications = Application.objects.filter(user=request.user).order_by('-applied_at')
    return render(request, 'applications/application_list.html', {'applications': applications})

@login_required
def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)
    return render(request, 'applications/application_details.html', {'application': application})

@login_required
def apply_to_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    
    if Application.objects.filter(user=request.user, job=job).exists():
        messages.info(request, 'You have already applied to this job.')
        return redirect('applications.index')
    
    if request.method == 'POST':
        tailored_note = request.POST.get('tailored_note', '').strip()
        
        application = Application.objects.create(
            user=request.user,
            job=job,
            tailored_note=tailored_note if tailored_note else "Happy to apply for this position!"
        )
        
        messages.success(request, f'Successfully applied to {job.title}!')
        return redirect('applications.index')
    
    return render(request, 'applications/apply_form.html', {'job': job})