from django.db import models
from django.contrib.auth.models import User
from teams.models import Team
from tasks.models import Task
from timer.models import TimerSession


class TeamAnalytics(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name='analytics')
    total_tasks_completed = models.IntegerField(default=0)
    total_work_hours = models.DurationField(default=0)
    average_task_completion_time = models.DurationField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.team.name} Analytics'


class UserAnalytics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='analytics')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='user_analytics')
    tasks_completed = models.IntegerField(default=0)
    work_hours = models.DurationField(default=0)
    tasks_created = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.username} Analytics'
    
    @property
    def productivity_score(self):
        # Simple productivity score based on tasks completed and work hours
        if self.work_hours.total_seconds() > 0:
            return self.tasks_completed / (self.work_hours.total_seconds() / 3600)
        return 0
