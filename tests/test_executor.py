# tests/test_strategy_executor.py

import pandas as pd
import pytest

from src.engine.executor import Executor
from src.engine.portfolio_valuator import PortfolioValuator
from src.engine.transaction_manager import TransactionManager


@pytest.fixture
def fake_strategy():
    def _strategy(date):
        if date == "2023-01-01":
            return (
                [{"ticker": "AAPL", "price": 100.0}],  # buy
                []                                     # sell
            )
        elif date == "2023-01-02":
            return (
                [],
                [{"ticker": "AAPL", "price": 110.0}]
            )
        return ([], [])
    return _strategy

@pytest.fixture
def price_provider():
    def _provider(ticker, date):
        return 100.0 if date == "2023-01-01" else 110.0
    return _provider

@pytest.fixture
def mock_position_sizer():
    class MockSizer:
        def fixed_amount_sizing(self, ticker, price, risk_per_trade, cash):
            return 5

        def calculate_quantity_to_sell(self, ticker):
            return 5
    return MockSizer()

@pytest.fixture
def executor(fake_strategy, price_provider, mock_position_sizer):
    tm = TransactionManager()
    valuator = PortfolioValuator(tm, price_provider)
    return Executor(fake_strategy, tm, valuator, mock_position_sizer, initial_cash=1000)

def test_buy_and_sell_flow(executor):
    df = executor.run_backtest(["2023-01-01", "2023-01-02"])
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert df.iloc[0]["companies"] >= 1
    assert df.iloc[1]["cash"] > 1000 - 5 * 100.0  # should reflect cash after buy/sell

def test_run_backtest_returns_dataframe(executor):
    result = executor.run_backtest(["2023-01-01"])
    assert isinstance(result, pd.DataFrame)
    assert "date" in result.columns
    assert "cash" in result.columns
    assert "holdings_value" in result.columns
    assert "total_value" in result.columns
