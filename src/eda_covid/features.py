"""Feature engineering y enriquecimiento con una segunda fuente.

Variables nuevas:
- Partes de fecha (año, mes) para análisis temporal por periodo.
- Ratios normalizados por 100.000 habitantes (merge con población por estado),
  para comparar estados de distinto tamaño de forma justa.
- Medias móviles para suavizar las series ruidosas de incrementos diarios.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

DEFAULT_POP_PATH = Path("data/external/population.csv")
CLAVES = ["state", "date"]


def agregar_partes_fecha(df: pd.DataFrame) -> pd.DataFrame:
    """Añade columnas de año y mes a partir de la columna ``date``."""
    out = df.copy()
    out["anio"] = out["date"].dt.year
    out["mes"] = out["date"].dt.month
    return out


def cargar_poblacion(path: str | Path = DEFAULT_POP_PATH) -> pd.DataFrame:
    """Carga la segunda fuente: población por estado/territorio."""
    return pd.read_csv(path)


def merge_poblacion(df: pd.DataFrame, poblacion: pd.DataFrame) -> pd.DataFrame:
    """Une el dataset principal con la población por estado (left join).

    Un estado sin población en la segunda fuente conserva sus filas con
    ``population`` nulo; no se pierde ninguna fila válida del dataset principal.
    """
    return df.merge(poblacion, on="state", how="left")


def agregar_ratio_por_100k(
    df: pd.DataFrame, columna: str, nombre: str
) -> pd.DataFrame:
    """Crea una métrica por cada 100.000 habitantes a partir de ``columna``."""
    out = df.copy()
    out[nombre] = out[columna] / out["population"] * 100_000
    return out


def agregar_media_movil(
    df: pd.DataFrame, columna: str, ventana: int = 7, por: str = "state"
) -> pd.DataFrame:
    """Añade la media móvil de ``columna`` dentro de cada grupo ``por``.

    La media se calcula respetando el orden temporal y por estado, para no
    mezclar series de estados distintos.
    """
    out = df.copy()
    nombre = f"{columna}_mm{ventana}"
    if por in out.columns:
        out = out.sort_values(CLAVES)
        out[nombre] = (
            out.groupby(por)[columna]
            .transform(lambda s: s.rolling(ventana, min_periods=1).mean())
        )
    else:
        out[nombre] = out[columna].rolling(ventana, min_periods=1).mean()
    return out


def construir_features(
    df: pd.DataFrame, poblacion: pd.DataFrame | None = None
) -> pd.DataFrame:
    """Aplica todo el feature engineering al dataset limpio.

    Genera al menos tres variables nuevas: partes de fecha, ratio de casos por
    100.000 habitantes y media móvil de 7 días de los casos nuevos.
    """
    out = agregar_partes_fecha(df)
    if poblacion is None:
        poblacion = cargar_poblacion()
    out = merge_poblacion(out, poblacion)
    if "positive" in out.columns:
        out = agregar_ratio_por_100k(out, "positive", "casos_por_100k")
    if "death" in out.columns:
        out = agregar_ratio_por_100k(out, "death", "muertes_por_100k")
    if "positiveIncrease" in out.columns:
        out = agregar_media_movil(out, "positiveIncrease", ventana=7)
    return out.reset_index(drop=True)
