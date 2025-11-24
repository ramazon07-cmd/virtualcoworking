from django.test import TestCase
from django.contrib.auth.models import User
from teams.models import Team
from .models import FocusSession, DailyFocusGoal, FocusStat


class FocusTestCase(TestCase):
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
        self.focus_session = FocusSession.objects.create(
            user=self.user,
            team=self.team,
            focus_type='pomodoro',
            start_time='2025-12-01T10:00:00Z',
            end_time='2025-12-01T10:25:00Z',
            duration_minutes=25
        )
        self.daily_goal = DailyFocusGoal.objects.create(
            user=self.user,
            team=self.team,
            date='2025-12-01',
            target_hours=8.0
        )
        self.focus_stat = FocusStat.objects.create(
            user=self.user,
            team=self.team,
            date='2025-12-01',
            total_focus_minutes=120,
            completed_sessions=3,
            avg_session_duration=40
        )
    
    def test_focus_session_creation(self):
        """Test that a focus session is created correctly"""
        self.assertEqual(self.focus_session.user.username, 'testuser')
        self.assertEqual(self.focus_session.team.name, 'Test Team')
        self.assertEqual(self.focus_session.focus_type, 'pomodoro')
        self.assertEqual(self.focus_session.duration_minutes, 25)
        self.assertFalse(self.focus_session.is_completed)
    
    def test_daily_goal_creation(self):
        """Test that a daily focus goal is created correctly"""
        self.assertEqual(self.daily_goal.user.username, 'testuser')
        self.assertEqual(self.daily_goal.team.name, 'Test Team')
        self.assertEqual(str(self.daily_goal.date), '2025-12-01')
        self.assertEqual(float(self.daily_goal.target_hours), 8.0)
    
    def test_focus_stat_creation(self):
        """Test that a focus stat is created correctly"""
        self.assertEqual(self.focus_stat.user.username, 'testuser')
        self.assertEqual(self.focus_stat.team.name, 'Test Team')
        self.assertEqual(str(self.focus_stat.date), '2025-12-01')
        self.assertEqual(self.focus_stat.total_focus_minutes, 120)
        self.assertEqual(self.focus_stat.completed_sessions, 3)
        self.assertEqual(self.focus_stat.avg_session_duration, 40)
    
    def test_focus_session_str_representation(self):
        """Test that the focus session string representation is correct"""
        self.assertEqual(str(self.focus_session), 'testuser - pomodoro session on 2025-12-01')
    
    def test_daily_goal_str_representation(self):
        """Test that the daily goal string representation is correct"""
        self.assertEqual(str(self.daily_goal), 'testuser - Goal for 2025-12-01')
    
    def test_focus_stat_str_representation(self):
        """Test that the focus stat string representation is correct"""
        self.assertEqual(str(self.focus_stat), 'testuser - Stats for 2025-12-01')