# Plan — open-human-memory

Objetivo: un servicio de memoria con ciclo de vida biológico y capa social, que
se instale en un computador y corra en Docker, consumible por agentes vía MCP.

## Rondas

### R1 — Investigación (completada)

- Entregable: `resources/investigation/` con 23 documentos, paper de trabajo,
  papers CUMULUS (EN/ES), revisión v0.2, JANUS y bibliografía con fuentes
  primarias.
- Criterio: cada mecanismo propuesto tiene fuente, traducción computacional y
  riesgo declarado; las preguntas de momento cero, contexto, filosofía del
  contexto, compactación humana y sueño tienen respuesta documentada.
- Revisión mayor incorporada: `22-respuesta-a-revision.md` y
  `23-marco-de-validez.md`; competidores 2026 en `precedentes/06`.

### R2 — Documento de diseño

- Entregable: especificación técnica de CUMULUS y JANUS (esquema SIR, ledger de
  decisiones, contrafactuales, algoritmos de Forja y Puente, protocolo del Pod)
  derivada de `papers/cumulus-es.md`, `papers/cumulus-en.md` y
  `papers/janus-es.md`.
- Criterio: enfoque elegido, alcance del MVP, no-objetivos, modelo de datos y
  decisiones abiertas resueltas o asignadas.

### R2.5 — Validación causal (JANUS)

- Entregable: prototipo del ledger de decisiones + jerarquía de evidencia
  contrafactual + puerta de promoción causal.
- Criterio: reduce habilidades espurias ≥30% frente a CUMULUS sin causalidad en
  un entorno con verdad causal conocida.

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
