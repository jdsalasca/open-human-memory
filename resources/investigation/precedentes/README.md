# Precedentes: qué se ha intentado en memoria agéntica

Este directorio cataloga el trabajo previo que importa para `open-human-memory`.
No es una bibliografía exhaustiva: es un mapa de **qué se intentó, qué funcionó,
qué quedó sin resolver y qué se puede reutilizar**.

## Criterio de inclusión

Un sistema entra si cumple al menos una condición:

- propone una arquitectura de memoria para agentes,
- aprende habilidades o procedimientos de la experiencia,
- mejora el aprendizaje continuo sin reentrenar,
- coordina memoria entre agentes,
- o define un benchmark que mide alguna de esas cosas.

## Matriz comparativa

| Sistema / línea | Unidad de memoria | Ciclo de vida | Multi-modelo | Capa social | Evaluación | Hueco principal |
|---|---|---|---|---|---|---|
| MemGPT / Letta | Bloques de contexto + archivo | Paginación, auto-edición | Parcial | No | DMR | Sin consolidación ni olvido |
| Generative Agents | Episodio en lenguaje natural | Stream + reflexión | No | Emergente | Simulación | Memoria plana, sin procedimientos |
| Mem0 | Hecho extraído | Extracción + consolidación | Parcial | Multi-usuario | LoCoMo | Sin habilidades |
| Zep / Graphiti | Hecho/relación temporal | Grafo bi-temporal | Parcial | Multi-usuario | DMR, LongMemEval | Sin procedimientos |
| HippoRAG | Nodo de grafo | Indexado + PPR | Parcial | No | Multi-hop QA | Solo retrieval |
| MemoryBank | Episodio | Decaimiento Ebbinghaus | No | No | Diálogo | Olvido uniforme |
| A-MEM | Nota Zettelkasten | Enlaces automáticos | No | No | LoCoMo | Sin metabolismo |
| Voyager | Habilidad en código | Biblioteca + currículo | No | No | Minecraft | Un entorno, un modelo |
| AWM | Workflow | Inducción + reutilización | No | No | Web/ALFWorld | Sin contrato ejecutable |
| ExpeL | Insight en lenguaje natural | Extracción | No | No | ALFWorld/HotpotQA | Sin verificación |
| Reflexion | Reflexión verbal | Episódica | No | No | Varias | No acumula |
| ACE | Playbook textual | Evolución | Parcial | No | Tareas | Sin IR agnóstica |
| Memento | Caso | Case-based reasoning | Parcial | No | DeepResearcher | Casos, no procedimientos |
| SkillWeaver | Skill web | APIs | Parcial | Transferencia | Web | Dominio específico |
| DGM | Código del agente | Evolución | No | Archivo | Benchmarks | Auto-modificación de código |
| Zep Agent Skills | Traza + skill versionada | Compilación + admisión + uso | Sí | Namespace | τ³, AppWorld, EnterpriseOps-Gym | Sin validación causal |
| MSCE | Traza + política + skill | Cristalización + gobernanza | Parcial | No | EvoAgentBench, LoCoMo | Ganancia heurística, no causal |
| AFTER | Benchmark | Transferencia | Sí (backbones) | Roles | 382 tareas | No arquitectura |
| Trace2Skill | Trayectoria + skill | Destilación | Sí (escalas/familias) | No | Benchmarks | Sin causalidad |
| CUMULUS (propuesta) | Skill SIR | Compilación + canon + olvido | Sí | Pod | Pendiente | Sin validación causal |

## Documentos

1. [01-memoria-de-agentes.md](01-memoria-de-agentes.md) — sistemas de memoria
   (hechos, episodios, grafos).
2. [02-habilidades-y-aprendizaje.md](02-habilidades-y-aprendizaje.md) —
   bibliotecas de habilidades y aprendizaje de experiencia.
3. [03-contexto-y-aprendizaje-continuo.md](03-contexto-y-aprendizaje-continuo.md)
   — límites del contexto y aprendizaje sin reentrenar.
4. [04-multiagente-y-sociedad.md](04-multiagente-y-sociedad.md) — memoria
   compartida, roles y coordinación.
5. [05-huecos-y-oportunidades.md](05-huecos-y-oportunidades.md) — síntesis y
   dirección novedosa.
6. [06-competidores-directos-2026.md](06-competidores-directos-2026.md) —
   Zep Agent Skills, MSCE, AFTER, Trace2Skill y el estado real de la novedad.
7. [07-antecedentes-2026-ii.md](07-antecedentes-2026-ii.md) — COUNTERMEM,
   ConMem, MemCon, anti-persistencia, utilidad y conflicto irreducible.

## Lo que se repite

- **La memoria se trata como almacén**, no como ciclo de vida.
- **El retrieval es el centro**; la consolidación y el olvido son secundarios.
- **Los procedimientos se guardan como texto o código**, no como artefactos
  portables.
- **La transferencia entre modelos casi no se mide**.
- **La capa social es un namespace**, no una institución.
- **Los benchmarks miden recall puntual**, no progreso longitudinal.
