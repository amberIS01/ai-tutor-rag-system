"""
Logging Configuration Module
Provides centralized logging for the application
"""

import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_logger(name: str = "ai_tutor", level: int = logging.INFO) -> logging.Logger:
    """
    Setup and configure application logger
    
    Args:
        name: Logger name
        level: Logging level
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Format with structured data
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(funcName)s() - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger


def log_structured(logger: logging.Logger, level: str, message: str, **kwargs):
    """
    Log with structured data
    
    Args:
        logger: Logger instance
        level: Log level (info, warning, error, etc.)
        message: Log message
        **kwargs: Additional structured data
    """
    extra_data = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
    full_message = f"{message} | {extra_data}" if extra_data else message
    getattr(logger, level)(full_message)


# Create default logger
logger = setup_logger()





