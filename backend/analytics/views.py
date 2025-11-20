from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count, Avg
from .models import TeamAnalytics, UserAnalytics
from teams.models import Team
from tasks.models import Task
from timer.models import TimerSession
from .serializers import TeamAnalyticsSerializer, UserAnalyticsSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def team_analytics(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    # Check if user is member of the team
    if not team.members.filter(id=request.user.id).exists():
        return Response({'error': 'You are not a member of this team'}, 
                      status=status.HTTP_403_FORBIDDEN)
    
    # Get or create team analytics
    team_analytics, created = TeamAnalytics.objects.get_or_create(team=team)
    
    # Update analytics
    team_analytics.total_tasks_completed = Task.objects.filter(
        column__board__team=team, 
        completed=True
    ).count()
    
    # Calculate total work hours
    work_sessions = TimerSession.objects.filter(team=team, session_type='work', end_time__isnull=False)
    total_seconds = sum(
        [session.duration.total_seconds() for session in work_sessions if session.duration],
        0
    )
    team_analytics.total_work_hours = total_seconds
    
    team_analytics.save()
    
    serializer = TeamAnalyticsSerializer(team_analytics)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_analytics(request):
    # Get or create user analytics for each team the user is a member of
    teams = Team.objects.filter(members=request.user)
    user_analytics_list = []
    
    for team in teams:
        user_analytics, created = UserAnalytics.objects.get_or_create(user=request.user, team=team)
        
        # Update analytics
        user_analytics.tasks_completed = Task.objects.filter(
            assignee=request.user, 
            column__board__team=team, 
            completed=True
        ).count()
        
        user_analytics.tasks_created = Task.objects.filter(
            creator=request.user, 
            column__board__team=team
        ).count()
        
        # Calculate work hours
        work_sessions = TimerSession.objects.filter(
            user=request.user, 
            team=team, 
            session_type='work', 
            end_time__isnull=False
        )
        total_seconds = sum(
            [session.duration.total_seconds() for session in work_sessions if session.duration],
            0
        )
        user_analytics.work_hours = total_seconds
        
        user_analytics.save()
        user_analytics_list.append(user_analytics)
    
    serializer = UserAnalyticsSerializer(user_analytics_list, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def team_productivity_report(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    # Check if user is member of the team
    if not team.members.filter(id=request.user.id).exists():
        return Response({'error': 'You are not a member of this team'}, 
                      status=status.HTTP_403_FORBIDDEN)
    
    # Get all team members' analytics
    team_members_analytics = UserAnalytics.objects.filter(team=team)
    
    # Calculate team productivity metrics
    total_members = team_members_analytics.count()
    avg_tasks_completed = team_members_analytics.aggregate(
        avg=Avg('tasks_completed')
    )['avg'] or 0
    
    avg_work_hours = team_members_analytics.aggregate(
        avg=Avg('work_hours')
    )['avg'] or 0
    
    report = {
        'team_id': team.id,
        'team_name': team.name,
        'total_members': total_members,
        'average_tasks_completed_per_member': round(avg_tasks_completed, 2),
        'average_work_hours_per_member': round(avg_work_hours / 3600, 2) if avg_work_hours else 0,
        'most_productive_member': None
    }
    
    # Find most productive member
    if team_members_analytics.exists():
        most_productive = max(team_members_analytics, key=lambda x: x.productivity_score)
        report['most_productive_member'] = {
            'user_id': most_productive.user.id,
            'username': most_productive.user.username,
            'productivity_score': round(most_productive.productivity_score, 2)
        }
    
    return Response(report)
