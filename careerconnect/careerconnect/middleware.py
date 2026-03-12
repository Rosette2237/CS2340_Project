from django.utils import timezone
from datetime import timedelta
from django.db.models import F

SESSION_TIMEOUT_MINUTES = 30


class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            self._record_activity(request.user)

        return self.get_response(request)

    @staticmethod
    def _record_activity(user):
        try:
            from accounts.models import Profile

            profile = user.profile
            now = timezone.now()

            if profile.last_activity:
                delta = now - profile.last_activity

                if delta < timedelta(minutes=SESSION_TIMEOUT_MINUTES):
                    Profile.objects.filter(pk=profile.pk).update(
                        total_time_on_site=F('total_time_on_site') + delta.total_seconds(),
                        last_activity=now,
                    )
                else:
                    Profile.objects.filter(pk=profile.pk).update(last_activity=now)
            else:
                Profile.objects.filter(pk=profile.pk).update(last_activity=now)

        except Exception:
            pass
