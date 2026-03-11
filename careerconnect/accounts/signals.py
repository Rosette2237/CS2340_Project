from .models import Profile
from django.contrib.auth.models import User

def get_sys():
    user, _ = User.objects.get_or_create(
        username="System",
        defaults={
            "email": "system@careerconnect.com",
            "is_staff": False,
            "is_superuser": False,
            "is_active": True,
        }
    )

    profile, _ = Profile.objects.get_or_create(
        user=user,
        defaults={
            "is_recruiter": True,
            "is_public": False,
        }
    )

    return profile

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
