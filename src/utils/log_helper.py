"""This module provides logging utilities for the backtesting framework.
It includes decorators for logging function calls and handling exceptions.
"""
# utils/logger.py
import logging
import os
from functools import wraps

# Setup log folder and file
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "backtest.log")

# Setup global logger
logger = logging.getLogger("backtester")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler(LOG_FILE)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(filename)s | %(funcName)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Optional: console output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

# Decorator: Logs function calls
def log_function_call(func):
    """Decorator that logs the start and end of a function call, including 
    its arguments and return value."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info("Starting function: %s", func.__name__)
        logger.debug("Function %s called with args: %s, kwargs: %s", func.__name__, args, kwargs)
        result = func(*args, **kwargs)
        logger.info("Ended function: %s", func.__name__)
        logger.debug("Function %s returned: %s", func.__name__, result)
        return result
    return wrapper

# Decorator: Logs uncaught exceptions
def handle_exceptions(func):
    """Decorator that logs exceptions raised by the function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exception:
            logger.exception("Exception occurred: %s", exception)
            raise
    return wrapper
