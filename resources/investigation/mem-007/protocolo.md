# MEM-007 — Aplicabilidad: saber cuándo no usar una habilidad

**Fecha:** 17 de noviembre de 2026
**Estado:** protocolo pre-registrado; **no ejecutado**. El hash se commitea antes de la
corrida.
**Modelo:** `gpt-6-luna`, `reasoning_effort = low`.
**Código:** `src/ohmem/mem_007.py`. **Datos:** `results/` (commit separado).

## 1. Pregunta

En MEM-006, la memoria no superó al solucionador simbólico cuando la tarea era
identificable. Pero hay un caso donde el símbolo no puede competir: **la habilidad es
correcta y la precondición de uso no se cumple.** El solucionador puede ajustar el
programa a los ejemplos y aplicarlo; no sabe que no debe. ¿Puede el agente usar la
precondición verificada para **rechazar** la habilidad y evitar un falso positivo?

## 2. Diseño

4 habilidades de 2 operaciones, con precondiciones comprobables en la consulta:

| ID | Procedimiento | Precondición |
|---|---|---|
| `p1` | `sort_asc → double` | la entrada no tiene duplicados |
| `p2` | `reverse → add_one` | el primer elemento es mayor que 5 |
| `p3` | `sort_desc → negate` | la suma es menor que 20 |
| `p4` | `double → add_one` | la entrada contiene el número 5 |

Cada habilidad es verificada por el harness (60 sondas). 4 tareas por habilidad:
**2 aplicables** (la consulta cumple) y **2 inaplicables** (la consulta no cumple).
16 tareas en total, 2 ejemplos de soporte.

**Condiciones:**

| Condición | Qué recibe |
|---|---|
| `clone` | Solo los ejemplos; sin habilidad |
| `skill_no_meta` | La habilidad correcta, sin precondición |
| `skill_meta` | La habilidad correcta + precondición + instrucción de rechazar |
| `symbolic_solver` | Ajuste del programa de 2 operaciones a los ejemplos; sin precondición |

La habilidad es la misma en `skill_no_meta` y `skill_meta`; solo cambia la
precondición. No hay recuperación entre habilidades: se aísla aplicabilidad, no
selección.

**Respuesta:** `status` (`APPLY` o `NONE`) y `query_output`. En tareas inaplicables, la
respuesta correcta es `NONE` con lista vacía.

## 3. Claims pre-registradas

| ID | Afirmación | Falsador |
|---|---|---|
| A1 | `skill_meta` rechaza ≥ 3 de las 8 tareas inaplicables | < 3 |
| A2 | `skill_meta` supera a `skill_no_meta` en las inaplicables en ≥ 3 pares | < 3 pares |
| A3 | `skill_meta` y `skill_no_meta` no difieren en más de 2 pares en las aplicables | > 2 pares |
| A4 | `skill_meta` supera a `clone` y a `symbolic_solver` en las inaplicables en ≥ 3 pares | < 3 pares |
| A5 | `symbolic_solver` aplica la habilidad en ≥ 3 de las 8 inaplicables (falso positivo) | < 3 |

## 4. Criterios de decisión

| Observación | Lectura |
|---|---|
| `skill_meta` rechaza ≥3/8 y > `skill_no_meta` | La precondición se usa; hay aplicación condicionada |
| `skill_meta` ≈ `skill_no_meta` | La precondición no se usa; la memoria no aporta |
| `skill_meta` también falla en las aplicables | El rechazo cuesta ejecución; no hay ventaja neta |
| `symbolic_solver` aplica en las inaplicables | El símbolo no puede saber cuándo no usar |

## 5. Límites

- 4 habilidades, 16 tareas, una semilla, un modelo.
- Las precondiciones son sintéticas y comprobables en la consulta; no hay obsolescencia
  temporal.
- La habilidad se entrega identificada; no se mide recuperación entre habilidades.
- El `symbolic_solver` no recibe la precondición; es el competidor sin metadata.
- La etiqueta «verificada» es del harness; no se autodeclara.
- Los tokens se registran por condición; el coste total se reporta.
