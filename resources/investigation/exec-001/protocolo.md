# EXEC-001 — Mapa de aplicación de programas

**Fecha:** 16 de noviembre de 2026
**Estado:** protocolo pre-registrado; no ejecutado.
**Modelo:** `gpt-6-luna`, `reasoning_effort = low`.
**Código:** por implementar sobre `src/ohmem/v7_transfer.py`.

## 1. Pregunta

El 007B mostró que, con el programa completo, `luna` resuelve 2/12 tareas de cinco
pasos. No sabemos si falla la ejecución de las operaciones, el orden, la aritmética,
la interpretación de los nombres o el seguimiento de instrucciones. EXEC-001 separa
esas causas y encuentra la profundidad a la que el modelo **aplica** un programa de
forma fiable.

## 2. Diseño

**Tareas.** Programas de 2 a 6 operaciones sobre las seis operaciones del dominio
(`sort_asc`, `sort_desc`, `double`, `negate`, `add_one`, `reverse`). 12 tareas por
profundidad, con dos ejemplos de soporte.

**Complejidad funcional.** Para cada tarea se enumera el espacio de programas más
cortos y se calcula la **longitud mínima equivalente** sobre 60 sondas. La dificultad
se reporta por esa longitud, no por la longitud nominal. Una tarea de 5 operaciones
que colapsa a 2 se analiza como 2.

**Condiciones:**

| Condición | Qué recibe | Qué mide |
|---|---|---|
| `symbolic` | Programa completo en notación `a -> b -> ...` | Aplicación con la representación mínima |
| `nl` | El mismo programa en español natural | Si el lenguaje natural ayuda o estorba |
| `steps` | Programa + devolver la lista tras cada operación | Seguimiento del estado intermedio |
| `interpreter` | Ejecución determinista en Python | Control de corrección de la tarea (12/12 por construcción) |

**Profundidades:** 2, 3, 4 y 5 operaciones (sufijos 0–3). 12 tareas × 4 profundidades
× 2 condiciones de LLM (`symbolic`, `steps`) = 96 llamadas. `nl` se añade en la
profundidad donde `symbolic` cruce el 50 % (12 llamadas más).

## 3. Métricas

- Acierto exacto por profundidad y por longitud mínima equivalente.
- Acierto del primer paso, del segundo, etc., en `steps`.
- Taxonomía del primer error: operación equivocada, orden equivocado, valor
  equivocado, elemento extra o faltante, formato inválido.
- Tokens y segundos por condición.
- `interpreter` = 12/12; si no, el generador de tareas está mal.

## 4. Criterios de decisión

| Observación | Lectura |
|---|---|
| `symbolic` ≥ 10/12 en profundidad 2 y cae con la profundidad | Hay un régimen aplicable; usarlo para MEM-002 |
| `steps` > `symbolic` en la profundidad de cruce | El fallo es de estado intermedio, no de operaciones |
| `steps` ≈ `symbolic` | El fallo está en la operación o en la interpretación |
| Ninguna profundidad ≥ 10/12 | `luna` low no aplica ni dos operaciones; cambiar de tarea o de modelo |
| `interpreter` < 12/12 | El generador o el evaluador están mal; no se interpreta nada |

## 5. Claims pre-registradas

| ID | Afirmación | Falsador |
|---|---|---|
| E1 | `symbolic` acierta ≥ 10/12 en profundidad 2 | < 10/12 |
| E2 | El acierto de `symbolic` decrece al aumentar la profundidad | Acierto igual o mayor en profundidad 5 que en 2 |
| E3 | `steps` mejora a `symbolic` en la profundidad donde `symbolic` está entre 40 % y 60 % | `steps` ≤ `symbolic` |
| E4 | La longitud mínima equivalente predice el acierto mejor que la longitud nominal | La nominal predice mejor |
| E5 | El intérprete determinista acierta 12/12 en todas las profundidades | < 12/12 |

## 6. Límites

- Un modelo, una semilla, 12 tareas por profundidad.
- La longitud mínima se calcula sobre 60 sondas, no es una prueba formal de
  equivalencia.
- La traducción a lenguaje natural es una de varias posibles.
- El prompt de `steps` cambia la tarea y el número de tokens; la comparación es
  informativa, no perfectamente controlada.
- Las tareas empiezan por el motivo del 007; para ejecución es irrelevante, pero se
  reporta.
