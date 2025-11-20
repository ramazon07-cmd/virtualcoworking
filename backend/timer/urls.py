from django.urls import path
from . import views

urlpatterns = [
    path('sessions/', views.timer_session_list, name='timer_session_list'),
    path('sessions/start/', views.start_timer, name='start_timer'),
    path('sessions/<int:session_id>/stop/', views.stop_timer, name='stop_timer'),
    path('sessions/<int:session_id>/delete/', views.delete_timer_session, name='delete_timer_session'),
    path('stats/', views.timer_stats, name='timer_stats'),
]