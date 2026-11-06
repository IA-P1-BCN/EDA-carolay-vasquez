# Tasks

## 1. Andamiaje del proyecto

- [x] 1.1 Crear la estructura `src/eda_covid/` (`__init__.py`), `tests/`, `notebooks/`, `dashboard/`, `data/{raw,processed,external}/` (con `.gitkeep`) y `reports/`, y verificar que las carpetas existen
- [x] 1.2 Crear `requirements.txt` con `requests`, `pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly`, `streamlit`, `pytest`, `jupyter` e instalar en `.venv`; verificar con `pip install -r requirements.txt` sin errores
- [x] 1.3 Añadir `.gitignore` que excluya `.venv/`, `data/raw/`, `data/processed/` (datos generados) y cachés; verificar que `git status` no lista los datos descargados

## 2. Ingesta reel (data-pipeline)

- [x] 2.1 Escribir tests de `pytest` para `ingest` (usa caché si el CSV existe, descarga si no, y cae a caché ante fallo de API con monkeypatch) y verificar que fallan antes de implementar
- [x] 2.2 Implementar `src/eda_covid/ingest.py` (descarga de la API a `data/raw/covid_states_daily.csv`, reuso de caché, flag `--refresh`, fallback con advertencia) y verificar que los tests de 2.1 pasan
- [x] 2.3 Descargar los datos reales una vez y verificar que el CSV crudo queda en `data/raw/` con ~20.780 filas

## 3. Limpieza determinista (data-pipeline)

- [x] 3.1 Escribir tests de limpieza sobre DataFrames mínimos en memoria: conversión de `date` entero a fecha, eliminación de duplicados estado+fecha, descarte de columnas con nulos > umbral, y negativos de incremento llevados a 0; verificar que fallan antes de implementar
- [x] 3.2 Implementar `src/eda_covid/clean.py` con funciones puras por regla (fecha, duplicados, nulos, columnas vacías, negativos) con umbral y regla parametrizables; verificar que los tests de 3.1 pasan
- [x] 3.3 Añadir test de idempotencia (limpiar dos veces produce el mismo DataFrame) y verificar que pasa
- [x] 3.4 Documentar en docstrings cada decisión de limpieza (motivo del umbral y del tratamiento de negativos) y verificar que `pytest` sigue en verde

## 4. Feature engineering y pipeline de un comando (data-pipeline + exploratory-analysis)

- [x] 4.1 Escribir tests para `features.py` (creación de parte de fecha, ratio por 100.000 hab. tras merge, y media móvil) y verificar que fallan antes de implementar
- [x] 4.2 Añadir `data/external/population.csv` (población por estado) y función de `merge` por código de estado; test que verifica que el merge no pierde filas válidas del dataset principal
- [x] 4.3 Implementar `src/eda_covid/features.py` (≥3 variables nuevas: partes de fecha, ratios normalizados, media móvil) y verificar que los tests de 4.1–4.2 pasan
- [x] 4.4 Implementar `src/eda_covid/pipeline.py` ejecutable con `python -m eda_covid.pipeline` que encadena ingesta → limpieza → features → guardado de `data/processed/covid_clean.csv`; verificar que el comando termina con código 0 y crea el CSV limpio

## 5. Análisis exploratorio en notebook (exploratory-analysis)

- [x] 5.1 Crear `notebooks/eda_covid.ipynb` que cargue `data/processed/covid_clean.csv` y muestre estructura (`shape`, `info()`, `head()`, `describe()`) con texto explicativo
- [x] 5.2 Plantear ≥3 preguntas de negocio al inicio en markdown (a responder en conclusiones)
- [x] 5.3 Análisis univariado de ≥3 variables (histograma/conteo/boxplot) y bivariado de ≥3 relaciones, cada gráfico con título, ejes y leyenda cuando aplique
- [x] 5.4 Detección de outliers (boxplot/IQR) en variables numéricas con decisión escrita
- [x] 5.5 Agregaciones con `groupby`/`agg` y `pivot_table`; matriz de correlación con heatmap e interpretación escrita
- [x] 5.6 Tendencias temporales (líneas), comparación de segmentos (regiones/periodos) y ≥1 gráfico interactivo con `plotly`
- [x] 5.7 Sección de conclusiones que responde por escrito cada pregunta de 5.2 con evidencia; verificar ejecutando el notebook de arriba abajo desde un kernel limpio sin errores (`jupyter nbconvert --execute`)

## 6. Dashboard interactivo (interactive-dashboard)

- [x] 6.1 Implementar `dashboard/app.py` (Streamlit) que lea `data/processed/covid_clean.csv`, con filtros de estado y rango de fechas en la barra lateral
- [x] 6.2 Mostrar métricas clave y ≥1 gráfico de evolución temporal (Plotly) que se actualiza con los filtros; verificar lanzando `streamlit run dashboard/app.py` y comprobando que los filtros cambian las vistas

## 7. Informes y documentación (reporting)

- [x] 7.1 Escribir `reports/informe_calidad_datos.md`: qué faltaba, qué se corrigió (nulos, columnas eliminadas, negativos), qué quedó pendiente y por qué
- [x] 7.2 Escribir `reports/informe_ejecutivo.md` (1–2 págs, público no técnico) con conclusiones claras y gráficos de respaldo, sin código
- [x] 7.3 Escribir `README.md`: origen de los datos, instalación de dependencias, y cómo ejecutar pipeline, notebook y dashboard; verificar siguiendo las instrucciones en un entorno limpio
- [x] 7.4 Confirmar que `requirements.txt` cubre notebook, pipeline y dashboard instalando desde cero en un entorno limpio

## 8. Verificación de integración

- [x] 8.1 Ejecutar la suite completa (`pytest`) y verificar que todos los tests pasan
- [x] 8.2 Ejecutar el flujo extremo a extremo (pipeline → notebook `--execute` → `streamlit run`) en un entorno limpio y verificar que funciona sin pasos manuales no documentados

## Workflow follow-up

- Archivar el cambio con `/opsx:archive` una vez implementado y verificado.
