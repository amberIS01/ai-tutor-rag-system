"""
Service Discovery Module
Service registration and discovery
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
from logger import logger


class ServiceStatus(str, Enum):
    """Service status"""
    UP = "up"
    DOWN = "down"
    DEGRADED = "degraded"


class ServiceInstance:
    """Service instance"""
    
    def __init__(self, name: str, host: str, port: int, metadata: Dict = None):
        self.name = name
        self.host = host
        self.port = port
        self.metadata = metadata or {}
        self.status = ServiceStatus.UP
        self.last_heartbeat = datetime.now()
        self.registered_at = datetime.now()
    
    def get_url(self) -> str:
        """Get service URL"""
        return f"http://{self.host}:{self.port}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "host": self.host,
            "port": self.port,
            "url": self.get_url(),
            "status": self.status,
            "metadata": self.metadata,
            "registered_at": self.registered_at.isoformat()
        }


class ServiceRegistry:
    """Service registry for service discovery"""
    
    def __init__(self, heartbeat_timeout: int = 30):
        self.services: Dict[str, List[ServiceInstance]] = {}
        self.heartbeat_timeout = heartbeat_timeout
    
    def register(
        self,
        name: str,
        host: str,
        port: int,
        metadata: Dict = None
    ) -> ServiceInstance:
        """Register service instance"""
        instance = ServiceInstance(name, host, port, metadata)
        
        if name not in self.services:
            self.services[name] = []
        
        self.services[name].append(instance)
        logger.info(f"Service registered: {name} at {instance.get_url()}")
        return instance
    
    def deregister(self, name: str, host: str, port: int) -> bool:
        """Deregister service instance"""
        if name not in self.services:
            return False
        
        self.services[name] = [
            s for s in self.services[name]
            if not (s.host == host and s.port == port)
        ]
        
        logger.info(f"Service deregistered: {name} at {host}:{port}")
        return True
    
    def discover(self, name: str) -> List[ServiceInstance]:
        """Discover service instances"""
        instances = self.services.get(name, [])
        
        # Filter out unhealthy instances
        healthy = [
            s for s in instances
            if s.status == ServiceStatus.UP
        ]
        
        return healthy if healthy else instances
    
    def heartbeat(self, name: str, host: str, port: int) -> bool:
        """Record heartbeat from service"""
        if name in self.services:
            for instance in self.services[name]:
                if instance.host == host and instance.port == port:
                    instance.last_heartbeat = datetime.now()
                    return True
        return False
    
    def check_health(self):
        """Check health of all services"""
        now = datetime.now()
        timeout = timedelta(seconds=self.heartbeat_timeout)
        
        for service_instances in self.services.values():
            for instance in service_instances:
                if now - instance.last_heartbeat > timeout:
                    instance.status = ServiceStatus.DOWN
    
    def get_services(self) -> Dict[str, List[Dict]]:
        """Get all registered services"""
        self.check_health()
        return {
            name: [s.to_dict() for s in instances]
            for name, instances in self.services.items()
        }
    
    def get_service_info(self, name: str) -> Optional[Dict]:
        """Get service info"""
        self.check_health()
        instances = self.discover(name)
        if instances:
            return instances[0].to_dict()
        return None


# Global service registry
_service_registry = None


def get_service_registry() -> ServiceRegistry:
    """Get global service registry"""
    global _service_registry
    if _service_registry is None:
        _service_registry = ServiceRegistry()
    return _service_registry
