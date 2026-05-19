import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time

from data_analyzer import DataAnalyzer
import graficos

# Configuración principal
st.set_page_config(
    page_title="Telco Churn EDA",
    page_icon="📊",
    layout="wide"
)

# Sidebar

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

with st.sidebar:
    st.markdown("## Configuración")

    dark = st.toggle("Modo oscuro", value=st.session_state.dark_mode)
    st.session_state.dark_mode = dark

    st.markdown("---")

    st.markdown("### Algunos proyectos similares")
    st.markdown("""
    - [EDA Telco Churn](https://github.com/search?q=telco+customer+churn+streamlit&type=repositories)
    - [Apps EDA con Streamlit](https://github.com/search?q=streamlit+EDA&type=repositories)
    """)

# Estilos

if st.session_state.dark_mode:
    st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"]{
        background-color:#0e1117;
        color:white;
    }

    [data-testid="stSidebar"]{
        background-color:#161b22;
    }

    .stTabs [data-baseweb="tab-list"]{
        background:#161b22;
        border-radius:10px;
        padding:5px;
    }

    .stTabs [aria-selected="true"]{
        background:#21262d !important;
        border-radius:8px;
    }
    </style>
    """, unsafe_allow_html=True)

# Navegación

st.title("📡 Telco Customer Churn - EDA")

tabs = st.tabs([
    "Inicio",
    "Carga de datos",
    "EDA",
    "Conclusiones"
])

# INICIO

with tabs[0]:

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Autor")

        st.markdown("""
        **Nombre:** Paulo Tapia Loor
        **Curso:** Python for Analytics  
        **Institución:** DMC Institute  2026
        """)

    with col2:
        st.markdown("### Sobre el proyecto")

        st.markdown("""
        Este proyecto analiza el dataset **TelcoCustomerChurn**
        utilizando Python y Streamlit.

        El objetivo es entender mejor qué variables parecen estar
        relacionadas con la pérdida de clientes.
        """)

    st.markdown("---")

    st.markdown("### Datos generales")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Clientes", "7043")

    with c2:
        st.metric("Variables", "21")

    with c3:
        st.metric("Target", "Churn")

    with c4:
        st.metric("Tipo", "Clasificación")

    st.markdown("---")

    st.markdown("### Herramientas usadas")

    a, b, c, d = st.columns(4)

    with a:
        st.success("Python")

    with b:
        st.success("Pandas")

    with c:
        st.success("Streamlit")

    with d:
        st.success("Matplotlib")

    st.info("Primero carga el dataset para comenzar el análisis.")

# CARGA DE DATOS

with tabs[1]:

    st.subheader("Carga del dataset")

    archivo = st.file_uploader(
        "Sube el archivo CSV",
        type=["csv"]
    )

    if archivo is None:

        st.warning("Aún no se ha cargado ningún archivo.")

    else:

        try:
            inicio = time.time()

            df = pd.read_csv(archivo)

            # Algunos valores vienen vacíos
            df["TotalCharges"] = pd.to_numeric(
                df["TotalCharges"],
                errors="coerce"
            )

            fin = time.time()

            tiempo = round(fin - inicio, 3)

            st.session_state["df"] = df

            filas, columnas = df.shape

            st.success(
                f"Archivo cargado correctamente: {filas} filas y {columnas} columnas"
            )

            st.markdown(f"Tiempo de carga: `{tiempo} segundos`")

            st.markdown("---")

            st.markdown("### Vista previa")

            n = st.slider(
                "Número de filas",
                5,
                50,
                10
            )

            st.dataframe(
                df.head(n),
                use_container_width=True
            )

            st.markdown("---")

            churn_pct = round(
                df["Churn"].value_counts(normalize=True)["Yes"] * 100,
                2
            )

            nulls = int(df.isnull().sum().sum())

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.metric("Filas", filas)

            with c2:
                st.metric("Columnas", columnas)

            with c3:
                st.metric("Churn %", f"{churn_pct}%")

            with c4:
                st.metric("Nulos", nulls)

        except Exception as e:
            st.error(f"Error al cargar archivo: {e}")

# EDA

with tabs[2]:

    if "df" not in st.session_state:

        st.warning("Primero debes cargar el dataset.")

    else:

        df = st.session_state["df"]

        analyzer = DataAnalyzer(df)

        st.subheader("Exploratory Data Analysis")

        st.markdown(
            f"Dataset actual: {df.shape[0]} filas y {df.shape[1]} columnas"
        )

        st.markdown("---")

        eda_tabs = st.tabs([
            "Info general",
            "Variables",
            "Estadísticas",
            "Nulos",
            "Numéricas",
            "Categóricas",
            "Bivariado Num",
            "Bivariado Cat",
            "Interactivo",
            "Hallazgos"
        ])

        # INFO GENERAL

        with eda_tabs[0]:

            st.markdown("### Información general")

            col1, col2 = st.columns(2)

            with col1:

                tipos = pd.DataFrame(
                    df.dtypes,
                    columns=["Tipo"]
                ).reset_index()

                tipos.columns = ["Columna", "Tipo"]

                st.dataframe(
                    tipos,
                    use_container_width=True,
                    hide_index=True
                )

            with col2:

                nulos = df.isnull().sum().reset_index()

                nulos.columns = ["Columna", "Nulos"]

                nulos = nulos[nulos["Nulos"] > 0]

                if nulos.empty:
                    st.success("No se encontraron valores nulos.")
                else:
                    st.dataframe(
                        nulos,
                        use_container_width=True,
                        hide_index=True
                    )

        # VARIABLES

        with eda_tabs[1]:

            st.markdown("### Tipos de variables")

            col1, col2 = st.columns(2)

            with col1:

                st.markdown("#### Numéricas")

                st.dataframe(
                    pd.DataFrame(
                        analyzer.numericas,
                        columns=["Variables"]
                    ),
                    use_container_width=True,
                    hide_index=True
                )

            with col2:

                st.markdown("#### Categóricas")

                st.dataframe(
                    pd.DataFrame(
                        analyzer.categoricas,
                        columns=["Variables"]
                    ),
                    use_container_width=True,
                    hide_index=True
                )

        # ESTADÍSTICAS

        with eda_tabs[2]:

            st.markdown("### Estadísticas descriptivas")

            st.dataframe(
                analyzer.estadisticas_descriptivas(),
                use_container_width=True
            )

        # NULOS

        with eda_tabs[3]:

            st.markdown("### Valores faltantes")

            tabla_nulos = analyzer.resumen_nulos()

            if tabla_nulos.empty:

                st.success("No hay valores nulos.")

            else:

                st.dataframe(
                    tabla_nulos,
                    use_container_width=True,
                    hide_index=True
                )

                fig, ax = plt.subplots(figsize=(6, 3))

                ax.barh(
                    tabla_nulos["Columna"],
                    tabla_nulos["Nulos"]
                )

                ax.set_title("Valores nulos")

                st.pyplot(fig)

                plt.close(fig)

        # NUMÉRICAS

        with eda_tabs[4]:

            st.markdown("### Variables numéricas")

            columnas_num = [
                c for c in
                ["tenure", "MonthlyCharges", "TotalCharges"]
                if c in df.columns
            ]

            columna = st.selectbox(
                "Selecciona una variable",
                columnas_num
            )

            fig = graficos.histograma_con_grupos(df, columna)

            st.pyplot(fig)

            plt.close(fig)

            st.markdown(
                f"Media: `{round(df[columna].mean(),2)}`"
            )

        # CATEGÓRICAS

        with eda_tabs[5]:

            st.markdown("### Variables categóricas")

            columnas_cat = [
                c for c in [
                    "Churn",
                    "Contract",
                    "InternetService",
                    "PaymentMethod"
                ] if c in df.columns
            ]

            columna = st.selectbox(
                "Selecciona una variable categórica",
                columnas_cat
            )

            conteos = df[columna].value_counts()

            st.dataframe(
                conteos.reset_index(),
                use_container_width=True
            )

            fig = analyzer.graficar_barras(columna)

            st.pyplot(fig)

            plt.close(fig)

        # BIVARIADO NUM

        with eda_tabs[6]:

            st.markdown("### Numérico vs Churn")

            columnas_num = [
                c for c in
                ["MonthlyCharges", "tenure", "TotalCharges"]
                if c in df.columns
            ]

            columna = st.selectbox(
                "Variable numérica",
                columnas_num,
                key="num"
            )

            fig = graficos.boxplot_por_churn(df, columna)

            st.pyplot(fig)

            plt.close(fig)

        # BIVARIADO CAT

        with eda_tabs[7]:

            st.markdown("### Categórico vs Churn")

            columnas_cat = [
                c for c in [
                    "Contract",
                    "InternetService",
                    "PaymentMethod"
                ] if c in df.columns
            ]

            columna = st.selectbox(
                "Variable categórica",
                columnas_cat,
                key="cat"
            )

            fig = graficos.barras_tasa_churn(df, columna)

            st.pyplot(fig)

            plt.close(fig)

        # INTERACTIVO


        with eda_tabs[8]:

            st.markdown("### Exploración interactiva")

            col1, col2 = st.columns(2)

            with col1:
                var_x = st.selectbox(
                    "Variable X",
                    df.columns,
                    key="x"
                )

            with col2:
                var_y = st.selectbox(
                    "Variable Y",
                    df.columns,
                    key="y"
                )

            df_f = df.copy()

            fig, ax = plt.subplots(figsize=(8,4))

            es_num_x = pd.api.types.is_numeric_dtype(df_f[var_x])
            es_num_y = pd.api.types.is_numeric_dtype(df_f[var_y])

            if es_num_x and es_num_y:

                sns.scatterplot(
                    data=df_f,
                    x=var_x,
                    y=var_y,
                    hue="Churn",
                    ax=ax
                )

            else:

                tabla = pd.crosstab(
                    df_f[var_x],
                    df_f[var_y]
                )

                sns.heatmap(
                    tabla,
                    annot=True,
                    fmt="d",
                    ax=ax
                )

            plt.tight_layout()

            st.pyplot(fig)

            plt.close(fig)

        # HALLAZGOS

        with eda_tabs[9]:

            st.markdown("### Hallazgos principales")

            churn_pct = round(
                df["Churn"].value_counts(normalize=True)["Yes"] * 100,
                2
            )

            st.metric(
                "Porcentaje de churn",
                f"{churn_pct}%"
            )

            st.markdown("""
            Algunas variables parecen tener relación con el churn,
            especialmente el tipo de contrato, el tiempo de permanencia
            y los cargos mensuales.
            """)

# CONCLUSIONES


with tabs[3]:

    st.subheader("Conclusiones")

    if "df" not in st.session_state:

        st.warning("Primero carga el dataset para generar conclusiones.")

    else:

        df = st.session_state["df"]

        # Métricas básicas
        churn_pct = round(
            df["Churn"].value_counts(normalize=True)["Yes"] * 100,
            2
        )

        contrato_churn = (
            df[df["Churn"] == "Yes"]["Contract"]
            .value_counts()
            .idxmax()
        )

        tenure_yes = round(
            df[df["Churn"] == "Yes"]["tenure"].mean(),
            1
        )

        tenure_no = round(
            df[df["Churn"] == "No"]["tenure"].mean(),
            1
        )

        monthly_yes = round(
            df[df["Churn"] == "Yes"]["MonthlyCharges"].mean(),
            2
        )

        monthly_no = round(
            df[df["Churn"] == "No"]["MonthlyCharges"].mean(),
            2
        )

        internet_churn = (
            df[df["Churn"] == "Yes"]["InternetService"]
            .value_counts()
            .idxmax()
        )

        # Conclusiones automáticas

        st.markdown("### Resumen del análisis")

        st.markdown(f"""
        #### 1. Tasa general de churn

        Aproximadamente el **{churn_pct}%** de los clientes abandonaron el servicio.
        Esto indica que una parte importante de usuarios no permanece a largo plazo.
        """)

        st.markdown(f"""
        #### 2. Tipo de contrato

        El tipo de contrato con mayor cantidad de churn fue
        **{contrato_churn}**.

        Esto sugiere que los clientes con contratos menos estables
        tienen más probabilidad de abandonar el servicio.
        """)

        st.markdown(f"""
        #### 3. Permanencia de clientes

        Los clientes que abandonaron el servicio tienen una permanencia
        promedio de **{tenure_yes} meses**, mientras que los clientes
        que permanecen tienen alrededor de **{tenure_no} meses**.

        Esto muestra que los clientes nuevos son los más propensos
        a irse.
        """)

        st.markdown(f"""
        #### 4. Cargos mensuales

        Los clientes con churn pagan en promedio
        **${monthly_yes}**, mientras que los demás pagan
        alrededor de **${monthly_no}**.

        Los cargos mensuales altos parecen estar relacionados
        con una mayor tasa de abandono.
        """)

        st.markdown(f"""
        #### 5. Servicio de internet

        El servicio con más churn registrado fue
        **{internet_churn}**.

        Esto podría indicar diferencias en experiencia de usuario
        o percepción del servicio.
        """)

        st.markdown("---")

        st.markdown("### Reflexión final")

        st.markdown("""
        Durante este proyecto fue posible aplicar técnicas básicas
        de análisis exploratorio de datos utilizando Python, Pandas
        y Streamlit.

        La parte más importante fue interpretar los gráficos y encontrar
        patrones que ayuden a entender el comportamiento de los clientes.
        """)