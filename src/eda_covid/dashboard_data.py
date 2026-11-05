"""Lógica de datos del dashboard, separada de la UI para poder testearla.

El módulo no depende de Streamlit: solo pandas. El dashboard (`dashboard/app.py`)
importa estas funciones y añade la capa visual.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

DEFAULT_CLEAN_PATH = Path("data/processed/covid_clean.csv")


def cargar_datos(path: str | Path = DEFAULT_CLEAN_PATH) -> pd.DataFrame:
    """Carga el dataset limpio generado por el pipeline."""
    df = pd.read_csv(path, parse_dates=["date"])
    return df


def aplicar_filtros(
    df: pd.DataFrame,
    estados: list[str] | None = None,
    fecha_inicio=None,
    fecha_fin=None,
) -> pd.DataFrame:
    """Filtra por estados y por rango de fechas (ambos opcionales)."""
    out = df
    if estados:
        out = out[out["state"].isin(estados)]
    if fecha_inicio is not None:
        out = out[out["date"] >= pd.Timestamp(fecha_inicio)]
    if fecha_fin is not None:
        out = out[out["date"] <= pd.Timestamp(fecha_fin)]
    return out


def calcular_kpis(df: pd.DataFrame) -> dict:
    """Calcula las métricas clave sobre el subconjunto filtrado."""
    def _max_por_estado(col: str) -> float:
        if col not in df.columns or df.empty:
            return 0.0
        return float(df.groupby("state")[col].max().sum())

    return {
        "casos": _max_por_estado("positive"),
        "muertes": _max_por_estado("death"),
        "casos_nuevos": float(df["positiveIncrease"].sum()) if "positiveIncrease" in df else 0.0,
        "estados": int(df["state"].nunique()) if "state" in df else 0,
    }


def serie_temporal(df: pd.DataFrame, columna: str = "positiveIncrease") -> pd.DataFrame:
    """Agrega la columna por fecha y añade media móvil de 7 días."""
    if df.empty:
        return pd.DataFrame(columns=["date", columna, "mm7"])
    serie = df.groupby("date")[columna].sum().reset_index()
    serie["mm7"] = serie[columna].rolling(7, min_periods=1).mean()
    return serie
