"""
Metrics Module
Application metrics and monitoring
"""

from typing import Dict, Any
from datetime import datetime, timedelta
from collections import defaultdict


class Metrics:
    """Enhanced application metrics collector with detailed monitoring"""
    
    def __init__(self):
        self.requests_count = 0
        self.errors_count = 0
        self.total_processing_time = 0
        self.pdfs_processed = 0
        self.embeddings_generated = 0
        self.start_time = datetime.now()
        self.request_times = []
        self.endpoint_metrics = defaultdict(lambda: {"count": 0, "errors": 0, "total_time": 0})
        self.status_codes = defaultdict(int)
        self.user_metrics = defaultdict(lambda: {"requests": 0, "errors": 0})
    
    def record_request(self, processing_time: float, success: bool = True):
        """Record API request"""
        self.requests_count += 1
        self.request_times.append(processing_time)
        
        if not success:
            self.errors_count += 1
        
        self.total_processing_time += processing_time
    
    def record_pdf_processed(self):
        """Record PDF processing"""
        self.pdfs_processed += 1
    
    def record_embeddings(self, count: int = 1):
        """Record embeddings generated"""
        self.embeddings_generated += count
    
    def record_endpoint(self, endpoint: str, processing_time: float, status_code: int, user_id: str = None):
        """Record endpoint-specific metrics"""
        self.endpoint_metrics[endpoint]["count"] += 1
        self.endpoint_metrics[endpoint]["total_time"] += processing_time
        if status_code >= 400:
            self.endpoint_metrics[endpoint]["errors"] += 1
        
        self.status_codes[status_code] += 1
        
        if user_id:
            self.user_metrics[user_id]["requests"] += 1
            if status_code >= 400:
                self.user_metrics[user_id]["errors"] += 1
    
    def get_summary(self) -> Dict[str, Any]:
        """Get comprehensive metrics summary"""
        uptime = datetime.now() - self.start_time
        avg_request_time = (
            self.total_processing_time / self.requests_count 
            if self.requests_count > 0 
            else 0
        )
        
        return {
            "uptime_seconds": uptime.total_seconds(),
            "requests_count": self.requests_count,
            "errors_count": self.errors_count,
            "error_rate": (
                (self.errors_count / self.requests_count * 100)
                if self.requests_count > 0
                else 0
            ),
            "avg_request_time_ms": round(avg_request_time * 1000, 2),
            "pdfs_processed": self.pdfs_processed,
            "embeddings_generated": self.embeddings_generated,
            "endpoint_metrics": dict(self.endpoint_metrics),
            "status_codes": dict(self.status_codes),
            "unique_users": len(self.user_metrics)
        }
    
    def get_endpoint_stats(self, endpoint: str) -> Dict[str, Any]:
        """Get statistics for specific endpoint"""
        metrics = self.endpoint_metrics[endpoint]
        avg_time = metrics["total_time"] / metrics["count"] if metrics["count"] > 0 else 0
        return {
            "count": metrics["count"],
            "errors": metrics["errors"],
            "avg_time_ms": round(avg_time * 1000, 2),
            "error_rate": (metrics["errors"] / metrics["count"] * 100) if metrics["count"] > 0 else 0
        }
    
    def reset(self):
        """Reset metrics"""
        self.requests_count = 0
        self.errors_count = 0
        self.total_processing_time = 0
        self.request_times = []


# Global metrics instance
_metrics = Metrics()


def get_metrics() -> Metrics:
    """Get global metrics instance"""
    return _metrics
