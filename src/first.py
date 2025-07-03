"""This module demonstrates a simple add_numbers function with type hints."""
from src.utils.decorator_utils import decorate_module_functions
from src.utils.log_helper import handle_exceptions, log_function_call


def add_numbers(a: int, b: int) -> int:
    """Add two integers and return the result. """
    return a + b

def main():
    """Main function to run the add_numbers function."""
    result = add_numbers(5, 7)
    print(f"The result is {result}")

decorate_module_functions(module=__import__(__name__), decorators=[handle_exceptions, log_function_call])


if __name__ == "__main__":
    main()

