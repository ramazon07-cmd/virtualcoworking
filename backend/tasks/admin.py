from django.contrib import admin
from .models import TaskBoard, TaskColumn, Task


class TaskColumnInline(admin.TabularInline):
    model = TaskColumn
    extra = 3


class TaskBoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'created_at')
    list_filter = ('created_at', 'team')
    search_fields = ('name',)
    inlines = [TaskColumnInline]


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'column', 'assignee', 'priority', 'completed', 'created_at')
    list_filter = ('completed', 'priority', 'column__board__team', 'assignee', 'created_at')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'


admin.site.register(TaskBoard, TaskBoardAdmin)
admin.site.register(TaskColumn)
admin.site.register(Task, TaskAdmin)
