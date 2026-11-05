"""Tests de la lógica de datos del dashboard."""
import pandas as pd

from eda_covid import dashboard_data as dd


def _df():
    return pd.DataFrame(
        {
            "date": pd.to_datetime(
                ["2020-03-13", "2020-03-14", "2020-03-13", "2020-03-14"]
            ),
            "state": ["NY", "NY", "CA", "CA"],
            "positive": [100, 300, 50, 80],
            "death": [1, 5, 0, 2],
            "positiveIncrease": [100, 200, 50, 30],
        }
    )


def test_filtra_por_estado():
    out = dd.aplicar_filtros(_df(), estados=["NY"])
    assert set(out["state"]) == {"NY"}
    assert len(out) == 2


def test_filtra_por_rango_de_fechas():
    out = dd.aplicar_filtros(_df(), fecha_inicio="2020-03-14")
    assert (out["date"] >= pd.Timestamp("2020-03-14")).all()
    assert len(out) == 2


def test_kpis_suman_maximo_por_estado():
    kpis = dd.calcular_kpis(_df())
    # casos = max NY (300) + max CA (80) = 380
    assert kpis["casos"] == 380
    assert kpis["estados"] == 2


def test_serie_temporal_tiene_media_movil():
    serie = dd.serie_temporal(_df())
    assert "mm7" in serie.columns
    assert len(serie) == 2  # dos fechas distintas


def test_filtros_cambian_la_vista():
    """Filtrar por un estado reduce el resultado respecto al total."""
    df = _df()
    total = dd.calcular_kpis(df)["casos"]
    filtrado = dd.calcular_kpis(dd.aplicar_filtros(df, estados=["CA"]))["casos"]
    assert filtrado < total
