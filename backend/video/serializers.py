from rest_framework import serializers
from .models import Meeting, MeetingParticipant


class MeetingParticipantSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = MeetingParticipant
        fields = '__all__'


class MeetingSerializer(serializers.ModelSerializer):
    participants = MeetingParticipantSerializer(many=True, read_only=True)
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    team_name = serializers.ReadOnlyField(source='team.name')
    
    class Meta:
        model = Meeting
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at', 'meeting_link', 'recording_url')


class MeetingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ('title', 'description', 'start_time', 'end_time', 'team', 'attendees')
        read_only_fields = ('created_by', 'meeting_link', 'recording_url')