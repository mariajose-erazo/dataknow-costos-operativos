# Resultados del Análisis Exploratorio (EDA)

## Información general del dataset

* Registros: 3.530 observaciones diarias.
* Periodo analizado: 2010-01-04 a 2023-08-31.
* Variables:

  * Price_X
  * Price_Y
  * Price_Z
  * Price_Equipo1
  * Price_Equipo2

## Calidad de datos

* No se encontraron valores faltantes.
* No se identificaron problemas de consistencia en las fechas.
* Las series presentan continuidad temporal.

## Hallazgos principales

### Correlaciones

Equipo 1:

* Correlación con Price_X: 0.523
* Correlación con Price_Y: 0.997
* Correlación con Price_Z: 0.844

Equipo 2:

* Correlación con Price_X: 0.530
* Correlación con Price_Y: 0.913
* Correlación con Price_Z: 0.983

### Estabilidad de relaciones

Las correlaciones rodantes muestran que las relaciones entre materias primas y equipos se mantienen fuertes durante la mayor parte del periodo analizado, aunque existen episodios temporales de debilitamiento asociados a cambios de mercado.

### Distribuciones

Los boxplots anuales muestran cambios estructurales en los precios a lo largo del tiempo, especialmente durante los periodos 2021-2022, donde se observan incrementos significativos y mayor volatilidad.
