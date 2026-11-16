# Revisión de rumbo científico

**Fecha:** 16 de noviembre de 2026
**Origen:** auditoría de dirección sobre `0f518cc`.
**Estado:** documento de decisión. No propone arquitectura nueva. Responde las
cinco preguntas exigidas, fija una definición operacional, responde las 35
preguntas y decide qué se abandona.

> **Documento histórico de decisión.** La formulación vigente del marco está en
> [`teoria.md`](teoria.md) y el estado de cada afirmación en
> [`registro-de-afirmaciones.md`](registro-de-afirmaciones.md). Si hay conflicto,
> mandan esos dos.

---

## 0. Resumen ejecutivo

1. **El 006-A queda retirado.** La auditoría encontró cinco fallos de
   implementación; corregidos, el resultado se invierte: la política aprendida
   **no supera a una regla de una línea** y **cuesta 1,8× más** cuando se cuenta
   su propio probe. Los detalles están en `prototipo-006-politica/` (corregido) y
   el resultado anterior queda archivado como histórico.
2. **El 005 se reetiqueta.** Compara dos diseños bajo el mismo presupuesto de
   pasos, no una ablación limpia de memoria: `NOLEARN` busca a profundidad 3 y las
   políticas con memoria a profundidad 2. La diferencia de expresividad es parte
   del objeto de estudio, no un detalle.
3. **Se abandona la línea de optimizar el probe.** No es la prioridad científica.
4. **Se adopta una definición operacional de «más capaz»** (§2) y un test de clon
   obligatorio para todo protocolo futuro.
5. **El 007 se redefine**: no más macros, sino el test de clon con un agente real,
   herramientas y un currículo de familias reservadas.

---

## 1. Las cinco preguntas exigidas

### A. ¿Qué competencia adquirida estamos intentando medir?

**La reducción del coste de adquirir una competencia nueva, atribuible al
historial.**

El documento anterior definía `C(A, F)` como «experiencias **y** pasos ejecutados»
y luego comparaba un único número. Eso mezcla dos recursos con precios distintos.
Se corrige: **tres métricas separadas**, nunca una sola.

| Métrica | Qué mide | Unidad |
|---|---|---|
| `E(A, F)` | Eficiencia muestral | Experiencias hasta el umbral `θ` |
| `K(A, F)` | Coste de cómputo y contexto | Pasos, tokens, llamadas, dinero |
| `P(A, F)` | Desempeño en tareas reservadas tras `N` experiencias | Acierto o calidad |

La comparación es contra un **clon** `A₀` sin historial, mismo modelo, mismas
herramientas iniciales, mismo presupuesto:

`E(A,F) < E(A₀,F)` y/o `P(A,F) > P(A₀,F)` **a igual `K`**.

**No se agregan en un escalar** hasta que un escenario concreto fije los precios.
Un agente que necesita menos experiencias y mucho más cómputo no es «mejor» en
abstracto: es distinto, y hay que decirlo.

El test de clon responde a una afirmación concreta —«esta diferencia se debe al
historial»—, no a una definición metafísica de inteligencia. Un empate en un
benchmark no prueba que no se aprendió nada; prueba que **ese** benchmark no
detecta la diferencia.

### B. ¿Qué mecanismo produce esa adquisición y qué antecedentes ya la explican?

El mecanismo propuesto es **compilar experiencias en artefactos acotados
(procedimientos, herramientas) y conservar solo los que reducen el coste futuro**.
Los antecedentes que ya lo explican, y contra los que hay que compararse:

| Antecedente | Qué cubre |
|---|---|
| DreamCoder, Stitch, LILO | Bibliotecas de funciones y compresión de programas |
| CEGIS, Angluin | Aprender de contraejemplos y consultas activas |
| LPA*, D* Lite | Reutilizar trabajo de búsqueda entre problemas |
| Metarrazonamiento (Russell y Wefald) | Valorar el coste de decidir |
| MAML, metaprendizaje | Reducir experiencias necesarias para tareas nuevas |
| Mem²Evolve, AdaMEM | Crear activos y adaptar memoria durante la tarea |
| MemDev-Bench, VibeMemBench | Medir memoria en agentes de programación reales |

**Ninguna pieza es nueva.** La contribución posible es una medición longitudinal
con el test de clon, no un mecanismo.

### C. ¿Qué comparación podría demostrar que no existe ventaja real?

Tres, y las tres deben estar implementadas antes de declarar nada:

1. **Clon sin historial** con el mismo modelo, herramientas y presupuesto.
2. **Historial completo** recuperado por un recuperador convencional (la línea
   base que la industria ya tiene).
3. **Regla simple sin aprendizaje** para cualquier política de control.

Si el clon empata, no hay aprendizaje. Si el historial completo empata, la
abstracción no aporta. Si una regla de una línea empata, el aprendiz no aporta.

El 006-A' ya mostró el valor de la tercera: la política perdió contra la regla
simple.

### D. ¿Qué relación tiene el experimento con miles de tareas y con el contexto?

Hoy, **ninguna demostrada**. Los prototipos usan 96 tareas, un universo de 14
comportamientos y no miden tokens. La relación es una hipótesis:

> Un artefacto acotado puede conservar competencia con menos contexto que el
> historial bruto, y esa ventaja crece con el número de tareas.

Para convertirla en evidencia hace falta: (i) medir tokens y almacenamiento
reales, no sustitutos; (ii) un currículo de cientos de tareas con familias
reservadas; (iii) comparar historial completo, resumen y artefacto bajo el mismo
presupuesto de contexto.

**No hemos medido nada de eso.** La frase «96 episodios no caben en una ventana»
se retira del README: no la medimos.

### E. ¿Qué abandonaríamos si el resultado fuera negativo?

- Se abandona la afirmación de **expansión de competencia** por macros.
- CUMULUS queda como hipótesis de **representación y portabilidad**, sin
  evidencia empírica propia.
- JANUS queda como **diseño de política de confianza**, sin validación.
- Se conserva el valor negativo: sabemos qué no funciona y por qué.
- **No se sustituye por otra arquitectura.** Se publica el resultado y se reduce
  el alcance del programa a lo que sobreviva.

---

## 1.5 El criterio que faltaba: valor neto de decidir

La auditoría señaló la tradición de metarrazón (Russell y Wefald, 1991). Su
criterio, aplicado a cualquier operación de control `q` (recuperar, verificar,
experimentar):

`V_neto(q) = E[U | q] − E[U | ¬q] − C(q)`

El 006-A′ lo midió por primera vez en el proyecto: `C ≈ 41` pasos de probe,
`E[U|q] − E[U|¬q] ≈ 29` pasos ahorrados. **`V_neto < 0`.**

Desde ahora, ningún controlador entra en un protocolo sin reportar `V_neto`. Una
política que acierta más y cuesta más no es una mejora; es un cambio de régimen de
coste.

## 2. Definición operacional de «más capaz»

Cuatro niveles, de menor a mayor exigencia. Cada uno tiene su prueba.

| Nivel | Qué cambia | Prueba operacional |
|---|---|---|
| **Memoria** | Información disponible | El agente recupera el episodio **sin conocer la solución** y su respuesta mejora |
| **Procedimiento** | Operaciones reutilizables | El artefacto reduce pasos con igual éxito |
| **Concepto** | Representación del problema | Identifica una relación, predice casos nuevos, reconoce contraejemplos y transfiere sin traducción humana |
| **Metaprendizaje** | Capacidad de adquirir | Menos experiencias para dominar una familia nueva |

El criterio de **concepto** se refuerza: cambiar nombres de variables o de
herramientas no es conceptualizar. Se exigen las cuatro condiciones:

1. **Relación**, no etiqueta: el agente identifica qué conecta los casos.
2. **Predicción**: acierta casos que no estaban en la experiencia.
3. **Contraejemplo**: reconoce uno y revisa la relación.
4. **Transferencia**: funciona con otra manifestación superficial y **sin** que un
   humano traduzca la estructura.

Regla de oro, obligatoria en cada protocolo nuevo:

> **Test de clon.** Después de `N` experiencias, comparar contra un clon idéntico
> iniciado desde cero, con el mismo presupuesto. Si el clon empata **en la métrica
> declarada**, la afirmación sobre esa métrica no se sostiene.

El test no dice «no aprendió nada»; dice «esta diferencia no es atribuible al
historial en esta distribución».

Estado actual: **nivel 1 no demostrado en un agente real** (el 006-B usó selección
por oráculo); nivel 2 refutado para macros de dos pasos en un universo finito;
niveles 3 y 4 sin evidencia.

> **Nota sobre las «14 funciones».** La cifra del 005 sale de comparar los
> programas sobre 40 entradas de prueba. Es una **aproximación de equivalencia
> conductual sobre ese conjunto**, no una demostración de equivalencia para toda
> entrada posible. Se usa para decir «la rejilla tiene muchas menos clases
> aparentes que filas», no como teorema.

---

## 3. Las 35 preguntas, en breve

### I. Propósito

| # | Respuesta breve |
|---|---|
| 1 | Más capaz = `Δ(F) > 0` con el test de clon, no más aciertos en lo conocido. Especialización se controla con familias reservadas. |
| 2 | Una competencia que no estuviera en el solucionador, herramientas ni espacio inicial. Hoy no hemos demostrado ninguna. |
| 3 | Hoy, una memoria que acelera cálculos conocidos. No una que mejore el pensamiento. |
| 4 | Resolvería el coste de reutilizar procedimientos verificados. **No** resolvería representación, planificación ni verificación. |
| 5 | El test de clon con currículo de familias reservadas. **No** optimizar el probe. |

### II. Aprendizaje conceptual

| # | Respuesta breve |
|---|---|
| 6 | En ningún algoritmo implementado. `learn_macros` cuenta pares; no descubre representaciones. |
| 7 | Macro = secuencia frecuente; relación estructural = invariancia entre programas; estrategia = política de búsqueda. Solo la primera está implementada. |
| 8 | No. No hay mecanismo de alineamiento entre dominios. |
| 9 | Se revisa con contraejemplos (CEGIS) y con una política de retirada. El 006 mostró que la retirada ingenua empeora. |
| 10 | No. El aprendizaje activo (Angluin) está citado y no implementado. |

### III. Memoria y contexto

| # | Respuesta breve |
|---|---|
| 11 | No lo sabemos: no medimos tokens. Es la pregunta central del 007. |
| 12 | Hay un indicio: 8 macros con 76 % de acierto. Falta medir contexto real y distribuciones. |
| 13 | Medimos pasos ejecutados; **no** tokens, ni recuperación, ni coste de almacenamiento. Es una carencia declarada. |
| 14 | Sí: el 005 mostró que acumular baja el acierto 8,7 pp. No sabemos predecir cuáles dañan. |
| 15 | No implementado. La reconstrucción desde episodios es una hipótesis abierta. |

### IV. Inteligencia y cómputo

| # | Respuesta breve |
|---|---|
| 16 | **No lo sabemos.** El piloto 006-B no separa las siete capacidades y sus intervalos cruzan cero. |
| 17 | Tampoco: la condición de herramienta estaba contaminada por errores de entorno y la de memoria usaba la respuesta. Ver `errata-006b.md`. |
| 18 | Una política de dos acciones sí; con cuatro (recuperar, razonar, experimentar, crear) no hay evidencia. |
| 19 | El 006-A' lo midió: decidir cuesta 41 pasos y ahorra 29. **La decisión no paga.** |
| 20 | Sí, en parte: el 005 midió la curva de continuidad. Predecir el cambio, no. |

### V. Validez experimental

| # | Respuesta breve |
|---|---|
| 21 | No siempre: el 005 mezcla profundidades y el 006 tenía cinco fallos. Corregidos en 006-A'. |
| 22 | El 004 estaba alineado con el mecanismo; el 005 y el 006-A' usan reserva. Sigue siendo un riesgo. |
| 23 | Sí: búsqueda profunda, regla simple, historial completo. Dos ya destruyeron nuestras hipótesis. |
| 24 | Repiten la misma estructura con otros números. Es una limitación declarada. |
| 25 | El 004 lo hizo: 64/64 → 54/64. El clon es el estándar desde ahora. |
| 26 | No hay ninguna prueba de transferencia a familias nuevas. Pendiente. |

### VI. Precedentes y originalidad

| # | Respuesta breve |
|---|---|
| 27 | Ninguno demostrado. DreamCoder/Stitch/LILO cubren bibliotecas; CEGIS, contraejemplos; LPA*, reutilización; MAML, metaprendizaje. |
| 28 | La afirmación defendible es **evaluación longitudinal honesta con test de clon**, no mecanismo nuevo. |
| 29 | No. Stitch y DreamCoder no están ejecutados. Es una deuda declarada. |
| 30 | MemDev-Bench (la memoria puede romper tareas antes resolubles) y SkillLearnBench (deriva) contradicen la hipótesis fuerte. |

### VII. Futuro

| # | Respuesta breve |
|---|---|
| 31 | No. Más macros no es el objetivo; el objetivo es `Δ(F) > 0`. |
| 32 | Sí, si reduce `C` en familias reservadas. Se mide con el test de clon. |
| 33 | No evaluado. La portabilidad es la hipótesis de CUMULUS y no tiene evidencia. |
| 34 | Sin evidencia. Es el nivel 4 y exige un currículo interdependiente. |
| 35 | `Δ(F) > 0` reproducible en ≥ 2 familias reservadas y ≥ 2 modelos, con coste total controlado. |

---

## 4. Qué se abandona, qué se conserva

**Se abandona**

- «Más macros = más inteligencia».
- «La memoria amplía lo que el agente puede expresar» como afirmación general.
- Optimizar el probe o el desalojo como prioridad científica.
- Presentar cotas superiores como mediciones.
- Presentar diferencias de una tarea como superioridad.

**Se conserva**

- Los resultados negativos: 004, 005, 006-A'.
- La disciplina de contabilidad y los protocolos congelados.
- El test de techo con agente real (46,9 %), que abre el experimento correcto.
- La pregunta del clon como puerta de entrada a todo protocolo.

---

## 4.5 Dos horizontes, dos preguntas

La auditoría propone separar lo inmediato de lo fundamental. Se adopta.

**Horizonte inmediato — ¿la memoria cambia una decisión real?**
Un agente congelado, tareas con verificación ejecutable, comparación pareada:
sin ayuda, con más ejemplos, con el lenguaje de operaciones, con herramienta de
ejecución, con verificador, con procedimiento recuperado, con biblioteca.
Métrica: acierto pareado y coste total. Es el experimento del 006-B ampliado.

**Horizonte fundamental — ¿la experiencia cambia cómo se aprende?**
Currículos interdependientes, familias reservadas, test de clon. Métricas: `E(F)`,
`K(F)` y `P(F)` por separado. Es el 007.

**Regla:** no se mezclan en una sola puntuación. Un resultado del horizonte
inmediato no se presenta como evidencia del fundamental.

## 4.6 Lo que el diagnóstico del agente **no** respondió

Cinco condiciones, 24 tareas pareadas, mismo modelo. Pero leídas con la errata
(`docs/errata-006b.md`):

| Intervención | Δ acierto | IC 95 % | Veredicto |
|---|---|---|---|
| Más ejemplos | +8,3 pp | −20,8 a +33,3 | Inconcluso |
| Vocabulario de operaciones | +4,2 pp | −12,5 a +25,0 | Inconcluso |
| **`ORACLE-MEMORY`** (seleccionada con la solución) | +8,3 pp | −12,5 a +33,3 | **No es memoria** |
| Intérprete exigido | 0,0 pp | −29,2 a +29,2 | **Condición inválida** (16/24 con errores de entorno) |

Tres correcciones que impiden la conclusión anterior:

1. La «memoria» se fabricaba con `task.solution.program`: conocía la respuesta.
2. La muestra `[:24]` son 16 tareas que empiezan por `sort_asc` y 8 por
   `sort_desc`; **ninguna** por `add_one` o `double`.
3. La condición de herramienta no verificó ejecución, validación ni uso del
   resultado; el exit 0 de Codex no es el exit del script.

**Conclusión correcta:** el piloto **no permite decidir** dónde está el cuello.
Identificó cinco fallos metodológicos, que es valioso, y nada más.

## 5. El 007: experimento mínimo

**Pregunta:** ¿una experiencia histórica **recuperada sin conocer la respuesta**
reduce el coste de resolver una tarea nueva en un agente real, frente a un clon sin
historial?

**Diseño**

- Agente: modelo congelado, herramientas **verificadas por tarea** en cinco etapas
  (disponible, intentada, ejecutada con exit real, validada contra los ejemplos,
  usada en la respuesta).
- Tareas: estratificadas por **clase conductual**, con instancias numéricas nuevas y
  familias reservadas.
- Condiciones pareadas, mismo modelo y presupuesto:
  1. clon sin historial;
  2. `ACTUAL-RETRIEVAL`: recuperador que **solo ve la observación actual**;
  3. `ORACLE-MEMORY`: techo de información, etiquetado como oráculo;
  4. procedimiento verificado;
  5. herramienta compilada y verificada.
- Métricas **separadas**: `E(F)` experiencias hasta el 80 %, `K(F)` cómputo y
  tokens, `P(F)` desempeño reservado. Sin escalar único.
- Refutación: si el clon empata en `E` y `P` a igual `K`, la memoria no aporta. Si
  `ACTUAL-RETRIEVAL` empata con el clon pero `ORACLE-MEMORY` gana, el fallo es del
  recuperador, no del mecanismo.
- **Puerta previa:** no se ejecuta el 007 hasta completar la descomposición del
  007A (siete capacidades) con muestra equilibrada.

**Lo que no hará:** añadir acciones al controlador, ni macros nuevas, ni otro
solucionador sintético.

**Si sale negativo:** se publica y se cierra la línea de expansión; CUMULUS y JANUS
quedan como marcos sin validación empírica.

---

## 6. Lo que este documento no arregla

- No hay medición de tokens ni de contexto real.
- No hay comparación ejecutada con Stitch, DreamCoder o LILO.
- No hay contraejemplos ni ambigüedad implementados.
- El 006-A' corrige cinco fallos, pero sigue siendo un universo de una familia.
- La respuesta a «¿qué entiende el agente después de mil experiencias?» es hoy:
  **no lo sabemos, y no tenemos el instrumento para medirlo.**
- El 007B no puede ejecutarse hasta completar el 007A: sin separar las siete
  capacidades, cualquier resultado de recuperación es ambiguo.
