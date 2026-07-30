# Manipulação de dados
import os
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf
from tqdm import tqdm

try:
    import __list__
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "SRC"))
    import __list__

# Warnings
import warnings

warnings.filterwarnings("ignore")

ACAO = __list__.lst_acao
DATE2 = date.today() - timedelta(days=1)
BASE_DIR = Path(__file__).parent.resolve()
COTACOES_PATH = BASE_DIR / "retornos" / "cotacoes.csv"


def retorno_acumulado() -> bool:
    res = np.busday_count(
        (date.today() - timedelta(days=2)).strftime("%Y-%m-%d"),
        DATE2.strftime("%Y-%m-%d"),
    )
    i = 1
    test_date1 = date.today() - timedelta(days=2)
    while res < 80:
        test_date1 = date.today() - timedelta(days=i)
        res = np.busday_count(
            test_date1.strftime("%Y-%m-%d"), DATE2.strftime("%Y-%m-%d")
        )
        i += 1

    df = pd.DataFrame()
    success_count = 0

    print(f"Iniciando download de {len(ACAO)} ativos de {test_date1} até {DATE2}...")
    for ticker in tqdm(ACAO):
        try:
            downloaded = yf.download(
                f"{ticker}.SA",
                start=test_date1,
                end=DATE2,
                progress=False,
                threads=False,
            )
            if not downloaded.empty and "Close" in downloaded.columns:
                close_data = downloaded["Close"]
                if isinstance(close_data, pd.DataFrame):
                    close_data = close_data.squeeze()
                if not close_data.empty:
                    df[ticker] = close_data
                    success_count += 1
        except Exception:
            continue

    print(f"Download concluído. Sucesso: {success_count}/{len(ACAO)} ativos.")

    if df.empty:
        print(
            "[ALERTA] Nenhum dado foi baixado! O arquivo 'cotacoes.csv' não será sobrescrito com dados vazios."
        )
        return False

    COTACOES_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(COTACOES_PATH, sep=";", index_label=False)
    return True


def retorno_acumulado_dias(days: int) -> None:
    try:
        df = pd.read_csv(COTACOES_PATH, sep=";")
    except FileNotFoundError:
        print(f"[ERRO] arquivo '{COTACOES_PATH}' não encontrado.")
        return
    except pd.errors.EmptyDataError:
        print(f"[ERRO] arquivo '{COTACOES_PATH}' está vazio.")
        return

    if df.empty or df.shape[0] < 2:
        print(
            f"[AVISO] Dados insuficientes em {COTACOES_PATH.name} ({df.shape[0]} linhas) para calcular retorno de {days} dias."
        )
        return

    df = df.tail(days)
    df = round(df.pct_change() * 100, 2)
    df.reset_index(inplace=True)
    df.rename(columns={"index": "Date"}, inplace=True)

    if 0 in df.index:
        df = df.drop(0)
    else:
        df = df.iloc[1:]

    if df.empty:
        print("[AVISO] Sem dias úteis suficientes após cálculo de variação percentual.")
        return

    if "Date" not in df.columns:
        print("[ERRO] Coluna 'Date' ausente após reset_index.")
        return

    lista_date = pd.to_datetime(df["Date"]).dt.date.tolist()
    df.drop(["Date"], axis=1, inplace=True)
    df = df.T
    df["Total_Acumulado"] = round(df.sum(axis=1), 2)

    for idx, data_label in enumerate(lista_date):
        if idx < len(df.columns):
            df.rename(columns={df.columns[idx]: str(data_label)}, inplace=True)

    df = df.sort_values(by="Total_Acumulado", ascending=False)
    df_filter = df[["Total_Acumulado"]].reset_index()
    df_filter.rename(columns={"index": "Papel"}, inplace=True)

    out_path = BASE_DIR / "retornos" / f"retornos_acumulados_{(days - 1)}d.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df_filter.to_csv(out_path, sep=";")
    print(
        f"[OK] Retornos acumulados de {days - 1} dias salvos com sucesso em {out_path.name}."
    )


def main() -> None:
    if retorno_acumulado():
        for days in (16, 31, 46, 61):
            retorno_acumulado_dias(days)


if __name__ == "__main__":
    main()
