##################################
# Bibliotecas/Pacotes importadas #
##################################
import math
import os
import re
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import seaborn as sb
import streamlit as st

##################################
# Inicio da Construção Streamlit #
##################################

######
st.set_option("deprecation.showPyplotGlobalUse", False)

st.set_page_config(layout="wide")

# CURRENT_THEME = "light"
# IS_DARK_THEME = False

# Cabeçalho da página - Informações de fechamento de alguns Ìndices
st.subheader("🌎 Alguns Índices Globais")

# Cria colunas
col1, col2, col3 = st.columns(3)

ibov = pd.read_csv("./Api/indices/BVSP.csv", sep=";")
ibov_preco = round(ibov["Adj Close"].iloc[-1], 2)
ibov_retorno = ibov["Retornos"].iloc[-1]
ibov["Date"] = pd.to_datetime(ibov["Date"], utc=True)
ibov["Date"] = ibov["Date"].dt.date
ibov_date = ibov["Date"].iloc[-1]
col1.metric(
    label=f"IBOVESPA - {ibov_date}",
    value=f"{ibov_preco:.2f}",
    delta=f"{ibov_retorno}%",
)

ixic = pd.read_csv("./Api/indices/IXIC.csv", sep=";")
ixic_preco = round(ixic["Adj Close"].iloc[-1], 2)
ixic_retorno = ixic["Retornos"].iloc[-1]
ixic["Date"] = pd.to_datetime(ixic["Date"], utc=True)
ixic["Date"] = ixic["Date"].dt.date
ixic_date = ixic["Date"].iloc[-1]
col2.metric(
    label=f"NASDAQ Composite - {ixic_date}",
    value=f"{ixic_preco:.2f}",
    delta=f"{ixic_retorno}%",
)

dji = pd.read_csv("./Api/indices/DJI.csv", sep=";")
dji_precos = round(dji["Adj Close"].iloc[-1], 2)
dji_retorno = dji["Retornos"].iloc[-1]
dji["Date"] = pd.to_datetime(dji["Date"], utc=True)
dji["Date"] = dji["Date"].dt.date
dji_date = dji["Date"].iloc[-1]
col3.metric(
    label=f"Dow Jones Ind. Average - {dji_date}",
    value=f"{dji_precos:.2f}",
    delta=f"{dji_retorno}%",
)

sp_500 = pd.read_csv("./Api/indices/GSPC.csv", sep=";")
sp_500_preco = round(sp_500["Adj Close"].iloc[-1], 2)
sp_500_retorno = sp_500["Retornos"].iloc[-1]
sp_500["Date"] = pd.to_datetime(sp_500["Date"], utc=True)
sp_500["Date"] = sp_500["Date"].dt.date
sp_500_date = sp_500["Date"].iloc[-1]
col1.metric(
    label=f"S&P 500 - {sp_500_date}",
    value=f"{sp_500_preco:.2f}",
    delta=f"{sp_500_retorno}%",
)

vix = pd.read_csv("./Api/indices/VIX.csv", sep=";")
vix_preco = round(vix["Adj Close"].iloc[-1], 2)
vix_retorno = vix["Retornos"].iloc[-1]
vix["Date"] = pd.to_datetime(vix["Date"], utc=True)
vix["Date"] = vix["Date"].dt.date
vix_date = vix["Date"].iloc[-1]
col2.metric(
    label=f"VIX - {vix_date}",
    value=f"{vix_preco:.2f}",
    delta=f"{vix_retorno}%"
)

n225 = pd.read_csv("./Api/indices/N225.csv", sep=";")
n225_preco = round(n225["Adj Close"].iloc[-1], 2)
n225_retorno = n225["Retornos"].iloc[-1]
n225["Date"] = pd.to_datetime(n225["Date"], utc=True)
n225["Date"] = n225["Date"].dt.date
n225_date = n225["Date"].iloc[-1]
col3.metric(
    label=f"Nikkei 225 - {n225_date}",
    value=f"{n225_preco:.2f}",
    delta=f"{n225_retorno}%",
)

######
# Cabeçalho da página - Informações de fechamento de alguns Pares de Moedas
st.subheader("💵 Alguns Pares de Moedas")

######
# Cria colunas
col1, col2, col3 = st.columns(3)

usdbrl = pd.read_csv("./Api/moedas/USDBRL=x.csv", sep=";")
usdbrl_preco = round(usdbrl["Adj Close"].iloc[-1], 2)
usdbrl_retorno = usdbrl["Retornos"].iloc[-1]
usdbrl["Date"] = pd.to_datetime(usdbrl["Date"], utc=True)
usdbrl["Date"] = usdbrl["Date"].dt.date
usdbrl_date = usdbrl["Date"].iloc[-1]
col1.metric(
    label=f"USD-BRL - {usdbrl_date}",
    value=f"{usdbrl_preco:.2f}",
    delta=f"{usdbrl_retorno}%",
)

eurbrl = pd.read_csv("./Api/moedas/EURBRL=x.csv", sep=";")
eurbrl_preco = round(eurbrl["Adj Close"].iloc[-1], 2)
eurbrl_retorno = eurbrl["Retornos"].iloc[-1]
eurbrl["Date"] = pd.to_datetime(eurbrl["Date"], utc=True)
eurbrl["Date"] = eurbrl["Date"].dt.date
eurbrl_date = eurbrl["Date"].iloc[-1]
col2.metric(
    label=f"EUR-BRL - {eurbrl_date}",
    value=f"{eurbrl_preco:.2f}",
    delta=f"{eurbrl_retorno}%",
)

gbpbrl = pd.read_csv("./Api/moedas/GBPBRL=x.csv", sep=";")
gbpbrl_preco = round(gbpbrl["Adj Close"].iloc[-1], 2)
gbpbrl_retorno = gbpbrl["Retornos"].iloc[-1]
gbpbrl["Date"] = pd.to_datetime(gbpbrl["Date"], utc=True)
gbpbrl["Date"] = gbpbrl["Date"].dt.date
gbpbrl_date = gbpbrl["Date"].iloc[-1]
col3.metric(
    label=f"GBP-BRL - {gbpbrl_date}",
    value=f"{gbpbrl_preco:.2f}",
    delta=f"{gbpbrl_retorno}%",
)

brlusd = pd.read_csv("./Api/moedas/BRLUSD=x.csv", sep=";")
brlusd_preco = round(brlusd["Adj Close"].iloc[-1], 2)
brlusd_retorno = brlusd["Retornos"].iloc[-1]
brlusd["Date"] = pd.to_datetime(brlusd["Date"], utc=True)
brlusd["Date"] = brlusd["Date"].dt.date
brlusd_date = brlusd["Date"].iloc[-1]
col1.metric(
    label=f"BRL-USD - {brlusd_date}",
    value=f"{brlusd_preco:.2f}",
    delta=f"{brlusd_retorno}%",
)

eurusd = pd.read_csv("./Api/moedas/EURUSD=x.csv", sep=";")
eurusd_preco = round(eurusd["Adj Close"].iloc[-1], 2)
eurusd_retorno = eurusd["Retornos"].iloc[-1]
eurbrl["Date"] = pd.to_datetime(eurbrl['Date'], utc=True)
eurbrl["Date"] = eurbrl['Date'].dt.date
eurusd_date = eurusd["Date"].iloc[-1]
col2.metric(
    label=f"EUR-USD - {eurusd_date}",
    value=f"{eurusd_preco:.2f}",
    delta=f"{eurusd_retorno}%",
)

######
# Cabeçalho da página - Informações de fechamento de algumas Cryptomoedas
st.subheader("🪙 Algumas Cryptomoedas")

######
# Cria colunas
col1, col2, col3 = st.columns(3)

btcusd = pd.read_csv("./Api/crypto/BTC-USD.csv", sep=";")
btcusd_preco = round(btcusd["Adj Close"].iloc[-1], 2)
btcusd_retorno = btcusd["Retornos"].iloc[-1]
btcusd["Date"] = pd.to_datetime(btcusd["Date"], utc=True)
btcusd["Date"] = btcusd["Date"].dt.date
btcusd_date = btcusd["Date"].iloc[-1]
col1.metric(
    label=f"BTC-USD - {btcusd_date}",
    value=f"{btcusd_preco:.2f}",
    delta=f"{btcusd_retorno}%",
)

ethusd = pd.read_csv("./Api/crypto/ETH-USD.csv", sep=";")
ethusd_preco = round(ethusd["Adj Close"].iloc[-1], 2)
ethusd_retorno = ethusd["Retornos"].iloc[-1]
ethusd["Date"] = pd.to_datetime(ethusd["Date"], utc=True)
ethusd["Date"] = ethusd["Date"].dt.date
ethusd_date = ethusd["Date"].iloc[-1]
col2.metric(
    label=f"ETH-USD - {ethusd_date}",
    value=f"{ethusd_preco:.2f}",
    delta=f"{ethusd_retorno}%",
)

ltcusd = pd.read_csv("./Api/crypto/LTC-USD.csv", sep=";")
ltcusd_preco = round(ltcusd["Adj Close"].iloc[-1], 2)
ltcusd_retorno = ltcusd["Retornos"].iloc[-1]
ltcusd["Date"] = pd.to_datetime(ltcusd["Date"], utc=True)
ltcusd["Date"] = ltcusd["Date"].dt.date
ltcusd_date = ltcusd["Date"].iloc[-1]
col3.metric(
    label=f"USDT-USD - {ltcusd_date}",
    value=f"{ltcusd_preco:.2f}",
    delta=f"{ltcusd_retorno}%",
)

######
# Cabeçalho da página - Informações das Ações
st.subheader("ℹ️ Informações das Ações Listadas na B3")

######
# Importando os dados atuais
df = pd.read_csv("./Dados_Atual/dados.csv", sep=";")

######
# Cria barra lateral
st.sidebar.header("Escolha sua ação")
col1_selection = st.sidebar.selectbox(
    "Papel",
    df.papel,
    list(df.papel).index("AALR3"),
)

######
# Cria colunas
col1, col2 = st.columns(2)

# col1.1 - tipo
tipo = df[df["papel"] == col1_selection]
tipo_index = int(tipo["Unnamed: 0"])
tipo_result = tipo["tipo"][tipo_index]
col1.metric(label="Tipo", value=tipo_result)

# col2.1 - empresa
empresa = df[df["papel"] == col1_selection]
empresa_index = int(empresa["Unnamed: 0"])
empresa_result = empresa["empresa"][empresa_index]
col2.metric(label="Empresa", value=empresa_result)

# col1.2 - data da última cotação
dt_ult_cotacao = df[df["papel"] == col1_selection]
dt_ult_cotacao_index = int(dt_ult_cotacao["Unnamed: 0"])
dt_ult_cotacao_result = dt_ult_cotacao["dt_ult_cotacao"][dt_ult_cotacao_index]
col1.metric(
    label="Data da Última Cotação",
    value=dt_ult_cotacao_result,
    delta="Janeiro",
)

# col2.2 - valor da cotação + Variação do dia anterior
cotacao = df[df["papel"] == col1_selection]
cotacao_index = int(cotacao["Unnamed: 0"])
cotacao_result = cotacao["cotacao"][cotacao_index]

os_dia = df[df["papel"] == col1_selection]
os_dia_index = int(os_dia["Unnamed: 0"])
os_dia_result = os_dia["os_dia"][os_dia_index]

# varição da cotação da ação(%)
col2.metric(
    label="Valor da Ação",
    value=f"R${cotacao_result}",
    delta=f"{os_dia_result}%",
)

# col1.3 - máxima do valor da cotação em 52 semanas
max_52_sem = df[df["papel"] == col1_selection]
max_52_sem_index = int(max_52_sem["Unnamed: 0"])
max_52_sem_result = max_52_sem["max_52_sem"][max_52_sem_index]
col1.metric(
    label="Valor Máximo da Ação em 52 Semanas",
    value=f"R${max_52_sem_result}",
)

# col2.3 - mínima dao valor da cotação em 52 semanas
min_52_sem = df[df["papel"] == col1_selection]
min_52_sem_index = int(max_52_sem["Unnamed: 0"])
min_52_sem_result = min_52_sem["min_52_sem"][min_52_sem_index]
col2.metric(label="Valor Mínimo da Ação em 52 Semanas", value=f"R${min_52_sem_result}")

# col1.4 - volume de negociações
vol_med = df[df["papel"] == col1_selection]
vol_med_index = int(vol_med["Unnamed: 0"])
vol_med_result = vol_med["vol_med"][vol_med_index]
col1.metric(
    label="Volume Médio de Negociações(2 meses)", value=f"R${vol_med_result},00"
)

# col2.4 - valor de mercado da empresa
valor_mercado = df[df["papel"] == col1_selection]
valor_mercado_index = int(valor_mercado["Unnamed: 0"])
valor_mercado_result = valor_mercado["valor_mercado"][valor_mercado_index]
col2.metric(label="Valor de Mercado", value=f"R${valor_mercado_result},00")

# col1.5 - valor da firma
valor_firma = df[df["papel"] == col1_selection]
valor_firma_index = int(valor_firma["Unnamed: 0"])
valor_firma_result = valor_firma["valor_firma"][valor_firma_index]
col1.metric(label="Valor da Firma", value=f"R${valor_firma_result},00")

# col2.5 - número de ações em circulação
nr_acoes = df[df["papel"] == col1_selection]
nr_acoes_index = int(nr_acoes["Unnamed: 0"])
nr_acoes_result = nr_acoes["nr_acoes"][nr_acoes_index]
nr_acoes_int = re.sub(r"(?<!^)(?=(\d{3})+$)", r".", str(nr_acoes_result))
col2.metric(label="Número de Ações em Circulação", value=nr_acoes_int)

# col1.6 - preço / lucro
pl = df[df["papel"] == col1_selection]
pl_index = int(pl["Unnamed: 0"])
pl_result = pl["pl"][pl_index]
col1.metric(label="P/L - (Preço/Lucro)", value=f"{pl_result:.2f}")

# col2.6 - lucro por ação
lpa = df[df["papel"] == col1_selection]
lpa_index = int(lpa["Unnamed: 0"])
lpa_result = lpa["lpa"][lpa_index]
col2.metric(label="LPA - (Lucro por Ação)", value=f"{lpa_result:.2f}")

# col1.7 - preço / valor patrimonial por ação
pvp = df[df["papel"] == col1_selection]
pvp_index = int(pvp["Unnamed: 0"])
pvp_result = pvp["pvp"][pvp_index]
col1.metric(
    label="P/VP - (Preço/Valor Patrimonial por Ação)", value=f"{pvp_result:.2f}"
)

# col2.7 - valor patrimonial por ação
vpa = df[df["papel"] == col1_selection]
vpa_index = int(vpa["Unnamed: 0"])
vpa_result = vpa["vpa"][vpa_index]
col2.metric(label="VPA - (Valor Patrimonial por Ação)", value=f"{vpa_result:.2f}")

# col1.8 - preço da ação / pelo ebit por ação
p_ebit = df[df["papel"] == col1_selection]
p_ebit_index = int(p_ebit["Unnamed: 0"])
p_ebit_result = p_ebit["p_ebit"][p_ebit_index]
col1.metric(label="P/EBIT - (Preço/Ebit por Ação)", value=f"{p_ebit_result:.2f}")

# col2.8 - margem bruta
marg_bruta = df[df["papel"] == col1_selection]
marg_bruta_index = int(marg_bruta["Unnamed: 0"])
marg_bruta_result = marg_bruta["marg_bruta"][marg_bruta_index]
col2.metric(label="Margem Bruta", value=f"{marg_bruta_result:.2f}%")

# col1.9 - psr
psr = df[df["papel"] == col1_selection]
psr_index = int(psr["Unnamed: 0"])
psr_result = psr["psr"][psr_index]
col1.metric(label="PSR", value=f"{psr_result:.2f}")

# col2.9 - margem ebit
marg_ebit = df[df["papel"] == col1_selection]
marg_ebit_index = int(marg_ebit["Unnamed: 0"])
marg_ebit_result = marg_ebit["marg_ebit"][marg_ebit_index]
col2.metric(label="Margem Ebit", value=f"{marg_ebit_result:.2f}%")

# col1.10 - P/Ativo
p_ativo = df[df["papel"] == col1_selection]
p_ativo_index = int(p_ativo["Unnamed: 0"])
p_ativo_result = p_ativo["p_ativo"][p_ativo_index]
col1.metric(label="P/Ativos", value=f"{p_ativo_result:.2f}")

# col2.10 - margem liquida
marg_liquida = df[df["papel"] == col1_selection]
marg_liquida_index = int(marg_liquida["Unnamed: 0"])
marg_liquida_result = marg_liquida["marg_liquida"][marg_liquida_index]
col2.metric(label="Margem Líquida", value=f"{marg_liquida_result:.2f}%")

# col1.11 - preço / pelo capital de giro por ação
p_cap_giro = df[df["papel"] == col1_selection]
p_cap_giro_index = int(p_cap_giro["Unnamed: 0"])
p_cap_giro_result = p_cap_giro["p_cap_giro"][p_cap_giro_index]
col1.metric(label="P/Cap. Giro", value=f"{p_cap_giro_result:.2f}")

# col2.11 - ebit / por ativos totais
ebit_ativo = df[df["papel"] == col1_selection]
ebit_ativo_index = int(ebit_ativo["Unnamed: 0"])
ebit_ativo_result = ebit_ativo["ebit_ativo"][ebit_ativo_index]
col2.metric(label="Ebit/Ativo", value=f"{ebit_ativo_result:.2f}")

# col1.12 - preço / pelos ativos circulantes líquidos por ação
p_ativo_circ_liq = df[df["papel"] == col1_selection]
p_ativo_circ_liq_index = int(p_ativo_circ_liq["Unnamed: 0"])
p_ativo_circ_liq_result = p_ativo_circ_liq["p_ativo_circ_liq"][p_ativo_circ_liq_index]
col1.metric(label="P/Ativ. Cir. liq.", value=f"{p_ativo_circ_liq_result:.2f}")

# col2.12 - roic
roic = df[df["papel"] == col1_selection]
roic_index = int(roic["Unnamed: 0"])
roic_result = roic["roic"][roic_index]
col2.metric(label="ROIC", value=f"{roic_result:.2f}%")

# col1.13 - dividend yield
div_yield = df[df["papel"] == col1_selection]
div_yield_index = int(div_yield["Unnamed: 0"])
div_yield_result = div_yield["div_yield"][div_yield_index]
col1.metric(label="Divd. Yield", value=f"{div_yield_result:.2f}%")

# col2.13 - roe
roe = df[df["papel"] == col1_selection]
roe_index = int(roe["Unnamed: 0"])
roe_result = roe["roe"][roe_index]
col2.metric(label="ROE", value=f"{roe_result:.2f}%")

# col1.14 - ev / ebitda
ev_ebitda = df[df["papel"] == col1_selection]
ev_ebitda_index = int(ev_ebitda["Unnamed: 0"])
ev_ebitda_result = ev_ebitda["ev_ebitda"][ev_ebitda_index]
col1.metric(label="EV/Ebitda", value=f"{ev_ebitda_result:.2f}")

# col2.14 - liquidez corrente
liquidez_corr = df[df["papel"] == col1_selection]
liquidez_corr_index = int(liquidez_corr["Unnamed: 0"])
liquidez_corr_result = liquidez_corr["liquidez_corr"][liquidez_corr_index]
col2.metric(
    label="Liquidez Corrente - (Ativo Circulante / Passivo Circulante)",
    value=f"{liquidez_corr_result:.2f}",
)

# col1.15 - ev / ebit
ev_ebit = df[df["papel"] == col1_selection]
ev_ebit_index = int(ev_ebit["Unnamed: 0"])
ev_ebit_result = ev_ebit["ev_ebit"][ev_ebit_index]
col1.metric(label="EV/Ebit", value=f"{ev_ebit_result:.2f}")

# col2.15 - crescimento da receita líquida (5a)
cres_rec = df[df["papel"] == col1_selection]
cres_rec_index = int(cres_rec["Unnamed: 0"])
cres_rec_result = cres_rec["cres_rec"][cres_rec_index]
col2.metric(
    label="Crescimento da Receita Líquida(5 anos)", value=f"{cres_rec_result:.2f}%"
)

# col1.17 - ativo
ativo = df[df["papel"] == col1_selection]
ativo_index = int(ativo["Unnamed: 0"])
ativo_result = ativo["ativo"][ativo_index]
col1.metric(label="Ativo", value=f"R${ativo_result},00")

# col2.17 - disponibilidades
disponibilidades = df[df["papel"] == col1_selection]
disponibilidades_index = int(disponibilidades["Unnamed: 0"])
disponibilidades_result = disponibilidades["disponibilidades"][disponibilidades_index]
col2.metric(label="Disponibilidades", value=f"R${disponibilidades_result},00")

# col1.18 - ativo circulante
ativo_circulante = df[df["papel"] == col1_selection]
ativo_circulante_index = int(ativo_circulante["Unnamed: 0"])
ativo_circulante_result = ativo_circulante["ativo_circulante"][ativo_circulante_index]
col1.metric(label="Ativo Circulante", value=f"R${ativo_circulante_result},00")

# col2.18 - patrimônio líquido
patr_liquido = df[df["papel"] == col1_selection]
patr_liquido_index = int(patr_liquido["Unnamed: 0"])
patr_liquido_result = patr_liquido["patr_liquido"][patr_liquido_index]
col2.metric(label="Patrimônio Líquido", value=f"R${patr_liquido_result},00")

# col1.19 - dívida bruta
divd_bruta = df[df["papel"] == col1_selection]
divd_bruta_index = int(divd_bruta["Unnamed: 0"])
divd_bruta_result = divd_bruta["divd_bruta"][divd_bruta_index]
col1.metric(label="Dívida Bruta", value=f"R${divd_bruta_result},00")

# col2.19 - dívida líquida
divd_liquida = df[df["papel"] == col1_selection]
divd_liquida_index = int(divd_liquida["Unnamed: 0"])
divd_liquida_result = divd_liquida["divd_liquida"][divd_liquida_index]
col2.metric(label="Dívida Líquida", value=f"R${divd_liquida_result},00")

# col1.20 - lucro líquido 12m
lucro_liquido_12m = df[df["papel"] == col1_selection]
lucro_liquido_12m_index = int(lucro_liquido_12m["Unnamed: 0"])
lucro_liquido_12m_result = lucro_liquido_12m["lucro_liquido_12m"][
    lucro_liquido_12m_index
]
col1.metric(
    label="Lucro Líquido Últimos 12 Meses", value=f"R${lucro_liquido_12m_result},00"
)

# col2.20 - lucro líquido 3m
lucro_liquido_3m = df[df["papel"] == col1_selection]
lucro_liquido_3m_index = int(lucro_liquido_3m["Unnamed: 0"])
lucro_liquido_3m_result = lucro_liquido_3m["lucro_liquido_3m"][lucro_liquido_3m_index]
col2.metric(
    label="Lucro Líquido Últimos 3 Meses", value=f"R${lucro_liquido_3m_result},00"
)

######

# Retorno Acumulado

st.write("-----------------------------------------")
st.subheader("🎯 Retorno Acumulado ")

col1, col2, col3, col4 = st.columns(4)

retAcm15 = pd.read_csv("./Api/retornos/retornos_acumulados_15d.csv", sep=';')
retAcm15V = retAcm15[retAcm15['Papel'] == col1_selection]
retAcm15_index = int(retAcm15V["Unnamed: 0"])
retAcm15_result = retAcm15V["Total_Acumulado"][retAcm15_index]
col1.metric(
    label="Retorno Acumulado 15 Dias", value=f"{retAcm15_result:.2f}%"
)

retAcm30 = pd.read_csv("./Api/retornos/retornos_acumulados_30d.csv", sep=';')
retAcm30V = retAcm30[retAcm30['Papel'] == col1_selection]
retAcm30_index = int(retAcm30V["Unnamed: 0"])
retAcm30_result = retAcm30V["Total_Acumulado"][retAcm30_index]
col2.metric(
    label="Retorno Acumulado 30 Dias", value=f"{retAcm30_result:.2f}%"
)

retAcm45 = pd.read_csv("./Api/retornos/retornos_acumulados_45d.csv", sep=';')
retAcm45V = retAcm45[retAcm45['Papel'] == col1_selection]
retAcm45_index = int(retAcm45V["Unnamed: 0"])
retAcm45_result = retAcm45V["Total_Acumulado"][retAcm45_index]
col3.metric(
    label="Retorno Acumulado 45 Dias", value=f"{retAcm45_result:.2f}%"
)

retAcm60 = pd.read_csv("./Api/retornos/retornos_acumulados_60d.csv", sep=';')
retAcm60V = retAcm60[retAcm60['Papel'] == col1_selection]
retAcm60_index = int(retAcm60V["Unnamed: 0"])
retAcm60_result = retAcm60V["Total_Acumulado"][retAcm60_index]
col4.metric(
    label="Retorno Acumulado 60 Dias", value=f"{retAcm60_result:.2f}%"
)

######

# valor justo de uma ação segundo o cálculo de Graham
st.write("-----------------------------------------")
st.subheader("💎 Valor Justo de uma ação segundo o cálculo de Graham ")
acao_g = df[df["papel"] == col1_selection]
acao_g_index = int(acao_g["Unnamed: 0"])
acao_g_result = acao_g["papel"][acao_g_index]

vpa_f = acao_g["vpa"][acao_g_index]
lpa_f = acao_g["lpa"][acao_g_index]
prc_f = acao_g["cotacao"][acao_g_index]
prc_f1 = prc_f.replace(",", ".")
prc_f2 = float(prc_f1)
divb_f = acao_g["divd_bruta"][acao_g_index]
prtl_f = acao_g["patr_liquido"][acao_g_index]
lucro_f = acao_g["lucro_liquido_12m"][acao_g_index]

if vpa_f <= 0 or lpa_f <= 0:
    st.write(
        f" A empresa {acao_g_result} nos últimos 12 meses teve um prejuizo de: R${lucro_f},00. "
    )
    st.write(
        f" Obs.: Empresa com prejuízo!!! - \
        Não será possível achar o valor justo da ação {acao_g_result} \
        segundo o cálculo de Graham. "
    )
    st.write("**Busque por outra empresa**")
else:
    st.write(
        f"A empresa {acao_g_result} nos últimos 12 meses teve um lucro de: R${lucro_f},00."
    )

    # Valor do cálculo de Graham:
    valor_gh = round(22.5 * vpa_f * lpa_f, 2)

    # Valor justo da ação analisada:
    valor_jt = round(math.sqrt(valor_gh), 2)

    # Cálculo do Upside / Downside:
    up_dw = round(((prc_f2 / valor_jt) - 1) * 100, 2)

    # Resultado da análise:
    st.write(f"O valor justo da ação {acao_g_result}: R${valor_jt}.")
    st.write(f"O valor atual da ação {acao_g_result}: R${prc_f}.")
    if up_dw > 0:
        st.write(
            f"\
 📈 A ação {acao_g_result}, esta com *{up_dw:.2f}%* acima do seu valor justo."
        )
    else:
        st.write(
            f"\
📉 A ação {acao_g_result}, esta com *{up_dw:.2f}%* abaixo do seu valor justo."
        )

######

# Tabela Fatos Relevantes
st.write("-----------------------------------------")
fr = df[df["papel"] == col1_selection]
fr_index = int(fr["Unnamed: 0"])
fr_papel = fr["papel"][fr_index]
fr_df = pd.read_csv(f"./Api/fatos_relevantes/{fr_papel}.csv", sep=";")
fr_df_1 = fr_df[["Data", "Hora", "Descrição", "Link"]]
st.caption(" ⏰ Fatos Relevamtes ")
st.write(fr_df_1)
fr_df_data = fr_df_1["Data"][0]
fr_df_link = fr_df_1["Link"][0]
st.write(f"Data Último Fato Relevante {fr_df_data} - Download: [Link]({fr_df_link})")

# Tabela Proventos
st.write("-----------------------------------------")
pr = df[df["papel"] == col1_selection]
pr_index = int(pr["Unnamed: 0"])
pr_papel = pr["papel"][pr_index]
# Pagando os dados dos proventos nos arquivos .csv
if os.path.isfile(f"./Api/proventos/{pr_papel}.csv"):
    pr_df = pd.read_csv(f"./Api/proventos/{pr_papel}.csv", sep=";")
    pr_df_1 = pr_df[["Data", "Valor", "Tipo", "Data de Pagamento", "Por quantas ações"]]
    st.caption(" 💵 Proventos ")
    st.caption(
        ' *A data se refere ao "último dia com", ou seja, \
    a data em que o acionista passa a ter o direito de receber o dividendo caso termine o dia com a ação. '
    )
    st.write(pr_df_1)
else:
    st.write(" 💵 Sem Proventos")

######

# Tabela Dados Trimestrais
st.write("-----------------------------------------")
tri = df[df["papel"] == col1_selection]
tri_index = int(tri["Unnamed: 0"])
tri_papel = tri["papel"][tri_index]
# Pagando os dados dos resultados trimestrais nos arquivos .csv
tri_df = pd.read_csv(f"./Api/trimestre/{tri_papel}.csv", sep=";")
tri_df_1 = tri_df[
    ["Data Referência", "Demonstração Financeira", "Release de Resultados"]
]
st.caption(" 💵 Dados Trimestrais ")
st.write(tri_df_1)
tri_ref = tri_df_1["Data Referência"][0]
tri_rel = tri_df_1["Release de Resultados"][0]
st.write(
    f"📝 Data de Referência {tri_ref} - Download Release {tri_papel}: [link]({tri_rel})"
)

######

# Gráfico de preço de fechamento da ações
# Código para pegar o preço das ações
st.write("-----------------------------------------")
precos = df[df["papel"] == col1_selection]
precos_index = int(precos["Unnamed: 0"])
precos_papel = precos["papel"][pr_index]
# Pegando os dados dos preços nos arquivos .csv
precos_df = pd.read_csv(f"./Api/precos/{precos_papel}.csv", sep=";")
precos_df_ad = precos_df.rename({"Adj Close": f"{precos_papel}"}, axis=1)
precos_df_ad = precos_df_ad.drop(precos_df_ad.columns[[1, 2, 3, 4, 6]], axis=1)

# Gráfico com o historico de fechamento
st.write(f" 📈📉 Histórico de Fechamento da Ação {precos_papel} ")
fig_pre = px.line(precos_df_ad, x="Date", y=f"{precos_papel}")
fig_pre.update_layout(
    xaxis_title="Date", yaxis_title=f"Preço de Fechamento - {precos_papel}"
)
st.plotly_chart(fig_pre)

df_download = pd.read_csv(f"./Api/precos/{precos_papel}p.csv", sep=';')

######

# Tabela de Retornos
st.write("-----------------------------------------")
st.write(f" ✳️ Retornos da Ação {precos_papel} - Mensal ")
tb_df = pd.read_csv(f"./Api/historico/{precos_papel}.csv", sep=";", index_col=[0])
cm = sb.light_palette("green", as_cmap=True)
st.table(tb_df.style.background_gradient(cmap=cm))

######

# Gráfico de Retornos Diários
st.write("-----------------------------------------")
st.write(f" ⌛ Retornos Diários da Ação {precos_papel} ")
precos_df_ret = precos_df_ad[f"{precos_papel}"].pct_change()
precos_df_ad[f"Ret {precos_papel}"] = precos_df_ret
fig_ret = px.line(precos_df_ad, x="Date", y=f"Ret {precos_papel}")
fig_ret.update_layout(
    xaxis_title="Date", yaxis_title=f"Retorno Diário - {precos_papel}"
)
st.plotly_chart(fig_ret)

######

# Gráfico de Retornos Diários
st.write("-----------------------------------------")
st.write(f" ⌛ Retornos Acumulados da Ação {precos_papel} ")
df_ret_ac = pd.read_csv(f"./Api/precos/{precos_papel}.csv", sep=";")
fig_ret_ac = px.line(df_ret_ac, x="Date", y="tret")
fig_ret_ac.update_layout(
    xaxis_title="Date", yaxis_title=f"Retorno Acumulado(%) - {precos_papel}"
)
st.plotly_chart(fig_ret_ac)
######

# Gráfico de Voltilidade
st.write("-----------------------------------------")
st.write(f" 🔥 Volatiliadade da Ação {precos_papel} - (30 dias) ")
precos_df_vol = precos_df_ad[f"Ret {precos_papel}"].rolling(window=30).std()
precos_df_ad[f"Vol {precos_papel}"] = precos_df_vol
fig_vol = px.line(precos_df_ad, x="Date", y=f"Vol {precos_papel}")
fig_vol.update_layout(xaxis_title="Date", yaxis_title=f"Volatilidade - {precos_papel}")
st.plotly_chart(fig_vol)

######

st.write("-----------------------------------------")
date_att = datetime.today()
atraso = timedelta(1)
date_atual = date_att - atraso
date_atual_m = date_atual.strftime("%d/%m/%Y")
st.write(f"Atualizações do dia {date_atual_m}:")

st.write("📰 Fatos Relevantes:")
# df_analisar_ft = pd.read_csv("./Todos/FT.csv", sep=";")
df_analisar_ft = pd.read_parquet("./Todos/FT.parquet.gzip")
df_date_ft = df_analisar_ft.loc[
    df_analisar_ft["Data"] == date_atual_m, ["Acao", "Link"]
]
if df_date_ft.empty is False:
    st.write(list(df_date_ft["Acao"].unique()))
else:
    st.write("*Sem Atualizações* 🤫")

st.write("💰 Proventos:")
# df_analisar_pr = pd.read_csv("./Todos/PR.csv", sep=";")
df_analisar_pr = pd.read_parquet("./Todos/PR.parquet.gzip")
df_date_pr = df_analisar_pr.loc[df_analisar_pr["Data"] == date_atual_m, ["Acao"]]
if df_date_pr.empty is False:
    st.write(list(df_date_pr["Acao"].unique()))
else:
    st.write("*Sem Atualizações* 🤫")

st.write("📋 Dados Trimestrais - Release de Resultados:")
# df_analisar_tr = pd.read_csv("./Todos/TR.csv", sep=";")
df_analisar_tr = pd.read_parquet("./Todos/TR.parquet.gzip")
df_date_tr = df_analisar_tr.loc[
    df_analisar_tr["Data Referência"] == date_atual_m, ["Acao"]
]
if df_date_tr.empty is False:
    st.write(list(df_date_tr["Acao"].unique()))
else:
    st.write("*Sem Atualizações* 🤫")

######

# Rodapé
st.write("-----------------------------------------")
st.write("*Utilize modo light para uma melhor visualização.*")

#####
