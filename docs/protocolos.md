# Registro de protocolos experimentales

Este archivo existe para evitar la colisión de identificadores detectada en la
auditoría: `A–E` se usaba para dos experimentos distintos y `C0–C8` no coincidía
con los criterios del plan. **Las letras son locales a cada protocolo; el ID
canónico incluye el prefijo.**

## Protocolos vigentes

### `MAIN-C0..C8` — protocolo principal

Documento: `resources/investigation/08-hipotesis-y-experimentos.md` v2.0.

| ID | Condición |
|---|---|
| MAIN-C0 | Sin memoria |
| MAIN-C1 | Resumen rodante |
| MAIN-C2 | RAG sobre episodios/hechos |
| MAIN-C3 | Rival simple: Markdown + tests + recuperador |
| MAIN-C4 | Zep Agent Skills (adaptación) |
| MAIN-C5 | MSCE-style |
| MAIN-C6 | CUMULUS sin capa social |
| MAIN-C7 | CUMULUS completo |
| MAIN-C8 | JANUS (contrafactual + puerta causal) |

**Hipótesis que valida:** H1 (CUMULUS vs rival simple), H2–H4, H7.
**Estado:** pendiente de ejecución.

### `MEM-A..E` — diagnóstico de mecanismos

Documento: `resources/investigation/29-experimento-diagnostico.md` y
`prototipo-002-diagnostico/`.

| ID | Condición |
|---|---|
| MEM-A | Sin memoria (respuesta fija) |
| **MEM-A0** | **Mismo solucionador composicional sin historial** |
| MEM-B | Retrieval por similitud |
| MEM-C | Oráculo (techo) |
| MEM-D | Procedimiento de una primitiva |
| MEM-E | Abstracción composicional |

**Hipótesis que valida:** ninguna; es un diagnóstico para decidir qué capa
importa. `MEM-A0` demostró que `MEM-E` no usa historial: el 002 es un benchmark de
solucionador.
**Estado:** ejecutado (Prototipo 002, 3 semillas).

### `LEARN-*` — aprendizaje de macros

Documento: `prototipo-003-aprendizaje/`.

| ID | Condición |
|---|---|
| LEARN-NONE | Sin macros; solucionador de profundidad 2 |
| LEARN-RANDOM | Mismo tamaño de biblioteca, macros distractoras |
| LEARN-MACROS | Macros aprendidas de la experiencia |
| LEARN-ABLATED | Macros borradas tras entrenar |

**Hipótesis que valida:** la experiencia produce una capacidad nueva y la
ablación la elimina.
**Estado:** ejecutado (Prototipo 003, 3 semillas).

### `CAUSAL-A..E` — experimento causal (histórico)

Documento: `resources/investigation/24-programa-de-investigacion-v2.md`
(histórico). Comparaba episodios, playbooks, anti-persistencia, JANUS y JANUS +
incertidumbre. **Deprecado como identificador** para evitar confusión con
`MEM-A..E`. La comparación causal se redefinirá como `COMP-C..E` o `MAIN-C8`.

### `COMP-*` — competencia acumulativa (planificado)

**Fases del programa** (no son tratamientos comparables):

| ID | Fase |
|---|---|
| COMP-P1 | Primitivas |
| COMP-P2 | Composición |
| COMP-P3 | Abstracción entre dominios |
| COMP-P4 | Aprender a aprender |

**Tratamientos del experimento** (misma tarea, mismo presupuesto):

| ID | Tratamiento |
|---|---|
| COMP-T0 | Sin experiencias históricas |
| COMP-T1 | Experiencias irrelevantes (control de tamaño) |
| COMP-T2 | Retrieval real |
| COMP-T3 | Abstracciones aprendidas durante tareas anteriores |

La comparación válida es `COMP-T3` vs `COMP-T0/T1/T2`, no `COMP-P*` entre sí.

**Estado:** diseño; no ejecutado.

## Reglas

1. Todo resultado debe citar `ID + versión del protocolo`.
2. No se reutilizan letras sin prefijo en tablas o papers.
3. `MEM-*` no prueba hipótesis de arquitectura; solo diagnostica.
4. `MAIN-*` es el protocolo que decide CUMULUS.
5. `COMP-*` es el que decide expansión de competencia.
6. Un protocolo se congela antes de la corrida principal; los cambios se
   versionan.

## Prioridad actual

1. `MEM-*` — hecho (Prototipo 002).
2. `COMP-*` — siguiente: transferencia composicional con tareas reales/LLM.
3. `MAIN-*` — solo si `COMP-*` muestra que la memoria/procedimiento es el cuello.
4. `CAUSAL-*` — solo si `COMP-*` muestra que la identificación causal es el cuello.
