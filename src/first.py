"""This module demonstrates a simple add_numbers function with type hints."""
def add_numbers(a: int, b: int) -> int:
    """Add two integers and return the result."""
    return a + b

def main():
    """Main function to run the add_numbers function."""
    result = add_numbers(5, 7)
    print(f"The result is {result}")

if __name__ == "__main__":
    main()