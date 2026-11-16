# Revisión estructurada de antecedentes

**Fecha:** 16 de noviembre de 2026
**Pregunta:** ¿qué se ha demostrado sobre convertir experiencia en competencia
reutilizable en agentes LLM, y qué queda realmente abierto?
**Alcance:** 31 trabajos de agentes (2023–2026) + 10 fundacionales.
**Método:** `busquedas.md`, `cribado.md`, `extraccion.md`.
**Advertencia:** una base (OpenAlex), un revisor, muestreo por relevancia y bola de
nieve. No es exhaustiva y no lo pretende.

---

## 1. Siete hallazgos

### H1. La biblioteca de skills ya existe, y es más rica que nuestras macros

El estado del arte no son «procedimientos reutilizables»: son **skills con
condiciones de aplicabilidad, políticas de ejecución, criterios de terminación e
interfaces** (SoK, 2026). Se generan desde trayectorias (Trace2Skill, EMNLP 2026;
SkillGen, 2026), se mantienen como ecosistemas (SkillOps) y se comprimen para
token efficiency (SkillReducer).

Nuestra macro de dos pasos es una versión de juguete de esa idea, sin condiciones
de aplicabilidad ni terminación. El Prototipo 003 no descubrió nada que el campo no
tuviera; lo redescubrió en un universo de cuatro operadores.

### H2. La verificación independiente no es una idea nuestra, y ya demostró que es imprescindible

**Proof-Gated Skill Compilation** (NeurIPS 2026 workshop) implementa la parte
**operacional** de lo que JANUS proponía: que solo persistan programas ejecutados
por el harness contra ground truth. Su resultado es contundente: de **538 aserciones
de verificación** hechas por modelos teacher, la ejecución independiente confirmó
**52** y rechazó **486 fabricaciones**. En un benchmark de 90 tareas derivadas de
ARC-AGI-2, la biblioteca verificada alcanza **98,9 %**.

Eso **no** significa que JANUS esté resuelto: verificar que una herramienta pasa
pruebas es corrección operacional; identificar causalmente por qué una intervención
produce un resultado es otro problema. Lo que queda refutado es la **novedad de la
verificación**; la parte causal de JANUS sigue sin compararse con la literatura de
identificación causal y evaluación contrafactual.

### H3. El valor de la memoria es condicional, y el campo tiene los mismos negativos

- **MemDev-Bench** (2026): la memoria mejora localización y edición, y **también
  causa fallos en tareas que antes eran resolubles** (555 base + 4.869 históricas).
- **More Skills, Worse Agents?** (2026): la biblioteca degrada al crecer, **hasta
  −21 %** al pasar a 202 skills (*skill shadowing*).
- **MemUse** (2026): en 8.000 episodios de SWE-bench Verified, las tasas de
  resolución quedan **a ±0,4 pp del baseline sin memoria**; la mayoría de entregas
  son irrelevantes y la mayoría de las relevantes no se usan. **23,2 % de los
  episodios con uso beneficioso igual fallaron.**
- **ContinualSkillBench** (2026): conservar contexto y feedback rinde **casi igual**
  que mantener una biblioteca explícita.

Nuestros negativos locales (004, 005, 006) no eran anomalías: son el mismo patrón
que el campo reporta con más escala.

### H4. La medición de transferencia ya está formalizada

- **EvoAgentBench** (EMNLP Findings 2026) mide transferencia de **procedimientos**
  en cuatro dominios, con *ability graphs* y cada tarea de test respaldada por
  entrenamiento verificado.
- **SelfImprove-Bench** (2026) separa **ganancia de capacidad** de **ajuste al
  escenario** en tareas no vistas.
- **AgentCL** (2026) exige dependencias cross-task en los streams.
- **SWE-Bench-CL** (2025) usa secuencias cronológicas para medir olvido.

Nuestro «test de clon» no es original. Es una forma mínima de lo que estos
benchmarks ya exigen. La contribución no puede ser el test; puede ser **aplicarlo
con separación de canales y coste total**.

### H5. El coste del contexto ya está medido, y no con nuestras intuiciones

**STRATUM** (2026) hace el censo que nos faltaba: **~4 GB de texto frente a ~298 TB
de estado KV fp16** por 1e9 tokens en un modelo de 70B; la mediana de un fix toca
**dos archivos**; el cierre de imports es **2,7–9,9 %** del repositorio.

Nuestra frase «96 episodios no caben en una ventana» era una intuición sin número.
El número real no trata de 96 episodios sintéticos: trata de la diferencia entre
texto indexado y estado KV.

### H6. La memoria puede envenenarse, derivar y necesitar olvido

- **RSE-Bench** (2026): el ruido no adversarial durante el aprendizaje **persiste**
  en las reglas.
- **MemEvoBench** (2026): 7 dominios y 36 tipos de riesgo de *misevolución*.
- **Skill Drift** (2026): las skills decaen cuando cambian APIs y dependencias;
  propone contratos ejecutables.
- **Bemula** (2026): benchmark de olvido a petición (50 diálogos, 135 peticiones).

Nuestro JANUS apuntaba a la confianza; el campo ya mide el daño y el olvido.

### H7. El hueco real es estrecho, y es de integración, no de mecanismo

Ninguno de los 31 trabajos reporta, a la vez:

1. `E(F)` — experiencias hasta competencia — en **familias estructurales
   reservadas**;
2. comparación contra **clon** con el mismo modelo y presupuesto;
3. separación de **canales** (información, representación, política, herramientas,
   parámetros);
4. **coste total** (adquisición, verificación, recuperación, mantenimiento);
5. **deriva** y retirada;
6. verificación de herramientas en **cinco etapas**.

EvoAgentBench y SelfImprove-Bench cubren partes de 1 y 2. MemDev-Bench cubre 5 y 6
parcialmente. STRATUM cubre 4. **La integración no está hecha.** Eso es lo único
defendible, y es una contribución de medición, no de arquitectura.

---

## 2. Contradicciones que la revisión deja abiertas

| Contradicción | Evidencia a favor | Evidencia en contra | Cómo se resuelve |
|---|---|---|---|
| ¿Las skills ayudan? | SkillsBench: +16,6 pp curadas | ContinualSkillBench: biblioteca ≈ contexto+feedback; MemUse: ±0,4 pp | Depende del régimen: skills curadas y reutilizables vs memoria episódica |
| ¿Las skills autocreadas sirven? | MUSE: superan a humanas en el subconjunto cubierto | SkillLearnBench: ningún método gana en todo; SkillsBench: autogeneradas sin beneficio medio | La verificación independiente separa los casos |
| ¿Se puede confiar en el modelo? | MUSE: skills autocreadas buenas | Proof-Gated: 486/538 aserciones de verificación falsas | No se confía; se ejecuta |
| ¿Más skills es mejor? | SkillsBench: ≤3 módulos mejor | More Skills: −21 % a 202 skills | El tamaño importa; la recuperación también |

---

## 3. Lo que ya está resuelto y no debemos repetir

- Descubrir que las macros reducen búsqueda en un universo enumerable.
- Proponer verificación de skills: existe y funciona (Proof-Gated).
- Proponer skills con aplicabilidad y terminación: existe (SoK, options).
- Medir retrieval vs no retrieval en agregado: está criticado (Skill Following, RAE).
- Medir memoria con resolve rate agregado: está criticado (MemUse).
- Decir que el contexto es caro: está medido (STRATUM).

---

## 4. Lo que sigue abierto

1. **`E(F)` con clon y familias estructurales reservadas.** EvoAgentBench y
   SelfImprove-Bench se acercan; ninguno reporta el coste de adquisición por familia.
2. **Separación de canales.** Nadie descompone información / representación /
   política / herramientas / parámetros en el mismo experimento.
3. **Portabilidad entre modelos.** VibeMemBench transfiere experiencia verificada a
   5 solvers; Mem²Evolve no mide cambio de modelo. Sigue abierto.
4. **Coste total con mantenimiento.** STRATUM mide representación; nadie suma
   adquisición + verificación + recuperación + mantenimiento + corrección.
5. **Deriva con retirada medida.** Skill Drift y MemEvoBench miden el fallo; no
   miden la recuperación de competencia tras retirar el artefacto obsoleto.

---

## 5. Implicaciones para Open Human Memory

### Se cierra

- La biblioteca de macros como línea: es una versión de juguete de algo ya
  superado.
- La política de activación como contribución: medida y negativa, y el campo tiene
  mejores mecanismos de recuperación.
- La **verificación operacional** como idea novedosa: Proof-Gated ya la implementó.
  La pretensión **causal** de JANUS sigue abierta y sin comparación.
- La frase «no cabe en la ventana»: sustituida por las estimaciones de STRATUM.

### Se conserva

- El **test de clon** como control mínimo.
- Las métricas **`E`, `K`, `P` separadas**.
- Las **familias estructurales reservadas**.
- La **verificación por ejecución** (ahora sabiendo que no es nuestra).
- La **contabilidad de coste total**.

### Se hace

1. **F0.1** Reproducir una línea base: SkillGen o Proof-Gated (código disponible)
   sobre su benchmark. Criterio: mismo orden de magnitud, no el mismo número.
2. **F1** Descomposición de las siete capacidades, muestra equilibrada.
3. **F2** `ACTUAL-RETRIEVAL` vs `ORACLE-MEMORY` vs clon.
4. **F3** Universo no enumerable (P1).
5. **F4** Currículo interdependiente con `E(F)`.

---

## 6. Límites de esta revisión

- **Una base.** OpenAlex. Sin Scopus, WoS ni ACM DL.
- **Un revisor.** Sin doble cribado ni cálculo de concordancia.
- **Muestreo por relevancia.** 177 títulos, no 7.100. **88 de los 131 candidatos no
  se evaluaron**; el hueco está declarado en `cribado.md`.
- **Resúmenes, no textos completos.** Las cifras son las **declaradas por los
  autores**, no verificadas documentalmente ni replicadas. Solo SkillsBench,
  Mem²Evolve y Proof-Gated se contrastaron con su página primaria.
- **Preprints.** La mayoría de 2026 no está revisada por pares.
- **Sin meta-análisis.** Los estudios miden unidades distintas (skills curadas,
  memoria episódica, flujos con biblioteca) y no se comparan directamente. Un
  resultado positivo en uno no refuta un negativo en otro.
- **Sin replicación.** Ningún resultado se reprodujo ejecutando el protocolo ajeno.

Sirve para saber qué existe, qué se ha demostrado y qué no; no para afirmar que
algo no existe.
