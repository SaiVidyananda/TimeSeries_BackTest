# tests/test_portfolio_valuator.py

import pandas as pd
import pytest

from src.engine.portfolio_valuator import PortfolioValuator
from src.engine.transaction_manager import TransactionManager


@pytest.fixture
def price_provider():
    def _provider(ticker, date):
        prices = {
            ("AAPL", "2023-01-01"): 150.0,
            ("GOOG", "2023-01-01"): 2800.0,
        }
        return prices.get((ticker, date))
    return _provider

@pytest.fixture
def empty_price_provider():
    def _provider(ticker, date):
        return None
    return _provider

@pytest.fixture
def valuator(price_provider):
    tm = TransactionManager()
    tm.buy("AAPL", 10, 100.0)
    tm.buy("GOOG", 5, 2000.0)
    return PortfolioValuator(tm, price_provider)

@pytest.fixture
def empty_valuator(price_provider):
    tm = TransactionManager()
    return PortfolioValuator(tm, price_provider)

def test_compute_daily_value_correct(valuator):
    value = valuator.compute_daily_value("2023-01-01")
    assert value == (10 * 150.0 + 5 * 2800.0)

def test_compute_daily_value_empty_portfolio(empty_valuator):
    value = empty_valuator.compute_daily_value("2023-01-01")
    assert value == pytest.approx(0.0)

def test_compute_daily_value_missing_price():
    tm = TransactionManager()
    tm.buy("AAPL", 10, 100.0)
    val = PortfolioValuator(tm, lambda t, d: None)
    with pytest.raises(ValueError, match="Some tickers do not have prices for the given date."):
        val.compute_daily_value("2023-01-01")
