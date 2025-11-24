from django.urls import path
from . import views

app_name = 'integrations'

urlpatterns = [
    path('', views.IntegrationListView.as_view(), name='integration-list'),
    path('<int:pk>/', views.IntegrationDetailView.as_view(), name='integration-detail'),
    path('<int:pk>/sync/', views.sync_integration, name='sync-integration'),
    path('status/<str:integration_type>/', views.integration_status, name='integration-status'),
    path('sync-logs/', views.SyncLogListView.as_view(), name='sync-log-list'),
]