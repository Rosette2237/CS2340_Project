from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    is_recruiter = models.BooleanField(default=False, help_text="Check this box if you are a recruiter")
    headline = models.CharField(max_length=200, blank=True)
    skills = models.TextField(help_text="Comma separated list of skills", blank=True)
    education = models.TextField(help_text="Details about your education", blank=True)
    work_experience = models.TextField(help_text="Details about your work history", blank=True)
    linkedin_link = models.URLField(blank=True)
    portfolio_link = models.URLField(blank=True)
    is_public = models.BooleanField(default=True)
    address = models.CharField(max_length=300, blank=True, help_text="Street address (optional)")
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    location_lat = models.DecimalField(decimal_places=6, max_digits=9, null=True, blank=True)
    location_long = models.DecimalField(decimal_places=6, max_digits=9, null=True, blank=True)
    notif_check = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class SavedSearch(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    skills = models.CharField(max_length=500, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_applicable = models.BooleanField(default=True)

    def __str__(self):
        return f'Saved Search {self.id} by {self.recruiter} at {self.creation_date:%Y-%m-%d %H:%M}'

    class Meta:
        verbose_name = 'Saved Search'
        verbose_name_plural = 'Saved Seaches'

