# Resumen Ejecutivo

Este proyecto analiza los costos históricos de dos equipos críticos en un proyecto de construcción, junto con los precios históricos de tres materias primas: Price_X, Price_Y y Price_Z.

El objetivo es identificar qué materias primas explican el comportamiento de cada equipo y proyectar los costos futuros para apoyar la planeación financiera.

## Hallazgos principales

- El dataset contiene 3.530 registros diarios entre 2010-01-04 y 2023-08-31.
- No se encontraron valores faltantes.
- El Equipo 1 está principalmente relacionado con Price_Y.
- El Equipo 2 está principalmente relacionado con Price_Z.
- La regresión lineal fue el mejor modelo para explicar los precios de los equipos.
- ARIMA fue el mejor modelo de forecasting frente a Prophet.
- Para el Equipo 1 se proyecta una variación aproximada de +0.95%.
- Para el Equipo 2 se proyecta una variación aproximada de -1.46%.

## Recomendación general

Se recomienda monitorear especialmente Price_Y para decisiones relacionadas con el Equipo 1 y Price_Z para decisiones relacionadas con el Equipo 2.

Las proyecciones deben interpretarse como escenarios estimados y no como valores exactos, debido a la incertidumbre propia de los precios de mercado.