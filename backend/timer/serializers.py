from rest_framework import serializers
from .models import TimerSession
from teams.models import Team
from django.contrib.auth.models import User


class TimerSessionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    team = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = TimerSession
        fields = ('id', 'user', 'team', 'session_type', 'start_time', 'end_time', 'duration', 'is_active')
        read_only_fields = ('user', 'duration', 'is_active')