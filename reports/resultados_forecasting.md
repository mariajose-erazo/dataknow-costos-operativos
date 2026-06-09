# Resultados de Forecasting

## Objetivo

Generar proyecciones de costos futuros para Equipo 1 y Equipo 2 utilizando modelos de series temporales.

---

## Validación Temporal

Se utilizó una validación cronológica:

- Entrenamiento: 2010-01-04 a 2022-12-30
- Prueba: 2023-01-03 a 2023-08-31

Cantidad de registros:

- Train: 3358
- Test: 172

Esta estrategia evita fuga de información futura hacia el entrenamiento.

---

## Comparación de Modelos

| Equipo | Modelo | RMSE | MAE | MAPE (%) |
|----------|----------|----------:|----------:|----------:|
| Equipo 1 | Prophet | 206.86 | 200.30 | 42.02 |
| Equipo 1 | ARIMA | 36.84 | 33.04 | 6.94 |
| Equipo 2 | Prophet | 387.72 | 379.73 | 39.23 |
| Equipo 2 | ARIMA | 63.06 | 52.74 | 5.47 |

---

## Mejor Modelo

### Equipo 1

Modelo seleccionado: ARIMA

Motivos:

- Menor RMSE
- Menor MAE
- Menor MAPE
- Mejor ajuste sobre datos reales

MAPE final: 6.94%

---

### Equipo 2

Modelo seleccionado: ARIMA

Motivos:

- Menor RMSE
- Menor MAE
- Menor MAPE
- Mejor comportamiento predictivo

MAPE final: 5.47%

---

## Proyecciones Futuras

Horizonte:

- 180 días

### Equipo 1

- Precio actual: 451.73
- Precio promedio proyectado: 456.03
- Mínimo proyectado: 455.90
- Máximo proyectado: 457.12
- Variación esperada: 0.95%

### Equipo 2

- Precio actual: 955.35
- Precio promedio proyectado: 941.42
- Mínimo proyectado: 941.42
- Máximo proyectado: 941.42
- Variación esperada: -1.46%

---

## Conclusiones

- ARIMA superó ampliamente a Prophet.
- El Equipo 1 presenta estabilidad relativa en el horizonte proyectado, con una variación esperada cercana a +0.95%.
- El Equipo 2 también se proyecta estable, con una ligera variación esperada de -1.46% respecto al último precio observado.
- Las proyecciones deben interpretarse como escenarios probables y no como valores exactos.
- Los intervalos de confianza muestran la incertidumbre inherente a los mercados de materias primas.