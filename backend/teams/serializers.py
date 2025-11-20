from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Team, TeamMembership


class TeamMembershipSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = TeamMembership
        fields = ('id', 'user', 'role', 'joined_at')


class TeamSerializer(serializers.ModelSerializer):
    members_count = serializers.SerializerMethodField()
    owner = serializers.StringRelatedField()
    
    class Meta:
        model = Team
        fields = ('id', 'name', 'description', 'created_at', 'updated_at', 'owner', 'members_count')
        
    def get_members_count(self, obj):
        return obj.members.count()


class TeamDetailSerializer(serializers.ModelSerializer):
    members = TeamMembershipSerializer(many=True, read_only=True)
    owner = serializers.StringRelatedField()
    
    class Meta:
        model = Team
        fields = ('id', 'name', 'description', 'created_at', 'updated_at', 'owner', 'members')


class TeamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('name', 'description')
        
    def create(self, validated_data):
        user = self.context['request'].user
        team = Team.objects.create(owner=user, **validated_data)
        # Add owner as a member with owner role
        TeamMembership.objects.create(user=user, team=team, role='owner')
        return team


class TeamMembershipCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMembership
        fields = ('user', 'team', 'role')
        
    def validate(self, attrs):
        # Check if user is already a member
        if TeamMembership.objects.filter(user=attrs['user'], team=attrs['team']).exists():
            raise serializers.ValidationError("User is already a member of this team.")
        return attrs