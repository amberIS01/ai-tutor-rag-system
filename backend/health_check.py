"""
Health Check Service
Extended health monitoring with detailed endpoints
"""

from typing import Dict, Any
import psutil
from datetime import datetime
from logger import logger


class HealthCheckService:
    """Comprehensive health check service with enhanced monitoring"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.last_check = None
        self.check_history = []
        self.max_history = 100
    
    def check_cpu_health(self) -> Dict[str, Any]:
        """Check CPU health"""
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        
        return {
            "status": "healthy" if cpu_percent < 80 else "warning" if cpu_percent < 95 else "unhealthy",
            "usage_percent": cpu_percent,
            "core_count": cpu_count,
            "threshold": 80
        }
    
    def check_memory_health(self) -> Dict[str, Any]:
        """Check memory health"""
        memory = psutil.virtual_memory()
        
        return {
            "status": "healthy" if memory.percent < 80 else "warning" if memory.percent < 95 else "unhealthy",
            "usage_percent": memory.percent,
            "used_mb": memory.used // (1024 * 1024),
            "total_mb": memory.total // (1024 * 1024),
            "available_mb": memory.available // (1024 * 1024),
            "threshold": 80
        }
    
    def check_disk_health(self) -> Dict[str, Any]:
        """Check disk health"""
        disk = psutil.disk_usage('/')
        
        return {
            "status": "healthy" if disk.percent < 80 else "warning" if disk.percent < 95 else "unhealthy",
            "usage_percent": disk.percent,
            "used_mb": disk.used // (1024 * 1024),
            "total_mb": disk.total // (1024 * 1024),
            "free_mb": disk.free // (1024 * 1024),
            "threshold": 80
        }
    
    def check_process_health(self) -> Dict[str, Any]:
        """Check process health"""
        process = psutil.Process()
        
        return {
            "status": "healthy",
            "pid": process.pid,
            "memory_mb": process.memory_info().rss // (1024 * 1024),
            "cpu_percent": process.cpu_percent(),
            "threads": process.num_threads()
        }
    
    def get_uptime(self) -> Dict[str, Any]:
        """Get application uptime"""
        uptime = datetime.now() - self.start_time
        
        return {
            "uptime_seconds": uptime.total_seconds(),
            "uptime_minutes": uptime.total_seconds() / 60,
            "uptime_hours": uptime.total_seconds() / 3600,
            "start_time": self.start_time.isoformat()
        }
    
    def perform_health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check"""
        health_status = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "healthy",
            "checks": {
                "cpu": self.check_cpu_health(),
                "memory": self.check_memory_health(),
                "disk": self.check_disk_health(),
                "process": self.check_process_health()
            },
            "uptime": self.get_uptime()
        }
        
        # Determine overall status
        statuses = [
            health_status["checks"]["cpu"]["status"],
            health_status["checks"]["memory"]["status"],
            health_status["checks"]["disk"]["status"]
        ]
        
        if "unhealthy" in statuses:
            health_status["overall_status"] = "unhealthy"
        elif "warning" in statuses:
            health_status["overall_status"] = "warning"
        
        self.last_check = health_status
        self.check_history.append(health_status)
        
        # Keep last max_history checks
        if len(self.check_history) > self.max_history:
            self.check_history.pop(0)
        
        return health_status
    
    def get_detailed_status(self) -> Dict[str, Any]:
        """Get detailed health status with history"""
        return {
            "current": self.last_check or self.perform_health_check(),
            "history_count": len(self.check_history),
            "start_time": self.start_time.isoformat(),
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds()
        }
    
    def get_readiness(self) -> Dict[str, bool]:
        """Check if service is ready to accept traffic"""
        health = self.perform_health_check()
        return {
            "ready": health["overall_status"] != "unhealthy",
            "status": health["overall_status"]
        }
    
    def get_liveness(self) -> Dict[str, bool]:
        """Check if service is alive"""
        return {
            "alive": True,
            "timestamp": datetime.now().isoformat()
        }


# Global health check service
_health_service = None


def get_health_service() -> HealthCheckService:
    """Get global health check service"""
    global _health_service
    if _health_service is None:
        _health_service = HealthCheckService()
    return _health_service
