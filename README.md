# 📊 EDA COVID-19 EE.UU.

Análisis exploratorio de datos (EDA) del COVID-19 en Estados Unidos, desde la carga y limpieza de los datos hasta un informe ejecutivo y un dashboard interactivo. El proyecto se desarrolló con un flujo **reproducible** y especificado con [OpenSpec](https://github.com/Fission-AI/OpenSpec).

## 🗂️ Origen de los datos

- **Fuente principal:** [COVID Tracking Project](https://covidtracking.com/data) — registro diario por estado/territorio de EE.UU. (13-ene-2020 a 7-mar-2021), vía la API `https://api.covidtracking.com/v1/states/daily.json`. Son 20.780 filas × 56 columnas. El pipeline la descarga y la cachea en `data/raw/`.
- **Segunda fuente (contexto):** población por estado (Census 2020), versionada en `data/external/population.csv`, usada para normalizar por cada 100.000 habitantes.

## 📦 Estructura del repositorio

```
src/eda_covid/      código reutilizable: ingest, clean, features, pipeline, dashboard_data
tests/              tests de pytest (escritos antes que las funciones)
notebooks/          eda_covid.ipynb — análisis exploratorio completo
dashboard/          app.py — dashboard Streamlit
data/raw/           datos crudos cacheados (ignorados en git)
data/processed/     dataset limpio generado por el pipeline (ignorado en git)
data/external/      segunda fuente: población por estado
reports/            informe ejecutivo e informe de calidad de datos
openspec/           especificación del proyecto (change: eda-covid19-experto)
```

## ⚙️ Instalación

Requiere **Python 3.10+**.

```bash
# 1. Crear y activar un entorno virtual
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# 2. Instalar dependencias y el paquete del proyecto
pip install -r requirements.txt
pip install -e .
```

El `pip install -e .` deja disponible el comando `python -m eda_covid.pipeline` desde cualquier carpeta.

## ▶️ Cómo ejecutar

### 1) Pipeline (descarga + limpieza + variables nuevas)

Genera `data/processed/covid_clean.csv` con un solo comando:

```bash
python -m eda_covid.pipeline
```

Opciones: `--refresh` (vuelve a descargar), `--out <ruta>`, `--umbral-nulos <0-1>`.

### 2) Notebook de análisis

```bash
jupyter notebook notebooks/eda_covid.ipynb
```

El notebook lee el dataset limpio y se ejecuta de arriba abajo sin errores. (Antes de abrirlo, ejecuta el pipeline para generar el CSV limpio.)

### 3) Dashboard interactivo

```bash
streamlit run dashboard/app.py
```

Permite filtrar por estado y por rango de fechas, con métricas clave y evolución temporal.

### 4) Tests

```bash
pytest
```

## 📑 Informes

- **Informe ejecutivo** (público no técnico): [`reports/informe_ejecutivo.md`](reports/informe_ejecutivo.md)
- **Informe de calidad de datos**: [`reports/informe_calidad_datos.md`](reports/informe_calidad_datos.md)

## 🏆 Alcance

Cubre hasta el **nivel Experto** del briefing: limpieza justificada y testeada, análisis univariado/bivariado, outliers, feature engineering, correlación, tendencias temporales, normalización, enriquecimiento con segunda fuente, gráficos interactivos, pipeline reproducible, tests con `pytest`, dashboard e informe de calidad de datos.
