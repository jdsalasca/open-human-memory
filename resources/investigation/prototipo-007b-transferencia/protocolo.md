# 007B — ¿Información, instrucción o reutilización?

**Fecha:** 16 de noviembre de 2026
**Estado:** protocolo corregido tras fallo de adquisición; corrida diagnóstica en curso.
**Modelo:** `gpt-6-luna`, `reasoning_effort = low`.
**Código:** `src/ohmem/v7_transfer.py` (condiciones `history` y `oracle`).
**Datos:** `results/luna-low-support2-history-oracle.json`, combinados con
`../prototipo-007-transferencia/results/luna-low-support2-12ex.json`.

## 1. Por qué

El 007 con `luna` low tocó el suelo: con 2 ejemplos de soporte, clon 1/12, memoria
3/12, placebo 6/12. Un diagnóstico mostró que **la respuesta de la consulta está
determinada por los 2 ejemplos** en las 12 tareas, aunque queden 10–320 programas
consistentes. El clon no falla por ambigüedad: falla por **búsqueda**.

El diseño original del 007B cubría 4 de 5 pasos con el artefacto. **La adquisición
falló:** `luna` low no reprodujo ningún motivo de 3 o 4 operaciones desde 12 ni 24
ejemplos (cuatro llamadas, todas rechazadas por la verificación). El 007B de 4/5
queda bloqueado en adquisición, no en transferencia.

La corrida diagnóstica usa el motivo de 2 operaciones que `luna` **sí** adquiere y
añade dos condiciones a las tres existentes, sobre las mismas 12 tareas:

- contra el clon: ¿se usa el artefacto?
- contra el placebo: ¿importa el contenido?
- contra el **historial de origen**: ¿importa que sea un programa verificado y no
  las experiencias crudas?
- contra el **programa completo**: ¿el modelo puede ejecutar la tarea cuando la
  conoce? (fuga deliberada; control de ejecución)

## 2. Diseño

**Motivo (2 operaciones):** `sort_asc → double`. Sesión 1 con 12 pares y
«exactamente 2 operaciones»; verificación con 60 sondas.

**Sesión 2.** 12 tareas de **5 pasos**: el motivo más tres operaciones aleatorias.
Dos ejemplos de soporte. Cinco condiciones pareadas:

| Condición | Qué recibe |
|---|---|
| `clone` | Solo la tarea y la instrucción de verificar |
| `memory` | El programa verificado de 2 operaciones |
| `placebo` | Un programa falso de 2 operaciones (`sort_desc → double`) |
| `history` | Los 12 pares de la sesión 1 (experiencias de origen) |
| `oracle` | El programa completo de 5 operaciones (**fuga; control de ejecución**) |

Las condiciones `clone`, `memory` y `placebo` ya están medidas en
`luna-low-support2-12ex.json` (semilla 0, 12 tareas, soporte 2). Esta corrida añade
`history` y `oracle` con la misma semilla, tareas y soporte. Las filas se combinan
por índice de tarea.

## 3. Métricas

- Acierto exacto por condición y por tarea.
- Pares discordantes: memoria vs clon, placebo e historial; historial vs clon;
  oráculo vs clon.
- Caracteres del prompt por condición (proxy de coste).
- Llamadas: 1 de adquisición + 24 nuevas (12 historial + 12 oráculo).

## 4. Criterios de decisión

| Observación | Lectura |
|---|---|
| `oracle` < 10/12 | La aplicación del programa es el cuello; no se identifica si es ejecución, interpretación o seguimiento de instrucciones. |
| `memory` ≤ `clone` | No hay evidencia de uso del artefacto. |
| `memory` ≤ `history` | El artefacto no aporta sobre las experiencias crudas; a lo sumo comprime. |
| `memory` ≤ `placebo` | No hay efecto de contenido. |
| `memory` > `clone`, `> placebo` y `> history` | Primera evidencia local de reutilización verificada; replicar con más tareas. |

## 5. Límites

- Una semilla, 12 tareas, un modelo. Los conteos no permiten significación.
- **Sesgo de construcción:** las tareas empiezan por el motivo. Es reutilización
  favorable, no transferencia a una familia independiente.
- El historial tiene más tokens que el artefacto; la comparación de acierto iguala
  información, no longitud.
- `oracle` es una fuga deliberada y se etiqueta como tal; no es una condición de
  memoria.
- La adquisición de motivos de 3–4 operaciones se intentó con 12 y 24 ejemplos y
  «exactamente N operaciones»; no se relajó la verificación.

## Apéndice. Adquisición fallida (4 llamadas)

| Motivo | Ejemplos | Programa devuelto | ¿Verifica? |
|---|---|---|---|
| `sort_asc → double → add_one → negate` | 12 | `negate → double → reverse → add_one` | No |
| `sort_asc → double → add_one → negate` | 24 | `negate → double → add_one → sort_desc` | No |
| `double → add_one → negate` | 12 | `negate → double → add_one` | No |
| `double → add_one → negate` | 24 | `double → negate → add_one` | No |

Los cuatro motivos son identificables: la enumeración exhaustiva deja 1–4 programas
consistentes, todos conductualmente equivalentes. El fallo es de **búsqueda**, no de
información.
