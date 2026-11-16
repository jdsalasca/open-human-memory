# 08 — Antecedentes 2026 (tercera ola): aplicabilidad, calibración y replay

La tercera ola estrecha todavía más el hueco. Estos trabajos no son periféricos:
tocan exactamente las decisiones que JANUS-C quiere controlar.

## 1. SkillApt — relevancia no es aplicabilidad (2026)

**Qué hace.** Separa retrieval (¿es relevante?) de aplicabilidad (¿vale la pena
cargarla ahora?). Usa pares WITH/WITHOUT de la misma skill en el mismo estado,
estima utilidad marginal y decide `Load` o `Abstain`. El modelo base y el
contenido de la skill no cambian; solo la política externa.

**Resultados.** 20 skills, 160 estados held-out: 81,9% → 91,3% de éxito tras 12
pares de evidencia por skill. Activa la skill en 26,3% de los estados, frente a
98,8% de un controlador zero-shot.

**Lo que cubre.** Aplicabilidad calibrada por evidencia pareada; abstención.

**Lo que deja abierto.** No usa contrafactuales verificados ni certificados de
restauración; no mide daño por look-alike; no decide entre retener, reconstruir,
promover e investigar.

**arXiv:** 2609.26863.

## 2. BASM — límites de aplicabilidad (Lin et al., Findings EMNLP 2026)

**Qué hace.** Añade a cada skill campos de aplicabilidad, riesgo, evitación y
recuperación, aplicados en retrieval, formato y ejecución. Convierte la imitación
incondicional en decisión condicionada al estado.

**Resultados.** Hasta +23,8% en AppWorld, +5,0% en BFCL, −4,6% de éxito de ataque
en AgentDojo; menos pasos en AppWorld. La ablación atribuye el efecto a la
atención a los límites, no al largo del prompt.

**Lo que cubre.** Límites explícitos; reducción de la "trampa de imitación".

**Lo que deja abierto.** Los límites son texto; no hay calibración estadística ni
certificado de restauración.

**Anthology:** 2026.findings-emnlp.1141.

## 3. MemCalib — calibración del uso de memoria (2026)

**Qué hace.** Benchmark de 1.500 ejemplos que mide si el modelo da a cada
proposición de memoria el nivel de influencia adecuado: `Ignore`, `Bound` o
`Control`. Mide sobre-uso, sub-uso y exactitud.

**Hallazgo.** Incluso modelos frontera fallan en calibrar el uso; el sobre-uso es
más frecuente que el sub-uso en casi todos. Modelos más grandes no
necesariamente calibran mejor.

**Lo que cubre.** El problema de "memoria entregada pero mal usada".

**Lo que deja abierto.** No decide qué memorizar ni cuándo verificar; mide uso.

**arXiv:** 2609.24259.

## 4. MemTrial — cuándo confiar en la memoria (2026)

**Qué hace.** En agentes de portafolio, mide el efecto de cada experiencia con un
pequeño experimento diseñado en cada fecha, agrega valores y solo actúa cuando
esos valores predicen fechas no vistas; hasta entonces usa un ancla conservadora
y se abstiene.

**Hallazgo.** El crédito por resultado sigue al mercado, no a la experiencia. La
prueba de confianza casi nunca pasa en mercados reales; MemTrial se mantiene
cerca del ancla 1/N, mientras otros agentes quedan atrás.

**Lo que cubre.** Confianza calibrada por predicción fuera de muestra;
abstención; experimentos diseñados.

**Lo que deja abierto.** Dominio específico; no memoria procedural general ni
contrafactuales ejecutables.

**arXiv:** 2610.11732.

## 5. CMI — selección causal de memoria (Srivastava, 2026)

**Qué hace.** Estima la contribución causal de memorias candidatas con
intervenciones controladas y selecciona solo las de efecto positivo y estable.
Benchmark Causal-LoCoMo.

**Resultados.** Mejor task score y F1 de memoria útil; rechazo de memoria mala
0,99; adopción de memoria envenenada 0,00; selecciona menos de una memoria en
promedio.

**Lo que cubre.** Selección causal de memoria en el punto de uso.

**Lo que deja abierto.** No promueve procedimientos ni mide portabilidad;
depende de intervenciones sobre el contexto.

**arXiv:** 2605.17641.

## 6. State-Complete Replay (Peimani, 2026)

**Qué hace.** Define condiciones de validez para replay contrafactual: hay que
restaurar el estado que afecta la intervención y su continuación, incluido
estado de herramientas, sesión y usuario latente. Propone un **Replay Validity
Certificate**.

**Hallazgo.** En ReplayShop, el replay solo visible coincide con la rama en 20/20
pero recupera el efecto equivocado en 3. El replay completo recupera todos los
efectos de referencia. En ToolSandbox, el estado de herramientas y el usuario
latente contribuyen por separado.

**Lo que cubre.** Certificado de restauración; estados ocultos.

**Lo que deja abierto.** No es un sistema de memoria; no decide promoción.

## 7. GCJR — familias de reparación mínima (2026)

**Qué hace.** Recupera todos los conjuntos minimales de eventos cuya intervención
restaura el éxito, usando un grafo de dependencias y replay. Distingue necesidad
conjunta de suficiencia alternativa.

**Resultados.** 1.000 Family Exact Match en 90 casos; reduce llamadas de replay
55,1% frente a búsqueda exhaustiva. El replay de un solo evento pierde
reparaciones conjuntamente necesarias.

**Lo que cubre.** El problema de la ablación simple: la causa puede ser conjunta.

**Lo que deja abierto.** Asistido por oráculo; no genera reparaciones.

**arXiv:** 2608.29228.

## 8. CRR — counterfactual rollout replay (2026)

**Qué hace.** Selecciona puntos de decisión, restaura el estado, muestrea una
acción alternativa y hace rollout; usa la diferencia de retorno como ventaja.
Entrena con GRPO-like en SWE-bench.

**Resultados.** 41,7% vs 36,7% con el mismo wall-clock en SWE-bench Verified
(+5,0 puntos), incluyendo overhead de fork.

**Lo que cubre.** Replay contrafactual para entrenamiento, no solo memoria.

**Lo que deja abierto.** Requiere restauración barata y fiable; continuaciones
estocásticas siguen siendo un límite.

**arXiv:** 2609.33875.

## 9. OAS — retener o consolidar según presupuesto (2026)

**Qué hace.** Descompone el valor de consolidar en cobertura y reemplazo; aprende
una política de retención vs consolidación con calibración de daño.

**Resultados.** En LongMemEval, consolidar mejora hasta 48 puntos con presupuesto
ajustado; retener es mejor con presupuesto holgado. El punto de cruce depende de
la longitud de la evidencia, no de un umbral fijo de tokens.

**Lo que cubre.** La decisión retener vs consolidar bajo presupuesto.

**Lo que deja abierto.** No incluye verificación contrafactual ni portabilidad.

**arXiv:** 2607.17545.

## 10. MERIT — evaluación consciente del costo (2026)

**Qué hace.** Evalúa memoria por "¿cambia lo que el agente hace, a qué costo y
cómo falla?", no por recall.

**Hallazgo.** Arquitecturas indistinguibles en recall difieren hasta 0,70 en task
success rate; la memoria más precisa es 2,7–3,9× menos económica que la más
eficiente; los agentes ignoran casi la mitad de los hechos recuperados.

**Lo que cubre.** Costo, uso y fallo; no solo recuperación.

**arXiv:** 2609.05441.

## 11. MemUse — memoria en el punto de uso (Xu, Li y Xu, 2026)

**Qué hace.** Evalúa cada entrega de memoria contra lo que el agente ya podía ver,
siguiendo acciones y consecuencias.

**Hallazgo.** 89 de 383 episodios con uso beneficioso fallaron; 5 de 16 con uso
dañino pasaron. El resultado de la tarea oculta el efecto de la memoria.

**Lo que cubre.** Uso real, no entrega.

**arXiv:** 2611.01718.

## 12. Conformal en trayectorias (Li et al., EMNLP 2026)

**Qué hace.** Muestra que la calibración conformal por paso no preserva la
cobertura a lo largo de una trayectoria: 10% nominal → 83,5% de miscobertura en
un agente de 15 pasos. Propone un wrapper con α-spending.

**Lo que implica.** La aplicabilidad de una skill no se puede calibrar paso a
paso; hay que calibrar a nivel de trayectoria.

**Anthology:** 2026.emnlp-main.1808.

## Tabla de solapamiento

| Decisión | Ya cubierta por | Sigue abierto |
|---|---|---|
| Retener vs consolidar | OAS | Con certificado causal |
| Cargar vs abstenerse | SkillApt, BASM | Con contrafactual verificado |
| Memorizar vs no | ConMem | Con costo y riesgo |
| Seleccionar memoria | CMI | Con promoción procedural |
| Confiar en memoria | MemTrial | General, no portafolios |
| Calibrar uso | MemCalib | A nivel de trayectoria |
| Restaurar estado | Peimani, Pakhomov, GCJR | Integrado en promoción |
| Reparar fallos | GCJR | Generar reparaciones |
| Entrenar con contrafactuales | CRR | Política de memoria, no pesos |
| Evaluar costo/uso | MERIT, MemUse | Longitudinal con deriva |

## Consecuencia

Ninguna pieza es nueva. La posible contribución es **integrar las decisiones**
—retener, reconstruir, promover, investigar, abstenerse— bajo un presupuesto, con
certificados por objeto y calibración por trayectoria. Eso es JANUS-C.
