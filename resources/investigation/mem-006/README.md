# MEM-006 — Múltiples habilidades: la búsqueda barata gana

**Fecha:** 17 de noviembre de 2026
**Estado:** **ejecutado; resultado negativo para la memoria en este régimen.**
**Modelo:** `gpt-6-luna`, `reasoning_effort = low`, `codex-cli 0.169.0`.
**Código:** `src/ohmem/mem_006.py`. **Protocolo:** `protocolo.md` (hash
`e2252308…`). **Análisis:** `analyze.py`.
**Datos:** `results/retrieval-seed1.json`.

## 1. Qué se midió

8 habilidades de 2 operaciones, cada una aprendida en una sesión separada y verificada
con 60 sondas. Después, 2 tareas por habilidad con 2 ejemplos de soporte. El evaluador
**no dice qué habilidad usar**: el agente debe recuperarla de una biblioteca de 5–8
candidatas. Competidores: clon sin biblioteca, oráculo (habilidad correcta),
habilidad aleatoria, biblioteca escrita por un experto y **solucionador simbólico** que
enumera los 36 programas de 2 operaciones.

## 2. Adquisición

| Habilidad | Programa | ¿Verificó? |
|---|---|---|
| s1 | `sort_asc → double` | Sí (`double → sort_asc`) |
| s2 | `reverse → add_one` | **No** (`negate → reverse`) |
| s3 | `sort_desc → negate` | Sí (`negate → sort_asc`) |
| s4 | `double → add_one` | Sí |
| s5 | `reverse → double` | **No** (3 operaciones) |
| s6 | `sort_asc → negate` | Sí (`negate → sort_desc`) |
| s7 | `sort_desc → add_one` | Sí |
| s8 | `sort_desc → double` | **No** (`double → reverse`) |

**Solo 5 de 8 habilidades verificaron.** La biblioteca quedó en 5; las tareas, en 10,
no en 16. No se relajó la verificación.

## 3. Resultados

| Condición | Acierto | Selección correcta |
|---|---|---|
| Clon | 8/10 | — |
| Oráculo (habilidad correcta) | 8/10 | 10/10 |
| **Recuperación autónoma** | **7/10** | **5/10** |
| Habilidad aleatoria | 1/10 | 0/10 |
| Biblioteca de experto | 5/10 | 5/10 |
| **Solucionador simbólico** | **10/10** | — |

Pares:

| Comparación | Acierta A / falla B | Acierta B / falla A | p |
|---|---|---|---|
| Recuperación vs clon | 1 | 2 | 1,0 |
| Recuperación vs aleatoria | **6** | 0 | **0,031** |
| Recuperación vs experto | 2 | 0 | 0,5 |
| Recuperación vs oráculo | 1 | 2 | 1,0 |
| Recuperación vs simbólico | 0 | **3** | 0,25 |

**Identificabilidad:** 10/10 tareas tienen respuesta determinada por los dos ejemplos;
1–2 programas consistentes por tarea. El solucionador simbólico acierta **10/10**.

**Coste:** tokens de entrada (mediana): clon 25.775; recuperación 25.866; oráculo
26.676; experto 25.900. Adquisición de 8 habilidades: **209.871 tokens** (mediana
26.011 por llamada). El simbólico no usa LLM.

## 4. Hallazgos

1. **El solucionador simbólico resuelve todo (10/10).** Las tareas no requieren
   memoria: 1–2 programas de 2 operaciones explican los ejemplos y determinan la
   consulta. La memoria no aporta información.
2. **La recuperación no supera al clon.** 7/10 vs 8/10; un par a favor y dos en
   contra. La selección de habilidad es 5/10 (azar 20 %): mejor que el azar, pero
   insuficiente para un sistema de memoria.
3. **La biblioteca de experto empata con la aprendida.** 5/10 vs 5/10 en acierto y
   selección: no hay evidencia de que la adquisición aporte una ventaja en esta tarea.
4. **La memoria es más cara y no ahorra uso.** La recuperación usa 25.866 tokens
   frente a 25.775 del clon y añade 209.871 de adquisición. El beneficio neto es
   negativo en este régimen.
5. **El cuello es la tarea, no el recuperador.** En 2 operaciones identificables, la
   búsqueda barata gana. La memoria tendría que aportar en tareas donde la búsqueda no
   quepa en el presupuesto o donde la aplicabilidad/obsolescencia sea el problema.

## 5. Claims

| ID | Afirmación | Estado |
|---|---|---|
| R1 | La recuperación elige la habilidad correcta en ≥ 70 % | **Refutada**: 5/10 = 50 % |
| R2 | La recuperación supera al clon y a la aleatoria en ≥ 3 pares | **Refutada**: 1/2 frente al clon; 6/0 frente a la aleatoria |
| R3 | La recuperación no supera al oráculo | Sostenida: 7 vs 8 |
| R4 | El solucionador simbólico acierta ≥ 90 % | Sostenida: 10/10 |
| R5 | Recuperación y experto no difieren en más de 2 pares | Sostenida: 7 vs 5; selección 5 vs 5 |
| R6 | Rechaza ≥ 3 de 4 habilidades obsoletas | Abierta: no ejecutado |

## 6. Qué significa

**En el régimen de 2 operaciones identificables, la memoria no tiene ventaja de
acierto y no se amortiza.** El solucionador simbólico resuelve todo sin aprendizaje;
el clon acierta 8/10; la recuperación 7/10 con selección 5/10. La biblioteca de experto
empata con la aprendida.

El siguiente paso no es otro formato de memoria ni otra habilidad de 2 operaciones:

- **F3 / MEM-007:** tareas donde la búsqueda de 2 operaciones no quepa en el
  presupuesto (3–4 operaciones con presupuesto fijado) y el modelo pueda aplicar.
  EXEC-001 dice que 3 operaciones ya es frágil (44 %); hay que medir el punto exacto.
- **Aplicabilidad y obsolescencia:** tareas donde la habilidad fue correcta y deja de
  serlo; el valor está en rechazar, no en ejecutar.
- **Coste total:** el beneficio neto con `N` usos; en este régimen es negativo.

## 7. Límites

- 5 habilidades verificadas (no 8), 10 tareas (no 16), una semilla, un modelo.
- La recuperación se mide con una biblioteca pequeña (5); el azar es 20 %, no 12,5 %.
- Las tareas son de 2 operaciones y el solucionador simbólico las resuelve; no
  representan el régimen donde la memoria podría importar.
- La obsolescencia (R6) no se ejecutó.
- El coste es en tokens, no en dinero; la adquisición se ejecutó antes de todas las
  condiciones.
- El protocolo se pre-registró con hash; los resultados se publican en un commit
  separado. Las desviaciones (5 habilidades, 10 tareas, sin obsolescencia) se declaran.

## 8. Reproducir

```powershell
$env:PYTHONPATH="src"
python -m ohmem.mem_006 --tasks-per-skill 2 --support 2 --seed 1 `
  --session1-examples 12 --model gpt-6-luna --effort low --timeout 120 `
  --out resources/investigation/mem-006/results/retrieval-seed1.json
python resources/investigation/mem-006/analyze.py
```
