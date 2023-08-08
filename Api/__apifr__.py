"""
Descrição:
Esse código pega os dados dos fatos relevantes das empresas listadas na bolsa brasileira e armazena cada ação com os dados coletados em um arquivo .csv

Local: pasta(fatos_relevantes)
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
    url = f"https://www.fundamentus.com.br/fatos_relevantes.php?papel={i}"
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
            df_dados

            # Coletando o link do documento
            rows1 = soup1.findAll("tr")[1:]
            lista_link = []
            for t in range(len(rows1)):
                for link in rows1[t].find_all("a"):
                    lista_link.append(link.get("href"))

    # Adicionando os dados coletados em um DataFrame
    data = pd.DataFrame(df_dados, columns=column_headers[:])
    data["Link"] = lista_link

    # Deletando colunas nulas
    del data["Download"]
    del data["Tipo"]

    # Ajustando a coluna Data e criando um nova coluna Hora e Acao
    # (com o código da ação)
    df = data["Data"].apply(lambda x: str(x)[10:])
    data["Data"] = data["Data"].apply(lambda x: str(x)[:12])
    data["Hora"] = df
    data["Acao"] = i

    # Organizando as colunas no DataFrame
    data = data[["Acao", "Data", "Hora", "Descrição", "Link"]]

    # Removendo os espaços vazios das colunas Data e Hora
    data["Data"] = data["Data"].str.strip()
    data["Hora"] = data["Hora"].str.strip()

    # Salavando os dados em um arquivo .csv
    data.to_csv(f"./fatos_relevantes/{i}.csv", sep=";")

arquivos = glob.glob("./fatos_relevantes/*.csv")
# "arquivos" agora é um array com o nome de todos os .csv
# que começam com "arquivo"
array_df = []

for x in arquivos:
    temp_df = pd.read_csv(x, sep=";")
    array_df.append(temp_df)

df = pd.concat(array_df, axis=0)
# df.to_csv('../Todos/FT.csv', sep=';')
df.to_parquet("../Todos/FT.parquet.gzip", compression="gzip")

#####
