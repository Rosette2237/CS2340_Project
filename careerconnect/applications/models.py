from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job

class Application(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('review', 'Under Review'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('closed', 'Closed'),
    ]    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    tailored_note = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} - {self.job.title} ({self.status})"