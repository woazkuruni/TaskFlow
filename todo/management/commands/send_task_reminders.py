from datetime import datetime, time, timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from todo.models import UserProfile, add_task


class Command(BaseCommand):
    help = 'Send due-task reminder emails that are ready to be sent.'

    def handle(self, *args, **options):
        now = timezone.localtime()
        tasks = add_task.objects.filter(
            owner__isnull=False,
            is_complete=False,
            due_date__isnull=False,
            reminder_minutes__gt=0,
            email_reminder_sent_at__isnull=True,
        ).select_related('owner')

        sent_count = 0

        for task in tasks:
            user = task.owner
            if not user.email:
                continue

            profile, _ = UserProfile.objects.get_or_create(user=user)
            if not profile.email_reminders:
                continue

            due_clock = task.due_time or time(23, 59, 59)
            due_datetime = datetime.combine(task.due_date, due_clock)
            due_datetime = timezone.make_aware(due_datetime, timezone.get_current_timezone())
            reminder_at = due_datetime - timedelta(minutes=task.reminder_minutes)

            if not (reminder_at <= now <= due_datetime):
                continue

            due_text = timezone.localtime(due_datetime).strftime('%d %b %Y, %I:%M %p')
            subject = f'TaskFlow reminder: {task.task}'
            message = (
                f'Hi {user.first_name or user.username},\n\n'
                f'This is a reminder for your task:\n\n'
                f'{task.task}\n'
                f'Due: {due_text}\n\n'
                'Open TaskFlow to review or update the task.'
            )

            try:
                sent = send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
            except Exception as error:
                self.stderr.write(self.style.ERROR(f'Could not send reminder for task {task.pk}: {error}'))
                continue

            if sent:
                task.email_reminder_sent_at = timezone.now()
                task.save(update_fields=['email_reminder_sent_at'])
                sent_count += 1
                self.stdout.write(self.style.SUCCESS(f'Reminder sent to {user.email}: {task.task}'))

        self.stdout.write(f'{sent_count} reminder email(s) sent.')
