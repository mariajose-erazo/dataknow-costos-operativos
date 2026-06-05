"""
preprocessing.py
----------------
Módulo de limpieza y preparación de datos.

Funciones principales:
- Carga de datos raw
- Limpieza de valores nulos
- Detección de outliers
- Normalización / escalado
- Generación de features temporales
"""

import pandas as pd
import numpy as np
from pathlib import Path

RAW_DATA_PATH = Path("data/raw")
PROCESSED_DATA_PATH = Path("data/processed")


def load_raw_data(filename: str) -> pd.DataFrame:
    """Carga un archivo CSV desde la carpeta data/raw."""
    filepath = RAW_DATA_PATH / filename
    return pd.read_csv(filepath, parse_dates=True)


def handle_missing_values(df: pd.DataFrame, strategy: str = "interpolate") -> pd.DataFrame:
    """
    Maneja valores nulos en el DataFrame.

    Estrategias disponibles:
    - 'interpolate': interpolación lineal (recomendada para series de tiempo)
    - 'ffill': forward fill
    - 'drop': elimina filas con nulos
    """
    if strategy == "interpolate":
        return df.interpolate(method="linear")
    elif strategy == "ffill":
        return df.ffill()
    elif strategy == "drop":
        return df.dropna()
    else:
        raise ValueError(f"Estrategia '{strategy}' no reconocida.")


def detect_outliers_iqr(series: pd.Series, factor: float = 1.5) -> pd.Series:
    """
    Detecta outliers usando el método IQR.
    Retorna una máscara booleana (True = outlier).
    """
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - factor * iqr
    upper = q3 + factor * iqr
    return (series < lower) | (series > upper)


def save_processed_data(df: pd.DataFrame, filename: str) -> None:
    """Guarda el DataFrame procesado en data/processed."""
    PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH / filename, index=False)
    print(f"Datos guardados en: {PROCESSED_DATA_PATH / filename}")
