"""
Feature Flag Manager
Feature flagging for gradual rollouts
"""

from typing import Dict, List, Any
from datetime import datetime
from logger import logger


class FeatureFlag:
    """Feature flag definition"""
    
    def __init__(
        self,
        name: str,
        enabled: bool = False,
        percentage: int = 0,
        description: str = ""
    ):
        self.name = name
        self.enabled = enabled
        self.percentage = min(100, max(0, percentage))
        self.description = description
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "enabled": self.enabled,
            "percentage": self.percentage,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class FeatureFlagManager:
    """Manage feature flags"""
    
    def __init__(self):
        self.flags: Dict[str, FeatureFlag] = {}
    
    def create_flag(
        self,
        name: str,
        enabled: bool = False,
        percentage: int = 0,
        description: str = ""
    ) -> FeatureFlag:
        """Create feature flag"""
        flag = FeatureFlag(name, enabled, percentage, description)
        self.flags[name] = flag
        logger.info(f"Feature flag created: {name}")
        return flag
    
    def update_flag(
        self,
        name: str,
        enabled: bool = None,
        percentage: int = None
    ) -> bool:
        """Update feature flag"""
        if name not in self.flags:
            return False
        
        flag = self.flags[name]
        if enabled is not None:
            flag.enabled = enabled
        if percentage is not None:
            flag.percentage = min(100, max(0, percentage))
        
        flag.updated_at = datetime.now()
        logger.info(f"Feature flag updated: {name}")
        return True
    
    def is_enabled(self, name: str, user_id: str = None) -> bool:
        """Check if feature flag is enabled"""
        if name not in self.flags:
            return False
        
        flag = self.flags[name]
        
        if not flag.enabled:
            return False
        
        if flag.percentage == 100:
            return True
        
        if flag.percentage == 0:
            return False
        
        # Hash user_id to determine if user is in the percentage
        if user_id:
            hash_value = int(
                hashlib.md5(f"{name}{user_id}".encode()).hexdigest(),
                16
            )
            return (hash_value % 100) < flag.percentage
        
        return True
    
    def get_flag(self, name: str) -> FeatureFlag:
        """Get feature flag"""
        return self.flags.get(name)
    
    def get_all_flags(self) -> Dict[str, Dict[str, Any]]:
        """Get all feature flags"""
        return {name: flag.to_dict() for name, flag in self.flags.items()}
    
    def delete_flag(self, name: str) -> bool:
        """Delete feature flag"""
        if name in self.flags:
            del self.flags[name]
            logger.info(f"Feature flag deleted: {name}")
            return True
        return False


# Global feature flag manager
_flag_manager = None


def get_flag_manager() -> FeatureFlagManager:
    """Get global feature flag manager"""
    global _flag_manager
    if _flag_manager is None:
        _flag_manager = FeatureFlagManager()
    return _flag_manager
