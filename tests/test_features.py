"""Tests de feature engineering y del merge con la segunda fuente (TDD)."""
import numpy as np
import pandas as pd

from eda_covid import features


def _df_base():
    return pd.DataFrame(
        {
            "date": pd.to_datetime(["2020-03-13", "2020-03-14", "2020-03-15"]),
            "state": ["NY", "NY", "NY"],
            "positive": [100, 300, 600],
            "positiveIncrease": [100, 200, 300],
        }
    )


def test_agrega_partes_de_fecha():
    out = features.agregar_partes_fecha(_df_base())
    assert out["anio"].tolist() == [2020, 2020, 2020]
    assert out["mes"].tolist() == [3, 3, 3]


def test_merge_poblacion_no_pierde_filas():
    df = _df_base()
    poblacion = pd.DataFrame({"state": ["NY"], "population": [19_000_000]})
    out = features.merge_poblacion(df, poblacion)
    assert len(out) == len(df)
    assert out["population"].notna().all()


def test_merge_conserva_filas_sin_poblacion():
    """Un estado sin población en la 2ª fuente no desaparece (left join)."""
    df = _df_base().assign(state=["NY", "NY", "ZZ"])
    poblacion = pd.DataFrame({"state": ["NY"], "population": [19_000_000]})
    out = features.merge_poblacion(df, poblacion)
    assert len(out) == len(df)
    assert out.loc[out["state"] == "ZZ", "population"].isna().all()


def test_ratio_por_100k():
    df = _df_base()
    df["population"] = 1_000_000
    out = features.agregar_ratio_por_100k(df, "positive", "casos_por_100k")
    # 100 casos / 1.000.000 hab * 100.000 = 10
    assert out["casos_por_100k"].iloc[0] == 10.0


def test_media_movil():
    df = _df_base()
    out = features.agregar_media_movil(df, "positiveIncrease", ventana=2)
    # media móvil de ventana 2: [100, (100+200)/2, (200+300)/2]
    esperado = [100.0, 150.0, 250.0]
    assert np.allclose(out["positiveIncrease_mm2"].tolist(), esperado)
