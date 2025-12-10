"""
Logging Formatter
Enhanced logging with formatting and rotation
"""

import logging
import logging.handlers
from datetime import datetime
from pathlib import Path


class ColoredFormatter(logging.Formatter):
    """Colored log formatter for console output"""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m'  # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        return super().format(record)


def setup_rotating_file_handler(
    logger_name: str,
    log_dir: str = "./logs",
    max_bytes: int = 10485760,
    backup_count: int = 5
) -> logging.Handler:
    """Setup rotating file handler"""
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    filename = f"{log_dir}/{logger_name}_{datetime.now().strftime('%Y%m%d')}.log"
    handler = logging.handlers.RotatingFileHandler(
        filename,
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    return handler


def setup_timed_rotating_handler(
    logger_name: str,
    log_dir: str = "./logs",
    when: str = "midnight",
    interval: int = 1
) -> logging.Handler:
    """Setup timed rotating file handler"""
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    filename = f"{log_dir}/{logger_name}.log"
    handler = logging.handlers.TimedRotatingFileHandler(
        filename,
        when=when,
        interval=interval
    )
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    return handler


def get_logger(
    name: str,
    level: int = logging.INFO,
    use_color: bool = True,
    enable_file_logging: bool = True
) -> logging.Logger:
    """Get configured logger"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    if use_color:
        formatter = ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    if enable_file_logging:
        file_handler = setup_rotating_file_handler(name)
        logger.addHandler(file_handler)
    
    return logger
