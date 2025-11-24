from django.contrib import admin
from .models import Integration, SyncLog

@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'integration_type', 'is_active', 'created_at')
    list_filter = ('integration_type', 'is_active', 'created_at')
    search_fields = ('user__username',)


@admin.register(SyncLog)
class SyncLogAdmin(admin.ModelAdmin):
    list_display = ('integration', 'sync_type', 'status', 'started_at', 'completed_at', 'records_synced')
    list_filter = ('status', 'sync_type', 'started_at')
    search_fields = ('integration__user__username', 'sync_type')