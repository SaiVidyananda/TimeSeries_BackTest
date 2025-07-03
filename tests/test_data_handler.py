# tests/test_data_handler.py

from unittest.mock import patch

import pandas as pd
import pytest

from src.utils.data_handler import download_data, fill_missing


@patch("src.utils.data_handler.yf.download")
def test_download_data_single_ticker(mock_download, tmp_path):
    # Setup mock
    df = pd.DataFrame({
        "Date": pd.date_range("2020-01-01", periods=3),
        "Adj Close": [100, 101, 102]
    }).set_index("Date")

    mock_download.return_value = df

    result = download_data("AAPL", start="2020-01-01", end="2020-01-04", cache=False)
    assert isinstance(result, pd.DataFrame)
    assert "Adj Close" in result.columns

@patch("src.utils.data_handler.yf.download")
def test_download_data_multiple_tickers(mock_download):
    df = pd.concat([
        pd.Series([100, 101, 102], name="AAPL"),
        pd.Series([200, 201, 202], name="MSFT")
    ], axis=1)
    df.index = pd.date_range("2020-01-01", periods=3)
    df.columns.name = "Ticker"

    # Multi-index structure like yfinance returns
    mock_download.return_value = pd.concat({
        "Adj Close": df
    }, axis=1)

    result = download_data(["AAPL", "MSFT"], start="2020-01-01", end="2020-01-04", cache=False)
    assert isinstance(result, pd.DataFrame)
    assert "AAPL" in result.columns
    assert "MSFT" in result.columns


