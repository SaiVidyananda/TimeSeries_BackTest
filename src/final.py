"""# src/final.py

This script serves as the main entry point for the portfolio valuation system.
It initializes the data download, transaction management, and portfolio valuation processes.
"""
#from datetime import datetime

#import pandas as pd
#import yfinance as yf

from src.engine.portfolio_valuator import PortfolioValuator
from src.engine.transaction_manager import TransactionManager
from src.utils.data_handler import download_data

#from src.utils.decorator_utils import decorate_module_functions
#from src.utils.log_helper import handle_exceptions, log_function_call

tickers = [
    "ADANIENT.NS", "ADANIGREEN.NS", "ADANIPORTS.NS", "ADANIPOWER.NS", "AMBUJACEM.NS",
    "APOLLOHOSP.NS", "ASIANPAINT.NS", "AUROPHARMA.NS", "AXISBANK.NS", "BAJAJ-AUTO.NS",
    "BAJFINANCE.NS", "BAJAJFINSV.NS", "BAJAJHLDNG.NS", "BANDHANBNK.NS", "BANKBARODA.NS",
    "BEL.NS", "BERGEPAINT.NS", "BHARATFORG.NS", "BHARTIARTL.NS", "BIOCON.NS",
    "BOSCHLTD.NS", "BPCL.NS", "BRITANNIA.NS", "CGPOWER.NS", "CHOLAFIN.NS",
    "CIPLA.NS", "COALINDIA.NS", "COLPAL.NS", "CONCOR.NS", "DABUR.NS",
    "DALBHARAT.NS", "DEEPAKNTR.NS", "DIVISLAB.NS", "DMART.NS", "DLF.NS",
    "DRREDDY.NS", "EICHERMOT.NS", "GAIL.NS", "GLAND.NS",
    "GODREJCP.NS", "GRASIM.NS", "HAVELLS.NS", "HCLTECH.NS",
    "HDFCAMC.NS", "HDFCBANK.NS", "HDFCLIFE.NS", "HEROMOTOCO.NS", "HINDALCO.NS",
    "HINDPETRO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "ICICIGI.NS", "ICICIPRULI.NS",
    "IDEA.NS", "IDFCFIRSTB.NS", "IGL.NS", "INDIGO.NS", "INDUSINDBK.NS",
    "INDUSTOWER.NS", "INFY.NS", "IOC.NS", "ITC.NS", "JINDALSTEL.NS",
    "JSWSTEEL.NS", "KOTAKBANK.NS", "LALPATHLAB.NS", "LICI.NS", "LT.NS",
    "LTIM.NS", "LTTS.NS", "M&M.NS", "M&MFIN.NS",
    "MANAPPURAM.NS", "MARICO.NS", "MARUTI.NS", "MUTHOOTFIN.NS", "NAUKRI.NS",
    "NESTLEIND.NS", "NMDC.NS", "NTPC.NS", "OBEROIRLTY.NS", "ONGC.NS",
    "PAGEIND.NS", "PEL.NS", "PETRONET.NS", "PFC.NS", "PIDILITIND.NS",
    "PIIND.NS", "PNB.NS", "POWERGRID.NS", "RECLTD.NS", "RELIANCE.NS",
    "SBILIFE.NS", "SBIN.NS", "SHREECEM.NS", "SIEMENS.NS", "SRF.NS",
    "SUNPHARMA.NS", "TATACHEM.NS", "TATACONSUM.NS", "TATAMOTORS.NS", "TATAPOWER.NS",
    "TATASTEEL.NS", "TCS.NS", "TECHM.NS", "TITAN.NS", "TORNTPHARM.NS",
    "TRENT.NS", "TVSMOTOR.NS", "ULTRACEMCO.NS", "UPL.NS", "VEDL.NS",
    "VOLTAS.NS", "WIPRO.NS", "ZEEL.NS"
]

data = download_data(tickers, start="2015-01-01", end=None, interval="1d", cache=True)
print(f"Data shape: {data.shape}")
print(data.head())
print(data.loc["2025-07-01", "RELIANCE.NS"])
print(data.loc["2025-07-01", "SBIN.NS"])

price_provider = lambda ticker, date: data.loc[date, ticker] if date in data.index else None


transaction_manager = TransactionManager()

transaction_manager.buy("RELIANCE.NS", 10, 2000, "2023-01-01")
transaction_manager.buy("SBIN.NS", 10, 2000, "2023-01-01")

portfolio_valuator = PortfolioValuator(transaction_manager, price_provider)
#portfolio_valuator.compute_daily_value("2025-01-01")
print("Portfolio valuation completed.", portfolio_valuator.compute_daily_value("2025-07-01"))
