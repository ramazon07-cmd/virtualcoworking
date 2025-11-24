from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Event, Reminder
from notifications.models import Notification


@shared_task
def send_event_reminders():
    """
    Send reminders for upcoming events
    """
    now = timezone.now()
    reminder_window_end = now + timedelta(hours=1)  # Check for events in the next hour
    
    # Find events that are coming up and have active reminders
    upcoming_events = Event.objects.filter(
        start_time__gt=now,
        start_time__lte=reminder_window_end
    )
    
    reminders_sent = 0
    for event in upcoming_events:
        # Get active reminders for this event
        active_reminders = Reminder.objects.filter(
            event=event,
            sent=False
        )
        
        for reminder in active_reminders:
            # Calculate if it's time to send this reminder
            reminder_time = event.start_time - timedelta(minutes=reminder.minutes_before)
            
            if now >= reminder_time:
                # Create notification
                Notification.objects.create(
                    recipient=event.created_by,
                    title=f"Upcoming Event: {event.title}",
                    message=f"Your event '{event.title}' starts at {event.start_time.strftime('%H:%M')}",
                    notification_type='info',
                    team=event.team
                )
                
                # Send email reminder if requested
                if reminder.reminder_type in ['email', 'both']:
                    # In a real implementation, you would send an email here
                    pass
                
                # Mark reminder as sent
                reminder.sent = True
                reminder.save()
                reminders_sent += 1
    
    return f"Sent {reminders_sent} event reminders"


@shared_task
def clean_up_past_reminders():
    """
    Clean up reminders for past events
    """
    now = timezone.now()
    
    # Find reminders for events that have already passed
    past_reminders = Reminder.objects.filter(
        event__start_time__lt=now,
        sent=False
    )
    
    count = past_reminders.count()
    past_reminders.delete()
    
    return f"Cleaned up {count} past reminders"