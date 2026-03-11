from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Profile, SavedSearch
from message.models import Conversation, Message
from django.contrib.auth.models import User

def get_sys():
    user = User.objects.get(username="System")
    return user.profile

def profile_match(candidate, searches):
    candidate_skills = [skill.strip().lower() for skill in (candidate.skills or "").split(",") if skill.strip()]
    search_skills = [skill.strip().lower() for skill in (searches.skills or "").split(",") if skill.strip()]

    if search_skills:
        if not any(skill in candidate_skills for skill in search_skills):
            return False;

    if searches.city:
        if (candidate.city or "").strip().lower() != searches.city.strip().lower():
            return False

    if searches.state:
        if (candidate.state or "").strip().lower() != searches.state.strip().lower():
            return False

    return True

@receiver(post_save, sender=Profile)
def notify_recruiter(sender, instance, created, **kwargs):
    if instance.is_recruiter:
        return

    if not instance.is_public:
        return

    def send_notif():
        system = get_sys()

        for search in SavedSearch.objects.filter(is_applicable=True):
            recruiter_profile = search.recruiter.profile

            if profile_match(instance, search):
                conversation, _ = Conversation.objects.get_or_create(
                    recruiter = recruiter_profile,
                    applicant = system
                )

                Message.objects.create(
                    conversation=conversation,
                    sender=system,
                    body=f'Hello, new candidate match found: {instance.user.username}. '
                )

            Profile.objects.filter(id=instance.id).update(notif_check=True)

    transaction.on_commit(send_notif)

