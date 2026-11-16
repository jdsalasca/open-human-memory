# Cribado

**Fecha:** 16 de noviembre de 2026. **Un solo revisor.** Sin doble ciego.

## Flujo

```
Registros identificados (8 cadenas, título, 2023–2026)      7.100
        │
        ├─ muestreo por relevancia: top 25 por cadena
        ▼
Registros únicos cribados por título                          177
        │  excluidos por filtro grueso (no agentes)           −46
        ▼
Candidatos plausibles por título                              131
        │  NO EVALUADOS (muestreo por relevancia)             −88
        ▼
Evaluados por resumen                                          43
        │  excluidos con motivo                                −12
        ▼
Incluidos                                                      31
        │
        └─ al menos 12 llegaron por bola de nieve, fuera de los 177
```

**El hueco de 88 está declarado, no oculto.** No se evaluaron porque el cribado fue
un muestreo por relevancia, no una lectura de los 131. Un lector no puede
reconstruir por qué se eligieron esos 43 y no otros. Es la mayor debilidad de este
registro y se corrige en la próxima iteración con doble cribado y criterios
explícitos por fila.

**La procedencia exacta por trabajo no se registró.** Al menos 12 de los 31 llegaron
por bola de nieve (EvoAgentBench, SelfImprove-Bench, Skill Following, Frozen
Weights, SkillEvoReg, RSE-Bench, Proof-Gated, SoK, Bemula, MemEvoBench, STRATUM,
Trace2Skill). El resto, por las cadenas. La asignación individual queda pendiente.

## Exclusiones y motivos

**Por título (46):** memoria biológica, hardware, bases de datos, educación,
seguridad sin aprendizaje, y variantes de "agent" ajenas a LLM.

**Por resumen (12):**

| Trabajo | Motivo |
|---|---|
| AdaMem | Controla **qué escribir** en memoria; no mide adquisición de competencia |
| PEAM | Memoria paramétrica encarnada; sin transferencia entre tareas |
| XSkill | Multimodal; no comparable con nuestros dominios |
| ASPIRE | Descubrimiento de skills en robótica; sin evaluación longitudinal |
| SkillReducer | Optimización de tokens; no mide competencia |
| SkillZip | Compresión de grafos de skills; no mide competencia |
| GroupMemBench | Conversaciones multipartitas; fuera del alcance |
| MemForm | Envenenamiento de memoria; seguridad, no adquisición |
| MemoryDojo | Envenenamiento; duplica MemForm |
| ClawBio | Dominio concreto (bioinformática), sin evaluación de mecanismo |
| SCLATE | Infraestructura de entrenamiento; sin resultados de competencia |
| Winter Is Over for Continual Learning | Posición/revisión, sin experimento propio |

## Incluidos (31)

**Benchmarks de memoria y skills (9):** SkillsBench, MemDev-Bench,
VibeMemBench, ContinualSkillBench, SkillLearnBench, MemCalib, MemUse,
MemoryArena, AgentCL.

**Sistemas de memoria y auto-evolución (8):** Mem²Evolve, MemEvolve, MUSE-Autoskill,
Trace2Skill, SkillGen, CoEvoSkills, SkillOpt, Proof-Gated Skill Compilation.

**Evaluación de aprendizaje continuo (5):** EvoAgentBench, SelfImprove-Bench,
SWE-Bench-CL, Skill Following, Agent Self-Improvement with Frozen Weights.

**Fallos, deriva y límites (6):** More Skills Worse Agents, Contextual Agentic
Memory is a Memo, SkillEvoReg, RSE-Bench, Skill Drift, Bemula.

**Medición de coste y estructura (3):** STRATUM, Measure Before You Manage,
MemEvoBench.

## Fundacionales incluidos por citación (10)

DreamCoder, Stitch, LILO, CEGIS/SyGuS, Angluin, LPA*, options, MAML,
Information Bottleneck, metarrazonamiento (Russell y Wefald).

## Advertencia

Este cribado **no** es exhaustivo. Un revisor, una base, muestreo por relevancia y
bola de nieve. Sirve para saber qué existe y qué se ha demostrado; no para afirmar
que no existe algo fuera de la muestra.
