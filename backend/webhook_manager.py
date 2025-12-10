"""
Webhook Manager
Handle webhooks for external integrations
"""

from typing import Dict, List, Callable, Any
import hashlib
import hmac
from datetime import datetime
from logger import logger


class WebhookEvent:
    """Webhook event wrapper"""
    
    def __init__(self, event_type: str, data: Dict[str, Any]):
        self.event_type = event_type
        self.data = data
        self.timestamp = datetime.now().isoformat()
        self.event_id = hashlib.md5(
            f"{event_type}{self.timestamp}".encode()
        ).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "data": self.data,
            "timestamp": self.timestamp
        }


class WebhookManager:
    """Manage webhooks and subscriptions"""
    
    def __init__(self, secret_key: str = "webhook-secret"):
        self.secret_key = secret_key
        self.subscriptions: Dict[str, List[Callable]] = {}
        self.webhook_history = []
        self.max_history = 1000
    
    def subscribe(self, event_type: str, callback: Callable):
        """Subscribe to webhook event"""
        if event_type not in self.subscriptions:
            self.subscriptions[event_type] = []
        
        self.subscriptions[event_type].append(callback)
        logger.info(f"Webhook subscribed: {event_type}")
    
    def unsubscribe(self, event_type: str, callback: Callable):
        """Unsubscribe from webhook event"""
        if event_type in self.subscriptions:
            self.subscriptions[event_type] = [
                cb for cb in self.subscriptions[event_type]
                if cb != callback
            ]
            logger.info(f"Webhook unsubscribed: {event_type}")
    
    async def trigger(self, event: WebhookEvent):
        """Trigger webhook event"""
        self.webhook_history.append(event.to_dict())
        
        if len(self.webhook_history) > self.max_history:
            self.webhook_history.pop(0)
        
        if event.event_type in self.subscriptions:
            for callback in self.subscriptions[event.event_type]:
                try:
                    if hasattr(callback, '__call__'):
                        result = callback(event)
                        if hasattr(result, '__await__'):
                            await result
                except Exception as e:
                    logger.error(f"Webhook callback error: {str(e)}")
    
    def generate_signature(self, payload: str) -> str:
        """Generate webhook signature"""
        return hmac.new(
            self.secret_key.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def verify_signature(self, payload: str, signature: str) -> bool:
        """Verify webhook signature"""
        expected = self.generate_signature(payload)
        return hmac.compare_digest(expected, signature)
    
    def get_history(self, event_type: str = None, limit: int = 100) -> List[Dict]:
        """Get webhook history"""
        history = self.webhook_history
        
        if event_type:
            history = [
                e for e in history
                if e["event_type"] == event_type
            ]
        
        return history[-limit:]


# Global webhook manager
_webhook_manager = None


def get_webhook_manager() -> WebhookManager:
    """Get global webhook manager"""
    global _webhook_manager
    if _webhook_manager is None:
        _webhook_manager = WebhookManager()
    return _webhook_manager
