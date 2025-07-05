# tests/test_portfolio_metrics.py

from datetime import datetime, timedelta

import pandas as pd
import pytest

from src.utils.metric_helper import (calculate_cagr, calculate_max_drawdown,
                                     calculate_sharpe, calculate_volatility,
                                     portfolio_summary_metrics)


@pytest.fixture
def steady_growth_df():
    dates = pd.date_range(start="2020-01-01", periods=4, freq="Y")
    values = [100000, 120000, 150000, 180000]
    return pd.DataFrame({"date": dates, "total_value": values})

@pytest.fixture
def drawdown_df():
    dates = pd.date_range(start="2020-01-01", periods=5)
    values = [100000, 120000, 90000, 95000, 110000]
    return pd.DataFrame({"date": dates, "total_value": values})

@pytest.fixture
def flat_df():
    dates = pd.date_range(start="2020-01-01", periods=3)
    values = [100000, 100000, 100000]
    return pd.DataFrame({"date": dates, "total_value": values})

def test_calculate_cagr_basic(steady_growth_df):
    result = calculate_cagr(steady_growth_df)
    assert isinstance(result, float)
    assert result > 0

def test_calculate_max_drawdown_basic(drawdown_df):
    result = calculate_max_drawdown(drawdown_df)
    assert isinstance(result, float)
    assert result < 0
    assert round(result, 2) == -0.25

def test_calculate_volatility(flat_df):
    result = calculate_volatility(flat_df)
    assert isinstance(result, float)
    assert result == 0.0

def test_calculate_sharpe_flat(flat_df):
    result = calculate_sharpe(flat_df)
    assert isinstance(result, float)
    assert result == float('inf') or result == 0.0 or pd.isna(result)

def test_portfolio_summary_metrics_keys(steady_growth_df):
    result = portfolio_summary_metrics(steady_growth_df)
    assert isinstance(result, dict)
    assert "CAGR" in result
    assert "Max Drawdown (%)" in result
    assert "Volatility (%)" in result
    assert "Sharpe Ratio" in result

def test_portfolio_summary_metrics_full(drawdown_df):
    result = portfolio_summary_metrics(drawdown_df)
    assert isinstance(result["CAGR"], float)
    assert isinstance(result["Max Drawdown (%)"], float)
    assert isinstance(result["Volatility (%)"], float)
    assert isinstance(result["Sharpe Ratio"], float)