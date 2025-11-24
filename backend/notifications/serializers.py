from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    recipient_username = serializers.ReadOnlyField(source='recipient.username')
    
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('recipient', 'created_at', 'read_at')


class NotificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('title', 'message', 'notification_type', 'team')