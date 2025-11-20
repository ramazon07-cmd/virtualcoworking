from django.contrib import admin
from .models import TeamAnalytics, UserAnalytics


class TeamAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('team', 'total_tasks_completed', 'total_work_hours', 'last_updated')
    list_filter = ('last_updated',)
    search_fields = ('team__name',)
    date_hierarchy = 'last_updated'


class UserAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'tasks_completed', 'work_hours', 'tasks_created', 'productivity_score', 'last_updated')
    list_filter = ('team', 'last_updated')
    search_fields = ('user__username', 'team__name')
    date_hierarchy = 'last_updated'


admin.site.register(TeamAnalytics, TeamAnalyticsAdmin)
admin.site.register(UserAnalytics, UserAnalyticsAdmin)
