# Plan — open-human-memory

Objetivo: un servicio de memoria con ciclo de vida biológico y capa social, que
se instale en un computador y corra en Docker, consumible por agentes vía MCP.

## Rondas

### R1 — Investigación (completada)

- Entregable: `resources/investigation/` con 20 documentos, paper de trabajo,
  papers CUMULUS en inglés/español y bibliografía con fuentes primarias.
- Criterio: cada mecanismo propuesto tiene fuente, traducción computacional y
  riesgo declarado; las preguntas de momento cero, contexto, filosofía del
  contexto, compactación humana y sueño tienen respuesta documentada.

### R2 — Documento de diseño

- Entregable: especificación técnica de CUMULUS (esquema SIR, algoritmos de
  Forja y Puente, protocolo del Pod) derivada de `papers/cumulus-es.md` y
  `papers/cumulus-en.md`.
- Criterio: enfoque elegido, alcance del MVP, no-objetivos, modelo de datos y
  decisiones abiertas resueltas o asignadas.

### R3 — Harness de evaluación

- Entregable: proyecto sintético longitudinal + líneas base (contexto completo,
  resumen rodante, RAG) + métricas del doc 08.
- Criterio: corre de punta a punta y produce un reporte reproducible.

### R4 — Núcleo MVP (A–D)

- Entregable: servicio con `encode`, `recall`, `consolidate`, `forget`,
  playbooks y MCP; almacenamiento local.
- Criterio: C3 supera a C1 en ≥ 2 métricas primarias con efecto ≥ 10%.

### R5 — Capa social (E)

- Entregable: directorio de expertise, pods, dialectos, `teach`, reputación,
  gobernanza básica.
- Criterio: C4 supera a C3 en ≥ 1 métrica social.

### R6 — Producto

- Entregable: Dockerfile, `docker compose`, configuración, documentación de
  instalación y demo.
- Criterio: instalación limpia en una máquina sin dependencias previas y
  verificación visual del flujo.

## Regla de corte

Ningún módulo entra a producción sin ablación que lo justifique. Si el sistema
no supera a un RAG con resumen, se reduce el alcance.
