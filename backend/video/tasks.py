from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Meeting


@shared_task
def cleanup_old_recordings():
    """
    Clean up recordings from meetings older than 30 days
    """
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    # Find completed meetings older than 30 days that have recordings
    old_meetings = Meeting.objects.filter(
        status='completed',
        end_time__lt=thirty_days_ago,
        recording_url__isnull=False
    ).exclude(recording_url='')
    
    cleaned_count = 0
    for meeting in old_meetings:
        # In a real implementation, you would delete the actual recording file
        # from storage (e.g., S3) here
        # For now, we'll just clear the recording URL
        meeting.recording_url = ''
        meeting.save(update_fields=['recording_url'])
        cleaned_count += 1
    
    return f"Cleaned up recordings from {cleaned_count} old meetings"


@shared_task
def update_meeting_statuses():
    """
    Update meeting statuses based on current time
    """
    now = timezone.now()
    
    # Mark meetings that have ended as completed
    ended_meetings = Meeting.objects.filter(
        status='in_progress',
        end_time__lt=now
    )
    
    updated_count = 0
    for meeting in ended_meetings:
        meeting.status = 'completed'
        meeting.save(update_fields=['status'])
        updated_count += 1
    
    # Mark meetings that should have started as in progress
    started_meetings = Meeting.objects.filter(
        status='scheduled',
        start_time__lt=now,
        end_time__gt=now
    )
    
    for meeting in started_meetings:
        meeting.status = 'in_progress'
        meeting.save(update_fields=['status'])
        updated_count += 1
    
    return f"Updated status for {updated_count} meetings"