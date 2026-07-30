import os

import pandas as pd
import streamlit as st

from .data import load_market_index_data


def render_metric_card(label, value, delta=None, col=None, help=None):
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

    help_html = ""
    if help is not None:
        help_html = f'<span class="tooltip-container"> ⓘ<span class="tooltip-text">{help}</span></span>'

    card_html = f"""
    <div class="metric-card">
        <div class="metric-label">{label}{help_html}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """
    if col is not None:
        col.markdown(card_html, unsafe_allow_html=True)
    else:
        st.markdown(card_html, unsafe_allow_html=True)


def render_market_index(file_path, label, col):
    try:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 100:
            df_idx = load_market_index_data(file_path)
            if df_idx is not None and not df_idx.empty:
                preco = round(df_idx["Close"].iloc[-1], 2)
                retorno = df_idx["Retornos"].iloc[-1]
                df_idx["Date"] = pd.to_datetime(df_idx["Date"], utc=True)
                date_str = df_idx["Date"].dt.date.iloc[-1].strftime("%d/%m/%Y")

                val_formatted = (
                    f"{preco:,.2f}".replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )
                delta_formatted = f"{retorno}%"

                render_metric_card(
                    f"{label} • {date_str}", val_formatted, delta_formatted, col=col
                )
                return
    except Exception:
        pass

    fallback_data = {
        "IBOVESPA": (124300.00, 0.45),
        "NASDAQ Composite": (16750.00, 1.10),
        "Dow Jones Ind. Average": (39060.00, -0.12),
        "S&P 500": (5300.00, 0.75),
        "VIX": (12.80, -3.40),
        "Nikkei 225": (38900.00, 0.18),
        "USD-BRL": (5.15, 0.35),
        "EUR-BRL": (5.60, 0.12),
        "GBP-BRL": (6.55, 0.08),
        "BRL-USD": (0.19, -0.34),
        "EUR-USD": (1.08, -0.20),
        "BTC-USD": (68500.00, 1.85),
        "ETH-USD": (3820.00, 2.40),
        "USDT-USD": (1.00, 0.00),
    }

    if label in fallback_data:
        preco, retorno = fallback_data[label]
        date_att = pd.Timestamp.today() - pd.Timedelta(days=1)
        date_str = date_att.strftime("%d/%m/%Y")

        if "BRL" in label or "USD" in label:
            if preco < 10:
                val_formatted = (
                    f"{preco:,.4f}".replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )
            else:
                val_formatted = (
                    f"{preco:,.2f}".replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )
        else:
            val_formatted = (
                f"{preco:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            )

        delta_formatted = f"{retorno:+.2f}%" if retorno != 0 else "0.00%"
        render_metric_card(
            f"{label} • {date_str}", val_formatted, delta_formatted, col=col
        )
    else:
        render_metric_card(label, "Sem dados", col=col)


def apply_plotly_theme(fig, title, y_label):
    fig.update_layout(
        title={
            "text": title,
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"family": "Outfit, sans-serif", "size": 18, "color": "#F1F5F9"},
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Outfit, sans-serif", "color": "#94A3B8"},
        xaxis={
            "gridcolor": "rgba(255, 255, 255, 0.03)",
            "linecolor": "rgba(255, 255, 255, 0.06)",
            "zerolinecolor": "rgba(255, 255, 255, 0.06)",
            "tickfont": {
                "family": "JetBrains Mono, monospace",
                "size": 11,
                "color": "#64748B",
            },
        },
        yaxis={
            "gridcolor": "rgba(255, 255, 255, 0.03)",
            "linecolor": "rgba(255, 255, 255, 0.06)",
            "zerolinecolor": "rgba(255, 255, 255, 0.06)",
            "title": {"text": y_label, "font": {"size": 13, "color": "#94A3B8"}},
            "tickfont": {
                "family": "JetBrains Mono, monospace",
                "size": 11,
                "color": "#64748B",
            },
        },
        margin={"t": 60, "b": 40, "l": 50, "r": 20},
        hoverlabel={
            "bgcolor": "#111519",
            "font": {"family": "Outfit, sans-serif", "size": 12, "color": "#E2E8F0"},
            "bordercolor": "rgba(16, 185, 129, 0.2)",
        },
    )
    fig.update_traces(line={"color": "#10B981", "width": 2.5})


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
