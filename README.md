<div align="center">

# ✅ TaskFlow

### Smart Task Manager Web Application

A modern and responsive Django-based task manager for organizing daily tasks, managing deadlines, tracking progress, and staying updated with reminders.

</div>

---

## ✨ Overview

**TaskFlow** is a personal task management web application developed with Django. It provides a simple and organized way to create tasks, set deadlines, monitor countdowns, receive reminders, and manage personal task activity from a responsive dashboard.

The project also includes user authentication, profile management, light/dark theme support, email reminder functionality, and a customized Django Admin Panel.

---

## 🚀 Key Features

- ✅ User Registration, Login, and Logout
- 👤 Personal Profile Management
- 📝 Add, Edit, Delete, Complete, and Reopen Tasks
- 📅 Due Date and Due Time Management
- ⏳ Live Countdown for Upcoming Tasks
- ⚠️ Automatic Overdue Task Detection
- 🔔 In-App and Browser Reminder Notifications
- 📧 Email Reminder Support
- 🔕 Reminder On/Off Control
- 📊 Total, Pending, and Completed Task Statistics
- 🔍 Search and Filter Tasks
- 👥 User-Specific Task Management
- 🌙 Light and Dark Theme Support
- 📱 Responsive Design for Desktop, Tablet, and Mobile
- 🖥️ Customized Django Admin Panel
- 🏠 Public Landing Page with Login and Registration Options

---

## 💻 Technologies Used

| Technology | Purpose |
|---|---|
| 🐍 Python | Backend programming |
| 🌿 Django | Web framework |
| 🌐 HTML5 | Page structure |
| 🎨 CSS3 | Styling and responsive design |
| ⚡ JavaScript | Countdown, theme, reminder, and UI interaction |
| 🗄️ SQLite | Database |

---

## 🧩 Main Components

📦 Django Models • 👁️ Function-Based Views • 📄 Templates • 🔐 Authentication System • 👤 User Profile System • ⏰ Countdown & Reminder Logic • 📧 Email Notification Support • ⚙️ Customized Admin Panel • 🗄️ SQLite Database • 🌗 Theme Management • 📱 Responsive User Interface

---

## 📁 Project Structure

```text
TaskFlow/
│
├── manage.py
├── requirements.txt
├── README.md
├── email_settings.example.txt
│
├── todo/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── todo_main/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── template/
│   ├── registration/
│   ├── admin/
│   └── ...
│
└── static/
    ├── css/
    ├── js/
    └── ...
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/woazkuruni/TaskFlow.git
cd TaskFlow
```

### 2. Create a virtual environment

```bash
python -m venv env
```

### 3. Activate the virtual environment

**Windows**
```bash
env\Scripts\activate
```

**Linux / macOS**
```bash
source env/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Run the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## 🔐 Admin Panel

Create an admin account:

```bash
python manage.py createsuperuser
```

Then open:

```text
http://127.0.0.1:8000/admin/
```

---

## 📧 Email Reminder Setup

TaskFlow includes email reminder support.

A sample configuration file is included:

```text
email_settings.example.txt
```

To check and send due-task reminders manually:

```bash
python manage.py send_task_reminders
```

For automatic reminders, schedule the command using **Windows Task Scheduler**, **cron**, or another server-side scheduler.

> Never upload real email passwords, app passwords, API keys, or `.env` files to a public repository.

---

## 🌗 Light & Dark Theme

- Theme preference is saved in the browser
- The selected theme remains active after refresh
- Landing, login, register, profile, task, and edit pages use the same theme system
- The initial theme can follow the device preference

---

## ⏳ Countdown & Reminders

TaskFlow displays a live countdown when a due date and due time are set.

```text
2d 5h 18m left
```

After the deadline:

```text
Overdue
```

Reminder options include:

- 15 minutes before
- 1 hour before
- 1 day before

---

## 👥 User-Based Task Management

Each registered user has a separate task workspace. Users can only view and manage their own tasks, reminders, deadlines, statistics, and profile information.

---

## 📱 Responsive Design

The interface is designed for:

- 💻 Desktop
- 🖥️ Laptop
- 📱 Tablet
- 📲 Mobile

---

## 📸 Project Preview

Add your TaskFlow screenshot or showcase banner here:

```md
![TaskFlow Preview](path/to/your/image.png)
```

---

## 🔒 Security Notes

Before publishing:

```gitignore
__pycache__/
*.py[cod]

env/
venv/
.venv/

.env
.env.*

db.sqlite3
db.sqlite3-journal

*.log

.idea/
.vscode/

.DS_Store
Thumbs.db
```

---

## 👨‍💻 Author

**Wazkuruni**

📧 wazkuruni.tech@gmail.com  
💻 GitHub: `woazkuruni`

---

<div align="center">

### ⭐ If you find this project useful, consider giving the repository a star.

**Built with Django, JavaScript, and SQLite.**

</div>
