from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Event, Reminder
from .serializers import EventSerializer, EventCreateSerializer


class EventListView(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Return events for the current user or team events
        return Event.objects.filter(
            attendees=self.request.user
        ).distinct() | Event.objects.filter(
            created_by=self.request.user
        ).distinct()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Event.objects.filter(attendees=self.request.user).distinct() | Event.objects.filter(created_by=self.request.user).distinct()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def upcoming_events(request):
    """
    Get events for the next 7 days
    """
    now = timezone.now()
    week_from_now = now + timedelta(days=7)
    
    events = Event.objects.filter(
        attendees=request.user,
        start_time__gte=now,
        start_time__lte=week_from_now
    ).distinct() | Event.objects.filter(
        created_by=request.user,
        start_time__gte=now,
        start_time__lte=week_from_now
    ).distinct()
    
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def events_by_date(request, year, month, day):
    """
    Get events for a specific date
    """
    from datetime import datetime
    
    try:
        date = datetime(year, month, day)
        next_day = date + timedelta(days=1)
        
        events = Event.objects.filter(
            attendees=request.user,
            start_time__gte=date,
            start_time__lt=next_day
        ).distinct() | Event.objects.filter(
            created_by=request.user,
            start_time__gte=date,
            start_time__lt=next_day
        ).distinct()
        
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    except ValueError:
        return Response({'error': 'Invalid date'}, status=status.HTTP_400_BAD_REQUEST)