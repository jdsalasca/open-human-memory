# MEM-006 — Múltiples habilidades, recuperación autónoma y coste total

**Fecha:** 17 de noviembre de 2026
**Estado:** protocolo pre-registrado; **no ejecutado**. El hash del protocolo se
commitea antes de la corrida.
**Modelo:** `gpt-6-luna`, `reasoning_effort = low`.
**Código:** por implementar sobre `src/ohmem/`.
**Datos:** `results/` (se publicarán en un commit separado).

## 1. Pregunta

Después de aprender **varias habilidades** en episodios separados y reiniciar el
contexto, ¿puede el agente **seleccionar autónomamente** la habilidad pertinente entre
varias, aplicarla, rechazar las inaplicables u obsoletas y hacerlo a un coste total
menor que un solucionador simbólico sin memoria?

Esta es la pregunta que MEM-002/003/004/005 no responden: allí el evaluador entregaba
el artefacto y una sola transformación.

## 2. Diseño

**Biblioteca:** 8 habilidades de 2 operaciones, distintas y parcialmente solapadas:

| ID | Procedimiento | Comparte |
|---|---|---|
| `s1` | `sort_asc → double` | sort, double |
| `s2` | `reverse → add_one` | reverse, add_one |
| `s3` | `sort_desc → negate` | sort, negate |
| `s4` | `double → add_one` | double, add_one |
| `s5` | `reverse → double` | reverse, double |
| `s6` | `sort_asc → negate` | sort, negate |
| `s7` | `sort_desc → add_one` | sort, add_one |
| `s8` | `sort_desc → double` | sort, double |

Cada habilidad se aprende en una sesión 1 con 12 ejemplos y se verifica con 60 sondas.
Los fallos de adquisición se registran; no se relaja la verificación.

**Metadatos por habilidad** (ver `docs/esquema-de-memoria.md`): `skill_id`,
`procedure`, `verification {status, method, tested_scope}`, `applicability
{requires, invalid_when}`, `provenance {source, evidence_count}`, `decision`.

**Prueba:** reinicio, 16 tareas (2 por habilidad), 2 ejemplos de soporte. El evaluador
**no dice qué habilidad usar**.

**Condiciones:**

| Condición | Qué recibe |
|---|---|
| `clone` | Sin biblioteca |
| `oracle_skill` | La habilidad correcta, identificada por el evaluador |
| `retrieval` | La biblioteca completa; el modelo elige |
| `random_skill` | Una habilidad incorrecta al azar |
| `symbolic_solver` | Enumeración de los 36 programas de 2 operaciones sobre los 2 ejemplos; sin LLM |
| `expert_written` | La misma biblioteca, atribuida a un experto, sin adquisición |

`expert_written` usa **las mismas cadenas de operaciones** que `retrieval` para no
confundir procedencia con orden.

**Obsolescencia:** 4 tareas adicionales donde la habilidad fue correcta en adquisición
pero la regla cambia en la prueba (p. ej., una postcondición invalida el resultado).
El agente debe rechazarla o marcarla para revisión.

## 3. Métricas

- Acierto final.
- **Acierto de recuperación:** ¿eligió la habilidad correcta? (elección forzada entre
  8; azar 12,5 %).
- **Rechazo:** ¿rechazó la habilidad inaplicable u obsoleta?
- **Coste:** tokens y llamadas de adquisición, verificación, recuperación y uso.
- **Beneficio neto:** `N·(C_sin − C_con) − C_adq − C_ver − C_mant`, con `N` usos.
- **Punto de equilibrio:** número de usos para el que el beneficio neto es cero.

## 4. Claims pre-registradas

| ID | Afirmación | Falsador |
|---|---|---|
| R1 | La recuperación elige la habilidad correcta en ≥ 70 % de las 16 tareas | < 70 % |
| R2 | La recuperación supera al clon y a la habilidad aleatoria en ≥ 3 pares | < 3 pares |
| R3 | La recuperación no supera a `oracle_skill` (control de fuga) | > `oracle_skill` |
| R4 | El solucionador simbólico acierta ≥ 90 % en las tareas de 2 operaciones | < 90 % |
| R5 | La recuperación y `expert_written` no difieren en más de 2 pares | > 2 pares |
| R6 | El sistema rechaza ≥ 3 de las 4 habilidades obsoletas | < 3 |

## 5. Criterios de decisión

| Observación | Lectura |
|---|---|
| Recuperación ≥ 70 % y > clon/aleatorio | Hay selección autónoma; no solo ejecución |
| Recuperación ≈ `oracle_skill` | La selección no pierde información |
| Recuperación ≈ `expert_written` | La adquisición no añade; el contenido manda |
| Simbólico ≥ 90 % y memoria ≈ simbólico | La memoria debe justificarse por coste o por tareas fuera del presupuesto |
| Rechazo ≥ 3/4 | Hay aplicación condicionada, no obediencia |
| Beneficio neto negativo en todos los `N` plausibles | Aprender no se amortiza en este dominio |

## 6. Pre-registro y transparencia

1. Este protocolo, el código y los tests se commitean **antes** de la corrida.
2. Se publica el SHA-256 del protocolo (`protocolo.sha256`).
3. La corrida se ejecuta después; los resultados se publican en un commit separado.
4. El protocolo no se edita después de la corrida; las correcciones van en una errata.
5. MEM-005 no cumple este flujo (protocolo, código, resultados y análisis en el mismo
   commit); se marca como **exploratorio**, no confirmatorio.

## 7. Límites

- 8 habilidades, 16 tareas, un modelo; no es un benchmark.
- Las habilidades son de 2 operaciones, el régimen aplicable de EXEC-001.
- El solucionador simbólico es un competidor fuerte y barato; si resuelve todo, la
  memoria debe justificarse por coste o por tareas donde la búsqueda no quepa.
- Los metadatos pueden filtrar la respuesta; el retrieval debe basarse en los ejemplos
  observables, no en el nombre de la habilidad.
- La obsolescencia es sintética y controlada; no cubre deriva real.
- El coste se mide en tokens/llamadas, no en dinero.
