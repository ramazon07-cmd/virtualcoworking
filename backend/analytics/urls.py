from django.urls import path
from . import views

urlpatterns = [
    path('team/<int:team_id>/', views.team_analytics, name='team_analytics'),
    path('user/', views.user_analytics, name='user_analytics'),
    path('team/<int:team_id>/productivity/', views.team_productivity_report, name='team_productivity_report'),
]