from rest_framework import serializers
from .models import TeamAnalytics, UserAnalytics
from teams.models import Team
from django.contrib.auth.models import User


class TeamAnalyticsSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.name', read_only=True)
    
    class Meta:
        model = TeamAnalytics
        fields = ('id', 'team', 'team_name', 'total_tasks_completed', 'total_work_hours', 
                  'average_task_completion_time', 'last_updated')


class UserAnalyticsSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)
    
    class Meta:
        model = UserAnalytics
        fields = ('id', 'user', 'user_name', 'team', 'team_name', 'tasks_completed', 
                  'work_hours', 'tasks_created', 'productivity_score', 'last_updated')