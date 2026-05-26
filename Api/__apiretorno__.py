# Manipulação de dados
import pathlib

# Warnings
import warnings

# Manipulação de datas
from datetime import date, timedelta

import numpy as np
import pandas as pd

# Coleta cotações
import yfinance as yf

# Barra de Progresso
from tqdm import tqdm

# Lista com o nome das ações
import __list__

# Elimina warnings
warnings.filterwarnings("ignore")

# Lista com o nome dos ativos
acao = __list__.lst_acao

# Pegando as datas para os últimos N dias úteis
date1, date2 = date.today() - timedelta(days=2), date.today() - timedelta(days=1)

# Caminho base do script para resolução de caminhos robusta
BASE_DIR = pathlib.Path(__file__).parent.resolve()
COTACOES_PATH = BASE_DIR / "retornos" / "cotacoes.csv"


# Função para coletar os dados de fechamento
def retornoAcumulado():
    res = np.busday_count(date1.strftime("%Y-%m-%d"), date2.strftime("%Y-%m-%d"))
    i = 1
    while res < 80:
        test_date1 = date.today() - timedelta(days=i)
        res = np.busday_count(
            test_date1.strftime("%Y-%m-%d"), date2.strftime("%Y-%m-%d")
        )
        i = i + 1

    # Coletando as cotações de fechamento
    df = pd.DataFrame()
    success_count = 0

    print(f"Iniciando download de {len(acao)} ativos de {test_date1} até {date2}...")
    for i in tqdm(acao):
        try:
            downloaded = yf.download(
                f"{i}.SA", start=test_date1, end=date2, progress=False, threads=False
            )
            if not downloaded.empty and "Close" in downloaded.columns:
                close_data = downloaded["Close"]
                # Caso o yfinance retorne um DataFrame MultiIndex, extraímos a coluna/série correspondente
                if isinstance(close_data, pd.DataFrame):
                    close_data = close_data.squeeze()

                if not close_data.empty:
                    df[i] = close_data
                    success_count += 1
        except Exception:
            pass  # Ignora falhas individuais silenciosamente para manter a barra limpa

    print(f"Download concluído. Sucesso: {success_count}/{len(acao)} ativos.")

    if df.empty:
        print(
            "[ALERTA] Nenhum dado foi baixado! O arquivo 'cotacoes.csv' não será sobrescrito com dados vazios."
        )
        return False

    # Garante que a pasta de destino exista
    COTACOES_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Salvando os dados coletados
    df.to_csv(COTACOES_PATH, sep=";", index_label=False)
    return True


def retornoAcumuladodias(X):
    try:
        # Carregando o Dataset com os dados
        df = pd.read_csv(COTACOES_PATH, sep=";")
    except FileNotFoundError:
        print(f"[ERRO] arquivo '{COTACOES_PATH}' não encontrado.")
        return
    except pd.errors.EmptyDataError:
        print(f"[ERRO] arquivo '{COTACOES_PATH}' está vazio.")
        return

    if df.empty or df.shape[0] < 2:
        print(
            f"[AVISO] Dados insuficientes em {COTACOES_PATH.name} ({df.shape[0]} linhas) para calcular retorno de {X} dias."
        )
        return

    # Selecionado as últimas N linhas
    df = df.tail(X)

    # Calculando os retonos diários
    df = round(df.pct_change() * 100, 2)

    # Reset do index
    df.reset_index(inplace=True)
    df.rename(columns={"index": "Date"}, inplace=True)

    # Apagando a primeira linha de forma segura
    if 0 in df.index:
        df = df.drop(0)
    else:
        df = df.iloc[1:]

    # Dias
    dias = df.shape[0]
    if dias == 0:
        print("[AVISO] Sem dias úteis suficientes após cálculo de variação percentual.")
        return

    # Coletando os valores da coluna que era index (Data)
    if "Date" not in df.columns:
        print("[ERRO] Coluna 'Date' ausente após reset_index.")
        return

    lista_date = pd.DataFrame(df["Date"])
    lista_date["Date"] = pd.to_datetime(lista_date["Date"])
    lista_date["Date2"] = lista_date["Date"].dt.date
    lista_date2 = list(lista_date["Date2"])

    # Apagando a coluna 'Date' do DataFrame
    df.drop(["Date"], axis=1, inplace=True)

    # Fazendo a transposição linhas para colunas | colunas para linhas
    df = df.T

    # Criando uma nova 'variável' coluna com os retornos acumulados
    df["Total_Acumulado"] = round(df.sum(axis=1), 2)

    # Renomeando as colunas
    j = 0
    for i in df.columns[:dias]:
        if j < len(lista_date2):
            df.rename(columns={i: f"{lista_date2[j]}"}, inplace=True)
            j = j + 1

    # Ordenando pelo maior retorno
    df = df.sort_values(by="Total_Acumulado", ascending=False)

    # Criando um DataFrame só com o Total acumulado
    df_filter = pd.DataFrame(df["Total_Acumulado"])

    # Reset do Index
    df_filter.reset_index(inplace=True)

    # Renomeando coluna 'index' -> 'Papel'
    df_filter.rename(columns={"index": "Papel"}, inplace=True)

    # Salva em um documento csv
    out_path = BASE_DIR / "retornos" / f"retornos_acumulados_{(X - 1)}d.csv"
    df_filter.to_csv(out_path, sep=";")
    print(
        f"[OK] Retornos acumulados de {X - 1} dias salvos com sucesso em {out_path.name}."
    )


if __name__ == "__main__":
    download_success = retornoAcumulado()
    # Só processa se o download ou arquivo existente tiver dados válidos
    retornoAcumuladodias(16)
    retornoAcumuladodias(31)
    retornoAcumuladodias(46)
    retornoAcumuladodias(61)
