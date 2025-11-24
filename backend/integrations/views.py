from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Integration, SyncLog
from .serializers import IntegrationSerializer, IntegrationCreateSerializer, SyncLogSerializer


class IntegrationListView(generics.ListCreateAPIView):
    serializer_class = IntegrationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Integration.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class IntegrationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IntegrationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Integration.objects.filter(user=self.request.user)


class SyncLogListView(generics.ListAPIView):
    serializer_class = SyncLogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return SyncLog.objects.filter(integration__user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sync_integration(request, pk):
    """
    Trigger a sync for a specific integration
    """
    integration = get_object_or_404(Integration, pk=pk, user=request.user)
    
    # Create a sync log entry
    sync_log = SyncLog.objects.create(
        integration=integration,
        sync_type='manual_sync'
    )
    
    # In a real implementation, you would trigger the actual sync process here
    # For now, we'll just mark it as completed
    sync_log.status = 'completed'
    sync_log.records_synced = 0
    sync_log.save(update_fields=['status', 'records_synced'])
    
    return Response({'status': 'success', 'message': 'Sync started successfully'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def integration_status(request, integration_type):
    """
    Get the status of a specific integration type for the current user
    """
    try:
        integration = Integration.objects.get(
            user=request.user,
            integration_type=integration_type
        )
        serializer = IntegrationSerializer(integration)
        return Response(serializer.data)
    except Integration.DoesNotExist:
        return Response({'error': 'Integration not found'}, status=status.HTTP_404_NOT_FOUND)