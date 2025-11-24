from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            bio='Test bio',
            location='Test Location',
            company_name='Test Company',
            role='member'
        )
    
    def test_profile_creation(self):
        """Test that a user profile is created correctly"""
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.bio, 'Test bio')
        self.assertEqual(self.profile.location, 'Test Location')
        self.assertEqual(self.profile.company_name, 'Test Company')
        self.assertEqual(self.profile.role, 'member')
        self.assertFalse(self.profile.is_verified)
        self.assertIsNotNone(self.profile.verification_token)
    
    def test_get_full_name(self):
        """Test that get_full_name returns the correct name"""
        # Test with no first/last name
        self.assertEqual(self.profile.get_full_name(), 'testuser')
        
        # Test with first and last name
        self.user.first_name = 'John'
        self.user.last_name = 'Doe'
        self.user.save()
        self.assertEqual(self.profile.get_full_name(), 'John Doe')
    
    def test_profile_str_representation(self):
        """Test that the string representation is correct"""
        self.assertEqual(str(self.profile), 'testuser Profile')
