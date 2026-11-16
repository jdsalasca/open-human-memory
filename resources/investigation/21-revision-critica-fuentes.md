# 21 — Revisión crítica de fuentes: qué sostiene el diseño y qué es metáfora

## 1. Método

Leí las fuentes primarias y revisiones citadas en los documentos 01–20 y las
clasifiqué por **tipo de evidencia** y **grado de confianza**. No basta con que
un paper sea famoso: importa si mide lo que afirma, en qué escala y con qué
límites.

Escala:

- **A — Consenso o evidencia convergente:** replicado, meta-análisis o múltiples
  líneas independientes.
- **B — Sólido con límites:** evidencia experimental o longitudinal, pero con
  debate, muestra pequeña o condiciones específicas.
- **C — Teoría o hipótesis:** plausible, con apoyo parcial, sin validación
  convergente.
- **D — Metáfora o evidencia débil:** atractivo narrativo, no base para diseño.

## 2. Neurociencia

| Fuente / idea | Evidencia | Confianza | Uso |
|---|---|---|---|
| Sistemas complementarios hipocampo–corteza (McClelland et al., 1995; Kumaran et al., 2016) | Teoría con apoyo experimental amplio | A/B | Arquitectura de dos velocidades |
| Replay durante el sueño (Wilson y McNaughton, 1994; Rasch y Born, 2013) | Registros neuronales + estudios de comportamiento | A | Consolidación offline |
| Triaje de memoria (Stickgold y Walker, 2013) | Revisión integradora | B | Selección, no copia |
| Homeostasis sináptica (Tononi y Cirelli, 2014) | Teoría con apoyo parcial | B | Poda global |
| Reconsolidación (Nader et al., 2000) | Experimental, con condiciones límite | B | Recuperar modifica |
| Olvido adaptativo (Richards y Frankland, 2017; Ryan y Frankland, 2022) | Revisión + experimentos | A/B | Olvido como función |
| Engramas (Josselyn et al., 2015) | Experimental en roedores | B | Recuerdo como ensamble |
| Neuromoduladores (Schultz et al., 1997; Hasselmo, 1999; Aston-Jones y Cohen, 2005) | Experimental sólido, pero mapeo funcional | B | Canales de saliencia |
| Mapas cognitivos para conocimiento (Behrens et al., 2018) | Teoría con evidencia neural | B | Grafo relacional |
| Memoria constructiva y futuro (Schacter y Addis, 2007) | Revisión | B | Memoria para simular |

**Lectura.** La neurociencia sostiene con fuerza la **necesidad de un ciclo de
vida** (dos velocidades, consolidación, olvido), no un algoritmo específico. La
analogía con el sueño es buena para diseñar una fase offline; no para afirmar
que un resumen es sueño.

## 3. Biología social y comparada

| Fuente / idea | Evidencia | Confianza | Uso |
|---|---|---|---|
| Dialectos y matrilinas de orcas (Ford, 1991; Deecke et al., 2000) | Observación longitudinal | B | Dialecto y transmisión |
| Menopausia y liderazgo (Brent et al., 2015) | Correlacional, muestra limitada | B | Custodios |
| Enseñanza de orcas (Guinet y Bouvier, 1995) | Observación detallada | B | `teach()` |
| Quórum en hormigas (Pratt et al., 2002) | Experimental | A | Promoción por quórum |
| Estigmergia (Grassé, 1959; Goss et al., 1989) | Experimental/modelado | A | Trazas que decaen |
| Memoria episódica-like en córvidos (Clayton y Dickinson, 1998) | Experimental | B | Qué/dónde/cuándo |
| Memoria inmune (Ahmed y Gray, 1996) | Consenso biomédico | A | Selección y amplificación |
| Moho sin neuronas (Nakagaki et al., 2000; Reid et al., 2012) | Experimental, pocos estudios | B | Memoria externalizada |
| Redes micorrícicas (Simard et al., 1997; Karst et al., 2023) | Evidencia débil y sobreinterpretada | D | No usar como base |
| Aprendizaje en plantas (Gagliano et al., 2014) | Controversial | C | Solo como primado |

**Lectura.** Lo más sólido es la coordinación distribuida (quórum, estigmergia) y
la memoria por selección (inmune). Lo más frágil es la interpretación romántica
de la naturaleza ("wood wide web"). La biología social da **protocolos**, no
pruebas de que un agente deba tener conciencia.

## 4. Sociología

| Fuente / idea | Evidencia | Confianza | Uso |
|---|---|---|---|
| Memoria transactiva (Wegner, 1987; Ren y Argote, 2011) | Meta-análisis de equipos | A | Directorio de expertise |
| Comunidades de práctica (Lave y Wenger, 1991) | Etnografía y teoría | B | Onboarding periférico |
| Cultura acumulativa (Tomasello, 1999; Henrich, 2015) | Evidencia comparada | A/B | Fidelidad de transmisión |
| Gobernanza de comunes (Ostrom, 1990) | Estudios de caso comparados | B | Reglas de memoria |
| Burocracia y legitimidad (Weber, 1922) | Teoría interpretativa | C | Procedencia y regímenes |
| Sesgo colectivo en LLM (Ashery et al., 2025) | Experimental | B | Riesgo de la capa social |
| Vínculos débiles (Granovetter, 1973) | Sociología empírica | B | Puentes entre pods |

**Lectura.** La memoria transactiva es la pieza sociológica con mejor evidencia y
la más directamente implementable. Weber es valioso como marco de gobernanza,
pero no es evidencia empírica. Ostrom es una guía de diseño, no una ley.

## 5. Psicología y aprendizaje humano

| Fuente / idea | Evidencia | Confianza | Uso |
|---|---|---|---|
| Memoria reconstructiva (Bartlett, 1932) | Experimental clásico | A | Fuente vs. interpretación |
| Desinformación (Loftus y Palmer, 1974) | Experimental replicado | A | No reescribir originales |
| Falsos recuerdos (Roediger y McDermott, 1995) | Experimental replicado | A | Verificación |
| Olvido inducido por recuperación (Anderson et al., 1994) | Experimental | B | Diversidad en recall |
| Inhibición colaborativa (Weldon y Bellinger, 1997) | Experimental | B | Buffers individuales |
| Contagio social (Roediger et al., 2001) | Experimental | B | Procedencia y auditoría |
| Sesgo de confirmación (Nickerson, 1998) | Revisión | A | Contraevidencia |
| Metacognición (Flavell, 1979; Nelson y Narens, 1990) | Teoría con apoyo | B | Gate de confianza |
| Espaciado (Cepeda et al., 2006) | Meta-análisis | A | Repasos |
| Práctica de recuperación (Roediger y Karpicke, 2006) | Experimental replicado | A | Preguntar antes de mostrar |
| Intercalado (Rohrer y Taylor, 2007) | Experimental | B | Replay mezclado |
| Dificultades deseables (Bjork y Bjork, 2011) | Revisión | B | No compactar de más |
| Práctica deliberada (Ericsson et al., 1993; Macnamara et al., 2014) | Meta-análisis con crítica | B | Feedback, no solo repetición |
| Chunking (Miller, 1956; Chase y Simon, 1973) | Experimental clásico | A | Unidades de compresión |
| Gist vs. verbo (Reyna y Brainerd, 1995) | Teoría con apoyo | B | Preservar significado |
| Esquemas (Ghosh y Gilboa, 2014; Gilboa y Marlatte, 2017) | Revisión | B | Consolidación |

**Lectura.** La psicología es la fuente más directly aplicable: dice qué preservar
y qué errores evitar. La memoria reconstructiva y el contagio social justifican
procedencia y auditoría ciega.

## 6. Humano vs. máquina y contexto

| Fuente / idea | Evidencia | Confianza | Uso |
|---|---|---|---|
| Eficiencia de muestra humana (Kühl, 2022; Lake et al., 2015) | Experimental | B | Priors y estructura |
| Interferencia catastrófica (McCloskey y Cohen, 1989; French, 1999) | Consenso en redes | A | Aislamiento por dominio |
| EWC / replay (Kirkpatrick et al., 2017; Rolnick et al., 2019) | Experimental | A | Estabilidad |
| Trade-off transferencia/interferencia (Holton et al., 2026) | Estudio nuevo, amplio | B | Medir ambos |
| Lost in the Middle (Liu et al., 2023) | Experimental robusto | A/B | Orden y posición |
| RULER (Hsieh et al., 2024) | Benchmark | B | Longitud efectiva |
| LongICLBench (Li et al., 2024) | Benchmark | B | Rendimientos decrecientes |
| ICL bayesiano (Xie et al., 2022) | Teoría con experimentos | B | Contexto como inferencia |
| Induction heads (Olsson et al., 2022) | Mecanicista | B | Copia de patrones |
| ICL como gradiente (von Oswald et al., 2023) | Teoría restringida | C | No generalizar |

**Lectura.** La evidencia sobre contexto es fuerte en el fenómeno (más no es
mejor, la posición importa) y más débil en la explicación (varias teorías
compiten). La comparación humano–máquina es prometedora pero joven.

## 7. Filosofía

La filosofía del contexto (Gadamer, Wittgenstein, Stalnaker, Sperber y Wilson,
Clark y Chalmers) no es evidencia empírica. Es un **marco interpretativo** que
ayuda a formular preguntas: qué es el terreno común, qué es una affordance, qué
hace que un recuerdo sea "mío". No se puede citar como prueba de que un agente
necesite tal o cual arquitectura.

**Lectura.** Útil para diseño y para evitar reduccionismos; peligrosa si se usa
como justificación científica.

## 8. Los huecos de evidencia más importantes

1. **Transferencia procedural entre modelos:** no hay estudios directos. Holton
   et al. estudian transferencia de tareas, no de procedimientos entre modelos.
2. **Memoria de agentes a meses:** los benchmarks miden conversaciones o tareas,
   no meses de trabajo real.
3. **Memoria contrafactual:** no existe un sistema de memoria de agentes que
   trate los contrafactuales como objetos de primera clase.
4. **Gobernanza de memoria:** poca evidencia empírica sobre qué reglas funcionan
   en sociedades de agentes.
5. **Olvido con auditoría:** MemoryBank prueba decaimiento, no auditoría.

## 9. Veredicto

- La evidencia **sostiene el problema**: la memoria como almacén no produce
  competencia acumulativa.
- La evidencia **sostiene los principios**: dos velocidades, consolidación,
  olvido selectivo, saliencia, procedencia, transmisión verificada.
- La evidencia **no sostiene** una arquitectura única ni una simulación neuronal
  literal.
- La mayor oportunidad de innovación está donde la evidencia es fina pero la
  teoría es fuerte: **memoria causal/contrafactual**.

La biología no prueba que un agente deba tener un hipocampo digital. Prueba que
cualquier sistema que aprenda durante meses necesita decidir qué conservar, qué
transformar y qué soltar. La novedad no está en copiar la biología; está en
construir la institución que la biología sugiere y que nadie ha construido para
agentes.
