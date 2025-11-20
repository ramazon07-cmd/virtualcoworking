from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from .models import File, Note
from teams.models import Team
from .serializers import FileSerializer, NoteSerializer, NoteCreateSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def file_list(request):
    # Get files for teams where user is a member
    teams = Team.objects.filter(members=request.user)
    files = File.objects.filter(team__in=teams)
    serializer = FileSerializer(files, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    serializer = FileSerializer(data=request.data)
    if serializer.is_valid():
        # Check if user is member of the team
        team = serializer.validated_data.get('team')
        if team and not team.members.filter(id=request.user.id).exists():
            return Response({'error': 'You are not a member of this team'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        # Save file
        serializer.save(uploaded_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_file(request, file_id):
    file_obj = get_object_or_404(File, id=file_id)
    # Check if user is member of the team
    if not file_obj.team.members.filter(id=request.user.id).exists():
        return Response({'error': 'You are not a member of this team'}, 
                      status=status.HTTP_403_FORBIDDEN)
    
    # In a real implementation, you would serve the file
    # For now, we'll just return the file information
    serializer = FileSerializer(file_obj)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_file(request, file_id):
    file_obj = get_object_or_404(File, id=file_id)
    # Check if user is the uploader or team owner
    if (file_obj.uploaded_by != request.user and 
        file_obj.team.owner != request.user):
        return Response({'error': 'You do not have permission to delete this file'}, 
                      status=status.HTTP_403_FORBIDDEN)
    
    file_obj.delete()
    return Response({'message': 'File deleted successfully'}, 
                  status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def note_list(request):
    # Get notes for teams where user is a member
    teams = Team.objects.filter(members=request.user)
    notes = Note.objects.filter(team__in=teams)
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_note(request):
    serializer = NoteCreateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        # Check if user is member of the team
        team = serializer.validated_data.get('team')
        if team and not team.members.filter(id=request.user.id).exists():
            return Response({'error': 'You are not a member of this team'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        note = serializer.save()
        return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    # Check if user is member of the team
    if not note.team.members.filter(id=request.user.id).exists():
        return Response({'error': 'You are not a member of this team'}, 
                      status=status.HTTP_403_FORBIDDEN)
    
    serializer = NoteSerializer(note)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    # Check if user is the author or team owner
    if (note.author != request.user and 
        note.team.owner != request.user):
        return Response({'error': 'You do not have permission to update this note'}, 
                      status=status.HTTP_403_FORBIDDEN)
    
    serializer = NoteSerializer(note, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    # Check if user is the author or team owner
    if (note.author != request.user and 
        note.team.owner != request.user):
        return Response({'error': 'You do not have permission to delete this note'}, 
                      status=status.HTTP_403_FORBIDDEN)
    
    note.delete()
    return Response({'message': 'Note deleted successfully'}, 
                  status=status.HTTP_204_NO_CONTENT)
