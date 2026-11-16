# MEM-002 — Memoria en el régimen aplicable

**Fecha:** 16 de noviembre de 2026
**Estado:** **ejecutado, dos pilotos.** El de 3 operaciones estaba pre-registrado; el
de 2 operaciones es exploratorio y motiva MEM-003.
**Modelo:** `gpt-6-luna`, `reasoning_effort = low`, `codex-cli 0.169.0`.
**Código:** `src/ohmem/v7_transfer.py`. **Protocolo:** `protocolo.md`.
**Datos:** `results/pilot-depth3.json`, `results/pilot-depth2.json`.
**Análisis:** `analyze.py`.

## 1. Pregunta

EXEC-001 mostró que `luna` aplica 2 operaciones al 86 %, 3 al 44–58 % y 5 al 0–33 %.
El 007 usó 5 pasos y midió el suelo. MEM-002 baja a 3 y a 2 operaciones para buscar
un régimen donde la memoria tenga margen.

## 2. Piloto de 3 operaciones (pre-registrado)

Motivo verificado de 2 operaciones + 1 operación aleatoria; 2 ejemplos de soporte.

| Condición | Acierto |
|---|---|
| Clon | 2/12 |
| Memoria (2 ops) | 3/12 |
| Placebo | 5/12 |
| Historial | 4/12 |
| **Oráculo (3 ops)** | **8/12** |

Pares: memoria vs clon 1/0; memoria vs placebo 2/4; memoria vs historial 1/2;
**oráculo vs clon 6/0 (p = 0,031)**.

**Lectura:** la memoria cubre 2 de 3 operaciones, pero el modelo **no completa la
tercera** desde dos ejemplos. El placebo y el historial tampoco. Solo el programa
completo despega. **No hay ventaja de memoria en 3 operaciones**; el cuello es la
operación que falta.

## 3. Piloto de 2 operaciones (exploratorio)

La tarea es el motivo completo; el oráculo y la memoria contienen el mismo programa
de 2 operaciones.

| Condición | Acierto |
|---|---|
| Clon | 5/12 |
| Memoria | 7/12 |
| Placebo | 4/12 |
| **Historial** | **9/12** |
| **Oráculo** | **11/12** |

Pares:

| Comparación | Acierta A / falla B | Acierta B / falla A | p |
|---|---|---|---|
| Memoria vs clon | **5** | 3 | 0,73 |
| Memoria vs placebo | **4** | 1 | 0,38 |
| Memoria vs historial | 1 | **3** | 0,63 |
| Oráculo vs clon | **6** | 0 | **0,031** |
| Historial vs clon | **6** | 2 | 0,29 |

**Lectura:**

1. **Primera señal positiva de memoria:** 7/12 frente a clon 5/12 y placebo 4/12.
   Cinco pares a favor del clon y cuatro del placebo.
2. **El historial crudo supera al programa verificado:** 9/12 vs 7/12. Doce ejemplos
   de la transformación son más útiles que la subrutina explícita.
3. **El oráculo es el mejor:** 11/12 con el **mismo programa** que la memoria. La
   diferencia es el encuadre: «programa completo, aplícalo» frente a «subrutina
   candidata, verifícala y úsala si encaja». El contenido no cambia; la instrucción sí.
4. **El placebo no supera a la memoria** (4 vs 7): el resultado del 007B de 5 pasos
   —placebo 6, memoria 3— no se replica en el régimen aplicable. Allí era suelo y
   ruido; aquí la memoria tiene contenido útil.
5. **La longitud no explica todo:** el historial es el prompt más largo (853 chars) y
   acierta 9/12; el oráculo es el más corto (371) y acierta 11/12; la memoria (458)
   acierta 7/12.

## 4. Qué significa para el problema de la memoria

- **La memoria sirve, pero el encuadre la limita.** El mismo programa rinde 7/12 como
  «candidata» y 11/12 como «programa completo». Antes de concluir que la memoria no
  funciona, hay que separar contenido de instrucción.
- **Las experiencias crudas son un competidor fuerte.** Si el historial de 12
  ejemplos supera al artefacto, la ventaja del artefacto no es la información: es la
  compresión, y esa compresión está costando fidelidad.
- **El régimen correcto es 2 operaciones.** En 3 y 5 el modelo no aplica; en 2 hay
  margen y la memoria se mueve.

## 5. Lo que sigue: MEM-003 (encuadre)

Pre-registrado en `../mem-003/protocolo.md`. Condiciones a 2 operaciones:

| Condición | Encuadre |
|---|---|
| `clone` | Sin artefacto |
| `memory_candidate` | «Subrutina candidata; verifícala y úsala si encaja» |
| `memory_verified` | «Programa retenido y verificado; aplícalo» |
| `history` | Los 12 pares de origen |
| `placebo` | Programa falso con el mismo encuadre |
| `oracle` | «Programa completo de esta tarea; aplícalo» (fuga) |

Hipótesis: si `memory_verified` ≈ `oracle`, el contenido es usable y el problema era
el encuadre. Si `memory_verified` sigue por debajo, el modelo no aplica un programa
retenido ni siquiera cuando se le presenta como definitivo.

## 6. Límites

- Dos pilotos, 12 tareas, una semilla, un modelo. No son confirmatorios.
- El de 3 operaciones estaba pre-registrado; el de 2 es exploratorio.
- Las tareas empiezan por el motivo; es reutilización favorable.
- Los prompts no tienen la misma longitud: historial 853, memoria 458, oráculo 371.
- El placebo comparte `double` con el motivo; es parcialmente pertinente. Las clases
  de placebo (irrelevante, parcial, plausible, equivalente) quedan para MEM-003.
- El oráculo es una fuga deliberada; no es una condición de memoria.
- El análisis no corrige por comparaciones múltiples.

## 7. Reproducir

```powershell
$env:PYTHONPATH="src"
python -m ohmem.v7_transfer --n 12 --support 2 --suffix 1 `
  --session1-examples 12 --exact-ops `
  --conditions clone,memory,placebo,history,oracle `
  --model gpt-6-luna --effort low --timeout 120 `
  --out resources/investigation/mem-002/results/pilot-depth3.json

python -m ohmem.v7_transfer --n 12 --support 2 --suffix 0 `
  --session1-examples 12 --exact-ops `
  --conditions clone,memory,placebo,history,oracle `
  --model gpt-6-luna --effort low --timeout 120 `
  --out resources/investigation/mem-002/results/pilot-depth2.json
```
