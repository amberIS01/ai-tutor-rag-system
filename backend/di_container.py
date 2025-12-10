"""
Dependency Injection Module
Manage application dependencies
"""

from typing import Dict, Any, Callable, Optional, Type
from logger import logger


class Container:
    """Dependency injection container"""
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, Callable] = {}
        self._singletons: Dict[str, Any] = {}
    
    def register(self, name: str, service: Any):
        """Register a service"""
        self._services[name] = service
        logger.info(f"Service registered: {name}")
    
    def register_factory(self, name: str, factory: Callable):
        """Register a factory function"""
        self._factories[name] = factory
        logger.info(f"Factory registered: {name}")
    
    def register_singleton(self, name: str, factory: Callable):
        """Register a singleton"""
        self._factories[name] = factory
        # Create instance immediately
        self._singletons[name] = factory()
        logger.info(f"Singleton registered: {name}")
    
    def get(self, name: str) -> Optional[Any]:
        """Get service or dependency"""
        # Check if it's a registered service
        if name in self._services:
            return self._services[name]
        
        # Check if it's a singleton
        if name in self._singletons:
            return self._singletons[name]
        
        # Check if it's a factory
        if name in self._factories:
            return self._factories[name]()
        
        logger.warning(f"Service not found: {name}")
        return None
    
    def has(self, name: str) -> bool:
        """Check if service is registered"""
        return name in self._services or name in self._factories or name in self._singletons
    
    def remove(self, name: str) -> bool:
        """Remove service"""
        removed = False
        
        if name in self._services:
            del self._services[name]
            removed = True
        
        if name in self._factories:
            del self._factories[name]
            removed = True
        
        if name in self._singletons:
            del self._singletons[name]
            removed = True
        
        if removed:
            logger.info(f"Service removed: {name}")
        
        return removed
    
    def clear(self):
        """Clear all services"""
        self._services.clear()
        self._factories.clear()
        self._singletons.clear()
        logger.info("Container cleared")


# Global container instance
_container = Container()


def get_container() -> Container:
    """Get global DI container"""
    return _container


def register_dependency(name: str, service: Any):
    """Register dependency in container"""
    _container.register(name, service)


def get_dependency(name: str) -> Optional[Any]:
    """Get dependency from container"""
    return _container.get(name)
