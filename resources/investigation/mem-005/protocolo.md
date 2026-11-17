# MEM-005 — Factorial contenido × estado × instrucción

**Fecha:** 16 de noviembre de 2026
**Estado:** protocolo pre-registrado; corrida en curso.
**Modelo:** `gpt-6-luna`, `reasoning_effort = low`.
**Código:** `src/ohmem/mem_005.py`.
**Datos:** `results/factorial-seed1.json`.

## 1. Por qué

MEM-003/004 cambiaron dos cosas a la vez: el **estado comunicado** (candidata vs
verificada) y la **instrucción operativa** (verificar vs aplicar). También faltaba el
control de un **programa escrito por un programador**, sin sesión previa de
aprendizaje. Sin ese control no se separa el valor del contenido del valor del proceso
de adquisición.

Además, las tareas de MEM-003/004 ya eran identificables desde los dos ejemplos: el
clon tenía la información. Lo que se mide es **inferir el programa frente a recibirlo**,
no un hecho que solo estuviera en la memoria.

## 2. Diseño

2 operaciones, 12 tareas, semilla 1 (nuevas tareas), 2 ejemplos de soporte. Diez
condiciones, orden aleatorizado por tarea:

| Condición | Contenido | Estado | Instrucción |
|---|---|---|---|
| `clone` | — | — | — |
| `correct_candidate_verify` | Correcto | Candidata | Verificar |
| `correct_candidate_apply` | Correcto | Candidata | Aplicar |
| `correct_verified_verify` | Correcto | Verificado | Verificar |
| `correct_verified_apply` | Correcto | Verificado | Aplicar |
| `placebo_candidate_verify` | Falso | Candidata | Verificar |
| `placebo_candidate_apply` | Falso | Candidata | Aplicar |
| `placebo_verified_verify` | Falso | Verificado | Verificar |
| `placebo_verified_apply` | Falso | Verificado | Aplicar |
| `written_verified_apply` | Correcto | Programador | Aplicar |

El programa correcto es el verificado en la sesión 1; el placebo es
`sort_desc → double`; el programa escrito es el motivo `sort_asc → double`, atribuido
a un programador y sin sesión previa.

## 3. Claims pre-registradas

| ID | Afirmación | Falsador |
|---|---|---|
| M13 | Con contenido correcto, estado verificado e instrucción de aplicar, el contenido correcto supera al placebo en ≥ 3 pares | < 3 pares |
| M14 | Con contenido correcto e instrucción de aplicar, el estado verificado supera a la candidata en ≥ 3 pares | < 3 pares |
| M15 | Con contenido correcto y estado verificado, la instrucción de aplicar supera a la de verificar en ≥ 3 pares | < 3 pares |
| M16 | El programa escrito por un programador queda a ≤ 2 pares del programa aprendido verificado | > 2 pares de diferencia |
| M17 | La condición correcta+verificada+aplicar acierta ≥ 9/12 en la semilla 1 | < 9/12 |

## 4. Criterios de decisión

| Observación | Lectura |
|---|---|
| El contenido correcto supera al placebo bajo el mismo estado e instrucción | El contenido importa, no solo la etiqueta |
| El estado verificado supera a la candidata con la misma instrucción | El estado comunicado tiene efecto propio |
| La instrucción de aplicar supera a la de verificar con el mismo estado | La instrucción operativa tiene efecto propio |
| El programa escrito ≈ el aprendido | La ventaja es del contenido, no de la adquisición |
| El programa escrito < el aprendido | La adquisición o la procedencia añaden algo |

## 5. Límites

- Una semilla, 12 tareas, un modelo; no es confirmatorio.
- Las tareas son de 2 operaciones y ya son identificables desde los dos ejemplos: el
  resultado mide **inferir frente a recibir**, no un hecho desconocido.
- El programa escrito usa el motivo; el aprendido puede ser una variante equivalente.
- Los valores p no corrigen por comparaciones múltiples.
- El orden de condiciones se aleatoriza por tarea, pero el servicio puede variar.
- El placebo comparte `double` con el motivo; es parcialmente pertinente.
