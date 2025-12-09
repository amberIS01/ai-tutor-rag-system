"""
Utility Functions
Helper functions for the application
"""

from datetime import datetime
from typing import Dict, Any


def format_timestamp() -> str:
    """Get formatted timestamp"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to remove dangerous characters
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    import re
    # Remove path separators and dangerous chars
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    return filename[:255]  # Limit length


def format_file_size(bytes: int) -> str:
    """
    Format file size in human-readable format
    
    Args:
        bytes: File size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.1f} TB"


def create_response(
    success: bool,
    data: Any = None,
    message: str = "",
    error: str = ""
) -> Dict[str, Any]:
    """
    Create standardized API response
    
    Args:
        success: Whether operation was successful
        data: Response data
        message: Success message
        error: Error message
        
    Returns:
        Formatted response dictionary
    """
    response = {
        "success": success,
        "timestamp": format_timestamp()
    }
    
    if data is not None:
        response["data"] = data
    
    if message:
        response["message"] = message
    
    if error:
        response["error"] = error
    
    return response





