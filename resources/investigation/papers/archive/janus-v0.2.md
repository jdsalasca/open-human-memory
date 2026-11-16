# JANUS v0.2: memoria con identificabilidad declarada

### De "recordar lo que no pasó" a "saber qué se puede afirmar"

**DeepSeek 4.1 Flash** — Modelo de lenguaje  
**Juan David Salas Camargo** — Massachusetts Institute of Technology (MIT)

*Documento de trabajo · v0.2 · noviembre de 2026 · no arbitrado*

> **Nota de revisión.** La v0.1 afirmaba que la memoria contrafactual era un
> terreno casi no explorado. Es falso: COUNTERMEM (Pu et al., 2026), ConMem
> (Zhang et al., 2026), MemCon (Jiang et al., 2026) y otros trabajos de 2026 ya
> la estudian. Esta versión retira la afirmación de prioridad y reduce la
> contribución a cuatro propiedades específicas. Ver
> `precedentes/07-antecedentes-2026-ii.md`.

---

## Resumen

Una trayectoria registra lo que el agente hizo, no lo que habría pasado si hacía
otra cosa. La memoria contrafactual intenta cerrar esa brecha, pero ya existe:
COUNTERMEM verifica alternativas locales con modelos del mundo ejecutables;
ConMem usa sondas contrafactuales para decidir qué memorizar; MemCon aprende
cuándo recuperar, consolidar o olvidar. Este trabajo no reclama prioridad.
Propone cuatro propiedades que esos sistemas no combinan: (1) **identificabilidad
declarada** en cada objeto de memoria —qué se puede estimar, con qué supuestos y
qué falta—; (2) **validación tridimensional** —fiabilidad, causalidad,
portabilidad— con una política de uso según riesgo; (3) un **ledger de
incertidumbre y agenda experimental** que recuerda preguntas abiertas y
experimentos pendientes; y (4) **anti-persistencia selectiva**, que decide cuándo
persistir una abstracción y cuándo reconstruirla. Se formula un experimento
diferencial A–E con errores persistentes, calibración y abandono de creencias
como métricas principales.

**Palabras clave:** identificabilidad, memoria contrafactual, incertidumbre,
anti-persistencia, validación tridimensional.

## Abstract

A trajectory records what the agent did, not what would have happened otherwise.
Counterfactual memory attempts to close that gap, but it already exists:
COUNTERMEM verifies local alternatives with executable world models; ConMem uses
counterfactual probes for memory admission; MemCon learns when to retrieve,
consolidate, or forget. This work claims no priority. It proposes four properties
these systems do not combine: (1) **declared identifiability** in every memory
object—what can be estimated, under which assumptions, and what is missing;
(2) **three-dimensional validation**—reliability, causality, portability—with a
risk-sensitive use policy; (3) an **uncertainty and experimental agenda ledger**
that remembers open questions and pending experiments; and (4) **selective
anti-persistence**, deciding when to persist an abstraction and when to
reconstruct it. We specify a differential A–E experiment with persistent errors,
calibration, and belief abandonment as primary metrics.

---

## 1. Introducción: de la memoria de lo que pasó a la memoria de lo que se puede saber

Un agente encuentra un fallo, prueba tres cambios —configuración del productor,
política de reintentos, reinicio del servicio— y el sistema vuelve a funcionar.
La memoria tradicional guarda: "A, B y C resolvieron el problema". CUMULUS
intenta descubrir cuáles eran necesarios. JANUS pregunta: "¿qué habría pasado si
solo se ejecutaba C?".

La pregunta es correcta, pero ya tiene respuestas parciales. COUNTERMEM restaura
el estado y ejecuta alternativas con tests o solvers. ConMem simula escenarios
futuros para decidir si una memoria debe admitirse. MemCon aprende cuándo
recuperar y cuándo olvidar.

El problema que queda es más profundo: **una alternativa registrada no es un
resultado; un resultado alternativo no es un efecto causal; y un efecto causal no
siempre es identificable**. La memoria debe saber qué puede afirmar y qué no.

## 2. Antecedentes y corrección de novedad

| Trabajo | Qué hace | Qué no resuelve |
|---|---|---|
| COUNTERMEM (Pu et al., 2026) | Alternativas locales verificadas con modelos ejecutables; condiciones de aplicabilidad; selector usar/saltar | Identificación con estado parcialmente oculto; longitudinal; portabilidad |
| ConMem (Zhang et al., 2026) | Admisión de memoria por sondas contrafactuales (relevante, irrelevante, riesgo) | Efectos secuenciales; acumulación |
| MemCon (Jiang et al., 2026) | Control adaptativo de memoria (recuperar, planificar, consolidar, olvidar) | Causalidad; beneficios de consolidación no establecidos |
| More Memory, Worse Agents (Wang et al., 2026) | Error reproduction; anti-persistencia | Política de cuándo persistir |
| Attributing Agent Failures... (Pakhomov y Nijkamp, 2026) | Replay con certificado; intervención sobre historia | Memoria de agentes |
| What Is This Memory Useful For? (Yang et al., 2026) | Utilidad condicionada a tarea | Procedimientos; coding sin efecto |
| TANGLE (Yang et al., 2026) | Conflicto irreducible; brecha reconocimiento–acción | Memoria que preserve y actúe bajo incertidumbre |
| When Errors Become Memories (Xiao et al., 2026) | Propagación causal de errores en memoria | Detección temprana y reparación |

**Conclusión:** JANUS no es la primera memoria contrafactual. Su espacio es la
**identificabilidad declarada**, la **validación tridimensional**, la
**incertidumbre como contenido** y la **anti-persistencia selectiva**.

## 3. El problema epistemológico

### 3.1 Cinco cosas distintas

| Nivel | Qué sabemos |
|---|---|
| Acción elegida | Que fue ejecutada |
| Resultado observado | Qué ocurrió después |
| Alternativa considerada | Que el agente la contempló |
| Resultado alternativo predicho | Qué cree un modelo que podría ocurrir |
| Resultado alternativo ejecutado | Qué ocurrió en otra ejecución, bajo condiciones |
| Efecto causal | Diferencia atribuible a la intervención, bajo supuestos |

La memoria no debe colapsar estos niveles. Un `Counterfactual Record` con
`evidence_type: model_judgment` es una **hipótesis**, no un hecho sobre un mundo
alternativo.

### 3.2 El estimando

Para un estado \(s\), acciones \(a\) y \(a'\):

\[
\tau(s,a,a') = \mathbb{E}[Y \mid do(a), s] - \mathbb{E}[Y \mid do(a'), s]
\]

En una tarea secuencial hay que especificar además:

- la política que se seguirá después de la intervención;
- el horizonte de observación;
- el resultado \(Y\) (éxito, daño, costo, tiempo);
- el estado \(s\) y qué parte es observable.

Sin esa especificación, "habría pasado" no es un estimando: es una frase.

### 3.3 Las condiciones de identificación

Un efecto es identificable si se cumplen, para el diseño usado:

1. **Consistencia:** la acción registrada corresponde a la intervención.
2. **Positividad:** las acciones comparadas tienen probabilidad positiva en el
   estado.
3. **Ignorabilidad:** no hay confusores no medidos relevantes, o se controlan.
4. **SUTVA / no interferencia:** el resultado de un agente no depende de las
   acciones de otro, o se modela.
5. **Restauración:** el estado se reproduce fielmente, con certificado.

Si falla una, el sistema debe **abstenerse** de afirmar causalidad.

## 4. Identificabilidad como propiedad del recuerdo

### 4.1 Decision Record ampliado

```yaml
decision:
  id: dr_...
  state:
    hash: ...
    observable: [...]
    hidden_assumptions: [...]
  policy:
    model: ...
    propensity: {a: 0.7, a1: 0.2, a2: 0.1}
  chosen: a
  alternatives: [a1, a2]
  predictions: {a: y_hat, a1: y_hat1}
  context:
    tool_versions: {...}
    exogenous: {...}
    observation_window: ...
  outcome: {y: ..., verifier: ..., time: ...}
```

La **propensión** es clave: sin la probabilidad con la que la política eligió
cada acción, los estimadores fuera de política (IPS, SNIPS, doubly robust) no se
pueden aplicar.

### 4.2 Counterfactual Record con estado epistémico

```yaml
counterfactual:
  id: cf_...
  decision: dr_...
  alternative: a1
  outcome_estimate: y1
  evidence_type: randomized | natural_experiment | simulation | model_judgment
  method: ...
  assumptions: [...]
  support: {n, overlap, restore_certificate}
  identifiability: identified | partially_identified | not_identified
  confidence_interval: ...
```

`identifiability` no es un adjetivo decorativo: es una propiedad que decide si el
registro puede sostener una afirmación causal o solo una hipótesis.

### 4.3 Abstención

El sistema debe poder responder:

> "No hay evidencia suficiente para determinar qué acción causó el resultado."

Eso no es un fallo; es una capacidad. La abstención evita consolidar una
superstición y abre una pregunta experimental.

## 5. Tres dimensiones, no una puerta

La v0.1 exigía causalidad para promover un procedimiento. Es demasiado rígido.
Fiabilidad, causalidad y portabilidad son propiedades distintas:

| Dimensión | Pregunta | Evidencia | Uso |
|---|---|---|---|
| Fiabilidad | ¿Funciona repetidamente? | Tasa de éxito, varianza, calibración | Acciones reversibles |
| Causalidad | ¿Por qué funciona? | Intervención, contrafactual, identificación | Acciones de alto riesgo |
| Portabilidad | ¿Dónde más funciona? | Matriz entre modelos/dominios | Reutilización |

Añadimos **riesgo** y **costo**:

| Riesgo | Política |
|---|---|
| Bajo y reversible | Fiabilidad suficiente; causalidad opcional |
| Medio | Fiabilidad + portabilidad; causalidad deseable |
| Alto e irreversible | Causalidad identificada + portabilidad + revisión |

Esto permite usar procedimientos empíricamente útiles sin atribuirles
explicaciones no demostradas, y exige más evidencia cuando el daño es grave.

## 6. Incertidumbre, ignorancia y agenda experimental

### 6.1 Ledger de incertidumbre

```yaml
uncertainty:
  id: un_...
  claim: "..."
  status: unknown | assumed | unverified | contested
  missing: [context, time, source, measurement]
  impact: high | medium | low
  resolution: {experiment, cost, expected_information_gain}
```

No guarda solo lo que se sabe: guarda **qué falta para saberlo**.

### 6.2 Agenda experimental

```yaml
open_question:
  id: oq_...
  observation: "el servicio se recuperó tras A, B y C"
  hypothesis: "C, no A, causó la recuperación"
  status: not_identified
  experiment:
    design: reset + solo C
    cost: ...
    safety: sandbox
  update_condition: "si el test pasa en 3/3 repeticiones"
```

Esto convierte la memoria en una **agenda de problemas progresivamente
resueltos**, no en un archivo de conclusiones.

### 6.3 Conflicto irreducible

No todo conflicto se resuelve. TANGLE muestra que los agentes detectan el
conflicto mejor de lo que actúan sobre él. JANUS debe preservar la tensión:

- `resolved`: hay evidencia suficiente.
- `contested`: hay evidencia en contra.
- `underdetermined`: falta contexto, tiempo o autoridad de fuente.

La acción puede ser `commit`, `conditionalize`, `clarify`, `verify`, `defer` o
`reversible_trial`, según riesgo y evidencia.

## 7. Anti-persistencia selectiva

More Memory, Worse Agents muestra que persistir abstracciones puede reproducir
errores. La política de JANUS:

1. **Persistir** trayectorias, resultados y evidencia factual.
2. **Reconstruir** guía y abstracciones bajo demanda, con la tarea actual.
3. **Persistir** una abstracción solo si:
   - es operacionalmente fiable;
   - tiene evidencia de estabilidad;
   - su aplicabilidad está acotada;
   - se monitorea su reproducción de errores.
4. **Revisar** cuando cambia el modelo, la API, el requisito o la distribución.

La memoria no es un canon inmutable: es un **proceso con curaduría**.

## 8. Arquitectura JANUS v0.2

```
┌─────────────────────────────────────────────────────────────┐
│ POD        proponente, ejecutor, auditor contrafactual,       │
│            auditor causal, curador, crítico                   │
├─────────────────────────────────────────────────────────────┤
│ AGENDA     preguntas abiertas, experimentos pendientes        │
├─────────────────────────────────────────────────────────────┤
│ INCERTIDUMBRE  desconocido, asumido, no verificado, contestado│
├─────────────────────────────────────────────────────────────┤
│ CANON      fiabilidad | causalidad | portabilidad | riesgo    │
├─────────────────────────────────────────────────────────────┤
│ FORJA      cribado, identificación, contrafactuales           │
├─────────────────────────────────────────────────────────────┤
│ LEDGER     decisiones, propensiones, estados, resultados      │
└─────────────────────────────────────────────────────────────┘
```

### 8.1 Bucle

```
1. Decisión: registrar estado, propensión, alternativas, predicción.
2. Resultado: observar, verificar, actualizar.
3. Cribado: ¿hay alternativa comparable? ¿hay estado restaurable?
4. Identificación: aplicar método; declarar supuestos y limitaciones.
5. Clasificar: fiable / causal / portable / incierto / abierto.
6. Política: usar, condicionar, verificar, abstenerse o experimentar.
7. Revisión: detectar deriva, error reproductivo y obsolescencia.
```

### 8.2 Roles

- **Proposer:** genera alternativas y hipótesis.
- **Executor:** actúa y registra.
- **Counterfactual Auditor:** reconstruye y verifica.
- **Causal Auditor:** evalúa identificación, confusores y transporte.
- **Curator:** decide persistir, reconstruir o archivar.
- **Critic:** busca contraejemplos y preserva disenso.

La auditoría es ciega: el auditor no ve la identidad del autor, solo el registro,
la evidencia y las postcondiciones.

## 9. Experimentos naturales y certificados de replay

### 9.1 No todo agente distinto es un experimento

Dos agentes que eligen acciones distintas no constituyen un experimento natural
si difieren en modelo, capacidades, instrucciones, herramientas, información o
política. Atribuir la diferencia a la acción sería incorrecto.

Para usar un experimento natural se necesita:

- estados comparables (matching o estratificación);
- solapamiento de acciones;
- ausencia de interferencia entre agentes;
- registro de la política de asignación;
- **certificado de replay** si se restaura el estado.

### 9.2 Certificado de replay

Pakhomov y Nijkamp (2026) muestran que snapshots con el mismo hash pueden diferir
de la continuación viva si no se restaura el estado del proceso (por ejemplo, la
posición del flujo aleatorio). Antes de afirmar identificación, JANUS debe medir:

- tasa de acuerdo entre restauración y referencia;
- condiciones de la medición;
- si el estimando requiere replay exacto o igualdad distribucional.

Sin certificado, el contrafactual es una simulación, no una intervención.

## 10. Casi-fallos y arrepentimiento

Un casi-fallo necesita una **métrica de distancia** al objetivo:

- en un test binario, no hay "casi";
- en un problema matemático, puede haber distancia a la solución;
- en un sistema distribuido, "casi" puede significar "a punto de un incidente".

El arrepentimiento:

\[
R = \max_{a'} \mathbb{E}[Y \mid do(a')] - \mathbb{E}[Y \mid do(a)]
\]

no es una observación: es una **estimación con incertidumbre**. Se guarda con
intervalo y método; si no se puede estimar, se guarda como pregunta abierta.

## 11. Hipótesis

| # | Hipótesis | Métrica | Falsación |
|---|---|---|---|
| HJ1 | La identificabilidad declarada reduce afirmaciones causales falsas | Tasa de claims causales no soportados | Sin reducción |
| HJ2 | La validación tridimensional mejora el uso de habilidades frente a una puerta causal única | Éxito en tareas reversibles + seguridad en irreversibles | Peor en ambas |
| HJ3 | El ledger de incertidumbre reduce errores persistentes | Errores repetidos tras consolidación | Sin diferencia |
| HJ4 | La agenda experimental mejora el aprendizaje por costo | Aprendizaje por 1k tokens | Peor que azar |
| HJ5 | La anti-persistencia selectiva reduce la reproducción de errores | Deriva de creencias | Igual o peor que Canon |
| HJ6 | El disentimiento preservado acelera la corrección | Tiempo a abandono | Sin diferencia |

## 12. Evaluación diferencial A–E

| Condición | Memoria |
|---|---|
| A | Episodios + recuperación |
| B | Playbooks persistentes (CUMULUS) |
| C | Hechos + abstracciones temporales (anti-persistencia) |
| D | JANUS con contrafactuales verificados |
| E | D + incertidumbre + agenda experimental |

**Diseño:** mismas familias de tareas, presupuesto igualado, modelos congelados,
restauraciones certificadas, holdouts ocultos, deriva programada, casos de
abstención.

**Métricas primarias:** errores persistentes, calibración de incertidumbre,
abandono de creencias refutadas.

**Secundarias:** éxito, costo por éxito, falsos recuerdos promovidos, detección
de contradicciones, transferencia negativa, abstención correcta.

**Criterio de muerte:** si E no supera a C o D en las primarias, la complejidad
adicional no se justifica.

## 13. Límites, seguridad y gobernanza

- **Estado parcialmente oculto:** la identificación puede ser imposible; el
  sistema debe abstenerse.
- **Contrafactuales confabulados:** el juicio del modelo es nivel 4; nunca prueba.
- **Costo:** simular y experimentar es caro; usar valor esperado de la
  información.
- **Privacidad:** las alternativas rechazadas pueden revelar información.
- **Envenenamiento:** una traza maliciosa puede generar una habilidad dañina.
- **Gobernanza:** procedencia, permisos, auditoría, rollback y caducidad.
- **Afiliación y autoría:** la afiliación MIT es la declarada por el autor humano;
  la participación de IA debe declararse antes de un envío.

## 14. Conclusión

JANUS v0.1 preguntaba qué habría pasado. JANUS v0.2 pregunta algo más difícil:
**qué se puede afirmar sobre lo que habría pasado, con qué evidencia y cuándo hay
que callar**.

No es la primera memoria contrafactual. Es una propuesta para que la memoria
sepa distinguir lo que observó, lo que infirió, lo que estimó y lo que todavía no
puede saber. En un campo que ya produce contrafactuales verificados y
abstracciones que se reproducen, esa distinción puede valer más que otra capa de
arquitectura.

---

## Referencias

Bareinboim, E., & Pearl, J. (2016). Causal inference and the data-fusion problem.
*PNAS, 113*(27), 7345–7352.

Belikova, J., et al. (2026). *Managing procedural memory in LLM agents*.
arXiv:2606.23127.

Chalef, D., et al. (2026). *Learning by doing: Autonomously compiling and
curating agent skills from verified traces*. arXiv:2611.01386.

Jiang, E. H., et al. (2026). *Memory as a controlled process: Learned adaptive
memory management for LLM agents*. arXiv:2607.13591.

Jiang, Z., et al. (2026). *Demystifying agent skills: Why they work—until they
don't*. arXiv:2608.14036.

Pakhomov, E., & Nijkamp, E. (2026). *Attributing agent failures to their history
needs an executed counterfactual*. arXiv:2611.05650.

Pearl, J. (2009). *Causality* (2nd ed.). Cambridge University Press.

Pu, H., Tang, R., & Zhang, Y. (2026). *COUNTERMEM: World-model verified
counter-factual memory for language agents*. arXiv:2609.31874.

Rosenbaum, P. R., & Rubin, D. B. (1983). The central role of the propensity score
in observational studies for causal effects. *Biometrika, 70*(1), 41–55.

Rubin, D. B. (1974). Estimating causal effects of treatments in randomized and
nonrandomized studies. *Journal of Educational Psychology, 66*(5), 688–701.

Tang, B., et al. (2026). From memory to skills: Evidence-grounded governance for
long-horizon LLM agents. *Findings of EMNLP 2026*, 34826–34847.

Wang, R., Panaganti, K., & Zhou, D. (2026). *More memory, worse agents: Error
reproduction and anti-persistence in LLM agents*. arXiv:2610.27406.

Xiao, S., et al. (2026). *When errors become memories: Causal pathway tracing in
multi-turn memory-augmented LLMs*. arXiv:2608.30198.

Yang, C.-H., et al. (2026). *What is this memory useful for? Measuring
task-conditioned utility in long-term agent memory*. arXiv:2611.03930.

Yang, L., et al. (2026). *When personal memory has no single answer: Evaluating
LLM agents under irreducible conflict*. arXiv:2608.13921.

Zhang, Q., et al. (2025). *Agentic Context Engineering*. arXiv:2510.04618.

Zhang, S., et al. (2026). *ConMem: Counterfactual multi-scenario probing for
resolving LLM memory misalignment*. arXiv:2610.33432.
