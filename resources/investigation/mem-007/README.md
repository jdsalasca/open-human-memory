# MEM-007 — Aplicabilidad: la metadata evita el falso positivo

**Fecha:** 17 de noviembre de 2026
**Estado:** **ejecutado; primer resultado positivo de aplicabilidad.**
**Modelo:** `gpt-6-luna`, `reasoning_effort = low`, `codex-cli 0.169.0`.
**Código:** `src/ohmem/mem_007.py`. **Protocolo:** `protocolo.md` (hash
`511848b1…`). **Análisis:** `analyze.py`.
**Datos:** `results/pilot-seed1-corrected.json` (clon corregido),
`results/pilot-seed1.json` (corrida original), `results/clone-fixed.json`.

## 1. Qué se midió

4 habilidades de 2 operaciones, cada una con una **precondición comprobable en la
consulta**:

| ID | Procedimiento | Precondición |
|---|---|---|
| p1 | `sort_asc → double` | sin duplicados |
| p2 | `reverse → add_one` | primer elemento > 5 |
| p3 | `sort_desc → negate` | suma < 20 |
| p4 | `double → add_one` | contiene el 5 |

16 tareas: 2 aplicables y 2 inaplicables por habilidad. La habilidad se entrega
identificada; se aísla **aplicabilidad**, no recuperación.

| Condición | Qué recibe |
|---|---|
| `clone` | Solo los ejemplos |
| `skill_no_meta` | La habilidad correcta, sin precondición |
| `skill_meta` | La habilidad correcta + precondición + instrucción de rechazar |
| `symbolic_solver` | Ajuste de un programa de 2 operaciones; sin precondición |

## 2. Resultados

| Condición | Total | Aplicables | Inaplicables | Falsos positivos |
|---|---|---|---|---|
| Clon | 5/16 | 4/8 | 1/8 | 7/8 |
| Habilidad sin metadata | 5/16 | 5/8 | 0/8 | 8/8 |
| **Habilidad con precondición** | **13/16** | **6/8** | **7/8** | **1/8** |
| Solucionador simbólico | 8/16 | 8/8 | 0/8 | 8/8 |

Pares (inaplicables):

| Comparación | Acierta A / falla B | Acierta B / falla A | p |
|---|---|---|---|
| `skill_meta` vs `skill_no_meta` | **7** | 0 | **0,016** |
| `skill_meta` vs clon | **6** | 0 | **0,031** |
| `skill_meta` vs simbólico | **7** | 0 | **0,016** |
| `skill_no_meta` vs clon | 0 | 1 | 1,0 |

En aplicables, `skill_meta` 6/8 vs `skill_no_meta` 5/8: un par a favor, ninguno en
contra. La precondición no cuesta precisión aplicable en esta muestra.

Tokens de entrada (mediana): clon 26.651; sin metadata 25.790; con metadata 25.794.
La metadata no añade coste apreciable.

## 3. Hallazgos

1. **La precondición evita el falso positivo.** `skill_meta` rechaza **7/8**
   inaplicables; `skill_no_meta` y el simbólico aplican **8/8**; el clon, 7/8.
2. **No cuesta aplicables.** 6/8 vs 5/8; el único par discordante favorece a la
   metadata. La muestra es pequeña, pero no hay señal de que rechazar empeore la
   ejecución.
3. **El solucionador simbólico no puede saber cuándo no usar.** Acierta 8/8
   aplicables y 0/8 inaplicables: ajusta el programa y lo aplica. La metadata es
   información que el símbolo no tiene.
4. **El valor de la memoria es condicional, no ejecucional.** En MEM-006 la memoria
   no superó al símbolo; aquí la metadata sí aporta porque el problema es **saber
   cuándo no aplicar**, no ejecutar.
5. **Cautela:** la precondición es una frase del prompt y es verdadera. No se probó
   una precondición **falsa** ni **obsoleta**. Si el modelo confía en la metadata sin
   comprobarla, un precondición falsa produciría rechazos incorrectos. Es el
   equivalente del placebo verificado de MEM-004 y el siguiente control obligatorio.

## 4. Claims

| ID | Afirmación | Estado |
|---|---|---|
| A1 | `skill_meta` rechaza ≥3/8 inaplicables | **Sostenida**: 7/8 |
| A2 | `skill_meta` supera a `skill_no_meta` en inaplicables en ≥3 pares | **Sostenida**: 7/0 (p = 0,016) |
| A3 | `skill_meta` y `skill_no_meta` no difieren en más de 2 pares en aplicables | **Sostenida**: 6 vs 5 |
| A4 | `skill_meta` supera a clon y simbólico en inaplicables en ≥3 pares | **Sostenida**: 6/0 y 7/0 |
| A5 | El simbólico aplica en ≥3/8 inaplicables | **Sostenida**: 8/8 |

## 5. Qué sigue

- **MEM-008: precondición falsa y obsoleta.** La misma habilidad con una precondición
  incorrecta o que dejó de cumplirse. Si el modelo rechaza cuando no debe, la metadata
  es peligrosa; si la comprueba, hay aplicación condicionada real.
- **Aplicabilidad multi-habilidad:** elegir entre 4 habilidades con precondiciones
  distintas, no solo aplicar/rechazar una dada.
- **Réplica:** 24 tareas, varias semillas, segundo modelo.
- **Coste total:** adquisición + verificación + uso; aquí la metadata no añade coste.

## 6. Límites

- 4 habilidades, 16 tareas, una semilla, un modelo.
- La precondición es verdadera y explícita; no hay metadata falsa ni obsolescencia.
- La habilidad se entrega identificada; no hay recuperación entre habilidades.
- El clon se re-ejecutó con el prompt corregido: el original no definía `APPLY` y
  devolvía `OK`; esa corrida no es válida y se conserva como registro.
- El solucionador simbólico no recibe la precondición; es el competidor sin metadata.
- Los tokens son de entrada; no se mide dinero.

## 7. Reproducir

```powershell
$env:PYTHONPATH="src"
python -m ohmem.mem_007 --support 2 --seed 1 `
  --model gpt-6-luna --effort low --timeout 120 `
  --out resources/investigation/mem-007/results/pilot-seed1.json
# El clon corregido (prompt con APPLY/NONE):
python -m ohmem.mem_007 --support 2 --seed 1 --conditions clone `
  --model gpt-6-luna --effort low --timeout 120 `
  --out resources/investigation/mem-007/results/clone-fixed.json
python resources/investigation/mem-007/analyze.py
```
