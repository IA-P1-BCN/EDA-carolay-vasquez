"""Ingesta reproducible de los datos COVID-19 de EE.UU.

Fuente: COVID Tracking Project, endpoint diario por estado.
La descarga (~29 MB) se cachea en CSV para no depender de la red en cada
ejecución. Si la API falla pero existe una copia local, se usa la copia.
"""
from __future__ import annotations

import warnings
from pathlib import Path

import pandas as pd
import requests

API_URL = "https://api.covidtracking.com/v1/states/daily.json"
DEFAULT_RAW_PATH = Path("data/raw/covid_states_daily.csv")


def fetch_from_api(url: str = API_URL) -> pd.DataFrame:
    """Descarga los datos crudos desde la API y los devuelve como DataFrame."""
    respuesta = requests.get(url, timeout=60)
    respuesta.raise_for_status()
    return pd.DataFrame(respuesta.json())


def load_raw(
    cache_path: str | Path = DEFAULT_RAW_PATH,
    url: str = API_URL,
    refresh: bool = False,
) -> pd.DataFrame:
    """Devuelve los datos crudos, usando caché local cuando es posible.

    - Si existe la caché y ``refresh`` es ``False``: lee el CSV local.
    - Si no, descarga de la API y guarda la caché.
    - Si la descarga falla pero existe la caché: usa la caché con advertencia.
    - Si la descarga falla y no hay caché: propaga el error.
    """
    cache_path = Path(cache_path)

    if cache_path.exists() and not refresh:
        return pd.read_csv(cache_path)

    try:
        df = fetch_from_api(url)
    except Exception as error:  # red caída, timeout, HTTP error, etc.
        if cache_path.exists():
            warnings.warn(
                f"Fallo al llamar a la API ({error}); se usa la caché local "
                f"en {cache_path}.",
                stacklevel=2,
            )
            return pd.read_csv(cache_path)
        raise

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(cache_path, index=False)
    return df
