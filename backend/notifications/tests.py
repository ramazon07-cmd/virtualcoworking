from django.test import TestCase
from django.contrib.auth.models import User
from teams.models import Team
from .models import Notification


class NotificationTestCase(TestCase):
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
        self.notification = Notification.objects.create(
            recipient=self.user,
            team=self.team,
            title='Test Notification',
            message='This is a test notification',
            notification_type='info'
        )
    
    def test_notification_creation(self):
        """Test that a notification is created correctly"""
        self.assertEqual(self.notification.recipient.username, 'testuser')
        self.assertEqual(self.notification.team.name, 'Test Team')
        self.assertEqual(self.notification.title, 'Test Notification')
        self.assertEqual(self.notification.message, 'This is a test notification')
        self.assertEqual(self.notification.notification_type, 'info')
        self.assertFalse(self.notification.is_read)
    
    def test_notification_str_representation(self):
        """Test that the string representation is correct"""
        self.assertEqual(str(self.notification), 'Test Notification - testuser')
    
    def test_notification_ordering(self):
        """Test that notifications are ordered by created_at descending"""
        notification2 = Notification.objects.create(
            recipient=self.user,
            title='Second Notification',
            message='This is the second test notification',
            notification_type='warning'
        )
        
        notifications = Notification.objects.all()
        # The most recent notification should be first
        self.assertEqual(notifications.first().title, 'Second Notification')