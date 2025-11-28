import logging
import os
import sys
from datetime import datetime
from src.config.settings import Settings

def setup_logger(name="ELEVEN"):
    """Configure and return a logger instance"""
    
    # Create logs directory if it doesn't exist
    if not os.path.exists(Settings.LOGS_DIR):
        os.makedirs(Settings.LOGS_DIR)
        
    # Generate log filename with timestamp
    log_filename = f"{datetime.now().strftime('%Y-%m-%d')}.log"
    log_path = os.path.join(Settings.LOGS_DIR, log_filename)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(name)

logger = setup_logger()
