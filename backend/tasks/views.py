from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import TaskBoard, TaskColumn, Task
from teams.models import Team
from .serializers import TaskBoardSerializer, TaskBoardCreateSerializer, TaskSerializer, TaskCreateSerializer, TaskUpdateSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def board_list(request):
    # Get boards for teams where user is a member
    teams = Team.objects.filter(members=request.user)
    boards = TaskBoard.objects.filter(team__in=teams)
    serializer = TaskBoardSerializer(boards, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_board(request):
    serializer = TaskBoardCreateSerializer(data=request.data)
    if serializer.is_valid():
        # Check if user is member of the team
        team = serializer.validated_data.get('team')
        if team and not team.members.filter(id=request.user.id).exists():
            return Response({'error': 'You are not a member of this team'}, 
                          status=status.HTTP_403_FORBIDDEN)
        board = serializer.save()
        return Response(TaskBoardSerializer(board).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def board_detail(request, board_id):
    board = get_object_or_404(TaskBoard, id=board_id)
    # Check if user is member of the team
    if not board.team.members.filter(id=request.user.id).exists():
        return Response({'error': 'You are not a member of this team'}, 
                      status=status.HTTP_403_FORBIDDEN)
    serializer = TaskBoardSerializer(board)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_board(request, board_id):
    board = get_object_or_404(TaskBoard, id=board_id)
    # Check if user is owner of the team
    if board.team.owner != request.user:
        return Response({'error': 'Only team owner can update board'}, 
                      status=status.HTTP_403_FORBIDDEN)
    serializer = TaskBoardCreateSerializer(board, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(TaskBoardSerializer(board).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_board(request, board_id):
    board = get_object_or_404(TaskBoard, id=board_id)
    # Check if user is owner of the team
    if board.team.owner != request.user:
        return Response({'error': 'Only team owner can delete board'}, 
                      status=status.HTTP_403_FORBIDDEN)
    board.delete()
    return Response({'message': 'Board deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def column_tasks(request, column_id):
    column = get_object_or_404(TaskColumn, id=column_id)
    # Check if user is member of the team
    if not column.board.team.members.filter(id=request.user.id).exists():
        return Response({'error': 'You are not a member of this team'}, 
                      status=status.HTTP_403_FORBIDDEN)
    tasks = Task.objects.filter(column=column)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_list(request):
    # Get tasks assigned to user or created by user
    tasks = Task.objects.filter(assignee=request.user) | Task.objects.filter(creator=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    serializer = TaskCreateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        # Check if user is member of the team
        column = serializer.validated_data.get('column')
        if column and not column.board.team.members.filter(id=request.user.id).exists():
            return Response({'error': 'You are not a member of this team'}, 
                          status=status.HTTP_403_FORBIDDEN)
        task = serializer.save()
        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    # Check if user is member of the team
    if not task.column.board.team.members.filter(id=request.user.id).exists():
        return Response({'error': 'You are not a member of this team'}, 
                      status=status.HTTP_403_FORBIDDEN)
    serializer = TaskSerializer(task)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    # Check if user is assignee, creator or team owner
    if (task.assignee != request.user and 
        task.creator != request.user and 
        task.column.board.team.owner != request.user):
        return Response({'error': 'You do not have permission to update this task'}, 
                      status=status.HTTP_403_FORBIDDEN)
    serializer = TaskUpdateSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(TaskSerializer(task).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    # Check if user is assignee, creator or team owner
    if (task.assignee != request.user and 
        task.creator != request.user and 
        task.column.board.team.owner != request.user):
        return Response({'error': 'You do not have permission to delete this task'}, 
                      status=status.HTTP_403_FORBIDDEN)
    task.delete()
    return Response({'message': 'Task deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def move_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    # Check if user is member of the team
    if not task.column.board.team.members.filter(id=request.user.id).exists():
        return Response({'error': 'You are not a member of this team'}, 
                      status=status.HTTP_403_FORBIDDEN)
    
    new_column_id = request.data.get('column_id')
    if not new_column_id:
        return Response({'error': 'column_id is required'}, 
                      status=status.HTTP_400_BAD_REQUEST)
    
    new_column = get_object_or_404(TaskColumn, id=new_column_id)
    # Check if new column is in the same board
    if new_column.board != task.column.board:
        return Response({'error': 'Cannot move task to a column in a different board'}, 
                      status=status.HTTP_400_BAD_REQUEST)
    
    task.column = new_column
    task.save()
    return Response(TaskSerializer(task).data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def assign_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    # Check if user is member of the team
    if not task.column.board.team.members.filter(id=request.user.id).exists():
        return Response({'error': 'You are not a member of this team'}, 
                      status=status.HTTP_403_FORBIDDEN)
    
    assignee_id = request.data.get('assignee_id')
    if not assignee_id:
        return Response({'error': 'assignee_id is required'}, 
                      status=status.HTTP_400_BAD_REQUEST)
    
    assignee = get_object_or_404(task.column.board.team.members, id=assignee_id)
    task.assignee = assignee
    task.save()
    return Response(TaskSerializer(task).data)
