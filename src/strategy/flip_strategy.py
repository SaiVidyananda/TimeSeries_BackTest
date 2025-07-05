"""# src/strategy/flip_strategy.py

This module implements a trading strategy that buys stocks when their price is below 96% of the 50-day SMA
and sells them based on specific conditions related to price movements and holding periods.
"""
import pandas as pd

from src.utils.log_helper import handle_exceptions, log_function_call, logger


class FlipStrategy:
    """
    A trading strategy that buys stocks when their price is below 96% of the 50-day SMA
    and sells them based on specific conditions related to price movements and holding periods.
    """
    def __init__(self, price_df: pd.DataFrame):
        self.price_df = price_df.sort_values(["ticker", "date"])

    
    @log_function_call
    @handle_exceptions
    def get_signals(self, tm, date: str):
        buy_signals = []
        sell_signals = []
        

        date_data = self.price_df[self.price_df["date"] == date]
        logger.info(f"Processing date: {date}")
        logger.debug(f"Date data: {date_data}")
        for _, row in date_data.iterrows():
            ticker = row["ticker"]
            price = row["close"]
            sma_50 = row["sma_50"]

            # --- BUY ---
            #if ticker not in self.holdings:
            if price < sma_50 * 0.96:
                buy_signals.append({"ticker": ticker, "price": price})
            elif price > sma_50 * 1.12:
                sell_signals.append({"ticker": ticker, "price": price})
            else:
                if self.sl_check(tm, ticker, price):
                    sell_signals.append({"ticker": ticker, "price": price})

        return buy_signals, sell_signals
    
    def sl_check(self, tm, ticker: str, price: float) -> bool:
        """Check if the stop-loss condition is met for a given ticker."""
        holding = tm.get_portfolio_dict().get(ticker, None)
        if holding is None:
            logger.debug(f"No holding found for {ticker}. Skipping stop-loss check.")
            return False
        days_held = holding.get("days_held",0)+1
        max_price = max(holding.get("max_price",0), price)
        stop_loss_price = max_price * 0.97
        tm.update_portfolio(ticker, days_held, max_price)
        return (days_held > 60 and price < stop_loss_price) or days_held >= 150
