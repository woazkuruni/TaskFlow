from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def assign_old_tasks(apps, schema_editor):
    Task = apps.get_model('todo', 'add_task')
    User = apps.get_model('auth', 'User')
    owner = User.objects.filter(is_superuser=True).order_by('id').first()
    if owner:
        Task.objects.filter(owner__isnull=True).update(owner=owner)


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todo', '0002_task_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='add_task',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='add_task',
            name='email_reminder_sent_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_reminders', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='taskflow_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RunPython(assign_old_tasks, migrations.RunPython.noop),
    ]
