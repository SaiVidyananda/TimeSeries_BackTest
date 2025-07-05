""" Position Sizer Module
This module contains the PositionSizer class, which is responsible for determining how many shares to buy or sell based on the current portfolio and available cash.
"""
# src/engine/position_sizer.py

from typing import Optional

from src.utils.log_helper import handle_exceptions, log_function_call, logger

""" This module contains the PositionSizer class, which is responsible for determining how many shares to buy or sell based on the current portfolio and available cash."""
class PositionSizer:
    def __init__(self, transaction_manager, min_cash_reserve=0.0, max_positions=10):
        self.tm = transaction_manager
        self.min_cash_reserve = min_cash_reserve  # e.g., 0.1 for 10%
        self.max_positions = max_positions        # Max simultaneous holdings

    @log_function_call
    @handle_exceptions
    def calculate_quantity_to_buy(self, ticker: str, price: float, cash_available: float) -> int:
        """Decides how many shares to buy based on equal weight strategy."""
        effective_cash = cash_available * (1 - self.min_cash_reserve)
        if effective_cash <= 0:
            return 0

        current_portfolio = self.tm.get_portfolio()
        num_positions = len(current_portfolio)

        # Target weight per position
        slots = max(self.max_positions - num_positions, 1)
        alloc_per_position = effective_cash / slots
        quantity = int(alloc_per_position // price)
        return max(quantity, 0)

    @log_function_call
    @handle_exceptions
    def calculate_quantity_to_sell(self, ticker: str) -> int:
        """Returns all available quantity to sell."""
        portfolio_df = self.tm.get_portfolio()
        if portfolio_df is None or portfolio_df.empty:
            return 0
        row = portfolio_df[portfolio_df["ticker"] == ticker]
        return int(row["quantity"].iloc[0]) if not row.empty else 0
    
    @log_function_call
    @handle_exceptions
    def fixed_amount_sizing(self, ticker: str, price: float, fixed_amount:float, cash_available: float) -> int:
        """Decides how many shares to buy based on equal weight strategy."""
        effective_cash = cash_available * (1 - self.min_cash_reserve)
        if effective_cash <= 0:
            return 0
        current_portfolio = self.tm.get_portfolio()
        num_positions = current_portfolio.shape[0]
        logger.info(" slots filled, but ticker %d", num_positions)
        # Target weight per position
        slots = max(self.max_positions - num_positions, 0)
        logger.info(" slots filled, but ticker %d, %d", num_positions, slots)
        if slots == 0:
            if ticker in current_portfolio.ticker.values:
                logger.info("No slots available, but ticker %s is already owned. Using fixed amount sizing.", ticker)
                return int(fixed_amount // price)
            else:
                return 0

        quantity = int(fixed_amount // price)
        logger.info(" slots filled, but ticker %d atlast %d", num_positions, slots)
        return max(quantity, 0)
