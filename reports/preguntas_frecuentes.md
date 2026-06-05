# Preguntas Frecuentes del Proyecto

## Preguntas de negocio

### ¿Cuál era el objetivo del proyecto?

El objetivo fue analizar el comportamiento histórico de los costos de dos equipos críticos de construcción, identificar qué materias primas explican sus variaciones y proyectar sus costos futuros para apoyar la planeación financiera.

### ¿Qué beneficio le aporta esto a la empresa?

El análisis permite anticipar posibles desviaciones presupuestales, monitorear materias primas relevantes y contar con una metodología reproducible para estimar costos futuros.

### ¿Qué equipo representa mayor riesgo presupuestal?

El Equipo 2 representa mayor riesgo presupuestal porque su precio promedio proyectado aumenta aproximadamente 11.94% frente al último precio observado.

### ¿Qué decisión puede tomar la gerencia con estos resultados?

La gerencia puede priorizar el monitoreo de Price_Y para Equipo 1 y Price_Z para Equipo 2, ajustar presupuestos, anticipar compras y mejorar la negociación con proveedores.

---

## Preguntas sobre datos

### ¿Cuántos registros se analizaron?

Se analizaron 3.530 registros diarios.

### ¿Cuál fue el periodo analizado?

El periodo histórico va desde 2010-01-04 hasta 2023-08-31.

### ¿Había datos faltantes?

No se encontraron valores faltantes en el dataset.

### ¿En qué unidades están los precios?

Los datos no especifican una moneda particular. Por esta razón, los precios se interpretan como unidades monetarias genéricas.

### ¿Qué limitación importante tienen los datos?

Los datos solo contienen precios históricos de materias primas y equipos. No incluyen variables externas como inflación, TRM, noticias, contratos, proveedor, logística o cambios regulatorios.

---

## Preguntas sobre análisis exploratorio

### ¿Qué materia prima tiene mayor relación con el Equipo 1?

Price_Y presenta la relación más fuerte con el Equipo 1, con una correlación de 0.997.

### ¿Qué materia prima tiene mayor relación con el Equipo 2?

Price_Z presenta la relación más fuerte con el Equipo 2, con una correlación de 0.983.

### ¿Price_X es relevante?

Price_X muestra una correlación moderada con ambos equipos, pero no fue la variable dominante en los modelos ni en el análisis de importancia.

### ¿Las relaciones son estables en el tiempo?

Las correlaciones rodantes muestran que las relaciones principales se mantienen fuertes durante gran parte del periodo analizado, aunque pueden presentarse cambios temporales asociados a volatilidad de mercado.

---

## Preguntas sobre modelado predictivo

### ¿Qué modelo explicó mejor los costos históricos?

La regresión lineal presentó el mejor equilibrio entre precisión, simplicidad e interpretabilidad.

### ¿Qué tan bueno fue el modelo del Equipo 1?

El modelo lineal del Equipo 1 obtuvo RMSE de 10.3088, MAE de 8.8699 y R² de 0.9913.

### ¿Qué tan bueno fue el modelo del Equipo 2?

El modelo lineal del Equipo 2 obtuvo RMSE de 19.3198, MAE de 16.5514 y R² de 0.9853.

### ¿Qué significa R²?

R² indica qué porcentaje de la variación del precio puede explicar el modelo. Un R² de 0.9913 significa que el modelo explica aproximadamente el 99.13% de la variabilidad observada.

### ¿Por qué no se eligió Gradient Boosting como modelo principal?

Gradient Boosting tuvo peor desempeño que la regresión lineal en este conjunto de datos. Esto sugiere que la relación entre materias primas y equipos es predominantemente lineal.

---

## Preguntas sobre forecasting

### ¿Qué modelo se usó para proyectar costos futuros?

Se seleccionó ARIMA como modelo principal de forecasting.

### ¿Por qué ARIMA fue mejor que Prophet?

ARIMA obtuvo errores mucho menores en la validación temporal. Para Equipo 1 logró un MAPE de 6.94%, mientras Prophet obtuvo 42.02%. Para Equipo 2, ARIMA obtuvo 5.47%, mientras Prophet obtuvo 39.23%.

### ¿Qué significa MAPE?

MAPE significa error porcentual absoluto medio. Indica, en promedio, qué porcentaje se equivoca el modelo respecto al valor real.

### ¿Qué tan confiables son las proyecciones?

Las proyecciones de ARIMA presentan errores menores al 7% en validación temporal, lo cual se considera un desempeño muy bueno. Sin embargo, deben interpretarse como escenarios probables, no como valores exactos.

### ¿Cuál es la proyección para el Equipo 1?

El Equipo 1 presenta un precio actual de 451.73 y un precio promedio proyectado de 452.58, con una variación esperada de 0.19%.

### ¿Cuál es la proyección para el Equipo 2?

El Equipo 2 presenta un precio actual de 955.35 y un precio promedio proyectado de 1069.38, con una variación esperada de 11.94%.

---

## Preguntas sobre limitaciones

### ¿El modelo considera noticias, inflación o crisis internacionales?

No directamente. El modelo se basa en la información histórica disponible. Factores externos no presentes en los datos podrían afectar los costos futuros.

### ¿Qué pasa si ocurre un shock de mercado?

Si ocurre un shock de mercado, las predicciones podrían perder precisión. En ese caso se recomienda actualizar los datos y reentrenar los modelos.

### ¿Cada cuánto debería actualizarse el análisis?

Se recomienda actualizar el análisis cuando haya nuevos datos relevantes o antes de cada fase importante de planeación financiera.

---

## Preguntas sobre el agente de IA

### ¿Qué diferencia hay entre un chatbot normal y este agente?

Un chatbot normal responde con conocimiento general. Este agente consulta documentos del proyecto, resultados de modelos y herramientas específicas antes de responder.

### ¿El agente puede inventar respuestas?

El agente debe estar diseñado para responder con base en los documentos del proyecto. Si no encuentra información suficiente, debe indicarlo en lugar de inventar.

### ¿Qué herramientas puede usar el agente?

Puede consultar documentos del proyecto, recuperar resultados de forecasting, explicar métricas y eventualmente combinar información interna con contexto externo de mercado.