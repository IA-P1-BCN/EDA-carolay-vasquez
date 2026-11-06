# reporting Specification

## Purpose
Comunicar los resultados del análisis a público no técnico y dejar el repositorio reproducible: un informe ejecutivo claro, un informe de calidad de datos y la documentación mínima (`README`, `requirements.txt`) para que cualquier persona reproduzca el trabajo.

## Requirements

### Requirement: Informe ejecutivo para público no técnico

El sistema SHALL incluir un informe ejecutivo de una a dos páginas, dirigido a alguien que no sabe de datos, con las conclusiones principales y los gráficos que las respaldan, sin jerga ni código.

#### Scenario: Informe legible por el CEO

- **WHEN** el cliente abre el informe ejecutivo
- **THEN** encuentra las conclusiones principales en lenguaje claro, cada una respaldada por un gráfico, sin código visible

### Requirement: Informe de calidad de datos

El sistema SHALL incluir un informe de calidad de datos que documente qué faltaba, qué se corrigió, qué quedó pendiente y por qué.

#### Scenario: Trazabilidad de las decisiones de limpieza

- **WHEN** se revisa el informe de calidad de datos
- **THEN** cada decisión de limpieza relevante (nulos, columnas eliminadas, valores negativos) aparece documentada con su motivo

### Requirement: README reproducible

El `README.md` del repositorio SHALL indicar de dónde salen los datos, cómo instalar las librerías y cómo ejecutar el notebook, el pipeline y el dashboard.

#### Scenario: Persona nueva reproduce el proyecto

- **WHEN** una persona nueva sigue las instrucciones del README en un entorno limpio
- **THEN** puede instalar dependencias, ejecutar el pipeline y abrir el notebook sin información adicional

### Requirement: Dependencias fijadas

El repositorio SHALL incluir un `requirements.txt` que liste las librerías necesarias para reproducir el análisis.

#### Scenario: Instalación desde requirements

- **WHEN** se ejecuta la instalación desde `requirements.txt` en un entorno limpio
- **THEN** quedan disponibles todas las librerías que usan el notebook, el pipeline y el dashboard
