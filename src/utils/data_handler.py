"""
Data handling utility using yfinance with logging and error decorators.
"""

from datetime import datetime
from pathlib import Path

import pandas as pd
import yfinance as yf

from src.utils.decorator_utils import decorate_module_functions
from src.utils.log_helper import handle_exceptions, log_function_call

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def _get_cache_filename(ticker, start, end, interval):
    """Construct cache filename."""
    safe_ticker = "_".join(ticker) if isinstance(ticker, list) else ticker
    return DATA_DIR / f"{safe_ticker}_{start}_{end}_{interval}.csv"


def download_data(tickers, start="2015-01-01", end=None, interval="1d", cache=True):
    """
    Download stock data using yfinance.

    Args:
        tickers (str | list): Tickers to fetch.
        start (str): Start date.
        end (str): End date.
        interval (str): Interval (e.g., '1d').
        cache (bool): Use cached file if available.

    Returns:
        pd.DataFrame: Price data.
    """
    if not end:
        end = datetime.today().strftime("%Y-%m-%d")

    cache_file = _get_cache_filename(tickers, start, end, interval)

    if cache and cache_file.exists():
        return pd.read_csv(cache_file, index_col="Date", parse_dates=True)

    data = yf.download(tickers, start=start, end=end, interval=interval, group_by="ticker", progress=False)

    if isinstance(tickers, str):
        data = data.reset_index().set_index("Date")
    else:
        data = data["Adj Close"].dropna(how="all")

    if cache and not data.empty:
        data.to_csv(cache_file)

    return data


def fill_missing(data, method="ffill"):
    """
    Fill missing values in DataFrame.

    Args:
        data (pd.DataFrame): Input data.
        method (str): Fill method ('ffill', 'bfill').

    Returns:
        pd.DataFrame: Cleaned data.
    """
    return data.fillna(method=method)

decorate_module_functions(module=__import__(__name__), decorators=[handle_exceptions, log_function_call])
