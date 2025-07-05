# tests/test_logger.py
import logging
import types

import pytest

from src.utils.decorator_utils import decorate_module_functions
from src.utils.log_helper import handle_exceptions, log_function_call


# Apply both decorators to test them together and separately
@log_function_call
def sample_function(x, y):
    return x + y

@handle_exceptions
def function_with_exception(x, y):
    return x / y  # Raises ZeroDivisionError when y = 0

@log_function_call
@handle_exceptions
def combined_function(x, y):
    return x / y

# --------------------------------------------
# ✅ Tests
# --------------------------------------------

def test_log_function_call(caplog):
    with caplog.at_level(logging.INFO):
        result = sample_function(2, 3)
    assert result == 5
    assert "Starting" in caplog.text
    assert "Ended" in caplog.text

def test_handle_exceptions_logs_exception(caplog):
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ZeroDivisionError):
            function_with_exception(1, 0)
    assert "Exception occurred" in caplog.text
    assert "function_with_exception" in caplog.text
    assert "ZeroDivisionError" in caplog.text

def test_combined_decorators_success(caplog):
    with caplog.at_level(logging.INFO):
        result = combined_function(10, 2)
    assert result == 5
    assert "Starting" in caplog.text
    assert "Ended" in caplog.text

def test_combined_decorators_exception(caplog):
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ZeroDivisionError):
            combined_function(10, 0)
    assert "Exception occurred" in caplog.text
    assert "combined_function" in caplog.text

def test_decorate_module_functions_applies_all(caplog):
    # Create a dummy module
    dummy_module = types.ModuleType("dummy_module")

    # Add functions
    def add(x, y):
        return x + y

    def fail():
        raise ValueError("fail")

    dummy_module.add = add
    dummy_module.fail = fail

    # Apply decorators globally
    decorate_module_functions(dummy_module, [handle_exceptions, log_function_call])

    # Use caplog to capture logs
    with caplog.at_level(logging.INFO):
        result = dummy_module.add(2, 3)
    assert result == 5
    assert "Starting" in caplog.text
    assert "Ended" in caplog.text

    # Now test exception handling
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError, match="fail"):
            dummy_module.fail()
    assert "Exception" in caplog.text