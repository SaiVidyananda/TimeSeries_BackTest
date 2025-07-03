"""This module provides logging utilities for the backtesting framework.
It includes decorators for logging function calls and handling exceptions.
"""
# utils/logger.py
import logging
import os
from functools import wraps
from logging.handlers import TimedRotatingFileHandler

# Setup log folder and file
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "backtest.log")

# Setup global logger
logger = logging.getLogger("backtester")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = TimedRotatingFileHandler(
        LOG_FILE,
        when='H',       # Rotate every hour
        interval=1,     # Every 1 hour
        backupCount=2,  # Keep last 2 files (~2 hours)
        encoding='utf-8'
    )
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(real_file)s | %(real_func)s | %(message)s",
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
        file_name = os.path.basename(func.__code__.co_filename)
        logger.info("Starting function",
                    extra={"real_func": func.__name__,"real_file": file_name})
        logger.debug("Function %s called with args: %s, kwargs: %s", func.__name__, args,
                     kwargs, extra={"real_func": func.__name__, "real_file": file_name})
        result = func(*args, **kwargs)
        logger.info("Ended function",
                    extra={"real_func": func.__name__, "real_file": file_name})
        logger.debug("Function %s returned: %s", func.__name__, result,
                     extra={"real_func": func.__name__, "real_file": file_name})
        return result
    return wrapper

# Decorator: Logs uncaught exceptions
def handle_exceptions(func):
    """Decorator that logs exceptions raised by the function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        file_name = os.path.basename(func.__code__.co_filename)
        try:
            return func(*args, **kwargs)
        except Exception as exception:
            logger.exception("Exception occurred: %s", exception,
                     extra={"real_func": func.__name__, "real_file": file_name})
            raise
    return wrapper
