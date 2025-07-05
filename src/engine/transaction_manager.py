"""This module manages transactions for a trading portfolio, including buying and selling stocks,
 and maintaining a record of transactions."""
# src/engine/transaction_manager.py

from datetime import datetime

import pandas as pd

from src.utils.log_helper import handle_exceptions, log_function_call, logger

"""Class to manage transactions in a trading portfolio, including buying and selling stocks,
 and maintaining a record of transactions."""
class TransactionManager:
    def __init__(self):
        self.portfolio = {}  # ticker: {ticker, quantity, avg_price}
        self.transactions = []
        self.trade_id = 0

    @log_function_call
    @handle_exceptions
    def buy(self, ticker: str, quantity: int, price: float, date: str = None):
        """        Buy shares of a stock and update the portfolio.

        Args:
            ticker (str): Stock ticker symbol.
            quantity (int): Number of shares to buy.
            price (float): Price per share.
            date (str, optional): Date of transaction in 'YYYY-MM-DD' format. Defaults to today.

        Raises:
            ValueError: If quantity is less than or equal to zero.
        """
        date = date or datetime.now().strftime("%Y-%m-%d")
        total_cost = quantity * price
        logger.info("Buying %s: %d shares at ₹%.2f", ticker, quantity, price)
        if ticker in self.portfolio:
            pos = self.portfolio[ticker]
            new_qty = pos["quantity"] + quantity
            new_avg = ((pos["quantity"] * pos["avg_price"]) + total_cost) / new_qty
            self.portfolio[ticker] = {"ticker":ticker, "quantity": new_qty, "avg_price": new_avg, 
                                      "date": pos["date"], "trade_id": pos["trade_id"]}
        else:
            self.trade_id += 1
            trade_id = f"{ticker}-{self.trade_id}"
            logger.info("New trade ID assigned: %s", trade_id)
            self.portfolio[ticker] = {"ticker":ticker, "quantity": quantity, "avg_price": price, 
                                      "date": date, "trade_id": trade_id}
        self._record_transaction("BUY", ticker, quantity, price, date, self.portfolio[ticker]["trade_id"])

    @log_function_call
    @handle_exceptions
    def sell(self, ticker: str, quantity: int, price: float, date: str = None):
        """Sell shares of a stock and update the portfolio.

        Args:
            ticker (str): Stock ticker symbol.
            quantity (int): Number of shares to sell.
            price (float): Price per share.
            date (str, optional): Date of transaction in 'YYYY-MM-DD' format. Defaults to today.

        Raises:
            ValueError: If not enough shares are available to sell.
        """
        date = date or datetime.now().strftime("%Y-%m-%d")
        trade_id = self.portfolio[ticker]["trade_id"]
        if ticker not in self.portfolio or self.portfolio[ticker]["quantity"] < quantity:
            raise ValueError("Not enough shares to sell.")
        self.portfolio[ticker]["quantity"] -= quantity
        if self.portfolio[ticker]["quantity"] == 0:
            del self.portfolio[ticker]
        logger.info("Sold %s: %d shares at ₹%.2f", ticker, quantity, price)
        self._record_transaction("SELL", ticker, quantity, price, date, trade_id)

    def _record_transaction(self, action, ticker, quantity, price, date, trade_id=None):
        txn = {"action": action, "ticker": ticker, "quantity": quantity, "price": price, "date": date, "trade_id": trade_id}
        self.transactions.append(txn)
        logger.info("Recorded transaction: %s", txn)

    def get_portfolio(self):
        """Get the current portfolio as a DataFrame."""
        return pd.DataFrame(self.portfolio.values())if self.portfolio else pd.DataFrame(columns=["ticker", "quantity", "avg_price", "date", "trade_id"])

    def get_transactions(self):
        """Get the list of recorded transactions."""
        return self.transactions
    
    def save_transactions(self, filename):
        """Save transactions to a file."""
        df = pd.DataFrame(self.transactions)
        df.to_csv(filename, index=False)
        logger.info("Transactions saved to %s", filename)

