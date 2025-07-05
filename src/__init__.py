
"""This module initializes the src package and imports key functions and utilities."""
# src/__init__.py

from .engine.executor import Executor
from .engine.portfolio_valuator import PortfolioValuator
from .engine.transaction_manager import TransactionManager
from .first import add_numbers, main
from .strategy.flip_strategy import FlipStrategy
from .utils.data_handler import download_data, fill_missing
from .utils.decorator_utils import decorate_module_functions
from .utils.log_helper import handle_exceptions, log_function_call, logger

__all__ = ["add_numbers", "main", "log_function_call", "handle_exceptions",
           "decorate_module_functions", "download_data", "fill_missing", 
           "PortfolioValuator", "TransactionManager", "logger", "FlipStrategy",
           "Executor"]
