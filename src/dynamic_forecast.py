from pathlib import Path
from typing import Dict

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "historico_equipos_limpio.csv"
)


ARIMA_ORDERS = {
    1: (1, 1, 1),
    2: (1, 1, 1),
}


def get_dynamic_forecast_by_date(
    equipo: int,
    fecha: str
) -> Dict[str, object]:
    """
    Genera un forecast dinámico con ARIMA desde el último
    dato histórico hasta la fecha solicitada.
    """

    if equipo not in [1, 2]:
        raise ValueError(
            "Equipo debe ser 1 o 2."
        )

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo: {DATA_PATH}"
        )

    value_col = f"Price_Equipo{equipo}"

    df = pd.read_csv(DATA_PATH)

    df["Date"] = pd.to_datetime(
        df["Date"]
    )

    df = df.sort_values("Date")

    last_date = df["Date"].max()

    target_date = pd.to_datetime(
        fecha
    )

    # =====================================================
    # FECHA DENTRO DEL HISTÓRICO
    # =====================================================

    if target_date <= last_date:

        row = df[
            df["Date"] == target_date
        ]

        if row.empty:

            return {
                "found": False,
                "type": "historical",
                "message": (
                    f"La fecha {fecha} está dentro "
                    f"del histórico, pero no existe "
                    f"registro exacto para ese día."
                ),
                "last_historical_date": str(
                    last_date.date()
                ),
            }

        return {
            "found": True,
            "type": "historical",
            "equipo": equipo,
            "fecha": fecha,
            "value": round(
                float(
                    row.iloc[0][value_col]
                ),
                2,
            ),
            "last_historical_date": str(
                last_date.date()
            ),
        }

    # =====================================================
    # FORECAST DINÁMICO
    # =====================================================

    steps = (
        target_date - last_date
    ).days

    series = (
        df
        .set_index("Date")[value_col]
        .asfreq("D")
    )

    series = series.interpolate(
        method="time"
    )

    order = ARIMA_ORDERS[equipo]

    model = ARIMA(
        series,
        order=order
    )

    fitted = model.fit()

    forecast_result = (
        fitted.get_forecast(
            steps=steps
        )
    )

    forecast_mean = (
        forecast_result.predicted_mean
    )

    conf_int = (
        forecast_result.conf_int()
    )

    forecast_value = (
        forecast_mean.iloc[-1]
    )

    lower = conf_int.iloc[-1, 0]

    upper = conf_int.iloc[-1, 1]

    # =====================================================
    # INCERTIDUMBRE
    # =====================================================

    uncertainty_width = (
        upper - lower
    )

    uncertainty_pct = (
        uncertainty_width
        / forecast_value
    ) * 100

    if uncertainty_pct < 20:
        uncertainty_level = "Baja"

    elif uncertainty_pct < 50:
        uncertainty_level = "Media"

    elif uncertainty_pct < 100:
        uncertainty_level = "Alta"

    else:
        uncertainty_level = "Muy Alta"

    # =====================================================
    # HORIZONTE DE PRONÓSTICO
    # =====================================================

    if steps <= 180:
        forecast_horizon = (
            "Corto plazo"
        )

    elif steps <= 365:
        forecast_horizon = (
            "Mediano plazo"
        )

    else:
        forecast_horizon = (
            "Largo plazo"
        )

    return {
        "found": True,
        "type": (
            "dynamic_arima_forecast"
        ),
        "equipo": equipo,
        "fecha": str(
            target_date.date()
        ),
        "last_historical_date": str(
            last_date.date()
        ),
        "days_ahead": steps,
        "forecast": round(
            float(forecast_value),
            2,
        ),
        "lower_bound": round(
            float(lower),
            2,
        ),
        "upper_bound": round(
            float(upper),
            2,
        ),
        "uncertainty_pct": round(
            float(
                uncertainty_pct
            ),
            2,
        ),
        "uncertainty_level": (
            uncertainty_level
        ),
        "forecast_horizon": (
            forecast_horizon
        ),
        "model": (
            f"ARIMA{order}"
        ),
    }


if __name__ == "__main__":

    print(
        get_dynamic_forecast_by_date(
            equipo=2,
            fecha="2026-06-05",
        )
    )