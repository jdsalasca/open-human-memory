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

### `LEARN-*` — aprendizaje de macros (exploratorio, superado)

Documento: `prototipo-003-aprendizaje/`.

| ID | Condición |
|---|---|
| LEARN-NONE | Sin macros; solucionador de profundidad 2 |
| LEARN-RANDOM | Mismo tamaño de biblioteca, macros distractoras (`reverse`/`negate`) |
| LEARN-MACROS | Macros aprendidas de la experiencia |
| LEARN-ABLATED | Macros compiladas borradas tras entrenar |

**Hipótesis que validaba:** la experiencia produce una capacidad nueva y la
ablación la elimina.
**Estado:** ejecutado (Prototipo 003, 3 semillas) y **retirado por `VALID-*`**.
`LEARN-ABLATED` borra macros, no historial; `LEARN-RANDOM` usaba operaciones
ajenas al lenguaje del generador.

### `VALID-*` — validez del aprendizaje de macros (Prototipo 004-A)

Documento: `prototipo-004-validez/` y su `protocolo-congelado.md` (SHA-256
verificado antes de medir).

| ID | Condición | Profundidad |
|---|---|---|
| VALID-A0 | Sin memoria | 2 |
| VALID-A1 | Sin memoria | **3** |
| VALID-A2 | 3 macros del mismo lenguaje, sin historial | 2 |
| VALID-A3 | Macros aprendidas de la experiencia | 2 |
| VALID-A4 | Macros aprendidas de la experiencia | 3 |
| VALID-SWEEP | Las 560 bibliotecas de 3 macros sobre los 16 pares del generador | 2 |

**Hipótesis que contrasta:** H1 (la experiencia produce una mejora que el mismo
solucionador sin historial no consigue) y H2 (las abstracciones reducen el costo
total con rendimiento comparable).
**Estado:** ejecutado (3 semillas, 64 tareas). **H1 refutada; H2 solo a
presupuesto ≤ 40 candidatos por tarea.**

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

`VALID-*` es el piloto sintético de este diseño y ya mostró el problema: sin
`COMP-T0` con el **mismo presupuesto de búsqueda**, la comparación no identifica
nada.

**Estado:** diseño; no ejecutado. Congelar antes de la corrida principal.

## Reglas

1. Todo resultado debe citar `ID + versión del protocolo`.
2. No se reutilizan letras sin prefijo en tablas o papers.
3. `MEM-*` no prueba hipótesis de arquitectura; solo diagnostica.
4. `MAIN-*` es el protocolo que decide CUMULUS.
5. `COMP-*` es el que decide expansión de competencia.
6. Un protocolo se congela antes de la corrida principal; los cambios se
   versionan.

## Prioridad actual

1. `VALID-*` — hecho (Prototipo 004-A). H1 refutada; H2 acotada a presupuesto bajo.
2. `COMP-*` — siguiente: tareas adversariales, actualización online y comparación
   con Stitch/DreamCoder. Protocolo congelado antes de medir.
3. `MAIN-*` — solo si `COMP-*` muestra que la memoria/procedimiento es el cuello.
4. `CAUSAL-*` — solo si `COMP-*` muestra que la identificación causal es el cuello.
