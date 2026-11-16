# 05 — Huecos y oportunidades: dónde está lo no intentado

## Criterio

Un hueco es una oportunidad si cumple tres condiciones:

1. **No está resuelto** por los sistemas del catálogo.
2. **Tiene base teórica** en la investigación revisada.
3. **Es medible** con un experimento asequible.

## Matriz de huecos

| Hueco | Estado actual | Novedad | Factibilidad | Evidencia base |
|---|---|---|---|---|
| Portabilidad procedural entre modelos | Casi inexistente | Alta | Alta | Holton et al.; CUMULUS |
| Validación causal de habilidades | Inexistente | Muy alta | Media | Pearl; Gopnik; Rubin |
| Memoria contrafactual | Inexistente en agentes | Muy alta | Media | Pearl; Lewis; Daw |
| Memoria de la ignorancia | Casi inexistente | Alta | Alta | Flavell; metacognición |
| Olvido con auditoría | Parcial (MemoryBank) | Media | Alta | Ryan y Frankland |
| Gobernanza social de la memoria | Namespaces | Alta | Media | Ostrom; Weber |
| Identidad narrativa | Prompts de persona | Alta | Media | Locke; Parfit; Conway |
| Benchmark longitudinal | Benchmarks cortos | Alta | Media | Holton; CUMULUS-Bench |

## Los tres candidatos fuertes

### 1. Portabilidad procedural (CUMULUS)

**Qué es.** Separar la semántica del procedimiento (SIR) de la sintaxis del
modelo; medir la transferencia con una matriz de portabilidad; auditar a ciegas.

**Por qué importa.** Es el único hueco con una solución arquitectónica clara y
una métrica directa. Ataca el problema de "el agente se vuelve estúpido al
cambiar de modelo".

**Riesgo.** Que la transferencia sea más parcial de lo esperado y que el costo de
la compilación no se pague.

### 2. Memoria contrafactual (JANUS)

**Qué es.** Guardar, además de lo que pasó, **lo que no pasó**: alternativas
consideradas, resultados predichos, resultados observados cuando se puede, y el
efecto causal estimado de cada decisión. Promover una habilidad solo si el
efecto causal es identificable y robusto.

**Por qué importa.** Los agentes aprenden de éxitos que pueden ser suerte.
Sin contrafactuales, consolidan supersticiones: "funcionó después de X, entonces
X fue la causa". La memoria contrafactual es la diferencia entre aprender y
racionalizar.

**Base teórica.** Causalidad de Pearl (2009), resultados potenciales de Rubin
(1974), condicionales contrafactuales de Lewis (1973), aprendizaje causal de
Gopnik et al. (2004), crédito contrafactual en RL (Daw et al., 2011).

**Riesgo.** Los contrafactuales generados por un LLM pueden ser confabulaciones.
Hay que jerarquizar la evidencia: experimento aleatorio > experimento natural >
simulación > juicio del modelo.

### 3. Memoria de la ignorancia

**Qué es.** Un registro de lo que el agente **no sabe**: preguntas abiertas,
búsquedas fallidas, supuestos no verificados, huecos de cobertura. La memoria no
solo responde; también dice qué falta.

**Por qué importa.** La metacognición es el mecanismo humano que decide cuándo
explorar, preguntar o actuar (Flavell, 1979). Un agente que solo recuerda
respuestas no sabe dónde está su borde.

**Riesgo.** Es fácil de implementar y fácil de ignorar; el valor está en que la
política de acción lo consulte.

## Por qué la memoria contrafactual es la apuesta más innovadora

1. **No está en el catálogo.** Mem0 guarda hechos, Zep relaciones temporales,
   Voyager habilidades, CUMULUS procedimientos. Ninguno guarda alternativas.
2. **Ataca un error real.** La promoción de habilidades por éxito observado
   confunde correlación con causa.
3. **Tiene una arquitectura clara.** Objetos: decisión, contrafactual, claim
   causal, procedimiento, casi-fallo, arrepentimiento.
4. **Tiene una métrica clara.** Tasa de habilidades espurias, precisión de
   identificación causal, transferencia, arrepentimiento.
5. **Se conecta con todo lo anterior.** El momento cero usa priors causales; el
   contexto se reduce a claims causales compactos; la compactación es
   consolidación contrafactual; el sueño es replay contrafactual.

## Lo que ya existe y no es lo mismo

- **Counterfactual replay en RL**: se usa para crédito y planificación, pero no
  como memoria de un agente de lenguaje.
- **Counterfactual data augmentation**: genera ejemplos contrafactuales para
  entrenar, no para recordar.
- **Causal discovery**: aprende grafos de datos, no de decisiones de agentes.
- **World models**: simulan futuros, pero no almacenan el contrafactual de una
  decisión pasada con su evidencia.

La combinación —memoria de decisiones + contrafactuales + promoción causal— no
está en la literatura de memoria agéntica.

## Propuesta de dirección

Construir **JANUS**: una capa de memoria contrafactual sobre CUMULUS.

- CUMULUS aporta el ciclo de vida y la portabilidad.
- JANUS aporta la validación causal y el crédito contrafactual.
- El resultado es una memoria que no solo recuerda lo que funcionó, sino **por
  qué funcionó y qué habría pasado si no**.

## Lo que hay que demostrar

1. Que la memoria contrafactual reduce las habilidades espurias.
2. Que mejora la asignación de crédito en tareas de horizonte largo.
3. Que los procedimientos causalmente validados transfieren mejor entre modelos.
4. Que los experimentos naturales entre agentes producen señal causal útil.
5. Que el costo de los contrafactuales se paga con menos reintentos.

Si no se demuestra, la idea queda como filosofía. El siguiente documento es el
paper que la desarrolla.
