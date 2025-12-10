"""
Metrics Module
Application metrics and monitoring
"""

from typing import Dict, Any
from datetime import datetime, timedelta
from collections import defaultdict


class Metrics:
    """Application metrics collector"""
    
    def __init__(self):
        self.requests_count = 0
        self.errors_count = 0
        self.total_processing_time = 0
        self.pdfs_processed = 0
        self.embeddings_generated = 0
        self.start_time = datetime.now()
        self.request_times = []
    
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
    
    def get_summary(self) -> Dict[str, Any]:
        """Get metrics summary"""
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
