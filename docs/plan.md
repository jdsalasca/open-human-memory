# Plan — open-human-memory

Objetivo: un servicio de memoria con ciclo de vida biológico y capa social, que
se instale en un computador y corra en Docker, consumible por agentes vía MCP.

## Rondas

### R1 — Investigación (completada)

- Entregable: `resources/investigation/` con 27 documentos, papers finales de
  CUMULUS (EN/ES) y JANUS (ES), y bibliografía con fuentes primarias.
- Criterio: cada mecanismo propuesto tiene fuente, traducción computacional y
  riesgo declarado; las preguntas de momento cero, contexto, filosofía,
  compactación, sueño, atención y DeepSeek tienen respuesta documentada.
- Revisión mayor incorporada: `22`–`27`; competidores 2026 en `precedentes/06` a
  `08`.

### R1.5 — Plan de implementación

- Entregable: `27-plan-de-implementacion.md` con JANUS-C, sandbox, baselines,
  métricas y fases.
- Criterio: el MVP demuestra que los certificados y la calibración reducen el
  efecto equivocado y la reutilización dañina frente a COUNTERMEM-style.

### R2 — Documento de diseño

- Entregable: especificación técnica de los objetos epistémicos de CUMULUS y
  JANUS (SIR, ledger de decisiones, identificabilidad, ledger de incertidumbre,
  agenda experimental) derivada de `24` y `papers/janus-v0.2.md`.
- Criterio: enfoque elegido, alcance del MVP, no-objetivos, modelo de datos y
  decisiones abiertas resueltas o asignadas.

### R2.5 — Experimento diferencial A–E

- Entregable: sandbox con verdad causal conocida y las cinco condiciones del
  programa v2.
- Criterio: E reduce errores persistentes, mejora calibración y abandona antes
  creencias refutadas frente a C y D; si no, se reduce el alcance.

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
