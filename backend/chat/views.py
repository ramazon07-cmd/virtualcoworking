from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_history(request, room_name):
    # In a real implementation, you would retrieve chat history from a database
    # For now, we'll return an empty list
    return Response({
        'room_name': room_name,
        'messages': []
    })
