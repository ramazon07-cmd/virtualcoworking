from django.contrib import admin
from .models import Team, TeamMembership


class TeamMembershipInline(admin.TabularInline):
    model = TeamMembership
    extra = 1


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    list_filter = ('created_at', 'owner')
    search_fields = ('name', 'description')
    inlines = [TeamMembershipInline]


admin.site.register(Team, TeamAdmin)
admin.site.register(TeamMembership)
