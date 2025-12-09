"""
Health Check Module
Provides system health monitoring
"""

from typing import Dict
import psutil
import platform


def get_system_info() -> Dict[str, str]:
    """Get system information"""
    return {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version()
    }


def get_resource_usage() -> Dict[str, float]:
    """Get current resource usage"""
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent
    }


def check_health() -> Dict[str, any]:
    """
    Perform health check
    
    Returns:
        Health status dictionary
    """
    try:
        resources = get_resource_usage()
        
        # Determine health status
        healthy = (
            resources["cpu_percent"] < 90 and
            resources["memory_percent"] < 90 and
            resources["disk_percent"] < 90
        )
        
        return {
            "status": "healthy" if healthy else "degraded",
            "resources": resources,
            "checks": {
                "cpu": "ok" if resources["cpu_percent"] < 90 else "warning",
                "memory": "ok" if resources["memory_percent"] < 90 else "warning",
                "disk": "ok" if resources["disk_percent"] < 90 else "warning"
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }





