import os

import pandas as pd
import streamlit as st


@st.cache_data(ttl=600)
def load_b3_data():
    df_data = pd.read_csv("./Dados_Atual/dados.csv", sep=";")
    ri_data = pd.read_csv("./Api/ri_empresas/ri_empresas.csv", sep=";")
    return df_data, ri_data


@st.cache_data(ttl=600)
def load_market_index_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path, sep=";")
    return None


@st.cache_data(ttl=600)
def load_parquet_data(file_path):
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    return None


@st.cache_data(ttl=600)
def load_stock_prices(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path, sep=";")
    return None


METRIC_HELPS = {
    "tipo": "ON: Ordinária com direito a voto. PN: Preferencial com preferência de dividendos e sem direito a voto clássico.",
    "empresa": "Nome comercial da empresa emissora listada na Bolsa de Valores (B3).",
    "dt_cotacao": "Data do fechamento do último pregão registrado para esta cotação de mercado.",
    "max_52": "Maior preço de fechamento atingido pela ação nas últimas 52 semanas (1 ano).",
    "min_52": "Menor preço de fechamento atingido pela ação nas últimas 52 semanas (1 ano).",
    "volume": "Média diária de volume financeiro negociado pelo ativo nos últimos 2 meses.",
    "valor_merc": "Preço da ação multiplicado pelo total de ações em circulação. Valor total da companhia na bolsa.",
    "valor_firma": "Valor de Mercado + Dívida Líquida. Representa o custo total teórico para adquirir a empresa inteira.",
    "nr_acoes": "Total de cotas/ações emitidas pela companhia e em circulação no mercado secundário.",
    "pl": "Preço / Lucro. Indica quantos anos o investidor levaria para recuperar o capital investido considerando o lucro atual constante.",
    "lpa": "Lucro por Ação. Parcela do lucro líquido atribuível a cada ação em circulação nos últimos 12 meses.",
    "pvp": "Preço / Valor Patrimonial. Relação entre o valor de mercado e o patrimônio contábil líquido. PVP < 1 indica desconto patrimonial.",
    "vpa": "Valor Patrimonial por Ação. Quanto vale cada ação com base no patrimônio líquido contábil da empresa.",
    "p_ebit": "Preço / EBIT. Relação entre preço de mercado e o lucro operacional antes de juros e impostos.",
    "psr": "Price to Sales Ratio. Relação entre o valor de mercado e sua receita operacional líquida.",
    "p_ativo": "Preço / Ativos Totais. Indica a proporção entre o valor que o mercado cobra pela empresa e seus ativos globais.",
    "p_cap": "Preço / Capital de Giro. Mede a avaliação de mercado da empresa em relação aos seus ativos circulantes líquidos.",
    "p_circ": "Preço / Ativos Circulantes Líquidos. Parâmetro de margem de segurança radical de Benjamin Graham.",
    "ev_ebitda": "Enterprise Value / EBITDA. Múltiplo operacional que indica quantos anos de geração de caixa operacional pagariam a firma.",
    "ev_ebit": "Enterprise Value / EBIT. Múltiplo operacional que mensura o retorno bruto do investimento na operação essencial.",
    "marg_bruta": "Margem Bruta. Lucro bruto dividido pela receita líquida. Mede a eficiência de produção de bens ou serviços.",
    "marg_ebit": "Margem EBIT. Lucro operacional dividido pela receita líquida. Indica a rentabilidade da operação essencial.",
    "marg_liquida": "Margem Líquida. Percentual de lucro líquido final gerado para cada real que entra como receita operacional líquida.",
    "div_yield": "Dividend Yield. Retorno pago em proventos nos últimos 12 meses dividido pela cotação atual do ativo.",
    "roe": "Return on Equity. Retorno sobre o Patrimônio Líquido. Capacidade de gerar lucro usando capital próprio dos acionistas.",
    "roic": "Return on Invested Capital. Retorno sobre Capital Investido. Rentabilidade gerada por todo o capital empregado (próprio + terceiros).",
    "ebit_ativo": "EBIT / Ativos Totais. Mede o poder de ganho bruto gerado pelos ativos globais operados pela companhia.",
    "ativo": "Valor total dos ativos da companhia, incluindo ativos operacionais e não operacionais, conforme o balanço patrimonial.",
    "ativo_circ": "Valor dos ativos circulantes da empresa, como caixa, estoques e contas a receber, disponível para uso de curto prazo.",
    "disponib": "Saldo de disponibilidades e caixa da companhia em relação ao período mais recente disponível no balanço.",
    "patr_liq": "Patrimônio líquido consolidado da companhia, representando o valor residual dos ativos após o desconto das obrigações.",
    "cres_rec": "Crescimento da receita líquida da empresa nos últimos 5 anos, indicando a evolução do negócio.",
    "liquidez": "Índice de liquidez corrente, medindo a capacidade da empresa de cumprir obrigações de curto prazo com seus ativos circulantes.",
    "div_bruta": "Valor total da dívida bruta da companhia, incluindo obrigações com terceiros antes de deduções de caixa e equivalentes.",
    "div_liquida": "Dívida líquida da empresa, considerando a dívida bruta menos as disponibilidades e equivalentes de caixa.",
    "lucro_12m": "Lucro líquido acumulado nos últimos 12 meses, refletindo a performance recente da companhia.",
    "lucro_3m": "Lucro líquido gerado nos últimos 3 meses, útil para avaliar a tendência recente dos resultados.",
}
