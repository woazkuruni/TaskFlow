document.addEventListener('DOMContentLoaded', function () {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const panels = document.querySelectorAll('.task-panel[data-panel]');

    filterButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            const filter = button.dataset.filter;

            filterButtons.forEach(function (item) {
                item.classList.remove('active');
            });
            button.classList.add('active');

            panels.forEach(function (panel) {
                const panelName = panel.dataset.panel;
                panel.style.display = filter === 'all' || filter === panelName ? '' : 'none';
            });
        });
    });

    document.querySelectorAll('[data-confirm-delete]').forEach(function (link) {
        link.addEventListener('click', function (event) {
            if (!confirm('Delete this task?')) {
                event.preventDefault();
            }
        });
    });

    const clearLink = document.querySelector('[data-confirm-clear]');
    if (clearLink) {
        clearLink.addEventListener('click', function (event) {
            if (!confirm('Clear all completed tasks?')) {
                event.preventDefault();
            }
        });
    }

    const notificationButton = document.querySelector('[data-notification-button]');
    const notificationNote = document.querySelector('[data-notification-note]');
    const toastStack = document.querySelector('[data-toast-stack]');
    const reminderStorageKey = 'taskflow-reminders-enabled';

    function showNote(text) {
        if (!notificationNote) return;
        notificationNote.textContent = text;
        notificationNote.hidden = false;
        window.setTimeout(function () {
            notificationNote.hidden = true;
        }, 5000);
    }

    function remindersEnabled() {
        try {
            return localStorage.getItem(reminderStorageKey) === '1';
        } catch (error) {
            return false;
        }
    }

    function saveReminderState(enabled) {
        try {
            localStorage.setItem(reminderStorageKey, enabled ? '1' : '0');
        } catch (error) {
            // The switch still works until the page is refreshed.
        }
    }

    function updateNotificationButton() {
        if (!notificationButton) return;

        const enabled = remindersEnabled();
        notificationButton.classList.toggle('is-enabled', enabled);
        notificationButton.title = enabled ? 'Turn reminders off' : 'Turn reminders on';
        notificationButton.setAttribute('aria-label', notificationButton.title);

        const label = notificationButton.querySelector('span');
        if (label) {
            label.textContent = enabled ? 'Reminders On' : 'Reminders Off';
        }
    }

    if (notificationButton) {
        notificationButton.addEventListener('click', function () {
            if (remindersEnabled()) {
                saveReminderState(false);
                updateNotificationButton();
                showNote('Task reminders are off on this browser. You can turn them on again anytime.');
                return;
            }

            if (!('Notification' in window)) {
                saveReminderState(true);
                updateNotificationButton();
                showNote('In-app reminders are on. This browser does not support desktop notifications.');
                return;
            }

            if (Notification.permission === 'granted') {
                saveReminderState(true);
                updateNotificationButton();
                showNote('Task reminders are on.');
                return;
            }

            if (Notification.permission === 'denied') {
                saveReminderState(true);
                updateNotificationButton();
                showNote('In-app reminders are on. Desktop notifications are blocked in browser settings.');
                return;
            }

            Notification.requestPermission().then(function (permission) {
                saveReminderState(true);
                updateNotificationButton();
                if (permission === 'granted') {
                    showNote('Task reminders are on. Browser notifications are also enabled.');
                } else {
                    showNote('In-app reminders are on. Browser notification permission was not enabled.');
                }
            });
        });
    }

    updateNotificationButton();

    function getDueDate(card) {
        const dateText = card.dataset.dueDate;
        if (!dateText) return null;

        const dateParts = dateText.split('-').map(Number);
        const timeText = card.dataset.dueTime || '23:59';
        const timeParts = timeText.split(':').map(Number);

        return new Date(
            dateParts[0],
            dateParts[1] - 1,
            dateParts[2],
            timeParts[0] || 0,
            timeParts[1] || 0,
            card.dataset.dueTime ? 0 : 59
        );
    }

    function formatDuration(milliseconds) {
        const totalSeconds = Math.max(0, Math.floor(milliseconds / 1000));
        const days = Math.floor(totalSeconds / 86400);
        const hours = Math.floor((totalSeconds % 86400) / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;

        if (days > 0) return days + 'd ' + hours + 'h ' + minutes + 'm';
        if (hours > 0) return hours + 'h ' + minutes + 'm ' + seconds + 's';
        return minutes + 'm ' + seconds + 's';
    }

    function storageHas(key) {
        try {
            return localStorage.getItem(key) === '1';
        } catch (error) {
            return false;
        }
    }

    function storageSet(key) {
        try {
            localStorage.setItem(key, '1');
        } catch (error) {
            // Reminders still work for the current page if storage is unavailable.
        }
    }

    function showToast(title, message, overdue) {
        if (!toastStack) return;

        const toast = document.createElement('div');
        toast.className = 'task-toast' + (overdue ? ' is-overdue' : '');
        toast.innerHTML =
            '<div class="task-toast-icon"><i class="fa-regular ' + (overdue ? 'fa-clock' : 'fa-bell') + '"></i></div>' +
            '<div><strong></strong><p></p></div>' +
            '<button type="button" aria-label="Close">&times;</button>';

        toast.querySelector('strong').textContent = title;
        toast.querySelector('p').textContent = message;
        toast.querySelector('button').addEventListener('click', function () {
            toast.remove();
        });

        toastStack.appendChild(toast);
        window.setTimeout(function () {
            toast.remove();
        }, 9000);
    }

    function browserNotify(title, message) {
        if (remindersEnabled() && 'Notification' in window && Notification.permission === 'granted') {
            new Notification(title, {
                body: message,
                icon: '/static/favicon.svg',
            });
        }
    }

    const taskCards = document.querySelectorAll('[data-task-card]');

    function updateTasks() {
        const now = new Date();

        taskCards.forEach(function (card) {
            const due = getDueDate(card);
            const countdown = card.querySelector('[data-countdown] .countdown-badge');
            if (!due || !countdown) return;

            const difference = due.getTime() - now.getTime();
            const taskName = card.dataset.taskName || 'Task';
            const taskId = card.dataset.taskId || '0';
            const reminderMinutes = Number(card.dataset.reminder || 0);
            const dueKey = card.dataset.dueDate + '-' + (card.dataset.dueTime || 'end');

            countdown.classList.remove('is-soon', 'is-overdue');

            if (difference <= 0) {
                card.classList.add('is-overdue');
                countdown.classList.add('is-overdue');
                countdown.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> Overdue by ' + formatDuration(Math.abs(difference));

                const overdueKey = 'taskflow-overdue-' + taskId + '-' + dueKey;
                if (remindersEnabled() && !storageHas(overdueKey)) {
                    const message = taskName + ' is overdue.';
                    showToast('Task overdue', message, true);
                    browserNotify('TaskFlow: Task overdue', message);
                    storageSet(overdueKey);
                }
                return;
            }

            card.classList.remove('is-overdue');
            countdown.innerHTML = '<span class="countdown-hourglass" aria-hidden="true"><i class="fa-solid fa-hourglass-half"></i></span><span>' + formatDuration(difference) + ' left</span>';

            if (difference <= 3600000) {
                countdown.classList.add('is-soon');
            }

            if (reminderMinutes > 0 && difference <= reminderMinutes * 60000) {
                const reminderKey = 'taskflow-reminder-' + taskId + '-' + dueKey + '-' + reminderMinutes;
                if (remindersEnabled() && !storageHas(reminderKey)) {
                    const label = reminderMinutes === 1440 ? '1 day' : reminderMinutes === 60 ? '1 hour' : '15 minutes';
                    const message = taskName + ' is due within ' + label + '.';
                    showToast('Task reminder', message, false);
                    browserNotify('TaskFlow Reminder', message);
                    storageSet(reminderKey);
                }
            }
        });
    }

    updateTasks();
    window.setInterval(updateTasks, 1000);
});


// Open native date/time pickers from the visible icon buttons.
document.addEventListener('click', function (event) {
    const button = event.target.closest('[data-picker-for]');
    if (!button) return;

    const input = document.getElementById(button.dataset.pickerFor);
    if (!input) return;

    input.focus();
    if (typeof input.showPicker === 'function') {
        try {
            input.showPicker();
        } catch (error) {
            input.click();
        }
    } else {
        input.click();
    }
});
