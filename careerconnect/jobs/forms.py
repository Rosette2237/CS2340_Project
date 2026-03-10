from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ['recruiter', 'posted_at', 'location_lat', 'location_long']