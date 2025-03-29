import logging
import os
import sys
from logging.handlers import RotatingFileHandler

def setup_logging(log_level='INFO', log_file=None, max_bytes=10485760, backup_count=5):
    """
    Configure application logging
    
    Args:
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file (str, optional): Path to log file. If None, only console logging is used.
        max_bytes (int): Maximum log file size before rotation
        backup_count (int): Number of backup log files to keep
    """
    # Convert string level to logging level
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Base configuration with console handler
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    handlers = [logging.StreamHandler(sys.stdout)]
    
    # Add file handler if log file is specified
    if log_file:
        # Create log directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # Create rotating file handler
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setFormatter(logging.Formatter(log_format))
        handlers.append(file_handler)
    
    # Configure the root logger
    logging.basicConfig(
        level=numeric_level,
        format=log_format,
        handlers=handlers
    )
    
    # Set lower log level for some noisy libraries
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    
    # Log startup message
    logging.info(f"Logging initialized at {log_level} level")

def get_logger(name):
    """
    Get a logger with the given name
    
    Args:
        name (str): Logger name, typically __name__
        
    Returns:
        logging.Logger: Configured logger
    """
    return logging.getLogger(name)