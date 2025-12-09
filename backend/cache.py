"""
Cache Module
In-memory caching for performance optimization
"""

from typing import Any, Optional, Dict
from datetime import datetime, timedelta
import hashlib


class CacheEntry:
    """Cache entry with timestamp and TTL"""
    
    def __init__(self, value: Any, ttl_seconds: int = 3600):
        self.value = value
        self.created_at = datetime.now()
        self.ttl_seconds = ttl_seconds
    
    def is_expired(self) -> bool:
        """Check if cache entry is expired"""
        expiry_time = self.created_at + timedelta(seconds=self.ttl_seconds)
        return datetime.now() > expiry_time


class Cache:
    """Simple in-memory cache with TTL support"""
    
    def __init__(self):
        self._cache: Dict[str, CacheEntry] = {}
    
    def set(self, key: str, value: Any, ttl_seconds: int = 3600):
        """Set cache value"""
        self._cache[key] = CacheEntry(value, ttl_seconds)
    
    def get(self, key: str) -> Optional[Any]:
        """Get cache value"""
        if key not in self._cache:
            return None
        
        entry = self._cache[key]
        if entry.is_expired():
            del self._cache[key]
            return None
        
        return entry.value
    
    def delete(self, key: str):
        """Delete cache entry"""
        if key in self._cache:
            del self._cache[key]
    
    def clear(self):
        """Clear all cache entries"""
        self._cache.clear()
    
    def cleanup_expired(self):
        """Remove all expired entries"""
        expired_keys = [k for k, v in self._cache.items() if v.is_expired()]
        for key in expired_keys:
            del self._cache[key]


# Global cache instance
_global_cache = Cache()


def cache_key(*args, **kwargs) -> str:
    """Generate cache key from arguments"""
    key_str = str(args) + str(sorted(kwargs.items()))
    return hashlib.md5(key_str.encode()).hexdigest()


def cache_result(ttl_seconds: int = 3600):
    """Decorator to cache function results"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            key = cache_key(func.__name__, *args, **kwargs)
            cached = _global_cache.get(key)
            
            if cached is not None:
                return cached
            
            result = func(*args, **kwargs)
            _global_cache.set(key, result, ttl_seconds)
            return result
        return wrapper
    return decorator
