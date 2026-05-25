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

st.set_option("deprecation.showPyplotGlobalUse", False)
st.set_page_config(
    page_title="Neo-B3 Obsidian | Painel Financeiro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# 1. CSS STYLING INJECTION (Neo-B3 Obsidian Theme)
def inject_custom_css():
    st.markdown(
        """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500;700&display=swap');

    /* Global styles */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0D0F12 !important;
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #E2E8F0 !important;
    }

    /* Main container background */
    [data-testid="stHeader"] {
        background-color: #0D0F12 !important;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #111418 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }

    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h3 {
        color: #00E676 !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        color: #E2E8F0 !important;
        font-weight: 600 !important;
    }

    .stSubheader {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: #F8FAFC !important;
        border-left: 4px solid #00E676;
        padding-left: 12px;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }

    /* Tab buttons */
    button[data-baseweb="tab"] {
        font-family: 'Outfit', sans-serif !important;
        font-size: 16px !important;
        color: #94A3B8 !important;
        background-color: transparent !important;
        border: none !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease !important;
    }
    button[data-baseweb="tab"]:hover {
        color: #E2E8F0 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #00E676 !important;
        border-bottom: 2px solid #00E676 !important;
        font-weight: 600 !important;
    }

    /* Custom metric card wrapper */
    .metric-card {
        background-color: #161A1F;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        margin-bottom: 16px;
        transition: all 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(0, 230, 118, 0.2);
        box-shadow: 0 6px 16px rgba(0, 230, 118, 0.05);
    }
    .metric-label {
        font-size: 12px;
        color: #94A3B8;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
        font-family: 'Outfit', sans-serif;
    }
    .metric-value {
        font-size: 24px;
        color: #F8FAFC;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }
    .metric-delta {
        font-size: 13px;
        font-weight: 600;
        margin-top: 6px;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }
    .delta-positive {
        color: #00E676;
    }
    .delta-negative {
        color: #FF3D71;
    }

    /* Graham Fair Value Card */
    .graham-card {
        background: linear-gradient(135deg, #161A1F 0%, #111418 100%);
        border-radius: 16px;
        padding: 24px;
        margin: 20px 0;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
    }
    .graham-card:hover {
        box-shadow: 0 10px 28px rgba(0, 230, 118, 0.05);
    }
    .graham-positive {
        border-left: 6px solid #00E676;
    }
    .graham-negative {
        border-left: 6px solid #FF3D71;
    }

    .graham-title {
        font-size: 18px;
        font-weight: 600;
        color: #E2E8F0;
        margin-bottom: 12px;
        font-family: 'Outfit', sans-serif;
    }
    .graham-text {
        font-size: 15px;
        color: #94A3B8;
        line-height: 1.6;
        margin-bottom: 8px;
    }
    .graham-highlight {
        font-weight: 700;
        color: #F8FAFC;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Custom divider line */
    .custom-hr {
        height: 1px;
        background: linear-gradient(90deg, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 0.05) 50%, rgba(255, 255, 255, 0) 100%);
        border: none;
        margin: 2.5rem 0;
    }

    /* Tables styling */
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        background-color: #161A1F !important;
        padding: 6px;
    }

    /* Streamlit overrides for better premium integration */
    [data-testid="stLinkButton"] a {
        background-color: #161A1F !important;
        color: #00E676 !important;
        border: 1px solid rgba(0, 230, 118, 0.3) !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stLinkButton"] a:hover {
        background-color: rgba(0, 230, 118, 0.1) !important;
        border-color: #00E676 !important;
        box-shadow: 0 0 10px rgba(0, 230, 118, 0.2) !important;
    }

    .stAlert {
        background-color: #161A1F !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
    }

    /* Scrollbars */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0D0F12;
    }
    ::-webkit-scrollbar-thumb {
        background: #1C232B;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #2D3748;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


# 2. UTILITY RENDER FUNCTIONS
def render_metric_card(label, value, delta=None, col=None):
    delta_html = ""
    if delta is not None:
        delta_str = str(delta).strip()
        is_positive = (
            not delta_str.startswith("-")
            and delta_str != "0"
            and delta_str != "0%"
            and delta_str != "0.0%"
            and delta_str != "0.00%"
        )
        class_name = "delta-positive" if is_positive else "delta-negative"
        arrow = "▲" if is_positive else "▼"
        delta_html = f'<div class="metric-delta {class_name}">{arrow} {delta_str}</div>'

    card_html = f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """
    if col is not None:
        col.markdown(card_html, unsafe_allow_html=True)
    else:
        st.markdown(card_html, unsafe_allow_html=True)


def render_market_index(file_path, label, col):
    if not os.path.exists(file_path):
        render_metric_card(label, "Sem dados", col=col)
        return
    try:
        df_idx = pd.read_csv(file_path, sep=";")
        preco = round(df_idx["Close"].iloc[-1], 2)
        retorno = df_idx["Retornos"].iloc[-1]
        df_idx["Date"] = pd.to_datetime(df_idx["Date"], utc=True)
        date_str = df_idx["Date"].dt.date.iloc[-1].strftime("%d/%m/%Y")

        val_formatted = (
            f"{preco:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )
        delta_formatted = f"{retorno}%"

        render_metric_card(
            f"{label} • {date_str}", val_formatted, delta_formatted, col=col
        )
    except Exception:
        render_metric_card(label, "Erro ao carregar", col=col)


def apply_plotly_theme(fig, title, y_label):
    fig.update_layout(
        title={
            "text": title,
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"family": "Outfit, sans-serif", "size": 18, "color": "#E2E8F0"},
        },
        paper_bgcolor="#0D0F12",
        plot_bgcolor="#161A1F",
        font={"family": "Outfit, sans-serif", "color": "#94A3B8"},
        xaxis={
            "gridcolor": "rgba(255, 255, 255, 0.03)",
            "linecolor": "rgba(255, 255, 255, 0.08)",
            "zerolinecolor": "rgba(255, 255, 255, 0.08)",
            "tickfont": {"family": "JetBrains Mono, monospace", "size": 11},
        },
        yaxis={
            "gridcolor": "rgba(255, 255, 255, 0.03)",
            "linecolor": "rgba(255, 255, 255, 0.08)",
            "zerolinecolor": "rgba(255, 255, 255, 0.08)",
            "title": {"text": y_label, "font": {"size": 13, "color": "#94A3B8"}},
            "tickfont": {"family": "JetBrains Mono, monospace", "size": 11},
        },
        margin={"t": 60, "b": 40, "l": 50, "r": 20},
        hoverlabel={
            "bgcolor": "#161A1F",
            "font": {"family": "Outfit, sans-serif", "size": 12, "color": "#E2E8F0"},
            "bordercolor": "rgba(255, 255, 255, 0.1)",
        },
    )
    fig.update_traces(line={"color": "#00E676", "width": 2.5})


# Clean data formats
def fmt_money(value):
    try:
        val = float(value)
        return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return str(value)


def fmt_percent(value):
    try:
        val = float(value)
        return f"{val:.2f}%"
    except Exception:
        return str(value)


def fmt_decimal(value):
    try:
        val = float(value)
        return f"{val:.2f}"
    except Exception:
        return str(value)


# Inject visual styles
inject_custom_css()

# Header - Global Indices
st.markdown(
    '<div class="stSubheader">🌎 Alguns Índices Globais</div>', unsafe_allow_html=True
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
    '<div class="stSubheader">💵 Alguns Pares de Moedas</div>', unsafe_allow_html=True
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
    '<div class="stSubheader">🪙 Algumas Cryptomoedas</div>', unsafe_allow_html=True
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
    '<div class="stSubheader">ℹ️ Informações das Ações Listadas na B3</div>',
    unsafe_allow_html=True,
)

# Read base data
df = pd.read_csv("./Dados_Atual/dados.csv", sep=";")
ri = pd.read_csv("./Api/ri_empresas/ri_empresas.csv", sep=";")

# Sidebar stock selectbox
st.sidebar.header("Escolha sua ação")
col1_selection = st.sidebar.selectbox(
    "Papel",
    df.papel,
    list(df.papel).index("AALR3"),
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


# Helper function to get row safely and get column value
def get_stock_data_val(column_name):
    try:
        row = df[df["papel"] == col1_selection]
        if row.empty:
            return None
        idx = int(row["Unnamed: 0"].iloc[0])
        return row[column_name].loc[idx]
    except Exception:
        try:
            return df[df["papel"] == col1_selection][column_name].iloc[0]
        except Exception:
            return None


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
    nr_acoes_formatted = "N/A"
    if nr_acoes_res is not None:
        nr_acoes_formatted = re.sub(r"(?<!^)(?=(\d{3})+$)", r".", str(nr_acoes_res))

    render_metric_card("Tipo da Ação", tipo_res, col=col1)
    render_metric_card("Empresa", empresa_res, col=col2)
    render_metric_card("Data da Última Cotação", dt_ult_res, col=col1)
    render_metric_card(
        "Valor da Ação", fmt_money(cotacao_res), fmt_percent(os_dia_res), col=col2
    )
    render_metric_card("Máxima 52 Semanas", fmt_money(max_52_res), col=col1)
    render_metric_card("Mínima 52 Semanas", fmt_money(min_52_res), col=col2)
    render_metric_card("Volume Médio (2 meses)", fmt_money(vol_med_res), col=col1)
    render_metric_card("Valor de Mercado", fmt_money(val_merc_res), col=col2)
    render_metric_card("Valor da Firma", fmt_money(val_firma_res), col=col1)
    render_metric_card("Ações em Circulação", nr_acoes_formatted, col=col2)

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

    render_metric_card("Preço / Lucro (P/L)", fmt_decimal(pl_res), col=col1)
    render_metric_card("Lucro por Ação (LPA)", fmt_decimal(lpa_res), col=col2)
    render_metric_card("P/VP", fmt_decimal(pvp_res), col=col1)
    render_metric_card(
        "Valor Patrimonial por Ação (VPA)", fmt_decimal(vpa_res), col=col2
    )
    render_metric_card("P/EBIT", fmt_decimal(p_ebit_res), col=col1)
    render_metric_card("PSR", fmt_decimal(psr_res), col=col2)
    render_metric_card("P/Ativos", fmt_decimal(p_ativo_res), col=col1)
    render_metric_card("P/Capital Giro", fmt_decimal(p_cap_res), col=col2)
    render_metric_card("P/Ativo Circulante Líquido", fmt_decimal(p_circ_res), col=col1)
    render_metric_card("EV / EBITDA", fmt_decimal(ev_ebitda_res), col=col2)
    render_metric_card("EV / EBIT", fmt_decimal(ev_ebit_res), col=col1)

with tab_efficiency:
    col1, col2 = st.columns(2)

    m_bruta = get_stock_data_val("marg_bruta")
    m_ebit = get_stock_data_val("marg_ebit")
    m_liquida = get_stock_data_val("marg_liquida")
    ebit_ativo_res = get_stock_data_val("ebit_ativo")
    roic_res = get_stock_data_val("roic")
    roe_res = get_stock_data_val("roe")
    div_yield_res = get_stock_data_val("div_yield")

    render_metric_card("Margem Bruta", fmt_percent(m_bruta), col=col1)
    render_metric_card("Margem EBIT", fmt_percent(m_ebit), col=col2)
    render_metric_card("Margem Líquida", fmt_percent(m_liquida), col=col1)
    render_metric_card("EBIT / Ativo", fmt_decimal(ebit_ativo_res), col=col2)
    render_metric_card("ROIC", fmt_percent(roic_res), col=col1)
    render_metric_card("ROE", fmt_percent(roe_res), col=col2)
    render_metric_card("Dividend Yield", fmt_percent(div_yield_res), col=col1)

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

    render_metric_card("Liquidez Corrente", fmt_decimal(liquidez_corr_res), col=col1)
    render_metric_card(
        "Crescimento Receita Líquida (5a)", fmt_percent(cres_rec_res), col=col2
    )
    render_metric_card("Ativo Total", fmt_money(ativo_res), col=col1)
    render_metric_card("Disponibilidades", fmt_money(disponib_res), col=col2)
    render_metric_card("Ativo Circulante", fmt_money(ativo_circ_res), col=col1)
    render_metric_card("Patrimônio Líquido", fmt_money(patr_liq_res), col=col2)
    render_metric_card("Dívida Bruta", fmt_money(div_bruta_res), col=col1)
    render_metric_card("Dívida Líquida", fmt_money(div_liquida_res), col=col2)
    render_metric_card("Lucro Líquido 12 Meses", fmt_money(lucro_12m_res), col=col1)
    render_metric_card("Lucro Líquido 3 Meses", fmt_money(lucro_3m_res), col=col2)

st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)

# Graham Fair Value Section
st.markdown(
    '<div class="stSubheader">💎 Valor Justo segundo Graham</div>',
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
    prc_f1 = str(prc_f).replace(",", ".")
    prc_f2 = float(prc_f1)

    # Graham calculations:
    valor_gh = round(22.5 * vpa_f * lpa_f, 2)
    valor_jt = round(math.sqrt(valor_gh), 2)

    # Upside / Downside:
    up_dw = round(((prc_f2 / valor_jt) - 1) * 100, 2)

    if up_dw > 0:
        card_class = "graham-negative"
        indicator_icon = "📈"
        desc_text = f'A ação está com o preço atual de mercado <span class="graham-highlight" style="color:#FF3D71">{up_dw:.2f}% acima</span> de seu valor justo calculado.'
    else:
        card_class = "graham-positive"
        indicator_icon = "📉"
        desc_text = f'A ação está com o preço atual de mercado <span class="graham-highlight" style="color:#00E676">{abs(up_dw):.2f}% abaixo</span> (desconto) de seu valor justo calculado.'

    st.markdown(
        f"""
    <div class="graham-card {card_class}">
        <div class="graham-title">{indicator_icon} Análise de Valuation (Graham)</div>
        <div class="graham-text">Valor Justo Calculado: <span class="graham-highlight" style="font-size: 17px; color: #00E676">R$ {valor_jt:.2f}</span></div>
        <div class="graham-text">Cotação Atual de Mercado: <span class="graham-highlight" style="font-size: 17px;">R$ {prc_f2:.2f}</span></div>
        <div class="graham-text" style="margin-top: 12px; font-size: 15px;">{desc_text}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

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
    '<div class="stSubheader">📊 Análise Visual do Histórico</div>',
    unsafe_allow_html=True,
)

# Load prices history
precos_path = f"./Api/precos/{col1_selection}.csv"
prices_loaded = False
if os.path.exists(precos_path):
    try:
        precos_df = pd.read_csv(precos_path, sep=";")
        # Keep original columns mutation
        precos_df_ad = precos_df.rename(columns={"Close": f"{col1_selection}"})
        # Clean columns to preserve original logic
        precos_df_clean = precos_df_ad.drop(
            precos_df_ad.columns[[2, 3, 4, 6]], axis=1, errors="ignore"
        )
        prices_loaded = True
    except Exception:
        st.write("Erro ao carregar os dados históricos de preços.")

if prices_loaded:
    # 1. Price History Line Chart
    st.write(f"📈 Histórico de Fechamento - **{col1_selection}**")
    fig_pre = px.line(precos_df_clean, x="Date", y=f"{col1_selection}")
    apply_plotly_theme(
        fig_pre,
        f"Histórico de Fechamento ({col1_selection})",
        "Preço de Fechamento (R$)",
    )
    st.plotly_chart(fig_pre, use_container_width=True)

    # 2. Monthly Returns Matrix/Table
    st.write("-----------------------------------------")
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
    st.write("-----------------------------------------")
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
    st.write("-----------------------------------------")
    st.write(f"⌛ Retornos Acumulados - **{col1_selection}**")
    try:
        df_ret_ac = pd.read_csv(f"./Api/precos/{col1_selection}.csv", sep=";")
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
    st.write("-----------------------------------------")
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
else:
    st.write("Dados de preços históricos indisponíveis para gráficos.")

# Retorno Acumulado
st.write("-----------------------------------------")
st.markdown(
    '<div class="stSubheader">🎯 Retornos Acumulados da Ação</div>',
    unsafe_allow_html=True,
)
col1, col2, col3, col4 = st.columns(4)


def render_ret_acum(file_path, label, col):
    if not os.path.exists(file_path):
        render_metric_card(label, "Sem dados", col=col)
        return
    try:
        ret_df = pd.read_csv(file_path, sep=";")
        ret_filtered = ret_df[ret_df["Papel"] == col1_selection]
        if not ret_filtered.empty:
            idx = int(ret_filtered["Unnamed: 0"].iloc[0])
            val = ret_filtered["Total_Acumulado"].loc[idx]
            render_metric_card(label, fmt_percent(val), col=col)
        else:
            render_metric_card(label, "N/A", col=col)
    except Exception:
        render_metric_card(label, "Erro", col=col)


render_ret_acum("./Api/retornos/retornos_acumulados_15d.csv", "15 Dias", col1)
render_ret_acum("./Api/retornos/retornos_acumulados_30d.csv", "30 Dias", col2)
render_ret_acum("./Api/retornos/retornos_acumulados_45d.csv", "45 Dias", col3)
render_ret_acum("./Api/retornos/retornos_acumulados_60d.csv", "60 Dias", col4)

st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)

# Daily Updates Section
st.markdown(
    '<div class="stSubheader">⚡ Atualizações Diárias do Sistema</div>',
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
        df_analisar_ft = pd.read_parquet("./Todos/FT.parquet.gzip")
        df_date_ft = df_analisar_ft.loc[
            df_analisar_ft["Data"] == date_atual_m, ["Acao", "Link"]
        ]
        if not df_date_ft.empty:
            st.write(list(df_date_ft["Acao"].unique()))
        else:
            st.write("*Nenhuma novidade hoje* 🤫")
    except Exception:
        st.write("*Erro ao consultar fatos relevantes*")

with col_att2:
    st.markdown("💰 **Proventos Anunciados:**")
    try:
        df_analisar_pr = pd.read_parquet("./Todos/PR.parquet.gzip")
        df_date_pr = df_analisar_pr.loc[
            df_analisar_pr["Data"] == date_atual_m, ["Acao"]
        ]
        if not df_date_pr.empty:
            st.write(list(df_date_pr["Acao"].unique()))
        else:
            st.write("*Nenhum provento anunciado* 🤫")
    except Exception:
        st.write("*Erro ao consultar proventos*")

with col_att3:
    st.markdown("📋 **Releases de Resultados:**")
    try:
        df_analisar_tr = pd.read_parquet("./Todos/TR.parquet.gzip")
        df_date_tr = df_analisar_tr.loc[
            df_analisar_tr["Data Referência"] == date_atual_m, ["Acao"]
        ]
        if not df_date_tr.empty:
            st.write(list(df_date_tr["Acao"].unique()))
        else:
            st.write("*Nenhum release hoje* 🤫")
    except Exception:
        st.write("*Erro ao consultar releases*")

# Footer
st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; color: #94A3B8; font-size: 13px; font-family: Outfit; padding-bottom: 20px;'>"
    "⚡ Plataforma integrada com dados B3 | Desenvolvido no tema <b>Neo-B3 Obsidian</b> para melhor legibilidade"
    "</div>",
    unsafe_allow_html=True,
)
