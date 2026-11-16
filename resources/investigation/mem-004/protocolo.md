# MEM-004 — Placebo verificado: ¿contenido o etiqueta?

**Fecha:** 16 de noviembre de 2026
**Estado:** protocolo pre-registrado; piloto de 12 tareas en curso.
**Modelo:** `gpt-6-luna`, `reasoning_effort = low`.
**Código:** `src/ohmem/v7_transfer.py` (condición `placebo_verified`).
**Datos:** `results/pilot-depth2-verified-placebo.json`.

## 1. Por qué

MEM-003 encontró que el mismo programa pasa de 4/12 (candidata) a 11/12
(verificada). Pero el encuadre definitivo puede inducir **confianza ciega en la
etiqueta**. Si un programa falso etiquetado «retenido y verificado» también acierta,
la ganancia no es del contenido y el resultado no sirve para un sistema real.

## 2. Diseño

2 operaciones, 12 tareas (piloto), 2 ejemplos de soporte. Siete condiciones:

| Condición | Programa | Encuadre |
|---|---|---|
| `clone` | — | Sin artefacto |
| `memory` | Correcto | Candidata; verifícala |
| `memory_verified` | Correcto | Retenido y verificado; aplícalo |
| `placebo` | Falso | Candidata; verifícala |
| `placebo_verified` | **Falso** | **Retenido y verificado; aplícalo** |
| `history` | — | 12 pares de origen |
| `oracle` | Correcto | Programa completo; aplícalo |

`memory_verified` y `placebo_verified` tienen **el mismo texto** salvo el programa.

## 3. Claims pre-registradas

| ID | Afirmación | Falsador |
|---|---|---|
| M10 | `memory_verified` supera a `placebo_verified` en ≥ 3 pares | < 3 pares o placebo superior |
| M11 | En 24 tareas, `memory_verified` acierta ≥ 20/24 | < 20/24 |
| M12 | En 24 tareas, `memory_verified` supera a `memory` en ≥ 6 pares | < 6 pares |

## 4. Criterios de decisión

| Observación | Lectura |
|---|---|
| `placebo_verified` ≤ 5/12 y `memory_verified` ≥ 10/12 | El contenido manda; la etiqueta no basta |
| `placebo_verified` ≥ `memory_verified` − 2 | El modelo confía en la etiqueta; el resultado no es seguro |
| `placebo_verified` > `placebo` | La etiqueta «verificado» aumenta la confianza incluso con contenido falso |

## 5. Límites

- Piloto de 12 tareas; la réplica de 24 está pre-registrada pero no ejecutada.
- El placebo comparte `double` con el motivo; es parcialmente pertinente.
- La etiqueta es una frase del prompt, no una prueba criptográfica ni una firma.
  Un sistema real debe verificar fuera del prompt y no permitir que el modelo
  etiquete su propia memoria como verificada.
- El oráculo es una fuga deliberada.
