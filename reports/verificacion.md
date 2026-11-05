# Verificación de integración

Resultado de ejecutar el proyecto de extremo a extremo en un entorno con las dependencias de `requirements.txt` instaladas.

| Paso | Comando | Resultado |
|---|---|---|
| Suite de tests | `pytest` | ✅ 21 tests pasan |
| Pipeline reproducible | `python -m eda_covid.pipeline` | ✅ genera `data/processed/covid_clean.csv` (20.780 × 47) |
| Notebook completo | `jupyter nbconvert --to notebook --execute notebooks/eda_covid.ipynb` | ✅ ejecuta de arriba abajo, 0 celdas con error |
| Dashboard | `streamlit run dashboard/app.py` | ✅ arranca (health `/_stcore/health` → `ok`) |

La suite de tests se ejecuta además automáticamente en cada push y pull request mediante GitHub Actions (`.github/workflows/ci.yml`).

## Cobertura de tests

- `test_ingest.py` — caché, refresh y fallback de la ingesta (sin red).
- `test_clean.py` — reglas de limpieza e idempotencia.
- `test_features.py` — partes de fecha, merge sin pérdida de filas, ratio por 100k, media móvil.
- `test_dashboard.py` — filtros por estado y fecha, KPIs y serie temporal.
