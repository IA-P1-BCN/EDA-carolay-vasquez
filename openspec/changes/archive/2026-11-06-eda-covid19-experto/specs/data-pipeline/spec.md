# Spec Delta

## Purpose

Obtener, cachear y limpiar de forma reproducible los datos crudos de COVID-19 de EE.UU., dejando un dataset limpio y documentado que el resto del análisis consume, todo ejecutable con un solo comando y respaldado por tests automatizados.

## ADDED Requirements

### Requirement: Ingesta reproducible con caché local

El sistema SHALL obtener los datos diarios por estado desde la API del COVID Tracking Project y guardar una copia cruda en CSV local, reutilizando la copia en ejecuciones posteriores en lugar de volver a descargar.

#### Scenario: Primera ejecución sin caché

- **WHEN** se ejecuta la ingesta y no existe el CSV crudo local
- **THEN** el sistema descarga los datos de la API y guarda el CSV crudo en disco

#### Scenario: Ejecución posterior con caché existente

- **GIVEN** ya existe el CSV crudo local de una ejecución previa
- **WHEN** se ejecuta la ingesta sin forzar refresco
- **THEN** el sistema carga los datos desde el CSV local sin llamar a la API

#### Scenario: La API no está disponible y hay caché

- **GIVEN** existe el CSV crudo local
- **WHEN** la API no responde o devuelve un error
- **THEN** el sistema usa la copia cacheada y registra una advertencia en lugar de fallar

### Requirement: Limpieza determinista del dataset

El sistema SHALL transformar los datos crudos en un dataset limpio aplicando siempre las mismas reglas: conversión de la columna de fecha entera a tipo fecha, eliminación de duplicados, tratamiento documentado de nulos y de columnas casi vacías, y tratamiento de los valores negativos de corrección en los incrementos diarios.

#### Scenario: La fecha entera se convierte a tipo fecha

- **WHEN** se limpia un dataset cuya columna `date` viene como entero `AAAAMMDD`
- **THEN** la columna de fecha queda como tipo fecha y las filas conservan su orden temporal por estado

#### Scenario: Se eliminan duplicados exactos

- **WHEN** el dataset crudo contiene filas duplicadas para el mismo estado y fecha
- **THEN** el dataset limpio conserva una sola fila por combinación de estado y fecha

#### Scenario: Columnas con exceso de nulos se descartan de forma documentada

- **WHEN** una columna supera un umbral de valores nulos definido
- **THEN** la columna se elimina del dataset limpio y la decisión queda registrada en el informe de calidad de datos

#### Scenario: Valores negativos de incremento se tratan de forma justificada

- **WHEN** una columna de incremento diario (p. ej. `deathIncrease`) contiene valores negativos de corrección
- **THEN** el sistema aplica la regla de tratamiento definida (p. ej. llevar a cero o marcar) de forma consistente y documentada

### Requirement: Limpieza determinista e idempotente

El sistema SHALL producir exactamente el mismo dataset limpio cuando se ejecuta la limpieza varias veces sobre la misma entrada, sin depender del orden de ejecución ni de estado previo.

#### Scenario: Dos ejecuciones producen el mismo resultado

- **WHEN** se ejecuta la limpieza dos veces sobre el mismo CSV crudo
- **THEN** ambos datasets limpios resultantes son idénticos

### Requirement: Pipeline ejecutable con un solo comando

El sistema SHALL ofrecer un comando único que ejecute ingesta y limpieza de principio a fin y guarde el dataset limpio en una ruta conocida.

#### Scenario: Ejecución del pipeline completo

- **WHEN** la persona ejecuta el comando único del pipeline
- **THEN** el sistema produce y guarda el dataset limpio y termina con un código de salida de éxito

### Requirement: Funciones de limpieza cubiertas por tests

Las funciones de limpieza SHALL ser funciones reutilizables importables, cubiertas por tests de `pytest` que validen cada regla de limpieza y que se escriben antes que la implementación de la función.

#### Scenario: La suite de tests valida las reglas de limpieza

- **WHEN** se ejecuta `pytest` sobre la suite del proyecto
- **THEN** existen tests que cubren conversión de fecha, duplicados, nulos y valores negativos, y todos pasan
