from django.test import TestCase
from django.contrib.auth.models import User
from teams.models import Team
from .models import Event


class EventTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.team = Team.objects.create(
            name='Test Team',
            description='Test team description',
            owner=self.user
        )
        self.event = Event.objects.create(
            title='Test Event',
            description='Test event description',
            start_time='2025-12-01T10:00:00Z',
            end_time='2025-12-01T11:00:00Z',
            created_by=self.user,
            team=self.team,
            event_type='meeting'
        )
        self.event.attendees.add(self.user)
    
    def test_event_creation(self):
        """Test that an event is created correctly"""
        self.assertEqual(self.event.title, 'Test Event')
        self.assertEqual(self.event.description, 'Test event description')
        self.assertEqual(self.event.created_by.username, 'testuser')
        self.assertEqual(self.event.team.name, 'Test Team')
        self.assertEqual(self.event.event_type, 'meeting')
        self.assertIn(self.user, self.event.attendees.all())
    
    def test_event_str_representation(self):
        """Test that the string representation is correct"""
        self.assertEqual(str(self.event), 'Test Event')
    
    def test_event_ordering(self):
        """Test that events are ordered by start_time"""
        event2 = Event.objects.create(
            title='Second Event',
            description='Second event description',
            start_time='2025-12-01T09:00:00Z',
            end_time='2025-12-01T10:00:00Z',
            created_by=self.user,
            event_type='deadline'
        )
        
        events = Event.objects.all()
        # Events should be ordered by start_time (ascending)
        self.assertEqual(events.first().title, 'Second Event')