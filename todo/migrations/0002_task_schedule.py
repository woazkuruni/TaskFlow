from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='add_task',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='add_task',
            name='due_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='add_task',
            name='reminder_minutes',
            field=models.IntegerField(choices=[(0, 'No reminder'), (15, '15 minutes before'), (60, '1 hour before'), (1440, '1 day before')], default=0),
        ),
        migrations.AddField(
            model_name='add_task',
            name='completed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
