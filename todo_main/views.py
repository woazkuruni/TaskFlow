from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, render

from todo.models import UserProfile, add_task


def login_view(request):
    if request.user.is_authenticated:
        return redirect('tasks')

    if request.method == 'POST':
        login_value = request.POST.get('login', '').strip()
        password = request.POST.get('password', '')
        username = login_value

        if '@' in login_value:
            email_user = User.objects.filter(email__iexact=login_value).first()
            if email_user:
                username = email_user.username

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('tasks')

        messages.error(request, 'Username/email or password is incorrect.')

    return render(request, 'registration/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('tasks')

    values = {
        'username': '',
        'full_name': '',
        'email': '',
    }

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        values.update(username=username, full_name=full_name, email=email)

        if not username or not email or not password:
            messages.warning(request, 'Please complete the required fields.')
        elif User.objects.filter(username__iexact=username).exists():
            messages.warning(request, 'This username is already being used.')
        elif User.objects.filter(email__iexact=email).exists():
            messages.warning(request, 'An account already exists with this email.')
        elif password != confirm_password:
            messages.warning(request, 'The two passwords do not match.')
        elif len(password) < 8:
            messages.warning(request, 'Use at least 8 characters for your password.')
        else:
            name_parts = full_name.split(maxsplit=1)
            first_name = name_parts[0] if name_parts else ''
            last_name = name_parts[1] if len(name_parts) > 1 else ''

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Your TaskFlow account is ready.')
            return redirect('tasks')

    return render(request, 'registration/register.html', {'values': values})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        email_reminders = request.POST.get('email_reminders') == 'on'

        if not email:
            messages.warning(request, 'Email cannot be empty.')
        elif User.objects.filter(email__iexact=email).exclude(pk=request.user.pk).exists():
            messages.warning(request, 'Another account is already using this email.')
        else:
            name_parts = full_name.split(maxsplit=1)
            request.user.first_name = name_parts[0] if name_parts else ''
            request.user.last_name = name_parts[1] if len(name_parts) > 1 else ''
            request.user.email = email
            request.user.save()

            profile.email_reminders = email_reminders
            profile.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')

    full_name = request.user.get_full_name().strip()
    return render(request, 'profile.html', {
        'profile': profile,
        'full_name': full_name,
    })


def landing(request):
    return render(request, 'landing.html')


@login_required
def tasks(request):
    search = request.GET.get('search', '').strip()

    task = add_task.objects.filter(owner=request.user, is_complete=False).order_by('-updated_at')
    completed_task = add_task.objects.filter(owner=request.user, is_complete=True).order_by('-updated_at')

    if search:
        task = task.filter(Q(task__icontains=search))
        completed_task = completed_task.filter(Q(task__icontains=search))

    total_tasks = add_task.objects.filter(owner=request.user).count()
    completed_count = add_task.objects.filter(owner=request.user, is_complete=True).count()
    pending_count = add_task.objects.filter(owner=request.user, is_complete=False).count()
    progress = round((completed_count / total_tasks) * 100) if total_tasks else 0

    context = {
        'task': task,
        'c_task': completed_task,
        'search': search,
        'total_tasks': total_tasks,
        'completed_count': completed_count,
        'pending_count': pending_count,
        'progress': progress,
        'reminder_choices': add_task.REMINDER_CHOICES,
    }
    return render(request, 'home.html', context)
