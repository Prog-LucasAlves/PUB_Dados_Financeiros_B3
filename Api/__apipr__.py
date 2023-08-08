"""
Descrição:
Esse código pega os dados dos proventos das empresas listadas
na bolsa brasileira e armazena cada ação com os
dados coletados em um arquivo .csv

Local: pasta(proventos)
"""

import glob

# Bibliotecas utilizadas
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm

# Lista com o nome das ações
import __list__

acao = __list__.lst_acao

for i in tqdm(acao):
    url = f"https://fundamentus.com.br/proventos.php?papel={i}%20&tipo=2"
    hearder = {"user-agent": "Mozilla/5.0"}
    ret1 = requests.get(url, headers=hearder)
    soup1 = bs(ret1.text, "html.parser")

    d = soup1.h1.string

    # Coletando os nomes das colunas
    if d == "Proventos:":
        column_headers = soup1.findAll("tr")[0]
        column_headers = [i.getText() for i in column_headers.findAll("th")]

        # Coletando os dados das colunas
        rows = soup1.findAll("tr")[1:]
        df_dados = []
        for h in range(len(rows)):
            df_dados.append([col.getText() for col in rows[h].findAll("td")])

        # Adicionando os dados coletados em um DataFrame
        data = pd.DataFrame(df_dados, columns=column_headers[:])
        data["Acao"] = i

        # Salavando os dados em um arquivo .csv
        data.to_csv(f"./proventos/{i}.csv", sep=";")

arquivos = glob.glob("./proventos/*.csv")
# 'arquivos' agora é um array com o nome de todos os .csv
# que começam com 'arquivo'
array_df = []

for x in arquivos:
    temp_df = pd.read_csv(x, sep=";")
    array_df.append(temp_df)

df = pd.concat(array_df, axis=0)
# df.to_csv('../Todos/PR.csv', sep=';')
df.to_parquet("../Todos/PR.parquet.gzip", compression="gzip")

#####
