# JANUS: memoria con identificabilidad declarada

### Cómo recordar lo que no pasó sin afirmar más de lo que se sabe

**DeepSeek 4.1 Flash** — Modelo de lenguaje  
**Juan David Salas Camargo** — Massachusetts Institute of Technology (MIT)

*Documento de trabajo · v1.0 · noviembre de 2026 · no arbitrado*

---

## Resumen

La memoria contrafactual ya existe: COUNTERMEM verifica alternativas locales con
modelos del mundo ejecutables; ConMem usa sondas contrafactuales para decidir qué
memorizar; MemCon aprende cuándo recuperar, consolidar o olvidar. Este trabajo no
reclama prioridad. Propone una memoria que **declara su identificabilidad**: cada
objeto dice qué se puede estimar, con qué supuestos y qué falta; distingue
fiabilidad, causalidad y portabilidad con una política de uso según riesgo;
mantiene un **ledger de incertidumbre y agenda experimental**; y aplica
**anti-persistencia selectiva** para no convertir errores en certezas. La tesis se
evalúa con un experimento diferencial A–E cuyas métricas primarias son errores
persistentes, calibración y abandono de creencias refutadas, no éxito bruto.

**Palabras clave:** identificabilidad, memoria contrafactual, incertidumbre,
anti-persistencia, validación tridimensional.

## Abstract

Counterfactual memory already exists: COUNTERMEM verifies local alternatives with
executable world models; ConMem uses counterfactual probes for memory admission;
MemCon learns when to retrieve, consolidate, or forget. This work claims no
priority. It proposes memory that **declares its identifiability**: each object
states what can be estimated, under which assumptions, and what is missing;
distinguishes reliability, causality, and portability with a risk-sensitive use
policy; keeps an **uncertainty and experimental agenda ledger**; and applies
**selective anti-persistence** to avoid turning errors into certainties. The
thesis is tested with a differential A–E experiment whose primary metrics are
persistent errors, calibration, and abandonment of refuted beliefs, not raw
success.

---

## 1. Introducción: la memoria que sabe lo que no sabe

Un agente encuentra un fallo, prueba tres cambios y el sistema vuelve a
funcionar. La memoria tradicional guarda "A, B y C lo resolvieron". CUMULUS
intenta descubrir cuáles eran necesarios. JANUS pregunta: "¿qué habría pasado si
solo se ejecutaba C?".

Pero una alternativa registrada no es un resultado; un resultado alternativo no
es un efecto causal; y un efecto causal no siempre es identificable. La memoria
debe distinguir esos niveles y, cuando no puede, **abstenerse**.

## 2. Antecedentes: el terreno ya está poblado

| Trabajo | Qué hace | Qué deja abierto |
|---|---|---|
| COUNTERMEM (Pu et al., 2026) | Alternativas locales verificadas con tests, proof checkers, SQL, solvers; condiciones de aplicabilidad; selector usar/saltar | Estado parcialmente oculto; longitudinal; portabilidad |
| ConMem (Zhang et al., 2026) | Admisión de memoria por sondas contrafactuales relevantes, irrelevantes y de riesgo | Efectos secuenciales; acumulación |
| MemCon (Jiang et al., 2026) | Control adaptativo: recuperar, planificar, re-sondear, consolidar, olvidar | Causalidad; consolidación/olvido no probados |
| More Memory, Worse Agents (Wang et al., 2026) | Error reproduction; anti-persistencia | Política de cuándo persistir |
| Attributing Agent Failures... (Pakhomov y Nijkamp, 2026) | Replay con certificado; intervención sobre la historia | Memoria de agentes |
| What Is This Memory Useful For? (Yang et al., 2026) | Utilidad condicionada a tarea | Procedimientos; coding sin efecto |
| TANGLE (Yang et al., 2026) | Conflicto irreducible; brecha reconocimiento–acción | Memoria que preserve y actúe bajo incertidumbre |
| When Errors Become Memories (Xiao et al., 2026) | Propagación causal de errores en memoria | Detección temprana y reparación |

**Conclusión:** la novedad no es "recordar alternativas". Es **declarar qué se
puede afirmar** y **usar esa declaración para decidir**.

## 3. Los cinco niveles

| Nivel | Qué sabemos |
|---|---|
| Acción elegida | Que fue ejecutada |
| Resultado observado | Qué ocurrió después |
| Alternativa considerada | Que el agente la contempló |
| Resultado alternativo predicho | Qué cree un modelo que podría ocurrir |
| Resultado alternativo ejecutado | Qué ocurrió en otra ejecución |
| Efecto causal | Diferencia atribuible a la intervención, bajo supuestos |

Un `Counterfactual Record` con `evidence_type: model_judgment` es una hipótesis,
no un hecho sobre un mundo alternativo.

## 4. Identificabilidad

### 4.1 El estimando

\[
\tau(s,a,a') = \mathbb{E}[Y \mid do(a), s] - \mathbb{E}[Y \mid do(a'), s]
\]

Hay que especificar la política posterior, el horizonte, el resultado \(Y\) y qué
parte del estado es observable.

### 4.2 Condiciones

1. **Consistencia:** la acción registrada corresponde a la intervención.
2. **Positividad:** ambas acciones tienen probabilidad positiva.
3. **Ignorabilidad:** no hay confusores no medidos relevantes.
4. **No interferencia:** el resultado de un agente no depende de otro.
5. **Restauración:** el estado se reproduce con certificado medido.

Si falla una, el sistema se abstiene de afirmar causalidad.

### 4.3 Decision Record con propensión

```yaml
decision:
  id: dr_...
  state: {hash, observable, hidden_assumptions}
  policy: {model, propensity: {a: 0.7, a1: 0.2, a2: 0.1}}
  chosen: a
  alternatives: [a1, a2]
  predictions: {a: y_hat, a1: y_hat1}
  context: {tool_versions, exogenous, observation_window}
  outcome: {y, verifier, time}
```

Sin propensión no se pueden aplicar estimadores fuera de política (IPS, SNIPS,
doubly robust).

### 4.4 Procedimiento de identificabilidad

No basta con escribir `identifiability: identified`. El sistema ejecuta cinco
chequeos y registra el resultado:

1. **Consistencia:** la acción registrada coincide con la intervención.
2. **Positividad:** ambas acciones tienen probabilidad positiva en el estado.
3. **Ignorabilidad:** no hay confusores no medidos relevantes, o se controlan.
4. **No interferencia:** el resultado no depende de acciones de otros agentes.
5. **Restauración:** el certificado de replay pasa el umbral del estimando.

| Resultado | Condición |
|---|---|
| `identified` | los cinco pasan |
| `partially_identified` | falla ignorabilidad o transporte, pero hay bounds |
| `not_identified` | falla consistencia, positividad, no interferencia o restauración |

Si es `not_identified`, se guarda como hipótesis y pregunta abierta, no como
claim causal.

**Procedencia de la propensión.** No todas las probabilidades son iguales:

- `measured`: frecuencia observada de la política real.
- `controlled`: asignación experimental conocida.
- `subjective`: estimación del modelo.

Solo `measured` y `controlled` se usan para IPS/SNIPS/doubly robust. La subjetiva
es un prior, no una probabilidad.

**Límite:** un certificado de restauración no prueba que la conclusión causal sea
verdadera; solo que la comparación se hizo sobre un estado reproducible. La
transportabilidad se prueba aparte.

### 4.5 Certificado de replay

Pakhomov y Nijkamp (2026) muestran que snapshots con el mismo hash pueden diferir
de la continuación viva si no se restaura el estado del proceso. Antes de afirmar
identificación, JANUS mide la tasa de acuerdo entre restauración y referencia.

## 5. Tres dimensiones, no una puerta

| Dimensión | Pregunta | Evidencia | Uso |
|---|---|---|---|
| Fiabilidad | ¿Funciona repetidamente? | Éxito, varianza, calibración | Acciones reversibles |
| Causalidad | ¿Por qué funciona? | Intervención, contrafactual | Alto riesgo |
| Portabilidad | ¿Dónde más funciona? | Matriz entre modelos/dominios | Reutilización |

Con riesgo y costo:

| Riesgo | Evidencia mínima |
|---|---|
| Bajo y reversible | Fiabilidad |
| Medio | Fiabilidad + portabilidad |
| Alto e irreversible | Causalidad identificada + portabilidad + revisión |

Esto evita bloquear procedimientos útiles por falta de explicación causal y
permite acciones irreversibles solo con evidencia fuerte.

## 6. Incertidumbre, ignorancia y agenda

### 6.1 Ledger de incertidumbre

```yaml
uncertainty:
  id: un_...
  claim: ...
  status: unknown | assumed | unverified | contested
  missing: [context, time, source, measurement]
  impact: high | medium | low
  resolution: {experiment, cost, expected_information_gain}
```

### 6.2 Agenda experimental

```yaml
open_question:
  id: oq_...
  observation: ...
  hypothesis: ...
  status: not_identified
  experiment: {design, cost, safety}
  update_condition: ...
```

La memoria deja de ser un archivo de conclusiones y se convierte en una agenda
de problemas progresivamente resueltos.

### 6.3 Conflicto irreducible

TANGLE muestra que los agentes detectan el conflicto mejor de lo que actúan sobre
él. JANUS preserva `resolved`, `contested` y `underdetermined`, y elige
`commit`, `conditionalize`, `clarify`, `verify`, `defer` o `reversible_trial`
según riesgo y evidencia.

## 7. Anti-persistencia selectiva

More Memory, Worse Agents documenta que persistir abstracciones puede reproducir
errores. La política:

1. Persistir trayectorias, resultados y evidencia factual.
2. Reconstruir guía y abstracciones bajo demanda.
3. Persistir una abstracción solo si es fiable, estable, acotada y monitoreada.
4. Revisar cuando cambia el modelo, la API, el requisito o la distribución.

El Canon no es inmutable: es un proceso con curaduría.

## 8. Arquitectura

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

## 9. La línea DeepSeek y el presupuesto de atención

- **MLA** (DeepSeek-V2) comprime el KV cache un 93,3%; el contexto es un problema
  de memoria y ancho de banda, no solo de tokens.
- **DeepSeek-V3** activa 37B de 671B; la capacidad total no es la capacidad
  activa. El enrutamiento de memoria se parece al enrutamiento de expertos.
- **NSA** selecciona bloques de atención de forma nativa; la memoria externa debe
  justificar su costo frente a atención larga eficiente.
- **GRPO** (DeepSeekMath, R1) permite entrenar una política de uso de memoria con
  recompensas verificables sin tocar el LLM base.
- **DeepSeek-Coder/Prover** muestran que tests y proof checkers son verificadores
  fiables; son los world models naturales para contrafactuales.

**Consecuencia:** JANUS no compite por tokens. Compite por **juicio por unidad de
cómputo**.

## 10. Hipótesis

| # | Hipótesis | Métrica | Falsación |
|---|---|---|---|
| HJ1 | La identificabilidad declarada reduce claims causales falsos | Claims no soportados | Sin reducción |
| HJ2 | La validación tridimensional mejora el uso frente a una puerta causal única | Éxito reversible + seguridad irreversible | Peor en ambas |
| HJ3 | El ledger de incertidumbre reduce errores persistentes | Errores repetidos | Sin diferencia |
| HJ4 | La agenda experimental mejora el aprendizaje por costo | Aprendizaje por 1k tokens | Peor que azar |
| HJ5 | La anti-persistencia selectiva reduce la reproducción de errores | Deriva de creencias | Igual o peor que Canon |
| HJ6 | El disenso preservado acelera la corrección | Tiempo a abandono | Sin diferencia |

## 11. Experimento diferencial A–E

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

**Primarias:** errores persistentes, calibración de incertidumbre, abandono de
creencias refutadas.

**Secundarias:** éxito, costo por éxito, falsos recuerdos promovidos, detección de
contradicciones, transferencia negativa, abstención correcta.

**Criterio de muerte:** si E no supera a C o D en las primarias, la complejidad
adicional no se justifica.

### 11.1 Nota empírica: prototipos 003 y 004-A (aprendizaje de macros)

El Prototipo 002 resultó ser un benchmark de solucionador: `MEM-A0`, el mismo
solucionador sin historial, empató con `MEM-E`. El 003 aprendió macros de programas
repetidos y pareció obtener una capacidad nueva. El 004-A lo reejecutó con
protocolo congelado, rejilla completa de 64 programas y control sin memoria a
profundidad 3 (media de 3 semillas):

| Condición | Aciertos /64 | Candidatos |
|---|---|---|
| Sin memoria, profundidad 2 | 33 (51,6 %) | 876 |
| **Sin memoria, profundidad 3** | **64 (100 %)** | 1.761 |
| Azar, mismo lenguaje, profundidad 2 | 50,7 (79,3 %) | 1.543 |
| Macros aprendidas, profundidad 2 | 54 (84,4 %) | 1.448 |
| Macros aprendidas, profundidad 3 | 64 (100 %) | 2.247 |

**No hay capacidad nueva**: sin historial y con búsqueda de tres pasos se resuelve
todo. La biblioteca ahorra 17,8 % de candidatos y pierde 15,6 pp de cobertura; por
acierto el ahorro es 2,6 %, y si se permite profundidad 3 encarece la búsqueda un
27,6 %. El control aleatorio del 003 estaba amañado: 250/560 bibliotecas
arbitrarias del mismo lenguaje eran perfectas en su conjunto.

**Precisión sobre la ablación:** el 003 borra las **macros compiladas**, no las
experiencias originales. La ventaja depende de conservar los artefactos, no
necesariamente el historial bruto. Eso convierte la consolidación en una pregunta
experimental sobre qué se puede borrar sin perder competencia, y no está medida.

JANUS sigue sin probarse: el prototipo muestra que compilar abstracciones puede
servir como prior bajo presupuesto acotado, no que la hipótesis causal se sostenga.
Detalles en `prototipo-004-validez/`.

## 12. Límites, seguridad y gobernanza

- Estado parcialmente oculto: la identificación puede ser imposible.
- Contrafactuales confabulados: el juicio del modelo nunca es prueba.
- Costo: simular y experimentar es caro; usar valor esperado de la información.
- Privacidad: las alternativas rechazadas pueden revelar información.
- Envenenamiento: una traza maliciosa puede generar una habilidad dañina.
- Gobernanza: procedencia, permisos, auditoría, rollback y caducidad.
- Autoría: la afiliación MIT es la declarada por el autor humano; la participación
  de IA debe declararse antes de un envío.

## 13. Conclusión

JANUS no es la primera memoria contrafactual. Es una propuesta para que la
memoria **sepa qué puede afirmar**: distinguir observación, inferencia,
predicción, intervención y efecto; declarar supuestos; medir restauración; y
abstenerse cuando no hay evidencia.

En un campo que ya produce contrafactuales verificados y abstracciones que se
reproducen, esa distinción puede valer más que otra capa de arquitectura.

---

## Referencias

Bareinboim, E., & Pearl, J. (2016). Causal inference and the data-fusion problem.
*PNAS, 113*(27), 7345–7352.

Chalef, D., et al. (2026). *Learning by doing: Autonomously compiling and
curating agent skills from verified traces*. arXiv:2611.01386.

DeepSeek-AI. (2024). *DeepSeek-V2: A strong, economical, and efficient
mixture-of-experts language model*. arXiv:2405.04434.

DeepSeek-AI. (2025). DeepSeek-R1 incentivizes reasoning in LLMs through
reinforcement learning. *Nature, 645*, 633–638.

Jiang, E. H., et al. (2026). *Memory as a controlled process: Learned adaptive
memory management for LLM agents*. arXiv:2607.13591.

Pakhomov, E., & Nijkamp, E. (2026). *Attributing agent failures to their history
needs an executed counterfactual*. arXiv:2611.05650.

Pearl, J. (2009). *Causality* (2nd ed.). Cambridge University Press.

Pu, H., Tang, R., & Zhang, Y. (2026). *COUNTERMEM: World-model verified
counter-factual memory for language agents*. arXiv:2609.31874.

Rosenbaum, P. R., & Rubin, D. B. (1983). The central role of the propensity score
in observational studies for causal effects. *Biometrika, 70*(1), 41–55.

Rubin, D. B. (1974). Estimating causal effects of treatments in randomized and
nonrandomized studies. *Journal of Educational Psychology, 66*(5), 688–701.

Shao, Z., et al. (2024). *DeepSeekMath: Pushing the limits of mathematical
reasoning in open language models*. arXiv:2402.03300.

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

Zhang, S., et al. (2026). *ConMem: Counterfactual multi-scenario probing for
resolving LLM memory misalignment*. arXiv:2610.33432.
