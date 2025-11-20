from django.urls import path
from . import views

urlpatterns = [
    # Chat functionality is primarily handled via WebSockets
    # But we can have some REST endpoints for chat history, etc.
    path('history/<str:room_name>/', views.chat_history, name='chat_history'),
]