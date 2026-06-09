# Preguntas Frecuentes (FAQ)

Documento generado a partir del análisis del código fuente, notebooks, configuración y documentación existente en el repositorio `dataknow-costos-operativos`.

---

## 1. ¿Qué problema resuelve este proyecto?

El proyecto aborda la anticipación de costos futuros de dos equipos críticos de construcción (**Equipo 1** y **Equipo 2**) a partir del comportamiento histórico de tres materias primas (**X**, **Y** y **Z**). Combina análisis estadístico, modelado predictivo, proyecciones con incertidumbre y un agente conversacional que responde preguntas de negocio en lenguaje natural.

**Evidencia encontrada:**

* `README.md`
* `reports/informe.md`
* `reports/resumen_ejecutivo.md`

---

## 2. ¿Cuál es la arquitectura general del sistema?

La arquitectura sigue un flujo en capas: datos históricos → exploración y limpieza → modelado → forecasting → agente conversacional → aplicación interactiva.

Componentes identificados:

| Capa | Componente | Rol |
|---|---|---|
| Datos | `data/raw/`, `data/processed/` | Almacenamiento de datos originales y procesados (CSV) |
| Análisis | `notebooks/01_*.ipynb` a `03_*.ipynb` | EDA, entrenamiento y forecasting reproducible |
| Lógica reutilizable | `src/` | Preprocesamiento, modelado, forecasting y agente |
| Conocimiento | `reports/*.md` | Documentos de resultados usados por el agente |
| Búsqueda | Azure AI Search (opcional) | Recuperación de contexto para el agente |
| API | `app/main.py` | FastAPI con endpoint `/chat` y UI HTML |
| UI alternativa | `app/streamlit_app.py` | Interfaz Streamlit (parcialmente implementada) |
| Scripts operativos | `scripts/` | Construcción y prueba del índice de búsqueda |

```
Datos históricos (CSV)
      │
      ▼
Notebooks EDA / Modelado / Forecasting
      │
      ▼
data/processed/ + reports/
      │
      ▼
Agente (RAG + herramientas) ──► FastAPI / Streamlit
```

**Evidencia encontrada:**

* `README.md`
* `src/agent.py`
* `app/main.py`
* `app/streamlit_app.py`
* `scripts/build_search_index.py`

---

## 3. ¿Qué tecnologías utiliza el proyecto?

| Categoría | Tecnologías identificadas |
|---|---|
| Lenguaje | Python 3.10+ |
| Análisis de datos | pandas, numpy, scipy, statsmodels |
| Visualización | matplotlib, seaborn, plotly |
| Machine Learning | scikit-learn (LinearRegression, Ridge, Lasso, GradientBoostingRegressor) |
| Forecasting | Prophet, pmdarima (ARIMA automático), statsmodels (ARIMA) |
| IA / Agente | LangChain, Google Gemini (`gemini-2.5-flash-lite`), Azure AI Search |
| API web | FastAPI, Uvicorn |
| UI | Streamlit, HTML/CSS/JS estático |
| Configuración | python-dotenv, pydantic |

**Nota:** `requirements.txt` también incluye `chromadb`, `openai`, `langchain-openai`, `xgboost` y `lightgbm`, pero no se encontró uso directo de esas librerías en el código fuente de `src/` ni en los notebooks analizados para el flujo principal del agente.

**Evidencia encontrada:**

* `README.md`
* `requirements.txt`
* `src/modeling.py`
* `src/forecasting.py`
* `src/dynamic_forecast.py`
* `src/agent.py`
* `notebooks/02_modelado_predictivo.ipynb`
* `notebooks/03_forecasting.ipynb`

---

## 4. ¿Cómo se ejecuta el proyecto localmente?

### Entorno base

1. Clonar el repositorio.
2. Crear y activar un entorno virtual.
3. Instalar dependencias con `pip install -r requirements.txt`.
4. Configurar variables de entorno en un archivo `.env` en la raíz.

### Notebooks de análisis

```bash
jupyter notebook
```

Ejecutar en orden: `01_exploracion_datos.ipynb` → `02_modelado_predictivo.ipynb` → `03_forecasting.ipynb`.

### Aplicación Streamlit

```bash
streamlit run app/streamlit_app.py
```

### API del agente (FastAPI)

El repositorio incluye `app/main.py` y la dependencia `uvicorn`, pero **no documenta explícitamente** el comando de arranque. Con la estructura actual, el arranque esperado sería:

```bash
uvicorn app.main:app --reload
```

Luego acceder a `http://localhost:8000/` para la interfaz de chat.

### Agente en consola

```bash
python src/agent.py
```

**Evidencia encontrada:**

* `README.md`
* `app/streamlit_app.py`
* `app/main.py`
* `requirements.txt` (uvicorn)
* `src/agent.py`

---

## 5. ¿Cómo se instalan las dependencias?

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate

pip install -r requirements.txt
```

El archivo `requirements.txt` fija versiones concretas de todas las dependencias del proyecto (más de 190 paquetes, incluyendo dependencias transitivas).

**Evidencia encontrada:**

* `README.md`
* `requirements.txt`

---

## 6. ¿Qué variables de entorno se requieren?

| Variable | Uso | Obligatoria |
|---|---|---|
| `GOOGLE_API_KEY` | Modelo generativo Gemini en el agente | Sí, para usar el agente |
| `AZURE_SEARCH_ENDPOINT` | Endpoint de Azure AI Search | No (hay fallback local) |
| `AZURE_SEARCH_KEY` | Clave de Azure AI Search | No |
| `AZURE_SEARCH_INDEX_NAME` | Nombre del índice (default: `dataknow-knowledge-index`) | No |

El `README.md` menciona `OPENAI_API_KEY`, pero el código actual del agente usa `GOOGLE_API_KEY` y no referencia `OPENAI_API_KEY`.

**Evidencia encontrada:**

* `README.md`
* `src/agent.py`
* `scripts/build_search_index.py`
* `.gitignore` (excluye `.env`)

---

## 7. ¿Qué datos utiliza el proyecto?

### Fuente original

* Archivo: `data/raw/historico_equipos.csv`
* Variables: `Date`, `Price_X`, `Price_Y`, `Price_Z`, `Price_Equipo1`, `Price_Equipo2`

### Dataset procesado

* Archivo: `data/processed/historico_equipos_limpio.csv`
* Generado por el notebook de EDA

### Forecasts exportados

* `data/processed/forecast_equipo1.csv`
* `data/processed/forecast_equipo2.csv`
* `data/processed/resumen_forecasts.csv`

### Características del dataset (según reportes)

* 3.530 registros diarios
* Periodo: 2010-01-04 a 2023-08-31
* Sin valores faltantes detectados

**Nota:** Los archivos CSV en `data/raw/` y `data/processed/` están en `.gitignore` y **no están presentes** en el repositorio clonado; deben generarse o aportarse localmente.

**Evidencia encontrada:**

* `notebooks/01_exploracion_datos.ipynb`
* `notebooks/02_modelado_predictivo.ipynb`
* `notebooks/03_forecasting.ipynb`
* `src/tools.py`
* `src/dynamic_forecast.py`
* `reports/resultados_eda.md`
* `.gitignore`

---

## 8. ¿Cómo se preparan y limpian los datos?

El preprocesamiento se realiza principalmente en el notebook `01_exploracion_datos.ipynb`, que carga `historico_equipos.csv`, valida calidad, analiza series temporales y exporta `historico_equipos_limpio.csv`.

Además existe el módulo `src/preprocessing.py` con funciones reutilizables:

* `load_raw_data()` — carga desde `data/raw/`
* `handle_missing_values()` — interpolación, forward fill o drop
* `detect_outliers_iqr()` — detección de outliers por IQR
* `save_processed_data()` — guardado en `data/processed/`

**Evidencia encontrada:**

* `notebooks/01_exploracion_datos.ipynb`
* `src/preprocessing.py`

---

## 9. ¿Cómo se entrenan los modelos predictivos?

### En notebooks

El notebook `02_modelado_predictivo.ipynb` importa funciones de `src/modeling.py` y entrena modelos con división temporal (`time_series_split_data`, 80/20).

### Modelos evaluados

* **Regresión lineal** (`LinearRegression`) — modelo principal seleccionado para ambos equipos
* **Gradient Boosting** (`GradientBoostingRegressor`) — evaluado para Equipo 2, con peor desempeño que la regresión lineal

El módulo `modeling.py` también expone `train_linear_model()` con variantes Ridge y Lasso, y `train_gradient_boosting_model()`.

### Métricas de evaluación

RMSE, MAE y R² mediante `evaluate_model()`.

### Resultados reportados (regresión lineal)

| Equipo | RMSE | MAE | R² |
|---|---|---|---|
| Equipo 1 | 10.3088 | 8.8699 | 0.9913 |
| Equipo 2 | 19.3198 | 16.5514 | 0.9853 |

### Persistencia de modelos

No se encontró evidencia de modelos serializados (`.pkl`, `.joblib`). Los coeficientes de regresión lineal están **hardcodeados** en `src/tools.py` para la herramienta de simulación de escenarios.

**Evidencia encontrada:**

* `notebooks/02_modelado_predictivo.ipynb`
* `src/modeling.py`
* `reports/resultados_modelado.md`
* `src/tools.py`
* `.gitignore` (excluye `models/`, `*.pkl`, `*.joblib`)

---

## 10. ¿Qué materias primas explican mejor el precio de cada equipo?

* **Equipo 1:** Price_Y (correlación 0.997; coeficiente dominante 0.796755)
* **Equipo 2:** Price_Z (correlación 0.983; importancia predominante en Gradient Boosting)

**Evidencia encontrada:**

* `reports/resultados_eda.md`
* `reports/resultados_modelado.md`
* `reports/resumen_ejecutivo.md`

---

## 11. ¿Cómo se generan los pronósticos (forecasts)?

### Proceso en notebook

El notebook `03_forecasting.ipynb`:

1. Carga `historico_equipos_limpio.csv`
2. Evalúa **Prophet** y **ARIMA** con validación temporal cronológica
3. Entrenamiento: 2010-01-04 a 2022-12-30 (3.358 registros)
4. Prueba: 2023-01-03 a 2023-08-31 (172 registros)
5. Proyecta un horizonte de **180 días**
6. Exporta CSVs a `data/processed/`

### Modelo seleccionado (según reportes)

**ARIMA** superó a Prophet en RMSE, MAE y MAPE para ambos equipos:

| Equipo | Modelo | MAPE (%) |
|---|---|---|
| Equipo 1 | ARIMA | 6.94 |
| Equipo 2 | ARIMA | 5.47 |

### Módulos de código

* `src/forecasting.py` — funciones `forecast_with_prophet()` y `forecast_with_arima()` (pmdarima)
* `src/dynamic_forecast.py` — forecast dinámico con `statsmodels.tsa.arima.model.ARIMA(1,1,1)` para fechas posteriores al histórico
* `src/tools.py` — consulta de forecasts precalculados desde CSV

### Inconsistencia detectada

Los reportes y conclusiones del notebook indican ARIMA como mejor modelo, pero la exportación de `forecast_equipo1.csv` y `forecast_equipo2.csv` en el notebook usa tablas derivadas de **Prophet** (`forecast_equipo1_tail` / `forecast_equipo2_tail`), no de ARIMA.

**Evidencia encontrada:**

* `notebooks/03_forecasting.ipynb`
* `src/forecasting.py`
* `src/dynamic_forecast.py`
* `src/tools.py`
* `reports/resultados_forecasting.md`

---

## 12. ¿Cómo funciona el sistema RAG del agente?

El agente implementa un patrón de **recuperación aumentada por generación (RAG)** con las siguientes características:

### Fuentes de conocimiento

Cinco archivos Markdown en `reports/`:

* `resumen_ejecutivo.md`
* `resultados_eda.md`
* `resultados_modelado.md`
* `resultados_forecasting.md`
* `preguntas_frecuentes.md`

### Recuperación de contexto

1. **Con Azure AI Search configurado:** búsqueda textual (`search_text`) sobre un índice con campos `content`, `source` y `category`. El índice se construye con `scripts/build_search_index.py` (fragmentación por párrafos, analizador `es.microsoft`).
2. **Sin Azure:** fallback que carga todos los documentos Markdown locales.

### Generación

* Modelo: **Google Gemini** (`gemini-2.5-flash-lite`) vía `langchain_google_genai`
* Prompt con reglas para no inventar cifras y responder en español
* Memoria conversacional: últimos 8 mensajes enviados desde FastAPI

### Herramientas complementarias (no LLM)

* **Simulación de escenarios:** `simulate_material_change()` — impacto lineal de cambios en materias primas
* **Forecast por fecha:** `get_forecast_by_date()` — consulta CSV precalculado
* **Forecast dinámico:** `get_dynamic_forecast_by_date()` — ARIMA on-the-fly para fechas futuras

**Nota:** Aunque `README.md` y `requirements.txt` mencionan ChromaDB y OpenAI, el código actual usa **Azure AI Search + Gemini**, no ChromaDB ni OpenAI.

**Evidencia encontrada:**

* `src/agent.py`
* `src/tools.py`
* `src/dynamic_forecast.py`
* `scripts/build_search_index.py`
* `scripts/test_search.py`
* `README.md` (descripción desactualizada)
* `.gitignore` (carpeta `chroma_db/`)

---

## 13. ¿Qué servicios de Azure utiliza el proyecto?

Se identificó uso de **Azure AI Search** (anteriormente Azure Cognitive Search):

* SDK: `azure-search-documents`
* Variables: `AZURE_SEARCH_ENDPOINT`, `AZURE_SEARCH_KEY`, `AZURE_SEARCH_INDEX_NAME`
* Operaciones: creación/actualización de índice, carga de documentos y búsqueda

No se encontró evidencia de otros servicios Azure (Blob Storage, Azure ML, Azure OpenAI, App Service, etc.).

**Evidencia encontrada:**

* `src/agent.py`
* `scripts/build_search_index.py`
* `scripts/test_search.py`
* `requirements.txt` (`azure-core`, `azure-search-documents`)

---

## 14. ¿Qué APIs externas consume el proyecto?

| API / Servicio | Propósito |
|---|---|
| Google Gemini API | Generación de respuestas del agente (`GOOGLE_API_KEY`) |
| Azure AI Search | Recuperación de contexto documental (opcional) |
| CDN jsDelivr | Librería `marked` para renderizar Markdown en el frontend (`app/templates/index.html`) |

**Evidencia encontrada:**

* `src/agent.py`
* `scripts/build_search_index.py`
* `app/templates/index.html`

---

## 15. ¿Utiliza bases de datos?

No se encontró evidencia de bases de datos relacionales o NoSQL. El almacenamiento es **basado en archivos CSV** locales y documentos Markdown. Azure AI Search actúa como motor de búsqueda de texto, no como base de datos transaccional.

**Evidencia encontrada:**

* `src/tools.py`
* `src/preprocessing.py`
* `src/dynamic_forecast.py`
* `src/agent.py`

---

## 16. ¿Cómo se realiza el despliegue?

No se encontró evidencia suficiente en el repositorio para responder esta pregunta de forma operativa.

No existen en el repositorio:

* `Dockerfile` ni `docker-compose.yml`
* Pipelines CI/CD (`.github/workflows/`, etc.)
* Infraestructura como código (Terraform, Bicep, ARM)
* Carpeta `architecture/` con diagramas o guías de despliegue (mencionada en `README.md` pero ausente)
* Scripts de despliegue a cloud

El `README.md` menciona "Arquitectura cloud" como objetivo propuesto, y `reports/informe.md` lista mejoras futuras (MLOps, reentrenamiento automático), pero sin implementación concreta.

**Evidencia encontrada:**

* `README.md` (objetivo y checklist pendiente)
* `reports/informe.md` (mejoras futuras propuestas)
* Ausencia de archivos de despliegue en el repositorio

---

## 17. ¿Cómo se monitorea el sistema?

La única evidencia de monitoreo es el endpoint de salud de FastAPI:

```
GET /health
```

Retorna `status: ok` y el resultado de `check_agent_ready()` (disponibilidad de archivos de conocimiento, clave de Google y configuración de Azure Search).

No se encontraron integraciones de observabilidad (Application Insights, Prometheus, logging estructurado, alertas). Aunque `requirements.txt` incluye paquetes OpenTelemetry, no se encontró configuración ni uso en el código del proyecto.

**Evidencia encontrada:**

* `app/main.py`
* `src/agent.py` (`check_agent_ready()`)
* `requirements.txt` (OpenTelemetry como dependencia transitiva, sin uso directo)

---

## 18. ¿Qué interfaces tiene el usuario final?

### FastAPI + UI web (funcional para el agente)

* Ruta `/` — chat HTML con historial en `localStorage`
* Ruta `/chat` — API POST para preguntas
* Ejemplos de preguntas predefinidos en la interfaz

> **Decisión de arquitectura (persistencia conversacional):** el backend es *stateless*; el historial se guarda en `localStorage` del navegador y el cliente lo reenvía a `/chat` en cada petición. Esto permite escalar el servidor horizontalmente sin estado de sesión. Como contrapartida, no hay continuidad entre dispositivos ni multiusuario real; el siguiente paso natural sería autenticación + persistencia server-side por usuario.

### Streamlit (parcialmente implementada)

* Páginas: Inicio, Análisis Exploratorio, Proyecciones, Agente IA
* Las secciones de EDA, Proyecciones y Agente IA muestran mensajes **"Pendiente"** y no están conectadas a `agent.py`

**Evidencia encontrada:**

* `app/main.py`
* `app/templates/index.html`
* `app/static/app.js`
* `app/streamlit_app.py`

---

## 19. ¿Qué limitaciones conocidas tiene el proyecto?

1. **Datos no versionados:** los CSV están en `.gitignore`; el proyecto no funciona sin ejecutar notebooks o aportar datos localmente.
2. **Modelos no persistidos:** coeficientes hardcodeados en `tools.py`; no hay pipeline de reentrenamiento automático.
3. **Inconsistencia Prophet vs ARIMA:** reportes seleccionan ARIMA, pero CSVs exportados provienen de Prophet.
4. **Documentación desactualizada:** `README.md` referencia ChromaDB, OpenAI y `OPENAI_API_KEY`; el código usa Gemini y Azure AI Search.
5. **Streamlit incompleta:** UI principal del README no conecta el agente ni visualiza resultados.
6. **Sin variables externas:** no considera inflación, TRM, contratos, logística ni shocks de mercado.
7. **Simulaciones lineales:** `simulate_material_change()` advierte que es aproximación lineal, no predicción definitiva.
8. **Sin despliegue ni tests automatizados:** no hay suite de pruebas unitarias ni integración continua.
9. **Informe técnico parcial:** `reports/informe.md` marca varias secciones como "Pendiente por completar".

**Evidencia encontrada:**

* `src/tools.py`
* `src/agent.py`
* `notebooks/03_forecasting.ipynb`
* `app/streamlit_app.py`
* `README.md`
* `reports/informe.md`
* `reports/preguntas_frecuentes.md`
* `.gitignore`

---

## 20. ¿Qué mejoras futuras podrían implementarse?

### Propuestas documentadas en el repositorio (`reports/informe.md`)

* Incorporar variables externas (índices macroeconómicos, TRM, energía)
* Reentrenamiento automático con pipelines MLOps (Airflow, Step Functions)
* Detección de cambios estructurales en series
* Modelos avanzados (LSTM, Transformers)
* Interfaz Streamlit más completa con dashboards y descarga de reportes
* Seguridad y autenticación en entornos productivos

### Mejoras inferibles por deuda técnica detectada

* Alinear exportación de forecasts con el modelo ARIMA seleccionado
* Conectar `streamlit_app.py` con `agent.py` y visualizaciones reales
* Actualizar `README.md` para reflejar Gemini + Azure AI Search
* Persistir modelos entrenados y automatizar su recarga
* Agregar `Dockerfile` y documentación de despliegue
* Implementar tests automatizados
* Completar carpeta `architecture/` prometida en el README

**Evidencia encontrada:**

* `reports/informe.md`
* `README.md` (checklist de estado)
* Análisis cruzado de `notebooks/`, `src/` y `app/`

---

## 21. ¿Cuál es el flujo recomendado para un nuevo desarrollador?

1. Clonar el repositorio y crear entorno virtual
2. `pip install -r requirements.txt`
3. Colocar `historico_equipos.csv` en `data/raw/` (o ejecutar notebook 01 si ya existe)
4. Ejecutar notebooks 01 → 02 → 03 en orden
5. Configurar `.env` con `GOOGLE_API_KEY` (y opcionalmente variables de Azure Search)
6. (Opcional) `python scripts/build_search_index.py` para indexar reportes en Azure
7. Levantar `uvicorn app.main:app --reload` para probar el agente
8. Verificar estado con `GET /health` o `python src/agent.py`

**Evidencia encontrada:**

* `README.md`
* `notebooks/01_exploracion_datos.ipynb`
* `app/main.py`
* `scripts/build_search_index.py`
* `src/agent.py`

---

## 22. ¿Cuál es el flujo recomendado para un científico de datos?

1. **EDA:** `notebooks/01_exploracion_datos.ipynb` — correlaciones, calidad, hipótesis
2. **Modelado:** `notebooks/02_modelado_predictivo.ipynb` — regresión lineal vs Gradient Boosting con split temporal
3. **Forecasting:** `notebooks/03_forecasting.ipynb` — Prophet vs ARIMA, horizonte 180 días
4. **Documentación de resultados:** actualizar archivos en `reports/`
5. **Reindexar conocimiento:** `scripts/build_search_index.py` si se usa Azure Search
6. Reutilizar funciones de `src/modeling.py`, `src/forecasting.py` y `src/preprocessing.py` para mantener consistencia con el agente

**Evidencia encontrada:**

* `notebooks/01_exploracion_datos.ipynb`
* `notebooks/02_modelado_predictivo.ipynb`
* `notebooks/03_forecasting.ipynb`
* `src/modeling.py`
* `src/forecasting.py`
* `reports/`

---

## 23. ¿Qué debe saber un perfil DevOps sobre este proyecto?

* **Runtime:** Python 3.10+, sin contenedor definido
* **Secretos:** `GOOGLE_API_KEY`, `AZURE_SEARCH_*` vía `.env` (no commitear)
* **Dependencias:** `requirements.txt` extenso con versiones fijadas
* **Servicios externos:** Google Gemini API y Azure AI Search (opcional)
* **Health check:** `GET /health` en FastAPI
* **Sin evidencia de:** Docker, Kubernetes manifests, CI/CD, IaC, logging centralizado ni estrategia de despliegue documentada

**Evidencia encontrada:**

* `requirements.txt`
* `app/main.py`
* `.gitignore`
* `scripts/build_search_index.py`

---

## 24. ¿Qué puede consultar un usuario final a través del agente?

Ejemplos incluidos en la interfaz web:

* "¿Cuál fue el mejor modelo de forecasting y por qué?"
* "¿Qué materia prima afecta más al Equipo 1?"
* "¿Cuál es la proyección del Equipo 2?"

El agente también responde preguntas de:

* **Simulación de escenarios** — si detecta materia prima (X/Y/Z), porcentaje y equipo en la pregunta
* **Forecast por fecha** — si detecta palabras clave de pronóstico y una fecha con formato `YYYY-MM-DD` o `DD/MM/YYYY`

**Evidencia encontrada:**

* `app/templates/index.html`
* `src/agent.py` (`detect_scenario_question`, `detect_forecast_date_question`)
* `reports/preguntas_frecuentes.md`

---

## 25. ¿Qué evalúa este proyecto desde la perspectiva de un reclutador o evaluador técnico?

Es una **prueba técnica de Científica de Datos / IA** para DataKnow (2026) que demuestra:

* Pipeline completo de datos: EDA → modelado → forecasting → documentación
* Selección fundamentada de modelos con métricas (R², RMSE, MAE, MAPE)
* Integración de IA generativa con recuperación de contexto (RAG)
* API REST con FastAPI y frontend de chat
* Uso de servicios cloud (Azure AI Search)
* Comunicación de resultados mediante reportes ejecutivos y FAQ de negocio

Áreas donde el evaluador podría profundizar: consistencia Prophet/ARIMA en exportación, documentación desactualizada del README, Streamlit incompleta y ausencia de despliegue productivo.

**Evidencia encontrada:**

* `README.md`
* `reports/informe.md`
* `reports/resumen_ejecutivo.md`
* Estructura general del repositorio

---

## 26. ¿Existen tests automatizados?

No se encontró evidencia de una suite de tests (pytest, unittest). El único script de prueba es `scripts/test_search.py`, que ejecuta una búsqueda manual contra Azure AI Search cuando se invoca directamente.

**Evidencia encontrada:**

* `scripts/test_search.py`
* Ausencia de carpetas `tests/` o archivos `test_*.py` en el proyecto

---

## 27. ¿Cuál es el estado actual del proyecto según el repositorio?

El `README.md` incluye un checklist donde varios ítems aparecen como pendientes (`[ ]`), pero el análisis del código y notebooks indica avance significativo en EDA, modelado, forecasting, módulos `src/`, agente y reportes. El checklist del README **no refleja el estado real** del desarrollo.

Ítems claramente pendientes o parciales:

* Datos en el repositorio (gitignored)
* Aplicación Streamlit desplegada/funcional
* Arquitectura cloud documentada
* Informe técnico finalizado (`reports/informe.md` parcial)

**Evidencia encontrada:**

* `README.md` (sección "Estado del Proyecto")
* `reports/informe.md`
* `app/streamlit_app.py`
* Notebooks y módulos `src/` implementados

---

# Hallazgos Técnicos Relevantes

## Arquitectura identificada

* **Patrón pipeline de datos** con separación `raw` → `processed` → `reports` → agente.
* **Doble interfaz:** FastAPI (operativa para el agente) y Streamlit (esqueleto UI).
* **RAG híbrido:** Azure AI Search con fallback a lectura local de Markdown; no usa embeddings vectoriales explícitos en el código del agente.
* **Herramientas determinísticas** acopladas al LLM mediante detección por regex (escenarios y forecasts por fecha).
* **Sin capa de persistencia** más allá de CSV y archivos Markdown.

## Patrones de diseño encontrados

* **Fallback graceful:** si Azure Search no está configurado, el agente carga documentos locales (`search_relevant_context` en `agent.py`).
* **Separación de responsabilidades:** `modeling.py`, `forecasting.py`, `tools.py`, `agent.py`.
* **Prompt engineering estructurado:** reglas explícitas en el system prompt para evitar alucinaciones.
* **Chunking de documentos** para indexación (`chunk_text` en `build_search_index.py`).
* **Chain de LangChain:** `prompt | llm` con `ChatPromptTemplate`.

## Riesgos técnicos

| Riesgo | Impacto |
|---|---|
| Coeficientes hardcodeados en `tools.py` | Desincronización si se reentrena el modelo sin actualizar el código |
| CSVs de forecast exportados desde Prophet | Respuestas del agente sobre pronósticos pueden no coincidir con el modelo ARIMA declarado como mejor |
| Dependencia de APIs externas (Gemini, Azure) | El agente falla sin `GOOGLE_API_KEY`; calidad de RAG depende de configuración Azure |
| Datos fuera del repositorio | Clon limpio no permite reproducir resultados sin datos locales |
| Sin autenticación en FastAPI | Exposición del agente si se despliega públicamente sin capa de seguridad |
| `requirements.txt` muy amplio | Superficie de dependencias grande; paquetes no usados (ChromaDB, OpenAI, XGBoost) |

## Deuda técnica

1. `README.md` desactualizado (ChromaDB/OpenAI vs Gemini/Azure Search; checklist de estado).
2. `app/streamlit_app.py` con TODOs sin implementar.
3. `reports/informe.md` con secciones pendientes pese a reportes de resultados completos.
4. Carpeta `architecture/` ausente.
5. Sin serialización ni versionado de modelos ML.
6. Inconsistencia en la fuente de forecasts exportados (Prophet) vs modelo seleccionado (ARIMA).
7. Comentario obsoleto en notebook 03 que menciona Prophet como modelo principal.

## Oportunidades de mejora

1. **Unificar pipeline de forecasting:** exportar CSVs desde ARIMA y alinear reportes, agente y herramientas.
2. **Automatizar sincronización de coeficientes** desde notebook de modelado hacia `tools.py`.
3. **Completar Streamlit** o consolidar en una sola interfaz (FastAPI o Streamlit).
4. **Reducir dependencias** eliminando paquetes no utilizados del entorno.
5. **Agregar contenedorización y CI/CD** para reproducibilidad y despliegue.
6. **Implementar tests** para `tools.py`, `dynamic_forecast.py` y endpoints de FastAPI.
7. **Completar documentación de arquitectura cloud** prometida en el README.
8. **Indexación incremental** de reportes tras cada ejecución de notebooks.
9. **Autenticación y rate limiting** antes de exposición productiva del agente.

---

*Documento generado en junio de 2026 a partir del análisis del repositorio `dataknow-costos-operativos`.*
