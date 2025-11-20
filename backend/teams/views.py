from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Team, TeamMembership
from .serializers import TeamSerializer, TeamDetailSerializer, TeamCreateSerializer, TeamMembershipCreateSerializer, TeamMembershipSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def team_list(request):
    # Get teams where user is a member
    teams = Team.objects.filter(members=request.user)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_team(request):
    serializer = TeamCreateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        team = serializer.save()
        return Response(TeamSerializer(team).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id, members=request.user)
    serializer = TeamDetailSerializer(team)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_team(request, team_id):
    team = get_object_or_404(Team, id=team_id, owner=request.user)
    serializer = TeamCreateSerializer(team, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(TeamSerializer(team).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_team(request, team_id):
    team = get_object_or_404(Team, id=team_id, owner=request.user)
    team.delete()
    return Response({'message': 'Team deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def team_members(request, team_id):
    team = get_object_or_404(Team, id=team_id, members=request.user)
    memberships = TeamMembership.objects.filter(team=team)
    serializer = TeamMembershipSerializer(memberships, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_member(request, team_id):
    team = get_object_or_404(Team, id=team_id, owner=request.user)
    serializer = TeamMembershipCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(team=team)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_member(request, team_id, user_id):
    team = get_object_or_404(Team, id=team_id, owner=request.user)
    membership = get_object_or_404(TeamMembership, team=team, user_id=user_id)
    # Prevent owner from removing themselves
    if membership.role == 'owner' and membership.user == request.user:
        return Response({'error': 'Cannot remove team owner'}, status=status.HTTP_400_BAD_REQUEST)
    membership.delete()
    return Response({'message': 'Member removed successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_member_role(request, team_id, user_id):
    team = get_object_or_404(Team, id=team_id, owner=request.user)
    membership = get_object_or_404(TeamMembership, team=team, user_id=user_id)
    new_role = request.data.get('role')
    
    if new_role in dict(TeamMembership.ROLE_CHOICES):
        membership.role = new_role
        membership.save()
        serializer = TeamMembershipSerializer(membership)
        return Response(serializer.data)
    
    return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)
