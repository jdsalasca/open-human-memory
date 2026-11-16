# 25 - Protocolo de recolección y evaluación de fuentes primarias

> **Actualizado 2026-11-16.** El protocolo se ejecutó parcialmente: 8 cadenas,
> 7.100 registros identificados, 177 cribados, 31 incluidos; una base (OpenAlex) y
> un revisor. La revisión declara sus límites en `revision-sistematica/`. **No es
> exhaustiva.**

## 1. Propósito

Evitar dos errores que la revisión detectó:

1. **Declarar novedad sin haber buscado lo suficiente.** "No existe" es una
   afirmación empírica que exige método.
2. **Mezclar evidencia del fenómeno con evidencia de la traducción.** Un paper
   puede demostrar que el sueño consolida y no demostrar nada sobre un algoritmo
   de consolidación.

Este protocolo convierte la revisión bibliográfica en un proceso **reproducible,
fechado y actualizable**.

## 2. Preguntas de la revisión

- **RQ1:** ¿qué sistemas de memoria procedural para agentes existen y qué
  mecanismos implementan?
- **RQ2:** ¿qué evidencia hay de transferencia de procedimientos entre modelos?
- **RQ3:** ¿qué evidencia hay de memoria contrafactual y atribución causal en
  agentes?
- **RQ4:** ¿qué evidencia hay de que la memoria persistente mejore o empeore el
  rendimiento?
- **RQ5:** ¿qué métodos existen para representar incertidumbre, ignorancia y
  conflicto en memoria?
- **RQ6:** ¿qué benchmarks miden acumulación longitudinal y deriva?

## 3. Fuentes

### 3.1 Bases académicas

- arXiv (cs.AI, cs.CL, cs.LG, cs.SE).
- Semantic Scholar.
- ACL Anthology.
- OpenReview (ICLR, NeurIPS, ICML, TMLR).
- NeurIPS, ICML, ICLR, AAAI, IJCAI proceedings.
- PubMed y PsycINFO para neurociencia y psicología.
- Google Scholar para citas y trabajos no indexados.
- DBLP para verificación de venues.

### 3.2 Fuentes grises

- Blogs técnicos de laboratorios (Zep, Letta, Mem0, Anthropic, OpenAI,
  DeepMind).
- Repositorios GitHub con código o benchmarks.
- Documentación de productos cuando describe mecanismos no publicados.

**Regla:** una fuente gris no cuenta como evidencia de efectividad; cuenta como
evidencia de que el sistema existe y de cómo se describe.

## 4. Cadenas de búsqueda

Se registran literalmente, con fecha y número de resultados.

### 4.1 Memoria de agentes

```
("agent memory" OR "LLM memory" OR "long-term memory")
AND (LLM OR "language model" OR agent)
```

### 4.2 Memoria procedural y skills

```
("procedural memory" OR "skill library" OR "skill compilation"
 OR "workflow memory" OR "playbook")
AND (agent OR LLM)
```

### 4.3 Contrafactuales y causalidad

```
("counterfactual memory" OR "counterfactual" OR "causal attribution"
 OR "credit assignment" OR "intervention")
AND (agent OR LLM)
```

### 4.4 Memoria y error

```
("error propagation" OR "error reproduction" OR "anti-persistence"
 OR "memory poisoning" OR "false memory")
AND (agent OR LLM)
```

### 4.5 Utilidad y control

```
("memory utility" OR "memory control" OR "retrieval policy"
 OR "when to retrieve" OR "memory management")
AND (agent OR LLM)
```

### 4.6 Incertidumbre y conflicto

```
("uncertainty" OR "ignorance" OR "conflict" OR "underdetermination"
 OR "abstention")
AND (memory OR agent)
AND (LLM OR language model)
```

### 4.7 Neurociencia y sueño

```
("complementary learning systems" OR "sleep replay" OR "systems consolidation"
 OR "adaptive forgetting" OR "engram")
```

### 4.8 Sociología y organización

```
("transactive memory" OR "organizational memory" OR "communities of practice"
 OR "collective memory" OR "epistemic trust")
```

## 5. Criterios de inclusión

Un trabajo entra si cumple **al menos uno**:

- propone o evalúa un mecanismo de memoria para agentes;
- estudia transferencia, retención o interferencia de procedimientos;
- estudia atribución causal o contrafactual en agentes;
- estudia error, olvido, incertidumbre o conflicto en memoria;
- define un benchmark relevante;
- aporta evidencia primaria de un fenómeno usado como inspiración (neurociencia,
  etología, psicología, sociología).

## 6. Criterios de exclusión

- Opinión sin datos ni mecanismo.
- Marketing sin descripción técnica.
- Trabajos sobre memoria humana sin conexión plausible con agentes, salvo que se
  usen como inspiración L1 y se marquen como tal.
- Duplicados o versiones preliminares de un trabajo ya incluido (se conserva la
  versión más reciente y se registra la anterior).
- Benchmarks sin datos ni código disponibles, si la afirmación central depende de
  ellos.

## 7. Cribado

1. **Título y abstract:** dos pasadas; se registra el motivo de exclusión.
2. **Texto completo:** se evalúa mecanismo, evidencia, límites y reproducibilidad.
3. **Bola de nieve:** se revisan referencias y citas de los incluidos.
4. **Consulta a expertos:** opcional; se registra.

### Diagrama de flujo

```
Identificados (n = ...)
   ↓ duplicados eliminados (n = ...)
Cribados por título/abstract (n = ...)
   ↓ excluidos (n = ..., motivos)
Texto completo evaluado (n = ...)
   ↓ excluidos (n = ..., motivos)
Incluidos (n = ...)
   ↓ bola de nieve (n = ...)
Total (n = ...)
```

## 8. Extracción de datos

Por trabajo:

```yaml
id: ...
title: ...
authors: ...
year: ...
venue: ...
url: ...
type: system | benchmark | empirical | review | theory | grey
problem: ...
mechanism: ...
memory_unit: ...
lifecycle: {encode, consolidate, forget, retrieve, teach}
verification: ...
cross_model: ...
social_layer: ...
evidence:
  design: ...
  sample: ...
  baselines: ...
  metrics: ...
  effect: ...
  limitations: ...
source_evidence: A | B | C | D
transfer_evidence: 0 | 1 | 2 | 3
claims_supported: [...]
claims_not_supported: [...]
relevance: ...
```

## 9. Evaluación de evidencia en dos ejes

### 9.1 Evidencia de origen

¿Qué tan sólido es el fenómeno en su disciplina?

- **A:** consenso, meta-análisis, replicación.
- **B:** evidencia sólida con límites.
- **C:** teoría o hipótesis.
- **D:** metáfora o evidencia débil.

### 9.2 Evidencia de transferencia

¿Qué demuestra que el mecanismo computacional inspirado en ese fenómeno mejora
el sistema artificial?

- **3:** experimento comparativo con líneas base fuertes y réplica.
- **2:** experimento comparativo sin réplica o con líneas base débiles.
- **1:** prototipo o estudio de caso.
- **0:** solo analogía, sin implementación.

**Regla:** una fuente puede ser A/0 (fenómeno sólido, transferencia no probada).
No se permite presentar A/0 como si fuera A/3.

## 10. Afirmaciones de ausencia

Para escribir "no existe" o "no se ha estudiado", se debe registrar:

- bases consultadas;
- cadenas exactas;
- fecha de consulta;
- número de resultados;
- criterios de cribado;
- motivos de exclusión de los candidatos cercanos.

Sin ese registro, la afirmación se escribe como **"no lo hemos encontrado"**, no
como "no existe".

## 11. Evaluación de riesgo de sesgo

- **Sesgo de selección:** ¿los benchmarks fueron elegidos después de ver
  resultados?
- **Sesgo de evaluación:** ¿el juez es el mismo modelo que genera?
- **Sesgo de cómputo:** ¿la condición ganadora gastó más tokens?
- **Sesgo de supervivencia:** ¿solo se reportan éxitos?
- **Sesgo de novedad:** ¿se compara contra líneas base débiles?
- **Confusión:** ¿hay variables no controladas?
- **Reproducibilidad:** ¿hay código, datos, semillas y presupuesto?

## 12. Actualización

- **Frecuencia:** mensual.
- **Ventana:** últimos 30 días + citas nuevas de trabajos clave.
- **Registro:** `recursos` de búsqueda, fecha, resultados, cambios.
- **Versión:** cada actualización produce una entrada en el changelog.
- **Cierre:** una revisión se congela para un paper; se indica la fecha de corte.

## 13. Registro actual (noviembre 2026)

| Fecha | Consulta | Resultados relevantes |
|---|---|---|
| 2026-11-14 | Zep Agent Skills / procedural memory | Chalef et al. (2026) |
| 2026-11-14 | Procedural memory benchmark | Belikova et al. (2026), AFTER |
| 2026-11-14 | Agent skills failure | Jiang et al. (2026) |
| 2026-11-14 | Memory-to-skills governance | Tang et al. (2026), MSCE |
| 2026-11-15 | Counterfactual memory | Pu et al. (2026), COUNTERMEM |
| 2026-11-15 | Counterfactual memory admission | Zhang et al. (2026), ConMem |
| 2026-11-15 | Memory control | Jiang et al. (2026), MemCon |
| 2026-11-15 | Error reproduction | Wang et al. (2026) |
| 2026-11-15 | Executed counterfactual | Pakhomov y Nijkamp (2026) |
| 2026-11-15 | Task-conditioned utility | Yang et al. (2026) |
| 2026-11-15 | Memory conflict | Yang et al. (2026), TANGLE |

Este registro se amplía en cada ronda. No es una prueba de exhaustividad; es la
base para no repetir afirmaciones de ausencia sin sustento.

## 14. Limitaciones

- Las búsquedas dependen de las bases y del idioma (inglés).
- Los preprints cambian; se registra la versión consultada.
- La bola de nieve puede sesgar hacia trabajos ya citados.
- La evaluación de evidencia es cualitativa; se busca convergencia entre
  evaluadores cuando sea posible.
- La revisión no reemplaza la replicación experimental.

## 15. Producto

Un **anexo de revisión** por paper, con:

- matriz de antecedentes por mecanismo;
- evidencia de origen y de transferencia;
- afirmaciones de ausencia justificadas;
- fecha de corte;
- changelog.

Ese anexo es el que permite decir, con honestidad, qué es nuevo y qué no.
