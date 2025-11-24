from django.db import models
from django.contrib.auth.models import User
from teams.models import Team


class Event(models.Model):
    EVENT_TYPES = [
        ('meeting', 'Meeting'),
        ('deadline', 'Deadline'),
        ('reminder', 'Reminder'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='meeting')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    attendees = models.ManyToManyField(User, related_name='events', blank=True)
    is_all_day = models.BooleanField(default=False)
    location = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['start_time']
        
    def __str__(self):
        return self.title


class Reminder(models.Model):
    REMINDER_TYPES = [
        ('email', 'Email'),
        ('notification', 'In-App Notification'),
        ('both', 'Both'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reminders')
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPES, default='notification')
    minutes_before = models.IntegerField(default=10)  # Remind 10 minutes before event
    sent = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Reminder for {self.event.title}"