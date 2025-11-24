from django.test import TestCase
from django.contrib.auth.models import User
from .models import Integration


class IntegrationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.integration = Integration.objects.create(
            user=self.user,
            integration_type='google_calendar',
            access_token='test_access_token',
            refresh_token='test_refresh_token'
        )
    
    def test_integration_creation(self):
        """Test that an integration is created correctly"""
        self.assertEqual(self.integration.user.username, 'testuser')
        self.assertEqual(self.integration.integration_type, 'google_calendar')
        self.assertEqual(self.integration.access_token, 'test_access_token')
        self.assertEqual(self.integration.refresh_token, 'test_refresh_token')
        self.assertTrue(self.integration.is_active)
    
    def test_integration_str_representation(self):
        """Test that the string representation is correct"""
        self.assertEqual(str(self.integration), 'testuser - Google Calendar')
    
    def test_unique_integration_constraint(self):
        """Test that a user can't have duplicate integrations of the same type"""
        with self.assertRaises(Exception):
            Integration.objects.create(
                user=self.user,
                integration_type='google_calendar',
                access_token='another_token'
            )