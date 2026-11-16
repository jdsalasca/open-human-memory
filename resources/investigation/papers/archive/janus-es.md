# JANUS: la memoria de lo que no pasó

### Consolidación contrafactual para agentes que aprenden de la experiencia

**DeepSeek 4.1 Flash** — Modelo de lenguaje  
**Juan David Salas Camargo** — Massachusetts Institute of Technology (MIT)

*Documento de trabajo · v0.1 · noviembre de 2026 · no arbitrado*

> **Revisión mayor (v0.2).** Esta v0.1 afirmaba que la memoria contrafactual era
> casi inexplorada. Es falso: COUNTERMEM, ConMem, MemCon y otros trabajos de 2026
> ya la estudian. Ver [`janus-v0.2.md`](janus-v0.2.md) para la novedad estrechada,
> la identificabilidad declarada y el experimento diferencial A–E.

---

## Resumen

La memoria agéntica ha aprendido a recordar hechos, episodios y habilidades. No
ha aprendido a recordar **lo que no pasó**. Un agente que solo guarda la
trayectoria elegida no puede distinguir si su procedimiento causó el éxito o si
el éxito ocurrió de todos modos; consolida supersticiones con la misma eficiencia
con que consolida conocimiento. Este trabajo propone JANUS, una capa de memoria
contrafactual: cada decisión se registra con sus alternativas, predicciones y
resultados observados; la consolidación estima el efecto causal de las acciones,
jerarquiza la evidencia (experimento aleatorio > experimento natural >
simulación > juicio del modelo) y solo promueve procedimientos cuyo efecto es
identificable y transportable. La memoria deja de ser un archivo de éxitos y se
convierte en un **libro de arrepentimientos y causalidad**. Se formulan siete
hipótesis falsables, un benchmark con verdad causal conocida y criterios de
muerte. La contribución no es un modelo más grande: es una arquitectura para
aprender la lección correcta.

**Palabras clave:** memoria contrafactual, inferencia causal, asignación de
crédito, aprendizaje de agentes, consolidación, arrepentimiento.

## Abstract

Agentic memory has learned to store facts, episodes, and skills. It has not
learned to store **what did not happen**. An agent that only records the chosen
trajectory cannot tell whether its procedure caused success or whether success
would have occurred anyway; it consolidates superstition as efficiently as
knowledge. We propose JANUS, a counterfactual memory layer: every decision is
recorded with alternatives, predictions, and observed outcomes; consolidation
estimates causal effects, ranks evidence (randomized > natural experiment >
simulation > model judgment), and promotes only procedures whose effect is
identifiable and transportable. Memory becomes a ledger of regret and causality
rather than an archive of successes. We state seven falsifiable hypotheses, a
benchmark with known causal ground truth, and kill criteria. The contribution is
not a larger model: it is an architecture for learning the right lesson.

**Keywords:** counterfactual memory, causal inference, credit assignment, agent
learning, consolidation, regret.

---

## 1. Introducción: la memoria que solo recuerda lo que pasó

Imaginemos un agente que arregla un test que fallaba. Hace cinco cambios; el test
pasa. Guarda el procedimiento: "cuando falle este test, haz estos cinco cambios".
La próxima vez funciona. La tercera, no. El agente no sabe por qué: nunca registró
qué habría pasado con cuatro cambios, ni con otro orden, ni si el test pasó por
una razón distinta.

Este es el problema central de la memoria agéntica actual: **registra
trayectorias, no causas**. Los sistemas existentes guardan hechos (Mem0), episodios
(Generative Agents), relaciones temporales (Zep), habilidades (Voyager, CUMULUS) o
casos (Memento). Ninguno guarda sistemáticamente las alternativas que se
consideraron y no se eligieron. Sin ellas, el agente no puede asignar crédito,
no puede aprender de los casi-fallos y no puede distinguir suerte de competencia.

La pregunta de este trabajo:

> ¿Puede una memoria agéntica mejorar la adquisición de procedimientos si
> registra y consolida **contrafactuales** —lo que no pasó— además de lo que
> pasó?

Sostenemos que sí, y que la diferencia es medible: menos habilidades espurias,
mejor asignación de crédito, mejor transferencia y menos arrepentimiento.

## 2. Precedentes y el hueco

### 2.1 Lo que ya se intentó

- **Memoria de hechos y episodios:** MemGPT, Generative Agents, Mem0, Zep,
  HippoRAG, MemoryBank, A-MEM.
- **Memoria de habilidades:** Voyager (código), AWM (workflows), ExpeL
  (insights), ACE (playbook), SkillWeaver (APIs), CUMULUS (SIR portable).
- **Aprendizaje continuo:** EWC, replay, redes progresivas.
- **Cómputo offline:** sleep-time compute.

### 2.2 Lo que falta

Ninguno de estos sistemas responde:

- ¿La habilidad funcionó por causalidad o por suerte?
- ¿Qué habría pasado si se elegía otra acción?
- ¿Qué casi falló y por qué?
- ¿La habilidad transfiere a otro modelo o solo a otro prompt?
- ¿Cuándo debe retirarse una habilidad?

CUMULUS ataca la portabilidad y la gobernanza. JANUS ataca la causalidad.

### 2.3 Trabajo adyacente que no es lo mismo

- **Counterfactual replay en RL:** se usa para crédito y planificación, pero no
  como memoria de un agente de lenguaje.
- **Counterfactual data augmentation:** genera ejemplos para entrenar, no para
  recordar.
- **Causal discovery:** aprende grafos de datos, no de decisiones de agentes.
- **World models:** simulan futuros, pero no guardan el contrafactual de una
  decisión pasada con su evidencia.
- **Pensamiento contrafactual humano:** la psicología muestra que los humanos
  generan contrafactuales espontáneamente, sobre todo tras casi-fallos, y que
  esos contrafactuales son funcionales para el aprendizaje (Roese, 1997;
  Epstude y Roese, 2008; Byrne, 2005).

La combinación —memoria de decisiones + contrafactuales + promoción causal— no
está en la literatura de memoria agéntica.

## 3. El problema: suerte, superstición y crédito

### 3.1 Superstición

Si un agente prueba acciones hasta que una funciona, la memoria de éxito
registra la última acción, no la causa. Es el equivalente computacional de la
paloma de Skinner: cualquier conducta que preceda la recompensa se refuerza.

### 3.2 Crédito en horizontes largos

En una tarea de veinte pasos, el éxito puede deberse al paso 3, al 11 o al 19.
Sin contrafactuales, el agente no puede distribuir crédito; atribuye al último
paso o al más saliente.

### 3.3 Casi-fallos

Los casi-fallos son la información más valiosa y la más desperdiciada. Un agente
que falla por poco y no registra la alternativa cercana no aprende la frontera
entre lo que funciona y lo que no.

### 3.4 Interferencia y confusión

Dos acciones distintas pueden producir el mismo resultado por confusión
(estacionalidad, ruido, cambios del entorno). Sin un diseño causal, la memoria
promueve la acción equivocada.

### 3.5 El costo

Cada procedimiento espurio que entra al canon consume contexto, tiempo y
confianza. La memoria de éxitos es una máquina de acumular deuda técnica
cognitiva.

## 4. La tesis: memoria contrafactual

> **Tesis.** Un agente aprende mejor cuando su memoria registra, para cada
> decisión, el espacio de alternativas y una estimación de lo que habría pasado;
> y cuando solo consolida procedimientos cuyo efecto causal es identificable,
> robusto y transportable.

La memoria contrafactual no es un archivo de fantasías. Es un **registro
estructurado de evidencia contrafactual**, con jerarquía y confianza.

## 5. JANUS: arquitectura

### 5.1 Objetos de memoria

**Decision Record (DR).** El punto de decisión:

```yaml
decision:
  id: dr_...
  state: {task, context_hash, observations, budget}
  chosen: a
  alternatives: [a1, a2, ...]
  predictions: {a: y_hat, a1: y_hat1, ...}
  confidence: {a: 0.7, ...}
  policy: {model, agent, skill_version}
```

**Counterfactual Record (CFR).** Lo que se sabe de una alternativa:

```yaml
counterfactual:
  id: cf_...
  decision: dr_...
  alternative: a1
  outcome_estimate: y1
  evidence_type: randomized | natural_experiment | simulation | model_judgment
  support: {n, conditions, source}
  confidence: 0.6
```

**Causal Claim (CC).** Una relación causal con alcance:

```yaml
causal_claim:
  id: cc_...
  cause: a
  effect: y
  estimate: tau
  method: {rct | matching | iv | backdoor | frontdoor | simulation}
  scope: {domain, population, conditions}
  transportability: {tested_on, passed}
  confidence: 0.65
```

**Procedure (SIR).** La habilidad, ahora con justificación causal:

```yaml
procedure:
  id: sk_...
  steps: [...]
  causal_basis: [cc_...]
  effect_size: tau
  evidence: [dr_..., cfr_...]
  status: candidate | validated | canonical | deprecated
```

**Near-Miss.** Un fallo con margen pequeño; se guarda la alternativa que casi
funcionó.

**Regret.** La pérdida esperada por no haber elegido la mejor alternativa:
\[
R = \max_{a'} E[Y \mid do(a')] - E[Y \mid do(a)]
\]
Se usa para priorizar exploración y para detectar políticas conservadoras.

### 5.2 Capas

```
┌─────────────────────────────────────────────────────────────┐
│ POD        roles: proponente, ejecutor, auditor contrafactual, │
│            auditor causal, curador, crítico                   │
├─────────────────────────────────────────────────────────────┤
│ CAUSAL CANON  claims, procedimientos, alcance, transporte     │
├─────────────────────────────────────────────────────────────┤
│ FORGE      reconstrucción de alternativas, estimación, test   │
├─────────────────────────────────────────────────────────────┤
│ LEDGER     decisiones, alternativas, predicciones, resultados │
├─────────────────────────────────────────────────────────────┤
│ BRIDGE     renderizado y portabilidad entre modelos           │
└─────────────────────────────────────────────────────────────┘
```

### 5.3 Jerarquía de evidencia contrafactual

No todos los contrafactuales valen lo mismo:

1. **Experimento aleatorio:** el agente (o el sistema) asigna acciones al azar
   en un subconjunto de casos. Es la evidencia más fuerte.
2. **Experimento natural:** dos agentes o dos contextos similares reciben
   acciones distintas; se comparan con matching o propensity scores.
3. **Simulación:** un modelo del entorno estima el resultado. Útil, pero depende
   de la fidelidad del simulador.
4. **Juicio del modelo:** el LLM imagina qué habría pasado. Es la evidencia más
   débil y la más propensa a confabular; se usa solo como hipótesis, nunca como
   prueba.

La regla: **una habilidad no se promueve con evidencia de nivel 4 si hay
evidencia de nivel 1–2 disponible.**

### 5.4 Puerta de promoción causal

Un procedimiento se promueve solo si cumple:

1. **Efecto:** \(\tau > \delta\) (delta depende del costo y del riesgo).
2. **Identificabilidad:** el método causal es válido para el diseño (no hay
   confusores no medidos conocidos).
3. **Robustez:** el efecto sobrevive a variaciones de contexto y de modelo.
4. **Transportabilidad:** se probó en al menos otro dominio o modelo
   (Bareinboim y Pearl, 2016).
5. **Verificación:** las postcondiciones se ejecutan y pasan.
6. **Auditoría ciega:** un verificador independiente no ve al autor.

Si falla 2, el procedimiento se guarda como **correlacional**, no como canon.

### 5.5 Sueño contrafactual

La consolidación offline no resume: **reconstruye decisiones y estima
contrafactuales**.

```
para cada punto de decisión en el ledger:
    recuperar alternativas (log, política, propuestas)
    estimar resultados (jerarquía de evidencia)
    actualizar el grafo causal
    probar transporte a otros dominios/modelos
    si el efecto es positivo, identificable y robusto:
        promover procedimiento
    si el efecto es nulo o negativo:
        degradar o archivar
    si el casi-fallo es informativo:
        guardar near-miss y arrepentimiento
podar procedimientos espurios
reprogramar experimentos para los huecos de identificación
```

Esto es un "sueño" en el sentido funcional: offline, replay, selección,
abstracción y poda. No es un resumen.

### 5.6 Autocolaboración y experimentos naturales

En un sistema multiagente, distintos agentes enfrentan estados similares y eligen
acciones distintas. Eso produce **experimentos naturales**. JANUS los explota:

- **Proposer:** genera alternativas.
- **Executor:** actúa y registra.
- **Counterfactual Auditor:** reconstruye qué habría pasado.
- **Causal Auditor:** verifica identificabilidad, confusores y transporte.
- **Curator:** promueve, degrada, archiva.
- **Critic:** busca contraejemplos y preserva el disenso.

La auditoría es ciega: el auditor no ve la identidad del autor ni su
razonamiento, solo el registro, la evidencia y las postcondiciones. Esto evita la
autopreferencia y el contagio social documentado por la psicología.

El matching entre agentes se hace con covariates del estado (tarea, contexto,
presupuesto), no con la identidad del agente. Si dos agentes con estados
comparables obtienen resultados distintos con acciones distintas, hay señal
causal; si los estados no son comparables, no se usa.

## 6. Hipótesis

| # | Hipótesis | Métrica primaria | Dirección |
|---|---|---|---|
| H1 | La memoria contrafactual reduce habilidades espurias | Tasa de promoción de procedimientos con efecto nulo | ↓ |
| H2 | Mejora la asignación de crédito en horizontes largos | Precisión de atribución al paso causal | ↑ |
| H3 | Los procedimientos causalmente validados transfieren mejor | Transferencia entre modelos/dominios | ↑ |
| H4 | Los experimentos naturales entre agentes producen señal útil | AUC de identificación causal | ↑ |
| H5 | El sueño contrafactual supera al resumen con igual compresión | Retención y transferencia | ↑ |
| H6 | La memoria de casi-fallos mejora la exploración | Arrepentimiento acumulado | ↓ |
| H7 | La validación causal reduce el juego del verificador | Tasa de skills que pasan tests y fallan holdouts | ↓ |

Hipótesis nula: cualquier mejora se explica por más cómputo, mejor retrieval o
un evaluador complaciente.

## 7. Evaluación

### 7.1 Entornos con verdad causal conocida

- **MDPs de juguete** con efectos causales plantados y confusores.
- **Reparación de código** con bugs plantados y cambios distractores.
- **Pipelines de datos** con variables omitidas y estacionalidad.
- **Respuesta a incidentes** con señales ruidosas y causas múltiples.
- **Orquestación de herramientas** con acciones redundantes.

En todos, el sistema conoce el efecto causal real y puede medir si el agente lo
descubre.

### 7.2 Condiciones

| Condición | Descripción |
|---|---|
| C0 | Sin memoria |
| C1 | Memoria de trazas (éxitos y fracasos) |
| C2 | CUMULUS sin causalidad |
| C3 | Causal discovery sobre trazas |
| C4 | JANUS con simulación |
| C5 | JANUS con experimentos naturales |
| C6 | JANUS completo (incluye aleatorización selectiva) |

### 7.3 Métricas

- **Precisión causal:** ¿el efecto estimado coincide con el verdadero?
- **Tasa de habilidades espurias:** procedimientos promovidos con efecto nulo.
- **Transferencia:** éxito en otro modelo/dominio.
- **Arrepentimiento acumulado:** costo de no elegir la mejor acción.
- **Costo:** contrafactuales, simulación, experimentos.
- **Calibración:** confianza declarada vs. acierto.
- **Casi-fallos:** ¿se detectan y se usan?

### 7.4 Ablaciones

Sin contrafactuales, sin experimentos naturales, solo juicio del modelo, sin
prueba de transporte, sin auditoría ciega, sin casi-fallos.

### 7.5 Criterios de muerte

Tras el ciclo de evaluación, JANUS debe:

- reducir la tasa de habilidades espurias ≥30% frente a C2, y
- mejorar la precisión causal ≥20% frente a C3, y
- no aumentar el costo por éxito en más del 50%.

Si no, la hipótesis falla para este diseño.

## 8. Relación con CUMULUS

CUMULUS responde: **¿funciona y es portable?**
JANUS responde: **¿funcionó por esta razón?**

CUMULUS compila procedimientos desde trazas; JANUS añade el registro de
alternativas y la puerta causal. Sin CUMULUS, JANUS no tiene dónde promover; sin
JANUS, CUMULUS promueve correlaciones.

La arquitectura completa:

```
Trace/Decision Ledger → Forge (compilación) → Causal Canon (JANUS)
                      → Canon portable (CUMULUS) → Pod → Bridge
```

## 9. Riesgos y gobernanza

- **Contrafactuales confabulados:** el LLM puede inventar resultados. Mitigación:
  jerarquía de evidencia y prohibición de promover con nivel 4.
- **Confusores no medidos:** el matching no elimina lo que no se observa.
  Mitigación: aleatorización selectiva y reporte de incertidumbre.
- **Costo:** simular y experimentar es caro. Mitigación: presupuesto por
  decisión y valor esperado de la información.
- **Privacidad:** las alternativas rechazadas pueden revelar información.
  Mitigación: redacción y permisos.
- **Sobreajuste al grafo causal:** un grafo equivocado se vuelve dogma.
  Mitigación: revisión, disenso y pruebas de transporte.
- **Manipulación:** la memoria de lo que no pasó puede usarse para justificar
  decisiones sesgadas. Mitigación: auditoría y procedencia.

## 10. Agenda y conclusión

La memoria agéntica ha pasado de recordar texto a recordar hechos, episodios y
habilidades. El siguiente paso no es recordar más: es recordar **mejor**, y eso
significa recordar lo que no pasó.

JANUS propone:

1. Contrafactuales como objetos de primera clase.
2. Una jerarquía de evidencia que separa experimento de imaginación.
3. Una puerta de promoción causal para las habilidades.
4. Experimentos naturales entre agentes.
5. Memoria de casi-fallos y arrepentimiento.
6. Un sueño contrafactual que consolida causas, no anécdotas.

Si funciona, el resultado no es un agente que sabe más. Es un agente que sabe
**por qué** sabe lo que sabe, y que puede descartar lo que solo parecía
funcionar.

---

## Referencias

Bareinboim, E., & Pearl, J. (2016). Causal inference and the data-fusion
problem. *PNAS, 113*(27), 7345–7352.

Byrne, R. M. J. (2005). *The rational imagination: How people create alternatives
to reality*. MIT Press.

Daw, N. D., Gershman, S. J., Seymour, B., Dayan, P., & Dolan, R. J. (2011).
Model-based influences on humans' choices and striatal prediction errors.
*Neuron, 69*(6), 1204–1215.

Epstude, K., & Roese, N. J. (2008). The functional theory of counterfactual
thinking. *Personality and Social Psychology Review, 12*(2), 168–192.

Gopnik, A., Glymour, C., Sobel, D. M., Schulz, L. E., Kushnir, T., & Danks, D.
(2004). A theory of causal learning in children: Causal maps and Bayes nets.
*Psychological Review, 111*(1), 3–32.

Hernán, M. A., & Robins, J. M. (2020). *Causal inference: What if*. CRC Press.

Holton, E., Braun, L., Thompson, J. A. F., Grohn, J., & Summerfield, C. (2026).
Humans and neural networks show similar patterns of transfer and interference
during continual learning. *Nature Human Behaviour, 10*, 111–125.

Kahneman, D., & Miller, D. T. (1986). Norm theory: Comparing reality to its
alternatives. *Cognitive Psychology, 18*(2), 136–168.

Lewis, D. (1973). *Counterfactuals*. Blackwell.

Pearl, J. (2009). *Causality: Models, reasoning, and inference* (2nd ed.).
Cambridge University Press.

Roese, N. J. (1997). Counterfactual thinking. *Psychological Bulletin, 121*(1),
133–148.

Rosenbaum, P. R., & Rubin, D. B. (1983). The central role of the propensity score
in observational studies for causal effects. *Biometrika, 70*(1), 41–55.

Rubin, D. B. (1974). Estimating causal effects of treatments in randomized and
nonrandomized studies. *Journal of Educational Psychology, 66*(5), 688–701.
