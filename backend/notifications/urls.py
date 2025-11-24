from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification-list'),
    path('<int:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),
    path('<int:pk>/mark-as-read/', views.mark_as_read, name='mark-as-read'),
    path('mark-all-as-read/', views.mark_all_as_read, name='mark-all-as-read'),
]