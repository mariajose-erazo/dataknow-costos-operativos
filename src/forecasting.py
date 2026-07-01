"""
forecasting.py
--------------

Módulo de forecasting del MVP.

Contiene funciones reutilizables para validar modelos ARIMA,
generar pronósticos operativos y preparar artefactos consumibles
por la Forecast Tool del asistente.
"""

from pathlib import Path
from typing import Any
import json

import numpy as np
import pandas as pd

from statsmodels.tsa.arima.model import ARIMA


DEFAULT_ARIMA_ORDER = (1, 1, 1)
DEFAULT_FORECAST_HORIZON_DAYS = 180


def load_historical_data(
    path: str | Path,
    date_col: str = "Date",
) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=[date_col])
    return df.sort_values(date_col).reset_index(drop=True)


def split_temporal_data(
    df: pd.DataFrame,
    split_date: str | pd.Timestamp,
    date_col: str = "Date",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    split_date = pd.Timestamp(split_date)

    train_df = df[df[date_col] < split_date].copy()
    test_df = df[df[date_col] >= split_date].copy()

    return train_df, test_df


def fit_arima(
    series: pd.Series,
    order: tuple[int, int, int] = DEFAULT_ARIMA_ORDER,
) -> Any:
    clean_series = series.astype(float).reset_index(drop=True)

    model = ARIMA(
        clean_series,
        order=order,
    )

    return model.fit()


def generate_forecast(
    model: Any,
    start_date: str | pd.Timestamp,
    periods: int = DEFAULT_FORECAST_HORIZON_DAYS,
    freq: str = "D",
) -> pd.DataFrame:
    dates = pd.date_range(
        start=pd.Timestamp(start_date),
        periods=periods,
        freq=freq,
    )

    forecast_result = model.get_forecast(steps=periods)
    conf_int = forecast_result.conf_int().reset_index(drop=True)

    forecast_df = pd.DataFrame({
        "Date": dates,
        "Forecast": forecast_result.predicted_mean.reset_index(drop=True),
        "Lower": conf_int.iloc[:, 0],
        "Upper": conf_int.iloc[:, 1],
    })

    return forecast_df


def add_uncertainty_columns(
    forecast_df: pd.DataFrame,
) -> pd.DataFrame:
    result = forecast_df.copy()

    result["Dia_horizonte"] = range(1, len(result) + 1)
    result["Ancho_IC"] = result["Upper"] - result["Lower"]
    result["Ancho_IC_%"] = result["Ancho_IC"] / result["Forecast"] * 100

    return result


def evaluate_forecast(
    y_true: pd.Series,
    y_pred: pd.Series,
    lower: pd.Series | None = None,
    upper: pd.Series | None = None,
    equipo: str | None = None,
) -> pd.DataFrame:
    y_true = y_true.reset_index(drop=True).astype(float)
    y_pred = y_pred.reset_index(drop=True).astype(float)

    error = y_true - y_pred
    error_abs = error.abs()
    error_pct = error_abs / y_true * 100

    metrics = {
        "MAE": error_abs.mean(),
        "RMSE": np.sqrt((error ** 2).mean()),
        "MAPE_%": error_pct.mean(),
    }

    if lower is not None and upper is not None:
        lower = lower.reset_index(drop=True).astype(float)
        upper = upper.reset_index(drop=True).astype(float)

        metrics["Cobertura_IC_%"] = (
            y_true.between(lower, upper).mean() * 100
        )

    if equipo is not None:
        metrics = {
            "Equipo": equipo,
            **metrics,
        }

    return pd.DataFrame([metrics])


def validate_arima(
    df: pd.DataFrame,
    target_col: str,
    split_date: str | pd.Timestamp,
    order: tuple[int, int, int] = DEFAULT_ARIMA_ORDER,
    date_col: str = "Date",
    equipo: str | None = None,
) -> tuple[Any, pd.DataFrame, pd.DataFrame]:
    train_df, test_df = split_temporal_data(
        df=df,
        split_date=split_date,
        date_col=date_col,
    )

    model = fit_arima(
        series=train_df[target_col],
        order=order,
    )

    forecast_df = generate_forecast(
        model=model,
        start_date=test_df[date_col].min(),
        periods=len(test_df),
        freq="D",
    )

    validation_df = pd.DataFrame({
        "Date": test_df[date_col].reset_index(drop=True),
        "Real": test_df[target_col].reset_index(drop=True),
        "Forecast": forecast_df["Forecast"],
        "Lower": forecast_df["Lower"],
        "Upper": forecast_df["Upper"],
    })

    metrics_df = evaluate_forecast(
        y_true=validation_df["Real"],
        y_pred=validation_df["Forecast"],
        lower=validation_df["Lower"],
        upper=validation_df["Upper"],
        equipo=equipo,
    )

    return model, validation_df, metrics_df


def summarize_uncertainty(
    forecasts: dict[str, pd.DataFrame],
    horizon_days: list[int] | tuple[int, ...] = (1, 30, 90, 180),
) -> pd.DataFrame:
    summaries = []

    for equipo, forecast_df in forecasts.items():
        enriched_df = add_uncertainty_columns(forecast_df)

        summary = enriched_df[
            enriched_df["Dia_horizonte"].isin(horizon_days)
        ].copy()

        summary["Equipo"] = equipo
        summaries.append(summary)

    result = pd.concat(summaries, ignore_index=True)

    return result[
        [
            "Equipo",
            "Dia_horizonte",
            "Date",
            "Forecast",
            "Lower",
            "Upper",
            "Ancho_IC",
            "Ancho_IC_%",
        ]
    ]


def save_forecast_csv(
    forecast_df: pd.DataFrame,
    path: str | Path,
) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    forecast_df.to_csv(path, index=False)

    return path


def build_forecast_metadata(
    model_name: str,
    horizon_days: int,
    last_historical_date: str | pd.Timestamp,
    forecast_start_date: str | pd.Timestamp,
    forecast_end_date: str | pd.Timestamp,
    forecast_files: dict[str, str],
    validation_metrics: pd.DataFrame,
    uncertainty_summary: pd.DataFrame,
) -> dict[str, Any]:
    return {
        "modelo": model_name,
        "horizonte_dias": horizon_days,
        "ultima_fecha_historica": str(pd.Timestamp(last_historical_date).date()),
        "fecha_inicio_forecast": str(pd.Timestamp(forecast_start_date).date()),
        "fecha_fin_forecast": str(pd.Timestamp(forecast_end_date).date()),
        "equipos": list(forecast_files.keys()),
        "archivos": forecast_files,
        "metricas_validacion": validation_metrics.to_dict(orient="records"),
        "resumen_incertidumbre": uncertainty_summary.to_dict(orient="records"),
    }


def save_metadata_json(
    metadata: dict[str, Any],
    path: str | Path,
) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        json.dumps(
            metadata,
            ensure_ascii=False,
            indent=4,
            default=str,
        ),
        encoding="utf-8",
    )

    return path


def load_forecast(
    path: str | Path,
) -> pd.DataFrame:
    return pd.read_csv(path, parse_dates=["Date"])


def get_forecast_by_date(
    forecast_df: pd.DataFrame,
    query_date: str | pd.Timestamp,
) -> dict[str, Any] | None:
    query_date = pd.Timestamp(query_date)

    result = forecast_df[forecast_df["Date"] == query_date]

    if result.empty:
        return None

    row = result.iloc[0]

    return {
        "Date": str(row["Date"].date()),
        "Forecast": float(row["Forecast"]),
        "Lower": float(row["Lower"]),
        "Upper": float(row["Upper"]),
    }