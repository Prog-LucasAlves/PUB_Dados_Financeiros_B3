"""
Descrição:
Esse código pega os dados das cotações das empresas
listadas na bolsa brasileira e armazena cada ação com os
dados coletados em um arquivo .csv.
Coleta também os dados das cotações de índices, criptoativos e moedas.
Local: pasta(precos)
"""

import logging
import os
import sys
import warnings
from datetime import date, timedelta
from pathlib import Path

import backoff
import numpy as np
import pandas as pd
import yfinance as yf
from tqdm import tqdm


try:
    import __list__
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "SRC"))
    import __list__

warnings.filterwarnings("ignore")

logging.basicConfig(
    filename="./log/espc.log",
    level=logging.DEBUG,
    format="%(asctime)s :: %(levelname)s :: %(filename)s :: %(lineno)d",
)

BASE_DIR = Path(__file__).parent
START_DATE = date.today() - timedelta(days=500)
END_DATE = date.today()
ACAO = __list__.lst_acao
INDICES = __list__.lst_indices
CRYPTO = __list__.lst_crypto
MOEDAS = __list__.lst_moedas


def _ensure_directory(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def _normalize_dataframe(df: pd.DataFrame, ticker: str):
    if isinstance(df.columns, pd.MultiIndex):
        for label in [f"{ticker}.SA", ticker]:
            try:
                df = df.xs(label, level="Ticker", axis=1, drop_level=True)
                break
            except Exception:
                try:
                    df = df.xs(label, axis=1, level=0, drop_level=True)
                    break
                except Exception:
                    continue
    return df


@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def fetch_yf_data(symbol, start, end):
    return yf.download(
        symbol,
        start=start,
        end=end,
        progress=False,
        threads=False,
    )


def collect_equity_prices():
    """Coleta dados históricos de preços para cada ação da lista."""
    preco_dir = BASE_DIR / "precos"
    _ensure_directory(preco_dir)

    for ticker in tqdm(ACAO, desc="Coletando cotações de ações"):
        try:
            df = fetch_yf_data(f"{ticker}.SA", START_DATE, END_DATE)

            if df.empty:
                logging.warning(f"Nenhum dado retornado para {ticker}")
                continue

            df = _normalize_dataframe(df, ticker)
            df["ret"] = round((df["Close"].pct_change()) * 100, 2)
            df["tret"] = df["ret"].cumsum()
            df["Returns"] = df["Close"].pct_change(1)
            df["Target"] = df["Returns"].shift(-1)
            df["Vol"] = np.round(df["Returns"].rolling(20).std() * np.sqrt(252), 4)
            df["MM20"] = df["Close"].rolling(20).mean()
            df["Detrend"] = df["Close"] - df["MM20"]
            df.to_csv(preco_dir / f"{ticker}.csv", sep=";")
            logging.info(f"Preços das ações salvos com SUCESSO: {ticker}")
        except Exception as exc:
            logging.error(f"Erro ao salvar os preços das ações {ticker}: {exc}")


def collect_index_prices():
    index_dir = BASE_DIR / "indices"
    _ensure_directory(index_dir)

    for symbol in tqdm(INDICES, desc="Coletando cotações de índices"):
        try:
            df = yf.download(
                f"^{symbol}",
                start=START_DATE,
                end=END_DATE,
                progress=False,
                threads=False,
            )
            if not df.empty:
                df = _normalize_dataframe(df, f"^{symbol}")
                df.to_csv(index_dir / f"{symbol}.csv", sep=";")
        except Exception as exc:
            logging.error(f"Erro ao salvar índice {symbol}: {exc}")


def collect_crypto_prices():
    crypto_dir = BASE_DIR / "crypto"
    _ensure_directory(crypto_dir)

    for symbol in tqdm(CRYPTO, desc="Coletando cotações de cripto"):
        try:
            df = yf.download(
                f"{symbol}",
                start=START_DATE,
                end=END_DATE,
                progress=False,
                threads=False,
            )
            if not df.empty:
                df = _normalize_dataframe(df, symbol)
                df.to_csv(crypto_dir / f"{symbol}.csv", sep=";")
        except Exception as exc:
            logging.error(f"Erro ao salvar cripto {symbol}: {exc}")


def collect_currency_prices():
    moedas_dir = BASE_DIR / "moedas"
    _ensure_directory(moedas_dir)

    for symbol in tqdm(MOEDAS, desc="Coletando cotações de moedas"):
        try:
            df = yf.download(
                f"{symbol}",
                start=START_DATE,
                end=END_DATE,
                progress=False,
                threads=False,
            )
            if not df.empty:
                df = _normalize_dataframe(df, symbol)
                df.to_csv(moedas_dir / f"{symbol}.csv", sep=";")
        except Exception as exc:
            logging.error(f"Erro ao salvar moeda {symbol}: {exc}")


def main():
    collect_equity_prices()
    collect_index_prices()
    collect_crypto_prices()
    collect_currency_prices()


if __name__ == "__main__":
    main()
