from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Notification


@shared_task
def send_email_notification(notification_id):
    """
    Send an email notification for a given notification
    """
    try:
        notification = Notification.objects.get(id=notification_id)
        
        # Send email
        send_mail(
            subject=notification.title,
            message=notification.message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[notification.recipient.email],
            fail_silently=False,
        )
        
        return f"Email notification sent to {notification.recipient.email}"
    except Notification.DoesNotExist:
        return f"Notification with id {notification_id} does not exist"
    except Exception as e:
        return f"Failed to send email notification: {str(e)}"


@shared_task
def send_reminder_notifications():
    """
    Send reminder notifications for upcoming events
    """
    from calendar_app.models import Reminder, Event
    from django.utils import timezone
    from datetime import timedelta
    
    # Get reminders that need to be sent
    now = timezone.now()
    reminders_to_send = Reminder.objects.filter(
        sent=False,
        event__start_time__gt=now,
        event__start_time__lte=now + timedelta(minutes=30)  # Remind within 30 minutes
    )
    
    sent_count = 0
    for reminder in reminders_to_send:
        # Create in-app notification
        Notification.objects.create(
            recipient=reminder.event.created_by,
            title=f"Reminder: {reminder.event.title}",
            message=f"Your event '{reminder.event.title}' starts soon at {reminder.event.start_time.strftime('%H:%M')}",
            notification_type='info',
            team=reminder.event.team
        )
        
        # Send email if requested
        if reminder.reminder_type in ['email', 'both']:
            send_mail(
                subject=f"Reminder: {reminder.event.title}",
                message=f"Your event '{reminder.event.title}' starts soon at {reminder.event.start_time.strftime('%H:%M')}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[reminder.event.created_by.email],
                fail_silently=False,
            )
        
        # Mark reminder as sent
        reminder.sent = True
        reminder.save()
        sent_count += 1
    
    return f"Sent {sent_count} reminder notifications"