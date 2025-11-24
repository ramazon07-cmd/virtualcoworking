from rest_framework import serializers
from .models import FocusSession, DailyFocusGoal, FocusStat


class FocusSessionSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    team_name = serializers.ReadOnlyField(source='team.name')
    
    class Meta:
        model = FocusSession
        fields = '__all__'
        read_only_fields = ('user', 'created_at')


class FocusSessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FocusSession
        fields = ('focus_type', 'start_time', 'end_time', 'duration_minutes', 'team', 'notes')
        read_only_fields = ('user',)


class DailyFocusGoalSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    team_name = serializers.ReadOnlyField(source='team.name')
    
    class Meta:
        model = DailyFocusGoal
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')


class FocusStatSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    team_name = serializers.ReadOnlyField(source='team.name')
    
    class Meta:
        model = FocusStat
        fields = '__all__'
        read_only_fields = ('user', 'created_at')