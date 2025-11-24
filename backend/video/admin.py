from django.contrib import admin
from .models import Meeting, MeetingParticipant

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'created_by', 'team', 'status')
    list_filter = ('status', 'start_time', 'team')
    search_fields = ('title', 'description', 'created_by__username')
    filter_horizontal = ('attendees',)


@admin.register(MeetingParticipant)
class MeetingParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'meeting', 'status', 'join_time', 'leave_time')
    list_filter = ('status', 'meeting')
    search_fields = ('user__username', 'meeting__title')