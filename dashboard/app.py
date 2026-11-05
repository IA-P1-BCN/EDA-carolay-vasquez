"""Dashboard interactivo del EDA COVID-19 (Streamlit).

Arranque:
    streamlit run dashboard/app.py

Lee el dataset limpio generado por el pipeline
(`python -m eda_covid.pipeline`) y permite filtrar por estado y por rango de
fechas, mostrando métricas clave y la evolución temporal.
"""
from __future__ import annotations

import sys
from pathlib import Path

import plotly.express as px
import streamlit as st

# Permite importar el paquete tanto si se lanza desde la raíz como desde otro sitio.
RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from eda_covid import dashboard_data as dd  # noqa: E402

CLEAN_PATH = RAIZ / "data" / "processed" / "covid_clean.csv"

st.set_page_config(page_title="EDA COVID-19 EE.UU.", layout="wide")
st.title("📊 COVID-19 en EE.UU. — panel interactivo")
st.caption("Fuente: COVID Tracking Project · datos limpios por el pipeline del proyecto")

if not CLEAN_PATH.exists():
    st.error(
        "No se encuentra el dataset limpio. Ejecuta primero el pipeline:\n\n"
        "`python -m eda_covid.pipeline`"
    )
    st.stop()


@st.cache_data
def _cargar():
    return dd.cargar_datos(CLEAN_PATH)


df = _cargar()

# --- Barra lateral: filtros ---
st.sidebar.header("Filtros")
estados = sorted(df["state"].unique())
sel_estados = st.sidebar.multiselect(
    "Estados", estados, default=["NY", "CA", "TX", "FL"]
)
fecha_min, fecha_max = df["date"].min().date(), df["date"].max().date()
rango = st.sidebar.slider(
    "Rango de fechas",
    min_value=fecha_min,
    max_value=fecha_max,
    value=(fecha_min, fecha_max),
)

filtrado = dd.aplicar_filtros(
    df, estados=sel_estados or None, fecha_inicio=rango[0], fecha_fin=rango[1]
)

# --- Métricas clave ---
kpis = dd.calcular_kpis(filtrado)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Casos acumulados", f"{kpis['casos']:,.0f}")
c2.metric("Fallecimientos", f"{kpis['muertes']:,.0f}")
c3.metric("Casos nuevos (periodo)", f"{kpis['casos_nuevos']:,.0f}")
c4.metric("Estados seleccionados", kpis["estados"])

# --- Evolución temporal ---
st.subheader("Evolución de nuevos casos diarios")
serie = dd.serie_temporal(filtrado, "positiveIncrease")
if serie.empty:
    st.info("Selecciona al menos un estado y un rango con datos.")
else:
    fig = px.line(
        serie,
        x="date",
        y=["positiveIncrease", "mm7"],
        labels={"value": "Casos nuevos", "date": "Fecha", "variable": "Serie"},
    )
    fig.update_layout(legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)

# --- Comparación por estado ---
st.subheader("Casos por 100.000 habitantes (comparación justa)")
if "casos_por_100k" in filtrado.columns and not filtrado.empty:
    ultimos = filtrado.sort_values("date").groupby("state").tail(1)
    fig2 = px.bar(
        ultimos.sort_values("casos_por_100k", ascending=False),
        x="state",
        y="casos_por_100k",
        labels={"state": "Estado", "casos_por_100k": "Casos por 100.000 hab."},
    )
    st.plotly_chart(fig2, use_container_width=True)

st.caption("Consulta el informe ejecutivo en `reports/informe_ejecutivo.md`.")
