# Anticipación de Costos Operativos — Prueba Técnica DataKnow

## Contexto del Problema

Una empresa constructora necesita anticipar los costos futuros de dos equipos críticos (**Equipo 1** y **Equipo 2**). Para ello, cuenta con datos históricos de precios de tres materias primas (**X**, **Y** y **Z**), y se busca determinar cuáles de estas materias primas explican mejor el comportamiento del precio de cada equipo.

El objetivo es construir un sistema completo que combine análisis estadístico, modelos predictivos, proyecciones con incertidumbre y un agente conversacional de IA que responda preguntas de negocio.

---

## Objetivos

1. **Análisis exploratorio:** identificar patrones, correlaciones y distribuciones en los datos históricos.
2. **Selección de variables:** determinar qué materias primas tienen mayor poder explicativo sobre el precio de cada equipo.
3. **Modelado predictivo:** construir y comparar modelos de regresión y series de tiempo.
4. **Forecasting con incertidumbre:** proyectar costos futuros con intervalos de confianza.
5. **Agente conversacional:** exponer los resultados mediante un agente de IA que responda preguntas en lenguaje natural.
6. **Arquitectura cloud:** proponer una arquitectura escalable para productivizar la solución.

---

## Metodología Propuesta

```
Datos históricos
      │
      ▼
Exploración y limpieza (EDA)
      │
      ▼
Análisis de correlación y selección de variables
      │
      ▼
Modelado predictivo (Regresión / Series de Tiempo)
      │
      ▼
Forecasting con intervalos de confianza
      │
      ▼
Agente conversacional (LangChain + ChromaDB + OpenAI)
      │
      ▼
Aplicación interactiva (Streamlit)
```

---

## Estructura del Repositorio

```
dataknow-costos-operativos/
│
├── data/
│   ├── raw/                  # Datos originales sin modificar
│   └── processed/            # Datos procesados y limpios
│
├── notebooks/
│   ├── 01_exploracion_datos.ipynb      # EDA y análisis de correlaciones
│   ├── 02_modelado_predictivo.ipynb    # Entrenamiento y evaluación de modelos
│   └── 03_forecasting.ipynb           # Proyecciones con incertidumbre
│
├── src/
│   ├── preprocessing.py      # Limpieza y preparación de datos
│   ├── modeling.py           # Entrenamiento y evaluación de modelos
│   ├── forecasting.py        # Generación de proyecciones
│   └── agent.py              # Agente conversacional con LangChain
│
├── app/
│   └── streamlit_app.py      # Interfaz interactiva con Streamlit
│
├── reports/
│   └── informe.md            # Informe técnico del proyecto
│
├── architecture/             # Diagramas y documentación de arquitectura cloud
│
├── requirements.txt          # Dependencias del proyecto
├── README.md                 # Este archivo
└── .gitignore
```

---

## Tecnologías

| Categoría | Herramientas |
|---|---|
| Lenguaje | Python 3.10+ |
| Análisis de datos | pandas, numpy, scipy, statsmodels |
| Visualización | matplotlib, seaborn, plotly |
| Machine Learning | scikit-learn, XGBoost, LightGBM |
| Forecasting | Prophet, pmdarima (ARIMA automático) |
| LLM / Agente | LangChain, OpenAI GPT, ChromaDB |
| Aplicación web | Streamlit |
| Entorno | python-dotenv, pydantic |

---

## Estado del Proyecto

- [x] Estructura del repositorio creada
- [x] README y documentación inicial
- [x] Requirements y .gitignore configurados
- [ ] Datos cargados en `data/raw/`
- [ ] Análisis exploratorio (notebook 01)
- [ ] Modelado predictivo (notebook 02)
- [ ] Forecasting (notebook 03)
- [ ] Módulos `src/` implementados
- [ ] Agente conversacional funcional
- [ ] Aplicación Streamlit desplegada
- [ ] Arquitectura cloud documentada
- [ ] Informe técnico finalizado

---

## Instrucciones de Ejecución

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd dataknow-costos-operativos
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```
OPENAI_API_KEY=tu_clave_aqui
```

### 5. Ejecutar notebooks

```bash
jupyter notebook
```

### 6. Ejecutar la aplicación Streamlit

```bash
streamlit run app/streamlit_app.py
```

---

## Autor

Prueba técnica — Científica de Datos / IA  
DataKnow · 2026
