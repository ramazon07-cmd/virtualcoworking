from rest_framework import serializers
from .models import File, Note
from teams.models import Team
from django.contrib.auth.models import User


class FileSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField(read_only=True)
    team = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = File
        fields = ('id', 'name', 'file', 'uploaded_by', 'team', 'created_at')
        read_only_fields = ('uploaded_by', 'created_at')


class NoteSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    team = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Note
        fields = ('id', 'title', 'content', 'author', 'team', 'created_at', 'updated_at')
        read_only_fields = ('author', 'created_at', 'updated_at')


class NoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('title', 'content', 'team')
        
    def create(self, validated_data):
        user = self.context['request'].user
        note = Note.objects.create(author=user, **validated_data)
        return note