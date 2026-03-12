from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application
from jobs.models import Job
import json
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST


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

@login_required
def kanban_board(request):
    if not getattr(request.user.profile, 'is_recruiter', False):
        return HttpResponseForbidden("Only recruiters can view the pipeline board.")

    recruiter_jobs = Job.objects.filter(recruiter=request.user).order_by('title')

    all_apps = (
        Application.objects
        .filter(job__recruiter=request.user)
        .select_related('user', 'user__profile', 'job')
        .order_by('-applied_at')
    )

    STATUS_META = [
        {'key': 'applied',   'label': 'Applied',      'color': '#6c757d'},
        {'key': 'review',    'label': 'Under Review',  'color': '#17a2b8'},
        {'key': 'interview', 'label': 'Interview',     'color': '#ffc107'},
        {'key': 'offer',     'label': 'Offer',         'color': '#28a745'},
        {'key': 'closed',    'label': 'Closed',        'color': '#dc3545'},
    ]

    for col in STATUS_META:
        col['apps'] = []

    col_map = {col['key']: col for col in STATUS_META}
    for app in all_apps:
        if app.status in col_map:
            col_map[app.status]['apps'].append(app)

    return render(request, 'applications/kanban.html', {
        'columns': STATUS_META,
        'jobs': recruiter_jobs,
    })


@login_required
@require_POST
def update_application_status(request, application_id):
    """
    AJAX endpoint called by Kanban drag-and-drop.
    Only the recruiter who owns the job may update an application's status.
    Expects JSON body: { "status": "<new_status_key>" }
    """
    if not getattr(request.user.profile, 'is_recruiter', False):
        return JsonResponse({'error': 'Forbidden'}, status=403)

    try:
        app = Application.objects.get(id=application_id, job__recruiter=request.user)
    except Application.DoesNotExist:
        return JsonResponse({'error': 'Application not found'}, status=404)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)

    new_status = data.get('status', '').strip()
    valid_statuses = [choice[0] for choice in Application.STATUS_CHOICES]

    if new_status not in valid_statuses:
        return JsonResponse(
            {'error': f'Invalid status. Must be one of: {valid_statuses}'},
            status=400,
        )

    app.status = new_status
    app.save(update_fields=['status', 'updated_at'])

    return JsonResponse({'success': True, 'status': new_status})
