from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta, date
from .models import FocusSession, DailyFocusGoal, FocusStat
from .serializers import FocusSessionSerializer, FocusSessionCreateSerializer, DailyFocusGoalSerializer, FocusStatSerializer


class FocusSessionListView(generics.ListCreateAPIView):
    serializer_class = FocusSessionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return FocusSession.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FocusSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FocusSessionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return FocusSession.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_session(request, pk):
    """
    Mark a focus session as completed
    """
    session = get_object_or_404(FocusSession, pk=pk, user=request.user)
    
    if session.is_completed:
        return Response({'error': 'Session already completed'}, status=status.HTTP_400_BAD_REQUEST)
    
    session.is_completed = True
    session.actual_duration_minutes = int((timezone.now() - session.start_time).total_seconds() / 60)
    session.save(update_fields=['is_completed', 'actual_duration_minutes'])
    
    # Update daily stats
    today = date.today()
    stat, created = FocusStat.objects.get_or_create(
        user=request.user,
        date=today,
        defaults={
            'total_focus_minutes': session.actual_duration_minutes,
            'completed_sessions': 1,
            'avg_session_duration': session.actual_duration_minutes,
            'interruptions': session.interruptions
        }
    )
    
    if not created:
        stat.total_focus_minutes += session.actual_duration_minutes
        stat.completed_sessions += 1
        stat.avg_session_duration = int(stat.total_focus_minutes / stat.completed_sessions)
        stat.interruptions += session.interruptions
        stat.save()
    
    return Response({'status': 'success', 'message': 'Session completed successfully'})


class DailyFocusGoalListView(generics.ListCreateAPIView):
    serializer_class = DailyFocusGoalSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return DailyFocusGoal.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DailyFocusGoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DailyFocusGoalSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return DailyFocusGoal.objects.filter(user=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weekly_stats(request):
    """
    Get focus stats for the last 7 days
    """
    week_ago = timezone.now().date() - timedelta(days=7)
    
    stats = FocusStat.objects.filter(
        user=request.user,
        date__gte=week_ago
    ).order_by('-date')
    
    serializer = FocusStatSerializer(stats, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def today_progress(request):
    """
    Get today's focus progress
    """
    today = date.today()
    
    # Get today's goal
    try:
        goal = DailyFocusGoal.objects.get(user=request.user, date=today)
    except DailyFocusGoal.DoesNotExist:
        goal = None
    
    # Get today's stats
    try:
        stat = FocusStat.objects.get(user=request.user, date=today)
    except FocusStat.DoesNotExist:
        stat = None
    
    return Response({
        'goal': DailyFocusGoalSerializer(goal).data if goal else None,
        'stats': FocusStatSerializer(stat).data if stat else None
    })