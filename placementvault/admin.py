from django.contrib import admin

from .models import Experience, Schedule


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'role', 'interview_round', 'date', 'time', 'user']
    list_filter = ['company_name', 'interview_round']
    search_fields = ['company_name', 'role', 'user__username']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'role', 'interview_round', 'focus_subject', 'user', 'created_at']
    list_filter = ['company_name', 'interview_round', 'focus_subject']
    search_fields = ['company_name', 'role', 'user__username', 'experience_text']
