import pytest
from src.first import add_numbers

def test_add_positive_numbers():
    assert add_numbers(2, 3) == 5

def test_add_zero():
    assert add_numbers(0, 0) == 0

def test_add_negative_and_positive():
    assert add_numbers(-2, 5) == 3

def test_add_two_negatives():
    assert add_numbers(-4, -1) == -5