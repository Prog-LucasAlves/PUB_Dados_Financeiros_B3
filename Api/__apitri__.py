"""
Descrição:
Esse código pega os dados dos releases trimestrais das
empresas listadas na bolsa brasileira e armazena cada ação com os
dados coletados em um arquivo .csv

Local: pasta(trimestre)
"""

# Bibliotecas utilizadas
import glob
import warnings
from datetime import datetime, timedelta

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm

# Lista com o nome das ações
import __list__

warnings.filterwarnings("ignore")

date_att = datetime.today()
atraso = timedelta(0)
date_atual = date_att - atraso
date_atual_m = date_atual.strftime("%d/%m/%Y")

# Lista com o nome das ações
acao = __list__.lst_acao

for i in tqdm(acao):
    url = f"https://www.fundamentus.com.br/resultados_trimestrais.php?papel={i}&tipo=1"
    hearder = {"user-agent": "Mozilla/5.0"}
    ret1 = requests.get(url, headers=hearder)
    soup1 = bs(ret1.text, "html.parser")

    header_site = soup1.h1
    if header_site:

        # Coletando os nomes das colunas
        column_headers = soup1.findAll("tr")[0]
        column_headers = [i.getText() for i in column_headers.findAll("th")]

        # Coletando os dados das colunas
        rows = soup1.findAll("tr")[1:]
        df_dados = []
        for h in range(len(rows)):
            df_dados.append([col.getText() for col in rows[h].findAll("td")])

            # Coletando o link do documento
            rows1 = soup1.findAll("tr")[1:]
            lista_link = []
            for t in range(len(rows1)):
                for link in rows1[t].find_all("a"):
                    lista_link.append(link.get("href"))

        lista_df = []
        for a in lista_link:
            if "NumeroSequencialDocumento" in a:
                lista_df.append(a)

        lista_rr = []
        for b in lista_link:
            if "Tela=ext&numProtocolo" in b:
                lista_rr.append(b)

    # Adicionando os dados coletados em um DataFrame
    data = pd.DataFrame(df_dados, columns=column_headers[:])
    data["Demonstração Financeira"] = lista_df
    data["Release de Resultados"] = pd.Series(lista_rr)
    data["Acao"] = i

    data.to_csv(f"../Api/trimestre/{i}.csv", sep=";")

    data_date = pd.read_csv(f"../Api/trimestre/{i}.csv", sep=";")

    if len(data) == len(data_date):
        # Salavando os dados em um arquivo .csv
        data.to_csv(f"../Api/trimestre/{i}.csv", sep=";")
    else:
        data["Data Divulgação"] = date_atual_m
        data.to_csv(f"../Api/trimestre/{i}.csv", sep=";")

arquivos = glob.glob("./trimestre/*.csv")
# "arquivos" agora é um array com o nome de todos os .csv que
# começam com "arquivo"
array_df = []
for x in arquivos:
    temp_df = pd.read_csv(x, sep=";")
    array_df.append(temp_df)

df = pd.concat(array_df, axis=0)
# df.to_csv("../Todos/TR.csv", sep=";")
df.to_parquet("../Todos/TR.parquet.gzip", compression="gzip")

#####
