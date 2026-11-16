# 06 — Estado del arte computacional: qué existe y dónde está el hueco

## 1. El problema que todos intentan resolver

**Olvido catastrófico** (McCloskey y Cohen, 1989; French, 1999): una red que
aprende una tarea nueva olvida la anterior porque ajusta los mismos pesos. Es el
dilema estabilidad–plasticidad. Los LLM no escapan: su "memoria" es el contexto
y el ajuste fino; ambos son frágiles.

Las soluciones conocidas caen en cuatro familias:

1. **Memoria externa** (RAG, bases vectoriales, grafos): no toca los pesos.
2. **Consolidación en contexto** (resúmenes, reflexión, paging): reescribe el
   contexto.
3. **Aprendizaje continuo** (replay, regularización, módulos): toca los pesos o
   los protege.
4. **Orquestación multi-agente**: distribuye el conocimiento entre agentes.

Cada familia resuelve una parte. Ninguna resuelve el ciclo completo.

## 2. Sistemas de memoria para agentes

### 2.1 MemGPT / Letta (Packer et al., 2023)

Trata el contexto como memoria RAM y el almacenamiento externo como disco:
paginación, edición de memoria por el propio agente, y un bucle de gestión.
Introdujo la metáfora de sistema operativo para la memoria.

**Aporte:** el agente administra su propia memoria; el contexto es un recurso
gestionado, no un vertedero.
**Límite:** la gestión es local a la sesión; no hay consolidación biológica ni
capa social.

### 2.2 Generative Agents (Park et al., 2023)

El **memory stream**: registro en lenguaje natural de todo lo observado. La
recuperación combina tres señales:

```
score = α_recencia · recencia + α_importancia · importancia + α_relevancia · relevancia
```

La importancia la puntúa el LLM; la reflexión se dispara cuando la importancia
acumulada supera un umbral (~150). Es el antecedente más citado de memoria
agéntica con reflexión.

**Aporte:** demuestra que recuperar por relevancia sola es insuficiente; la
importancia y la recencia importan.
**Límite:** memoria plana, sin olvido real, sin dominios, sin transmisión entre
agentes.

### 2.3 Mem0 (Chhikara et al., 2025)

Extracción de hechos, consolidación y actualización incremental; variante con
grafo (Mem0g). Optimiza el costo de contexto y la consistencia en diálogos
multi-sesión.

**Aporte:** pipeline de extracción + deduplicación + actualización, que es
justo la parte que un RAG ingenuo no tiene.
**Límite:** orientado a memoria de usuario/conversación, no a aprendizaje de
tareas ni a sociedades de agentes.

### 2.4 Zep / Graphiti (Rasmussen et al., 2025)

Grafo de conocimiento **temporal**: entidades, relaciones con validez temporal
(bi-temporal), episodios como fuente. Reporta 94.8% en DMR frente a 93.4% de
MemGPT, y mejoras de hasta 18.5% en LongMemEval con menor latencia.

**Aporte:** el tiempo es de primera clase; una relación puede ser cierta en un
intervalo y dejar de serlo. Esto es imprescindible para "por qué cambiamos de
decisión".
**Límite:** sigue siendo recuperación sobre un grafo; la consolidación y el
olvido no son el foco.

### 2.5 HippoRAG (Gutiérrez et al., 2024; 2025)

Inspirado en la **teoría del indexado hipocámpico**: un grafo de conocimiento
hace de índice; la recuperación usa propagación tipo PageRank para asociar
entidades y responder preguntas multi-hop. La versión 2 extiende a aprendizaje
continuo no paramétrico.

**Aporte:** demuestra que la inspiración neurológica puede producir mejoras
medibles en recuperación asociativa.
**Límite:** es recuperación, no ciclo de vida; no modela consolidación, olvido ni
sociedad.

### 2.6 MemoryBank (Zhong et al., 2024)

Aplica la curva de Ebbinghaus: los recuerdos decaen y se refuerzan con el uso.
Es uno de los pocos sistemas con olvido explícito.

**Aporte:** el olvido como función, no como bug.
**Límite:** decaimiento uniforme; sin saliencia multidominio ni gobernanza.

### 2.7 GraphRAG (Edge et al., 2024)

Construye comunidades jerárquicas en el grafo y genera resúmenes por comunidad
para preguntas globales. Útil para "¿de qué trata este corpus?".

**Aporte:** la estructura jerárquica permite resumir sin perder ejes.
**Límite:** es indexación de corpus, no memoria de agente.

### 2.8 A-MEM (Xu et al., 2025)

Memoria tipo Zettelkasten: cada nota tiene contexto, etiquetas y enlaces; el
sistema genera enlaces nuevos al insertar. Se acerca a una red de recuerdos con
estructura propia.

**Aporte:** la asociación explícita entre recuerdos, no solo similitud.
**Límite:** sin consolidación ni olvido; el grafo crece sin metabolismo.

### 2.9 Sleep-time compute (Lin et al., 2025)

Calcular offline, antes de que llegue la consulta: reorganizar memoria, anticipar
preguntas. Inspirado en el sueño y en la consolidación.

**Aporte:** separa el costo de pensar del costo de responder; el "sueño" es una
fase de cómputo.
**Límite:** es una técnica de inferencia, no una arquitectura de memoria
completa.

## 3. Arquitecturas cognitivas clásicas

- **ACT-R** (Anderson et al., 2004): memoria declarativa con activación
  `B_i = ln(Σ_j t_j^{-d})` — frecuencia y recencia — más activación asociativa
  y ruido; memoria procedural con reglas de producción. Es la formalización más
  madura de "memoria declarativa + procedural".
- **Soar** (Laird, 2012): chunking; cuando una regla se aplica repetidamente, se
  compila en un chunk. Análogo funcional de la automaticidad.
- **CLARION** (Sun): implícito/explícito en capas.
- **LIDA / Global Workspace** (Baars, 1988; Dehaene, 2014): la conciencia como
  broadcast de un espacio de trabajo común. Relevante para el "qué se atiende",
  no para el almacenamiento.

**Aporte:** llevan décadas modelando memoria y aprendizaje con métricas.
**Límite:** no usan LLM; su vocabulario simbólico no captura el conocimiento
difuso de un modelo de lenguaje.

## 4. Aprendizaje continuo en redes

- **EWC** (Kirkpatrick et al., 2017): protege los pesos importantes con una
  penalización de Fisher. Estabilidad sin olvidar.
- **Replay** (Rolnick et al., 2019): mezclar datos viejos con nuevos.
- **Redes progresivas**: módulos nuevos por tarea.
- **Memorias asociativas modernas** (Ramsauer et al., 2021): Hopfield
  actualizado; capacidad de almacenamiento mucho mayor.

**Aporte:** técnicas probadas para no destruir lo aprendido.
**Límite:** requieren acceso a pesos o datos de entrenamiento; un agente de
producción normalmente no los tiene.

## 5. Neuromodulación en RL

La dopamina como error de predicción de recompensa (Schultz, Dayan y Montague,
1997) es el puente más limpio entre neurociencia y algoritmo: una señal escalar
que modula el aprendizaje. Se usa en RL y en meta-aprendizaje.

**Aporte:** demuestra que "neuromodulador" puede ser una variable de control, no
una metáfora.
**Límite:** en LLM no hay una señal de recompensa densa por token; hay que
inventarla (resultado de tarea, corrección del usuario, tests).

## 6. Cultura en poblaciones de agentes

Ashery et al. (2025, *Science Advances*): poblaciones descentralizadas de agentes
LLM desarrollan convenciones sociales espontáneas y sesgos colectivos, incluso si
cada individuo parece neutral. La memoria compartida y la comunicación local
basta para que emerja una norma.

**Aporte:** confirma que la capa social no es decorativa; cambia el resultado.
**Límite:** describe el fenómeno, no diseña gobernanza.

## 7. Benchmarks: qué miden y qué no

| Benchmark | Mide | No mide |
|---|---|---|
| LoCoMo (Maharana et al., 2024) | Recall en conversaciones largas | Progreso entre tareas, transferencia |
| LongMemEval (Wu et al., 2025) | Memoria a largo plazo en asistencia | Consolidación, olvido, sociedad |
| DMR (MemGPT) | Recuperación profunda | Ciclo de vida |
| Needle-in-a-haystack | Localización exacta | Comprensión, asociación |

El hueco: **ningún benchmark mide si un agente deja de repetir errores tras un
millón de tokens.** Miden recuperación puntual, no acumulación.

## 8. El hueco real

1. **La memoria se trata como almacén, no como ciclo de vida.** Casi todos
   optimizan retrieval; pocos optimizan codificación, consolidación y olvido.
2. **No hay separación de dominios con políticas propias.** Un solo índice para
   todo produce interferencia entre campos.
3. **No hay olvido con auditoría.** O se guarda todo, o se borra sin rastro.
4. **No hay transmisión entre agentes con fidelidad medida.** Compartir un log no
   es enseñar.
5. **No hay gobernanza de la memoria compartida.** Procedencia, confianza y
   contradicciones quedan fuera.
6. **Los benchmarks son transversales, no longitudinales.** Nadie mide el
   "después de 1M de tokens".

## 9. Conclusión

Las piezas existen por separado: indexado hipocámpico (HippoRAG), olvido
(MemoryBank), grafo temporal (Zep), consolidación offline (sleep-time), reflexión
(Generative Agents), activación cognitiva (ACT-R). **Nadie las ha unido en un
ciclo de vida con capa social y métricas de progreso.** Ese es el espacio de
`open-human-memory`.

## 10. Preguntas abiertas

- ¿Se puede construir un benchmark longitudinal sin un proyecto real de meses?
- ¿La consolidación debe usar el LLM del cliente o uno propio? El costo decide
  la viabilidad.
- ¿Cómo se compara contra "RAG + resumen" sin trampa metodológica?
- ¿Qué parte del ciclo puede ser determinista (barata) y qué parte necesita LLM?
