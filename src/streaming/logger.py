"""
Logging Module for AMR Detection System

Provides comprehensive logging to both file and console with color-coded output.
"""

import logging
import os
from pathlib import Path
from datetime import datetime
import sys

# Create logs directory
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Log file path
LOG_FILE = LOGS_DIR / f"amr_detection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Color codes for console output
class ColoredFormatter(logging.Formatter):
    """Custom formatter with color codes"""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[41m',   # Red background
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        if sys.platform == 'win32':
            # Windows doesn't support ANSI codes in default terminal
            return super().format(record)
        
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
        
        return super().format(record)


def setup_logger():
    """Setup logger with file and console handlers"""
    
    logger = logging.getLogger("amr_detection")
    logger.setLevel(logging.DEBUG)
    
    # File handler - logs everything
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s - [%(levelname)s] - %(name)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)
    
    # Console handler - info and above
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s - [%(levelname)s] - %(message)s',
        datefmt='%H:%M:%S'
    )
    if sys.platform != 'win32':
        console_handler.setFormatter(ColoredFormatter(
            '%(asctime)s - [%(levelname)s] - %(message)s',
            datefmt='%H:%M:%S'
        ))
    else:
        console_handler.setFormatter(console_format)
    
    # Remove existing handlers
    logger.handlers = []
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger, str(LOG_FILE)


# Initialize logger
logger, log_file_path = setup_logger()


def get_logger():
    """Get the configured logger instance"""
    return logger


def get_log_file_path():
    """Get the current log file path"""
    return log_file_path


if __name__ == "__main__":
    # Test logging
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    print(f"\nLog file: {log_file_path}")
