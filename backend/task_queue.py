"""
Async Task Queue
Background task processing
"""

import asyncio
from typing import Callable, Any, List, Dict
from enum import Enum
from datetime import datetime
from logger import logger


class TaskStatus(str, Enum):
    """Task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Task:
    """Async task wrapper"""
    
    def __init__(self, task_id: str, func: Callable, *args, **kwargs):
        self.task_id = task_id
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.status = TaskStatus.PENDING
        self.result = None
        self.error = None
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
    
    async def execute(self):
        """Execute the task"""
        try:
            self.status = TaskStatus.RUNNING
            self.started_at = datetime.now()
            
            if asyncio.iscoroutinefunction(self.func):
                self.result = await self.func(*self.args, **self.kwargs)
            else:
                self.result = self.func(*self.args, **self.kwargs)
            
            self.status = TaskStatus.COMPLETED
            logger.info(f"Task {self.task_id} completed successfully")
        except Exception as e:
            self.status = TaskStatus.FAILED
            self.error = str(e)
            logger.error(f"Task {self.task_id} failed: {self.error}")
        finally:
            self.completed_at = datetime.now()


class TaskQueue:
    """Async task queue for background processing"""
    
    def __init__(self, max_workers: int = 5):
        self.max_workers = max_workers
        self.tasks: Dict[str, Task] = {}
        self.queue: asyncio.Queue = None
    
    async def initialize(self):
        """Initialize the task queue"""
        self.queue = asyncio.Queue()
        for _ in range(self.max_workers):
            asyncio.create_task(self._worker())
    
    async def _worker(self):
        """Worker coroutine processing tasks"""
        while True:
            task = await self.queue.get()
            try:
                await task.execute()
            finally:
                self.queue.task_done()
    
    async def enqueue(self, task_id: str, func: Callable, *args, **kwargs) -> str:
        """Enqueue a task"""
        task = Task(task_id, func, *args, **kwargs)
        self.tasks[task_id] = task
        await self.queue.put(task)
        return task_id
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get task status and result"""
        if task_id not in self.tasks:
            return {"error": "Task not found"}
        
        task = self.tasks[task_id]
        return {
            "task_id": task_id,
            "status": task.status,
            "result": task.result,
            "error": task.error,
            "created_at": task.created_at.isoformat(),
            "completed_at": task.completed_at.isoformat() if task.completed_at else None
        }
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Get all tasks status"""
        return [self.get_task_status(task_id) for task_id in self.tasks]


# Global task queue
_task_queue = None


async def get_task_queue() -> TaskQueue:
    """Get global task queue"""
    global _task_queue
    if _task_queue is None:
        _task_queue = TaskQueue()
        await _task_queue.initialize()
    return _task_queue
