"""# src/final.py

This script serves as the main entry point for the portfolio valuation system.
It initializes the data download, transaction management, and portfolio valuation processes.
"""
#from datetime import datetime

from pathlib import Path

import pandas as pd
import yfinance as yf

from src.engine.executor import Executor
from src.engine.portfolio_valuator import PortfolioValuator
from src.engine.position_sizer import PositionSizer
from src.engine.transaction_manager import TransactionManager
from src.strategy.flip_strategy import FlipStrategy
from src.utils.data_handler import download_data
from src.utils.metric_helper import portfolio_summary_metrics

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

data = download_data(tickers, start="2019-01-01", end=None, interval="1d", cache=True)
print(f"Data shape: {data.shape}")
print(data.head())
print(data.loc["2025-07-01", "RELIANCE.NS"])
print(data.loc["2025-07-01", "SBIN.NS"])

price_provider = lambda ticker, date: data.loc[date, ticker] if date in data.index else None
def prepare_price_data(tickers, start, end):
    """
    Downloads historical price data for multiple tickers
    and calculates 50-day SMA.
    
    Returns:
        DataFrame with ['ticker', 'date', 'close', 'sma_50']
    """
    all_data = []

    for ticker in tickers:
        series = data[ticker].loc[start:end]
        df = series.to_frame(name="close")
        df["ticker"] = ticker
        df["sma_50"] = df["close"].rolling(50).mean()
        df = df.reset_index().rename(columns={"Date": "date"})
        all_data.append(df)

    result_df = pd.concat(all_data, ignore_index=True)
    result_df.dropna(inplace=True)  # remove early rows without SMA
    return result_df

flip_stratey_data = prepare_price_data(tickers, start="2015-01-01", end="2025-07-01")
strategy = FlipStrategy(flip_stratey_data)
transaction_manager = TransactionManager()
portfolio_valuator = PortfolioValuator(transaction_manager, price_provider)
position_sizer = PositionSizer(transaction_manager, 0, 30)

exec =  Executor(strategy.get_signals, transaction_manager, portfolio_valuator,
                 position_sizer, 300000)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
#transaction_manager.save_transactions(DATA_DIR/"transactions.csv")
#print(data.index.strftime("%Y-%m-%d").to_list())
daily_value = exec.run_backtest(date_range=data[100:].index.strftime("%Y-%m-%d").tolist())
#portfolio_valuator.compute_daily_value("2025-01-01")
print("Portfolio valuation completed.")
print(daily_value)

#print(transaction_manager.get_transactions())
pd.DataFrame(transaction_manager.get_transactions()).to_csv(DATA_DIR/"transactions.csv", index=False)
pd.DataFrame(daily_value).to_csv(DATA_DIR/"daily_value.csv", index=False)

print(portfolio_summary_metrics(pd.DataFrame(daily_value)))
print(pd.DataFrame(daily_value).describe())
print("Plotting portfolio values...")
