from django.contrib.auth.models import User
from django.db import models


class add_task(models.Model):
    REMINDER_CHOICES = [
        (0, 'No reminder'),
        (15, '15 minutes before'),
        (60, '1 hour before'),
        (1440, '1 day before'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    task = models.CharField(max_length=250)
    is_complete = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    due_time = models.TimeField(null=True, blank=True)
    reminder_minutes = models.IntegerField(choices=REMINDER_CHOICES, default=0)
    email_reminder_sent_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='taskflow_profile')
    email_reminders = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
