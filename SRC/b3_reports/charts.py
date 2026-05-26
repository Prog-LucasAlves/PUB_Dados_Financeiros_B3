import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Caminho base do módulo
BASE_DIR = pathlib.Path(__file__).parent.resolve()


def setup_obsidian_dark_theme():
    """
    Configura rcParams globais do Matplotlib para o tema Dark Obsidian do projeto.
    """
    plt.rcParams["figure.facecolor"] = "#0D0F12"
    plt.rcParams["axes.facecolor"] = "#161A1F"
    plt.rcParams["axes.edgecolor"] = (1.0, 1.0, 1.0, 0.08)
    plt.rcParams["text.color"] = "#E2E8F0"
    plt.rcParams["axes.labelcolor"] = "#94A3B8"
    plt.rcParams["xtick.color"] = "#94A3B8"
    plt.rcParams["ytick.color"] = "#94A3B8"
    plt.rcParams["grid.color"] = (1.0, 1.0, 1.0, 0.03)
    plt.rcParams["grid.alpha"] = 0.3
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.size"] = 10


def plot_stock_history(ticker: str, dates: list, prices: list, out_path: pathlib.Path):
    """
    Gera um gráfico de linha do histórico de cotações com preenchimento gradiente.
    """
    setup_obsidian_dark_theme()
    fig, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)

    # Plota a linha de fechamento com cor verde brilhante B3 accent
    ax.plot(dates, prices, color="#00E676", linewidth=2.5, label="Fechamento")

    # Preenchimento sombreado sob a curva
    ax.fill_between(dates, prices, color="#00E676", alpha=0.08)

    # Customizações
    ax.set_title(
        f"Histórico de Cotações - {ticker}", fontsize=14, fontweight="bold", pad=15
    )
    ax.set_xlabel("Data")
    ax.set_ylabel("Preço (R$)")
    ax.grid(True)
    ax.legend(framealpha=0.1, loc="upper left")

    # Garante diretórios
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Salva em alta resolução
    fig.savefig(out_path, dpi=300, facecolor="#0D0F12", edgecolor="none")
    plt.close(fig)
    print(f"[OK] Gráfico histórico de {ticker} salvo em {out_path.name}")


def plot_graham_bar(
    ticker: str, current_price: float, graham_price: float, out_path: pathlib.Path
):
    """
    Gera um gráfico de barras comparando o preço atual de mercado com o Valor Justo de Graham.
    """
    setup_obsidian_dark_theme()
    fig, ax = plt.subplots(figsize=(8, 4), constrained_layout=True)

    categories = ["Cotação Atual", "Valor Justo (Graham)"]
    values = [current_price, graham_price]
    colors = ["#94A3B8", "#00E676" if graham_price >= current_price else "#FF3D71"]

    bars = ax.barh(
        categories, values, color=colors, edgecolor=(1.0, 1.0, 1.0, 0.05), height=0.5
    )

    # Adiciona os rótulos de valores nas pontas das barras
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + (width * 0.02),
            bar.get_y() + bar.get_height() / 2,
            f"R$ {width:.2f}",
            va="center",
            ha="left",
            fontweight="bold",
            color="#F8FAFC",
        )

    # Customizações
    ax.set_title(
        f"Valuation Graham vs Mercado - {ticker}",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )
    ax.set_xlabel("Valor (R$)")

    # Remove as bordas desnecessárias
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)

    ax.grid(axis="x")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=300, facecolor="#0D0F12", edgecolor="none")
    plt.close(fig)
    print(f"[OK] Gráfico Graham de {ticker} salvo em {out_path.name}")


def plot_correlation_heatmap(df_correlations: pd.DataFrame, out_path: pathlib.Path):
    """
    Gera uma matriz térmica de correlação entre os múltiplos financeiros das empresas.
    """
    setup_obsidian_dark_theme()
    fig, ax = plt.subplots(figsize=(10, 8), constrained_layout=True)

    # Renderiza o Heatmap usando um colormap divergente elegante
    im = ax.imshow(df_correlations.values, cmap="coolwarm", vmin=-1, vmax=1)

    # Adiciona a colorbar
    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.ax.tick_params(labelsize=9)

    # Customização de labels
    columns = list(df_correlations.columns)
    ax.set_xticks(np.arange(len(columns)))
    ax.set_yticks(np.arange(len(columns)))
    ax.set_xticklabels(columns, rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels(columns, fontsize=9)

    # Escreve os coeficientes numéricos dentro da matriz
    for i in range(len(columns)):
        for j in range(len(columns)):
            val = df_correlations.values[i, j]
            color = "#0D0F12" if abs(val) > 0.5 else "#F8FAFC"
            ax.text(
                j,
                i,
                f"{val:.2f}",
                ha="center",
                va="center",
                color=color,
                fontsize=8,
                fontweight="bold",
            )

    ax.set_title(
        "Matriz de Correlação - Indicadores de Valuation B3",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=300, facecolor="#0D0F12", edgecolor="none")
    plt.close(fig)
    print(f"[OK] Matriz de correlação salva em {out_path.name}")
