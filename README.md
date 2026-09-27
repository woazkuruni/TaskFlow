# TaskFlow

A simple Django ToDo project upgraded into a small multi-user task manager while keeping the original function-based project flow.

## Features

- Public landing page before login
- Landing page changes actions for signed-in users

- User registration, login and logout
- Login with username or email
- User profile with name and email
- Every user sees only their own tasks
- Add, edit, complete, reopen and delete tasks
- Due date and optional due time
- Live countdown and overdue state
- 15 minute, 1 hour and 1 day reminders
- Browser/in-app reminder On/Off switch
- Optional email reminders
- Day/Night mode with saved browser preference
- Responsive user interface
- Custom responsive Django admin

## Run the project

```bash
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open:

- Landing page: `http://127.0.0.1:8000/`
- My Tasks: `http://127.0.0.1:8000/tasks/`
- Admin: `http://127.0.0.1:8000/admin/`

The existing database already contains the previous admin account and tasks. If the admin password is forgotten:

```bash
python manage.py changepassword admin
```

## Reminder switch

The **Reminders On / Reminders Off** button controls TaskFlow reminders in the current browser. Turning it off does not change the browser's notification permission; TaskFlow simply stops sending browser and in-app reminder alerts until it is turned on again.

## Email reminders

Email reminders are enabled or disabled from the user's Profile page.

For local development, Django prints reminder emails in the terminal. To send real email, configure SMTP using the values shown in `email_settings.example.txt`.

Run the reminder checker with:

```bash
python manage.py send_task_reminders
```

For automatic delivery, schedule that command to run every minute using Windows Task Scheduler, cron, or another scheduler. This keeps the project lightweight without Celery/Redis.

### Latest task-card polish
- Countdown is shown on the right side of pending task cards on wider screens.
- Long task names wrap safely without pushing the action buttons out of the card.
- The hourglass icon uses a small flip/up-down animation while the countdown is active.
- New tasks default to 09:00 AM when a due date is used; the user can change the time before saving.

## Page flow

- `/` - public landing page
- `/login/` - sign in
- `/register/` - create an account
- `/tasks/` - the signed-in user's task dashboard
- `/profile/` - profile and email reminder preference

The same Day/Night preference is shared across the landing page, login, registration, profile and task dashboard.

### Countdown animation
The countdown keeps its place on the right side of wide task cards. Its hourglass has a small flip, vertical movement and sand-dot animation. Long task names wrap inside the available space instead of pushing the countdown or action buttons out of the card.
