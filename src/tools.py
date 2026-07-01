from pathlib import Path
from typing import Any

import pandas as pd

try:
    from .dynamic_forecast import get_dynamic_forecast_by_date
except ImportError:
    from dynamic_forecast import get_dynamic_forecast_by_date


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_PATH = PROJECT_ROOT / "data" / "processed"

DATA_PATH = PROCESSED_PATH / "historico_equipos_limpio.csv"


LINEAR_COEFFICIENTS = {
    "Price_Equipo1": {
        "Price_X": 0.203392,
        "Price_Y": 0.796755,
        "Price_Z": 0.001188,
    },
    "Price_Equipo2": {
        "Price_X": 0.341043,
        "Price_Y": 0.332841,
        "Price_Z": 0.332109,
    },
}


VALID_MATERIALS = ["Price_X", "Price_Y", "Price_Z"]
VALID_TARGETS = ["Price_Equipo1", "Price_Equipo2"]


def load_latest_values() -> dict[str, Any]:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    df = df.sort_values("Date").reset_index(drop=True)

    latest = df.iloc[-1]

    return {
        "Date": str(latest["Date"].date()),
        "Price_X": float(latest["Price_X"]),
        "Price_Y": float(latest["Price_Y"]),
        "Price_Z": float(latest["Price_Z"]),
        "Price_Equipo1": float(latest["Price_Equipo1"]),
        "Price_Equipo2": float(latest["Price_Equipo2"]),
    }


def simulate_material_change(
    material: str,
    percent_change: float,
    target: str = "Price_Equipo2",
) -> dict[str, Any]:
    latest = load_latest_values()

    if material not in VALID_MATERIALS:
        raise ValueError("Materia prima no válida.")

    if target not in VALID_TARGETS:
        raise ValueError("Equipo objetivo no válido.")

    current_material_price = latest[material]
    current_target_price = latest[target]

    absolute_material_change = current_material_price * (percent_change / 100)
    coefficient = LINEAR_COEFFICIENTS[target][material]

    estimated_target_change = coefficient * absolute_material_change
    estimated_new_target_price = current_target_price + estimated_target_change

    estimated_target_percent_change = (
        estimated_target_change / current_target_price
    ) * 100

    return {
        "date": latest["Date"],
        "material": material,
        "target": target,
        "percent_change_material": round(percent_change, 2),
        "current_material_price": round(current_material_price, 2),
        "absolute_material_change": round(absolute_material_change, 2),
        "coefficient": round(coefficient, 6),
        "current_target_price": round(current_target_price, 2),
        "estimated_target_change": round(estimated_target_change, 2),
        "estimated_new_target_price": round(estimated_new_target_price, 2),
        "estimated_target_percent_change": round(
            estimated_target_percent_change,
            2,
        ),
    }


def get_forecast_by_date(
    equipo: int,
    fecha: str,
) -> dict[str, Any]:
    return get_dynamic_forecast_by_date(
        equipo=equipo,
        fecha=fecha,
    )


if __name__ == "__main__":
    print(
        get_forecast_by_date(
            equipo=1,
            fecha="2023-11-03",
        )
    )