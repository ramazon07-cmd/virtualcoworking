from celery import shared_task
from django.utils import timezone
from datetime import date
from .models import FocusSession, FocusStat


@shared_task
def calculate_daily_focus_stats():
    """
    Calculate daily focus statistics for all users
    """
    today = date.today()
    yesterday = today - timezone.timedelta(days=1)
    
    # Get all completed focus sessions from yesterday
    completed_sessions = FocusSession.objects.filter(
        is_completed=True,
        end_time__date=yesterday
    )
    
    # Group by user and calculate stats
    user_stats = {}
    for session in completed_sessions:
        user_id = session.user.id
        if user_id not in user_stats:
            user_stats[user_id] = {
                'user': session.user,
                'team': session.team,
                'total_minutes': 0,
                'session_count': 0,
                'interruptions': 0
            }
        
        user_stats[user_id]['total_minutes'] += session.actual_duration_minutes or 0
        user_stats[user_id]['session_count'] += 1
        user_stats[user_id]['interruptions'] += session.interruptions
    
    # Create or update FocusStat records
    stats_created = 0
    for user_id, stats in user_stats.items():
        avg_duration = stats['total_minutes'] // stats['session_count'] if stats['session_count'] > 0 else 0
        
        FocusStat.objects.update_or_create(
            user=stats['user'],
            date=yesterday,
            defaults={
                'team': stats['team'],
                'total_focus_minutes': stats['total_minutes'],
                'completed_sessions': stats['session_count'],
                'avg_session_duration': avg_duration,
                'interruptions': stats['interruptions']
            }
        )
        stats_created += 1
    
    return f"Calculated focus stats for {stats_created} users"