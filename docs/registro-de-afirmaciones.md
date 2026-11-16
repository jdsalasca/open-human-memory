# Registro de afirmaciones

**Fecha:** 16 de noviembre de 2026
**Para qué:** evitar que el proyecto gire en círculos. Cada afirmación tiene estado,
nivel de evidencia y falsador. Si una afirmación no está aquí, no existe.

**Niveles** (definidos en `precedentes/09`, sección 9.5): E0 idea, E1 mecanismo
implementado, E2 comparación controlada local, E3 varias distribuciones, E4
reproducción independiente con tareas reales, E5 longitudinal y transferencia.

**Estados:** sostenida, refutada, abierta, inválida (no interpretable).

---

## A. Afirmaciones metodológicas

| ID | Afirmación | Estado | Evidencia |
|---|---|---|---|
| M1 | El 001 filtraba la regla en la superficie (target leakage) | Refutada como evidencia | `prototipo-001` |
| M2 | El 002 no usaba el historial: `MEM-A0` empata con `MEM-E` | Sostenida | `prototipo-002`, 3 semillas |
| M3 | El «100 % en D3» del 003 era artefacto del límite de profundidad 2 | Sostenida | 004-A: 64/64 sin memoria |
| M4 | El control `RANDOM` del 003 estaba ama­ñado (usaba `reverse`/`negate`) | Sostenida | 004-A: 250/560 perfectas del mismo lenguaje |
| M5 | La muestra `[:24]` del 006-B está sesgada (16 `sort_asc`, 8 `sort_desc`) | Sostenida | `errata-006b.md` |
| M6 | La condición `retrieved` del 006-B era oráculo, no recuperación | Sostenida | usaba `task.solution.program` |
| M7 | La condición `tool-forced` del 006-B no es interpretable | Sostenida | 16/24 trazas con errores de entorno |
| M8 | La ausencia de significación no es ausencia de efecto | Sostenida | IC ±20 pp |

## B. Afirmaciones sobre el mecanismo (macros)

| ID | Afirmación | Estado | Nivel | Falsador |
|---|---|---|---|---|
| H1 | Una biblioteca de macros reduce candidatos | Sostenida | E2 | — |
| H2 | Esa reducción es del 17,8 % en la rejilla completa | Sostenida | E2 | — |
| H3 | La reducción viene con 15,6 pp menos de cobertura | Sostenida | E2 | — |
| H4 | Con profundidad 3 permitida, la biblioteca encarece la búsqueda (+27,6 %) | Sostenida | E2 | — |
| H5 | La cobertura conductual de la biblioteca es 9/14 | Sostenida | E2 | — |
| H6 | La adquisición satura en 6 experiencias | Sostenida | E2 | — |
| H7 | El ahorro por acierto es 2,6 % | Sostenida | E2 | — |
| H8 | Las macros del 003 amplían la cobertura máxima en su D3 | **Refutada** | — | 004-A |
| H9 | La memoria puede mejorar competencia efectiva bajo presupuesto limitado | **Abierta** | — | P1, P2 |

## C. Afirmaciones sobre el valor de la memoria

| ID | Afirmación | Estado | Nivel | Falsador |
|---|---|---|---|---|
| V1 | Con continuidad 1,0, igual cobertura con 41,8 % menos pasos | Sostenida | E2 | — |
| V2 | Con continuidad 0,0, el mismo trabajo rinde 22,1 pp menos | Sostenida | E2 | — |
| V3 | Congelar lo aprendido ahorra 26,2 % de trabajo con igual precisión | Sostenida | E2 | — |
| V4 | Seguir acumulando empeora (−8,7 pp) | Sostenida | E2 | Política distinta que no empeore |
| V5 | El desalojo por uso arregla la acumulación | **Refutada** | — | −10,8 pp |
| V6 | La memoria recuperada ayuda a un LLM | **Inválida** | — | `ORACLE-MEMORY` |
| V7 | Un intérprete fiable ayuda a un LLM | **Abierta** | — | Condición inválida |

## D. Afirmaciones sobre la política

| ID | Afirmación | Estado | Nivel | Falsador |
|---|---|---|---|---|
| P1 | Una política lineal aprende a cambiar entre memoria y búsqueda | Sostenida | E2 | — |
| P2 | Esa política supera a una regla de una línea | **Refutada** | — | −1,0 pp, IC −3,1 a 0 |
| P3 | El probe de aplicabilidad aporta información | Sostenida | E2 | +5,2 pp sobre barajada, IC 1,0–9,4 |
| P4 | El probe paga su coste | **Refutada** | — | 41 pasos vs 29 ahorrados |
| P5 | Un controlador con más acciones ayudaría | **Abierta** | — | Sin evidencia |

## E. Afirmaciones teóricas

| ID | Afirmación | Estado | Nivel | Falsador |
|---|---|---|---|---|
| T1 | En espacio **explorable, identificable y dentro del presupuesto**, la memoria no amplía cobertura | Sostenida **con condiciones** | E0 + 004/006 | Un contraejemplo que cumpla las tres condiciones |
| T2 | En espacio no explorable bajo el presupuesto, una herramienta compilada amplía cobertura | **Abierta** (P1) | — | Cobertura igual sin historial |
| T3 | A igual información, un procedimiento bate a un episodio | **Abierta** (P2) | — | Empatan |
| T4 | `E(F)` baja solo con estructura compartida | **Abierta** (P3) | — | Baja con vocabulario compartido |
| T5 | El efecto sobrevive a cambiar de modelo | **Abierta** (P5) | — | Desaparece |
| T6 | Elegir la **forma** del conocimiento según utilidad futura bate a una forma fija | **Abierta** (P6) | — | Una forma fija iguala o supera |

## F. Afirmaciones sobre las fuentes

| ID | Afirmación | Estado |
|---|---|---|
| F1 | DreamCoder, Stitch y LILO cubren aprendizaje de bibliotecas | Sostenida (lectura) |
| F2 | CEGIS y Angluin cubren aprendizaje activo y contraejemplos | Sostenida (lectura) |
| F3 | MemDev-Bench muestra que la memoria puede romper tareas antes resolubles | **Sostenida y verificada** |
| F4 | La neurociencia y la sociología han aportado hipótesis comprobables | **Refutada**: solo analogías |
| F5 | Se ha ejecutado una revisión sistemática exhaustiva | **Refutada**: estructurada, una base, un revisor |
| F6 | Se ha reproducido un competidor | **Refutada**: ninguno |
| F7 | Existe una revisión estructurada con búsquedas y cribado registrados | **Sostenida** (`revision-sistematica/`) |
| F8 | La verificación independiente de skills ya está implementada y es imprescindible | **Declarada por terceros; no replicada** |
| F9 | Las bibliotecas de skills degradan al crecer | **Declarada por terceros; no replicada** |
| F10 | El lift agregado de retrieval no implica uso efectivo | **Declarada por terceros; no replicada** |
| F11 | La memoria episódica no mejora el resolve rate en código | **Declarada por terceros; no replicada** |
| F12 | Solo tres filas de la revisión están verificadas documentalmente; el resto son declaradas por los autores | **Sostenida** (extraccion.md) |
| F13 | Ninguna cifra de la revisión está replicada | **Sostenida** |

## G. Retención y transferencia (Prototipo 007)

| ID | Afirmación | Estado | Nivel | Falsador |
|---|---|---|---|---|
| G1 | `gpt-6.1-terra` medium resuelve profundidad 5–9 con 1–3 ejemplos en esta familia | Sostenida | E2 local | Un modelo o familia donde el clon falle de forma estable |
| G2 | Un procedimiento verificado presentado como programa completo perjudica la composición (8/0) | Sostenida | E2 local | Repetir sin el anclaje del prompt |
| G3 | Presentado como subrutina, no supera a un placebo (11/11) | Sostenida | E2 local | Un artefacto necesario, no solo útil |

---

## Lo que este registro dice del proyecto

- **34 sostenidas**: 29 propias (casi todas E2 locales) y 5 declaradas por terceros,
  no replicadas.
- **8 refutadas**, incluidas nuestras dos hipótesis principales.
- **9 abiertas o inválidas**, y son justo las que responderían la pregunta del
  proyecto.
- **0 en E3, E4 o E5 propias.**
- **0 competidores reproducidos.**

El patrón es claro: somos buenos refutando nuestros propios mecanismos y malos
construyendo evidencia acumulativa. La causa está en `docs/teoria.md`: seis
prototipos en el mismo régimen enumerable, donde la teoría predice que no puede
haber expansión. La revisión de antecedentes confirma que el campo ya pasó por
donde nosotros estamos: bibliotecas con aplicabilidad y terminación, verificación
por ejecución, benchmarks de transferencia y resultados negativos a escala.

## Regla de mantenimiento

1. Toda afirmación nueva entra aquí **antes** del experimento, con su falsador.
2. Un resultado negativo cambia el estado; no se borra la fila.
3. Un cambio de estado exige enlace al resultado crudo.
4. Las filas `inválida` se conservan: son lecciones metodológicas.
