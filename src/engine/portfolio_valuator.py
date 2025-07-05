""" this module does the valuation of a portfolio by computing the daily value based on transactions and current prices.
It uses the TransactionManager to get the portfolio and a price provider to fetch current prices.
"""
# src/engine/portfolio_valuator.py

import pandas as pd

from src.utils.log_helper import handle_exceptions, log_function_call, logger


class PortfolioValuator:
    def __init__(self, transaction_manager, price_provider):
        self.transaction_manager = transaction_manager
        self.price_provider = price_provider

    @log_function_call
    @handle_exceptions
    def compute_daily_value(self, date: str) -> float:
        portfolio = self.transaction_manager.get_portfolio()
        print(f"Portfolio on {date}:\n{portfolio}")
        if portfolio is None or portfolio.empty:
            logger.warning("Portfolio is empty. Cannot compute value.")
            return 0.0
        
        portfolio['close_price'] = portfolio['ticker'].apply(lambda x: self.price_provider(x, date))
        
        if portfolio['close_price'].isnull().any():
            logger.warning("Some tickers do not have prices for %s. Skipping valuation.", date)
            raise ValueError("Some tickers do not have prices for the given date.")
        portfolio["value"] = portfolio["quantity"] * portfolio["close_price"]

        total_value = portfolio["value"].sum()
        logger.info("Total portfolio value on %s: ₹%.2f", date, total_value)
        return total_value
