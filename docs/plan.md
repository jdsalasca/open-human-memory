# Plan de investigación

**Fecha:** 16 de noviembre de 2026
**Cambio de régimen:** este plan sustituye la secuencia anterior de rondas
(R1–R6), que producía un prototipo por auditoría. El patrón era circular: cada
auditoría encontraba un fallo, se construía otro prototipo para responderla, y la
siguiente auditoría encontraba otro fallo. Seis prototipos no produjeron una teoría;
produjeron correcciones.

**Regla nueva:** ninguna ronda empieza con código. Empieza con una deuda de base
cerrada: teoría, registro de afirmaciones, antecedente o reproducción.

---

## Principios

1. **Una afirmación entra en `docs/registro-de-afirmaciones.md` antes del
   experimento**, con su falsador.
2. **Ningún prototipo nuevo sin una predicción derivada de `docs/teoria.md`.**
3. **Ninguna comparación sin clon** (mismo modelo, herramientas y presupuesto).
4. **Ninguna condición con información privilegiada sin etiqueta `ORACLE-*`.**
5. **Ninguna muestra sin estratificar por clase conductual.**
6. **Ningún resultado sin coste total** (`E`, `K`, `P` separados).
7. **Ningún competidor citado como si lo hubiéramos reproducido.**

---

## F0 — Bases (en curso, bloqueante)

**Objetivo:** que el proyecto tenga una teoría, un registro y un mapa de
antecedentes antes de medir otra cosa.

| Entregable | Estado |
|---|---|
| `docs/teoria.md` con canales, rivales, predicciones P1–P5 | Hecho |
| `docs/registro-de-afirmaciones.md` con estados y niveles | Hecho |
| `precedentes/10-matriz-de-antecedentes.md` | Hecho |
| `docs/problema-central.md` con las siete capacidades | Hecho |
| Revisión estructurada: 7.100 identificados, 177 cribados, 31 incluidos | **Hecho**, con límites declarados (`revision-sistematica/`) |
| Una línea base reproducida (SkillGen, Proof-Gated, CEGIS o retrieval) | **Pendiente** |

**Puerta F0:** falta la reproducción. Sin ella no se pasa a F1. Si no se puede
reproducir ninguna línea base, se documenta por qué y se reduce el alcance.

**Candidatos de reproducción, por coste:** CEGIS mínimo (bajo), SkillGen (medio),
Proof-Gated (medio), EvoAgentBench (alto), DreamCoder (alto).

---

## F1 — Descomposición de capacidades (`DECOMP-*`)

**Pregunta:** ¿de qué capacidad viene el fallo del agente?

- Siete capacidades separadas (inferencia, desambiguación, experimentación,
  ejecución, verificación, memoria, generalización).
- Muestra **estratificada por clase conductual**, no por fila.
- Herramientas con las **cinco etapas verificadas** por tarea.
- Sin memoria todavía.

**Criterio:** identificar al menos una capacidad con efecto distinguishable y un
intervalo que excluya cero. Si ninguna lo hace, se revisa el instrumento.

**Puerta F1:** sin esta descomposición no se ejecuta F2. Cualquier resultado de
memoria sería ambiguo.

---

## F2 — Recuperación genuina (`RETRIEVAL-*`)

**Pregunta:** ¿un recuerdo elegido **sin conocer la respuesta** cambia la decisión?

| Condición | Qué es |
|---|---|
| `CLONE` | Sin historial |
| `ACTUAL-RETRIEVAL` | Recuperador que solo ve la observación actual |
| `ORACLE-MEMORY` | Techo de información, etiquetado como oráculo |
| `FULL-HISTORY` | Historial completo en contexto |
| `PROCEDURE` | Procedimiento verificado |

**Métricas:** `E`, `K`, `P` separadas. Comparación pareada por tarea.

**Criterio:** `ACTUAL-RETRIEVAL` supera al clon con IC que excluye cero. Si el
oráculo gana y la recuperación no, el fallo es del recuperador.

---

## F3 — Universo no enumerable (`EXPAND-*`)

**Pregunta:** ¿una herramienta compilada amplía la cobertura cuando la solución no
cabe en el presupuesto? Es la predicción **P1** de `docs/teoria.md`.

- `|O| ≥ 6`, profundidad ≥ 6, presupuesto que enumere < 1 % del espacio.
- Misma tarea, mismo presupuesto, con y sin herramientas compiladas.
- Comparación contra búsqueda profunda y contra clon.

**Criterio:** la cobertura sube con historial y no sube sin él. Si no, la línea de
expansión se cierra.

---

## F4 — Currículo interdependiente (`META-*`)

**Pregunta:** ¿baja `E(F)` en familias reservadas? Predicción **P3**.

- Familias con estructura compartida y superficie distinta (listas → cadenas →
  registros con clave).
- Dependencia real: una tarea posterior exige un artefacto obtenido antes.
- Familias reservadas que no intervienen en el diseño.

**Criterio:** `E(F)` del agente < `E(F)` del clon, con IC que excluya cero. Si no,
no hay metaprendizaje y el programa se reduce a herramientas.

---

## F5 — Deriva y portabilidad (`DRIFT-*`)

**Pregunta:** ¿sobrevive el conocimiento a un cambio de reglas y a un cambio de
modelo? Predicción **P5**.

- Cambio de semántica a mitad de currículo.
- Cambio de modelo subyacente.
- Retirada de artefactos obsoletos sin perder los válidos.

**Criterio:** el agente detecta la obsolescencia y no arrastra el error. Si el
efecto desaparece al cambiar de modelo, CUMULUS no tiene objeto.

---

## Lo que no se hace

- No se añaden acciones al controlador.
- No se construyen SIR, Canon ni JANUS-C.
- No se escribe otra capa social.
- No se ejecuta el 007 antes de F1.

---

## Rondas históricas (cerradas)

| Ronda | Qué produjo | Lección |
|---|---|---|
| R1 | Corpus interdisciplinar (01–14) | Vocabulario y analogías, no hipótesis comprobables |
| R1.5 | Diagnóstico 002 | El solucionador, no la memoria |
| R2 | Diseño CUMULUS/JANUS | Sin semántica ejecutable |
| R2.5 | 004-A | Las macros no amplían cobertura en espacio enumerable |
| R2.6 | 005 | El valor es condicional a la continuidad |
| R2.7 | 006 | La política no paga su instrumento |
| R2.8 | Errata 006-B | Tres inferencias invalidadas |

Se conservan como registro. No se reabren.
