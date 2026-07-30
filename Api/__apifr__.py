"""
Descrição:
Esse código pega os dados dos fatos relevantes das empresas listadas na bolsa brasileira e armazena cada ação com os dados coletados em um arquivo .csv

Local: pasta(fatos_relevantes)
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
OUTPUT_DIR = BASE_DIR / "fatos_relevantes"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def collect_relevant_facts():
    all_rows = []

    for ticker in tqdm(__list__.lst_acao, desc="Coletando fatos relevantes"):
        url = f"https://www.fundamentus.com.br/fatos_relevantes.php?papel={ticker}"
        headers = {"user-agent": "Mozilla/5.0"}

        response = requests.get(url, headers=headers)
        soup = bs(response.text, "html.parser")
        header_site = soup.h1

        if not header_site:
            continue

        column_headers = [th.getText() for th in soup.find_all("tr")[0].find_all("th")]
        rows = soup.find_all("tr")[1:]
        data_rows = [[td.getText() for td in row.find_all("td")] for row in rows]

        lista_link = [
            link.get("href")
            for row in rows
            for link in row.find_all("a")
            if link.get("href")
        ]

        if not data_rows:
            continue

        data = pd.DataFrame(data_rows, columns=column_headers)
        data["Link"] = lista_link
        if "Download" in data.columns:
            data.drop(columns=["Download"], inplace=True)
        if "Tipo" in data.columns:
            data.drop(columns=["Tipo"], inplace=True)

        if "Data" in data.columns:
            data["Hora"] = data["Data"].apply(lambda x: str(x)[10:]).str.strip()
            data["Data"] = data["Data"].apply(lambda x: str(x)[:12]).str.strip()
        data["Acao"] = ticker
        data = data[["Acao", "Data", "Hora", "Descrição", "Link"]]

        data.to_csv(OUTPUT_DIR / f"{ticker}.csv", sep=";", index=False)
        all_rows.append(data)

    if all_rows:
        df = pd.concat(all_rows, axis=0)
        df.to_parquet(Path("../Todos/FT.parquet.gzip"), compression="gzip")


if __name__ == "__main__":
    collect_relevant_facts()
