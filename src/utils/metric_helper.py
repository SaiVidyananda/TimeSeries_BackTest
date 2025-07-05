import pandas as pd


def calculate_cagr(df):
    start_val = df["total_value"].iloc[0]
    end_val = df["total_value"].iloc[-1]
    days = (df["date"].iloc[-1] - df["date"].iloc[0]).days
    years = days / 365.25
    return ((end_val / start_val) ** (1 / years)) - 1

def calculate_max_drawdown(df):
    cumulative = df["total_value"]
    rolling_max = cumulative.cummax()
    drawdown = (cumulative - rolling_max) / rolling_max
    return drawdown.min()  # this will be a negative number

def calculate_volatility(df):
    df["daily_return"] = df["total_value"].pct_change()
    return df["daily_return"].std() * (252 ** 0.5)  # annualized

def calculate_sharpe(df):
    df["daily_return"] = df["total_value"].pct_change()
    avg_daily = df["daily_return"].mean()
    std_daily = df["daily_return"].std()
    sharpe = (avg_daily / std_daily) * (252 ** 0.5)
    return sharpe

def portfolio_summary_metrics(df):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], dayfirst=True)
    df = df.sort_values("date").reset_index(drop=True)

    cagr = calculate_cagr(df)
    max_dd = calculate_max_drawdown(df)
    vol = calculate_volatility(df)
    sharpe = calculate_sharpe(df)

    return {
        "CAGR": round(cagr * 100, 2),
        "Max Drawdown (%)": round(max_dd * 100, 2),
        "Volatility (%)": round(vol * 100, 2),
        "Sharpe Ratio": round(sharpe, 2)
    }
