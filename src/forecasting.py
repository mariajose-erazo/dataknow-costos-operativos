"""
forecasting.py
--------------
Módulo de generación de proyecciones con incertidumbre.

Incluye:
- Proyecciones con Prophet
- Proyecciones con ARIMA (pmdarima)
- Generación de intervalos de confianza
- Visualización de forecasts
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Optional


def forecast_with_prophet(
    df: pd.DataFrame,
    date_col: str,
    value_col: str,
    periods: int = 12,
    freq: str = "M"
) -> pd.DataFrame:
    """
    Genera proyecciones usando Facebook Prophet.

    Args:
        df: DataFrame con columnas de fecha y valor
        date_col: nombre de la columna de fechas
        value_col: nombre de la columna de valores
        periods: número de períodos a proyectar
        freq: frecuencia ('D'=diario, 'W'=semanal, 'M'=mensual)

    Returns:
        DataFrame con proyecciones e intervalos de confianza
    """
    try:
        from prophet import Prophet
    except ImportError:
        raise ImportError("Instala prophet: pip install prophet")

    prophet_df = df[[date_col, value_col]].rename(columns={date_col: "ds", value_col: "y"})
    model = Prophet(interval_width=0.95)
    model.fit(prophet_df)
    future = model.make_future_dataframe(periods=periods, freq=freq)
    forecast = model.predict(future)
    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]


def forecast_with_arima(
    series: pd.Series,
    periods: int = 12,
    seasonal: bool = False
) -> pd.DataFrame:
    """
    Genera proyecciones usando ARIMA automático (pmdarima).

    Args:
        series: Serie temporal de valores
        periods: períodos a proyectar
        seasonal: si True, usa SARIMA

    Returns:
        DataFrame con proyecciones e intervalos de confianza
    """
    try:
        import pmdarima as pm
    except ImportError:
        raise ImportError("Instala pmdarima: pip install pmdarima")

    model = pm.auto_arima(series, seasonal=seasonal, stepwise=True, suppress_warnings=True)
    forecast, conf_int = model.predict(n_periods=periods, return_conf_int=True)
    result = pd.DataFrame({
        "forecast": forecast,
        "lower_80": conf_int[:, 0],
        "upper_80": conf_int[:, 1],
    })
    return result


def plot_forecast(
    historical: pd.Series,
    forecast_df: pd.DataFrame,
    title: str = "Proyección de costos",
    ylabel: str = "Precio"
) -> None:
    """Visualiza la serie histórica junto con la proyección e intervalos de confianza."""
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(historical.index, historical.values, label="Histórico", color="steelblue")
    ax.plot(forecast_df.index, forecast_df["forecast"], label="Proyección", color="darkorange", linestyle="--")
    if "lower_80" in forecast_df.columns:
        ax.fill_between(
            forecast_df.index,
            forecast_df["lower_80"],
            forecast_df["upper_80"],
            alpha=0.2,
            color="darkorange",
            label="IC 80%"
        )
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
