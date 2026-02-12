from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    JOB_TYPES = [
        ('remote', 'Remote'),
        ('onsite', 'On-site'),
        ('hybrid', 'Hybrid'),
    ]

    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    skills_required = models.CharField(max_length=500, help_text="Comma-separated skills")
    job_type = models.CharField(max_length=10, choices=JOB_TYPES)
    visa_sponsorship = models.BooleanField(default=False)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title