"""
modeling.py
-----------
Módulo de entrenamiento y evaluación de modelos predictivos.

Incluye:
- Regresión lineal, Ridge, Lasso
- XGBoost / LightGBM
- Evaluación con métricas: RMSE, MAE, R²
- Selección de features por importancia
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split, cross_val_score
from typing import Tuple, Dict


def split_data(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple:
    """Divide los datos en conjuntos de entrenamiento y prueba."""
    return train_test_split(X, y, test_size=test_size, random_state=random_state)


def evaluate_model(model, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, float]:
    """
    Evalúa un modelo entrenado y retorna métricas de desempeño.

    Retorna:
        dict con RMSE, MAE y R²
    """
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return {"RMSE": round(rmse, 4), "MAE": round(mae, 4), "R2": round(r2, 4)}


def train_linear_model(X_train, y_train, model_type: str = "linear"):
    """
    Entrena un modelo de regresión lineal.

    model_type: 'linear', 'ridge', 'lasso'
    """
    models = {
        "linear": LinearRegression(),
        "ridge": Ridge(alpha=1.0),
        "lasso": Lasso(alpha=0.1),
    }
    if model_type not in models:
        raise ValueError(f"Tipo de modelo '{model_type}' no reconocido.")
    model = models[model_type]
    model.fit(X_train, y_train)
    return model


def get_feature_importance(model, feature_names: list) -> pd.DataFrame:
    """
    Extrae la importancia de variables de un modelo basado en árboles.
    Compatible con GradientBoosting, XGBoost, LightGBM.
    """
    if not hasattr(model, "feature_importances_"):
        raise AttributeError("El modelo no tiene atributo 'feature_importances_'.")
    importance_df = pd.DataFrame({
        "feature": feature_names,
        "importance": model.feature_importances_
    }).sort_values("importance", ascending=False)
    return importance_df

def time_series_split_data(
    df: pd.DataFrame,
    feature_cols: list,
    target_col: str,
    date_col: str = "Date",
    test_size: float = 0.2
):
    """
    Divide un dataset temporal en entrenamiento y prueba respetando el orden cronológico.
    """

    df_sorted = df.sort_values(date_col).reset_index(drop=True).copy()

    split_idx = int(len(df_sorted) * (1 - test_size))

    train_df = df_sorted.iloc[:split_idx].copy()
    test_df = df_sorted.iloc[split_idx:].copy()

    X_train = train_df[feature_cols]
    X_test = test_df[feature_cols]

    y_train = train_df[target_col]
    y_test = test_df[target_col]

    return X_train, X_test, y_train, y_test, train_df, test_df

def train_gradient_boosting_model(X_train, y_train, random_state: int = 42):
    """
    Entrena un modelo Gradient Boosting Regressor.

    Este modelo permite capturar relaciones no lineales entre las materias primas
    y el precio de los equipos. Además, permite obtener importancia de variables.
    """
    model = GradientBoostingRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=3,
        random_state=random_state
    )

    model.fit(X_train, y_train)
    return model