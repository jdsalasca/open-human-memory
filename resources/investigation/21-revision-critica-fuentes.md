# 21 - Revisión crítica de fuentes v2: dos ejes, no una escala

> **Actualizado 2026-11-16.** La revisión de fuentes ya se ejecutó de forma
> estructurada (`revision-sistematica/`, 31 trabajos). Los dos ejes siguen
> vigentes; la matriz de antecedentes que este documento inspiraba está
> sustituida. Estado de cada afirmación: `docs/registro-de-afirmaciones.md`.

**Estado:** reescrito tras la segunda auditoría. Sustituye la escala única A/B/C/D
por **dos evaluaciones separadas**: evidencia de origen y evidencia de
transferencia.

## 1. El error de la versión anterior

La v1 asignaba una letra a un mecanismo (por ejemplo, `[A]` a la consolidación)
y esa letra se leía como si validara también el componente artificial. No es
válido: un fenómeno puede estar probado y su traducción computacional no.

Ahora cada mecanismo tiene dos notas:

- **Origen (O):** qué tan sólido es el fenómeno en su disciplina.
  - **A:** consenso, meta-análisis, replicación.
  - **B:** evidencia sólida con límites.
  - **C:** teoría o hipótesis.
  - **D:** metáfora o evidencia débil.
- **Transferencia (T):** qué demuestra que el mecanismo artificial inspirado en
  ese fenómeno mejora el sistema.
  - **3:** experimento comparativo con líneas base fuertes y réplica.
  - **2:** experimento comparativo sin réplica o con líneas base débiles.
  - **1:** prototipo o estudio de caso.
  - **0:** solo analogía, sin implementación.

Una fuente puede ser **A/0**. De hecho, la mayoría de los mecanismos de este
proyecto lo son.

## 2. Neurociencia

| Mecanismo | Origen | Transferencia | Comentario |
|---|---|---|---|
| Sistemas complementarios hipocampo–corteza | A/B | 0 | Teoría sólida; no prueba dos almacenes artificiales |
| Replay durante el sueño | A | 0 | Fuerte en biología; no prueba que un job de replay mejore un LLM |
| Triaje de memoria | B | 0 | Revisión integradora; sin implementación comparable |
| Homeostasis sináptica | B | 0 | Teoría con apoyo; sin análogo artificial validado |
| Reconsolidación | B | 0 | Condiciones límite; no equivale a "recuperar actualiza peso" |
| Olvido adaptativo | A/B | 1 | MemoryBank implementa decaimiento; no auditoría |
| Engramas | B | 0 | Roedores; no traduce a nodos de memoria |
| Neuromoduladores | B | 0 | Canales de saliencia plausibles; sin validación |
| Mapas cognitivos para conocimiento | B | 0 | Inspira grafos; no prueba que un grafo mejore |
| Memoria constructiva y futuro | B | 0 | Marco; no mecanismo |

**Lectura:** la neurociencia sostiene la **necesidad** de un ciclo de vida, no un
algoritmo. Casi todo es A/0 o B/0.

## 3. Biología social y comparada

| Mecanismo | Origen | Transferencia | Comentario |
|---|---|---|---|
| Dialectos y matrilinas de orcas | B | 0 | Observacional; inspira dialecto, no lo valida |
| Menopausia y liderazgo | B | 0 | Correlacional; inspira custodios |
| Enseñanza de orcas | B | 0 | Observacional; inspira `teach()` |
| Quórum en hormigas | A | 1 | Protocolo implementable; no prueba verdad |
| Estigmergia | A | 1 | Trazas con evaporación; usado en ACO, no en memoria de agentes |
| Memoria episódica-like en córvidos | B | 0 | Inspira qué/dónde/cuándo |
| Memoria inmune | A | 0 | Inspira selección; no se implementó |
| Moho sin neuronas | B | 0 | Memoria externalizada; caso aislado |
| Redes micorrícicas | D | 0 | Evidencia débil; no usar |
| Aprendizaje en plantas | C | 0 | Controversial; solo primado |

**Lectura:** los protocolos de coordinación (quórum, estigmergia) son los únicos
con traducción parcial. El resto es inspiración.

## 4. Sociología

| Mecanismo | Origen | Transferencia | Comentario |
|---|---|---|---|
| Memoria transactiva | A | 1 | Meta-análisis; directorio implementable, sin validación en agentes |
| Comunidades de práctica | B | 0 | Onboarding; no medido |
| Cultura acumulativa | A/B | 0 | Fidelidad de transmisión; no medida entre modelos |
| Gobernanza de comunes | B | 0 | Marco de diseño; sin experimento |
| Burocracia y legitimidad | C | 0 | Interpretativa; solo se conserva trazabilidad |
| Sesgo colectivo en LLM | B | 2 | Ashery et al. muestra el fenómeno; no una solución |
| Vínculos débiles | B | 0 | Inspira enlaces entre pods |

**Lectura:** la memoria transactiva es la pieza más implementable; su
transferencia a agentes sigue sin probarse.

## 5. Psicología y aprendizaje humano

| Mecanismo | Origen | Transferencia | Comentario |
|---|---|---|---|
| Memoria reconstructiva | A | 0 | Inspira fuente vs. interpretación |
| Desinformación | A | 0 | Inspira procedencia |
| Falsos recuerdos | A | 0 | Inspira verificación |
| Olvido inducido por recuperación | B | 0 | Inspira diversidad; no contador |
| Inhibición colaborativa | B | 0 | Inspira buffers individuales |
| Contagio social | B | 0 | Inspira auditoría ciega |
| Sesgo de confirmación | A | 0 | Inspira contraevidencia |
| Metacognición | B | 1 | Inspira calibración; sin implementación validada |
| Espaciado | A | 0 | Inspira repasos; no probado en agentes |
| Práctica de recuperación | A | 0 | **No** justifica refuerzo artificial |
| Intercalado | B | 0 | Inspira replay mezclado; no probado |
| Dificultades deseables | B | 0 | Inspira no compactar de más |
| Chunking | A | 1 | Inspira unidades; SIR es una forma |
| Gist vs. verbo | B | 0 | Inspira preservar significado |
| Esquemas | B | 0 | Inspira consolidación |

**Lectura:** la psicología es la fuente más aplicable para **qué preservar y qué
errores evitar**, pero casi nada tiene transferencia medida.

## 6. Aprendizaje humano vs. máquina y contexto

| Mecanismo | Origen | Transferencia | Comentario |
|---|---|---|---|
| Eficiencia de muestra humana | B | 0 | Inspira priors; no se iguala con retrieval |
| Interferencia catastrófica | A | 3 | EWC/replay son evidencia comparativa en redes |
| Trade-off transferencia/interferencia | B | 2 | Holton et al. lo miden en humanos y redes |
| Lost in the Middle | A/B | 3 | Fenómeno robusto en LLM |
| RULER | B | 3 | Benchmark; longitud efectiva |
| LongICLBench | B | 2 | Benchmark; rendimientos decrecientes |
| ICL bayesiano | B | 1 | Teoría con experimentos |
| Induction heads | B | 1 | Mecanicista |
| ICL como gradiente | C | 1 | Régimen restringido |

**Lectura:** el contexto es el área con más evidencia de transferencia directa
(porque se mide en LLM). La comparación humano–máquina es prometedora pero joven.

## 7. Memoria de agentes 2026

| Sistema | Origen | Transferencia | Comentario |
|---|---|---|---|
| Zep Agent Skills | A/B | 2 | Producción; benchmarks de replay, no tareas nuevas |
| MSCE | B | 2 | Evidencia multi-benchmark; ganancia heurística, no causal |
| AFTER | B | 2 | Benchmark de transferencia entre roles y backbones |
| Trace2Skill | B | 2 | Transferencia entre escalas y familias |
| COUNTERMEM | B | 2 | 12 benchmarks; requiere estados restaurables |
| ConMem | B | 1 | Benchmark de admisión; no acumulación |
| MemCon | B | 2 | Control adaptativo; consolidación/olvido no probados |
| More Memory, Worse Agents | B | 2 | Anti-persistencia; evidencia asociacional de error reproduction |
| What Is This Memory Useful For? | B | 1 | Utilidad factual; sin efecto en coding |
| TANGLE | B | 1 | Benchmark de conflicto; no arquitectura |
| Attributing Agent Failures... | B | 0 | Estándar metodológico; sin resultado conductual |

**Lectura:** aquí sí hay transferencia 2, pero con límites: replay de tareas,
benchmarks simulados, ganancias heurísticas, dependencia de verificadores.

## 8. Los huecos reales después de la segunda ola

1. **Identificación causal bajo estado parcialmente oculto.** COUNTERMEM
   verifica alternativas cuando el estado se puede copiar; no resuelve
   confusores no observados.
2. **Acumulación longitudinal con deriva real.** Los benchmarks miden ciclos,
   no meses de cambios de API/modelo/requisitos.
3. **Transferencia procedural entre modelos con tareas nuevas.** AFTER y
   Trace2Skill miden transferencia, pero no en tareas fuera de distribución
   durante meses.
4. **Incertidumbre e ignorancia como contenido.** TANGLE mide conflicto; no hay
   un ledger de ignorancia con agenda experimental.
5. **Anti-persistencia selectiva.** More Memory, Worse Agents compara diseños;
   no hay una política que decida cuándo persistir y cuándo reconstruir.
6. **Utilidad en tareas procedimentales.** Yang et al. no encuentran efecto en
   coding; falta medir utilidad condicionada a tarea en procedimientos.

## 9. Veredicto

- La evidencia **sostiene el problema**: la memoria como almacén no produce
  competencia acumulativa.
- La evidencia **sostiene principios de diseño**: dos velocidades, consolidación,
  olvido selectivo, procedencia, verificación, transmisión.
- La evidencia **no sostiene** una arquitectura única, una simulación neuronal
  literal, ni la superioridad de CUMULUS/JANUS.
- La mayoría de los mecanismos biológicos son **A/0**: inspiran, no validan.
- La innovación debe buscarse donde hay menos evidencia pero mejor teoría:
  **incertidumbre, identificación causal y corrección**.

## 10. Cómo se actualiza

Este documento se acompaña de `25-protocolo-fuentes-primarias.md`. Cada
afirmación de ausencia debe tener búsqueda registrada, fecha y criterios. Sin
eso, se escribe "no lo hemos encontrado", no "no existe".
