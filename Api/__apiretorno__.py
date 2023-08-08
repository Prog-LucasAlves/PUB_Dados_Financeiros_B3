# Manipulação de dados
import pandas as pd
import numpy as np

# Barra de Progresso
from tqdm import tqdm

# Manipulação de datas
from datetime import timedelta, date
import time

# Coleta cotações
import yfinance as yf

# Lista com o nome das ações
import __list__

import warnings
warnings.filterwarnings('ignore')

# Lista com o nome dos ativos
acao = __list__.lst_acao

# Pegando as datas para os últimos N dias úteis
date1, date2 = date.today() - timedelta(days=2), date.today() - timedelta(days=0)


def retornoAcumulado():

    res = np.busday_count(date1.strftime('%Y-%m-%d'),
                          date2.strftime('%Y-%m-%d'))
    i = 1
    while res < 80:
        test_date1 = date.today() - timedelta(days=i)
        res = np.busday_count(test_date1.strftime('%Y-%m-%d'),
                              date2.strftime('%Y-%m-%d'))
        i = i + 1

    # Coletando as cotações de fechamento
    df = pd.DataFrame()
    for i in tqdm(acao):
        df[i] = yf.download(f'{i}.SA', start=test_date1, end=date2, progress=False, threads=False)['Adj Close']
        df.append(df)
        time.sleep(1)

    # Salvando os dados coletados
    df.to_csv('./retornos/cotacoes.csv', sep=';', index_label=False)


def retornoAcumuladodias(X):

    # Carregando o Dataset com os dados
    df = pd.read_csv('./retornos/cotacoes.csv', sep=';')

    # Selecionado as últimas N linhas
    df = df.tail(X)

    # Calculando os retonos diários
    df = round(df.pct_change() * 100, 2)

    # Reset do index
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Date'}, inplace=True)

    # Apagando a primeira linha
    df = df.drop(0)

    # Dias
    dias = df.shape[0]

    # Coletando os valores da coluna que era index (Data)
    lista_date = pd.DataFrame(df['Date'])
    lista_date['Date'] = pd.to_datetime(lista_date['Date'])
    lista_date['Date2'] = lista_date['Date'].dt.date
    lista_date2 = list(lista_date['Date2'])

    # Apagando a coluna 'Date' do DataFrame
    df.drop(['Date'], axis=1, inplace=True)

    # Fazendo a transposição linhas para colunas | colunas para linhas
    df = df.T

    # Criando uma nova 'variável' coluna com os retornos acumulados
    df['Total_Acumulado'] = round(df.sum(axis=1), 2)

    # Renomeando as colunas
    j = 0
    for i in df.columns[:dias]:
        df.rename(columns={i: f'{lista_date2[j]}'}, inplace=True)
        j = j + 1

    # Ordenando pelo maior retorno
    df.sort_values(by='Total_Acumulado', ascending=False)

    # Criando um DataFrame só com o Total acumulado de 10 dias
    df_filter = pd.DataFrame(df['Total_Acumulado'])

    # Reset do Index
    df_filter.reset_index(inplace=True)

    # Renomeando coluna 'index' -> 'Ação
    df_filter.rename(columns={'index': 'Papel'}, inplace=True)

    # Salva em um documento csv
    df_filter.to_csv(f'./retornos/retornos_acumulados_{(X-1)}d.csv', sep=';')


if __name__ == "__main__":
    retornoAcumulado()
    retornoAcumuladodias(16)
    retornoAcumuladodias(31)
    retornoAcumuladodias(46)
    retornoAcumuladodias(61)
