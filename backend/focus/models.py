from django.db import models
from django.contrib.auth.models import User
from teams.models import Team


class FocusSession(models.Model):
    FOCUS_TYPES = [
        ('pomodoro', 'Pomodoro (25 min)'),
        ('custom', 'Custom Duration'),
        ('deep_work', 'Deep Work (90 min)'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='focus_sessions')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    focus_type = models.CharField(max_length=20, choices=FOCUS_TYPES, default='pomodoro')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_minutes = models.IntegerField()  # Total planned duration
    actual_duration_minutes = models.IntegerField(null=True, blank=True)  # Actual time spent
    is_completed = models.BooleanField(default=False)
    interruptions = models.IntegerField(default=0)  # Number of interruptions
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-start_time']
        
    def __str__(self):
        return f"{self.user.username} - {self.focus_type} session on {self.start_time.date()}"


class DailyFocusGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_focus_goals')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    target_hours = models.DecimalField(max_digits=4, decimal_places=2, default=8.0)  # Target hours per day
    actual_hours = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)  # Actual hours focused
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']
        
    def __str__(self):
        return f"{self.user.username} - Goal for {self.date}"


class FocusStat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='focus_stats')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    total_focus_minutes = models.IntegerField(default=0)
    completed_sessions = models.IntegerField(default=0)
    avg_session_duration = models.IntegerField(default=0)  # In minutes
    interruptions = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']
        
    def __str__(self):
        return f"{self.user.username} - Stats for {self.date}"