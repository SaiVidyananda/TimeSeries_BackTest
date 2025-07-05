"""This module provides utilities for applying decorators to functions in a module."""
# utils/decorator_utils.py

import inspect
import types


def decorate_module_functions(module, decorators):
    """
    Apply decorators to all functions in a module.

    Args:
        module (module): The imported module (not the path).
        decorators (list): List of decorators to apply (order matters).
    """
    for name, obj in inspect.getmembers(module):
        if isinstance(obj, types.FunctionType) and not name.startswith("_"):
            wrapped = obj
            for decorator in reversed(decorators):  # Apply in decorator stack order
                wrapped = decorator(wrapped)
            setattr(module, name, wrapped)
