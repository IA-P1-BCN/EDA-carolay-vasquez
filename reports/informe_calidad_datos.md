# Informe de calidad de datos

**Dataset:** COVID-19 EE.UU. — COVID Tracking Project (API `states/daily`).
**Registros crudos:** 20.780 filas × 56 columnas (13-ene-2020 a 7-mar-2021, por estado/territorio).
**Registros tras limpieza + variables nuevas:** 20.780 filas × 47 columnas.

Este informe documenta qué faltaba, qué se corrigió, qué quedó pendiente y por qué. Las reglas están implementadas como funciones puras en `src/eda_covid/clean.py` y cubiertas por tests (`tests/test_clean.py`).

## 1. Qué faltaba (valores ausentes)

- **15 columnas con más del 80 % de valores nulos** se descartaron, por no tener datos suficientes para un análisis fiable:
  `dataQualityGrade`, `grade`, `hospitalizedDischarged`, `inIcuCumulative`, `negativeTestsAntibody`, `negativeTestsPeopleAntibody`, `onVentilatorCumulative`, `pending`, `positiveTestsAntibody`, `positiveTestsAntigen`, `positiveTestsPeopleAntibody`, `positiveTestsPeopleAntigen`, `totalTestsAntigen`, `totalTestsPeopleAntibody`, `totalTestsPeopleAntigen`.
- El umbral del 80 % es un **parámetro** (`umbral_nulos`), no un valor fijo en el código, para poder ajustarlo y justificarlo.
- Los nulos restantes en columnas que sí conservamos corresponden a fechas en que un estado todavía no reportaba esa métrica; se mantienen como `NaN` y se tratan por análisis (p. ej. `dropna` puntual en los gráficos que lo requieren), sin imputar valores inventados.

## 2. Qué se corrigió

| Problema | Decisión | Motivo |
|---|---|---|
| `date` venía como entero `AAAAMMDD` | Conversión a tipo fecha | Permite ordenar y analizar series temporales |
| Posibles filas duplicadas (state, date) | Eliminación de duplicados (se encontraron **0**) | Una observación por estado y día |
| **304 valores negativos** en columnas de incremento diario (`positiveIncrease` 24, `negativeIncrease` 70, `totalTestResultsIncrease` 49, `deathIncrease` 73, `hospitalizedIncrease` 88) | Se llevan a **0** (no se eliminan filas) | Son correcciones retroactivas de los estados; borrarlas rompería las series y las sumas acumuladas |

La limpieza es **determinista e idempotente**: ejecutarla dos veces produce exactamente el mismo resultado (verificado con un test).

## 3. Qué quedó pendiente / limitaciones

- Los **números son acumulados y absolutos**: un estado grande siempre mostrará más casos. Para comparar con justicia se añadió una segunda fuente (población por estado, `data/external/population.csv`) y métricas **por cada 100.000 habitantes**.
- Los valores atípicos en los incrementos diarios **no se eliminan**: son reales (picos de olas). Se suavizan con media móvil de 7 días en el análisis, pero se conservan en el dato.
- El proyecto dejó de actualizarse el **7 de marzo de 2021**, por lo que el análisis no cubre fechas posteriores.
- Algunas métricas de anticuerpos/antígenos se perdieron al descartar columnas muy vacías; si en el futuro se necesitaran, habría que buscar otra fuente.
