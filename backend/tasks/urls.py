from django.urls import path
from . import views

urlpatterns = [
    path('boards/', views.board_list, name='board_list'),
    path('boards/create/', views.create_board, name='create_board'),
    path('boards/<int:board_id>/', views.board_detail, name='board_detail'),
    path('boards/<int:board_id>/update/', views.update_board, name='update_board'),
    path('boards/<int:board_id>/delete/', views.delete_board, name='delete_board'),
    path('columns/<int:column_id>/tasks/', views.column_tasks, name='column_tasks'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/update/', views.update_task, name='update_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('tasks/<int:task_id>/move/', views.move_task, name='move_task'),
    path('tasks/<int:task_id>/assign/', views.assign_task, name='assign_task'),
]