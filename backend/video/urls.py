from django.urls import path
from . import views

app_name = 'video'

urlpatterns = [
    path('meetings/', views.MeetingListView.as_view(), name='meeting-list'),
    path('meetings/<int:pk>/', views.MeetingDetailView.as_view(), name='meeting-detail'),
    path('meetings/<int:pk>/join/', views.join_meeting, name='join-meeting'),
    path('meetings/<int:pk>/leave/', views.leave_meeting, name='leave-meeting'),
    path('meetings/upcoming/', views.upcoming_meetings, name='upcoming-meetings'),
]