from django.db import models
from django.contrib.auth.models import User
from teams.models import Team


class TimerSession(models.Model):
    WORK_SESSION = 'work'
    BREAK_SESSION = 'break'
    SESSION_TYPES = [
        (WORK_SESSION, 'Work Session'),
        (BREAK_SESSION, 'Break Session'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='timer_sessions')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='timer_sessions', null=True, blank=True)
    session_type = models.CharField(max_length=10, choices=SESSION_TYPES, default=WORK_SESSION)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.session_type} - {self.start_time}'
    
    @property
    def is_active(self):
        return self.end_time is None
