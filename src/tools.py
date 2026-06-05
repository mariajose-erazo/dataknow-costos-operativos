from pathlib import Path
from typing import Dict

import pandas as pd


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


def load_latest_values() -> Dict[str, float]:
    """
    Carga el último registro disponible del dataset procesado.
    """
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

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
) -> Dict[str, float]:
    """
    Simula el impacto aproximado de un cambio porcentual en una materia prima
    sobre el precio estimado de un equipo usando coeficientes de regresión lineal.
    """
    latest = load_latest_values()

    if material not in ["Price_X", "Price_Y", "Price_Z"]:
        raise ValueError("Materia prima no válida.")

    if target not in ["Price_Equipo1", "Price_Equipo2"]:
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
        "estimated_target_percent_change": round(estimated_target_percent_change, 2),
    }


def get_forecast_by_date(equipo: int, fecha: str) -> Dict[str, object]:
    """
    Consulta el forecast para una fecha específica.

    Args:
        equipo: 1 o 2.
        fecha: fecha en formato YYYY-MM-DD.

    Returns:
        Diccionario con forecast, límite inferior y límite superior.
    """
    if equipo == 1:
        file_path = PROCESSED_PATH / "forecast_equipo1.csv"
    elif equipo == 2:
        file_path = PROCESSED_PATH / "forecast_equipo2.csv"
    else:
        raise ValueError("Equipo debe ser 1 o 2.")

    if not file_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")

    df = pd.read_csv(file_path)

    fecha_col = df.columns[0]

    df[fecha_col] = pd.to_datetime(df[fecha_col])
    target_date = pd.to_datetime(fecha)

    row = df[df[fecha_col] == target_date]

    if row.empty:
        min_date = df[fecha_col].min().date()
        max_date = df[fecha_col].max().date()

        return {
            "found": False,
            "equipo": equipo,
            "fecha": fecha,
            "message": (
                f"No existe forecast para {fecha}. "
                f"El rango disponible es {min_date} a {max_date}."
            ),
            "available_start": str(min_date),
            "available_end": str(max_date),
        }

    row = row.iloc[0]

    return {
        "found": True,
        "equipo": equipo,
        "fecha": fecha,
        "forecast": round(float(row.iloc[1]), 2),
        "lower_bound": round(float(row.iloc[2]), 2),
        "upper_bound": round(float(row.iloc[3]), 2),
    }


if __name__ == "__main__":
    print(
        get_forecast_by_date(
            equipo=2,
            fecha="2023-09-05",
        )
    )