# Spec Delta

## Purpose

Analizar el dataset limpio en un notebook ordenado y explicado que entienda la estructura de los datos, explore variables y relaciones, cree nuevas variables, compare grupos de forma justa y responda por escrito las preguntas de negocio, con visualizaciones estáticas e interactivas.

## ADDED Requirements

### Requirement: Revisión de estructura del dataset

El notebook SHALL mostrar la estructura del dataset limpio (dimensiones, tipos, primeras filas y resumen estadístico) antes de cualquier análisis.

#### Scenario: Resumen inicial de estructura

- **WHEN** se ejecuta la sección inicial del notebook
- **THEN** se muestran `shape`, tipos/`info()`, `head()` y `describe()` del dataset limpio

### Requirement: Preguntas de negocio planteadas y respondidas

El notebook SHALL plantear al menos tres preguntas de negocio al inicio y responder cada una por escrito con evidencia de datos y visualizaciones.

#### Scenario: Cada pregunta recibe respuesta escrita

- **GIVEN** se plantearon al menos tres preguntas al inicio del notebook
- **WHEN** se llega a las conclusiones
- **THEN** cada pregunta tiene una respuesta escrita apoyada en al menos una visualización o tabla

### Requirement: Análisis univariado y bivariado

El notebook SHALL incluir análisis univariado de al menos tres variables y análisis bivariado de al menos tres relaciones entre pares de variables.

#### Scenario: Univariado de tres variables

- **WHEN** se ejecuta la sección univariada
- **THEN** se presentan al menos tres variables con una visualización adecuada a su tipo (histograma, conteo o boxplot)

#### Scenario: Bivariado de tres relaciones

- **WHEN** se ejecuta la sección bivariada
- **THEN** se presentan al menos tres relaciones entre dos variables con su visualización e interpretación

### Requirement: Visualizaciones legibles

El notebook SHALL incluir un mínimo de cinco visualizaciones, cada una con título, ejes nombrados y leyenda cuando aplique.

#### Scenario: Visualización completa

- **WHEN** se muestra cualquier gráfico del notebook
- **THEN** el gráfico tiene título, ejes con nombre y leyenda cuando hay más de una serie

### Requirement: Detección de valores atípicos

El notebook SHALL detectar valores atípicos en variables numéricas mediante boxplot o rango intercuartílico y decidir de forma justificada qué hacer con ellos.

#### Scenario: Outliers detectados y decididos

- **WHEN** se analiza una variable numérica con posibles atípicos
- **THEN** se identifican los atípicos y se documenta la decisión sobre ellos

### Requirement: Agregaciones y feature engineering

El notebook SHALL resumir los datos con `groupby`/`agg` y tablas dinámicas, y crear al menos tres variables nuevas justificadas (rangos, partes de fecha, ratios o porcentajes).

#### Scenario: Agregaciones por grupo

- **WHEN** se agregan los datos por estado o por periodo
- **THEN** se obtiene una tabla resumen con una métrica agregada por grupo

#### Scenario: Tres variables nuevas

- **WHEN** se ejecuta la sección de feature engineering
- **THEN** existen al menos tres variables nuevas en el dataset de análisis con su justificación escrita

### Requirement: Matriz de correlación interpretada

El notebook SHALL calcular una matriz de correlación entre variables numéricas, mostrarla como heatmap e interpretar sus hallazgos principales.

#### Scenario: Heatmap de correlación

- **WHEN** se calcula la correlación entre las variables numéricas
- **THEN** se muestra un heatmap y un texto que interpreta las correlaciones más relevantes

### Requirement: Tendencias temporales

El notebook SHALL analizar la evolución en el tiempo de las métricas clave con gráficos de líneas.

#### Scenario: Serie temporal de una métrica

- **WHEN** se analiza una métrica a lo largo del tiempo
- **THEN** se muestra un gráfico de líneas con la fecha en el eje temporal

### Requirement: Normalización para comparar con justicia

El notebook SHALL normalizar las métricas absolutas (p. ej. ratios por cada 100.000 habitantes o porcentajes) para comparar estados de distinto tamaño de forma justa.

#### Scenario: Comparación normalizada entre estados

- **WHEN** se comparan estados de distinta población
- **THEN** la comparación usa una métrica normalizada en lugar de totales absolutos

### Requirement: Enriquecimiento con una segunda fuente

El notebook SHALL enriquecer el dataset principal con una segunda fuente de datos mediante `merge` que aporte contexto (p. ej. población por estado).

#### Scenario: Unión con la segunda fuente

- **WHEN** se combina el dataset principal con la segunda fuente por la clave de estado
- **THEN** el dataset resultante incorpora las columnas de contexto sin perder las filas válidas del dataset principal

### Requirement: Transformaciones justificadas

El notebook SHALL aplicar al menos una transformación justificada (media móvil para suavizar series o escala logarítmica para distribuciones sesgadas) y explicar por qué.

#### Scenario: Transformación aplicada y explicada

- **WHEN** una serie es ruidosa o una distribución está muy sesgada
- **THEN** se aplica la transformación adecuada y se explica por escrito el motivo

### Requirement: Comparación de segmentos

El notebook SHALL comparar segmentos o grupos (regiones, categorías o periodos) con visualizaciones claras.

#### Scenario: Comparación entre segmentos

- **WHEN** se comparan varios segmentos
- **THEN** se muestra una visualización que contrasta la métrica entre los segmentos

### Requirement: Gráficos interactivos

El notebook SHALL incluir al menos un gráfico interactivo con `plotly`.

#### Scenario: Gráfico interactivo con plotly

- **WHEN** se renderiza el gráfico interactivo
- **THEN** la persona puede inspeccionar valores al pasar el cursor sobre el gráfico

### Requirement: Notebook ejecutable de arriba abajo

El notebook SHALL ejecutarse completo de la primera a la última celda sin errores y alternar texto explicativo en markdown con el código.

#### Scenario: Ejecución completa sin errores

- **WHEN** se ejecutan todas las celdas en orden desde un kernel limpio
- **THEN** el notebook termina sin errores y cada sección tiene texto explicativo
