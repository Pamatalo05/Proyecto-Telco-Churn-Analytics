# 📡 TelcoCustomerChurn — Análisis Exploratorio de Datos

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://TU_APP.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.0-150458?logo=pandas)](https://pandas.pydata.org)

---

## 📋 Descripción del Proyecto

Este proyecto es una aplicación interactiva construida con **Streamlit** que realiza un **Análisis Exploratorio de Datos (EDA)** sobre el dataset `TelcoCustomerChurn.csv`.

El objetivo es identificar patrones asociados a la **fuga de clientes** (*churn*) en una empresa de telecomunicaciones, aplicando técnicas de visualización y estadística descriptiva. El enfoque es completamente **exploratorio**, sin desarrollo de modelos predictivos.

Durante el último mes, la empresa incrementó su tasa de churn en +0.5 puntos porcentuales debido al contexto del COVID-19. Dado que adquirir un nuevo cliente cuesta entre 6 y 7 veces más que retener uno existente, comprender las causas del abandono es una prioridad estratégica.

---

## 🎯 Objetivos Específicos

- Aplicar conceptos de Python, Pandas, NumPy, Matplotlib y Seaborn de forma integrada
- Desarrollar una interfaz profesional e interactiva con Streamlit
- Implementar Programación Orientada a Objetos (POO)
- Identificar patrones de comportamiento en clientes que abandonan el servicio
- Presentar hallazgos orientados a la toma de decisiones de negocio

---

## 🛠️ Tecnologías Utilizadas

| Herramienta | Versión | Uso |
|---|---|---|
| Python | 3.11 | Lenguaje principal |
| Streamlit | ≥ 1.32 | Interfaz interactiva |
| Pandas | ≥ 2.0 | Manipulación de datos |
| NumPy | ≥ 1.26 | Operaciones numéricas |
| Matplotlib | ≥ 3.8 | Visualización |
| Seaborn | ≥ 0.13 | Visualización estadística |

---

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
cd TU_REPO
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

> *Agregar capturas una vez desplegada la aplicación.*

![Home](images\Screenshot 2026-05-18 233541.png)
![Home](images\Screenshot 2026-05-18 233600.png)
![Home](images\Screenshot 2026-05-18 233613.png)
![Home](images\Screenshot 2026-05-18 233622.png)
![Home](images\Screenshot 2026-05-18 233632.png)
![Home](images\Screenshot 2026-05-18 233643.png)
![Home](images\Screenshot 2026-05-18 233705.png)
![Home](images\Screenshot 2026-05-18 233725.png)
![Home](images\Screenshot 2026-05-18 233755.png)
![Home](images\Screenshot 2026-05-18 233812.png)
![Home](images\Screenshot 2026-05-18 233835.png)
![Home](images\Screenshot 2026-05-18 233850.png)
![Home](images\Screenshot 2026-05-18 233915.png)


## 📊 Módulos de la Aplicación

| Módulo | Descripción |
|---|---|
| 🏠 Home | Presentación del proyecto y datos del autor |
| 📂 Carga del Dataset | Carga, validación y vista previa del CSV |
| 🔍 Análisis EDA | 10 ítems de análisis exploratorio con tabs interactivos |
| 📌 Conclusiones | 5 conclusiones con enfoque en decisiones de negocio |

---

## 🔗 Links Relevantes

- 🌐 **App desplegada:** [TU_APP.streamlit.app](https://proyecto-telco-churn-analytics-tapia-paulo.streamlit.app/)
- 💻 **Repositorio GitHub:** [github.com/TU_USUARIO/TU_REPO](https://github.com/pamatalo05/proyecto-telco-churn-analytics)
- 📦 **Dataset original:** [Kaggle — Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

---

## 👤 Autor

**Nombre:** TU NOMBRE AQUÍ  
**Especialización:** Python for Analytics — DMC Institute  
**Año:** 2025
