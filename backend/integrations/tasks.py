from celery import shared_task
from django.utils import timezone
from .models import Integration, SyncLog


@shared_task
def sync_user_integrations(user_id=None):
    """
    Sync all active integrations for a user or all users
    """
    integrations = Integration.objects.filter(is_active=True)
    
    if user_id:
        integrations = integrations.filter(user_id=user_id)
    
    synced_count = 0
    for integration in integrations:
        # Create a sync log entry
        sync_log = SyncLog.objects.create(
            integration=integration,
            sync_type='scheduled_sync',
            status='in_progress'
        )
        
        try:
            # In a real implementation, you would sync with the external service here
            # For now, we'll just simulate a successful sync
            records_synced = 0
            
            if integration.integration_type == 'google_calendar':
                records_synced = sync_google_calendar(integration)
            elif integration.integration_type == 'slack':
                records_synced = sync_slack(integration)
            # Add more integration types as needed
            
            # Update sync log
            sync_log.status = 'completed'
            sync_log.records_synced = records_synced
            sync_log.completed_at = timezone.now()
            sync_log.save()
            
            synced_count += 1
        except Exception as e:
            # Update sync log with error
            sync_log.status = 'failed'
            sync_log.error_message = str(e)
            sync_log.completed_at = timezone.now()
            sync_log.save()
    
    return f"Synced {synced_count} integrations"


def sync_google_calendar(integration):
    """
    Sync Google Calendar events
    In a real implementation, this would connect to Google Calendar API
    """
    # Simulate syncing some records
    return 5


def sync_slack(integration):
    """
    Sync Slack messages or channels
    In a real implementation, this would connect to Slack API
    """
    # Simulate syncing some records
    return 10