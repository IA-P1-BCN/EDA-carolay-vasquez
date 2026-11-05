"""Limpieza determinista del dataset COVID-19.

Cada regla es una función pura: recibe un DataFrame y devuelve uno nuevo sin
mutar la entrada. Así la limpieza es testeable e idempotente (limpiar dos veces
produce el mismo resultado).

Decisiones de limpieza (documentadas en reports/informe_calidad_datos.md):
- La columna ``date`` llega como entero AAAAMMDD y se convierte a fecha real.
- Se eliminan filas duplicadas por (state, date): no aportan información.
- Se descartan columnas con demasiados nulos (por defecto >80%): sin datos
  suficientes para analizar, y su ausencia se documenta.
- Los incrementos diarios negativos son correcciones retroactivas de los
  estados; se llevan a 0 (no se borran filas) para no romper las series
  temporales ni las sumas acumuladas.
"""
from __future__ import annotations

import pandas as pd

UMBRAL_NULOS_DEFECTO = 0.8
CLAVES = ["state", "date"]


def convertir_fecha(df: pd.DataFrame) -> pd.DataFrame:
    """Convierte la columna ``date`` de entero AAAAMMDD a datetime.

    Si la columna ya es datetime (p. ej. al reaplicar la limpieza), la deja
    intacta, de modo que la operación es idempotente.
    """
    out = df.copy()
    if pd.api.types.is_datetime64_any_dtype(out["date"]):
        return out
    out["date"] = pd.to_datetime(out["date"].astype(str), format="%Y%m%d")
    return out


def eliminar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina filas duplicadas por (state, date), conservando la primera."""
    subset = [c for c in CLAVES if c in df.columns]
    return df.drop_duplicates(subset=subset).reset_index(drop=True)


def descartar_columnas_vacias(
    df: pd.DataFrame, umbral: float = UMBRAL_NULOS_DEFECTO
) -> pd.DataFrame:
    """Descarta columnas cuya proporción de nulos supera ``umbral``."""
    proporcion_nulos = df.isna().mean()
    a_descartar = proporcion_nulos[proporcion_nulos > umbral].index
    return df.drop(columns=list(a_descartar))


def tratar_incrementos_negativos(df: pd.DataFrame) -> pd.DataFrame:
    """Lleva a 0 los valores negativos de las columnas de incremento diario."""
    out = df.copy()
    columnas_incremento = [c for c in out.columns if c.endswith("Increase")]
    for col in columnas_incremento:
        out[col] = out[col].clip(lower=0)
    return out


def clean_dataset(
    df: pd.DataFrame, umbral_nulos: float = UMBRAL_NULOS_DEFECTO
) -> pd.DataFrame:
    """Aplica todas las reglas de limpieza en orden determinista.

    Es idempotente: ``clean_dataset(clean_dataset(df)) == clean_dataset(df)``.
    """
    out = df.copy()
    out = convertir_fecha(out)
    out = eliminar_duplicados(out)
    out = descartar_columnas_vacias(out, umbral=umbral_nulos)
    out = tratar_incrementos_negativos(out)
    out = out.sort_values(CLAVES).reset_index(drop=True)
    return out
