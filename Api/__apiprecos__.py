"""
Descrição:
Esse código pega os dados das cotações das empresas
listadas na bolsa brasileira e armazena cada ação com os
dados coletados em um arquivo .csv \
Coleta também os dados da cotações do índice bovespa e
armazena os dados coletados em um arquivo .csv \
Local: pasta(precos)
"""

import logging
from datetime import date
from datetime import timedelta

import pandas as pd
import numpy as np

# Bibliotecas utilizadas
import yfinance as yf
from tqdm import tqdm

import warnings

# Lista com o nome das ações
import __list__

# Ignorando os avisos de erro
warnings.filterwarnings("ignore")

logging.basicConfig(
    filename="./log/espc.log",
    level=logging.DEBUG,
    format="%(asctime)s :: %(levelname)s :: %(filename)s :: %(lineno)d",
)

# Criando DataFrame
df = pd.DataFrame()

# Criando datas de inicio e fim
inicio = date.today() - timedelta(days=500)
fim = date.today()

# Tickers
acao = __list__.lst_acao
indices = __list__.lst_indices
crypto = __list__.lst_crypto
moedas = __list__.lst_moedas

# Coletando as cotações das ações
for i in tqdm(acao):
    try:
        df = yf.download(
            f"{i}.SA",
            start=inicio,
            end=fim,
            progress=False,
            threads=False,
        )
        df = df.xs(f"{i}.SA", level="Ticker", axis=1, drop_level=True)
        df["ret"] = round((df["Close"].pct_change()) * 100, 2)
        df["tret"] = df["ret"].cumsum()
        # df["Adj Low"] = df["Low"] - (df["Close"] - df["Adj Close"])
        # df["Adj High"] = df["High"] - (df["Close"] - df["Adj Close"])
        # df["Adj Open"] = df["Open"] - (df["Close"] - df["Adj Close"])
        df["Returns"] = df["Close"].pct_change(1)
        df["Target"] = df["Returns"].shift(-1)
        vol_p1 = 20
        df["Vol"] = np.round(df["Returns"].rolling(vol_p1).std() * np.sqrt(252), 4)
        df["MM20"] = df["Close"].rolling(20).mean()
        df["Detrend"] = df["Close"] - df["MM20"]
        df.to_csv(f"./precos/{i}.csv", sep=";")
        logging.info("Preços das ações salvos com SUCESSO")

    except Exception as e:
        logging.error(f"Erro ao salvar os preços das ações: {e}")

# Coletando as cotações de alguns índices
for i in tqdm(indices):
    df_b = yf.download(
        f"^{i}",
        start=inicio,
        end=fim,
        progress=False,
        threads=False,
    )
    df_b = df_b.xs(f"^{i}", level="Ticker", axis=1, drop_level=True)
    df_b.to_csv(f"./indices/{i}.csv", sep=";")


# Coletando as cotações de algumas crypto
for i in tqdm(crypto):
    df_crypto = yf.download(
        f"{i}", start=inicio, end=fim, progress=False, threads=False
    )
    df_crypto = df_crypto.xs(f"{i}", level="Ticker", axis=1, drop_level=True)
    df_crypto.to_csv(f"./crypto/{i}.csv", sep=";")

# Coletando as cotações de algumas moedas
for i in tqdm(moedas):
    df_moedas = yf.download(
        f"{i}", start=inicio, end=fim, progress=False, threads=False
    )
    df_moedas = df_moedas.xs(f"{i}", level="Ticker", axis=1, drop_level=True)
    df_moedas.to_csv(f"./moedas/{i}.csv", sep=";")


# Função para calcular o retorno(Índices)
def calcula_retono_indices():
    for i in indices:
        df = pd.read_csv(f"./indices/{i}.csv", sep=";")
        df["Retornos"] = round(df["Close"].pct_change() * 100, 2)
        df.to_csv(f"./indices/{i}.csv", sep=";")


# Função para calcular o retorno(Crypto)
def calcula_retorno_crypto():
    for i in crypto:
        df = pd.read_csv(f"./crypto/{i}.csv", sep=";")
        df["Retornos"] = round(df["Close"].pct_change() * 100, 2)
        df.to_csv(f"./crypto/{i}.csv", sep=";")


# Função para calcular o retorno(Moedas)
def calcula_retorno_moedas():
    for i in moedas:
        df = pd.read_csv(f"./moedas/{i}.csv", sep=";")
        df["Retornos"] = round(df["Close"].pct_change() * 100, 2)
        df.to_csv(f"./moedas/{i}.csv", sep=";")


if __name__ == "__main__":
    calcula_retono_indices()
    calcula_retorno_crypto()
    calcula_retorno_moedas()
