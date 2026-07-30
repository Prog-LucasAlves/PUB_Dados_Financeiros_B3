"""
Descrição:
Esse código pega os dados dos proventos das empresas listadas
na bolsa brasileira e armazena cada ação com os dados coletados
em um arquivo .csv

Local: pasta(proventos)
"""

import os
import sys
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

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "proventos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_ARCHIVE = Path("../Todos")
OUTPUT_ARCHIVE.mkdir(parents=True, exist_ok=True)


def fetch_proventos_data(ticker: str) -> pd.DataFrame | None:
    url = f"https://fundamentus.com.br/proventos.php?papel={ticker}%20&tipo=2"
    headers = {"user-agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = bs(response.text, "html.parser")

    title = soup.h1.string if soup.h1 else ""
    if title != "Proventos:":
        return None

    rows = soup.find_all("tr")[1:]
    data_rows = [[td.getText() for td in row.find_all("td")] for row in rows]

    if not data_rows:
        return None

    column_headers = [th.getText() for th in soup.find_all("tr")[0].find_all("th")]
    data = pd.DataFrame(data_rows, columns=column_headers)
    data["Acao"] = ticker
    return data


def collect_proventos() -> None:
    frames = []

    for ticker in tqdm(__list__.lst_acao, desc="Coletando proventos"):
        data = fetch_proventos_data(ticker)
        if data is None:
            continue
        output_file = OUTPUT_DIR / f"{ticker}.csv"
        data.to_csv(output_file, sep=";", index=False)
        frames.append(data)

    if frames:
        df = pd.concat(frames, axis=0)
        df.to_parquet(OUTPUT_ARCHIVE / "PR.parquet.gzip", compression="gzip")


if __name__ == "__main__":
    collect_proventos()
