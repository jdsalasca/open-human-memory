# MEM-002 — Memoria en el régimen aplicable (piloto)

**Fecha:** 16 de noviembre de 2026
**Estado:** protocolo pre-registrado; piloto en curso.
**Modelo:** `gpt-6-luna`, `reasoning_effort = low`.
**Código:** `src/ohmem/v7_transfer.py`.
**Datos:** `results/pilot-depth3.json`.

## 1. Por qué

EXEC-001 mostró que `luna` aplica 2 operaciones al 86 %, 3 al 44–58 % y 5 al 0–33 %.
El 007 usó 5 pasos y midió el suelo: memoria 3/12, placebo 6/12, clon 1/12. **La
tarea estaba fuera del régimen de aplicación.** MEM-002 baja a **3 operaciones**
—el motivo aprendido de 2 más una operación aleatoria— donde el oráculo aún acierta
7/12 y la memoria puede tener margen.

## 2. Diseño

**Sesión 1:** 12 pares del motivo `sort_asc → double`; verificación con 60 sondas.

**Sesión 2:** 12 tareas de **3 operaciones** (motivo + 1 operación aleatoria), 2
ejemplos de soporte. Condiciones pareadas:

| Condición | Qué recibe |
|---|---|
| `clone` | Solo la tarea |
| `memory` | El motivo verificado de 2 operaciones |
| `placebo` | Un motivo falso de 2 operaciones (`sort_desc → double`) |
| `history` | Los 12 pares de la sesión 1 |
| `oracle` | El programa completo de 3 operaciones (fuga; control de ejecución) |

## 3. Métricas

- Acierto exacto por condición y pares discordantes vs clon, placebo e historial.
- Coste en llamadas; caracteres del prompt.
- `oracle` como techo de aplicación.

## 4. Criterios de decisión

| Observación | Lectura |
|---|---|
| `oracle` < 7/12 | La tarea sigue fuera del régimen; no se interpreta la memoria |
| `memory` < `clone` + 3 pares | No hay evidencia de uso |
| `memory` ≤ `history` | El artefacto no aporta sobre las experiencias crudas |
| `memory` ≤ `placebo` | No hay efecto de contenido |
| `memory` > clon, placebo e historial por ≥ 3 pares | Primera señal local; replicar con 24 tareas y placebos por clase |

## 5. Claims pre-registradas

| ID | Afirmación | Falsador |
|---|---|---|
| M1 | La memoria supera al clon en ≥ 3 pares | < 3 pares |
| M2 | La memoria supera al placebo en ≥ 3 pares | ≤ 0 pares o placebo superior |
| M3 | La memoria supera al historial en ≥ 3 pares | < 3 pares |
| M4 | El oráculo acierta ≥ 7/12 | < 7/12 |

## 6. Límites

- Piloto: una semilla, 12 tareas, un modelo. No es confirmatorio.
- Las tareas empiezan por el motivo; es reutilización favorable.
- El historial tiene más tokens que el artefacto; no se iguala longitud.
- El placebo comparte `double` con el motivo; es parcialmente pertinente. Las clases
  de placebo (irrelevante, parcial, plausible, equivalente) quedan para la réplica.
- El oráculo es una fuga deliberada.
