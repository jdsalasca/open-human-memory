# 01 — Sistemas de memoria de agentes (hechos, episodios, grafos)

## MemGPT / Letta (Packer et al., 2023)

**Qué hace.** Trata el contexto como memoria principal y el almacenamiento
externo como disco. El agente pagina información, edita sus bloques de memoria y
decide qué traer. Introduce la metáfora del sistema operativo para la memoria.

**Qué resuelve.** El contexto deja de ser un vertedero: se administra.

**Qué no resuelve.** No hay consolidación (episodio → esquema), ni olvido
selectivo, ni procedimientos, ni transferencia entre modelos. La "edición" es
texto que el agente reescribe, con el riesgo de reescribir mal.

**Lección.** El agente puede ser su propio gestor de memoria, pero necesita
límites y verificación.

## Generative Agents (Park et al., 2023)

**Qué hace.** Registra observaciones en un *memory stream*; recupera por una
combinación de recencia, importancia (puntuada por el LLM) y relevancia. Cuando
la importancia acumulada cruza un umbral, reflexiona y genera inferencias de
orden superior.

**Qué resuelve.** Demuestra que la importancia y la recencia importan, no solo la
similitud. La reflexión produce abstracciones útiles.

**Qué no resuelve.** La memoria es plana y en lenguaje natural; no hay
deduplicación, ni olvido, ni dominios, ni procedimientos ejecutables. La
reflexión puede confabular y no se verifica.

**Lección.** El puntaje de recuperación debe combinar señales; la reflexión es
una forma primitiva de consolidación.

## Mem0 (Chhikara et al., 2025)

**Qué hace.** Extrae hechos de la conversación, los consolida, actualiza y
elimina duplicados; variante con grafo (Mem0g). Optimiza el costo de contexto y
la consistencia multi-sesión. Reporta mejoras en LoCoMo y reducción de tokens y
latencia.

**Qué resuelve.** El pipeline de extracción + consolidación + actualización es
justo lo que un RAG ingenuo no tiene.

**Qué no resuelve.** Está orientado a memoria de usuario/conversación, no a
aprendizaje de tareas. No hay procedimientos, ni validación causal, ni
portabilidad entre modelos.

**Lección.** La consolidación de hechos es un problema de ingeniería resuelto a
medias; la consolidación de procedimientos es otro problema.

## Zep / Graphiti (Rasmussen et al., 2025)

**Qué hace.** Grafo de conocimiento temporal con entidades, relaciones y validez
bi-temporal; los episodios son la fuente. Reporta 94,8% en DMR frente a 93,4% de
MemGPT y mejoras de hasta 18,5% en LongMemEval con menor latencia.

**Qué resuelve.** El tiempo es de primera clase: una relación puede ser cierta en
un intervalo y dejar de serlo. Es imprescindible para "por qué cambiamos de
decisión".

**Qué no resuelve.** Sigue siendo recuperación sobre un grafo; no hay
consolidación de habilidades, ni olvido, ni gobernanza.

**Lección.** La validez temporal es un requisito, no un lujo. Sin ella, el agente
repite decisiones revocadas.

## HippoRAG (Gutiérrez et al., 2024, 2025)

**Qué hace.** Inspirado en el indexado hipocámpico: un grafo de conocimiento hace
de índice y la recuperación usa propagación tipo PageRank para asociar entidades
y responder preguntas multi-hop. La versión 2 extiende a aprendizaje continuo no
paramétrico.

**Qué resuelve.** Demuestra que la inspiración neurológica puede producir mejoras
medibles en recuperación asociativa.

**Qué no resuelve.** Es recuperación, no ciclo de vida. No modela consolidación,
olvido ni sociedad.

**Lección.** El grafo es un índice, no un cerebro. La asociación mejora el
recall, pero no crea competencia.

## MemoryBank (Zhong et al., 2024)

**Qué hace.** Aplica la curva de Ebbinghaus: los recuerdos decaen y se refuerzan
con el uso. Es uno de los pocos sistemas con olvido explícito.

**Qué resuelve.** El olvido como función, no como bug.

**Qué no resuelve.** El decaimiento es uniforme; no hay saliencia multidominio,
ni archivo, ni auditoría, ni procedimientos.

**Lección.** El olvido es implementable y barato; la pregunta es qué proteger.

## A-MEM (Xu et al., 2025)

**Qué hace.** Memoria tipo Zettelkasten: cada nota tiene contexto, etiquetas y
enlaces; el sistema genera enlaces nuevos al insertar.

**Qué resuelve.** La asociación explícita entre recuerdos, no solo similitud.

**Qué no resuelve.** Sin consolidación ni olvido; el grafo crece sin metabolismo.

**Lección.** La estructura de enlaces es parte del recuerdo, no un adorno.

## GraphRAG (Edge et al., 2024)

**Qué hace.** Construye comunidades jerárquicas en el grafo y genera resúmenes por
comunidad para preguntas globales.

**Qué resuelve.** La estructura jerárquica permite resumir sin perder ejes.

**Qué no resuelve.** Es indexación de corpus, no memoria de agente.

**Lección.** La jerarquía es una forma de compresión útil; el resumen por
comunidad se parece a un esquema.

## Lo que estos sistemas comparten

1. **Unidad de memoria:** hecho, episodio o nota. Ninguno tiene una unidad
   procedural ejecutable.
2. **Ciclo de vida:** casi todos tienen escritura y recuperación; pocos tienen
   consolidación real y olvido.
3. **Evaluación:** recall en conversaciones o QA. Ninguno mide mejora de tareas a
   lo largo de meses.
4. **Modelo:** casi todos asumen un modelo fijo. La portabilidad no se mide.
5. **Sociedad:** la memoria compartida es un namespace, no una institución.

## Qué reutilizar

- La **paginación** de MemGPT para el presupuesto de contexto.
- La **importancia + recencia + relevancia** de Generative Agents.
- La **extracción y deduplicación** de Mem0.
- La **validez temporal** de Zep.
- El **indexado asociativo** de HippoRAG.
- El **decaimiento** de MemoryBank.
- Los **enlaces** de A-MEM.
- La **jerarquía** de GraphRAG.

## Qué no copiar

- La memoria plana sin metabolismo.
- El resumen como sustituto de consolidación.
- El olvido uniforme.
- La evaluación de recall como prueba de competencia.
