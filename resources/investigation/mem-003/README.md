# MEM-003 — El encuadre era el cuello: memoria verificada 11/12

**Fecha:** 16 de noviembre de 2026
**Estado:** **ejecutado, primer resultado positivo de memoria.**
**Modelo:** `gpt-6-luna`, `reasoning_effort = low`, `codex-cli 0.169.0`.
**Código:** `src/ohmem/v7_transfer.py` (condición `memory_verified`).
**Protocolo:** `protocolo.md`. **Análisis:** `analyze.py`.
**Datos:** `results/pilot-depth2-framing.json`.

## 1. Pregunta

En MEM-002, la memoria rindió 7/12 y el oráculo 11/12 con el mismo programa. La
memoria se presentaba como «subrutina candidata; verifícala y úsala si encaja»; el
oráculo, como «programa completo; aplícalo». ¿Explica el encuadre la brecha?

## 2. Diseño

2 operaciones, 12 tareas, 2 ejemplos de soporte. Seis condiciones pareadas:

| Condición | Encuadre | Programa |
|---|---|---|
| `clone` | Sin artefacto | — |
| `memory` | «Subrutina candidata; verifícala» | Correcto |
| `memory_verified` | «Programa retenido y verificado; aplícalo» | Correcto |
| `placebo` | «Subrutina candidata; verifícala» | Falso |
| `history` | Los 12 pares de origen | — |
| `oracle` | «Programa completo de esta tarea; aplícalo» | Correcto |

`memory` y `memory_verified` contienen **el mismo programa**. Solo cambia la
instrucción.

## 3. Resultados

| Condición | Acierto |
|---|---|
| Clon | 3/12 |
| Memoria candidata | 4/12 |
| Placebo | 3/12 |
| Historial | 10/12 |
| **Memoria verificada** | **11/12** |
| **Oráculo** | **12/12** |

Pares:

| Comparación | Acierta A / falla B | Acierta B / falla A | p |
|---|---|---|---|
| Verificada vs candidata | **7** | 0 | **0,016** |
| Verificada vs placebo | **8** | 0 | **0,008** |
| Verificada vs historial | 2 | 1 | 1,0 |
| Verificada vs oráculo | 0 | 1 | 1,0 |
| Candidata vs historial | 0 | **6** | **0,031** |
| Candidata vs placebo | 2 | 1 | 1,0 |
| Oráculo vs clon | **9** | 0 | **0,004** |

## 4. Hallazgos

1. **El encuadre era el cuello.** El mismo programa pasa de **4/12 a 11/12** al
   presentarlo como verificado y aplicable (7 pares, p = 0,016). El contenido era
   usable; la instrucción de «verificar una candidata» hacía que el modelo no lo
   aplicara.
2. **Con el encuadre definitivo, el contenido importa.** Verificada 11/12 vs placebo
   3/12 (8 pares, p = 0,008). No es solo una etiqueta: el programa correcto rinde.
3. **La memoria verificada empata con el historial y con el oráculo.** 11/12 vs
   10/12 vs 12/12; las diferencias no son significativas. El artefacto comprimido
   conserva la información necesaria en este régimen.
4. **El encuadre de candidata es tóxico.** Candidata 4/12 vs historial 10/12 (6
   pares, p = 0,031) y vs placebo 3/12 (sin diferencia). Pedirle al modelo que
   verifique una subrutina candidata en cada uso la vuelve peor que no darle nada.
5. **Esto reinterpreta el 007.** En 5 pasos, la tarea estaba fuera de la ejecución
   (oráculo 2/12) y el artefacto se presentaba como candidato. Dos causas
   independientes ocultaban el efecto. En 2 pasos, con encuadre definitivo, la
   memoria aparece.

## 5. La solución, con su riesgo

**La memoria verificada funciona si se presenta como conocimiento verificado y se
aplica, no si se re-verifica en cada uso.** El sistema debe distinguir:

- artefacto **candidato** → el agente lo verifica antes de usarlo;
- artefacto **verificado** → el agente lo aplica como autoritativo.

El riesgo inmediato: si el modelo confía en la etiqueta «verificado», un artefacto
falso etiquetado así podría colarse. **La verificación tiene que ser real, no una
frase del prompt.** El siguiente experimento debe incluir un **placebo verificado**:
un programa falso con el mismo encuadre definitivo. Si ese placebo también acierta
11/12, la ganancia es de la etiqueta, no del contenido, y el resultado no sirve.

## 6. Límites

- Una semilla, 12 tareas, un modelo. No es confirmatorio; hay que replicar con 24
  tareas y varias semillas.
- El encuadre cambia más de una palabra; la comparación es de autoridad/instrucción,
  no de un token aislado.
- El oráculo es una fuga deliberada.
- El historial tiene más tokens (853) que la memoria verificada (370).
- Las tareas empiezan por el motivo; es reutilización favorable.
- No se probó el **placebo verificado**; es el control crítico pendiente.

## 7. Reproducir

```powershell
$env:PYTHONPATH="src"
python -m ohmem.v7_transfer --n 12 --support 2 --suffix 0 `
  --session1-examples 12 --exact-ops `
  --conditions clone,memory,memory_verified,placebo,history,oracle `
  --model gpt-6-luna --effort low --timeout 120 `
  --out resources/investigation/mem-003/results/pilot-depth2-framing.json
python resources/investigation/mem-003/analyze.py
```
