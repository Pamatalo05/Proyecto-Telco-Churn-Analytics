import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, List


class DataAnalyzer:

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.numericas, self.categoricas = self.clasificar_variables()

    def clasificar_variables(self) -> Tuple[List[str], List[str]]:
        numericas = self.df.select_dtypes(include="number").columns.tolist()
        categoricas = self.df.select_dtypes(include="object").columns.tolist()
        return numericas, categoricas

    def estadisticas_descriptivas(self) -> pd.DataFrame:
        desc = self.df[self.numericas].describe().T
        desc["mediana"] = self.df[self.numericas].median()
        desc["moda"] = self.df[self.numericas].mode().iloc[0]
        return desc.round(2)

    def resumen_nulos(self) -> pd.DataFrame:
        nulos = self.df.isnull().sum()
        porcentaje = (nulos / len(self.df) * 100).round(2)
        tabla = pd.DataFrame({
            "Columna": nulos.index,
            "Nulos": nulos.values,
            "Porcentaje (%)": porcentaje.values
        })
        tabla = tabla[tabla["Nulos"] > 0].sort_values("Nulos", ascending=False).reset_index(drop=True)
        return tabla

    def tasa_churn_por_grupo(self, columna: str) -> pd.DataFrame:
        tasa = (
            self.df.groupby(columna)["Churn"]
            .apply(lambda x: (x == "Yes").mean() * 100)
            .round(2)
            .reset_index()
        )
        tasa.columns = [columna, "Tasa Churn (%)"]
        return tasa.sort_values("Tasa Churn (%)", ascending=False).reset_index(drop=True)

    def resumen_general(self) -> str:
        filas, columnas = self.df.shape
        churn_pct = round(self.df["Churn"].value_counts(normalize=True).get("Yes", 0) * 100, 2)
        nulos = int(self.df.isnull().sum().sum())
        return (
            f"Dataset: {filas:,} filas · {columnas} columnas\n"
            f"Variables: {len(self.numericas)} numéricas · {len(self.categoricas)} categóricas\n"
            f"Tasa de Churn: {churn_pct}%\n"
            f"Valores nulos: {nulos}"
        )

    def graficar_histograma(self, columna: str, color: str = "steelblue"):
        media = self.df[columna].mean()
        mediana = self.df[columna].median()
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(self.df[columna], kde=True, ax=ax, color=color)
        ax.axvline(media, color="red", linestyle="--", linewidth=1.5, label=f"Media: {media:.2f}")
        ax.axvline(mediana, color="green", linestyle="--", linewidth=1.5, label=f"Mediana: {mediana:.2f}")
        ax.set_title(f"Distribución de {columna}")
        ax.set_xlabel(columna)
        ax.set_ylabel("Frecuencia")
        ax.legend()
        plt.tight_layout()
        return fig

    def graficar_barras(self, columna: str, palette: str = "Set2"):
        conteos = self.df[columna].value_counts()
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x=conteos.index, y=conteos.values, ax=ax, palette=palette)
        ax.bar_label(ax.containers[0], fmt="%d", padding=3)
        ax.set_title(f"Distribución de {columna}")
        ax.set_xlabel(columna)
        ax.set_ylabel("Cantidad")
        plt.tight_layout()
        return fig
