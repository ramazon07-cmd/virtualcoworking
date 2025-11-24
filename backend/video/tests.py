from django.test import TestCase
from django.contrib.auth.models import User
from teams.models import Team
from .models import Meeting, MeetingParticipant


class MeetingTestCase(TestCase):
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
        self.meeting = Meeting.objects.create(
            title='Test Meeting',
            description='Test meeting description',
            start_time='2025-12-01T10:00:00Z',
            end_time='2025-12-01T11:00:00Z',
            created_by=self.user,
            team=self.team,
            status='scheduled'
        )
        self.meeting.attendees.add(self.user)
        self.participant = MeetingParticipant.objects.create(
            meeting=self.meeting,
            user=self.user,
            status='invited'
        )
    
    def test_meeting_creation(self):
        """Test that a meeting is created correctly"""
        self.assertEqual(self.meeting.title, 'Test Meeting')
        self.assertEqual(self.meeting.description, 'Test meeting description')
        self.assertEqual(self.meeting.created_by.username, 'testuser')
        self.assertEqual(self.meeting.team.name, 'Test Team')
        self.assertEqual(self.meeting.status, 'scheduled')
        self.assertIn(self.user, self.meeting.attendees.all())
    
    def test_participant_creation(self):
        """Test that a meeting participant is created correctly"""
        self.assertEqual(self.participant.meeting.title, 'Test Meeting')
        self.assertEqual(self.participant.user.username, 'testuser')
        self.assertEqual(self.participant.status, 'invited')
    
    def test_meeting_str_representation(self):
        """Test that the string representation is correct"""
        self.assertEqual(str(self.meeting), 'Test Meeting')
    
    def test_participant_str_representation(self):
        """Test that the participant string representation is correct"""
        self.assertEqual(str(self.participant), 'testuser - Test Meeting')
    
    def test_unique_participant_constraint(self):
        """Test that a user can't be added twice to the same meeting"""
        with self.assertRaises(Exception):
            MeetingParticipant.objects.create(
                meeting=self.meeting,
                user=self.user,
                status='joined'
            )