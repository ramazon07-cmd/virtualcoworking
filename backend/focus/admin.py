from django.contrib import admin
from .models import FocusSession, DailyFocusGoal, FocusStat

@admin.register(FocusSession)
class FocusSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'focus_type', 'start_time', 'duration_minutes', 'is_completed', 'interruptions')
    list_filter = ('focus_type', 'is_completed', 'start_time', 'team')
    search_fields = ('user__username', 'notes')


@admin.register(DailyFocusGoal)
class DailyFocusGoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'target_hours', 'actual_hours')
    list_filter = ('date', 'team')
    search_fields = ('user__username',)


@admin.register(FocusStat)
class FocusStatAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'total_focus_minutes', 'completed_sessions', 'avg_session_duration', 'interruptions')
    list_filter = ('date', 'team')
    search_fields = ('user__username',)