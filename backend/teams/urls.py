from django.urls import path
from . import views

urlpatterns = [
    path('', views.team_list, name='team_list'),
    path('create/', views.create_team, name='create_team'),
    path('<int:team_id>/', views.team_detail, name='team_detail'),
    path('<int:team_id>/update/', views.update_team, name='update_team'),
    path('<int:team_id>/delete/', views.delete_team, name='delete_team'),
    path('<int:team_id>/members/', views.team_members, name='team_members'),
    path('<int:team_id>/members/add/', views.add_member, name='add_member'),
    path('<int:team_id>/members/<int:user_id>/remove/', views.remove_member, name='remove_member'),
    path('<int:team_id>/members/<int:user_id>/role/', views.update_member_role, name='update_member_role'),
]