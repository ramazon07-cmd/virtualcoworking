from django.contrib import admin
from .models import Event, Reminder

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'event_type', 'created_by', 'team')
    list_filter = ('event_type', 'start_time', 'team')
    search_fields = ('title', 'description', 'created_by__username')
    filter_horizontal = ('attendees',)


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('event', 'reminder_type', 'minutes_before', 'sent')
    list_filter = ('reminder_type', 'sent')
    search_fields = ('event__title',)