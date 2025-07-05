# tests/test_position_sizer.py

import pandas as pd
import pytest

from src.engine.position_sizer import PositionSizer
from src.engine.transaction_manager import TransactionManager


@pytest.fixture
def tm():
    tm = TransactionManager()
    tm.buy("AAPL", 5, 100)
    tm.buy("GOOG", 10, 200)
    return tm

@pytest.fixture
def empty_tm():
    return TransactionManager()

@pytest.fixture
def sizer(tm):
    return PositionSizer(tm, min_cash_reserve=0.1, max_positions=5)

@pytest.fixture
def empty_sizer(empty_tm):
    return PositionSizer(empty_tm, min_cash_reserve=0.1, max_positions=5)

def test_calculate_quantity_to_buy_normal(sizer):
    qty = sizer.calculate_quantity_to_buy("MSFT", 50, 10000)
    assert isinstance(qty, int)
    assert qty > 0

def test_calculate_quantity_to_buy_low_cash(sizer):
    qty = sizer.calculate_quantity_to_buy("MSFT", 50, 0)
    assert qty == 0

def test_calculate_quantity_to_sell_existing(sizer):
    qty = sizer.calculate_quantity_to_sell("AAPL")
    assert qty == 5

def test_calculate_quantity_to_sell_not_owned(sizer):
    qty = sizer.calculate_quantity_to_sell("MSFT")
    assert qty == 0

def test_calculate_quantity_to_sell_empty(empty_sizer):
    qty = empty_sizer.calculate_quantity_to_sell("AAPL")
    assert qty == 0

def test_fixed_amount_sizing_normal(sizer):
    qty = sizer.fixed_amount_sizing("MSFT", price=100, fixed_amount=1000, cash_available=5000)
    assert qty == 10

def test_fixed_amount_sizing_insufficient_cash(sizer):
    qty = sizer.fixed_amount_sizing("MSFT", price=100, fixed_amount=1000, cash_available=0)
    assert qty == 0

def test_fixed_amount_sizing_slots_zero_but_owned():
    tm = TransactionManager()
    tm.buy("MSFT", 10, 100)
    sizer = PositionSizer(tm, max_positions=1)
    qty = sizer.fixed_amount_sizing("MSFT", price=100, fixed_amount=1000, cash_available=5000)
    assert qty == 10

def test_fixed_amount_sizing_slots_zero_not_owned():
    tm = TransactionManager()
    tm.buy("AAPL", 10, 100)
    tm.buy("GOOG", 10, 200)
    sizer = PositionSizer(tm, max_positions=2)
    qty = sizer.fixed_amount_sizing("MSFT", price=100, fixed_amount=1000, cash_available=5000)
    assert qty == 0
