"""
Rate Limiter Module
API rate limiting for request throttling
"""

from typing import Dict, Tuple
from datetime import datetime, timedelta
from collections import defaultdict


class RateLimiter:
    """Token bucket rate limiter"""
    
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.window_size = 60  # seconds
        self.requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, client_id: str) -> Tuple[bool, dict]:
        """Check if request is allowed for client"""
        now = datetime.now()
        window_start = now - timedelta(seconds=self.window_size)
        
        # Remove old requests outside window
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if req_time > window_start
        ]
        
        request_count = len(self.requests[client_id])
        
        if request_count >= self.requests_per_minute:
            oldest_request = self.requests[client_id][0]
            reset_time = oldest_request + timedelta(seconds=self.window_size)
            wait_seconds = (reset_time - now).total_seconds()
            
            return False, {
                "remaining": 0,
                "reset_in_seconds": max(0, int(wait_seconds))
            }
        
        # Add new request
        self.requests[client_id].append(now)
        
        return True, {
            "remaining": self.requests_per_minute - request_count - 1,
            "reset_in_seconds": self.window_size
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
