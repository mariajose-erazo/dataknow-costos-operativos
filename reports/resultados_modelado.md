# Resultados del Modelado Predictivo

## Equipo 1

### Regresión Lineal

Métricas:

* RMSE: 10.3088
* MAE: 8.8699
* R²: 0.9913

Coeficientes:

* Price_Y: 0.796755
* Price_X: 0.203392
* Price_Z: 0.001188

Interpretación:

Price_Y es la variable con mayor influencia sobre el precio del Equipo 1.

---

## Equipo 2

### Regresión Lineal

Métricas:

* RMSE: 19.3198
* MAE: 16.5514
* R²: 0.9853

Coeficientes:

* Price_X: 0.341043
* Price_Y: 0.332841
* Price_Z: 0.332109

Interpretación:

Las tres materias primas contribuyen al comportamiento del Equipo 2, aunque el análisis de importancia de variables mostró una influencia predominante de Price_Z.

---

## Gradient Boosting

Equipo 2:

* RMSE: 96.995
* MAE: 57.4077
* R²: 0.6289

Importancia de variables:

* Price_Z: 0.800184
* Price_Y: 0.192098
* Price_X: 0.007718

Conclusión:

La regresión lineal presentó mejor desempeño predictivo que Gradient Boosting para este conjunto de datos.
