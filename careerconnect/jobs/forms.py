from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    address = forms.CharField(
        max_length=300,
        required=False,
        label="Address (optional)",
    )

    skills_required = forms.CharField(
        max_length=500,
        required=False,
        label="Skills Required (Comma-Separated List)",
    )

    visa_sponsorship = forms.BooleanField(
        required=False,
        label="Visa Sponsorship: ",
    )

    class Meta:
        model = Job
        exclude = ['recruiter', 'posted_at', 'location_lat', 'location_long']
