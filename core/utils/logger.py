"""
This module utilises the logging module to log messages to a file.
"""

import logging
from logging.handlers import RotatingFileHandler

# Definitions
LOG_PATH: str = ".logs/home-security-system.log"
LOG_MB: int = 5
LOG_FILE_COUNT: int = 5


def get_logger(name: str) -> logging.Logger:
    """This function returns a logger with the given name.
    It sets the logger to log messages to a rotated file.
    """
    # Configure the log messages.
    formatter: logging.Formatter = logging.Formatter(
        fmt='[%(asctime)s] -- [%(levelname)s] -- %(name)s (%(funcName)s): %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger: logging.Logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler: logging.FileHandler = RotatingFileHandler(
        LOG_PATH,
        maxBytes=LOG_MB * 1024 * 1024 / LOG_FILE_COUNT,
        backupCount=LOG_FILE_COUNT
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
