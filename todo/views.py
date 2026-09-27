from datetime import datetime, time

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import add_task


def read_task_form(request):
    task_text = request.POST.get('task', '').strip()
    due_date_text = request.POST.get('due_date', '').strip()
    due_time_text = request.POST.get('due_time', '').strip()
    reminder_text = request.POST.get('reminder_minutes', '0').strip()

    due_date = None
    due_time = None

    if due_date_text:
        try:
            due_date = datetime.strptime(due_date_text, '%Y-%m-%d').date()
        except ValueError:
            pass

    if due_date:
        if due_time_text:
            try:
                due_time = datetime.strptime(due_time_text, '%H:%M').time()
            except ValueError:
                due_time = time(9, 0)
        else:
            due_time = time(9, 0)

    try:
        reminder_minutes = int(reminder_text)
    except ValueError:
        reminder_minutes = 0

    allowed_reminders = {choice[0] for choice in add_task.REMINDER_CHOICES}
    if reminder_minutes not in allowed_reminders:
        reminder_minutes = 0

    return task_text, due_date, due_time, reminder_minutes


@login_required
def addTask(request):
    if request.method == 'POST':
        task_text, due_date, due_time, reminder_minutes = read_task_form(request)

        if task_text:
            add_task.objects.create(
                owner=request.user,
                task=task_text,
                due_date=due_date,
                due_time=due_time,
                reminder_minutes=reminder_minutes,
            )
            messages.success(request, 'Task added successfully.')
        else:
            messages.warning(request, 'Please write a task before adding it.')

    return redirect('tasks')


@login_required
def mark_as_done(request, pk):
    task = get_object_or_404(add_task, pk=pk, owner=request.user)
    task.is_complete = True
    task.completed_at = timezone.now()
    task.save()
    messages.success(request, 'Task marked as completed.')
    return redirect('tasks')


@login_required
def mark_as_pending(request, pk):
    task = get_object_or_404(add_task, pk=pk, owner=request.user)
    task.is_complete = False
    task.completed_at = None
    task.email_reminder_sent_at = None
    task.save()
    messages.info(request, 'Task moved back to pending.')
    return redirect('tasks')


@login_required
def edit_task(request, pk):
    get_task = get_object_or_404(add_task, pk=pk, owner=request.user)

    if request.method == 'POST':
        task_text, due_date, due_time, reminder_minutes = read_task_form(request)

        if task_text:
            schedule_changed = (
                get_task.due_date != due_date
                or get_task.due_time != due_time
                or get_task.reminder_minutes != reminder_minutes
            )

            get_task.task = task_text
            get_task.due_date = due_date
            get_task.due_time = due_time
            get_task.reminder_minutes = reminder_minutes
            if schedule_changed:
                get_task.email_reminder_sent_at = None
            get_task.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('tasks')

        messages.warning(request, 'Task cannot be empty.')

    context = {
        'get_task': get_task,
        'reminder_choices': add_task.REMINDER_CHOICES,
    }
    return render(request, 'edit_task.html', context)


@login_required
def delete_task(request, pk):
    task = get_object_or_404(add_task, pk=pk, owner=request.user)
    task.delete()
    messages.success(request, 'Task deleted.')
    return redirect('tasks')


@login_required
def clear_completed(request):
    completed_tasks = add_task.objects.filter(owner=request.user, is_complete=True)
    count = completed_tasks.count()

    if count:
        completed_tasks.delete()
        messages.success(request, f'{count} completed task(s) cleared.')
    else:
        messages.info(request, 'There are no completed tasks to clear.')

    return redirect('tasks')
