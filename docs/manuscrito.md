# Memoria y competencia en agentes: seis experimentos, un resultado negativo y un instrumento

**Autor:** Juan David Salas Camargo (MIT)
**Colaboración:** DeepSeek 4.1 Flash (agente de investigación)
**Fecha:** 16 de noviembre de 2026
**Estado:** preprint no arbitrado. Listo para revisión por pares.
**Repositorio:** https://github.com/jdsalasca/open-human-memory
**Versión:** `v1.14-review`

---

## Resumen

Los agentes basados en modelos de lenguaje están limitados por el contexto y por la
dificultad de conservar competencia entre sesiones. La literatura reciente propone
bibliotecas de habilidades, memoria episódica, verificación por ejecución y
benchmarks de aprendizaje continuo. Este trabajo no propone un mecanismo nuevo:
pone a prueba la hipótesis de que la experiencia acumulada expande la competencia
de un agente y documenta por qué esa hipótesis no se sostiene en el régimen
experimental habitual.

Presentamos seis experimentos con un solucionador de programas sobre cuatro
operaciones. El resultado central es negativo: en un espacio **explorable,
identificable y dentro del presupuesto**, la búsqueda sin memoria iguala la
cobertura de una biblioteca aprendida; la biblioteca solo reduce coste (41,8 % menos
pasos con continuidad total) y lo pierde todo con continuidad cero (22,1 pp menos).
Una política aprendida de activación no supera a una regla de una línea y cuesta
1,9× más. Un agente real (`gpt-6-luna`, esfuerzo bajo) acierta 46,9 % en la misma
rejilla; las intervenciones probadas no permiten atribuir el fallo a la memoria.

La contribución es doble: (i) una **proposición** que explica por qué los negativos
estaban cantados —enumerar candidatos no garantiza cobertura si hay ambigüedad o si
el presupuesto no alcanza— y seis predicciones falsables para salir de ese régimen;
(ii) un **instrumento** de medición con clon, canales separados, coste total y
verificación de herramientas en cinco etapas. Una revisión estructurada de 31
trabajos sitúa el resultado: el campo ya tiene los mecanismos, pero no una medición
longitudinal que los separe.

**Palabras clave:** memoria de agentes, competencia acumulativa, aprendizaje de
bibliotecas, metacognición, resultados negativos.

---

## Abstract

LLM agents are constrained by context and by the difficulty of preserving competence
across sessions. Recent work proposes skill libraries, episodic memory,
execution-based verification and continual-learning benchmarks. This paper does not
propose a new mechanism: it tests whether accumulated experience expands agent
competence and documents why that hypothesis fails in the usual experimental regime.

We report six experiments with a program solver over four operations. The central
result is negative: in an **explorable, identifiable, budgeted** space, memoryless
search matches the coverage of a learned library; the library only reduces cost
(41.8% fewer steps at full continuity) and loses it all at zero continuity (22.1 pp
less). A learned activation policy does not beat a one-line rule and costs 1.9×
more. A real agent (`gpt-6-luna`, low effort) scores 46.9% on the same grid;
the interventions tested do not attribute the failure to memory.

The contribution is twofold: (i) a **proposition** explaining why the negatives were
predictable —enumerating candidates does not guarantee coverage under ambiguity or
budget— plus six falsifiable predictions to leave that regime; (ii) a **measurement
instrument** with a clone, separated channels, total cost and five-stage tool
verification. A structured review of 31 works locates the result: the field has the
mechanisms, but not a longitudinal measurement that separates them.

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

La respuesta que podemos sostener hoy es: **en nuestro entorno, ninguno**. Lo que sí
podemos sostener es por qué, y qué haría falta para que la respuesta cambie.

### Contribuciones

1. **Una proposición con condiciones.** En un espacio explorable, identificable y
   dentro del presupuesto, la memoria no puede ampliar cobertura; solo reordenar
   coste. Los negativos de los seis experimentos son consecuencias, no sorpresas.
2. **Seis experimentos documentados**, con protocolos congelados, resultados crudos
   y contabilidad de coste. Cinco son negativos o condicionales.
3. **Una revisión estructurada de 31 trabajos** que sitúa el proyecto frente a
   DreamCoder, Stitch, LILO, CEGIS, Mem²Evolve, EvoAgentBench, MemDev-Bench, MemUse
   y Proof-Gated, entre otros.
4. **Un instrumento**: clon sin historial, canales separados, métricas `E`/`K`/`P`,
   muestras por clase conductual y verificación de herramientas en cinco etapas.
5. **Un registro público de 44 afirmaciones** con estado, nivel de evidencia y
   falsador.

### Lo que no se afirma

- No se afirma que la memoria no sirva a los agentes.
- No se afirma que las habilidades no funcionen.
- No se afirma novedad algorítmica: ninguna pieza es nueva.
- No se afirma transferencia entre modelos ni aprendizaje conceptual.

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
profundidad a dos, no una capacidad del agente. (ii) Los negativos de 004–006 son
predicciones de la teoría en el régimen identificable y presupuestado; fuera de él,
la teoría no dice nada y no puede cerrar la línea. (iii) Para probar expansión hacen
falta un espacio que no quepa en `B` **y** ambigüedad que la búsqueda no resuelva.

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
manuscrito usó `gpt-6-luna` con esfuerzo `max`; `gpt-6-terra` no está disponible para
cuentas ChatGPT.

---

## 5. Resultados

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

### 5.6 Prototipo 006-B: el agente real

`gpt-6-luna` low acierta **30/64 (46,9 %)**. En 24 tareas pareadas: más ejemplos
+8,3 pp (IC −20,8 a +33,3), vocabulario +4,2 pp (IC −12,5 a +25,0), `ORACLE-MEMORY`
+8,3 pp (IC −12,5 a +33,3), herramienta exigida 0,0 pp (IC −29,2 a +29,2, condición
inválida). Ninguna intervención se distingue de cero.

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

**Por qué todos los negativos.** Los seis experimentos viven en el mismo régimen: un
espacio que cabe en el presupuesto, con tareas mayormente identificables. La
proposición predice que ahí la memoria solo puede optimizar coste. Y eso es lo que
se observó: 41,8 % menos pasos con continuidad total, nada con continuidad cero.

**Qué sobrevive.** (i) La ventaja de eficiencia es real pero condicional. (ii) La
política de activación no paga su señal. (iii) La verificación por ejecución es
imprescindible y ajena. (iv) El agente real falla por identificación, pero el piloto
no lo demuestra.

**Sobre la innovación.** No hay innovación algorítmica demostrada. La contribución
posible es una medición: clon, canales, `E`/`K`/`P`, formas y verificación en cinco
etapas. Si esa medición no distingue nada, tampoco habrá contribución.

**El siguiente test.** P1 (expansión en espacio no explorable) y P6 (selección de
forma). Antes, F1: descomponer las siete capacidades. Sin eso, cualquier resultado de
memoria es ambiguo.

---

## 8. Limitaciones

1. **Un solo entorno sintético**, cuatro operaciones, 14 clases conductuales.
2. **Un solo modelo** (`gpt-6-luna`), un esfuerzo (`low`), una corrida.
3. **n=24** en el diagnóstico: los IC son de ±20 pp.
4. **Sin replicación** de ningún competidor.
5. **Revisión con una base y un revisor**; 88 candidatos sin evaluar.
6. **Preprints** en la mayoría de 2026.
7. **Sin medición de tokens** en los experimentos sintéticos.
8. **La condición de herramienta** no verificó las cinco etapas.

---

## 9. Reproducibilidad

```bash
python -m unittest discover -s tests -v          # 60 tests
python resources/investigation/prototipo-004-validez/reproduce.py
python resources/investigation/prototipo-005-presupuesto/reproduce.py
python resources/investigation/prototipo-006-politica/reproduce_corrected.py
python resources/investigation/prototipo-006-agente-llm/analyze.py
```

Los protocolos congelados verifican sus hashes y abortan si el código cambió. Los
resultados crudos están en `results/` de cada prototipo. El registro de ejecuciones
(modelo, esfuerzo, semillas, comandos) está en `docs/registro-de-ejecuciones.md`.

---

## 10. Referencias

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

44 filas en `docs/registro-de-afirmaciones.md`: 29 sostenidas (5 de terceros, no
replicadas), 8 refutadas, 7 abiertas o inválidas. Ninguna propia alcanza E3.

## Apéndice B. Qué se retiró

- «La memoria amplía la capacidad del agente» (004).
- «La política aprendida supera a la regla fija» (006-A′).
- «La memoria recuperada ayuda a un LLM» (oráculo, no recuperación).
- «El intérprete no ayuda» (condición inválida).
- «96 episodios no caben en una ventana» (no se midió).
- «JANUS es novedoso» (la verificación operacional ya existe).
