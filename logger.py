import logging
from logging.handlers import RotatingFileHandler
from config import LOG_CONFIG

def setup_logger():
    """
    Setup application logger with rotation and debug level
    """
    logger = logging.getLogger('AnsibleInventoryReporter')
    logger.setLevel(logging.DEBUG)  # Set to DEBUG for more detailed logs

    # Create handlers
    file_handler = RotatingFileHandler(
        LOG_CONFIG['filename'],
        maxBytes=5*1024*1024,  # 5MB
        backupCount=5
    )
    console_handler = logging.StreamHandler()

    # Set levels
    file_handler.setLevel(logging.DEBUG)
    console_handler.setLevel(logging.INFO)

    # Create formatters and add it to handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger