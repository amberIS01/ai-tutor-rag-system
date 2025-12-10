"""
Analytics Module
Track and analyze user behavior
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
from logger import logger


class Event:
    """Analytics event"""
    
    def __init__(self, event_type: str, user_id: str, data: Dict[str, Any] = None):
        self.event_type = event_type
        self.user_id = user_id
        self.data = data or {}
        self.timestamp = datetime.now()


class AnalyticsEngine:
    """Analytics tracking and analysis"""
    
    def __init__(self, max_events: int = 10000):
        self.events: List[Event] = []
        self.max_events = max_events
        self.event_counts = defaultdict(int)
    
    def track_event(self, event_type: str, user_id: str, data: Dict[str, Any] = None):
        """Track an event"""
        event = Event(event_type, user_id, data)
        self.events.append(event)
        self.event_counts[event_type] += 1
        
        # Remove old events if exceeding limit
        if len(self.events) > self.max_events:
            self.events = self.events[-self.max_events:]
        
        logger.info(f"Event tracked: {event_type} by {user_id}")
    
    def get_event_count(self, event_type: str) -> int:
        """Get total count for event type"""
        return self.event_counts.get(event_type, 0)
    
    def get_user_events(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all events for user"""
        return [
            {
                "event_type": e.event_type,
                "timestamp": e.timestamp.isoformat(),
                "data": e.data
            }
            for e in self.events if e.user_id == user_id
        ]
    
    def get_daily_stats(self, days: int = 7) -> Dict[str, int]:
        """Get daily event statistics"""
        stats = defaultdict(int)
        cutoff = datetime.now() - timedelta(days=days)
        
        for event in self.events:
            if event.timestamp >= cutoff:
                date_key = event.timestamp.strftime("%Y-%m-%d")
                stats[date_key] += 1
        
        return dict(stats)
    
    def get_top_events(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top events by frequency"""
        return sorted(
            [
                {"event_type": name, "count": count}
                for name, count in self.event_counts.items()
            ],
            key=lambda x: x["count"],
            reverse=True
        )[:limit]
    
    def get_funnel_analysis(self, events: List[str]) -> Dict[str, Any]:
        """Analyze conversion funnel"""
        result = {
            "total_users": len(set(e.user_id for e in self.events))
        }
        
        for i, event_type in enumerate(events):
            count = len(set(
                e.user_id for e in self.events
                if e.event_type == event_type
            ))
            result[f"step_{i+1}"] = {
                "event": event_type,
                "unique_users": count
            }
        
        return result
    
    def clear_old_events(self, days: int = 30):
        """Clear events older than specified days"""
        cutoff = datetime.now() - timedelta(days=days)
        self.events = [e for e in self.events if e.timestamp >= cutoff]
        logger.info(f"Old events cleared (older than {days} days)")


# Global analytics engine
_analytics = None


def get_analytics() -> AnalyticsEngine:
    """Get global analytics engine"""
    global _analytics
    if _analytics is None:
        _analytics = AnalyticsEngine()
    return _analytics
