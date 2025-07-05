# tests/test_flip_strategy_v2.py

import pandas as pd
import pytest

from src.strategy.flip_strategy import FlipStrategy


class MockTM:
    def __init__(self):
         self.portfolio = {
            "AAPL": {"days_held": 61, "max_price": 100},
            "MSFT": {"days_held": 149, "max_price": 120}
        }

    def get_portfolio_dict(self):
        return self.portfolio

    def update_portfolio(self, ticker, days_held, max_price):
        self.portfolio[ticker]["days_held"] = days_held
        self.portfolio[ticker]["max_price"] = max_price


@pytest.fixture
def price_df():
    return pd.DataFrame([
        {"date": "2023-01-01", "ticker": "AAPL", "close": 95, "sma_50": 100},  # Buy
        {"date": "2023-01-01", "ticker": "GOOG", "close": 113, "sma_50": 100},  # Sell (>112%)
        {"date": "2023-01-01", "ticker": "MSFT", "close": 115, "sma_50": 100},  # SL check (150 days)
    ])


def test_buy_and_sell_signals(price_df):
    tm = MockTM()
    strat = FlipStrategy(price_df)
    strat.holdings = {}

    buys, sells = strat.get_signals(tm, "2023-01-01")

    buy_tickers = [b["ticker"] for b in buys]
    sell_tickers = [s["ticker"] for s in sells]

    assert "AAPL" in buy_tickers
    assert "GOOG" in sell_tickers
    assert "MSFT" in sell_tickers


def test_sl_check_true_conditions(price_df):
    tm = MockTM()
    strat = FlipStrategy(price_df)

    # AAPL: days_held = 61, max_price = 100, current price = 94 (below stop-loss price of 97)
    assert strat.sl_check(tm, "AAPL", 94) is True

    # MSFT: days_held = 149, next will be 150 (hit holding limit)
    assert strat.sl_check(tm, "MSFT", 130) is True

def test_sl_check_false_condition(price_df):
    tm = MockTM()
    strat = FlipStrategy(price_df)

    # AAPL: days_held = 61 -> becomes 62, price = 99, max_price = 100, sl = 97 → price above SL
    assert strat.sl_check(tm, "AAPL", 99) is False
