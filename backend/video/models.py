from django.db import models
from django.contrib.auth.models import User
from teams.models import Team


class Meeting(models.Model):
    MEETING_STATUS = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_meetings')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    attendees = models.ManyToManyField(User, related_name='meetings', blank=True)
    meeting_link = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=MEETING_STATUS, default='scheduled')
    recording_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['start_time']
        
    def __str__(self):
        return self.title


class MeetingParticipant(models.Model):
    PARTICIPANT_STATUS = [
        ('invited', 'Invited'),
        ('joined', 'Joined'),
        ('left', 'Left'),
    ]
    
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    join_time = models.DateTimeField(null=True, blank=True)
    leave_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=PARTICIPANT_STATUS, default='invited')
    
    class Meta:
        unique_together = ('meeting', 'user')
        
    def __str__(self):
        return f"{self.user.username} - {self.meeting.title}"