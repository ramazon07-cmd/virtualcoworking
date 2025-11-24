from rest_framework import serializers
from .models import Integration, SyncLog


class IntegrationSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Integration
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')


class IntegrationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Integration
        fields = ('integration_type', 'access_token', 'refresh_token', 'expires_at', 'is_active')


class SyncLogSerializer(serializers.ModelSerializer):
    integration_type = serializers.ReadOnlyField(source='integration.get_integration_type_display')
    
    class Meta:
        model = SyncLog
        fields = '__all__'