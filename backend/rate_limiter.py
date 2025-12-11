"""
Rate Limiter Module
API rate limiting for request throttling
"""

from typing import Dict, Tuple
from datetime import datetime, timedelta
from collections import defaultdict


class RateLimiter:
    """Token bucket rate limiter with per-user tracking"""
    
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.window_size = 60  # seconds
        self.requests: Dict[str, list] = defaultdict(list)
        self.user_requests: Dict[str, list] = defaultdict(list)  # Track per user
    
    def is_allowed(self, client_id: str, user_id: str = None) -> Tuple[bool, dict]:
        """Check if request is allowed for client or user"""
        now = datetime.now()
        window_start = now - timedelta(seconds=self.window_size)
        
        # Check user-specific limit if user_id provided
        check_id = user_id if user_id else client_id
        request_store = self.user_requests if user_id else self.requests
        
        # Remove old requests outside window
        request_store[check_id] = [
            req_time for req_time in request_store[check_id]
            if req_time > window_start
        ]
        
        request_count = len(request_store[check_id])
        
        if request_count >= self.requests_per_minute:
            oldest_request = request_store[check_id][0]
            reset_time = oldest_request + timedelta(seconds=self.window_size)
            wait_seconds = (reset_time - now).total_seconds()
            
            return False, {
                "remaining": 0,
                "reset_in_seconds": max(0, int(wait_seconds)),
                "user_id": user_id
            }
        
        # Add new request
        request_store[check_id].append(now)
        
        return True, {
            "remaining": self.requests_per_minute - request_count - 1,
            "reset_in_seconds": self.window_size,
            "user_id": user_id
        }


# Global rate limiter instance
_rate_limiter = RateLimiter()


def rate_limit(requests_per_minute: int = 60):
    """Decorator to rate limit function calls"""
    limiter = RateLimiter(requests_per_minute)
    
    def decorator(func):
        async def async_wrapper(request, *args, **kwargs):
            client_id = request.client.host if hasattr(request, 'client') else "unknown"
            allowed, info = limiter.is_allowed(client_id)
            
            if not allowed:
                from fastapi import HTTPException
                raise HTTPException(
                    status_code=429,
                    detail=f"Rate limit exceeded. Try again in {info['reset_in_seconds']}s"
                )
            
            return await func(request, *args, **kwargs)
        
        def sync_wrapper(*args, **kwargs):
            allowed, info = limiter.is_allowed("default")
            
            if not allowed:
                from fastapi import HTTPException
                raise HTTPException(
                    status_code=429,
                    detail=f"Rate limit exceeded. Try again in {info['reset_in_seconds']}s"
                )
            
            return func(*args, **kwargs)
        
        return async_wrapper if hasattr(func, '__await__') else sync_wrapper
    
    return decorator
