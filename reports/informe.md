# Informe Técnico — Anticipación de Costos Operativos

**Proyecto:** Modelado predictivo de costos de equipos críticos  
**Empresa:** DataKnow  
**Fecha:** Junio 2026  
**Estado:** En desarrollo

---

## 1. Explicación del Caso

Una empresa constructora enfrenta el desafío de anticipar los costos futuros de dos equipos críticos para su operación: **Equipo 1** y **Equipo 2**. Estos equipos están directamente relacionados con el precio de mercado de tres materias primas: **X**, **Y** y **Z**.

La empresa cuenta con datos históricos de los precios de estas materias primas y de los equipos. El problema tiene dos dimensiones:

- **Explicativa:** ¿qué materias primas determinan el precio de cada equipo, y en qué medida?
- **Predictiva:** ¿cuáles serán los costos futuros de los equipos dado el comportamiento esperado de las materias primas?

La solución completa incluye análisis estadístico, modelos de machine learning y series de tiempo, un agente conversacional que responde preguntas de negocio, y una propuesta de arquitectura cloud para productivizar la solución.

---

## 2. Supuestos

- Los datos históricos proporcionados son representativos del comportamiento real del mercado.
- Las relaciones entre materias primas y precios de equipos son estables en el tiempo (no hay cambios estructurales abruptos sin explicación).
- Las proyecciones de materias primas futuras se construyen a partir de sus propias tendencias históricas, en ausencia de datos externos adicionales.
- Se asume que las series de tiempo no tienen gaps significativos ni errores sistemáticos de medición.
- El horizonte de proyección se definirá en función de la cantidad de datos disponibles y la estabilidad de los modelos.

> **Pendiente por completar:** ajustar supuestos una vez revisados los datos reales.

---

## 3. Formas para Resolver el Caso y la Opción Tomada

### Enfoques considerados

**Opción A — Modelos de regresión pura:**  
Regresión lineal múltiple, Ridge, Lasso o modelos de árbol (XGBoost, LightGBM) usando las materias primas como variables independientes y el precio del equipo como variable dependiente. Es interpretable y permite cuantificar el impacto de cada materia prima.

**Opción B — Modelos de series de tiempo univariados:**  
ARIMA/SARIMA o Prophet sobre la serie del precio de cada equipo, sin usar las materias primas como covariables. Captura tendencias y estacionalidad, pero ignora las relaciones causales.

**Opción C — Modelos de series de tiempo multivariados (enfoque híbrido):**  
VAR (Vector Autoregression) o modelos de regresión con rezagos temporales, combinando la dinámica temporal con el efecto de las materias primas. Es el enfoque más completo pero también el más complejo.

### Opción tomada en esta prueba

> **Pendiente por completar:** se definirá tras el análisis exploratorio. Se evaluarán los enfoques A y C, comparando métricas de error (RMSE, MAE, R²) y eligiendo el que mejor balance ofrezca entre precisión e interpretabilidad.

---

## 4. Resultados del Análisis de los Datos y los Modelos

> **Pendiente por completar** una vez ejecutado el análisis exploratorio y el modelado.

### 4.1 Análisis exploratorio

- Estadísticas descriptivas de materias primas y equipos
- Distribuciones y detección de outliers
- Análisis de correlación (Pearson, Spearman)
- Análisis de multicolinealidad

### 4.2 Selección de variables

- Materias primas más relevantes para Equipo 1: *por determinar*
- Materias primas más relevantes para Equipo 2: *por determinar*

### 4.3 Resultados de los modelos

| Modelo | Equipo | RMSE | MAE | R² |
|---|---|---|---|---|
| *Por completar* | Equipo 1 | — | — | — |
| *Por completar* | Equipo 2 | — | — | — |

---

## 5. Proyección de Costos y Horizonte de Predicción

> **Pendiente por completar** una vez entrenados los modelos finales.

- **Horizonte de predicción:** *por determinar en función de los datos*
- **Método de proyección:** *por determinar*
- **Intervalos de confianza:** se reportarán bandas del 80% y 95%

### Resultados de proyección

| Período | Equipo 1 — Proyección | IC 80% | IC 95% |
|---|---|---|---|
| *Por completar* | — | — | — |

| Período | Equipo 2 — Proyección | IC 80% | IC 95% |
|---|---|---|---|
| *Por completar* | — | — | — |

---

## 6. Futuros Ajustes o Mejoras

Las siguientes mejoras podrían implementarse en iteraciones futuras del proyecto:

- **Incorporar variables externas:** índices macroeconómicos, tasas de cambio, precios de energía u otras variables que puedan mejorar el poder predictivo de los modelos.
- **Reentrenamiento automático:** implementar pipelines de MLOps que reentrenan los modelos periódicamente con datos nuevos (por ejemplo, usando Airflow o Step Functions en AWS).
- **Detección de cambios estructurales:** agregar alertas automáticas cuando se detecten cambios en el comportamiento de las series que invaliden los supuestos del modelo.
- **Modelos más avanzados:** explorar redes neuronales recurrentes (LSTM) o modelos de atención (Transformer) para capturar dependencias temporales complejas.
- **Interfaz más completa:** expandir la aplicación Streamlit con dashboards interactivos, descarga de reportes y configuración de parámetros del agente.
- **Seguridad y autenticación:** agregar control de acceso a la aplicación y al agente en entornos productivos.

---

## 7. Apreciaciones y Comentarios del Caso

> **Pendiente por completar** con reflexiones finales tras culminar el análisis.

Algunas reflexiones preliminares:

- El problema combina análisis estadístico clásico con herramientas modernas de IA, lo que lo hace particularmente interesante desde la perspectiva de ingeniería de datos.
- La selección correcta de variables es crítica: un modelo con pocas variables bien elegidas puede superar a uno complejo con ruido innecesario.
- La incertidumbre en las proyecciones no debe subestimarse — comunicar los intervalos de confianza es tan importante como la proyección puntual.
- La experiencia del usuario final (a través del agente conversacional y la app Streamlit) es parte fundamental de la solución, no solo el modelo subyacente.

---

*Informe generado como parte de la prueba técnica DataKnow — Científica de Datos / IA*
