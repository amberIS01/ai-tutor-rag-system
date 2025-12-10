"""
A/B Testing Module
A/B testing framework for experiments
"""

import random
from typing import Dict, List, Any, Optional
from datetime import datetime
from logger import logger


class Variant:
    """A/B test variant"""
    
    def __init__(self, name: str, weight: float = 0.5):
        self.name = name
        self.weight = min(1.0, max(0.0, weight))
        self.conversions = 0
        self.visitors = 0
    
    def get_conversion_rate(self) -> float:
        """Get conversion rate"""
        return (self.conversions / self.visitors) if self.visitors > 0 else 0


class Experiment:
    """A/B test experiment"""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.variants: Dict[str, Variant] = {}
        self.created_at = datetime.now()
        self.started_at = None
        self.ended_at = None
        self.is_active = False
    
    def add_variant(self, name: str, weight: float = 0.5):
        """Add variant to experiment"""
        variant = Variant(name, weight)
        self.variants[name] = variant
    
    def start(self):
        """Start experiment"""
        self.is_active = True
        self.started_at = datetime.now()
        logger.info(f"Experiment started: {self.name}")
    
    def end(self):
        """End experiment"""
        self.is_active = False
        self.ended_at = datetime.now()
        logger.info(f"Experiment ended: {self.name}")
    
    def assign_variant(self, user_id: str) -> str:
        """Assign user to variant"""
        if not self.is_active or not self.variants:
            return None
        
        # Seed with user_id for consistency
        random.seed(hash(user_id) % 2**32)
        rand = random.random()
        
        cumulative = 0
        for variant_name, variant in self.variants.items():
            cumulative += variant.weight
            if rand <= cumulative:
                return variant_name
        
        return list(self.variants.keys())[0]
    
    def record_visitor(self, variant_name: str):
        """Record visitor for variant"""
        if variant_name in self.variants:
            self.variants[variant_name].visitors += 1
    
    def record_conversion(self, variant_name: str):
        """Record conversion for variant"""
        if variant_name in self.variants:
            self.variants[variant_name].conversions += 1
    
    def get_results(self) -> Dict[str, Any]:
        """Get experiment results"""
        return {
            "name": self.name,
            "is_active": self.is_active,
            "variants": {
                name: {
                    "visitors": variant.visitors,
                    "conversions": variant.conversions,
                    "conversion_rate": variant.get_conversion_rate()
                }
                for name, variant in self.variants.items()
            }
        }


class ABTestManager:
    """A/B testing manager"""
    
    def __init__(self):
        self.experiments: Dict[str, Experiment] = {}
    
    def create_experiment(self, name: str, description: str = "") -> Experiment:
        """Create new experiment"""
        experiment = Experiment(name, description)
        self.experiments[name] = experiment
        return experiment
    
    def get_experiment(self, name: str) -> Optional[Experiment]:
        """Get experiment"""
        return self.experiments.get(name)
    
    def get_all_experiments(self) -> List[Dict[str, Any]]:
        """Get all experiments"""
        return [exp.get_results() for exp in self.experiments.values()]


# Global A/B test manager
_ab_test_manager = None


def get_ab_test_manager() -> ABTestManager:
    """Get global A/B test manager"""
    global _ab_test_manager
    if _ab_test_manager is None:
        _ab_test_manager = ABTestManager()
    return _ab_test_manager
