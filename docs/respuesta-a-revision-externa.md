# Respuesta a la revisión externa

**Revisor:** `gpt-6.1-terra`, `reasoning_effort = medium`, `codex-cli 0.169.0`,
sandbox `read-only`, 16 de noviembre de 2026.
**Informe:** [`../resources/investigation/revision-externa/codex-gpt-6.1-terra-medium.md`](../resources/investigation/revision-externa/codex-gpt-6.1-terra-medium.md)
**Dictamen recibido:** rechazar en su estado actual.
**Respuesta:** aceptado. Se corrigió lo corregible y se declaró lo que falta.

---

## 1. Errores factuales

| # | Hallazgo | Acción |
|---|---|---|
| 1 | «Cuesta 1,9× más que buscar» era falso: 84,3/59,5 = **1,42×**; el 1,89 es contra macros primero | Corregido en README, 006-A, protocolos y manuscrito |
| 2 | F12 decía que todas las cifras estaban verificadas; solo tres lo están | F12 reescrita; F13 añadida («ninguna replicada») |
| 3 | «96 episodios no caben en una ventana» seguía en el 005 | Retirada en el punto donde aparecía |
| 4 | «El agente no identifica el programa» reaparecía en 006-B | Reformulado: salida incorrecta, causa no identificada |
| 5 | SkillsBench mezclaba versiones | Tabla separa arXiv (86/11/+16,2) y v1.1 (87/8/+16,6) |
| 6 | JANUS presentaba la ignorabilidad como chequeo automático y decía «cinco niveles» con seis filas | Reescrito: seis condiciones, ignorabilidad como **supuesto**, propensión acotada |
| 7 | «Verificación imprescindible» por «el estudio reporta discrepancias» | Reformulado en la revisión |

## 2. P0 — Imprescindible

| # | Hallazgo | Acción |
|---|---|---|
| 1 | Elegir una contribución única | Manuscrito reencuadrado como **artículo metodológico**; el aprendizaje acumulativo queda como pregunta abierta |
| 2 | Contradicciones y cifras | Corregidas (tabla anterior) |
| 3 | La teoría exigía ambigüedad **y** espacio no explorable | Corolario 3 corregido: basta que la solución caiga fuera del presupuesto; la ambigüedad es un problema adicional. Añadidos supuestos de realizabilidad |
| 4 | Presupuesto no estricto y probe no descontado | Medido: exceso máximo 6 pasos, media ≤0,83, ≤4/24 tareas. Declarado que la comparación es de **coste ex post** |
| 5 | Falta recuperación genuina | **No ejecutada.** `ORACLE-MEMORY` etiquetado; `ACTUAL-RETRIEVAL` queda como el experimento que falta |
| 6 | Faltan familias reservadas y repeticiones | **No ejecutado.** Declarado como límite y como F1/F2 del plan |

## 3. P1 — Necesario

| # | Hallazgo | Acción |
|---|---|---|
| 1 | Reproducir una línea base externa | Pendiente; bloquea F0 del plan |
| 2 | Costes separados | `E`/`K`/`P` definidos; solo se mide `steps`. Declarado |
| 3 | Registros de búsqueda incompletos | Hueco de 88 declarado; respuestas crudas de OpenAlex no archivadas. Declarado |
| 4 | Análisis por clase conductual | Pendiente; declarado |
| 5 | JANUS: supuestos vs comprobaciones | Reescrito §4.4 |

## 4. P2 — Claridad

| # | Hallazgo | Acción |
|---|---|---|
| 1 | Falta una tabla única | Añadida **Tabla 1** al manuscrito |
| 2 | Avisos junto a cada afirmación retirada | Corregidos 005 y 006-B |
| 3 | Scripts de auditoría | Añadido `budget_audit.py`; los demás, pendientes |

## 5. Lo que no se corrige, y por qué

- **Las 209 llamadas al LLM no se repiten.** El baseline es `gpt-6-luna` low y se
  declara; repetirlo con `gpt-6.1-terra` medium es trabajo futuro, no una
  corrección documental.
- **No se reproduce ningún competidor.** Es la deuda F0 y no se puede simular con
  texto.
- **No se añaden familias reservadas.** Requiere un experimento nuevo.
- **El bootstrap no se rehace por clases.** Con dos semillas no hay unidad de
  agrupación suficiente; se declara optimista y no se usa para equivalencia.

## 6. Cambios de estado en el registro

| Afirmación | Antes | Ahora |
|---|---|---|
| P2 (política vs regla) | «Refutada» | «En estas dos semillas, −1,0 pp; no establece equivalencia» |
| P3 (probe aporta) | «Sostenida» | «En esta muestra; falta ablación del probe» |
| T1 (cobertura) | «Sostenida» | «Sostenida **con condiciones** de realizabilidad» |
| F12 | «Verificada» | «Solo tres filas» |

## 7. Dictamen propio

Con estas correcciones el trabajo **sigue sin demostrar aprendizaje acumulativo**.
Lo que cambia es que ahora **no afirma lo contrario** y deja medido el instrumento.
Un revisor humano puede rechazarlo por falta de evidencia principal —es lo que hizo
el revisor automático— sin que eso obligue a retirar los resultados negativos, que
son locales y verificables.

La respuesta a la pregunta del proyecto sigue siendo: **no lo sabemos, y ahora
sabemos mejor por qué**.
