from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import TimerSession
from teams.models import Team
from .serializers import TimerSessionSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def timer_session_list(request):
    sessions = TimerSession.objects.filter(user=request.user)
    serializer = TimerSessionSerializer(sessions, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_timer(request):
    session_type = request.data.get('session_type', 'work')
    team_id = request.data.get('team_id')
    
    # Validate team membership if provided
    team = None
    if team_id:
        team = get_object_or_404(Team, id=team_id)
        if not team.members.filter(id=request.user.id).exists():
            return Response({'error': 'You are not a member of this team'}, 
                          status=status.HTTP_403_FORBIDDEN)
    
    # Stop any active sessions
    active_sessions = TimerSession.objects.filter(user=request.user, end_time__isnull=True)
    for session in active_sessions:
        session.end_time = timezone.now()
        session.duration = session.end_time - session.start_time
        session.save()
    
    # Create new session
    session = TimerSession.objects.create(
        user=request.user,
        team=team,
        session_type=session_type,
        start_time=timezone.now()
    )
    
    serializer = TimerSessionSerializer(session)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def stop_timer(request, session_id):
    session = get_object_or_404(TimerSession, id=session_id, user=request.user)
    
    if session.end_time is not None:
        return Response({'error': 'Session already stopped'}, 
                      status=status.HTTP_400_BAD_REQUEST)
    
    session.end_time = timezone.now()
    session.duration = session.end_time - session.start_time
    session.save()
    
    serializer = TimerSessionSerializer(session)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_timer_session(request, session_id):
    session = get_object_or_404(TimerSession, id=session_id, user=request.user)
    session.delete()
    return Response({'message': 'Session deleted successfully'}, 
                  status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def timer_stats(request):
    # Get user's timer statistics
    total_work_sessions = TimerSession.objects.filter(
        user=request.user, 
        session_type='work', 
        end_time__isnull=False
    ).count()
    
    total_break_sessions = TimerSession.objects.filter(
        user=request.user, 
        session_type='break', 
        end_time__isnull=False
    ).count()
    
    # Calculate total work time
    work_sessions = TimerSession.objects.filter(
        user=request.user, 
        session_type='work', 
        end_time__isnull=False
    )
    
    total_work_time = sum(
        [session.duration.total_seconds() for session in work_sessions if session.duration],
        0
    )
    
    stats = {
        'total_work_sessions': total_work_sessions,
        'total_break_sessions': total_break_sessions,
        'total_work_time_seconds': total_work_time,
        'total_work_time_hours': round(total_work_time / 3600, 2)
    }
    
    return Response(stats)
