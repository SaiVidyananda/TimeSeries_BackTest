""" This module contains the Executor class that runs a trading strategy backtest.
It manages the execution of buy and sell signals, updates the portfolio, and logs daily performance.
"""
# src/engine/strategy_executor.py

import pandas as pd

from src.utils.log_helper import handle_exceptions, log_function_call, logger


class Executor:
    def __init__(self, strategy_func, transaction_manager, portfolio_valuator,
                 position_sizer, initial_cash=1000000):
        self.strategy_func = strategy_func
        self.tm = transaction_manager
        self.valuator = portfolio_valuator
        self.position_sizer = position_sizer
        self.cash = initial_cash
        self.initial_cash = initial_cash
        self.snapshot_value = initial_cash  # Initial cash value for the portfolio
        self.daily_log = []  # stores P&L, cash, value

    def _sell_executor(self, sell_signals, date):
        # SELL
        for signal in sell_signals:
            ticker = signal["ticker"]
            price = signal["price"]

            if "quantity" in signal and signal["quantity"] is not None:
                quantity = signal["quantity"]
            else:
                quantity = self.position_sizer.calculate_quantity_to_sell(ticker)

            if quantity <= 0:
                logger.info("Skipping sell: %s (nothing to sell)", ticker)
                continue

            try:
                self.tm.sell(ticker, quantity, price, date)
                self.cash += quantity * price
            except Exception as e:
                logger.warning("Sell failed: %s", e)

    def _buy_executor(self, buy_signals, date, snapshot_value):
        """Executes buy orders based on the provided signals."""
        for signal in buy_signals:
            ticker = signal["ticker"]
            price = signal["price"]

            if "quantity" in signal and signal["quantity"] is not None:
                quantity = signal["quantity"]
            else:
                quantity = self.position_sizer.fixed_amount_sizing(ticker, price, snapshot_value/(20*10), self.cash)
            if quantity is None or quantity <= 0:
                quantity = 1
            if price * quantity > self.cash:
                logger.info("Skipping buy: %s (insufficient cash)", ticker)
                continue

            try:
                self.tm.buy(ticker, quantity, price, date)
                self.cash -= quantity * price
            except Exception as e:
                logger.warning("Buy failed: %s", e)
    
    @log_function_call
    @handle_exceptions
    def run_backtest(self, date_range: list[str]):
        """Runs the backtest for the given date range using the strategy function.

        Args:
            date_range (list[str]): List of dates in 'YYYY-MM-DD' format for the backtest.

        Returns:
            pd.DataFrame: DataFrame containing daily logs with cash, holdings value, and total value.
        """
        for date in date_range:
            logger.info("Running strategy for %s", date)
            # 1. Get signals
            buy_signals, sell_signals = self.strategy_func(date)
            # 2. Execute sell orders first
            self._sell_executor(sell_signals, date)
            # 3. Then execute buy orders
            self._buy_executor(buy_signals, date, self.snapshot_value)
            # 4. Compute end-of-day portfolio value
            portfolio_value = self.valuator.compute_daily_value(date)
            self.snapshot_value = portfolio_value + self.cash
            # 5. Save log
            self.daily_log.append({
                "date": date,
                "cash": self.cash,
                "companies": len(self.tm.get_portfolio()),
                "holdings_value": portfolio_value,
                "total_value": self.snapshot_value
            })

        return pd.DataFrame(self.daily_log)
