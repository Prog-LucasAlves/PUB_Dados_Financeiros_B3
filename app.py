##################################
# Bibliotecas/Pacotes importadas #
##################################
import importlib
import math
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import plotly.express as px
import seaborn as sb
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "SRC"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

try:
    __list__ = importlib.import_module("__list__")
except ImportError:
    if str(SRC_DIR) not in sys.path:
        sys.path.insert(0, str(SRC_DIR))
    __list__ = importlib.import_module("__list__")

b3_app = importlib.import_module("b3_app")
METRIC_HELPS = b3_app.METRIC_HELPS
apply_plotly_theme = b3_app.apply_plotly_theme
check_stock_data_integrity = b3_app.check_stock_data_integrity
estimate_accumulated_return = b3_app.estimate_accumulated_return
fmt_decimal = b3_app.fmt_decimal
fmt_money = b3_app.fmt_money
fmt_percent = b3_app.fmt_percent
format_thousands = b3_app.format_thousands
get_stock_data_val_from_df = b3_app.get_stock_data_val
inject_custom_css = b3_app.inject_custom_css
load_b3_data = b3_app.load_b3_data
load_parquet_data = b3_app.load_parquet_data
load_price_history = b3_app.load_price_history
load_accumulated_return = b3_app.load_accumulated_return
prepare_price_metrics = b3_app.prepare_price_metrics
render_market_index = b3_app.render_market_index
render_metric_card = b3_app.render_metric_card
render_status_card = b3_app.render_status_card

##################################
# Inicio da Construção Streamlit #
##################################

st.set_page_config(
    page_title="Neo-B3 Obsidian | Painel Financeiro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Inject visual styles
inject_custom_css()

# Branded Hero Header
st.markdown(
    """
    <div class="hero-header">
        <div class="hero-nav">
            <div class="hero-logo"><span class="hero-logo-accent">⚡</span> NEO-B3 <span style="font-weight: 300; opacity: 0.8;">OBSIDIAN</span></div>
            <div class="hero-badge"><span class="hero-badge-dot"></span> LIVE DATA TRACKING</div>
        </div>
        <div class="hero-title">Inteligência Financeira Premium</div>
        <div class="hero-subtitle">Sua central definitiva de análise, valuation e métricas de mercado para ativos da B3. Alta performance com design de ponta.</div>
        <div class="hero-actions">
            <a class="hero-btn hero-btn-primary" href="#informacoes-das-acoes-listadas-na-b3">Começar Análise</a>
            <a class="hero-btn hero-btn-secondary" href="https://github.com/Prog-LucasAlves/PUB_Dados_Financeiros_B3" target="_blank">Repositório GitHub</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Header - Global Indices, Currencies & Cryptos in a clean expander to avoid visual clutter
with st.expander(
    "🌍 Painel de Mercado: Índices Globais, Moedas e Cripto", expanded=False
):
    # Header - Global Indices
    st.markdown(
        '<h3 class="stSubheader" style="margin-top: 0 !important;">🌎 Alguns Índices Globais</h3>',
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns(3)

    render_market_index("./Api/indices/BVSP.csv", "IBOVESPA", col1)
    render_market_index("./Api/indices/IXIC.csv", "NASDAQ Composite", col2)
    render_market_index("./Api/indices/DJI.csv", "Dow Jones Ind. Average", col3)
    render_market_index("./Api/indices/GSPC.csv", "S&P 500", col1)
    render_market_index("./Api/indices/VIX.csv", "VIX", col2)
    render_market_index("./Api/indices/N225.csv", "Nikkei 225", col3)

    st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)

    # Header - Currencies
    st.markdown(
        '<h3 class="stSubheader">💵 Alguns Pares de Moedas</h3>', unsafe_allow_html=True
    )
    col1, col2, col3 = st.columns(3)

    render_market_index("./Api/moedas/USDBRL=x.csv", "USD-BRL", col1)
    render_market_index("./Api/moedas/EURBRL=x.csv", "EUR-BRL", col2)
    render_market_index("./Api/moedas/GBPBRL=x.csv", "GBP-BRL", col3)
    render_market_index("./Api/moedas/BRLUSD=x.csv", "BRL-USD", col1)
    render_market_index("./Api/moedas/EURUSD=x.csv", "EUR-USD", col2)

    st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)

    # Header - Cryptos
    st.markdown(
        '<h3 class="stSubheader">🪙 Algumas Cryptomoedas</h3>', unsafe_allow_html=True
    )
    col1, col2, col3 = st.columns(3)

    render_market_index("./Api/crypto/BTC-USD.csv", "BTC-USD", col1)
    render_market_index("./Api/crypto/ETH-USD.csv", "ETH-USD", col2)
    render_market_index(
        "./Api/crypto/LTC-USD.csv", "USDT-USD", col3
    )  # note: using path LTC-USD but keeping visual label USDT-USD as original

st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)

# B3 Stock details section
st.markdown(
    '<h3 class="stSubheader">ℹ️ Informações das Ações Listadas na B3</h3>',
    unsafe_allow_html=True,
)

# Read base data
df, ri = load_b3_data()

# Combine tickers from dados.csv and the master ticker list in SRC/__list__.py to ensure all appear
all_tickers = sorted(list(set(df.papel.tolist() + __list__.lst_acao)))

# Sidebar stock selectbox
st.sidebar.header("Escolha sua ação")
default_index = 0
if "AALR3" in all_tickers:
    default_index = all_tickers.index("AALR3")

col1_selection = st.sidebar.selectbox(
    "Papel",
    all_tickers,
    index=default_index,
)

# Render RI button
ri_filtered = ri[ri["Acao"] == col1_selection]
if not ri_filtered.empty:
    ri_index = int(ri_filtered["Unnamed: 0"].iloc[0])
    ri_result = ri_filtered["Site"].loc[ri_index]
    st.sidebar.link_button(
        f"🔗 RI da Ação {col1_selection}",
        ri_result,
    )

# 1. Simulação de Valuation: Graham Constant Slider
st.sidebar.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
st.sidebar.subheader("Simulação de Valuation")
graham_constant = st.sidebar.slider(
    "Constante de Graham",
    min_value=10.0,
    max_value=30.0,
    value=22.5,
    step=0.5,
    help="Ajuste a constante clássica de Graham (padrão 22.5, que assume P/L de até 15 e P/VP de até 1.5) para simular diferentes margens de segurança.",
)


# 2. Scraper Data Integrity Panel
integrity_data = check_stock_data_integrity(col1_selection)

any_critical_missing = any(
    not exists and is_critical for name, (exists, is_critical) in integrity_data.items()
)


def get_stock_data_val(column_name):
    return get_stock_data_val_from_df(df, col1_selection, column_name)


# --- PRE-LOAD STOCK PRICES & HISTORICAL METRICS ---
if any_critical_missing:
    status_class = "status-alert"
    header_title = "⚠️ Dados Incompletos"
else:
    status_class = "status-success"
    header_title = "🛡️ Integridade de Dados"

rows_html = ""
for name, (exists, is_critical) in integrity_data.items():
    if exists:
        color = "#10B981"
        status_text = "Disponível"
    else:
        color = "#EF4444" if is_critical else "#64748B"
        status_text = "Ausente" if is_critical else "Não se aplica"

    rows_html += (
        f"<span style=\"display: flex; justify-content: space-between; align-items: center; font-size: 12px; font-family: 'Outfit', sans-serif; width: 100%;\">"
        f'<span style="color: #94A3B8;">{name}</span>'
        f'<span style="display: flex; align-items: center; gap: 4px; font-weight: 500; color: {color};">'
        f'<span style="color: {color}; font-size: 8px; vertical-align: middle;">●</span> {status_text}'
        f"</span></span>"
    )

st.sidebar.markdown(
    f'<div class="status-card {status_class}" style="margin-top: 15px; padding: 12px 16px;">'
    f'<p style="font-size: 13px; font-weight: 600; color: #F8FAFC; margin-top: 0; margin-bottom: 10px; display: flex; align-items: center; gap: 6px;">{header_title}</p>'
    f'<span style="display: flex; flex-direction: column; gap: 8px; width: 100%;">{rows_html}</span>'
    f"</div>",
    unsafe_allow_html=True,
)


# --- PRE-LOAD STOCK PRICES & HISTORICAL METRICS ---
precos_path = f"./Api/precos/{col1_selection}.csv"
last_close = get_stock_data_val("cotacao")
precos_df_clean, prices_loaded, is_contingency = load_price_history(
    precos_path, col1_selection, last_close
)

if prices_loaded and precos_df_clean is not None:
    precos_df_clean = prepare_price_metrics(precos_df_clean, col1_selection)


def render_ret_acum(file_path, label, days, col):
    val = load_accumulated_return(file_path, col1_selection)
    if val is None or pd.isna(val):
        val = estimate_accumulated_return(precos_df_clean, col1_selection, days)

    if val is not None and not pd.isna(val):
        is_pos = val >= 0
        color = "#10B981" if is_pos else "#EF4444"
        arrow = "▲" if is_pos else "▼"
        delta_class = "delta-positive" if is_pos else "delta-negative"
        sign = "+" if is_pos else ""

        card_html = f"""
        <div class="metric-card" style="border-left: 3px solid {color};">
            <div class="metric-label">{label} <span style="font-size: 10px; color: #64748B; font-family: 'Outfit', sans-serif;">(Histórico)</span></div>
            <div class="metric-value" style="color: {color}; font-size: 24px; margin-top: 4px;">{sign}{val:.2f}%</div>
            <div class="metric-delta {delta_class}" style="margin-top: 8px;">{arrow} {abs(val):.2f}%</div>
        </div>
        """
        col.markdown(card_html, unsafe_allow_html=True)
    else:
        render_metric_card(label, "N/A", col=col)


# Organize stock data metrics in tabs
tab_overview, tab_valuation, tab_efficiency, tab_balance = st.tabs(
    [
        "📊 Visão Geral & Mercado",
        "🔑 Valuation & Multiplicadores",
        "📈 Rentabilidade & Eficiência",
        "🏛️ Saúde Financeira & Balanço",
    ]
)

with tab_overview:
    col1, col2 = st.columns(2)

    tipo_res = get_stock_data_val("tipo")
    empresa_res = get_stock_data_val("empresa")
    dt_ult_res = get_stock_data_val("dt_ult_cotacao")
    cotacao_res = get_stock_data_val("cotacao")
    os_dia_res = get_stock_data_val("os_dia")
    max_52_res = get_stock_data_val("max_52_sem")
    min_52_res = get_stock_data_val("min_52_sem")
    vol_med_res = get_stock_data_val("vol_med")
    val_merc_res = get_stock_data_val("valor_mercado")
    val_firma_res = get_stock_data_val("valor_firma")
    nr_acoes_res = get_stock_data_val("nr_acoes")

    # Format actions count
    nr_acoes_formatted = format_thousands(nr_acoes_res)

    # Coluna 1 - Identidade & Valores Corporativos
    render_metric_card("Empresa", empresa_res, col=col1, help=METRIC_HELPS["empresa"])
    render_metric_card("Tipo da Ação", tipo_res, col=col1, help=METRIC_HELPS["tipo"])
    render_metric_card(
        "Ações em Circulação",
        nr_acoes_formatted,
        col=col1,
        help=METRIC_HELPS["nr_acoes"],
    )
    render_metric_card(
        "Valor de Mercado",
        fmt_money(val_merc_res),
        col=col1,
        help=METRIC_HELPS["valor_merc"],
    )
    render_metric_card(
        "Valor da Firma",
        fmt_money(val_firma_res),
        col=col1,
        help=METRIC_HELPS["valor_firma"],
    )

    # Coluna 2 - Negociação & Histórico de Preços
    render_metric_card(
        "Valor da Ação",
        fmt_money(cotacao_res),
        fmt_percent(os_dia_res),
        col=col2,
        help="Último preço de fechamento registrado (com variação diária).",
    )
    render_metric_card(
        "Data da Última Cotação", dt_ult_res, col=col2, help=METRIC_HELPS["dt_cotacao"]
    )
    render_metric_card(
        "Máxima 52 Semanas",
        fmt_money(max_52_res),
        col=col2,
        help=METRIC_HELPS["max_52"],
    )
    render_metric_card(
        "Mínima 52 Semanas",
        fmt_money(min_52_res),
        col=col2,
        help=METRIC_HELPS["min_52"],
    )
    render_metric_card(
        "Volume Médio (2 meses)",
        fmt_money(vol_med_res),
        col=col2,
        help=METRIC_HELPS["volume"],
    )

    # Retornos Acumulados da Ação (Neatly integrated inside Visão Geral tab)
    st.markdown(
        '<div class="custom-hr" style="margin: 1.5rem 0 1rem 0;"></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h4 style=\"font-family: 'Outfit', sans-serif; font-weight: 600; color: #F1F5F9; margin-bottom: 12px; font-size: 1.15rem;\">🎯 Retornos Acumulados da Ação</h4>",
        unsafe_allow_html=True,
    )
    col_ret1, col_ret2, col_ret3, col_ret4 = st.columns(4)

    render_ret_acum(
        "./Api/retornos/retornos_acumulados_15d.csv", "15 Dias", 15, col_ret1
    )
    render_ret_acum(
        "./Api/retornos/retornos_acumulados_30d.csv", "30 Dias", 30, col_ret2
    )
    render_ret_acum(
        "./Api/retornos/retornos_acumulados_45d.csv", "45 Dias", 45, col_ret3
    )
    render_ret_acum(
        "./Api/retornos/retornos_acumulados_60d.csv", "60 Dias", 60, col_ret4
    )

with tab_valuation:
    col1, col2 = st.columns(2)

    pl_res = get_stock_data_val("pl")
    lpa_res = get_stock_data_val("lpa")
    pvp_res = get_stock_data_val("pvp")
    vpa_res = get_stock_data_val("vpa")
    p_ebit_res = get_stock_data_val("p_ebit")
    psr_res = get_stock_data_val("psr")
    p_ativo_res = get_stock_data_val("p_ativo")
    p_cap_res = get_stock_data_val("p_cap_giro")
    p_circ_res = get_stock_data_val("p_ativo_circ_liq")
    ev_ebitda_res = get_stock_data_val("ev_ebitda")
    ev_ebit_res = get_stock_data_val("ev_ebit")

    # Coluna 1 - Multiplicadores de Preço & Patrimônio (Equity Valuation)
    render_metric_card(
        "Preço / Lucro (P/L)", fmt_decimal(pl_res), col=col1, help=METRIC_HELPS["pl"]
    )
    render_metric_card(
        "Lucro por Ação (LPA)", fmt_decimal(lpa_res), col=col1, help=METRIC_HELPS["lpa"]
    )
    render_metric_card("P/VP", fmt_decimal(pvp_res), col=col1, help=METRIC_HELPS["pvp"])
    render_metric_card(
        "Valor Patrimonial por Ação (VPA)",
        fmt_decimal(vpa_res),
        col=col1,
        help=METRIC_HELPS["vpa"],
    )
    render_metric_card("PSR", fmt_decimal(psr_res), col=col1, help=METRIC_HELPS["psr"])
    render_metric_card(
        "P/Ativos", fmt_decimal(p_ativo_res), col=col1, help=METRIC_HELPS["p_ativo"]
    )

    # Coluna 2 - Enterprise Value, Operacional & Liquidez Ativa
    render_metric_card(
        "EV / EBITDA",
        fmt_decimal(ev_ebitda_res),
        col=col2,
        help=METRIC_HELPS["ev_ebitda"],
    )
    render_metric_card(
        "EV / EBIT", fmt_decimal(ev_ebit_res), col=col2, help=METRIC_HELPS["ev_ebit"]
    )
    render_metric_card(
        "P/EBIT", fmt_decimal(p_ebit_res), col=col2, help=METRIC_HELPS["p_ebit"]
    )
    render_metric_card(
        "P/Capital Giro", fmt_decimal(p_cap_res), col=col2, help=METRIC_HELPS["p_cap"]
    )
    render_metric_card(
        "P/Ativo Circulante Líquido",
        fmt_decimal(p_circ_res),
        col=col2,
        help=METRIC_HELPS["p_circ"],
    )

with tab_efficiency:
    col1, col2 = st.columns(2)

    m_bruta = get_stock_data_val("marg_bruta")
    m_ebit = get_stock_data_val("marg_ebit")
    m_liquida = get_stock_data_val("marg_liquida")
    ebit_ativo_res = get_stock_data_val("ebit_ativo")
    roic_res = get_stock_data_val("roic")
    roe_res = get_stock_data_val("roe")
    div_yield_res = get_stock_data_val("div_yield")

    # Coluna 1 - Margens de Lucro & Dividendos
    render_metric_card(
        "Margem Bruta", fmt_percent(m_bruta), col=col1, help=METRIC_HELPS["marg_bruta"]
    )
    render_metric_card(
        "Margem EBIT", fmt_percent(m_ebit), col=col1, help=METRIC_HELPS["marg_ebit"]
    )
    render_metric_card(
        "Margem Líquida",
        fmt_percent(m_liquida),
        col=col1,
        help=METRIC_HELPS["marg_liquida"],
    )
    render_metric_card(
        "Dividend Yield",
        fmt_percent(div_yield_res),
        col=col1,
        help=METRIC_HELPS["div_yield"],
    )

    # Coluna 2 - Retornos & Eficiência de Capital
    render_metric_card("ROE", fmt_percent(roe_res), col=col2, help=METRIC_HELPS["roe"])
    render_metric_card(
        "ROIC", fmt_percent(roic_res), col=col2, help=METRIC_HELPS["roic"]
    )
    render_metric_card(
        "EBIT / Ativo",
        fmt_decimal(ebit_ativo_res),
        col=col2,
        help=METRIC_HELPS["ebit_ativo"],
    )

with tab_balance:
    col1, col2 = st.columns(2)

    liquidez_corr_res = get_stock_data_val("liquidez_corr")
    cres_rec_res = get_stock_data_val("cres_rec")
    ativo_res = get_stock_data_val("ativo")
    disponib_res = get_stock_data_val("disponibilidades")
    ativo_circ_res = get_stock_data_val("ativo_circulante")
    patr_liq_res = get_stock_data_val("patr_liquido")
    div_bruta_res = get_stock_data_val("divd_bruta")
    div_liquida_res = get_stock_data_val("divd_liquida")
    lucro_12m_res = get_stock_data_val("lucro_liquido_12m")
    lucro_3m_res = get_stock_data_val("lucro_liquido_3m")

    # Coluna 1 - Estrutura Patrimonial & Ativos
    render_metric_card(
        "Ativo Total", fmt_money(ativo_res), col=col1, help=METRIC_HELPS["ativo"]
    )
    render_metric_card(
        "Ativo Circulante",
        fmt_money(ativo_circ_res),
        col=col1,
        help=METRIC_HELPS["ativo_circ"],
    )
    render_metric_card(
        "Disponibilidades",
        fmt_money(disponib_res),
        col=col1,
        help=METRIC_HELPS["disponib"],
    )
    render_metric_card(
        "Patrimônio Líquido",
        fmt_money(patr_liq_res),
        col=col1,
        help=METRIC_HELPS["patr_liq"],
    )
    render_metric_card(
        "Crescimento Receita Líquida (5a)",
        fmt_percent(cres_rec_res),
        col=col1,
        help=METRIC_HELPS["cres_rec"],
    )

    # Coluna 2 - Perfil de Endividamento, Liquidez & Lucros
    render_metric_card(
        "Liquidez Corrente",
        fmt_decimal(liquidez_corr_res),
        col=col2,
        help=METRIC_HELPS["liquidez"],
    )
    render_metric_card(
        "Dívida Bruta",
        fmt_money(div_bruta_res),
        col=col2,
        help=METRIC_HELPS["div_bruta"],
    )
    render_metric_card(
        "Dívida Líquida",
        fmt_money(div_liquida_res),
        col=col2,
        help=METRIC_HELPS["div_liquida"],
    )
    render_metric_card(
        "Lucro Líquido 12 Meses",
        fmt_money(lucro_12m_res),
        col=col2,
        help=METRIC_HELPS["lucro_12m"],
    )
    render_metric_card(
        "Lucro Líquido 3 Meses",
        fmt_money(lucro_3m_res),
        col=col2,
        help=METRIC_HELPS["lucro_3m"],
    )

st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)

# Graham Fair Value Section
st.markdown(
    '<h3 class="stSubheader">💎 Valor Justo segundo Graham</h3>',
    unsafe_allow_html=True,
)

vpa_f = get_stock_data_val("vpa")
lpa_f = get_stock_data_val("lpa")
prc_f = get_stock_data_val("cotacao")
lucro_f = get_stock_data_val("lucro_liquido_12m")

if vpa_f is None or lpa_f is None or prc_f is None:
    st.markdown(
        """
    <div class="graham-card graham-negative">
        <div class="graham-title">⚠️ Dados Indisponíveis</div>
        <div class="graham-text">Não há dados suficientes de VPA, LPA ou Cotação para realizar o cálculo de Graham.</div>
    </div>
    """,
        unsafe_allow_html=True,
    )
elif vpa_f <= 0 or lpa_f <= 0:
    st.markdown(
        f"""
    <div class="graham-card graham-negative">
        <div class="graham-title">⚠️ Empresa em Prejuízo ou PL Negativo</div>
        <div class="graham-text">A empresa nos últimos 12 meses teve um Lucro Líquido de <span class="graham-highlight">{fmt_money(lucro_f)}</span>.</div>
        <div class="graham-text">Obs.: Com VPA (<span class="graham-highlight">{vpa_f:.2f}</span>) ou LPA (<span class="graham-highlight">{lpa_f:.2f}</span>) negativos, não é possível calcular o valor justo segundo a metodologia clássica de Benjamin Graham.</div>
        <div class="graham-text" style="font-weight: 600; margin-top: 10px;">👉 Busque por outra empresa estável.</div>
    </div>
    """,
        unsafe_allow_html=True,
    )
else:
    # Clean price value robustly to handle potential string formatting (e.g. "R$ 16.40")
    prc_cleaned = (
        str(prc_f).replace("R$", "").replace(" ", "").replace(",", ".").strip()
    )
    try:
        prc_f2 = float(prc_cleaned)
    except ValueError:
        prc_f2 = 0.0

    # Graham calculations:
    valor_gh = round(graham_constant * vpa_f * lpa_f, 2)
    valor_jt = round(math.sqrt(valor_gh), 2)

    # Upside / Downside:
    up_dw = round(((prc_f2 / valor_jt) - 1) * 100, 2)

    if up_dw > 0:
        card_class = "graham-negative"
        indicator_icon = "📈"
        desc_text = f'A ação está com o preço atual de mercado <span class="graham-highlight" style="color:#EF4444">{up_dw:.2f}% acima</span> de seu valor justo calculado (usando constante {graham_constant:.1f}).'
    else:
        card_class = "graham-positive"
        indicator_icon = "📉"
        desc_text = f'A ação está com o preço atual de mercado <span class="graham-highlight" style="color:#10B981">{abs(up_dw):.2f}% abaixo</span> (desconto) de seu valor justo calculado (usando constante {graham_constant:.1f}).'

    margem_color = "#EF4444" if up_dw > 0 else "#10B981"
    margem_prefix = "+" if up_dw <= 0 else ""
    st.markdown(
        f"""
    <div class="graham-card {card_class}">
        <div class="graham-title">{indicator_icon} Valuation de Graham (Constante {graham_constant:.1f})</div>
        <div class="graham-text" style="margin-bottom: 16px; font-size: 13.5px;">Cálculo clássico de Benjamin Graham de margem de segurança e valor intrínseco.</div>
        <div class="graham-values-row">
            <div class="graham-value-box">
                <div class="graham-value-box-label">Valor Justo (V.J.)</div>
                <div class="graham-value-box-number" style="color: #10B981">R$ {valor_jt:.2f}</div>
            </div>
            <div class="graham-value-box">
                <div class="graham-value-box-label">Preço Atual</div>
                <div class="graham-value-box-number" style="color: #E2E8F0">R$ {prc_f2:.2f}</div>
            </div>
            <div class="graham-value-box">
                <div class="graham-value-box-label">Margem Relativa</div>
                <div class="graham-value-box-number" style="color: {margem_color}">{margem_prefix}{up_dw:.2f}%</div>
            </div>
        </div>
        <div class="graham-text" style="margin-top: 14px; font-size: 14px; color: #94A3B8;">{desc_text}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    try:
        import pathlib

        from b3_reports.charts import plot_graham_bar

        dash_images_dir = pathlib.Path("./Api/relatorios/images")
        dash_images_dir.mkdir(parents=True, exist_ok=True)
        graham_img_path = (
            dash_images_dir / f"graham_{col1_selection.lower()}_dashboard.png"
        )
        plot_graham_bar(col1_selection, prc_f2, valor_jt, graham_img_path)
        st.image(str(graham_img_path), use_column_width=True)
    except Exception:
        pass

st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)

# Relevant Facts, Proventos, and Trimestrais (organized nicely in tabs)
tab_facts, tab_proventos, tab_trimestres = st.tabs(
    [
        "⏰ Fatos Relevantes",
        "💵 Histórico de Proventos",
        "📋 Dados Trimestrais (Releases)",
    ]
)

with tab_facts:
    fr_path = f"./Api/fatos_relevantes/{col1_selection}.csv"
    if os.path.exists(fr_path):
        try:
            fr_df = pd.read_csv(fr_path, sep=";")
            fr_df_1 = fr_df[["Data", "Hora", "Descrição", "Link"]]
            st.caption(f"Fatos Relevantes Recentes para {col1_selection}")
            st.dataframe(fr_df_1, use_container_width=True)

            if not fr_df_1.empty:
                fr_df_data = fr_df_1["Data"].iloc[0]
                fr_df_link = fr_df_1["Link"].iloc[0]
                st.markdown(
                    f"**Último fato relevante registrado em {fr_df_data}:** [Download do Relatório]({fr_df_link})"
                )
        except Exception:
            st.write("Erro ao carregar os dados de Fatos Relevantes.")
    else:
        st.write("Sem fatos relevantes registrados para esta ação.")

with tab_proventos:
    pr_path = f"./Api/proventos/{col1_selection}.csv"
    if os.path.exists(pr_path):
        try:
            pr_df = pd.read_csv(pr_path, sep=";")
            pr_df_1 = pr_df[
                ["Data", "Valor", "Tipo", "Data de Pagamento", "Por quantas ações"]
            ]
            st.caption("💵 Distribuição de Proventos Recentes")
            st.caption(
                '*A data de referência é a "data com" (direito de receber o provento).'
            )
            st.dataframe(pr_df_1, use_container_width=True)
        except Exception:
            st.write("Erro ao processar proventos.")
    else:
        st.write("💵 Sem proventos registrados para este ativo.")

with tab_trimestres:
    tri_path = f"./Api/trimestre/{col1_selection}.csv"
    if os.path.exists(tri_path):
        try:
            tri_df = pd.read_csv(tri_path, sep=";")
            tri_df_1 = tri_df[
                ["Data Referência", "Demonstração Financeira", "Release de Resultados"]
            ]
            st.caption("Demonstrações e Resultados Trimestrais")
            st.dataframe(tri_df_1, use_container_width=True)

            if not tri_df_1.empty:
                tri_ref = tri_df_1["Data Referência"].iloc[0]
                tri_rel = tri_df_1["Release de Resultados"].iloc[0]
                st.markdown(
                    f"📝 **Último Release de Resultados (Referência {tri_ref}):** [Baixar Release]({tri_rel})"
                )
        except Exception:
            st.write("Erro ao carregar dados trimestrais.")
    else:
        st.write("Dados trimestrais indisponíveis.")

st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)

# Charts Section
st.markdown(
    '<h3 class="stSubheader">📊 Análise Visual do Histórico</h3>',
    unsafe_allow_html=True,
)

# Load prices history (already initialized at the top)
pass

# --- CHART RENDERING (always runs when prices_loaded is True) ---
if prices_loaded:
    # 1. Price History Line Chart
    st.write(f"📈 Histórico de Fechamento - **{col1_selection}**")

    if is_contingency:
        st.markdown(
            """
            <div class="status-card status-alert" style="margin-bottom: 15px; padding: 10px 14px;">
                <div class="status-title" style="font-size: 13px; font-weight: 600; color: #EF4444; margin-bottom: 2px;">
                    ⚠️ Modo de Contingência Ativo
                </div>
                <div class="status-body" style="font-size: 12px; color: #94A3B8; font-family: Outfit, sans-serif;">
                    Não foi possível conectar ao Yahoo Finance devido a restrições temporárias de rede local/DNS.
                    Exibindo estimativa de cotação histórica baseada no último fechamento consolidado.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    tab_plotly, tab_matplotlib = st.tabs(
        ["📊 Gráfico Interativo (Plotly)", "🎨 Gráfico de Publicação (Matplotlib)"]
    )

    with tab_plotly:
        fig_pre = px.line(precos_df_clean, x="Date", y=f"{col1_selection}")
        apply_plotly_theme(
            fig_pre,
            f"Histórico de Fechamento ({col1_selection})",
            "Preço de Fechamento (R$)",
        )
        st.plotly_chart(fig_pre, use_container_width=True)

    with tab_matplotlib:
        try:
            import pathlib

            from b3_reports.charts import plot_stock_history

            dash_images_dir = pathlib.Path("./Api/relatorios/images")
            dash_images_dir.mkdir(parents=True, exist_ok=True)
            hist_img_path = (
                dash_images_dir / f"history_{col1_selection.lower()}_dashboard.png"
            )

            # Convierte las columnas Date y el precio a listas para pasar a plot_stock_history
            dates_list = (
                pd.to_datetime(precos_df_clean["Date"]).dt.strftime("%Y-%m-%d").tolist()
            )
            prices_list = precos_df_clean[f"{col1_selection}"].astype(float).tolist()

            plot_stock_history(col1_selection, dates_list, prices_list, hist_img_path)
            st.image(str(hist_img_path), use_column_width=True)
        except Exception:
            st.write("Erro ao processar o gráfico de publicação.")

    # 2. Monthly Returns Matrix/Table
    st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)
    st.write(f"✳️ Retornos Mensais Históricos - **{col1_selection}**")
    hist_path = f"./Api/historico/{col1_selection}.csv"
    if os.path.exists(hist_path):
        try:
            tb_df = pd.read_csv(hist_path, sep=";", index_col=[0])
            # Diverging color palette: red/rose for negative, green for positive
            cm = sb.diverging_palette(12, 135, sep=10, as_cmap=True)
            st.dataframe(
                tb_df.style.background_gradient(cmap=cm, axis=None).format(
                    "{:.2f}%", na_rep="-"
                ),
                use_container_width=True,
            )
        except Exception:
            st.write("Erro ao carregar matriz de retornos mensais.")
    else:
        st.write("Matriz de retornos mensais indisponível.")

    # 3. Daily Returns
    st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)
    st.write(f"⌛ Retornos Diários - **{col1_selection}**")
    try:
        # Calculate daily change percent
        precos_df_ret = precos_df_clean[f"{col1_selection}"].pct_change()
        precos_df_clean[f"Ret {col1_selection}"] = precos_df_ret
        fig_ret = px.line(precos_df_clean, x="Date", y=f"Ret {col1_selection}")
        apply_plotly_theme(
            fig_ret, f"Retornos Diários ({col1_selection})", "Retorno Diário (%)"
        )
        st.plotly_chart(fig_ret, use_container_width=True)
    except Exception:
        st.write("Erro ao calcular retornos diários.")

    # 4. Cumulative Returns
    st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)
    st.write(f"⌛ Retornos Acumulados - **{col1_selection}**")
    try:
        df_ret_ac = precos_df_clean.copy()
        if "tret" not in df_ret_ac.columns and "ret" in df_ret_ac.columns:
            df_ret_ac["tret"] = df_ret_ac["ret"].cumsum()
        fig_ret_ac = px.line(df_ret_ac, x="Date", y="tret")
        apply_plotly_theme(
            fig_ret_ac,
            f"Retorno Acumulado % ({col1_selection})",
            "Retorno Acumulado (%)",
        )
        st.plotly_chart(fig_ret_ac, use_container_width=True)
    except Exception:
        st.write("Erro ao renderizar retornos acumulados.")

    # 5. Volatility (30 days)
    st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)
    st.write(f"🔥 Volatilidade Móvel (30 Dias) - **{col1_selection}**")
    try:
        precos_df_vol = (
            precos_df_clean[f"Ret {col1_selection}"].rolling(window=30).std()
        )
    except Exception:
        precos_df_vol = None

    if precos_df_vol is not None:
        precos_df_clean[f"Vol {col1_selection}"] = precos_df_vol
        fig_vol = px.line(precos_df_clean, x="Date", y=f"Vol {col1_selection}")
        apply_plotly_theme(
            fig_vol,
            f"Volatilidade (Janela de 30 Dias) - {col1_selection}",
            "Volatilidade (%)",
        )
        st.plotly_chart(fig_vol, use_container_width=True)

    # 6. Sector Correlation (Matplotlib Heatmap)
    st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)
    st.write("🧬 Correlação Multidimensional de Indicadores no Setor")
    try:
        import pathlib

        from b3_reports.charts import plot_correlation_heatmap

        # Filtra empresas do mesmo setor
        empresa_setor = get_stock_data_val("setor")
        df_setor = df[df["setor"] == empresa_setor]

        # Seleciona indicadores numéricos viáveis
        df_corr_input = df_setor[["pl", "pvp", "div_yield", "roe", "roic"]].dropna()
        if len(df_corr_input) > 1:
            correlations_df = df_corr_input.corr()
            dash_images_dir = pathlib.Path("./Api/relatorios/images")
            dash_images_dir.mkdir(parents=True, exist_ok=True)
            heatmap_img_path = dash_images_dir / "correlation_heatmap_dashboard.png"

            plot_correlation_heatmap(correlations_df, heatmap_img_path)
            st.image(str(heatmap_img_path), use_column_width=True)
        else:
            st.write("Dados insuficientes no setor para traçar a correlação térmica.")
    except Exception:
        st.write("Erro ao processar matriz de correlação térmica.")
else:
    st.write("Dados de preços históricos indisponíveis para gráficos.")

# Retornos Acumulados moved to the top


# Daily Updates Section
st.markdown(
    '<h3 class="stSubheader">⚡ Atualizações Diárias do Sistema</h3>',
    unsafe_allow_html=True,
)

date_att = datetime.today()
atraso = timedelta(1)
date_atual = date_att - atraso
date_atual_m = date_atual.strftime("%d/%m/%Y")
st.markdown(f"**Situação e Fechamento Geral do Dia: {date_atual_m}**")

col_att1, col_att2, col_att3 = st.columns(3)

with col_att1:
    st.markdown("📰 **Fatos Relevantes:**")
    try:
        df_analisar_ft = load_parquet_data("./Todos/FT.parquet.gzip")
        df_date_ft = df_analisar_ft.loc[
            df_analisar_ft["Data"] == date_atual_m, ["Acao", "Link"]
        ]
        if not df_date_ft.empty:
            acoes = ", ".join(list(df_date_ft["Acao"].unique()))
            render_status_card("Novos Relatórios", acoes, type="success")
        else:
            render_status_card("Status", "Nenhuma novidade hoje 🤫", type="neutral")
    except Exception:
        render_status_card("Status", "Erro ao carregar dados", type="alert")

with col_att2:
    st.markdown("💰 **Proventos Anunciados:**")
    try:
        df_analisar_pr = load_parquet_data("./Todos/PR.parquet.gzip")
        df_date_pr = df_analisar_pr.loc[
            df_analisar_pr["Data"] == date_atual_m, ["Acao"]
        ]
        if not df_date_pr.empty:
            acoes = ", ".join(list(df_date_pr["Acao"].unique()))
            render_status_card("Dividendos/JCP", acoes, type="success")
        else:
            render_status_card("Status", "Nenhum provento anunciado 🤫", type="neutral")
    except Exception:
        render_status_card("Status", "Erro ao carregar proventos", type="alert")

with col_att3:
    st.markdown("📋 **Releases de Resultados:**")
    try:
        df_analisar_tr = load_parquet_data("./Todos/TR.parquet.gzip")
        df_date_tr = df_analisar_tr.loc[
            df_analisar_tr["Data Referência"] == date_atual_m, ["Acao"]
        ]
        if not df_date_tr.empty:
            acoes = ", ".join(list(df_date_tr["Acao"].unique()))
            render_status_card("Releases Trimestrais", acoes, type="success")
        else:
            render_status_card("Status", "Nenhum release hoje 🤫", type="neutral")
    except Exception:
        render_status_card("Status", "Erro ao carregar releases", type="alert")

# Footer
st.markdown(
    """
    <div class="footer-container">
        <div class="footer-divider"></div>
        <div class="footer-brand">⚡ NEO-B3 <span>OBSIDIAN</span> | Plataforma Analítica Premium</div>
        <div class="footer-copy">© 2026 Lucas Alves. Dados integrados e estruturados com APIs B3 e Scrapers de alta integridade.</div>
    </div>
    """,
    unsafe_allow_html=True,
)
