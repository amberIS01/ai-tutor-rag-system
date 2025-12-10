"""
Pagination Module
Pagination utilities for API responses
"""

from typing import TypeVar, Generic, List, Dict, Any
from math import ceil

T = TypeVar('T')


class PaginationParams:
    """Pagination parameters"""
    
    def __init__(self, page: int = 1, page_size: int = 10):
        self.page = max(1, page)
        self.page_size = max(1, min(page_size, 100))  # Max 100 items per page
    
    @property
    def skip(self) -> int:
        """Get skip count"""
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        """Get limit"""
        return self.page_size


class PaginatedResponse(Generic[T]):
    """Paginated response wrapper"""
    
    def __init__(self, items: List[T], total: int, page: int, page_size: int):
        self.items = items
        self.total = total
        self.page = page
        self.page_size = page_size
        self.total_pages = ceil(total / page_size) if page_size > 0 else 1
        self.has_next = page < self.total_pages
        self.has_prev = page > 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "items": self.items,
            "pagination": {
                "page": self.page,
                "page_size": self.page_size,
                "total": self.total,
                "total_pages": self.total_pages,
                "has_next": self.has_next,
                "has_prev": self.has_prev
            }
        }


def paginate(items: List[T], params: PaginationParams) -> PaginatedResponse[T]:
    """Paginate a list of items"""
    total = len(items)
    start = params.skip
    end = start + params.page_size
    
    paginated_items = items[start:end]
    return PaginatedResponse(
        items=paginated_items,
        total=total,
        page=params.page,
        page_size=params.page_size
    )
