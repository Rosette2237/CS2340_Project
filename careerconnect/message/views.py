from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.utils.timesince import timesince
import json
from .models import Conversation, Message
from accounts.models import Profile

User = get_user_model()

@login_required
def inbox(request):
    profile = request.user.profile

    if profile.is_recruiter:
        conversations = Conversation.objects.filter(
            recruiter=profile
        ).select_related('applicant').prefetch_related('messages')
    else:
        conversations = Conversation.objects.filter(
            applicant=profile
        ).select_related('recruiter').prefetch_related('messages')

    active_conv = None
    messages = []
    other_user = None

    conv_id = request.GET.get('conv')
    if conv_id:
        active_conv = get_object_or_404(Conversation, id=conv_id)

        if profile != active_conv.recruiter and profile != active_conv.applicant:
            raise PermissionDenied("You are not part of this conversation.")

        Message.objects.filter(
            conversation=active_conv,
            is_read=False
        ).exclude(sender=profile).update(is_read=True)

        messages = active_conv.messages.select_related('sender').all()
        other_user = active_conv.get_other_user(profile)

    return render(request, 'message/inbox.html', {
        'conversations': conversations,
        'active_conv': active_conv,
        'messages': messages,
        'other_user': other_user,
    })

@login_required
def conversation(request, conversation_id):
    profile = request.user.profile
    conv = get_object_or_404(Conversation, id=conversation_id)

    if profile != conv.recruiter and profile != conv.applicant:
        raise PermissionDenied("You are not part of this conversation.")

    Message.objects.filter(
        conversation=conv,
        is_read=False
    ).exclude(sender=profile).update(is_read=True)

    messages = conv.messages.select_related('sender').all()
    other_user = conv.get_other_user(profile)

    return render(request, 'message/conversation.html', {
        'conversation': conv,
        'messages': messages,
        'other_user': other_user,
    })


@login_required
def start_conversation(request, applicant_id):
    if not request.user.profile.is_recruiter:
        raise PermissionDenied("Only recruiters can start conversations.")

    applicant = get_object_or_404(Profile, id=applicant_id)

    conv, created = Conversation.objects.get_or_create(
        recruiter=request.user.profile,
        applicant=applicant
    )

    return redirect(f"{reverse('inbox')}?conv={conv.id}")


@login_required
@require_POST
def send_message(request, conversation_id):
    profile = request.user.profile
    conv = get_object_or_404(Conversation, id=conversation_id)

    if profile != conv.recruiter and profile != conv.applicant:
        return JsonResponse({'error': 'Not a participant'}, status=403)

    data = json.loads(request.body)
    body = data.get('body', '').strip()
    if not body:
        return JsonResponse({'error': 'Empty message'}, status=400)

    msg = Message.objects.create(
        conversation=conv,
        sender=profile,
        body=body
    )

    return JsonResponse({
        'id': msg.id,
        'body': msg.body,
        'timestamp': msg.time_stamp.strftime('%H:%M'),
        'sender_id': profile.id,
    })


@login_required
def poll_messages(request, conversation_id):
    profile = request.user.profile
    conv = get_object_or_404(Conversation, id=conversation_id)

    if profile != conv.recruiter and profile != conv.applicant:
        return JsonResponse({'error': 'Not a participant'}, status=403)

    last_id = request.GET.get('last_id', 0)
    new_messages = Message.objects.filter(
        conversation=conv,
        id__gt=last_id
    ).exclude(sender=profile).select_related('sender')

    new_messages.update(is_read=True)

    return JsonResponse({
        'messages': [
            {
                'id': msg.id,
                'body': msg.body,
                'timestamp': msg.time_stamp.strftime('%H:%M'),
                'sender_id': msg.sender.id,
            }
            for msg in new_messages
        ]
    })