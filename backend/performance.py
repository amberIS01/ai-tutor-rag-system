"""
Performance Profiler
Application performance monitoring and profiling
"""

from typing import Dict, Any
from datetime import datetime
import time
from logger import logger


class PerformanceTracker:
    """Track performance metrics"""
    
    def __init__(self):
        self.metrics = {}
        self.start_times = {}
    
    def start_timer(self, name: str):
        """Start a performance timer"""
        self.start_times[name] = time.time()
    
    def end_timer(self, name: str) -> float:
        """End a performance timer and return elapsed time"""
        if name not in self.start_times:
            return 0
        
        elapsed = time.time() - self.start_times[name]
        
        if name not in self.metrics:
            self.metrics[name] = []
        
        self.metrics[name].append(elapsed)
        del self.start_times[name]
        
        return elapsed
    
    def get_average(self, name: str) -> float:
        """Get average time for operation"""
        if name not in self.metrics or not self.metrics[name]:
            return 0
        
        times = self.metrics[name]
        return sum(times) / len(times)
    
    def get_stats(self, name: str) -> Dict[str, Any]:
        """Get statistics for operation"""
        if name not in self.metrics or not self.metrics[name]:
            return {"count": 0}
        
        times = self.metrics[name]
        return {
            "count": len(times),
            "min": min(times),
            "max": max(times),
            "avg": sum(times) / len(times),
            "total": sum(times)
        }
    
    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get all statistics"""
        return {name: self.get_stats(name) for name in self.metrics}
    
    def reset(self):
        """Reset all metrics"""
        self.metrics.clear()
        self.start_times.clear()


class PerformanceContext:
    """Context manager for performance tracking"""
    
    def __init__(self, name: str, tracker: PerformanceTracker):
        self.name = name
        self.tracker = tracker
    
    def __enter__(self):
        self.tracker.start_timer(self.name)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = self.tracker.end_timer(self.name)
        if elapsed > 0.1:  # Log if took more than 100ms
            logger.warning(f"Performance: {self.name} took {elapsed*1000:.2f}ms")


# Global performance tracker
_performance_tracker = PerformanceTracker()


def get_performance_tracker() -> PerformanceTracker:
    """Get global performance tracker"""
    return _performance_tracker


def performance_context(name: str) -> PerformanceContext:
    """Create performance tracking context"""
    return PerformanceContext(name, _performance_tracker)
