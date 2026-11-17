# Memoria útil en agentes: información, aplicación y verificación

**Subtítulo:** de los resultados negativos a un protocolo de memoria verificada

**Autor:** Juan David Salas Camargo (MIT)
**Colaboración:** DeepSeek 4.1 Flash (agente de investigación)
**Fecha:** 16 de noviembre de 2026
**Estado:** preprint no arbitrado. Listo para revisión por pares.
**Repositorio:** https://github.com/jdsalasca/open-human-memory
**Versión:** `v1.26-review`

---

## Resumen

Este es un **artículo metodológico** sobre memoria en agentes. No demuestra
aprendizaje acumulativo ni expansión de competencia. Su contribución es un estudio de
caso replicable de por qué los experimentos de memoria producen conclusiones
engañosas, y el instrumento que separa información, aplicación, verificación y
encuadre.

Primero presentamos **seis experimentos negativos** (002–007) con un solucionador de
programas. En un espacio **explorable, identificable y presupuestado**, la búsqueda
sin memoria iguala la cobertura de una biblioteca aprendida; la biblioteca solo reduce
coste (41,8 % menos pasos con continuidad total) y lo pierde todo con continuidad cero
(22,1 pp menos). Una política aprendida no supera a una regla de una línea y cuesta
1,42× la búsqueda. Un agente real (`gpt-6-luna`, esfuerzo bajo) acierta 46,9 %.

Después de una auditoría externa, el trabajo **retracta** su experimento de
representación (LIRE-001b): las 120 reglas eran una sola fórmula, el verificador no
comprobaba pertenencia y el orden no estaba aleatorizado. El reemplazo, LIRE-002, usa
información independiente y un **control sin tabla**: el control acierta 0/7 casos
positivos; la recuperación funciona (6–7/7), pero **los fallos que quedan están en
evaluar la condición**, no en almacenar la regla. El chino no ahorra tokens (2.949 vs
2.841 del español) ni acierta más: la ventaja anterior era un artefacto.

El **diagnóstico de ejecución** muestra que el 007 estaba fuera de régimen: con el
programa completo, `luna` acierta 11/12 con 2 operaciones, 7/12 con 3, 8/12 con 4 y
4/12 con 5. Medido por **longitud mínima equivalente**, 2 operaciones aciertan 18/21
(86 %), 3 aciertan 8/18 (44 %) y 5, 0/1.

El **primer resultado positivo de este programa** aparece en 2 operaciones: un
artefacto **verificado fuera del prompt** y presentado como **conocimiento aplicable**
acierta 10–11/12, frente a 3–5/12 del clon, 2–3/12 del placebo y 0/12 de un placebo
etiquetado como verificado. El mismo programa presentado como «subrutina candidata;
verifícala» acierta 3–4/12: **el encuadre y la instrucción explican parte de la
diferencia**. El placebo verificado demuestra que la etiqueta sola no basta; el
contenido correcto supera al incorrecto bajo el mismo encuadre, pero un procedimiento
falso declarado verificado induce errores sistemáticos.

**El alcance es más estrecho de lo que parece.** Las doce tareas ya están determinadas
por los dos ejemplos de soporte: el clon tiene la información. El artefacto no aporta
un hecho desconocido; entrega el programa explícito en lugar de exigir inferirlo. El
resultado mide **inferir frente a recibir**, no memoria de algo que solo estuviera en
la experiencia. **MEM-005** separa contenido, estado e instrucción: el efecto grande
solo aparece en verificado+aplicar (12/12 vs 1/12), y un **programa escrito por un
programador, sin aprendizaje previo, acierta 12/12**. No hay evidencia de ventaja de
adquisición en esta tarea, pero el control cambia procedencia y orden: no es una
equivalencia. El positivo es instrucción y contenido, no memoria. No hay recuperación
autónoma entre varias memorias.

El resultado es **uso de memoria**, no expansión de competencia: la tarea de 2
operaciones es enumerable e identificable, y la memoria ahorra el coste de
identificarla. La pregunta de expansión sigue abierta y exige una tarea que el modelo
pueda aplicar y que no quepa en el presupuesto. La comparación decisiva
—recuperación genuina, familias reservadas, coste total y ciclo longitudinal— **no se
ha ejecutado**.

**Palabras clave:** memoria de agentes, competencia acumulativa, verificación,
encuadre, información usable, validez experimental, resultados negativos.

---

## Abstract

This is a **methodological paper** on memory in agents. It does not demonstrate
cumulative learning or competence expansion. Its contribution is a replicable case
study of why memory experiments produce misleading conclusions, and the instrument
that separates information, application, verification, and framing.

We first report **six negative experiments** (002–007) with a program solver. In an
**explorable, identifiable, budgeted** space, memoryless search matches the coverage
of a learned library; the library only reduces cost (41.8% fewer steps at full
continuity) and loses it all at zero continuity (22.1 pp). A learned activation
policy does not beat a one-line rule and costs 1.42× memoryless search. A real agent
(`gpt-6-luna`, low effort) scores 46.9%.

After an external audit, the paper **retracts** its representation experiment
(LIRE-001b): the 120 rules were one formula, the verifier did not check membership,
and case order was not randomized. Its replacement, LIRE-002, uses independent
information and a **no-table control**: the control scores 0/7 positive cases;
retrieval works (6–7/7), but **the remaining failures are in evaluating the
condition**, not in storing the rule. Chinese does not save tokens (2,949 vs 2,841 for
Spanish) or improve accuracy: the earlier advantage was an artifact.

The **execution diagnosis** shows that 007 was outside the regime: with the full
program, `luna` scores 11/12 with 2 operations, 7/12 with 3, 8/12 with 4, and 4/12
with 5. Measured by **minimum equivalent length**, 2 operations score 18/21 (86%), 3
score 8/18 (44%), and 5 score 0/1.

The **first positive result in this project** appears at 2 operations: an artifact
**verified outside the prompt** and presented as **applicable knowledge** scores
10–11/12, versus 3–5/12 for the clone, 2–3/12 for the placebo, and 0/12 for a placebo
labeled as verified. The same program presented as a “candidate subroutine; verify
it” scores 3–4/12: **framing and instruction explain part of the difference**. The
verified placebo shows that the label alone is not enough; correct content beats
incorrect content under the same framing, but a false procedure declared verified
induces systematic errors.

**The scope is narrower than it looks.** The twelve tasks are already determined by
the two support examples: the clone has the information. The artifact does not supply
an unknown fact; it supplies the explicit program instead of requiring inference. The
result measures **inferring versus receiving**, not memory of something that only the
experience contained. **MEM-005** separates content, status, and instruction: the
large effect appears only under verified+apply (12/12 vs 1/12), and a
**programmer-written program with no prior learning scores 12/12**. Acquisition adds
nothing in this task; the positive result is instruction and content, not memory.
There is no autonomous retrieval across multiple memories.

The result is **instruction/content use**, not memory acquisition and not competence
expansion: the 2-operation task is enumerable and identifiable, and the artifact saves
the cost of identifying it. The
expansion question remains open and requires a task the model can apply and that does
not fit the budget. The decisive comparison — genuine retrieval, reserved families,
total cost, and a longitudinal cycle — **has not been run**.

---

## 1. Introducción

Un agente que reinicia su contexto olvida lo que aprendió. La respuesta habitual es
añadir memoria: episodios, resúmenes, bibliotecas de habilidades, herramientas. La
literatura de 2025–2026 está llena de sistemas que declaran mejoras. La evidencia
sobre **qué parte de la mejora se debe a la experiencia** es mucho más débil.

Este trabajo empezó con una ambición mayor —memoria inspirada en neurociencia,
etología y sociología— y terminó en una pregunta más pequeña y más honesta:

> Si el agente reinicia su contexto, cambia de tarea y encuentra un problema nuevo,
> ¿qué aprendizaje adquirido antes modifica su forma de comprenderlo y resolverlo?

La respuesta que podemos sostener hoy es doble. **En las tareas que el modelo no
puede aplicar, no hay evidencia**: el 007 pedía cinco operaciones y el oráculo mismo
acertaba 2/12. **En una tarea de dos operaciones efectivas, un artefacto verificado y
presentado como conocimiento aplicable se usa**: 10–11/12 frente a 3–5/12 del clon.
Pero eso es **uso de información**, no expansión de competencia: la tarea es
enumerable e identificable, el clon ya tiene la información en los dos ejemplos y la
memoria ahorra el coste de identificarla. El resultado mide **inferir frente a
recibir**, no un hecho que solo estuviera en la experiencia. Lo que sí podemos
sostener es por qué los negativos no eran interpretables, qué separa el uso de la
expansión y qué haría falta para que la respuesta cambie.

### Contribución

Una **demostración metodológica** con cuatro piezas:

1. **El instrumento:** clon sin historial, canales separados, métricas `E`/`K`/`P`,
   control sin tabla, acierto estratificado, tokens incrementales pareados, longitud
   mínima equivalente y **placebo verificado**.
2. **Los negativos, con diagnóstico:** en espacio enumerable la memoria solo reduce
   coste; el 007 estaba fuera de la ejecución y presentaba el artefacto como
   candidato; el LIRE-001b era una tabla redundante.
3. **El positivo condicionado:** en 2 operaciones, un procedimiento correcto
   presentado como verificado se usa (10–11/12) si el contenido está verificado fuera
   del prompt y el encuadre es definitivo; el encuadre de candidata lo hunde a 3–4/12.
   Las tareas son identificables desde los ejemplos: el artefacto entrega el programa,
   no un hecho desconocido.
4. **La condición de seguridad:** la etiqueta «verificado» no basta; un programa falso
   etiquetado así acierta 0/12. El modelo no puede ser el verificador de su propia
   memoria.

Las piezas de apoyo son: la proposición con condiciones, los experimentos, la revisión
estructurada de 31 trabajos y el registro de 100 afirmaciones. Ninguna se presenta como
una teoría general de memoria.

### Lo que no se afirma

- No se afirma que la memoria no sirva a los agentes.
- No se afirma que las habilidades no funcionen.
- No se afirma novedad algorítmica: ninguna pieza es nueva.
- No se afirma transferencia entre modelos ni aprendizaje conceptual.
- **No se afirma expansión de competencia:** el resultado positivo vive en un espacio
  enumerable e identificable; la memoria ahorra identificación, no amplía el espacio.
- **No se afirma transferencia a familias reservadas:** las tareas empiezan por el
  motivo aprendido; es reutilización favorable.
- **No se afirma generalidad:** n=12 por condición, una semilla, un modelo; la réplica
  de 24 tareas está pre-registrada y pendiente.
- **No se afirma que el modelo pueda autoverificarse:** la verificación es externa;
  un placebo verificado acierta 0/12 y se aplica con confianza.

---

## 2. Trabajo relacionado

La revisión completa está en `resources/investigation/revision-sistematica/`. Aquí
se sintetiza por mecanismo, no por cronología.

**Aprendizaje de bibliotecas.** DreamCoder (Ellis et al., 2021) aprende abstracciones
y una política de búsqueda; Stitch (Bowers et al., 2023) hace tratable el
descubrimiento por compresión; LILO (Grand et al., 2024) añade documentación. Nuestro
Prototipo 003 es una versión mínima de esta idea, sin aplicabilidad ni terminación.

**Sistemas de habilidades.** Mem²Evolve (ACL 2026) coevoluciona experiencia y
activos (+18,53 % sobre LLM, +11,80 % sobre experiencia sola, +6,46 % sobre activos
solos). MUSE-Autoskill crea y refina skills; Trace2Skill destila trayectorias;
SkillGen induce contrastivamente de éxitos y fallos. SoK: Agentic Skills (2026)
documenta que una skill incluye aplicabilidad, política y terminación: nuestra macro
no era una skill.

**Verificación.** Proof-Gated Skill Compilation (NeurIPS 2026 workshop) solo conserva
programas ejecutados contra ground truth: **52 de 538** aserciones de verificación
fueron confirmadas y **486** rechazadas. La verificación operacional, por tanto, ya
existe; la identificación causal es otro problema.

**Benchmarks de memoria y transferencia.** MemDev-Bench (555 tareas base + 4.869
históricas) muestra que la memoria mejora localización y edición y **también rompe
tareas antes resolubles**. VibeMemBench (111 objetivos, 90 repositorios) transfiere
experiencia verificada a cinco solvers. MemUse (8.000 episodios) encuentra que las
tasas de resolución quedan **a ±0,4 pp** del baseline sin memoria y que **23,2 %** de
los usos beneficiosos igual fallan. EvoAgentBench mide transferencia de
procedimientos en cuatro dominios; SelfImprove-Bench separa capacidad de ajuste al
escenario; AgentCL exige dependencias cross-task; SWE-Bench-CL usa streams
cronológicos.

**Fallos y límites.** *Skill shadowing*: hasta **−21 %** al crecer a 202 skills.
«Contextual Agentic Memory is a Memo» (2026) argumenta que retrieval no es memoria y
que existe un techo de generalización composicional. RSE-Bench muestra que el ruido
no adversarial persiste en las reglas aprendidas. Skill Drift mide la decadencia por
cambios de API. Bemula mide el olvido a petición.

**Clásicos.** CEGIS y SyGuS (contraejemplos), Angluin (consultas), LPA* (reutilizar
búsqueda), options (inicio, política, terminación), MAML (adaptación rápida),
Information Bottleneck (compresión útil) y metarrazonamiento (valor neto de decidir).

**Posición.** El campo tiene los mecanismos. Lo que no tiene es una medición
longitudinal que separe información, representación, política, herramientas y
parámetros, con clon y coste total. Eso es lo que este trabajo intenta aportar, y
todavía no lo ha ejecutado.

---

## 3. Teoría

### 3.1 Los cinco canales

La historia puede cambiar la competencia por cinco vías: **información** (episodios,
ejemplos), **representación** (conceptos, vocabulario), **política** (qué buscar,
cuándo parar), **herramientas** (procedimientos verificados) y **parámetros** (pesos).
Confundirlos produce resultados ambiguos: una mejora por más ejemplos no es una
mejora por memoria.

### 3.2 La proposición

> Sea `O` finito, `L` una profundidad y `B` un presupuesto. Si el solucionador
> enumera todos los programas de longitud `≤ L` dentro de `B` **y la tarea es
> identificable** —todas las hipótesis compatibles coinciden en la consulta—, su
> cobertura es **1 por construcción**. En ese régimen la memoria no puede aumentar
> la cobertura; solo reordenar la búsqueda y reducir coste.

Tres precisiones que la versión anterior de este trabajo no hacía:

1. **Identificabilidad.** Enumerar no garantiza acertar. Si dos programas
   compatibles divergen en la consulta, el solucionador devuelve el primero y falla.
   Con entradas constantes, `sort_asc` y `sort_desc` son indistinguibles.
2. **Candidatos no es coste.** `4 + 16 + 64 = 84` programas no son 84 pasos: cada
   candidato se comprueba contra tres ejemplos. Bajo 120 pasos el espacio puede no
   recorrerse entero. La proposición vale para el espacio **explorado**.
3. **Terminología.** No es un «universo no enumerable»: es un espacio **no
   explorable exhaustivamente bajo el presupuesto**. Con seis operadores y
   profundidad seis son 55.986 programas; siguen siendo finitos, pero no caben en
   `B`.

**Corolarios.** (i) El 100 % del Prototipo 003 era el experimentador bajando la
profundidad a dos, no una capacidad del agente. (ii) Los negativos de 004–006 son **coherentes con la teoría** en el régimen
identificable y presupuestado; fuera de él, la teoría no dice nada y no puede
cerrar la línea. (iii) Para probar expansión basta con que la solución caiga fuera
del presupuesto; la ambigüedad es un problema **adicional**, no una condición
necesaria.

### 3.3 Las siete capacidades

Inferencia, desambiguación, experimentación, ejecución, verificación, memoria y
generalización. Un fallo del agente puede venir de cualquiera; nuestro piloto no las
separó. El diagnóstico es la primera fase del plan (F1).

### 3.4 Los cinco confundidores

Fuga de la respuesta (001, `ORACLE-MEMORY`), confusor de profundidad (005), muestra
sesgada (006-B), integración fallida de herramientas (006-B) y clases conductuales
correlacionadas (004/005). Añadimos un sexto, metodológico: inferir de un piloto con
intervalos que cruzan cero.

### 3.5 Hipótesis y predicciones

**H.** La historia puede actuar por cualquiera de los cinco canales. El programa no
declara un ganador de antemano: mide cuál reduce `E(F)` a igual `K`.

| ID | Predicción | Se refuta si |
|---|---|---|
| P1 | En espacio no explorable bajo `B`, una herramienta compilada amplía cobertura a igual presupuesto | La cobertura no sube, o sube sin historial |
| P2 | A igual información, un procedimiento verificado bate a un episodio | Empatan |
| P3 | `E(F)` baja solo con estructura compartida | Baja con vocabulario compartido y estructura distinta |
| P4 | **Discriminante:** ventaja informacional desaparece al dar los mismos ejemplos al clon; ventaja de herramienta o política persiste | Persiste sin herramienta ni política distinta |
| P5 | El efecto sobrevive a cambiar de modelo | Desaparece |
| P6 | Elegir la **forma** (episodio, procedimiento, herramienta, concepto) según utilidad futura bate a una forma fija | Una forma fija iguala o supera |

P1–P5 están sin probar. P6 es la hipótesis nueva del programa y **no se ha buscado
suficientemente**: la revisión detectó al menos seis trabajos de 2026 sobre
selección de forma y granularidad. No se declara novedad.

---

## 4. Método

### 4.1 Tareas

Cuatro primitivas (`sort_asc`, `sort_desc`, `add_one`, `double`), profundidad
máxima tres. El espacio son 64 programas, que medidos por comportamiento sobre 40
sondas colapsan a **14 clases** (aproximación conductual, no equivalencia formal).
Cada tarea da tres pares entrada-salida y una consulta.

### 4.2 Solucionador

Búsqueda en anchura sobre secuencias de operaciones. Dos contadores:
`candidates` (programas examinados) y `executed_steps` (aplicaciones primitivas
ejecutadas hasta el primer contraejemplo). El segundo es el usado en 005 y 006; el
004 conserva `primitive_ops` como cota superior por trazabilidad.

**El presupuesto es aproximado.** Se comprueba antes de evaluar cada candidato, así
que el candidato aceptado puede rebasar el límite. Medido en las condiciones del
006: exceso máximo **6 pasos**, media ≤ 0,83, en ≤ 4 de 24 tareas
(`prototipo-006-politica/results/budget-overshoot.json`). No es un límite estricto
de 120 aplicaciones.

**El probe no se descuenta de la búsqueda.** En 006-A se contabiliza después de
resolver: la comparación de la política es de **coste ex post**, no de presupuesto
total igual. Una evaluación con presupuesto compartido queda pendiente.

### 4.3 Condiciones

- `MEM-A0`: mismo solucionador composicional, sin historial.
- `VALID-A1`: búsqueda a profundidad 3 sin biblioteca.
- `LEARNED`: biblioteca aprendida por frecuencia (pares repetidos ≥2).
- `ORACLE-MEMORY`: recuerdo construido con la solución verdadera (techo, no memoria).
- `ACTUAL-RETRIEVAL`: recuperador ciego a la solución (no ejecutado).
- `POLICY`: política lineal sobre un probe de aplicabilidad.
- `CLONE`: clon sin historial (control estándar).

### 4.4 Métricas

`accuracy`, `E(F)` (experiencias hasta umbral), `K(F)` (pasos, tokens, coste),
`P(F)` (desempeño reservado). No se agregan en un escalar.

### 4.5 Protocolos

- 004-A: SHA-256 del protocolo, reglas D1–D7 fijadas antes de la corrida. D8 es post
  hoc y se declara.
- 006-A: `frozen.sha256` con protocolo, cinco archivos de código y datos de las
  semillas 1 y 2. La semilla 0 fue desarrollo.
- 006-B: sin congelar; se declara exploratorio.

### 4.6 Modelo y esfuerzo

| Campo | Valor |
|---|---|
| Modelo | `gpt-6-luna` |
| Esfuerzo | `low` |
| CLI | `codex-cli 0.169.0` |
| Llamadas | 209 |
| Sandbox | `read-only` (excepto herramienta) |
| Fecha | 16 de noviembre de 2026 |

Detalle completo en `docs/registro-de-ejecuciones.md`. La revisión externa de este
manuscrito usó **`gpt-6.1-terra` con esfuerzo `medium`**; `gpt-6-terra` (sin punto)
no está disponible para cuentas ChatGPT. OpenCode se usó con
`deepseek-v4.1-flash-1017`.

> **Limitación.** El baseline del agente se ejecutó con `gpt-6-luna` low. Debe
> repetirse con `gpt-6.1-terra` medium antes de publicar; los resultados de este
> manuscrito son de ese modelo y esa configuración.

---

## 5. Resultados

**Tabla 1. Resumen verificable.** Unidad = tareas; la inferencia no es sobre
familias. Datos crudos en `results/` de cada prototipo. Las filas 002–007 son la fase
negativa; 007B, EXEC-001 y LIRE-002 la fase de diagnóstico; MEM-002/003/004 la fase
positiva condicionada.

| Exp | Hipótesis | Unidad | Condiciones | Coste medido | Resultado | Incertidumbre | Estado |
|---|---|---|---|---|---|---|---|
| 002 | `MEM-E` usa historial | 200/50, 3 semillas | A, A0, B, C, D, E | candidatos | A0 = E (1,000) | 3 semillas | Refutada |
| 003 | macros amplían D3 | 60/30, 3 semillas | NOLEARN, RANDOM, LEARNED, ABLATED | candidatos | 1,000 vs 0,000 | 3 semillas | Retirado por 004 |
| 004 | cobertura vs coste | 64 programas | A0–A4 + 560 bibliotecas | candidatos, steps | A1 64/64; A3 54/64; −17,8 % candidatos | 3 semillas | Negativo |
| 005 | valor condicional | 96 tareas, 4 fases | NOLEARN, FROZEN, ONLINE, GATED | steps | FROZEN 76 % con −26,2 % trabajo | 3 semillas | Condicional |
| 006-A′ | la política aprende | 48 tareas, semillas 1–2 | 7 condiciones | steps + probe | 92,7 % vs regla 93,8 %; 1,42× | bootstrap optimista | Negativo |
| 006-B | agente real | 24–64 tareas | 6 condiciones | llamadas, tiempo | 46,9 %; ninguna Δ ≠ 0 | IC ±20 pp | Inconcluso |
| 007 | retención + reinicio + transferencia | 12 tareas, `luna` low | clone, memory, placebo | llamadas | 1 ejemplo: 0/0/2; 2 ejemplos: 1/3/6 | 1–6 tareas | Negativo: el placebo supera a la memoria |
| 007B | información, instrucción o ejecución | 12 tareas, `luna` low | clone, memory, placebo, history, oracle | llamadas | 1/3/6/4/2 | — | Negativo: el oráculo 2/12 |
| EXEC-001 | aplicación con el programa dado | 12 tareas × 4 profundidades, `luna` low | oráculo simbólico | llamadas | 2 ops 11/12; 3 ops 7/12; 4 ops 8/12; 5 ops 4/12 | 1–5 tareas | La longitud efectiva manda |
| LIRE-001b | representación de una skill larga | 12 casos × 5 formas, `luna` low | español, inglés, chino, conciso, DSL | tokens | chino 11/12 (−1,4 %); conciso 8/12 (−6,1 %); DSL 7/12 (−4,4 %) | 1–4 casos | Retractado: la tabla era una fórmula |
| LIRE-002 | información independiente | 12 casos × 8 formas, `luna` low | 7 representaciones + sin tabla | tokens incrementales | sin tabla 0/7; en/DSL 12/12; tabla 8/12 | 1–2 casos | Mixto: condición, no idioma |
| MEM-002 | memoria en 2–3 operaciones | 12 tareas, `luna` low | clon, memoria, placebo, historial, oráculo | llamadas | 3 ops: 2/3/5/4/8; 2 ops: 5/7/4/9/11 | 1–6 pares | 3 ops negativo; 2 ops señal |
| MEM-003 | encuadre de la memoria verificada | 12 tareas, `luna` low | clon, candidata, verificada, placebo, historial, oráculo | llamadas | 3/4/11/3/10/12 | 0–7 pares | Positivo: el encuadre era el cuello |
| MEM-004 | placebo con etiqueta «verificado» | 12 tareas, `luna` low | 7 condiciones | llamadas | verificada 10/12; placebo verificado 0/12 | 0–10 pares | El contenido, no la etiqueta |
| MEM-005 | factorial contenido × estado × instrucción | 12 tareas, `luna` low | 10 condiciones, semilla 1 | llamadas | verificado+aplicar 12/12; placebo verificado+aplicar 1/12; escrito 12/12 | 0–11 pares | Sin evidencia de ventaja de adquisición; contenido+instrucción |

### 5.1 Prototipo 002: el solucionador, no la memoria

`MEM-A0`, el mismo solucionador sin historial, empata con `MEM-E` en D1, D2 y D3
(1,000). El 100 % de `MEM-E` no mide aprendizaje: mide que la composición está en el
espacio de hipótesis.

### 5.2 Prototipo 003: la capacidad retirada

Con profundidad 2, `LEARNED` resuelve 30/30 tareas D3 y `NOLEARN` 0/30. El 004
mostró que el límite de profundidad era del experimentador: a profundidad 3 sin
memoria se resuelve **64/64**.

### 5.3 Prototipo 004: cobertura frente a coste

| Condición | Aciertos /64 | Candidatos |
|---|---|---|
| Sin memoria, profundidad 2 | 33 (51,6 %) | 876 |
| **Sin memoria, profundidad 3** | **64 (100 %)** | 1.761 |
| Azar, mismo lenguaje, profundidad 2 | 50,7 (79,3 %) | 1.543 |
| Macros aprendidas, profundidad 2 | 54 (84,4 %) | 1.448 |
| Macros aprendidas, profundidad 3 | 64 (100 %) | 2.247 |

Barrido de las 560 bibliotecas de tres macros del mismo lenguaje: media **77,3 %**,
máximo 93,8 %, **ninguna perfecta** en la rejilla; en el conjunto de tres programas
del 003, **250/560 perfectas**. La adquisición satura en **6 experiencias**.

### 5.4 Prototipo 005: el valor es condicional

| Continuidad | Sin memoria d3 | Macros d2 |
|---|---|---|
| 0,00 | **100 %** · 58,0 pasos | 78 % · 57,8 |
| 0,50 | **100 %** · 81,1 | 80 % · 63,1 |
| **1,00** | **100 %** · 91,0 | **100 % · 52,9** |

Flujo de 96 tareas con deriva: congelar lo aprendido da **76,0 % con 5.074 pasos**
frente a 76,0 % con 6.877 sin memoria (−26,2 % de trabajo). Aprender siempre baja a
67,0 %; el desalojo por uso, a 64,6 %.

### 5.5 Prototipo 006-A′: la política no paga

| Condición | Mixto | Búsqueda + probe |
|---|---|---|
| Buscar sin memoria | 83,3 % | 59,5 |
| Macros primero | 90,6 % | 44,5 |
| Regla del probe (una línea) | **93,8 %** | 83,5 |
| Política aprendida | 92,7 % | 84,3 |
| Aleatoria uniforme | 85,4 % | 56,9 |
| Barajada (mismas frecuencias) | 87,5 % | 49,4 |

La política pierde contra la regla simple (−1,0 pp, IC −3,1 a 0); gana a buscar
(+9,4 pp, IC 3,1–15,6) y a su control barajado (+5,2 pp, IC 1,0–9,4). El probe
cuesta 41,2 pasos y el ahorro es 29: **valor neto negativo**.

**Advertencia estadística.** El bootstrap trata 96 tareas como independientes, pero
comparten generador, programas equivalentes, biblioteca y política; con dos semillas,
los IC son optimistas. No se usan para afirmar equivalencia ni ausencia de efecto.

### 5.6 Prototipo 006-B: el agente real

`gpt-6-luna` low acierta **30/64 (46,9 %)**. En 24 tareas pareadas: más ejemplos
+8,3 pp (IC −20,8 a +33,3), vocabulario +4,2 pp (IC −12,5 a +25,0), `ORACLE-MEMORY`
+8,3 pp (IC −12,5 a +33,3), herramienta exigida 0,0 pp (IC −29,2 a +29,2, condición
inválida). Ninguna intervención se distingue de cero.

### 5.7 Prototipo 007: retención, reinicio y transferencia

Primera prueba con retención real, reinicio de contexto y **placebo**. Sesión 1: el
agente devuelve un programa que nosotros verificamos con 60 entradas. Reinicio.
Sesión 2: 12 tareas de cinco pasos (motivo + tres operaciones), en tres condiciones
pareadas.

Con el modelo de experimentos (`gpt-6-luna` low), **la adquisición falló con seis
ejemplos**: el programa devuelto no reprodujo el motivo y el experimento abortó antes
de la sesión 2, como está diseñado. Con **doce ejemplos y «exactamente dos
operaciones»** verificó un programa conductualmente equivalente (`double → sort_asc`).

| Régimen (`luna` low) | `clone` | `memory` | `placebo` |
|---|---|---|---|
| 1 ejemplo de soporte | 0/12 | 0/12 | 2/12 |
| 2 ejemplos de soporte | 1/12 | 3/12 | **6/12** |

Con un ejemplo, el clon está en el suelo: la familia no discrimina. Con dos, el
placebo acierta el doble que la memoria (cuatro tareas discordantes a favor del
placebo, una a favor de la memoria; p = 0,38). **El artefacto verificado no supera a
uno falso.** La retención funcionó —el artefacto sobrevivió al reinicio— pero no
produjo ventaja.

La corrida con `gpt-6.1-terra` medium (exploratoria, no evidencia) había mostrado el
mismo patrón por arriba: clon 9–12/12, memoria 11/12 y placebo 11/12; el clon estaba
en techo. Las dos corridas, con modelos distintos, coinciden en el diagnóstico: **la
familia no tiene margen** para medir transferencia. Sin espacio para fallar, no hay
nada que transferir.

**007B: el cuello está en la aplicación del programa.** El diagnóstico añadió dos
condiciones a las mismas 12 tareas: **historial de origen** (los 12 pares de la
sesión 1) y **oráculo** (el programa completo, fuga deliberada). Resultado con
`luna` low: clon 1/12, memoria 3/12, placebo 6/12, historial 4/12, **oráculo 2/12**
(réplica: historial 3/12, oráculo 3/12). Con el programa completo, el modelo apenas
resuelve 2 de 12 composiciones de cinco pasos; los errores son permutaciones,
operaciones saltadas y aritmética. **No se identifica un mecanismo único**: puede ser
ejecución, interpretación de las operaciones, seguimiento de instrucciones o una
heurística. El control demuestra que conocer el programa no basta. La memoria tampoco
supera al historial (3/12 vs 4/12), así que el programa verificado no aporta sobre
las experiencias crudas.

**EXEC-001: mapa de aplicación.** Con el programa completo, `luna` acierta 11/12 con
2 operaciones, 7/12 con 3, 8/12 con 4 y 4/12 con 5. La **longitud mínima
equivalente** separa mejor que la nominal: 2 operaciones 18/21, 3 operaciones 8/18,
4 operaciones 4/8, 5 operaciones 0/1. La profundidad nominal no es monótona (4 supera
a 3). El único régimen aplicable es 2 operaciones; la memoria debe probarse ahí, no
en cinco pasos.

### 5.8 LIRE-001b: representación con skill larga (retractado)

La representación de una competencia conocida se midió aparte, con una skill
sintética de **120 reglas** con código, umbral y estado, en cinco formas: español,
inglés, chino, español conciso y DSL simbólico. **Doce casos**: seis cumplen el
umbral (`Sxxx`) y seis no (`NONE`). Modelo de experimentos: `gpt-6-luna` low.

| Representación | Acierto | Caracteres | Tokens (mín.) | Δ vs español |
|---|---|---|---|---|
| Español | 8/12 | 9.267 | 28.250 | — |
| Inglés | 10/12 | 9.034 | 28.100 | −0,5 % |
| Chino | **11/12** | **4.258** | 27.861 | −1,4 % |
| Español conciso | 8/12 | **3.052** | **26.534** | **−6,1 %** |
| DSL simbólico | 7/12 | 4.963 | 27.009 | −4,4 % |

**Retractación.** Cada regla era `C{i}` / umbral `{i}` / `S{i}`: una sola fórmula
reconstruye la tabla. El verificador no comprobaba la pertenencia del código y el
orden de casos no estaba aleatorizado. Las cifras describen el seguimiento de una
tabla redundante, no información retenida. **No se atribuye la diferencia al idioma.**
Ver `docs/errata-lire-001b.md`.

### 5.9 LIRE-002: información independiente y condición

Una tabla de 120 reglas con **código, umbral, estado y excepción aleatorios e
independientes** (~3.759 bits), 12 casos estratificados y un **control sin tabla**.
Siete representaciones; el coste es la diferencia pareada de tokens contra el control.

| Representación | Positivos | Secundarios | Total | Tokens incr. |
|---|---|---|---|---|
| Español | 6/7 | 4/5 | 10/12 | 2.841 |
| Inglés | **7/7** | **5/5** | **12/12** | 2.605 |
| Chino | **7/7** | 4/5 | 11/12 | **2.949** |
| Español conciso | **7/7** | 3/5 | 10/12 | **1.477** |
| DSL | **7/7** | **5/5** | **12/12** | 2.490 |
| JSON | 6/7 | 2/5 | 8/12 | 2.356 |
| Tabla TSV | 6/7 | 2/5 | 8/12 | **1.400** |
| Sin tabla | **0/7** | 5/5 | 5/12 | 0 |

El control sin tabla acierta **0/7 positivos**: responder siempre `NONE` explota la
distribución y da 5/12, pero no sabe nada. **La recuperación funciona** (6–7/7
positivos); **el fallo está en la condición**: el modelo devuelve el estado cuando el
importe no cumple el umbral, o falla la excepción. El chino no ahorra tokens (2.949
vs 2.841) ni acierta más (11 vs 10): **la ventaja de LIRE-001b no se replica**. La
tabla TSV ahorra 51 % de tokens y baja a 8/12; el conciso ahorra 48 % y se queda en
10/12. No hay una representación que domine fidelidad, tokens y condición.

### 5.10 MEM-002/MEM-003: un procedimiento correcto presentado como verificado

**MEM-002: el régimen y el historial.** En 3 operaciones, la memoria de 2 operaciones
no superó al clon ni al placebo (clon 2, memoria 3, placebo 5, historial 4, oráculo
8). En 2 operaciones, la memoria acierta 7/12 frente a 5/12 del clon y 4/12 del
placebo, pero el **historial 9/12** y el **oráculo 11/12** la superan. La memoria se
usa, pero el historial crudo es mejor y el oráculo —el mismo programa con otro
encuadre— despega. Eso motivó MEM-003.

En dos operaciones —el régimen aplicable según EXEC-001— se comparó el **mismo
programa verificado** con dos encuadres, más clon, placebo, historial y oráculo:

| Condición | Acierto |
|---|---|
| Clon | 3/12 |
| Memoria candidata | 4/12 |
| Placebo | 3/12 |
| Historial | 10/12 |
| **Memoria verificada** | **11/12** |
| **Oráculo** | **12/12** |

El mismo programa pasa de **4/12 a 11/12** al presentarlo como «retenido y
verificado; aplícalo» en vez de «subrutina candidata; verifícala» (7 pares,
p = 0,016). Con el encuadre definitivo, el contenido importa: verificada 11/12 vs
placebo 3/12 (8 pares, p = 0,008). La memoria verificada empata con el historial
(10/12) y con el oráculo (12/12). El encuadre de candidata es tóxico: 4/12, peor que
el historial (6 pares, p = 0,031). **El encuadre y la instrucción explican parte de la
diferencia; este diseño no separa cuánto corresponde al estado comunicado y cuánto a
la instrucción de aplicar.** MEM-005 hace el factorial.

**MEM-004: la etiqueta no basta.** Un programa falso etiquetado «retenido y
verificado» acierta **0/12**, peor que el clon (5/12); la memoria verificada acierta
10/12 (10 pares, p = 0,002). El modelo no verifica por sí mismo: **aplica el programa
falso y falla**. La ganancia es del contenido correcto bajo el mismo encuadre; el
placebo verificado muestra **obediencia peligrosa a la autoridad declarada**, no
seguridad. La verificación debe ser real y externa al prompt; un sistema que permita
al modelo etiquetar su propia memoria como verificada es vulnerable.

### 5.11 MEM-005: el factorial reencuadra el positivo

MEM-005 separó contenido, estado e instrucción en un factorial 2×2×2, con un control
de **programa escrito por un programador** y orden de condiciones aleatorizado por
tarea. Doce tareas, semilla 1, 2 operaciones.

| Condición | Acierto |
|---|---|
| Clon | 6/12 |
| Correcto · candidata · verificar | 8/12 |
| Correcto · candidata · aplicar | 9/12 |
| Correcto · verificada · verificar | 8/12 |
| **Correcto · verificada · aplicar** | **12/12** |
| Placebo · candidata · verificar | 6/12 |
| Placebo · candidata · aplicar | 4/12 |
| Placebo · verificada · verificar | 6/12 |
| **Placebo · verificada · aplicar** | **1/12** |
| **Escrito por un programador** | **12/12** |

El efecto grande está en **una sola celda**: contenido correcto, estado verificado e
instrucción de aplicar (12 vs 1; 11 pares, p = 0,001). En candidata+verificar el
contenido apenas separa (8 vs 6; 3/1, p = 0,625). Los efectos individuales son
direccionales, no significativos: verificado vs candidata con instrucción de aplicar,
12 vs 9 (3/0, p = 0,25); aplicar vs verificar con estado verificado, 12 vs 8 (4/0,
p = 0,125). **La interacción triple es 0,50 con bootstrap 95 % [−0,17, 1,17]**, que
incluye cero (10.000 remuestreos). El resultado bien respaldado es
**verificado+aplicar frente a su placebo**; cuánto aporta causalmente cada factor y si
la interacción se reproduce con otras habilidades sigue abierto.

**El control escrito es informativo, no una equivalencia:** un programa escrito por un
programador, sin sesión previa de aprendizaje, acierta **12/12**, igual que el
aprendido. **No hay evidencia de ventaja de adquisición en esta tarea.** Pero el
control cambia la procedencia declarada y el orden (`double → sort_asc` aprendido vs
`sort_asc → double` escrito), así que no prueba que la procedencia sea irrelevante en
general. La formulación defendible es: *entregar el procedimiento correcto como
instrucción autoritativa y aplicable mejora la ejecución local en una transformación
identificable*, no *la memoria acumulativa funciona*.

El placebo verificado+aplicar acierta **1/12**: la autoridad declarada aplicada a
contenido falso produce errores sistemáticos. Es **obediencia peligrosa**, no
verificación. El modelo no distingue por sí mismo el contenido correcto del falso.

Con esto, el «positivo» de MEM-003/004 queda reencuadrado: no demuestra adquisición ni
memoria; demuestra que la instrucción y el contenido correcto mejoran la ejecución. La
pregunta de memoria acumulativa exige **MEM-006** (varias memorias, recuperación
autónoma) y **META-001** (ciclo longitudinal), no otro formato de entrega.

---

## 6. Revisión de antecedentes

**Método.** Ocho cadenas por título en OpenAlex (2023–2026), 7.100 registros, 177
únicos cribados, 43 resúmenes evaluados, 31 incluidos, más 10 fundacionales. Bola de
nieve sobre seis semillas. Una base, un revisor, sin replicación.

**Hallazgos.** El campo tiene bibliotecas con aplicabilidad y terminación, verificación
por ejecución, benchmarks de transferencia y resultados negativos a escala. Los
nuestros coinciden: la memoria episódica no mueve el resolve rate (MemUse), las
bibliotecas degradan al crecer (−21 %), y entregar no es usar.

**Limitaciones.** 88 de los 131 candidatos no se evaluaron; las cifras son
declaradas por los autores, no replicadas; hay preprints y heterogeneidad de
unidades. El flujo está en `revision-sistematica/cribado.md`.

---

## 7. Discusión

**Por qué los negativos y qué cambió.** Los seis experimentos negativos viven en el
mismo régimen: un espacio que cabe en el presupuesto, con tareas mayormente
identificables. La proposición **explica retrospectivamente** por qué ahí la memoria
solo puede optimizar coste. No fue una predicción registrada: el 006 incluye
políticas, probes y costes que no satisfacen todas las premisas. Y eso es lo que
se observó: 41,8 % menos pasos con continuidad total, nada con continuidad cero.

El 007 añadió dos causas que no eran la memoria: la tarea de cinco pasos estaba fuera
de la **aplicación** (oráculo 2/12) y el artefacto se presentaba como **candidato** a
re-verificar. EXEC-001 midió la primera; MEM-003/004, la segunda. Cuando se
corrigieron las dos, en dos operaciones, un procedimiento correcto presentado como
verificado se usó (10–11/12). El negativo no era una ley sobre la memoria: era un
artefacto de régimen y de encuadre.

**Qué sobrevive.** (i) La ventaja de eficiencia es real pero condicional. (ii) La
política de activación no paga su señal. (iii) La verificación por ejecución es
imprescindible y ajena. (iv) El agente real acierta 46,9 %; el piloto no permite
atribuir el fallo a una capacidad concreta.

**Sobre la innovación.** No hay innovación algorítmica demostrada. La contribución
posible es una medición: clon, canales, `E`/`K`/`P`, formas y verificación en cinco
etapas. Si esa medición no distingue nada, tampoco habrá contribución.

**Lo que 007 enseña.** La retención funcionó —el artefacto sobrevivió al reinicio—
pero no bastó. El 007B mostró por qué: **con el programa completo, `luna` acierta
2/12**. El cuello está en la **aplicación** de composiciones de cinco pasos, no en la
memoria; no se identifica si falla la ejecución, la interpretación de las operaciones
o el seguimiento de instrucciones. El artefacto verificado no supera al historial ni
al placebo, y el oráculo está en el suelo. Para medir acumulación hace falta primero
una tarea que el modelo pueda aplicar; después, una donde el clon no pueda
identificar el procedimiento.

**Lo que MEM-003 añade.** En 2 operaciones —el régimen aplicable— el mismo programa
verificado acierta **11/12** si se presenta como definitivo, frente a 3/12 del clon,
3/12 del placebo y 4/12 si se presenta como candidata. Empata con el historial
(10/12) y con el oráculo (12/12). **El 007 no era evidencia contra la memoria:** la
tarea estaba fuera de la ejecución y el artefacto se presentaba como candidato. Pero
las doce tareas ya están determinadas por los dos ejemplos: el artefacto entrega el
programa explícito, no un hecho que el clon no pudiera saber.

**Lo que MEM-004 añade.** La etiqueta «verificado» no basta: un programa falso
etiquetado así acierta 0/12, mientras la memoria verificada acierta 10/12 (10 pares,
p = 0,002). El modelo no verifica por sí mismo: aplica el programa falso y falla. La
memoria útil exige **verificación real fuera del prompt** y un encuadre definitivo; el
modelo no puede ser el verificador de su propia memoria. El placebo verificado es
**obediencia peligrosa**, no seguridad.

**Lo que MEM-005 añade.** El factorial 2×2×2 muestra que el efecto grande está en una
sola celda: contenido correcto, estado verificado e instrucción de aplicar (12 vs 1;
11 pares, p = 0,001). En candidata+verificar el contenido apenas separa (8 vs 6). Los
efectos individuales son direccionales, no significativos. Y el control decisivo: un
**programa escrito por un programador, sin aprendizaje previo, acierta 12/12**, igual
que el aprendido. **No hay evidencia de ventaja de adquisición en esta tarea**; el
control cambia procedencia y orden, así que no es una equivalencia. El positivo es
contenido correcto más instrucción definitiva, no memoria.

**Qué es y qué no es el resultado positivo.** Es **uso de un procedimiento correcto
presentado como verificado**: el artefacto contiene el programa que el clon tendría
que inferir, el modelo puede aplicarlo y el encuadre definitivo hace que lo aplique.
**No es memoria de un hecho desconocido**: las doce tareas ya están determinadas por
los dos ejemplos; el clon tiene la información. **No es adquisición**: el programa
escrito por un programador rinde igual; no hay ventaja del proceso de aprendizaje.
**No es expansión de competencia**: la tarea es enumerable e identificable; el
artefacto ahorra el coste de identificarla. **No es transferencia**: las tareas
empiezan por el motivo aprendido. **No es general**: n=12, una semilla, un modelo; la
réplica de 24 tareas está pendiente. La proposición de `teoria.md` sigue siendo el
marco: en el espacio enumerable, la memoria optimiza coste; el resultado positivo es
consistente con ella, no la refuta.

**El siguiente test.** **MEM-006**: varias memorias, recuperación autónoma y selección
entre candidatos, sin que el evaluador entregue el artefacto. **META-001**: ciclo
longitudinal con familias nuevas, menos experiencias para el umbral, artefactos
obsoletos y contradictorios. Después, la réplica de **24 tareas y varias semillas**, la
**familia reservada**, la **comunicación aprendida** (COMM-001) y el baseline externo
(F0), que sigue pendiente y es condición para cualquier comparación general.

---

## 8. Limitaciones

1. **Un solo entorno sintético** de seis operaciones; no es un benchmark de LLM.
2. **Un solo modelo** (`gpt-6-luna`), un esfuerzo (`low`) y una semilla. Las corridas
   con `gpt-6.1-terra` son exploratorias y no se usan como evidencia.
3. **n=12 por condición** en LIRE-002, EXEC-001 y MEM. La réplica de 24 tareas está
   pre-registrada y pendiente (M11/M12); los intervalos no están ajustados por
   comparaciones múltiples.
4. **Las tareas empiezan por el motivo** aprendido: reutilización favorable, no
   transferencia a una familia reservada.
5. **La etiqueta «verificado» es una frase del prompt** en el experimento. Un sistema
   real necesita verificación externa; el placebo verificado (0/12) muestra el riesgo
   de una etiqueta no respaldada.
6. **El historial tiene más tokens** que la memoria verificada (853 vs 370); no se
   iguala longitud.
7. **LIRE-002**: idioma, longitud, redundancia y estructura siguen confundidos; no es
   un factorial; LLMLingua-2 no se ejecutó. La instrucción de `NONE` se añadió tras el
   piloto; el piloto se conserva como ablación, no como evidencia principal.
8. **EXEC-001**: solo se ejecutó la condición simbólica; `steps` y `nl` están
   pendientes. La longitud mínima se calcula sobre 60 sondas; no es una prueba formal
   de equivalencia.
9. **Sin baseline externo reproducido**, sin `ACTUAL-RETRIEVAL` y sin ciclo
   longitudinal `E`/`K`/`P`.
10. **Los negativos del 006** conservan sus límites: el presupuesto puede rebasarse
    hasta 6 pasos, los IC tratan tareas como independientes con dos semillas y la
    condición de herramienta no verificó las cinco etapas.
11. **LIRE-001b está retractado**: sus cifras describen una tabla redundante y no se
    usan como evidencia de información retenida.
12. **El mecanismo del fallo del 007B no está identificado**: puede ser ejecución,
    interpretación de las operaciones, seguimiento de instrucciones o una heurística.
13. **La revisión de literatura** se hizo con una base y un revisor; 88 candidatos no
    se evaluaron y la mayoría de los trabajos son preprints de 2026.
14. **Las tareas de MEM son identificables desde los dos ejemplos**: el clon tiene la
    información; el artefacto entrega el programa explícito. El resultado mide
    **inferir frente a recibir**, no un hecho que solo estuviera en la experiencia.
15. **MEM-002/003/004 usan las mismas 12 tareas y la misma semilla**: no son réplicas
    independientes; la réplica de 24 tareas y varias semillas está pendiente.
16. **El contraste candidata/verificada cambió dos variables** (estado comunicado e
    instrucción operativa); MEM-005 las separa en un factorial 2×2×2.
17. **No hay recuperación autónoma**: el evaluador entrega el artefacto; no hay
    selección entre varias memorias ni decisión de cuándo recordar.
18. **MEM-004 vs clon no alcanza p < 0,05** (p = 0,0625); los valores p no corrigen
    por comparaciones múltiples y el orden de condiciones era fijo en MEM-002/003/004.
    MEM-005 aleatoriza el orden por tarea.
19. **La interacción triple de MEM-005 no está establecida**: 0,50 con bootstrap 95 %
    [−0,17, 1,17], que incluye cero. El resultado bien respaldado es
    verificado+aplicar frente a su placebo.
20. **La manipulación textual mezcla factores**: autoridad declarada, completitud
    sugerida («el programa completo puede tener más pasos») e instrucción operativa.
    Con `suffix=0` el programa no está incompleto, así que la sugerencia es un
    confundidor.
21. **MEM-005 no es pre-registro independiente**: protocolo, código, resultados y
    análisis entraron en el mismo commit. MEM-006 se pre-registrará con hash antes de
    la corrida.
22. **No hay coste total**: no se guardaron tokens por condición y la adquisición se
    ejecuta antes de todas las condiciones. Falta el beneficio neto
    `N·(C_sin − C_con) − C_adq − C_ver − C_mant`.

---

## 9. Reproducibilidad

```bash
python -m unittest discover -s tests -v          # 87 tests
python docs/verificar_afirmaciones.py            # 100 claims y totales citados

# Experimentos clave (modelo de experimentos: gpt-6-luna low)
python -m ohmem.lire_002 --model gpt-6-luna --effort low --timeout 120 \
  --out resources/investigation/lire-002/results/luna-low-12cases.json
python resources/investigation/lire-002/analyze.py

python -m ohmem.v7_transfer --n 12 --support 2 --suffix 0 \
  --session1-examples 12 --exact-ops \
  --conditions clone,memory,memory_verified,placebo,placebo_verified,history,oracle \
  --model gpt-6-luna --effort low --timeout 120 \
  --out resources/investigation/mem-004/results/pilot-depth2-verified-placebo.json
python resources/investigation/mem-004/analyze.py
```

Los protocolos congelados del 004-A y el 006-A verifican hashes SHA-256 y abortan si
el código cambió. Los resultados crudos están en `results/` de cada prototipo, con las
filas por condición y tarea. El registro de ejecuciones (modelo, esfuerzo, semillas,
comandos y número de llamadas) está en `docs/registro-de-ejecuciones.md`; la tabla de
trazabilidad, en `docs/para-revisores.md` §5.3. La retractación de LIRE-001b está en
`docs/errata-lire-001b.md`.

---

## 10. Conclusión

En nuestras tareas, la memoria no falla principalmente por almacenar poco: falla por
**aplicar mal, verificar mal y presentar mal** lo almacenado. En nuestras tareas
enumerables, la memoria solo puede reducir coste; el 007 pedía cinco operaciones, que
el modelo no aplica ni con el programa completo (oráculo 2/12), y presentaba el
artefacto como candidato a re-verificar. Corregidos el régimen (dos operaciones
efectivas) y el encuadre (procedimiento correcto presentado como verificado y
aplicable), la ejecución mejora: 10–11/12 frente a 3–5/12 del clon y 2–3/12 del
placebo. Pero **MEM-005 muestra que un programa escrito por un programador, sin
aprendizaje previo, acierta 12/12**, igual que el aprendido: no hay evidencia de
ventaja de adquisición en esta tarea, y el control cambia procedencia y orden. El
«positivo» es **contenido correcto más instrucción definitiva**,
no memoria acumulativa. Un placebo etiquetado como verificado acierta 0–1/12: la
etiqueta no basta y puede inducir errores sistemáticos.

El problema del lenguaje es el mismo problema visto desde el otro lado: no se trata de
qué idioma ocupa menos caracteres, sino de cuánta información independiente se
conserva y se aplica bajo una condición. Con información independiente, el control sin
tabla acierta 0/7; la recuperación funciona, pero falla la condición; el chino no
ahorra tokens ni acierta más. La compresión ahorra tokens y cuesta excepciones.

No hay evidencia de **expansión de competencia** ni de **adquisición acumulativa**. El
resultado positivo es **uso de un procedimiento correcto en un espacio enumerable**:
ahorra identificación, no amplía lo expresable, y no requiere que el procedimiento
haya sido aprendido. La pregunta mayor sigue abierta y exige una tarea que el modelo
pueda aplicar, que no quepa en el presupuesto, y un recuperador que elija entre varias
memorias sin que el evaluador le entregue la respuesta. Ese es el trabajo siguiente;
este artículo deja el instrumento para medirlo sin engañarse.

---

## 11. Referencias

- Angluin, D. (1987). Learning regular sets from queries and counterexamples. *Information and Computation*, 75(2), 87–106.
- Bowers, M., et al. (2023). Top-down synthesis for library learning. *POPL 2023*.
- Cheng, Z., et al. (2026). Mem²Evolve: Towards self-evolving agents via co-evolutionary capability expansion and experience distillation. *ACL 2026*, 20784–20831.
- Ellis, K., et al. (2021). DreamCoder: Bootstrapping inductive program synthesis with wake-sleep library learning. *PLDI 2021*.
- Finn, C., Abbeel, P., & Levine, S. (2017). Model-agnostic meta-learning for fast adaptation of deep networks. *ICML 2017*.
- Grand, G., et al. (2024). LILO: Learning interpretable libraries by compressing and documenting code. *ICLR 2024*.
- Koenig, S., Likhachev, M., & Furcy, D. (2004). Lifelong planning A*. *Artificial Intelligence*, 155(1–2), 93–146.
- Page, M. J., et al. (2021). The PRISMA 2020 statement. *BMJ*, 372, n71.
- Russell, S., & Wefald, E. (1991). Principles of metareasoning. *Artificial Intelligence*, 49(1–3), 361–395.
- Sutton, R. S., Precup, D., & Singh, S. (1999). Between MDPs and semi-MDPs. *Artificial Intelligence*, 112(1–2), 181–211.
- Tishby, N., Pereira, F. C., & Bialek, W. (1999). The information bottleneck method. *Allerton 1999*.
- **MemDev-Bench** (2026). arXiv:2610.27524.
- **VibeMemBench** (2026). arXiv:2609.23570.
- **SkillsBench** (2026). arXiv:2602.12670 (v1.1: 87 tareas, 8 dominios, +16,6 pp).
- **ContinualSkillBench** (2026). arXiv:2608.03874.
- **SkillLearnBench** (2026). arXiv:2604.20087.
- **MemCalib** (2026). arXiv:2609.24259.
- **MemUse** (2026). arXiv:2611.01718.
- **EvoAgentBench** (2026). EMNLP Findings.
- **SelfImprove-Bench** (2026). arXiv:2611.02797.
- **Skill Following** (2026). EMNLP Findings.
- **Proof-Gated Skill Compilation** (2026). NeurIPS 2026 CL4FMAgents workshop.
- **More Skills, Worse Agents?** (2026). arXiv:2605.24050.
- **Contextual Agentic Memory is a Memo** (2026). arXiv:2604.27707.
- **SkillEvoReg** (2026). arXiv:2609.30861.
- **RSE-Bench** (2026). arXiv:2610.19910.
- **Skill Drift** (2026). arXiv:2605.10990.
- **Bemula** (2026). arXiv:2610.18052.
- **STRATUM** (2026). Zenodo 23615179.
- **MemEvoBench** (2026). arXiv:2604.15774.
- **AgentCL** (2026). arXiv:2606.02461.
- **SWE-Bench-CL** (2025). arXiv:2507.00014.

---

## Apéndice A. Registro de afirmaciones

100 afirmaciones en `docs/registro-de-afirmaciones.md`: 65 sostenidas (60 propias; 5 de
terceros, no replicadas), 18 refutadas, 17 abiertas, inválidas o no demostradas.
Ninguna propia alcanza E3.

## Apéndice B. Qué se retiró

- «La memoria amplía la capacidad del agente» (004).
- «La política aprendida supera a la regla fija» (006-A′).
- «La memoria recuperada ayuda a un LLM» (oráculo, no recuperación).
- «El intérprete no ayuda» (condición inválida).
- «96 episodios no caben en una ventana» (no se midió).
- «JANUS es novedoso» (la verificación operacional ya existe).
- «El procedimiento retenido ayuda en cinco pasos» (007: empata con un placebo falso).
- «El chino conserva mejor una skill larga» (LIRE-001b: tabla redundante; LIRE-002 no
  replica la ventaja).
- «La compresión ahorra tokens y conserva la fidelidad» (LIRE-002: la tabla TSV ahorra
  51 % y pierde condiciones).
- «El cuello es la ejecución» (007B: se suaviza a «la aplicación del programa»; el
  mecanismo no está identificado).
- «La memoria no funciona tras el reinicio» (007: era un artefacto de régimen de cinco
  pasos y de encuadre de candidata; MEM-003/004).
- «La etiqueta “verificado” basta» (MEM-004: un placebo verificado acierta 0/12).




