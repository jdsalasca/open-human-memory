# MEM-003 — Encuadre: candidata frente a programa verificado

**Fecha:** 16 de noviembre de 2026
**Estado:** protocolo pre-registrado; corrida en curso.
**Modelo:** `gpt-6-luna`, `reasoning_effort = low`.
**Código:** `src/ohmem/v7_transfer.py` (condición `memory_verified`).
**Datos:** `results/pilot-depth2.json`.

## 1. Por qué

En MEM-002 (2 operaciones), la memoria rindió **7/12** y el oráculo **11/12** con el
**mismo programa**. La diferencia no es de contenido: es el encuadre. La memoria se
presenta como «subrutina candidata; verifícala y úsala si encaja», mientras el oráculo
dice «programa completo de esta tarea; aplícalo». Si el encuadre explica la brecha, un
programa retenido presentado como definitivo debería acercarse al oráculo.

## 2. Diseño

**Sesión 1:** 12 pares del motivo `sort_asc → double`; verificación con 60 sondas.

**Sesión 2:** 12 tareas de **2 operaciones** (el motivo completo), 2 ejemplos de
soporte. Seis condiciones pareadas:

| Condición | Encuadre |
|---|---|
| `clone` | Sin artefacto |
| `memory` | «Subrutina candidata; verifícala y úsala si encaja» |
| `memory_verified` | «Programa retenido y verificado; aplícalo» |
| `placebo` | Programa falso con el encuadre de candidata |
| `history` | Los 12 pares de la sesión 1 |
| `oracle` | «Programa completo de esta tarea; aplícalo» (fuga) |

**Diferencia clave:** `memory` y `memory_verified` contienen el **mismo programa**;
solo cambia la instrucción. `oracle` contiene el mismo programa con el encuadre
definitivo de la tarea.

## 3. Claims pre-registradas

| ID | Afirmación | Falsador |
|---|---|---|
| M5 | `memory_verified` supera a `memory` en ≥ 3 pares | < 3 pares |
| M6 | `memory_verified` acierta ≥ 10/12 | < 10/12 |
| M7 | `history` supera a `memory` en ≥ 2 pares | < 2 pares |
| M8 | `memory_verified` supera al placebo en ≥ 3 pares | < 3 pares |
| M9 | `oracle` acierta ≥ 10/12 | < 10/12 |

## 4. Criterios de decisión

| Observación | Lectura |
|---|---|
| `memory_verified` ≥ 10/12 y > `memory` por ≥ 3 pares | El encuadre era el cuello; el contenido retenido es usable |
| `memory_verified` ≈ `memory` | El modelo no aplica el programa retenido ni cuando es autoritativo |
| `history` > `memory_verified` | Las experiencias crudas siguen siendo mejores que el programa explícito |
| `oracle` < 10/12 | La tarea no es aplicable; no se interpreta la memoria |

## 5. Límites

- Una semilla, 12 tareas, un modelo; no es confirmatorio.
- El encuadre `memory_verified` cambia más de una palabra respecto a `memory` y
  `oracle`; la comparación es de autoridad/instrucción, no de un token aislado.
- El historial tiene más tokens (853 vs 458 vs 371).
- El placebo comparte `double` con el motivo; las clases de placebo quedan pendientes.
- El oráculo es una fuga deliberada.
