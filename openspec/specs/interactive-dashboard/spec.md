# interactive-dashboard Specification

## Purpose
Ofrecer al cliente una aplicación interactiva donde pueda filtrar y explorar los datos limpios por su cuenta (por estado y por periodo), viendo métricas clave y su evolución sin tocar código.

## Requirements

### Requirement: Dashboard interactivo sobre el dataset limpio

El sistema SHALL ofrecer un dashboard interactivo que cargue el dataset limpio y permita filtrar por al menos estado y rango de fechas, actualizando las visualizaciones según el filtro.

#### Scenario: Filtrar por estado y fechas

- **WHEN** el usuario selecciona un estado y un rango de fechas en el dashboard
- **THEN** las métricas y los gráficos se actualizan para reflejar solo los datos filtrados

#### Scenario: Visualización de métricas clave

- **WHEN** el usuario abre el dashboard
- **THEN** ve las métricas clave y al menos un gráfico de evolución temporal del conjunto o del estado seleccionado

### Requirement: Arranque del dashboard documentado

El dashboard SHALL arrancar con un comando único documentado en el README y cargar el dataset limpio generado por el pipeline.

#### Scenario: Arranque local del dashboard

- **GIVEN** el pipeline ya generó el dataset limpio
- **WHEN** la persona ejecuta el comando documentado para arrancar el dashboard
- **THEN** el dashboard abre en el navegador y muestra los datos sin pasos manuales adicionales
