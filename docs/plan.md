# Plan de investigación

**Fecha:** 16 de noviembre de 2026
**Cambio de régimen:** este plan sustituye la secuencia R1–R6, que producía un
prototipo por auditoría. El patrón era circular: auditoría → fallo → prototipo →
auditoría. Los seis prototipos negativos produjeron correcciones; el 007/MEM produjo
el primer resultado positivo condicionado.

**Regla nueva:** ninguna ronda empieza con código. Empieza con una deuda de base
cerrada: teoría, registro, antecedente o reproducción.

---

## La pregunta

> Si mañana este agente reinicia su contexto, cambia de tarea y encuentra un
> problema que nunca ha visto, ¿qué aprendizaje adquirido en sus experiencias
> anteriores modifica realmente su manera de comprenderlo y resolverlo?

Todo lo que no acerque una respuesta verificable a esta pregunta es instrumento,
no objetivo.

---

## Las cinco preguntas que cada ronda debe responder

**A. ¿Qué competencia adquirida medimos?**
La reducción de `E(A,F)` —experiencias hasta el umbral— o el aumento de `P(A,F)` a
igual `K(A,F)`, contra un clon sin historial. Tres métricas separadas; no se
agregan hasta que un escenario fije precios.

**B. ¿Qué mecanismo la produce y qué antecedente ya la explica?**
Compilar experiencias en artefactos verificados y conservar solo los que reducen el
coste futuro. DreamCoder, Stitch, LILO, CEGIS, LPA*, MAML y Proof-Gated ya cubren
partes. Ninguna pieza es nueva; la contribución posible es la medición.

**C. ¿Qué comparación podría demostrar que no hay ventaja?**
Clon sin historial, historial completo con recuperador convencional y una regla
simple. Las tres deben estar implementadas antes de declarar nada. Dos ya
refutaron dos de nuestras hipótesis.

**D. ¿Qué relación tiene con miles de tareas y con el contexto?**
Hoy, ninguna demostrada. No medimos tokens. La hipótesis es que un artefacto
acotado conserva competencia con menos contexto que el historial bruto; exige medir
tokens, almacenamiento y mantenimiento reales.

**E. ¿Qué abandonamos si sale negativo?**
La afirmación de expansión por macros. CUMULUS queda como hipótesis de
representación y JANUS como diseño de confianza, ambos sin validación. No se
sustituyen por otra arquitectura: se publica y se reduce el alcance.

---

## Principios

1. Toda afirmación entra en `registro-de-afirmaciones.md` **antes** del experimento.
2. Ningún prototipo sin una predicción derivada de `teoria.md`.
3. Ninguna comparación sin clon (mismo modelo, herramientas y presupuesto).
4. Ninguna condición con información privilegiada sin etiqueta `ORACLE-*`.
5. Ninguna muestra sin estratificar por clase conductual.
6. Ningún resultado sin coste total (`E`, `K`, `P` separados).
7. Ningún competidor citado como si lo hubiéramos reproducido.
8. Una sola base de evidencia por afirmación; el resto son registros históricos.

---

## Estado de las rondas (16 de noviembre de 2026)

| Ronda | Estado | Qué falta |
|---|---|---|
| **F0** bases y baseline externo | **Bloqueante, no ejecutado** | Reproducir un competidor |
| **F0.5** retención y transferencia | **Ejecutado; positivo condicionado** | Réplica de 24 tareas y varias semillas (M11/M12) |
| **F1** descomposición de capacidades | **Parcial**: ejecución medida (EXEC-001); inferencia parcial | Desambiguación, experimentación, verificación y generalización |
| **F2** recuperación genuina | **Pre-registrada (MEM-006), no ejecutada** | Implementar y correr 8 habilidades, retrieval, simbólico y experto |
| **F2.5** forma del conocimiento | **Parcial**: LIRE-002 mide coste/fidelidad, no forma | Factorial idioma × longitud × estructura; LLMLingua-2 |
| **MEM-006** múltiples habilidades y recuperación | **Ejecutado; negativo** | En 2 ops, simbólico 10/10; retrieval 7/10 (selección 5/10); clon 8/10; no se amortiza |
| **F3** universo no explorable | No ejecutado | Tarea identificable pero fuera del presupuesto |
| **F4** currículo interdependiente | No ejecutado | — |
| **F5** deriva y portabilidad | No ejecutado | — |

---

## F0 — Bases (en curso, bloqueante)

| Entregable | Estado |
|---|---|
| `teoria.md` con canales, rivales y P1–P5 | Hecho |
| `registro-de-afirmaciones.md` | Hecho |
| Revisión estructurada: 7.100 identificados, 177 cribados, 31 incluidos | Hecho, con límites declarados |
| Una línea base reproducida | **Pendiente** |

**Puerta F0:** la falta de reproducción **no bloquea la instrumentación**, pero sí
bloquea **declarar ventajas**. Se puede construir el diagnóstico en paralelo; no se
publica una comparación hasta tener baseline.

**Fidelidad exigida:** no basta «mismo orden de magnitud». Se comparan protocolo,
configuración, métricas y variabilidad del estudio original. Un 30 % frente a un
80 % no es una reproducción.

**Candidatos, por coste:** CEGIS mínimo (bajo), SkillGen (medio), Proof-Gated
(medio), EvoAgentBench (alto), DreamCoder (alto). El referente principal debería ser
un sistema de **transferencia de habilidades** con código y datos, no el más fácil
de reproducir.

**F0.5 — Retención y transferencia (007, ejecutado).** Sesión 1 aprende un
procedimiento verificado; reinicio; sesión 2 lo aplica a composiciones de cinco
pasos. Con `gpt-6-luna` low: 6 ejemplos no verifican (aborta); 12 ejemplos sí. Con 1
ejemplo de soporte, clon 0/12, memoria 0/12, placebo 2/12 (suelo); con 2, clon 1/12,
memoria 3/12, placebo 6/12. **El artefacto verificado no supera al placebo: no hay
ventaja atribuible al contenido.** La familia no tiene margen para `luna` low (suelo)
ni para `terra` (techo). Siguiente: **007B** con un dominio donde el clon falle y el
artefacto sea necesario (vocabulario opaco, horizonte 20+).

**007B (diagnóstico, ejecutado).** Se intentó un motivo de 3–4 operaciones para
cubrir 4 de 5 pasos: `luna` low no lo adquiere (cuatro intentos con 12 y 24
ejemplos; todos rechazados por la verificación). La corrida diagnóstica usó el motivo
de 2 operaciones y añadió `history` (los 12 pares de origen) y `oracle` (el programa
completo) a las 12 tareas del soporte 2. Resultado: clon 1/12, memoria 3/12, placebo
6/12, historial 4/12, **oráculo 2/12**. Con el programa completo el modelo apenas
resuelve 2 de 12: **el cuello está en la aplicación del programa, no en la memoria**;
el mecanismo exacto queda abierto.

**EXEC-001 (ejecutado).** Con el programa completo: 2 operaciones 11/12, 3
operaciones 7/12, 4 operaciones 8/12, 5 operaciones 4/12. Por longitud mínima
equivalente: 2 ops 18/21, 3 ops 8/18, 4 ops 4/8, 5 ops 0/1. La profundidad nominal no
es monótona. El siguiente paso es **MEM-002** con procedimientos de 2–3 operaciones
efectivas, donde el clon aplica pero no identifica; la familia de 5 pasos queda
cerrada para memoria.

**MEM-003 (ejecutado, positivo).** En 2 operaciones, el mismo programa verificado:
candidata 4/12, verificada 11/12, placebo 3/12, historial 10/12, oráculo 12/12. El
encuadre era el cuello (7 pares, p = 0,016); el contenido importa (8 pares vs
placebo, p = 0,008).

**MEM-004 (ejecutado, control superado).** El programa falso etiquetado «verificado»
acierta 0/12; la memoria verificada, 10/12 (10 pares, p = 0,002). La etiqueta no
basta; la verificación debe ser real, fuera del prompt. **Siguiente:** réplica de 24
tareas (M11/M12), varias semillas; después MEM-005 en 3 operaciones con encuadre
definitivo y, más adelante, el ciclo longitudinal `E`/`K`/`P`.

---

## F1 — Descomposición de capacidades (`DECOMP-*`)

**Pregunta:** ¿de qué capacidad viene el fallo?

- Siete capacidades separadas (teoría §4).
- Muestra estratificada por clase conductual.
- Herramientas con las cinco etapas verificadas por tarea.
- Sin memoria todavía.

**Criterio:** al menos una capacidad con efecto distinguishable e IC que excluya
cero. Si ninguna, se revisa el instrumento.

**Puerta:** sin F1 no se ejecuta F2.

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

**Criterio:** `ACTUAL-RETRIEVAL` supera al clon con IC que excluye cero. Si el
oráculo gana y la recuperación no, el fallo es del recuperador.

---

## F2.5 — Forma del conocimiento (`FORM-*`)

**Pregunta:** ¿importa la **forma** en que se conserva una experiencia? Predicción
P6. Es la hipótesis nueva del programa.

- Cuatro formas de la misma experiencia: **episodio, procedimiento, herramienta,
  concepto**.
- Misma información disponible para el clon; mismo presupuesto de contexto y
  cómputo.
- Cota superior: oráculo que conoce la forma óptima por tarea.
- Métricas `E`, `K` y `P` separadas; coste de construir cada forma incluido.

**Criterio:** la selección aprendida se acerca al oráculo y supera a toda forma fija
a igual coste. Si una forma fija iguala o supera, **ese resultado no respalda la
ventaja del selector evaluado**; las formas todavía podrían diferir entre tareas, y
el selector podría ser deficiente o demasiado caro.

**LIRE-001 (piloto ejecutado, negativo).** La misma regla de cuatro ramas en cinco
representaciones (español, inglés, chino, español conciso, DSL), con tokens reales
del modelo. Las prosas 8/8; el DSL 7/8. El chino usó 64 % menos caracteres y +2
tokens de mediana. **No se demostró ahorro de tokens** y el DSL perdió fidelidad.
Ver `../resources/investigation/lire-001/`.

---

## F3 — Universo no explorable (`EXPAND-*`)

**Pregunta:** ¿una herramienta compilada amplía la cobertura cuando la solución no
cabe en el presupuesto? Predicción **P1**.

- `|O| ≥ 6`, profundidad ≥ 6, presupuesto que enumere < 1 % del espacio.
- Misma tarea, mismo presupuesto, con y sin herramientas compiladas.
- Contra búsqueda profunda y contra clon.

**Criterio:** la cobertura sube con historial y no sin él. Si no, se cierra la línea
de expansión.

---

## F4 — Currículo interdependiente (`META-*`)

**Pregunta:** ¿baja `E(F)` en familias reservadas? Predicción **P3**.

- Estructura compartida, superficie distinta (listas → cadenas → registros).
- Dependencia real: una tarea posterior exige un artefacto anterior.
- Familias reservadas que no intervienen en el diseño.
- **Canales competidores:** herramienta, política y **representación**. No se
  declara ganador antes de medir; la representación vuelve a ser una hipótesis, no
  un descarte.

**Criterio:** `E(F)` del agente < `E(F)` del clon, con IC que excluya cero.

---

## F5 — Deriva y portabilidad (`DRIFT-*`)

**Pregunta:** ¿sobrevive el conocimiento a un cambio de reglas y de modelo?
Predicción **P5**.

- Cambio de semántica a mitad de currículo.
- Cambio de modelo subyacente.
- Retirada de artefactos obsoletos sin perder los válidos.

**Criterio:** detecta la obsolescencia y no arrastra el error. Si el efecto
desaparece al cambiar de modelo, CUMULUS no tiene objeto.

---

## Lo que no se hace

- No se añaden acciones al controlador.
- No se construyen SIR, Canon ni JANUS-C.
- No se escribe otra capa social.
- No se ejecuta el 007 antes de F1.
- No se cita un competidor sin haberlo reproducido o declarado la deuda.

---

## Lo que se abandona

- «Más macros = más inteligencia».
- «La memoria amplía lo que el agente puede expresar» como afirmación general.
- Optimizar el probe o el desalojo como prioridad científica.
- Presentar cotas superiores como mediciones.
- Presentar diferencias de una tarea como superioridad.
- «96 episodios no caben en una ventana»: no medimos tokens.

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
