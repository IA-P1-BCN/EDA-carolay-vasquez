# Proposal

## Why

El CEO de un cliente entrega un conjunto de datos de COVID-19 de EE.UU. que nadie ha mirado con calma y pide datos limpios, con sentido, y la historia que hay detrás de ellos, antes de decidir qué hacer con esa información. El CEO no lee código: lee el informe. Hoy no existe ningún artefacto en el repositorio (ingesta, limpieza, análisis ni informe), así que hay que construir el producto de datos completo de forma reproducible y comunicable a público no técnico.

## What Changes

- Construir la **ingesta reproducible** de los datos públicos del COVID Tracking Project (API `https://api.covidtracking.com/v1/states/daily.json`), con caché local en CSV para no depender de la red en cada ejecución.
- Construir la **limpieza reproducible** en código `.py` reutilizable (nulos, duplicados, tipos de fecha, columnas casi vacías, valores negativos de corrección), con decisiones justificadas y cubierta por **tests de `pytest` escritos antes que las funciones**.
- Encadenar ingesta + limpieza en un **pipeline reproducible ejecutable con un solo comando** que guarde el dataset limpio.
- Realizar el **análisis exploratorio (EDA)** en un notebook Jupyter ordenado y explicado: estructura, univariado, bivariado, outliers, `groupby`/`pivot_table`, feature engineering, matriz de correlación, tendencias temporales, normalización por ratios, enriquecimiento con una **segunda fuente** vía `merge`, transformaciones justificadas (media móvil, escala log) y gráficos interactivos con `plotly`.
- Producir los **informes**: informe ejecutivo para público no técnico, informe de calidad de datos, `README.md` con origen de datos e instrucciones y `requirements.txt` reproducible.
- Construir un **dashboard interactivo** (Streamlit) donde el CEO pueda filtrar y explorar los datos por su cuenta.

## Capabilities

### New Capabilities

- `data-pipeline`: obtención, caché y limpieza reproducible de los datos crudos en código `.py` reutilizable, orquestada por un pipeline de un solo comando y respaldada por tests automatizados.
- `exploratory-analysis`: el análisis exploratorio del dataset limpio en un notebook (estructura, univariado, bivariado, outliers, agregaciones, feature engineering, correlación, series temporales, normalización, enriquecimiento con segunda fuente y transformaciones) con visualizaciones estáticas e interactivas.
- `reporting`: comunicación de resultados a público no técnico: informe ejecutivo, informe de calidad de datos y documentación reproducible del repositorio (`README`, `requirements.txt`).
- `interactive-dashboard`: aplicación interactiva que permite al cliente filtrar, segmentar y explorar los datos limpios sin tocar código.

### Modified Capabilities

<!-- Ninguna: el repositorio no tiene specs previas. -->

## Impact

- **Nuevo código**: módulo de ingesta y limpieza en `src/` (`.py` reutilizable), pipeline CLI de un comando, dashboard Streamlit, y suite de tests en `tests/`.
- **Nuevos artefactos**: notebook Jupyter de EDA, informe ejecutivo (PDF/markdown), informe de calidad de datos, `README.md`, `requirements.txt`.
- **Datos**: descarga de ~29 MB cacheada como CSV; segunda fuente de datos de contexto (p. ej. población por estado) para normalización.
- **Dependencias**: `requests`, `pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly`, `streamlit`, `pytest`, `jupyter`.
- **Sin rupturas**: no existe código previo que cambie de comportamiento.
