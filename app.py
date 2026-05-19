import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Backend sin GUI, evita crashes en Streamlit
import matplotlib.pyplot as plt
import seaborn as sns
import time

from data_analyzer import DataAnalyzer
import graficos

# ─── Configuración principal ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Telco Churn EDA",
    page_icon="📊",
    layout="wide"
)

# ─── Estilos globales (fijo, sin modo oscuro/claro) ───────────────────────────
st.markdown("""
<style>
/* Encabezado principal */
h1 { color: #1a5276; }

/* Tabs con mejor contraste */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 6px 6px 0 0;
    padding: 8px 16px;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background-color: #eaf3fb;
    border-bottom: 2px solid #1a5276;
}

/* Métricas más limpias */
[data-testid="metric-container"] {
    background: #f7fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 12px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #f0f4f8;
}
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📡 Telco Churn EDA")
    st.markdown("---")
    st.markdown("### 👤 Autor")
    st.markdown("""
    **Paulo Tapia Loor**  
    Python for Analytics  
    DMC Institute · 2026
    """)
    st.markdown("---")
    st.markdown("### 🔗 Links útiles")
    st.markdown("""
    - [Dataset en Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
    - [Repositorio GitHub](https://github.com/pamatalo05/proyecto-telco-churn-analytics)
    - [Apps EDA con Streamlit](https://github.com/search?q=streamlit+EDA&type=repositories)
    """)

# ─── Funciones cacheadas para no regenerar en cada rerun ─────────────────────

@st.cache_data
def cargar_csv(archivo_bytes: bytes) -> pd.DataFrame:
    """Carga y limpia el CSV. Se cachea por contenido del archivo."""
    import io
    df = pd.read_csv(io.BytesIO(archivo_bytes))
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    return df


@st.cache_data
def estadisticas_desc(df: pd.DataFrame) -> pd.DataFrame:
    analyzer = DataAnalyzer(df)
    return analyzer.estadisticas_descriptivas()


@st.cache_data
def resumen_nulos_df(df: pd.DataFrame) -> pd.DataFrame:
    analyzer = DataAnalyzer(df)
    return analyzer.resumen_nulos()


@st.cache_data
def tasa_churn_grupo(df: pd.DataFrame, columna: str) -> pd.DataFrame:
    analyzer = DataAnalyzer(df)
    return analyzer.tasa_churn_por_grupo(columna)


def mostrar_fig(fig):
    """Muestra figura y la cierra inmediatamente para liberar memoria."""
    st.pyplot(fig, clear_figure=True)
    plt.close(fig)


# ─── Título ──────────────────────────────────────────────────────────────────
st.title("📡 Telco Customer Churn — EDA")

tabs = st.tabs(["🏠 Inicio", "📂 Carga de datos", "🔍 EDA", "📌 Conclusiones"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — INICIO
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:

    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        st.markdown("### 📋 Sobre el proyecto")
        st.markdown("""
        Este proyecto analiza el dataset **TelcoCustomerChurn** usando Python y Streamlit
        para identificar patrones relacionados con la **fuga de clientes** (*churn*)
        en una empresa de telecomunicaciones.

        El enfoque es completamente **exploratorio**: estadísticas descriptivas,
        visualizaciones y análisis bivariados.
        """)

    with col2:
        st.markdown("### 📊 Datos del dataset")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("👥 Clientes", "7 043")
        c2.metric("📐 Variables", "21")
        c3.metric("🎯 Target", "Churn")
        c4.metric("📌 Tipo", "Binario")

        st.markdown("### 🛠️ Herramientas")
        a, b, c, d = st.columns(4)
        a.success("🐍 Python")
        b.success("🐼 Pandas")
        c.success("📊 Streamlit")
        d.success("📈 Seaborn")

    st.info("⬆️ Ve a **Carga de datos** para subir el CSV y comenzar el análisis.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — CARGA DE DATOS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:

    st.subheader("📂 Carga del dataset")

    archivo = st.file_uploader("Sube el archivo CSV", type=["csv"])

    if archivo is None:
        st.warning("Aún no se ha cargado ningún archivo.")
    else:
        try:
            inicio = time.time()

            # Leer bytes una sola vez y cachear
            archivo_bytes = archivo.read()
            df = cargar_csv(archivo_bytes)

            fin = time.time()
            tiempo = round(fin - inicio, 4)

            # Guardar en session_state
            st.session_state["df"] = df

            filas, columnas = df.shape

            st.success(f"✅ Archivo cargado: **{filas:,} filas** y **{columnas} columnas** — {tiempo}s")

            # Vista previa
            st.markdown("---")
            st.markdown("### Vista previa")
            n = st.slider("Número de filas a mostrar", 5, 50, 10)
            st.dataframe(df.head(n), use_container_width=True)

            # Métricas rápidas
            st.markdown("---")
            churn_pct = round(
                df["Churn"].value_counts(normalize=True).get("Yes", 0) * 100, 2
            )
            nulls = int(df.isnull().sum().sum())

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Filas", f"{filas:,}")
            c2.metric("Columnas", columnas)
            c3.metric("Churn %", f"{churn_pct}%")
            c4.metric("Valores nulos", nulls)

        except Exception as e:
            st.error(f"Error al cargar archivo: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — EDA
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:

    if "df" not in st.session_state:
        st.warning("⚠️ Primero debes cargar el dataset en la pestaña **Carga de datos**.")
        st.stop()

    df = st.session_state["df"]
    analyzer = DataAnalyzer(df)

    st.subheader("🔍 Exploratory Data Analysis")
    st.caption(f"Dataset: {df.shape[0]:,} filas · {df.shape[1]} columnas")
    st.markdown("---")

    eda_tabs = st.tabs([
        "📋 Info general",
        "📐 Variables",
        "📊 Estadísticas",
        "❓ Nulos",
        "🔢 Numéricas",
        "🔤 Categóricas",
        "📉 Bivariado Num",
        "📊 Bivariado Cat",
        "🔎 Interactivo",
        "💡 Hallazgos"
    ])

    # ── 1. INFO GENERAL ───────────────────────────────────────────────────────
    with eda_tabs[0]:
        st.markdown("### Información general del dataset")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Tipos de datos por columna**")
            tipos = pd.DataFrame(df.dtypes, columns=["Tipo"]).reset_index()
            tipos.columns = ["Columna", "Tipo"]
            tipos["Tipo"] = tipos["Tipo"].astype(str)
            st.dataframe(tipos, use_container_width=True, hide_index=True)

        with col2:
            st.markdown("**Valores nulos**")
            nulos = df.isnull().sum().reset_index()
            nulos.columns = ["Columna", "Nulos"]
            nulos = nulos[nulos["Nulos"] > 0]
            if nulos.empty:
                st.success("✅ No se encontraron valores nulos.")
            else:
                st.dataframe(nulos, use_container_width=True, hide_index=True)

    # ── 2. VARIABLES ──────────────────────────────────────────────────────────
    with eda_tabs[1]:
        st.markdown("### Clasificación de variables")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🔢 Numéricas")
            st.dataframe(
                pd.DataFrame(analyzer.numericas, columns=["Variable"]),
                use_container_width=True, hide_index=True
            )

        with col2:
            st.markdown("#### 🔤 Categóricas")
            st.dataframe(
                pd.DataFrame(analyzer.categoricas, columns=["Variable"]),
                use_container_width=True, hide_index=True
            )

    # ── 3. ESTADÍSTICAS ───────────────────────────────────────────────────────
    with eda_tabs[2]:
        st.markdown("### Estadísticas descriptivas")
        st.dataframe(
            estadisticas_desc(df),
            use_container_width=True
        )

    # ── 4. NULOS ──────────────────────────────────────────────────────────────
    with eda_tabs[3]:
        st.markdown("### Valores faltantes")

        tabla_nulos = resumen_nulos_df(df)

        if tabla_nulos.empty:
            st.success("✅ No hay valores nulos en el dataset.")
        else:
            st.dataframe(tabla_nulos, use_container_width=True, hide_index=True)

            fig, ax = plt.subplots(figsize=(6, 3))
            ax.barh(tabla_nulos["Columna"], tabla_nulos["Nulos"], color="#4C9BE8")
            ax.set_title("Columnas con valores nulos")
            ax.set_xlabel("Cantidad de nulos")
            plt.tight_layout()
            mostrar_fig(fig)

    # ── 5. NUMÉRICAS ──────────────────────────────────────────────────────────
    with eda_tabs[4]:
        st.markdown("### Variables numéricas")

        columnas_num = [c for c in ["tenure", "MonthlyCharges", "TotalCharges"] if c in df.columns]
        columna_num = st.selectbox("Selecciona una variable numérica", columnas_num, key="sel_num")

        col1, col2 = st.columns(2)

        with col1:
            fig = graficos.histograma_con_grupos(df, columna_num)
            mostrar_fig(fig)

        with col2:
            fig = graficos.boxplot_por_churn(df, columna_num)
            mostrar_fig(fig)

        # Estadísticas de la variable seleccionada
        stats = df[columna_num].describe().round(2)
        st.markdown("**Resumen estadístico:**")
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Media", stats["mean"])
        s2.metric("Mediana", round(df[columna_num].median(), 2))
        s3.metric("Std", stats["std"])
        s4.metric("Máx", stats["max"])

    # ── 6. CATEGÓRICAS ────────────────────────────────────────────────────────
    with eda_tabs[5]:
        st.markdown("### Variables categóricas")

        columnas_cat = [
            c for c in ["Churn", "Contract", "InternetService", "PaymentMethod"]
            if c in df.columns
        ]
        columna_cat = st.selectbox("Selecciona una variable categórica", columnas_cat, key="sel_cat")

        col1, col2 = st.columns([1, 2])

        with col1:
            conteos = df[columna_cat].value_counts().reset_index()
            conteos.columns = [columna_cat, "Cantidad"]
            st.dataframe(conteos, use_container_width=True, hide_index=True)

        with col2:
            fig = analyzer.graficar_barras(columna_cat)
            mostrar_fig(fig)

    # ── 7. BIVARIADO NUMÉRICO ─────────────────────────────────────────────────
    with eda_tabs[6]:
        st.markdown("### Variable numérica vs Churn")

        columnas_num2 = [
            c for c in ["MonthlyCharges", "tenure", "TotalCharges"]
            if c in df.columns
        ]
        columna_bv_num = st.selectbox("Variable numérica", columnas_num2, key="bv_num")

        col1, col2 = st.columns(2)

        with col1:
            fig = graficos.boxplot_por_churn(df, columna_bv_num)
            mostrar_fig(fig)

        with col2:
            fig = graficos.violinplot_por_churn(df, columna_bv_num)
            mostrar_fig(fig)

    # ── 8. BIVARIADO CATEGÓRICO ───────────────────────────────────────────────
    with eda_tabs[7]:
        st.markdown("### Variable categórica vs Churn")

        columnas_cat2 = [
            c for c in ["Contract", "InternetService", "PaymentMethod"]
            if c in df.columns
        ]
        columna_bv_cat = st.selectbox("Variable categórica", columnas_cat2, key="bv_cat")

        col1, col2 = st.columns(2)

        with col1:
            fig = graficos.barras_tasa_churn(df, columna_bv_cat)
            mostrar_fig(fig)

        with col2:
            fig = graficos.barras_apiladas(df, columna_bv_cat)
            mostrar_fig(fig)

        # Tabla de tasas
        st.markdown("**Tasa de churn por categoría:**")
        st.dataframe(
            tasa_churn_grupo(df, columna_bv_cat),
            use_container_width=True,
            hide_index=True
        )

    # ── 9. INTERACTIVO ────────────────────────────────────────────────────────
    with eda_tabs[8]:
        st.markdown("### Exploración interactiva")
        st.caption("Selecciona dos variables para visualizar su relación. Se usa una muestra de 1 000 filas para mayor velocidad.")

        col1, col2 = st.columns(2)

        with col1:
            var_x = st.selectbox("Variable X", df.columns, key="ix")

        with col2:
            var_y = st.selectbox("Variable Y", df.columns, key="iy")

        # Muestra para evitar sobrecarga
        df_sample = df.sample(min(1000, len(df)), random_state=42)

        es_num_x = pd.api.types.is_numeric_dtype(df_sample[var_x])
        es_num_y = pd.api.types.is_numeric_dtype(df_sample[var_y])

        fig, ax = plt.subplots(figsize=(8, 4))

        try:
            if es_num_x and es_num_y:
                sns.scatterplot(
                    data=df_sample,
                    x=var_x,
                    y=var_y,
                    hue="Churn",
                    palette={"No": "#4C9BE8", "Yes": "#E85C4C"},
                    alpha=0.6,
                    ax=ax
                )
                ax.set_title(f"{var_x} vs {var_y} (muestra 1 000 filas)")
            else:
                tabla = pd.crosstab(df_sample[var_x], df_sample[var_y])
                # Limitar tamaño del heatmap para evitar crash
                if tabla.shape[0] > 15 or tabla.shape[1] > 15:
                    st.warning("Las variables seleccionadas tienen demasiadas categorías para un heatmap. Elige otras.")
                    plt.close(fig)
                else:
                    sns.heatmap(tabla, annot=True, fmt="d", cmap="Blues", ax=ax)
                    ax.set_title(f"{var_x} vs {var_y}")
                    plt.tight_layout()
                    mostrar_fig(fig)
                    fig = None  # ya fue mostrada

            if fig is not None:
                plt.tight_layout()
                mostrar_fig(fig)

        except Exception as e:
            st.error(f"No se pudo generar el gráfico: {e}")
            plt.close(fig)

    # ── 10. HALLAZGOS ─────────────────────────────────────────────────────────
    with eda_tabs[9]:
        st.markdown("### 💡 Hallazgos principales")

        churn_pct = round(
            df["Churn"].value_counts(normalize=True).get("Yes", 0) * 100, 2
        )

        col1, col2, col3 = st.columns(3)
        col1.metric("Tasa de churn", f"{churn_pct}%")
        col2.metric(
            "Tenure promedio (Churn Sí)",
            f"{round(df[df['Churn']=='Yes']['tenure'].mean(), 1)} meses"
        )
        col3.metric(
            "Cargo mensual promedio (Churn Sí)",
            f"${round(df[df['Churn']=='Yes']['MonthlyCharges'].mean(), 2)}"
        )

        st.markdown("""
        **Principales hallazgos del análisis:**

        - 📌 **Tipo de contrato:** Los clientes con contrato *Month-to-month* tienen
          tasas de churn notablemente más altas que quienes tienen contratos anuales o bianuales.

        - 📌 **Permanencia:** Los clientes que abandonan llevan significativamente menos
          meses en la empresa — los primeros meses son el período de mayor riesgo.

        - 📌 **Cargos mensuales:** A mayor cargo mensual, mayor probabilidad de churn.
          Posiblemente refleja insatisfacción con la relación precio/valor.

        - 📌 **Tipo de internet:** Los clientes con fibra óptica muestran más churn
          que los de DSL, lo que podría indicar expectativas más altas no cumplidas.

        - 📌 **Correlación variables numéricas:** `tenure` y `TotalCharges` tienen
          alta correlación positiva, mientras que `tenure` y churn son inversamente relacionados.
        """)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — CONCLUSIONES
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:

    st.subheader("📌 Conclusiones")

    if "df" not in st.session_state:
        st.warning("⚠️ Primero carga el dataset para generar conclusiones.")
        st.stop()

    df = st.session_state["df"]

    # Métricas calculadas
    churn_pct = round(df["Churn"].value_counts(normalize=True).get("Yes", 0) * 100, 2)
    contrato_churn = df[df["Churn"] == "Yes"]["Contract"].value_counts().idxmax()
    tenure_yes = round(df[df["Churn"] == "Yes"]["tenure"].mean(), 1)
    tenure_no  = round(df[df["Churn"] == "No"]["tenure"].mean(), 1)
    monthly_yes = round(df[df["Churn"] == "Yes"]["MonthlyCharges"].mean(), 2)
    monthly_no  = round(df[df["Churn"] == "No"]["MonthlyCharges"].mean(), 2)
    internet_churn = df[df["Churn"] == "Yes"]["InternetService"].value_counts().idxmax()

    # Panel de métricas resumen
    st.markdown("### Resumen numérico")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tasa de churn", f"{churn_pct}%")
    c2.metric("Tenure (churn)", f"{tenure_yes} m", delta=f"{tenure_yes - tenure_no:.1f} m vs retención", delta_color="inverse")
    c3.metric("Cargo mensual (churn)", f"${monthly_yes}", delta=f"+${round(monthly_yes - monthly_no, 2)} vs retención", delta_color="inverse")
    c4.metric("Contrato de mayor churn", contrato_churn)

    st.markdown("---")
    st.markdown("### Análisis detallado")

    with st.expander("1️⃣ Tasa general de churn", expanded=True):
        st.markdown(f"""
        Aproximadamente el **{churn_pct}%** de los clientes abandonaron el servicio.
        Dado que adquirir un nuevo cliente cuesta entre **6 y 7 veces más** que retener uno existente,
        reducir esta tasa tiene un alto impacto económico directo.
        """)

    with st.expander("2️⃣ Tipo de contrato"):
        st.markdown(f"""
        El tipo de contrato con mayor cantidad de clientes que se fueron fue
        **{contrato_churn}**.

        Los contratos de corta duración ofrecen más flexibilidad al cliente para
        abandonar sin penalización. Migrar clientes hacia contratos anuales podría
        ser una palanca clave de retención.
        """)

    with st.expander("3️⃣ Permanencia y fidelización"):
        st.markdown(f"""
        Los clientes que se fueron tenían en promedio **{tenure_yes} meses** en la empresa,
        frente a **{tenure_no} meses** de quienes permanecieron.

        Esto sugiere que los **primeros meses son el período crítico**: programas de
        onboarding y fidelización temprana podrían reducir significativamente el churn.
        """)

    with st.expander("4️⃣ Cargos mensuales"):
        st.markdown(f"""
        El cargo mensual promedio de los clientes con churn fue **${monthly_yes}**,
        versus **${monthly_no}** de los que se quedaron.

        Los clientes que pagan más parecen ser más sensibles a la percepción de valor.
        Revisar la estructura de precios o agregar beneficios a los planes más costosos
        podría mejorar la retención.
        """)

    with st.expander("5️⃣ Tipo de servicio de internet"):
        st.markdown(f"""
        El servicio con más churn registrado fue **{internet_churn}**.

        Esto podría reflejar mayores expectativas de rendimiento no cumplidas,
        o una mayor competencia en ese segmento del mercado.
        """)

    st.markdown("---")
    st.markdown("### 🔍 Reflexión final")
    st.info("""
    Este análisis exploratorio permite identificar **perfiles de riesgo de churn**
    basados en variables como el tipo de contrato, tiempo de permanencia y cargos.
    Aunque no se construyó un modelo predictivo, los patrones encontrados son
    suficientemente claros como para orientar decisiones de negocio concretas
    en retención y fidelización de clientes.
    """)