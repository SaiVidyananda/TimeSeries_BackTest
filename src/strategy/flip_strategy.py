"""# src/strategy/flip_strategy.py

This module implements a trading strategy that buys stocks when their price is below 96% of the 50-day SMA
and sells them based on specific conditions related to price movements and holding periods.
"""
import pandas as pd


class FlipStrategy:
    """
    A trading strategy that buys stocks when their price is below 96% of the 50-day SMA
    and sells them based on specific conditions related to price movements and holding periods.
    """
    def __init__(self, price_df: pd.DataFrame):
        self.price_df = price_df.sort_values(["ticker", "date"])
        self.holdings = {}  # ticker -> dict with buy_date, buy_price, peak_price

    def get_signals(self, date: str):
        buy_signals = []
        sell_signals = []

        date_data = self.price_df[self.price_df["date"] == date]

        for _, row in date_data.iterrows():
            ticker = row["ticker"]
            price = row["close"]
            sma_50 = row["sma_50"]

            # --- BUY ---
            #if ticker not in self.holdings:
            if price < sma_50 * 0.96:
                buy_signals.append({"ticker": ticker, "price": price})
                self.holdings[ticker] = {
                    "buy_date": date,
                    "buy_price": price,
                    "peak_price": price,
                    "days_held": 0
                }

            # --- SELL ---
            elif ticker in self.holdings:
                holding = self.holdings[ticker]
                holding["days_held"] += 1
                holding["peak_price"] = max(holding["peak_price"], price)

                stop_loss_price = holding["peak_price"] * 0.97

                tlsl_hit = holding["days_held"] > 60 and price < stop_loss_price

                if price > sma_50 * 1.12 or tlsl_hit or holding["days_held"] >= 150:
                    sell_signals.append({"ticker": ticker, "price": price})
                    del self.holdings[ticker]

        return buy_signals, sell_signals
