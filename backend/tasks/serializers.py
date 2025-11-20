from rest_framework import serializers
from .models import TaskBoard, TaskColumn, Task
from teams.models import Team
from django.contrib.auth.models import User


class TaskColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskColumn
        fields = ('id', 'name', 'order')


class TaskBoardSerializer(serializers.ModelSerializer):
    columns = TaskColumnSerializer(many=True, read_only=True)
    
    class Meta:
        model = TaskBoard
        fields = ('id', 'name', 'team', 'created_at', 'updated_at', 'columns')


class TaskBoardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskBoard
        fields = ('name', 'team')
        
    def create(self, validated_data):
        board = TaskBoard.objects.create(**validated_data)
        # Create default columns
        TaskColumn.objects.create(board=board, name='To Do', order=1)
        TaskColumn.objects.create(board=board, name='In Progress', order=2)
        TaskColumn.objects.create(board=board, name='Done', order=3)
        return board


class TaskSerializer(serializers.ModelSerializer):
    assignee = serializers.StringRelatedField(read_only=True)
    creator = serializers.StringRelatedField(read_only=True)
    column = TaskColumnSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'assignee', 'creator', 'column', 
                  'priority', 'due_date', 'created_at', 'updated_at', 'completed')


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'description', 'column', 'priority', 'due_date')
        
    def create(self, validated_data):
        user = self.context['request'].user
        task = Task.objects.create(creator=user, **validated_data)
        return task


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'description', 'priority', 'due_date', 'completed')