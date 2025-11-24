from django.urls import path
from . import views

app_name = 'focus'

urlpatterns = [
    path('sessions/', views.FocusSessionListView.as_view(), name='session-list'),
    path('sessions/<int:pk>/', views.FocusSessionDetailView.as_view(), name='session-detail'),
    path('sessions/<int:pk>/complete/', views.complete_session, name='complete-session'),
    path('goals/', views.DailyFocusGoalListView.as_view(), name='goal-list'),
    path('goals/<int:pk>/', views.DailyFocusGoalDetailView.as_view(), name='goal-detail'),
    path('stats/weekly/', views.weekly_stats, name='weekly-stats'),
    path('progress/today/', views.today_progress, name='today-progress'),
]