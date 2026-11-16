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

### R2.5 — Validación del aprendizaje de macros `VALID-*` (completada)

- Entregable: `prototipo-004-validez/` con protocolo congelado antes de medir,
  rejilla completa de 64 programas, control sin memoria a profundidad 3, barrido de
  las 560 bibliotecas del mismo lenguaje, curva de adquisición, costo
  compartido/incremental y registro de uso de macros.
- Criterio: si `VALID-A1` (sin historial, profundidad 3) iguala o supera a
  `VALID-A3` (macros aprendidas), se retira la afirmación de «capacidad nueva».
- Resultado: **criterio cumplido**. 64/64 frente a 54/64. La biblioteca ahorra
  17,8 % de candidatos y pierde 15,6 pp de cobertura; por acierto el ahorro es
  2,6 %. Solo gana con presupuesto ≤ 40 candidatos por tarea. Saturación en 6
  experiencias. El control `RANDOM` del 003 queda invalidado (250/560 bibliotecas
  arbitrarias del mismo lenguaje eran perfectas en su D3).
- Registro de IDs: `docs/protocolos.md` (`VALID-*`).

### R2.6 — Memoria bajo presupuesto `BUDGET-*` (005-A, exploratorio)

- Entregable: `prototipo-005-presupuesto/` con contabilidad de pasos ejecutados,
  deduplicación conductual, curvas de continuidad, control de orden de búsqueda,
  selección por desarrollo y flujo prequential con cuatro políticas.
- Criterio: si con continuidad total la biblioteca no ahorra trabajo a igual
  cobertura, o si acumular supera a congelar, se retira la línea.
- Resultado: **41,8 % menos pasos con cobertura idéntica en continuidad total**;
  **−22,1 pp en continuidad cero**; **congelar ahorra 26,2 % de trabajo**;
  **acumular cuesta −8,7 pp** y el controlador con tope **−10,8 pp** (hipótesis
  propia refutada).
- Requisito para el 005-B: protocolo congelado con hash de código y datos, tareas
  reservadas y una política de activación aprendida, no heurística.

### R2.7 — Política de activación y techo del agente `POLICY-*` (006)

- Entregable: `prototipo-006-politica/` con protocolo, código y datos congelados
  por hash; `prototipo-006-agente-llm/` con el test de techo.
- Criterio: la política aprendida debe superar a cada acción fija en acierto y
  pagar su propio costo de señal.
- Resultado: **acierto sí, economía no.** +3,1 pp sobre la mejor acción fija y
  +10,4 pp sobre buscar, pero el probe cuesta 96–122 pasos frente a 29 ahorrados.
  El agente real acierta **30/64 (46,9 %)**, por debajo de BFS profundidad 2.
- **Corrección posterior (006-A′):** cinco fallos de implementación encontrados
  por la auditoría. Corregidos y pareados, la política **no supera a la regla
  simple** (−1,0 pp) y **cuesta 1,9× más**. El resultado positivo queda retirado.
- Siguiente: procedimiento recuperado en el agente real y probe barato (caché por
  firma o índice), con protocolo congelado. Ver `docs/revision-de-rumbo.md`.

### R2.8 — Experimento de competencia `COMP-*`

- Entregable: sandbox con verdad causal conocida, tareas adversariales (ruido,
  ambigüedad, equivalencias, deriva, macros perjudiciales) y actualización online
  durante la secuencia.
- Criterio: `COMP-T3` (abstracciones aprendidas) supera a `COMP-T0/T1/T2` en
  errores persistentes, calibración y abandono de creencias refutadas **a igual
  presupuesto de cómputo**; si no, se reduce el alcance.
- Requisito institucional: protocolo congelado, tareas reservadas y criterios
  definidos antes de la corrida principal. Las mejoras exploratorias van a otro
  documento y no sustituyen la evaluación.
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
