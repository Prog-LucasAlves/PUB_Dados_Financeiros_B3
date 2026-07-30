import os
import re
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from .data import load_stock_prices


def normalize_price_value(value):
    if value is None:
        return None
    try:
        text = str(value).replace("R$", "").replace(" ", "").replace(",", ".")
        return float(text)
    except Exception:
        return None


def get_stock_data_val(df, ticker, column_name):
    if df is None or column_name not in df.columns:
        return None

    try:
        row = df[df["papel"] == ticker]
        if row.empty:
            return None

        if "Unnamed: 0" in row.columns:
            idx = int(row["Unnamed: 0"].iloc[0])
            return row[column_name].loc[idx] if column_name in row else None

        return row[column_name].iloc[0]
    except Exception:
        try:
            return row[column_name].iloc[0]
        except Exception:
            return None


def format_thousands(value):
    if value is None:
        return "N/A"
    try:
        text = str(value)
        return re.sub(r"(?<!^)(?=(\d{3})+$)", r".", text)
    except Exception:
        return str(value)


def try_load_stock_prices(precos_path, ticker):
    if os.path.exists(precos_path) and os.path.getsize(precos_path) > 200:
        precos_df = load_stock_prices(precos_path)
        if precos_df is not None and not precos_df.empty and len(precos_df) > 5:
            if "Close" in precos_df.columns:
                precos_df_ad = precos_df.rename(columns={"Close": ticker})
            elif "Adj Close" in precos_df.columns:
                precos_df_ad = precos_df.rename(columns={"Adj Close": ticker})
            else:
                numeric_cols = [c for c in precos_df.columns if c != "Date"]
                if numeric_cols:
                    precos_df_ad = precos_df.rename(columns={numeric_cols[0]: ticker})
                else:
                    precos_df_ad = precos_df.copy()
            return precos_df_ad.copy(), True, False
    return None, False, False


def simulate_stock_price_history(base_price, ticker, days=90, seed=42):
    np.random.seed(seed)
    dates_sim = [
        (datetime.today() - timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(days, -1, -1)
    ]

    prices_sim = [base_price]
    for _ in range(days):
        change = np.random.normal(0.0002, 0.015)
        prices_sim.append(prices_sim[-1] * (1 + change))

    return pd.DataFrame({"Date": dates_sim, ticker: prices_sim})


def load_price_history(precos_path, ticker, last_close=None):
    precos_df_clean, prices_loaded, is_contingency = try_load_stock_prices(
        precos_path, ticker
    )
    if prices_loaded:
        return precos_df_clean, True, False

    base_price = normalize_price_value(last_close) or 10.0
    return simulate_stock_price_history(base_price, ticker), True, True


def prepare_price_metrics(precos_df_clean, ticker):
    if precos_df_clean is None or precos_df_clean.empty:
        return precos_df_clean

    df = precos_df_clean.copy()
    df["ret"] = round((df[ticker].pct_change()) * 100, 2)
    df["tret"] = df["ret"].cumsum()
    df["Returns"] = df[ticker].pct_change(1)
    df["Target"] = df["Returns"].shift(-1)
    df["Vol"] = np.round(df["Returns"].rolling(20).std() * np.sqrt(252), 4)
    df["MM20"] = df[ticker].rolling(20).mean()
    df["Detrend"] = df[ticker] - df["MM20"]
    return df


def load_accumulated_return(file_path, ticker):
    if not os.path.exists(file_path):
        return None

    try:
        ret_df = pd.read_csv(file_path, sep=";")
        ret_filtered = ret_df[ret_df["Papel"] == ticker]
        if not ret_filtered.empty:
            idx = (
                int(ret_filtered["Unnamed: 0"].iloc[0])
                if "Unnamed: 0" in ret_filtered.columns
                else ret_filtered.index[0]
            )
            return ret_filtered["Total_Acumulado"].loc[idx]
    except Exception:
        pass
    return None


def estimate_accumulated_return(precos_df, ticker, days):
    if precos_df is None or precos_df.empty or ticker not in precos_df.columns:
        return None

    try:
        prices_series = precos_df[ticker].astype(float)
        pct_changes = prices_series.pct_change() * 100
        return pct_changes.tail(days).sum()
    except Exception:
        return None


def check_stock_data_integrity(ticker):
    paths = {
        "Preços Históricos": ("./Api/precos/{ticker}.csv", True),
        "Histórico Mensal": ("./Api/historico/{ticker}.csv", False),
        "Proventos & Dividendos": ("./Api/proventos/{ticker}.csv", False),
        "Releases Trimestrais": ("./Api/trimestre/{ticker}.csv", False),
        "Fatos Relevantes": ("./Api/fatos_relevantes/{ticker}.csv", False),
    }

    integrity = {}
    for name, (path_template, is_critical) in paths.items():
        path = path_template.format(ticker=ticker)
        exists = os.path.exists(path) and os.path.getsize(path) > 0
        integrity[name] = (exists, is_critical)
    return integrity
