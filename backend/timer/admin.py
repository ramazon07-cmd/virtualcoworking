from django.contrib import admin
from .models import TimerSession


class TimerSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'session_type', 'start_time', 'end_time', 'duration', 'is_active')
    list_filter = ('session_type', 'team', 'start_time', 'end_time')
    search_fields = ('user__username',)
    date_hierarchy = 'start_time'


admin.site.register(TimerSession, TimerSessionAdmin)
