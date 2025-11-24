from django.db import models
from django.contrib.auth.models import User


class Integration(models.Model):
    INTEGRATION_TYPES = [
        ('google_calendar', 'Google Calendar'),
        ('slack', 'Slack'),
        ('github', 'GitHub'),
        ('notion', 'Notion'),
        ('zoom', 'Zoom'),
        ('microsoft_teams', 'Microsoft Teams'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='integrations')
    integration_type = models.CharField(max_length=50, choices=INTEGRATION_TYPES)
    access_token = models.TextField()
    refresh_token = models.TextField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'integration_type')
        
    def __str__(self):
        return f"{self.user.username} - {self.get_integration_type_display()}"


class SyncLog(models.Model):
    SYNC_STATUS = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE, related_name='sync_logs')
    sync_type = models.CharField(max_length=50)  # e.g., 'events', 'tasks', 'messages'
    status = models.CharField(max_length=20, choices=SYNC_STATUS, default='pending')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    error_message = models.TextField(blank=True)
    records_synced = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Sync {self.sync_type} for {self.integration} - {self.status}"