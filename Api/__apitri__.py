"""
Descrição:
Esse código pega os dados dos releases trimestrais das
empresas listadas na bolsa brasileira e armazena cada ação com os
dados coletados em um arquivo .csv

Local: pasta(trimestre)
"""

import os
import sys
import warnings
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm

try:
    import __list__
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "SRC"))
    import __list__

warnings.filterwarnings("ignore")

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "trimestre"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_ARCHIVE = Path("../Todos")
OUTPUT_ARCHIVE.mkdir(parents=True, exist_ok=True)


def fetch_trimestral_data(ticker: str) -> pd.DataFrame | None:
    url = f"https://www.fundamentus.com.br/resultados_trimestrais.php?papel={ticker}&tipo=1"
    headers = {"user-agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = bs(response.text, "html.parser")

    if not soup.h1:
        return None

    table = soup.find_all("tr")
    if len(table) < 2:
        return None

    column_headers = [th.getText() for th in table[0].find_all("th")]
    rows = table[1:]
    data_rows = [[td.getText() for td in row.find_all("td")] for row in rows]

    if not data_rows:
        return None

    links = [
        link.get("href")
        for row in rows
        for link in row.find_all("a")
        if link.get("href")
    ]
    lista_df = [link for link in links if "NumeroSequencialDocumento" in link]
    lista_rr = [link for link in links if "Tela=ext&numProtocolo" in link]

    data = pd.DataFrame(data_rows, columns=column_headers)
    data["Demonstração Financeira"] = pd.Series(lista_df)
    data["Release de Resultados"] = pd.Series(lista_rr)
    data["Acao"] = ticker
    return data


def collect_trimestral_reports() -> None:
    frames = []

    for ticker in tqdm(__list__.lst_acao, desc="Coletando resultados trimestrais"):
        data = fetch_trimestral_data(ticker)
        if data is None:
            continue
        output_file = OUTPUT_DIR / f"{ticker}.csv"
        data.to_csv(output_file, sep=";", index=False)
        frames.append(data)

    if frames:
        df = pd.concat(frames, axis=0)
        df.to_parquet(OUTPUT_ARCHIVE / "TR.parquet.gzip", compression="gzip")


if __name__ == "__main__":
    collect_trimestral_reports()
