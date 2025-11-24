from rest_framework import serializers
from .models import Event, Reminder


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    reminders = ReminderSerializer(many=True, read_only=True)
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    team_name = serializers.ReadOnlyField(source='team.name')
    
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')


class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('title', 'description', 'start_time', 'end_time', 'event_type', 'team', 'attendees', 'is_all_day', 'location')
        read_only_fields = ('created_by',)