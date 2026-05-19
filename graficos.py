import matplotlib
matplotlib.use("Agg")  # Backend sin GUI — obligatorio para Streamlit
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd
import numpy as np

PALETTE_CHURN = {
    "No": "#4C9BE8",
    "Yes": "#E85C4C"
}

STYLE = "whitegrid"


def _estilo():
    sns.set_theme(style=STYLE, font_scale=1.0)
    plt.rcParams["axes.spines.top"] = False
    plt.rcParams["axes.spines.right"] = False


# ─── HISTOGRAMA POR GRUPOS ────────────────────────────────────────────────────

def histograma_con_grupos(df: pd.DataFrame, columna: str):
    _estilo()
    fig, ax = plt.subplots(figsize=(8, 4))

    colores = {"Yes": "#E85C4C", "No": "#4C9BE8"}

    for churn, color in colores.items():
        subset = df[df["Churn"] == churn][columna].dropna()
        ax.hist(subset, bins=30, alpha=0.55, color=color, label=f"Churn {churn}")

    ax.set_title(f"Distribución de {columna} por Churn")
    ax.set_xlabel(columna)
    ax.set_ylabel("Frecuencia")
    ax.legend()
    plt.tight_layout()
    return fig


# ─── BOXPLOT ──────────────────────────────────────────────────────────────────

def boxplot_por_churn(df: pd.DataFrame, columna: str):
    _estilo()
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.boxplot(
        data=df,
        x="Churn",
        y=columna,
        palette=PALETTE_CHURN,
        ax=ax
    )
    ax.set_title(f"{columna} según Churn")
    plt.tight_layout()
    return fig


# ─── VIOLINPLOT ───────────────────────────────────────────────────────────────

def violinplot_por_churn(df: pd.DataFrame, columna: str):
    _estilo()
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.violinplot(
        data=df,
        x="Churn",
        y=columna,
        palette=PALETTE_CHURN,
        ax=ax
    )
    ax.set_title(f"{columna} según Churn")
    plt.tight_layout()
    return fig


# ─── BARRAS TASA CHURN ────────────────────────────────────────────────────────

def barras_tasa_churn(df: pd.DataFrame, columna: str):
    _estilo()

    tasa = (
        df.groupby(columna)["Churn"]
        .apply(lambda x: (x == "Yes").mean() * 100)
        .round(1)
        .reset_index()
    )
    tasa.columns = [columna, "Tasa Churn"]

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(
        data=tasa,
        x=columna,
        y="Tasa Churn",
        ax=ax,
        color="#E85C4C"
    )

    # Etiquetas encima de cada barra
    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f%%", padding=3)

    ax.set_title(f"Tasa de churn por {columna}")
    ax.set_ylabel("Tasa de churn (%)")
    ax.tick_params(axis="x", rotation=20)
    plt.tight_layout()
    return fig


# ─── BARRAS APILADAS ──────────────────────────────────────────────────────────

def barras_apiladas(df: pd.DataFrame, columna: str):
    _estilo()

    tabla = pd.crosstab(df[columna], df["Churn"], normalize="index") * 100

    # Asegurar que las columnas estén en orden correcto (No, Yes)
    for col in ["No", "Yes"]:
        if col not in tabla.columns:
            tabla[col] = 0
    tabla = tabla[["No", "Yes"]]

    fig, ax = plt.subplots(figsize=(8, 4))
    tabla.plot(
        kind="bar",
        stacked=True,
        color=[PALETTE_CHURN["No"], PALETTE_CHURN["Yes"]],
        ax=ax,
        legend=True
    )

    ax.set_title(f"{columna} vs Churn (proporcional)")
    ax.yaxis.set_major_formatter(mticker.PercentFormatter())
    ax.legend(title="Churn", loc="upper right")
    plt.xticks(rotation=25)
    plt.tight_layout()
    return fig


# ─── HEATMAP CORRELACIÓN ──────────────────────────────────────────────────────

def heatmap_correlacion(df: pd.DataFrame):
    _estilo()

    numericas = df.select_dtypes(include=np.number)
    corr = numericas.corr()

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    ax.set_title("Matriz de correlación")
    plt.tight_layout()
    return fig