"""Tests de limpieza. Escritos antes que la implementación (TDD).

Usan DataFrames mínimos en memoria que reproducen cada defecto real.
"""
import numpy as np
import pandas as pd

from eda_covid import clean


def test_convierte_fecha_entera_a_datetime():
    df = pd.DataFrame({"date": [20200313, 20200314], "state": ["NY", "NY"]})
    out = clean.convertir_fecha(df)
    assert pd.api.types.is_datetime64_any_dtype(out["date"])
    assert out["date"].iloc[0] == pd.Timestamp("2020-03-13")


def test_elimina_duplicados_estado_fecha():
    df = pd.DataFrame(
        {
            "date": [20200313, 20200313, 20200314],
            "state": ["NY", "NY", "NY"],
            "positive": [100, 100, 200],
        }
    )
    out = clean.eliminar_duplicados(df)
    assert len(out) == 2


def test_descarta_columnas_con_demasiados_nulos():
    df = pd.DataFrame(
        {
            "state": ["NY", "CA", "TX", "FL"],
            "casi_vacia": [1, np.nan, np.nan, np.nan],  # 75% nulos
            "completa": [1, 2, 3, 4],
        }
    )
    out = clean.descartar_columnas_vacias(df, umbral=0.8)
    assert "casi_vacia" in out.columns  # 75% < 80% -> se conserva
    out2 = clean.descartar_columnas_vacias(df, umbral=0.5)
    assert "casi_vacia" not in out2.columns  # 75% > 50% -> se descarta
    assert "completa" in out2.columns


def test_negativos_de_incremento_a_cero():
    df = pd.DataFrame(
        {
            "state": ["NY", "NY"],
            "deathIncrease": [5, -3],
            "positive": [100, 90],  # columna no-Increase: no se toca
        }
    )
    out = clean.tratar_incrementos_negativos(df)
    assert out["deathIncrease"].tolist() == [5, 0]
    assert out["positive"].tolist() == [100, 90]


def test_clean_dataset_integra_todo():
    df = pd.DataFrame(
        {
            "date": [20200313, 20200313, 20200314],
            "state": ["NY", "NY", "NY"],
            "deathIncrease": [5, 5, -2],
            "vacia": [np.nan, np.nan, np.nan],
        }
    )
    out = clean.clean_dataset(df, umbral_nulos=0.8)
    assert pd.api.types.is_datetime64_any_dtype(out["date"])
    assert len(out) == 2
    assert "vacia" not in out.columns
    assert (out["deathIncrease"] >= 0).all()


def test_clean_dataset_es_idempotente():
    df = pd.DataFrame(
        {
            "date": [20200313, 20200313, 20200314],
            "state": ["NY", "NY", "NY"],
            "deathIncrease": [5, 5, -2],
            "vacia": [np.nan, np.nan, np.nan],
        }
    )
    una_vez = clean.clean_dataset(df, umbral_nulos=0.8)
    dos_veces = clean.clean_dataset(df, umbral_nulos=0.8)
    pd.testing.assert_frame_equal(una_vez, dos_veces)
