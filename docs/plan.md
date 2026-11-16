# Plan — open-human-memory

Objetivo: un servicio de memoria con ciclo de vida biológico y capa social, que
se instale en un computador y corra en Docker, consumible por agentes vía MCP.

## Rondas

### R1 — Investigación (completada)

- Entregable: `resources/investigation/` con 29 documentos, papers finales de
  CUMULUS (EN/ES) y JANUS (ES), y bibliografía con fuentes primarias.
- Criterio: cada mecanismo propuesto tiene fuente, traducción computacional y
  riesgo declarado; las preguntas de momento cero, contexto, filosofía,
  compactación, sueño, atención y DeepSeek tienen respuesta documentada.
- Revisión mayor incorporada: `22`–`29`; competidores 2026 en `precedentes/06` a
  `08`.

### R1.5 — Programa de competencia y diagnóstico

- Entregable: `28-programa-de-competencia.md`,
  `29-experimento-diagnostico.md`, `docs/protocolos.md`, harness `src/ohmem/` y
  `prototipo-002-diagnostico/` con resultados crudos.
- Criterio: el diagnóstico distingue memoria, selección, procedimiento y
  composición antes de construir otra arquitectura.
- Resultado: sin filtración, retrieval no basta; una primitiva resuelve reglas
  simples; la composición es el discriminador. No es un resultado sobre LLM.

### R2 — Documento de diseño

- Entregable: especificación técnica de los objetos epistémicos de CUMULUS y
  JANUS (SIR, ledger de decisiones, identificabilidad, ledger de incertidumbre,
  agenda experimental) derivada de `24` y `papers/janus-v0.2.md`.
- Criterio: enfoque elegido, alcance del MVP, no-objetivos, modelo de datos y
  decisiones abiertas resueltas o asignadas.

### R2.5 — Experimento de competencia `COMP-A..E`

- Entregable: sandbox con verdad causal conocida y las fases de primitivas,
  composición, abstracción entre dominios y aprender a aprender.
- Criterio: `COMP-E` reduce errores persistentes, mejora calibración y abandona
  antes creencias refutadas frente a `COMP-B/C/D`; si no, se reduce el alcance.
- Registro de IDs: `docs/protocolos.md`.

### R3 — Harness de evaluación

- Entregable: proyecto sintético longitudinal + líneas base (contexto completo,
  resumen rodante, RAG) + métricas del doc 08.
- Criterio: corre de punta a punta y produce un reporte reproducible.

### R4 — Núcleo MVP

- Entregable: servicio con `encode`, `recall`, `consolidate`, `forget`,
  playbooks y MCP; almacenamiento local.
- Criterio: `MAIN-C6` supera a `MAIN-C3` en la métrica primaria con IC 95% que
  excluya cero.

### R5 — Capa social

- Entregable: directorio de expertise, pods, dialectos, `teach`, reputación,
  gobernanza básica.
- Criterio: `MAIN-C7` supera a `MAIN-C6` en ≥ 1 métrica social con presupuesto
  igualado; si no, se elimina la capa.

### R6 — Producto

- Entregable: Dockerfile, `docker compose`, configuración, documentación de
  instalación y demo.
- Criterio: instalación limpia en una máquina sin dependencias previas y
  verificación visual del flujo.

## Regla de corte

Ningún módulo entra a producción sin ablación que lo justifique. Si el sistema
no supera a un RAG con resumen, se reduce el alcance.
