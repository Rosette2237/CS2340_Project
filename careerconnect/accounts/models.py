from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    headline = models.CharField(max_length=200, blank=True)
    skills = models.TextField(help_text="Comma separated list of skills", blank=True)
    education = models.TextField(help_text="Details about your education", blank=True)
    work_experience = models.TextField(help_text="Details about your work history", blank=True)
    linkedin_link = models.URLField(blank=True)
    portfolio_link = models.URLField(blank=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
