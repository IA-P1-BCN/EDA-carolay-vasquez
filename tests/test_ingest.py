"""Tests de la ingesta. Escritos antes que la implementación (TDD).

No tocan la red: se sustituye `fetch_from_api` con monkeypatch.
"""
import warnings

import pandas as pd
import pytest

from eda_covid import ingest


def _fake_api_df():
    return pd.DataFrame(
        {
            "date": [20200313, 20200314],
            "state": ["NY", "NY"],
            "positive": [100, 200],
        }
    )


def test_descarga_cuando_no_hay_cache(tmp_path, monkeypatch):
    """Sin CSV local, la ingesta llama a la API y guarda la caché."""
    llamadas = {"n": 0}

    def fake_fetch(url):
        llamadas["n"] += 1
        return _fake_api_df()

    monkeypatch.setattr(ingest, "fetch_from_api", fake_fetch)
    cache = tmp_path / "raw.csv"

    df = ingest.load_raw(cache_path=cache)

    assert llamadas["n"] == 1
    assert cache.exists()
    assert len(df) == 2


def test_usa_cache_en_ejecucion_posterior(tmp_path, monkeypatch):
    """Con CSV local y sin refresh, no se llama a la API."""
    cache = tmp_path / "raw.csv"
    _fake_api_df().to_csv(cache, index=False)

    def boom(url):
        raise AssertionError("no debería llamar a la API habiendo caché")

    monkeypatch.setattr(ingest, "fetch_from_api", boom)

    df = ingest.load_raw(cache_path=cache)
    assert len(df) == 2


def test_refresh_fuerza_nueva_descarga(tmp_path, monkeypatch):
    """Con refresh=True se vuelve a llamar a la API aunque exista caché."""
    cache = tmp_path / "raw.csv"
    _fake_api_df().to_csv(cache, index=False)
    llamadas = {"n": 0}

    def fake_fetch(url):
        llamadas["n"] += 1
        return _fake_api_df()

    monkeypatch.setattr(ingest, "fetch_from_api", fake_fetch)
    ingest.load_raw(cache_path=cache, refresh=True)
    assert llamadas["n"] == 1


def test_fallback_a_cache_si_falla_api(tmp_path, monkeypatch):
    """Si la API falla pero hay caché, se usa la caché con una advertencia."""
    cache = tmp_path / "raw.csv"
    _fake_api_df().to_csv(cache, index=False)

    def fail(url):
        raise ConnectionError("API caída")

    monkeypatch.setattr(ingest, "fetch_from_api", fail)

    with warnings.catch_warnings(record=True) as capturado:
        warnings.simplefilter("always")
        df = ingest.load_raw(cache_path=cache, refresh=True)

    assert len(df) == 2
    assert any("cach" in str(w.message).lower() for w in capturado)


def test_error_si_falla_api_y_no_hay_cache(tmp_path, monkeypatch):
    """Si la API falla y no hay caché, se propaga un error."""
    cache = tmp_path / "raw.csv"

    def fail(url):
        raise ConnectionError("API caída")

    monkeypatch.setattr(ingest, "fetch_from_api", fail)

    with pytest.raises(Exception):
        ingest.load_raw(cache_path=cache)
