from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Meeting, MeetingParticipant
from .serializers import MeetingSerializer, MeetingCreateSerializer


class MeetingListView(generics.ListCreateAPIView):
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Return meetings for the current user or team meetings
        return Meeting.objects.filter(
            attendees=self.request.user
        ).distinct() | Meeting.objects.filter(
            created_by=self.request.user
        ).distinct()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class MeetingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Meeting.objects.filter(attendees=self.request.user).distinct() | Meeting.objects.filter(created_by=self.request.user).distinct()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_meeting(request, pk):
    """
    Join a meeting
    """
    meeting = get_object_or_404(Meeting, pk=pk)
    
    # Check if user is invited to the meeting
    if request.user not in meeting.attendees.all():
        return Response({'error': 'You are not invited to this meeting'}, status=status.HTTP_403_FORBIDDEN)
    
    # Create or update participant record
    participant, created = MeetingParticipant.objects.get_or_create(
        meeting=meeting,
        user=request.user,
        defaults={'status': 'joined', 'join_time': timezone.now()}
    )
    
    if not created:
        participant.status = 'joined'
        participant.join_time = timezone.now()
        participant.save(update_fields=['status', 'join_time'])
    
    # Update meeting status if needed
    if meeting.status == 'scheduled':
        meeting.status = 'in_progress'
        meeting.save(update_fields=['status'])
    
    return Response({'status': 'success', 'message': 'Joined meeting successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def leave_meeting(request, pk):
    """
    Leave a meeting
    """
    meeting = get_object_or_404(Meeting, pk=pk)
    
    # Get participant record
    try:
        participant = MeetingParticipant.objects.get(meeting=meeting, user=request.user)
        participant.status = 'left'
        participant.leave_time = timezone.now()
        participant.save(update_fields=['status', 'leave_time'])
        
        return Response({'status': 'success', 'message': 'Left meeting successfully'})
    except MeetingParticipant.DoesNotExist:
        return Response({'error': 'You are not a participant in this meeting'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def upcoming_meetings(request):
    """
    Get upcoming meetings for the next 7 days
    """
    now = timezone.now()
    week_from_now = now + timedelta(days=7)
    
    meetings = Meeting.objects.filter(
        attendees=request.user,
        start_time__gte=now,
        start_time__lte=week_from_now
    ).distinct() | Meeting.objects.filter(
        created_by=request.user,
        start_time__gte=now,
        start_time__lte=week_from_now
    ).distinct()
    
    serializer = MeetingSerializer(meetings, many=True)
    return Response(serializer.data)