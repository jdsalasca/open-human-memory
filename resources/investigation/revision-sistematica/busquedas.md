# Registro de búsquedas

**Base:** OpenAlex API (`api.openalex.org`), consultada el **16 de noviembre de 2026**.
**Cobertura:** una sola base. No se consultaron Scopus, Web of Science ni ACM DL
(sin acceso). Es una limitación declarada, no un detalle.

## Cadenas por título (filtro `from_publication_date:2023-01-01`)

| ID | Cadena | Registros |
|---|---|---|
| S1 | `agent memory` | 2.689 |
| S2 | `agent skills` | 1.208 |
| S3 | `library learning` | 1.778 |
| S4 | `tool creation` | 662 |
| S5 | `memory coding agent` | 78 |
| S6 | `continual learning agent` | 100 |
| S7 | `metareasoning` | 44 |
| S8 | `skill library` | 541 |
| | **Total (con solapamiento)** | **7.100** |

## Cadenas por título y resumen (conteo de sensibilidad)

| Cadena | Registros |
|---|---|
| `agent memory` | 24.866 |
| `agent skills library` | 738 |
| `library learning program synthesis` | 297 |
| `tool creation LLM agent` | 354 |
| `memory coding agent repository` | 373 |
| `continual learning LLM agent` | 349 |
| `metareasoning` | 87 |
| `program synthesis abstraction` | 659 |

## Muestreo

El cribado no recorrió los 7.100 registros. Se aplicó un muestreo por relevancia:
**los 25 primeros resultados de cada cadena** (8 × 25 = 200; 177 únicos tras
deduplicar). Es una revisión **estructurada con muestreo por relevancia**, no una
revisión sistemática exhaustiva.

## Bola de nieve

| Semilla | Referencias | Citas directas revisadas |
|---|---|---|
| MemDev-Bench | 23 | 0 |
| VibeMemBench | 23 | 3 |
| SkillLearnBench | 22 | 8 |
| ContinualSkillBench | 30 | 8 |
| MemCalib | 21 | 4 |
| MemUse | 20 | 0 |

La bola de nieve aportó los trabajos que el muestreo por título no trajo:
EvoAgentBench, SelfImprove-Bench, Skill Following, SkillEvoReg, RSE-Bench,
Proof-Gated Skill Compilation, SoK Agentic Skills, Bemula, MemEvoBench, STRATUM,
Trace2Skill, MemoryArena, SkillGen, AgentCL, SWE-Bench-CL, MemEvolve,
More Skills Worse Agents, Skill Drift, Measure Before You Manage.

## Reproducir

```python
# Ejemplo: conteo de una cadena
GET https://api.openalex.org/works
  ?filter=title.search:agent%20memory,from_publication_date:2023-01-01
  &per-page=1&select=title
```

Los resultados crudos de esta sesión están en el historial del agente; las cifras
de arriba son las devueltas por `meta.count`.
