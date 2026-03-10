from django.db import models
from django.conf import settings
from accounts.models import Profile

class Conversation(models.Model):
    recruiter = models.ForeignKey(
        Profile,
        related_name="recruiter_conversation",
        on_delete=models.CASCADE
    )
    applicant = models.ForeignKey(
        Profile,
        related_name="applicant_conversation",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('recruiter', 'applicant')
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.recruiter} <-> {self.applicant}"
    
    def get_other_user(self, user):
        return self.applicant if user == self.recruiter else self.recruiter
    
class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        related_name="messages",
        on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        Profile,
        related_name="sent_message",
        on_delete=models.CASCADE
    )

    body = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=True)

    class Meta:
        ordering = ['time_stamp']

    def __str__(self):
        return f"{self.sender} at {self.time_stamp}: {self.body}"