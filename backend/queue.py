"""
Queue Module
Priority queue and task ordering
"""

import heapq
from typing import List, Tuple, Any, Callable, Optional
from datetime import datetime
from enum import Enum


class Priority(int, Enum):
    """Task priority levels"""
    LOW = 3
    MEDIUM = 2
    HIGH = 1
    CRITICAL = 0


class QueuedTask:
    """Task in queue"""
    
    _counter = 0
    
    def __init__(
        self,
        priority: Priority,
        task_id: str,
        func: Callable,
        *args,
        **kwargs
    ):
        self.priority = priority
        self.task_id = task_id
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.created_at = datetime.now()
        self._order = QueuedTask._counter
        QueuedTask._counter += 1
    
    def __lt__(self, other):
        """Comparison for heapq"""
        if self.priority == other.priority:
            return self._order < other._order
        return self.priority < other.priority
    
    async def execute(self):
        """Execute the task"""
        if hasattr(self.func, '__call__'):
            import asyncio
            if asyncio.iscoroutinefunction(self.func):
                return await self.func(*self.args, **self.kwargs)
            else:
                return self.func(*self.args, **self.kwargs)


class PriorityQueue:
    """Priority queue for tasks"""
    
    def __init__(self):
        self.queue: List[QueuedTask] = []
    
    def enqueue(
        self,
        task_id: str,
        func: Callable,
        priority: Priority = Priority.MEDIUM,
        *args,
        **kwargs
    ):
        """Add task to queue"""
        task = QueuedTask(priority, task_id, func, *args, **kwargs)
        heapq.heappush(self.queue, task)
    
    def dequeue(self) -> Optional[QueuedTask]:
        """Remove and return highest priority task"""
        if not self.queue:
            return None
        return heapq.heappop(self.queue)
    
    def peek(self) -> Optional[QueuedTask]:
        """View highest priority task without removing"""
        if not self.queue:
            return None
        return self.queue[0]
    
    def size(self) -> int:
        """Get queue size"""
        return len(self.queue)
    
    def is_empty(self) -> bool:
        """Check if queue is empty"""
        return len(self.queue) == 0
    
    def clear(self):
        """Clear queue"""
        self.queue.clear()


class QueueWorker:
    """Worker that processes queue items"""
    
    def __init__(self, queue: PriorityQueue, num_workers: int = 1):
        self.queue = queue
        self.num_workers = num_workers
        self.running = False
    
    async def start(self):
        """Start workers"""
        self.running = True
        import asyncio
        
        workers = [
            asyncio.create_task(self._worker())
            for _ in range(self.num_workers)
        ]
        
        await asyncio.gather(*workers)
    
    async def _worker(self):
        """Worker coroutine"""
        while self.running:
            task = self.queue.dequeue()
            
            if task:
                try:
                    await task.execute()
                except Exception as e:
                    print(f"Task {task.task_id} failed: {str(e)}")
            else:
                import asyncio
                await asyncio.sleep(0.1)
    
    def stop(self):
        """Stop workers"""
        self.running = False
