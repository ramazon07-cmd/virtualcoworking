from django.urls import path
from . import views

app_name = 'calendar_app'

urlpatterns = [
    path('events/', views.EventListView.as_view(), name='event-list'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('events/upcoming/', views.upcoming_events, name='upcoming-events'),
    path('events/<int:year>/<int:month>/<int:day>/', views.events_by_date, name='events-by-date'),
]