from django.contrib import admin

from .models import UserProfile, add_task


class task_admin(admin.ModelAdmin):
    list_display = ('task', 'owner', 'is_complete', 'due_date', 'due_time', 'reminder_minutes', 'created_at')
    list_filter = ('is_complete', 'due_date', 'created_at')
    search_fields = ('task', 'owner__username', 'owner__email')
    ordering = ('-updated_at',)
    list_per_page = 20


class profile_admin(admin.ModelAdmin):
    list_display = ('user', 'email_reminders', 'updated_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('email_reminders',)


admin.site.register(add_task, task_admin)
admin.site.register(UserProfile, profile_admin)

admin.site.site_header = 'TaskFlow Administration'
admin.site.site_title = 'TaskFlow Admin'
admin.site.index_title = 'Manage your ToDo application'
