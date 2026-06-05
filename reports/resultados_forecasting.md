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
- Precio promedio proyectado: 452.58
- Mínimo proyectado: 414.70
- Máximo proyectado: 488.38
- Variación esperada: 0.19%

### Equipo 2

- Precio actual: 955.35
- Precio promedio proyectado: 1069.38
- Mínimo proyectado: 1043.33
- Máximo proyectado: 1114.74
- Variación esperada: 11.94%

---

## Conclusiones

- ARIMA superó ampliamente a Prophet.
- El Equipo 1 presenta estabilidad relativa en el horizonte proyectado.
- El Equipo 2 presenta una expectativa de crecimiento cercana al 12%.
- Las proyecciones deben interpretarse como escenarios probables y no como valores exactos.
- Los intervalos de confianza muestran la incertidumbre inherente a los mercados de materias primas.