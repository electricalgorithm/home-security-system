"""
This module utilises the logging module to log messages to a file.
"""
import logging
import os

# Definitions
LOG_PATH: str = str(os.path.expanduser("~/.home-security-system/logs/hss.log"))
LOG_MB: int = 5
LOG_FILE_COUNT: int = 5


def get_logger(name: str) -> logging.Logger:
    """This function returns a logger with the given name.
    It sets the logger to log messages to a rotated file.
    """
    # Create log directory if not exists.
    log_dir: str = os.path.dirname(LOG_PATH)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    # Configure the log messages.
    formatter: logging.Formatter = logging.Formatter(
        fmt='[%(asctime)s] -- [%(levelname)s] -- %(name)s (%(funcName)s): %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger: logging.Logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(LOG_PATH)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
