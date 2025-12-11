"""
Batch Processing Module
Process items in batches for efficiency
"""

from typing import List, Callable, Any, Optional
from datetime import datetime
from logger import logger


class BatchProcessor:
    """Process items in batches with optimizations"""
    
    def __init__(
        self,
        batch_size: int = 100,
        max_wait_ms: int = 5000,
        enable_parallel: bool = True
    ):
        self.batch_size = batch_size
        self.max_wait_ms = max_wait_ms
        self.enable_parallel = enable_parallel
        self.items: List[Any] = []
        self.last_process_time = datetime.now()
        self.processed_count = 0
        self.failed_count = 0
    
    def add_item(self, item: Any):
        """Add item to batch"""
        self.items.append(item)
    
    def should_process(self) -> bool:
        """Check if batch should be processed"""
        if len(self.items) >= self.batch_size:
            return True
        
        elapsed = (datetime.now() - self.last_process_time).total_seconds() * 1000
        if elapsed >= self.max_wait_ms and self.items:
            return True
        
        return False
    
    async def process(self, processor_func: Callable) -> List[Any]:
        """Process batch with optional parallelization"""
        if not self.items:
            return []
        
        batch = self.items.copy()
        self.items.clear()
        self.last_process_time = datetime.now()
        
        try:
            import asyncio
            
            if self.enable_parallel and len(batch) > 1:
                # Process items in parallel
                if asyncio.iscoroutinefunction(processor_func):
                    tasks = [processor_func(item) for item in batch]
                    result = await asyncio.gather(*tasks, return_exceptions=True)
                    # Filter out exceptions
                    result = [r for r in result if not isinstance(r, Exception)]
                else:
                    # Sequential processing for sync functions
                    result = [processor_func(item) for item in batch]
            else:
                # Process as single batch
                if asyncio.iscoroutinefunction(processor_func):
                    result = await processor_func(batch)
                else:
                    result = processor_func(batch)
            
            self.processed_count += len(batch)
            return result
        except Exception as e:
            self.failed_count += len(batch)
            logger.error(f"Batch processing failed: {str(e)}")
            return []
    
    def get_statistics(self) -> dict:
        """Get processing statistics"""
        return {
            "processed": self.processed_count,
            "failed": self.failed_count,
            "pending": len(self.items),
            "success_rate": self.processed_count / (self.processed_count + self.failed_count) 
                           if (self.processed_count + self.failed_count) > 0 else 0
        }
    
    def get_pending_count(self) -> int:
        """Get number of pending items"""
        return len(self.items)
    
    def clear(self):
        """Clear all pending items"""
        self.items.clear()


class BatchManager:
    """Manage multiple batch processors"""
    
    def __init__(self):
        self.processors = {}
    
    def create_processor(
        self,
        name: str,
        batch_size: int = 100,
        max_wait_ms: int = 5000
    ) -> BatchProcessor:
        """Create new batch processor"""
        processor = BatchProcessor(batch_size, max_wait_ms)
        self.processors[name] = processor
        return processor
    
    def get_processor(self, name: str) -> Optional[BatchProcessor]:
        """Get batch processor"""
        return self.processors.get(name)
    
    def add_item(self, processor_name: str, item: Any) -> bool:
        """Add item to processor"""
        if processor_name in self.processors:
            self.processors[processor_name].add_item(item)
            return True
        return False
    
    async def process_all(self, processor_func: Callable) -> dict:
        """Process all batch processors"""
        results = {}
        
        for name, processor in self.processors.items():
            if processor.should_process():
                results[name] = await processor.process(processor_func)
        
        return results
    
    def get_status(self) -> dict:
        """Get status of all processors"""
        return {
            name: {
                "pending_items": processor.get_pending_count(),
                "batch_size": processor.batch_size
            }
            for name, processor in self.processors.items()
        }


# Global batch manager
_batch_manager = None


def get_batch_manager() -> BatchManager:
    """Get global batch manager"""
    global _batch_manager
    if _batch_manager is None:
        _batch_manager = BatchManager()
    return _batch_manager
