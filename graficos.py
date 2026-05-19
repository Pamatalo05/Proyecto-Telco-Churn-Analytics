import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import pandas as pd
import numpy as np
 
PALETTE_CHURN = {"No": "#4C9BE8", "Yes": "#E85C4C"}
PALETTE_CAT   = "Blues_r"
STYLE         = "whitegrid"
 
def _estilo():
    sns.set_theme(style=STYLE, font_scale=1.05)
    plt.rcParams["axes.spines.top"]   = False
    plt.rcParams["axes.spines.right"] = False
 
 
def histograma_con_grupos(df, columna):

    fig, ax = plt.subplots(figsize=(8, 4))

    colores = {
        "Yes": "#E85C4C",
        "No": "#4C9BE8"
    }

    for churn, color in colores.items():

        subset = df[df["Churn"] == churn][columna].dropna()

        ax.hist(
            subset,
            bins=30,
            alpha=0.5,
            color=color,
            label=f"Churn {churn}"
        )

    ax.set_title(f"Distribución de {columna}")
    ax.set_xlabel(columna)
    ax.set_ylabel("Frecuencia")
    ax.legend()

    plt.tight_layout()

    return fig
 
 
def boxplot_por_churn(df: pd.DataFrame, columna: str):
    _estilo()
    mediana_global = df[columna].median()
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.boxplot(
        data=df, x="Churn", y=columna, ax=ax,
        palette=PALETTE_CHURN, width=0.45,
        boxprops=dict(linewidth=1.5),
        whiskerprops=dict(linewidth=1.2),
        medianprops=dict(color="white", linewidth=2),
        flierprops=dict(marker="o", markersize=3, alpha=0.4)
    )
    ax.axhline(mediana_global, color="#888", linestyle="--", linewidth=1.2,
               label=f"Mediana global: {mediana_global:.1f}")
    ax.set_title(f"{columna} según Churn", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Churn", fontsize=11)
    ax.set_ylabel(columna, fontsize=11)
    ax.legend(frameon=False, fontsize=9)
    plt.tight_layout()
    return fig
 
 
def barras_tasa_churn(df: pd.DataFrame, columna: str):
    _estilo()
    tasa = (
        df.groupby(columna)["Churn"]
        .apply(lambda x: (x == "Yes").mean() * 100)
        .round(1).reset_index()
    )
    tasa.columns = [columna, "Tasa Churn (%)"]
    tasa = tasa.sort_values("Tasa Churn (%)", ascending=False)
 
    fig, ax = plt.subplots(figsize=(9, 4))
    colores = plt.cm.RdYlGn_r(np.linspace(0.15, 0.85, len(tasa)))
    bars = ax.bar(tasa[columna].astype(str), tasa["Tasa Churn (%)"], color=colores, edgecolor="white", linewidth=0.8)
    for bar, val in zip(bars, tasa["Tasa Churn (%)"]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f"{val:.1f}%", ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.set_title(f"Tasa de Churn por {columna}", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel(columna, fontsize=11)
    ax.set_ylabel("Tasa Churn (%)", fontsize=11)
    ax.set_ylim(0, tasa["Tasa Churn (%)"].max() * 1.2)
    ax.tick_params(axis="x", rotation=20)
    plt.tight_layout()
    return fig
 
 
def heatmap_correlacion(df: pd.DataFrame):
    _estilo()
    corr = df.select_dtypes(include="number").corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        corr, mask=mask, annot=True, fmt=".2f",
        cmap="coolwarm", ax=ax,
        linewidths=0.5, linecolor="white",
        cbar_kws={"shrink": 0.8},
        annot_kws={"size": 10}
    )
    ax.set_title("Matriz de Correlación — Variables Numéricas", fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()
    return fig
 
 
def violinplot_por_churn(df: pd.DataFrame, columna: str):
    _estilo()
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.violinplot(
        data=df, x="Churn", y=columna, ax=ax,
        palette=PALETTE_CHURN, inner="quartile",
        linewidth=1.5, cut=0
    )
    ax.set_title(f"Distribución de {columna} por Churn", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Churn", fontsize=11)
    ax.set_ylabel(columna, fontsize=11)
    plt.tight_layout()
    return fig
 
 
def barras_apiladas(df: pd.DataFrame, columna: str):
    _estilo()
    tabla = pd.crosstab(df[columna], df["Churn"], normalize="index") * 100
    fig, ax = plt.subplots(figsize=(9, 4))
    tabla.plot(kind="bar", stacked=True, ax=ax,
               color=[PALETTE_CHURN["No"], PALETTE_CHURN["Yes"]],
               edgecolor="white", linewidth=0.8)
    ax.set_title(f"Proporción de Churn por {columna}", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel(columna, fontsize=11)
    ax.set_ylabel("Porcentaje (%)", fontsize=11)
    ax.legend(title="Churn", frameon=False, fontsize=9)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=25, ha="right")
    ax.yaxis.set_major_formatter(mticker.PercentFormatter())
    plt.tight_layout()
    return fig
 
 
def scatter3d_churn(df: pd.DataFrame):
    df_plot = df.dropna(subset=["tenure", "MonthlyCharges", "TotalCharges"]).copy()
    colores = df_plot["Churn"].map(PALETTE_CHURN)
 
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection="3d")
 
    for churn_val, color in PALETTE_CHURN.items():
        sub = df_plot[df_plot["Churn"] == churn_val]
        ax.scatter(
            sub["tenure"], sub["MonthlyCharges"], sub["TotalCharges"],
            c=color, label=f"Churn {churn_val}",
            alpha=0.45, s=12, edgecolors="none"
        )
 
    ax.set_xlabel("Tenure (meses)", fontsize=9, labelpad=8)
    ax.set_ylabel("Monthly Charges ($)", fontsize=9, labelpad=8)
    ax.set_zlabel("Total Charges ($)", fontsize=9, labelpad=8)
    ax.set_title("Vista 3D — Tenure · Cargos Mensuales · Cargos Totales", fontsize=11, fontweight="bold", pad=14)
    ax.legend(frameon=False, fontsize=9)
    ax.view_init(elev=22, azim=135)
    plt.tight_layout()
    return fig