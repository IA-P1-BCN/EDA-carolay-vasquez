# Design

## Context

Repositorio nuevo sin código previo (ver `proposal.md` — Why). Los datos vienen de la API del COVID Tracking Project (`https://api.covidtracking.com/v1/states/daily.json`): ~20.780 filas × 56 columnas, un registro por estado/territorio y día (2020-01-13 a 2021-03-07). La columna `date` llega como entero `AAAAMMDD`; muchas columnas tienen >80% de nulos; hay valores negativos de corrección en incrementos diarios; los números son acumulados y absolutos (los estados grandes siempre tienen más). La descarga es grande (~29 MB), por lo que conviene cachearla. Entorno Windows con `.venv` ya presente; Python 3 + Jupyter.

## Goals / Non-Goals

**Goals:**

- Separar claramente **código reutilizable** (`src/`) del **análisis narrativo** (notebook) y de la **comunicación** (informes, dashboard).
- Pipeline determinista e idempotente, ejecutable con un solo comando, con caché de la descarga.
- Tests escritos antes que las funciones de limpieza (TDD) sobre DataFrames pequeños en memoria, sin red.
- Comparaciones justas entre estados vía normalización por población (segunda fuente).

**Non-Goals:**

- No se construye API ni backend; el dashboard lee el CSV limpio en local.
- No se hace modelado predictivo ni inferencia estadística formal; es EDA descriptivo.
- No se despliega infraestructura; la publicación (si se hace) es un enlace a Streamlit Community Cloud o al informe, fuera del alcance del código.

## Decisions

- **Estructura de carpetas**: `src/eda_covid/` (paquete con `ingest.py`, `clean.py`, `features.py`, `pipeline.py`), `tests/`, `notebooks/`, `dashboard/app.py`, `data/raw/` y `data/processed/` (ignoradas en git salvo `.gitkeep`), `reports/`. Alternativa descartada: todo en el notebook — no es reutilizable ni testeable, y el nivel Experto exige código en `.py` y tests.
- **Caché de ingesta**: `ingest.py` descarga a `data/raw/covid_states_daily.csv` y en ejecuciones posteriores lee el CSV salvo `--refresh`. Si la API falla y hay caché, se usa la caché con advertencia. Alternativa descartada: descargar siempre — frágil y lento (~29 MB por corrida).
- **Limpieza como funciones puras**: cada regla (convertir fecha, quitar duplicados, tratar nulos, descartar columnas con nulos > umbral configurable, tratar negativos) es una función que recibe y devuelve un DataFrame, sin efectos secundarios. Facilita TDD y la idempotencia. El umbral de nulos y la regla de negativos son parámetros con valores por defecto documentados.
- **Tratamiento de negativos**: los incrementos negativos son correcciones retroactivas de los estados; se llevan a `0` (no se eliminan filas) para no romper las series temporales, y se registra cuántos se ajustaron. Alternativa considerada: dejarlos — distorsiona medias móviles y sumas acumuladas.
- **Segunda fuente para normalizar**: población por estado de EE.UU. (archivo estático versionado en `data/external/population.csv` para reproducibilidad offline), unido por código de estado. Métricas normalizadas por 100.000 habitantes. Alternativa descartada: llamar a otra API en vivo — añade fragilidad de red.
- **TDD con `pytest`**: los tests construyen DataFrames mínimos en memoria que reproducen cada defecto (fecha entera, duplicado, columna vacía, incremento negativo) y verifican la salida esperada; no tocan la red ni archivos grandes.
- **Dashboard con Streamlit**: lee `data/processed/covid_clean.csv`, con filtros de estado y rango de fechas en la barra lateral y gráficos Plotly. Se elige Streamlit sobre Dash por su menor código para el mismo resultado y despliegue sencillo.
- **Pipeline de un comando**: `python -m eda_covid.pipeline` (o `scripts/run_pipeline.py`) encadena ingesta → limpieza → feature engineering → guardado del CSV limpio, con código de salida 0 en éxito.

## Risks / Trade-offs

- **API retirada o inestable (el proyecto cerró en marzo de 2021)** → la caché local y el CSV crudo versionable permiten trabajar aunque la API no responda.
- **Emparejamiento de nombres/códigos de estado entre fuentes** → usar el código de dos letras del estado como clave y validar con un test que no se pierdan filas en el `merge`.
- **Umbral de nulos arbitrario** → hacerlo parámetro con valor por defecto y justificar el valor elegido en el informe de calidad de datos.
- **Datos acumulados vs. incrementos** → documentar explícitamente qué columnas son acumuladas y usar los `*Increase` para análisis temporal, evitando sumar acumulados.
- **Tamaño del notebook ejecutándose de cabo a rabo** → mantener la carga desde el CSV limpio ya generado por el pipeline, no recalcular la limpieza pesada dentro del notebook.

## Open Questions

- ¿El informe ejecutivo final se entrega como PDF exportado o como markdown en el repo? No afecta specs ni tareas; se decide al redactar (por defecto: markdown en `reports/` y, si se pide, exportar a PDF).
