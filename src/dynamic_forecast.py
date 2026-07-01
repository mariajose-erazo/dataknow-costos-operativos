from pathlib import Path
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

HISTORICAL_PATH = DATA_PROCESSED / "historico_equipos_limpio.csv"
METADATA_PATH = DATA_PROCESSED / "forecast_metadata.json"

FORECAST_PATHS = {
    1: DATA_PROCESSED / "forecast_equipo1.csv",
    2: DATA_PROCESSED / "forecast_equipo2.csv",
}


def _validate_equipo(equipo: int) -> None:
    if equipo not in FORECAST_PATHS:
        raise ValueError("Equipo debe ser 1 o 2.")


def _load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {path}")

    df = pd.read_csv(path, parse_dates=["Date"])
    return df.sort_values("Date").reset_index(drop=True)


def _load_metadata() -> dict[str, Any]:
    if not METADATA_PATH.exists():
        return {}

    return pd.read_json(METADATA_PATH, typ="series").to_dict()


def _classify_uncertainty(uncertainty_pct: float) -> str:
    if uncertainty_pct < 20:
        return "Baja"

    if uncertainty_pct < 50:
        return "Media"

    if uncertainty_pct < 100:
        return "Alta"

    return "Muy Alta"


def _classify_horizon(days_ahead: int) -> str:
    if days_ahead <= 180:
        return "Corto plazo"

    if days_ahead <= 365:
        return "Mediano plazo"

    return "Largo plazo"


def _build_historical_response(
    equipo: int,
    fecha: str,
    target_date: pd.Timestamp,
    historical_df: pd.DataFrame,
    last_historical_date: pd.Timestamp,
) -> dict[str, Any]:
    value_col = f"Price_Equipo{equipo}"

    row = historical_df[historical_df["Date"] == target_date]

    if row.empty:
        return {
            "found": False,
            "type": "historical",
            "message": (
                f"La fecha {fecha} está dentro del histórico, "
                "pero no existe registro exacto para ese día."
            ),
            "last_historical_date": str(last_historical_date.date()),
        }

    return {
        "found": True,
        "type": "historical",
        "equipo": equipo,
        "fecha": str(target_date.date()),
        "value": round(float(row.iloc[0][value_col]), 2),
        "last_historical_date": str(last_historical_date.date()),
    }


def _build_forecast_response(
    equipo: int,
    target_date: pd.Timestamp,
    forecast_df: pd.DataFrame,
    metadata: dict[str, Any],
    last_historical_date: pd.Timestamp,
) -> dict[str, Any]:
    row = forecast_df[forecast_df["Date"] == target_date]

    if row.empty:
        return {
            "found": False,
            "type": "forecast",
            "equipo": equipo,
            "fecha": str(target_date.date()),
            "message": (
                "La fecha solicitada no existe dentro del forecast operativo "
                "generado por el Notebook 03."
            ),
            "last_historical_date": str(last_historical_date.date()),
        }

    row = row.iloc[0]

    forecast_value = float(row["Forecast"])
    lower = float(row["Lower"])
    upper = float(row["Upper"])

    uncertainty_width = upper - lower
    uncertainty_pct = uncertainty_width / forecast_value * 100

    days_ahead = (target_date - last_historical_date).days

    return {
        "found": True,
        "type": "operational_forecast",
        "equipo": equipo,
        "fecha": str(target_date.date()),
        "last_historical_date": str(last_historical_date.date()),
        "days_ahead": days_ahead,
        "forecast": round(forecast_value, 2),
        "lower_bound": round(lower, 2),
        "upper_bound": round(upper, 2),
        "uncertainty_pct": round(float(uncertainty_pct), 2),
        "uncertainty_level": _classify_uncertainty(uncertainty_pct),
        "forecast_horizon": _classify_horizon(days_ahead),
        "model": metadata.get("modelo", "ARIMA(1, 1, 1)"),
        "source_file": FORECAST_PATHS[equipo].name,
    }


def get_dynamic_forecast_by_date(
    equipo: int,
    fecha: str,
) -> dict[str, Any]:
    """
    Consulta el forecast operativo generado por el Notebook 03.

    Esta función no entrena modelos en tiempo de consulta.
    Lee los artefactos persistidos en data/processed y devuelve
    el valor esperado, el límite inferior y el límite superior para
    la fecha solicitada.
    """

    _validate_equipo(equipo)

    historical_df = _load_csv(HISTORICAL_PATH)
    forecast_df = _load_csv(FORECAST_PATHS[equipo])
    metadata = _load_metadata()

    target_date = pd.Timestamp(fecha)

    last_historical_date = historical_df["Date"].max()
    forecast_start_date = forecast_df["Date"].min()
    forecast_end_date = forecast_df["Date"].max()

    if target_date <= last_historical_date:
        return _build_historical_response(
            equipo=equipo,
            fecha=fecha,
            target_date=target_date,
            historical_df=historical_df,
            last_historical_date=last_historical_date,
        )

    if target_date < forecast_start_date or target_date > forecast_end_date:
        return {
            "found": False,
            "type": "out_of_forecast_horizon",
            "equipo": equipo,
            "fecha": str(target_date.date()),
            "message": (
                "La fecha solicitada está fuera del horizonte operativo "
                "generado por el Notebook 03."
            ),
            "last_historical_date": str(last_historical_date.date()),
            "forecast_start_date": str(forecast_start_date.date()),
            "forecast_end_date": str(forecast_end_date.date()),
            "model": metadata.get("modelo", "ARIMA(1, 1, 1)"),
        }

    return _build_forecast_response(
        equipo=equipo,
        target_date=target_date,
        forecast_df=forecast_df,
        metadata=metadata,
        last_historical_date=last_historical_date,
    )


if __name__ == "__main__":
    print(
        get_dynamic_forecast_by_date(
            equipo=1,
            fecha="2023-11-03",
        )
    )