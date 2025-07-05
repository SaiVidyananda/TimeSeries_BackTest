# tests/test_transaction_manager.py

import os
from datetime import datetime

import pandas as pd
import pytest

from src.engine.transaction_manager import TransactionManager


@pytest.fixture
def tm():
    return TransactionManager()

def test_buy_new_stock(tm):
    tm.buy("AAPL", 10, 150.0, "2023-01-01")
    assert "AAPL" in tm.portfolio
    assert tm.portfolio["AAPL"]["quantity"] == 10
    assert tm.portfolio["AAPL"]["avg_price"] == pytest.approx(150.0)
    assert len(tm.transactions) == 1

def test_buy_existing_stock_updates_avg(tm):
    tm.buy("AAPL", 10, 150.0, "2023-01-01")
    tm.buy("AAPL", 10, 130.0, "2023-01-02")
    assert tm.portfolio["AAPL"]["quantity"] == 20
    assert round(tm.portfolio["AAPL"]["avg_price"], 2) == pytest.approx(140.0)
    assert len(tm.transactions) == 2

def test_sell_stock(tm):
    tm.buy("AAPL", 10, 150.0, "2023-01-01")
    tm.sell("AAPL", 5, 160.0, "2023-01-03")
    assert tm.portfolio["AAPL"]["quantity"] == 5
    assert len(tm.transactions) == 2

def test_sell_all_stock_removes_from_portfolio(tm):
    tm.buy("AAPL", 10, 150.0, "2023-01-01")
    tm.sell("AAPL", 10, 160.0, "2023-01-03")
    assert "AAPL" not in tm.portfolio
    assert len(tm.transactions) == 2

def test_sell_more_than_owned_raises(tm):
    tm.buy("AAPL", 5, 150.0, "2023-01-01")
    with pytest.raises(ValueError, match="Not enough shares to sell."):
        tm.sell("AAPL", 10, 160.0, "2023-01-03")

def test_get_portfolio_returns_dataframe(tm):
    tm.buy("AAPL", 10, 150.0)
    df = tm.get_portfolio()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_get_portfolio_returns_none_when_empty(tm):
    assert tm.get_portfolio().empty

def test_get_transactions(tm):
    tm.buy("AAPL", 10, 150.0)
    txns = tm.get_transactions()
    assert isinstance(txns, list)
    assert len(txns) == 1
    assert txns[0]["ticker"] == "AAPL"

def test_save_transactions_creates_file(tm, tmp_path):
    tm.buy("AAPL", 10, 150.0)
    file_path = tmp_path / "transactions.csv"
    tm.save_transactions(file_path)
    assert os.path.exists(file_path)
    df = pd.read_csv(file_path)
    assert not df.empty
    assert df.iloc[0]["ticker"] == "AAPL"
