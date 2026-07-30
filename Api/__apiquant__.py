"""
Descrição:
Esse código pega os dados upside ou downside mês a mês em porcentagem
das empresas listadas na bolsa brasileira e armazena cada ação com os
dados coletados em um arquivo .csv

Local: pasta(histórico)
"""

import os
import sys
from pathlib import Path
import warnings

import quantstats as qs
from tqdm import tqdm

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR.parent / "SRC"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

try:
    import __list__
except ImportError:
    if str(SRC_DIR) not in sys.path:
        sys.path.insert(0, str(SRC_DIR))
    import __list__


def collect_monthly_returns(target_dir="./historico"):
    warnings.filterwarnings("ignore")
    qs.extend_pandas()
    tickers = getattr(__list__, "lst_acao", [])
    os.makedirs(target_dir, exist_ok=True)

    for ticker in tqdm(tickers, desc="Baixando retornos mensais"):
        try:
            data = qs.utils.download_returns(f"{ticker}.SA")
            if data.empty:
                continue

            datah = data.monthly_returns()
            for month in [
                "JAN",
                "FEB",
                "MAR",
                "APR",
                "MAY",
                "JUN",
                "JUL",
                "AUG",
                "SEP",
                "OCT",
                "NOV",
                "DEC",
                "EOY",
            ]:
                if month in datah.columns:
                    datah[[month]] = datah[[month]].applymap("{0:.2%}".format)

            output_path = Path(target_dir) / f"{ticker}.csv"
            datah.to_csv(output_path, sep=";")
        except Exception:
            continue


if __name__ == "__main__":
    collect_monthly_returns()
