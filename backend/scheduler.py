"""
Scheduling Module
Task scheduling and cron jobs
"""

import asyncio
from typing import Callable, Optional
from datetime import datetime, timedelta
from logger import logger


class ScheduledTask:
    """Scheduled task wrapper"""
    
    def __init__(
        self,
        name: str,
        func: Callable,
        interval_seconds: int,
        run_immediately: bool = False
    ):
        self.name = name
        self.func = func
        self.interval_seconds = interval_seconds
        self.run_immediately = run_immediately
        self.last_run = None
        self.next_run = datetime.now() if run_immediately else datetime.now() + timedelta(seconds=interval_seconds)
        self.is_running = False
    
    async def should_run(self) -> bool:
        """Check if task should run"""
        return datetime.now() >= self.next_run
    
    async def execute(self):
        """Execute the task"""
        if self.is_running:
            return
        
        try:
            self.is_running = True
            logger.info(f"Executing scheduled task: {self.name}")
            
            if asyncio.iscoroutinefunction(self.func):
                await self.func()
            else:
                self.func()
            
            self.last_run = datetime.now()
            self.next_run = self.last_run + timedelta(seconds=self.interval_seconds)
            logger.info(f"Scheduled task completed: {self.name}")
        except Exception as e:
            logger.error(f"Scheduled task failed: {self.name} - {str(e)}")
        finally:
            self.is_running = False


class Scheduler:
    """Task scheduler for background jobs"""
    
    def __init__(self):
        self.tasks = {}
        self.running = False
    
    def add_task(
        self,
        name: str,
        func: Callable,
        interval_seconds: int,
        run_immediately: bool = False
    ):
        """Add scheduled task"""
        task = ScheduledTask(name, func, interval_seconds, run_immediately)
        self.tasks[name] = task
        logger.info(f"Task scheduled: {name} (every {interval_seconds}s)")
    
    async def start(self):
        """Start scheduler"""
        self.running = True
        logger.info("Scheduler started")
        
        while self.running:
            for task in self.tasks.values():
                if await task.should_run():
                    await task.execute()
            
            await asyncio.sleep(1)  # Check every second
    
    def stop(self):
        """Stop scheduler"""
        self.running = False
        logger.info("Scheduler stopped")
    
    def remove_task(self, name: str) -> bool:
        """Remove scheduled task"""
        if name in self.tasks:
            del self.tasks[name]
            logger.info(f"Task removed: {name}")
            return True
        return False
    
    def get_tasks_status(self):
        """Get all tasks status"""
        return {
            name: {
                "name": task.name,
                "interval_seconds": task.interval_seconds,
                "last_run": task.last_run.isoformat() if task.last_run else None,
                "next_run": task.next_run.isoformat(),
                "is_running": task.is_running
            }
            for name, task in self.tasks.items()
        }


# Global scheduler instance
_scheduler = None


def get_scheduler() -> Scheduler:
    """Get global scheduler instance"""
    global _scheduler
    if _scheduler is None:
        _scheduler = Scheduler()
    return _scheduler
