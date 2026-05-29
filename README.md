# 📡 Telco Customer Churn Analytics Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://proyecto-telco-churn-analytics-tapia-paulo.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.0-150458?logo=pandas)](https://pandas.pydata.org)

---

## Descripción del Proyecto

Este proyecto es una aplicación interactiva construida con **Streamlit** que realiza un **Análisis Exploratorio de Datos (EDA)** sobre el dataset `TelcoCustomerChurn.csv`.

El objetivo es identificar patrones asociados a la **fuga de clientes** (*churn*) en una empresa de telecomunicaciones, aplicando técnicas de visualización y estadística descriptiva. El enfoque es completamente **exploratorio**, sin desarrollo de modelos predictivos.

El proyecto busca identificar patrones asociados a la fuga de clientes mediante análisis exploratorio, visualización y exploración interactiva de datos.
---

## 🎯 Objetivos Específicos

- Aplicar conceptos de Python, Pandas, NumPy, Matplotlib y Seaborn de forma integrada
- Desarrollar una interfaz profesional e interactiva con Streamlit
- Implementar Programación Orientada a Objetos (POO)
- Identificar patrones de comportamiento en clientes que abandonan el servicio
- Presentar hallazgos orientados a la toma de decisiones de negocio

---

## Tecnologías Utilizadas

| Herramienta | Versión | Uso |
|---|---|---|
| Python | 3.11 | Lenguaje principal |
| Streamlit | ≥ 1.32 | Interfaz interactiva |
| Pandas | ≥ 2.0 | Manipulación de datos |
| NumPy | ≥ 1.26 | Operaciones numéricas |
| Matplotlib | ≥ 3.8 | Visualización |
| Seaborn | ≥ 0.13 | Visualización estadística |

---

## Key Insights

- Clientes con menor permanencia presentan mayores tasas de churn
- Determinados contratos presentan mayor riesgo de abandono
- Monthly Charges muestra patrones diferenciados entre grupos

## 📁 Estructura del Proyecto

```
📦 TelcoChurnEDA/
├── app.py                      # Aplicación principal Streamlit
├── data_analyzer.py            # Clase DataAnalyzer (POO)
├── graficos.py                 # Funciones de visualización
├── requirements.txt            # Dependencias
├── README.md                   # Este archivo
└── data/
    └── TelcoCustomerChurn.csv  # Dataset
```

---

## 🚀 Instrucciones de Ejecución

**1. Clona el repositorio**
```bash
git clone https://github.com/pamatalo05/proyecto-telco-churn-analytics
cd Proyecto-Telco-Churn-Analytics
```

**2. Crea un entorno virtual**
```bash
python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows
```

**3. Instala las dependencias**
```bash
pip install -r requirements.txt
```

**4. Ejecuta la aplicación**
```bash
streamlit run app.py
```

**5. Carga el dataset**

En la app, navega a **📂 Carga del Dataset** en el menú lateral y sube el archivo `TelcoCustomerChurn.csv`.

---

## 📸 Capturas de la Aplicación

**Captura 1 — Pantalla de inicio**
![Captura 1](images/Screenshot%202026-05-18%20233541.png)

**Captura 2 — Carga del dataset**
![Captura 2](images/Screenshot%202026-05-18%20233600.png)

**Captura 3 — Vista previa del CSV**
![Captura 3](images/Screenshot%202026-05-18%20233613.png)

**Captura 4 — EDA: Información general**
![Captura 4](images/Screenshot%202026-05-18%20233622.png)

**Captura 5 — EDA: Clasificación de variables**
![Captura 5](images/Screenshot%202026-05-18%20233632.png)

**Captura 6 — EDA: Estadísticas descriptivas**
![Captura 6](images/Screenshot%202026-05-18%20233643.png)

**Captura 7 — EDA: Variables numéricas**
![Captura 7](images/Screenshot%202026-05-18%20233705.png)

**Captura 8 — EDA: Variables categóricas**
![Captura 8](images/Screenshot%202026-05-18%20233725.png)

**Captura 9 — EDA: Análisis bivariado numérico**
![Captura 9](images/Screenshot%202026-05-18%20233755.png)

**Captura 10 — EDA: Análisis bivariado categórico**
![Captura 10](images/Screenshot%202026-05-18%20233812.png)

**Captura 11 — EDA: Exploración interactiva**
![Captura 11](images/Screenshot%202026-05-18%20233835.png)

**Captura 12 — EDA: Hallazgos principales**
![Captura 12](images/Screenshot%202026-05-18%20233850.png)

**Captura 13 — Conclusiones**
![Captura 13](images/Screenshot%202026-05-18%20233915.png)

---

## 📊 Módulos de la Aplicación

| Módulo | Descripción |
|---|---|
| 🏠 Home | Presentación del proyecto y datos del autor |
| 📂 Carga del Dataset | Carga, validación y vista previa del CSV |
| 🔍 Análisis EDA | 10 ítems de análisis exploratorio con tabs interactivos |
| 📌 Conclusiones | 5 conclusiones con enfoque en decisiones de negocio |

---

## 🔗 Links 

- 🌐 **App desplegada:** [proyecto-telco-churn-analytics-tapia-paulo.streamlit.app](https://proyecto-telco-churn-analytics-tapia-paulo.streamlit.app/)
- 💻 **Repositorio GitHub:** [github.com/pamatalo05/proyecto-telco-churn-analytics](https://github.com/pamatalo05/proyecto-telco-churn-analytics)
- 📦 **Dataset original:** [Kaggle — Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

---

## 👤 Autor

**Nombre:** Paulo Tapia Loor
**Especialización:** Python for Analytics — DMC Institute  
**Año:** 2026
