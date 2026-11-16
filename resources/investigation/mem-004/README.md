# MEM-004 — Placebo verificado: la etiqueta no basta

**Fecha:** 16 de noviembre de 2026
**Estado:** **ejecutado, control adversarial superado.**
**Modelo:** `gpt-6-luna`, `reasoning_effort = low`, `codex-cli 0.169.0`.
**Código:** `src/ohmem/v7_transfer.py` (condición `placebo_verified`).
**Protocolo:** `protocolo.md`. **Análisis:** `analyze.py`.
**Datos:** `results/pilot-depth2-verified-placebo.json`.

## 1. Pregunta

MEM-003 encontró que el mismo programa pasa de 4/12 (candidata) a 11/12 (verificada).
¿La ganancia es del contenido o de la etiqueta «verificado»? Si un programa falso
etiquetado igual también acierta, el resultado no sirve.

## 2. Resultados

| Condición | Programa | Acierto |
|---|---|---|
| Clon | — | 5/12 |
| Memoria candidata | Correcto | 3/12 |
| **Memoria verificada** | Correcto | **10/12** |
| Placebo candidato | Falso | 2/12 |
| **Placebo verificado** | **Falso** | **0/12** |
| Historial | — | 9/12 |
| Oráculo | Correcto | 12/12 |

Pares:

| Comparación | Acierta A / falla B | Acierta B / falla A | p |
|---|---|---|---|
| Verificada vs placebo verificado | **10** | 0 | **0,002** |
| Verificada vs candidata | **8** | 1 | **0,039** |
| Verificada vs historial | 2 | 1 | 1,0 |
| Verificada vs oráculo | 0 | 2 | 0,5 |
| Placebo verificado vs clon | 0 | **5** | 0,063 |

## 3. Hallazgos

1. **La etiqueta no basta.** El programa falso etiquetado «retenido y verificado»
   acierta **0/12**, peor que el clon (5/12, 5 pares en contra). El modelo no se
   limita a confiar: **aplica el programa falso y falla**.
2. **El contenido manda.** Memoria verificada 10/12 vs placebo verificado 0/12:
   diez pares, p = 0,002. La ganancia de MEM-003 es del programa correcto, no de la
   frase «verificado».
3. **El encuadre se replica.** Verificada 10/12 vs candidata 3/12 (8 pares,
   p = 0,039). MEM-003 dio 11 vs 4. La diferencia es estable en las dos corridas.
4. **La memoria verificada empata con el historial y casi con el oráculo.** 10, 9 y
   12 sobre 12; sin diferencias significativas. El artefacto comprimido conserva la
   información en 2 operaciones.
5. **Implicación de seguridad:** un artefacto falso **etiquetado** como verificado se
   aplica con confianza y produce fallos. La etiqueta debe provenir de una
   verificación real fuera del prompt (nuestras 60 sondas), no de una frase que el
   modelo o el generador puedan escribir. **El modelo no puede ser el verificador de
   su propia memoria.**

## 4. La solución, con su condición

La memoria útil requiere tres cosas, y las tres son medibles:

1. **Tarea aplicable:** 2 operaciones efectivas (EXEC-001: 86 %).
2. **Artefacto verificado fuera del prompt:** el harness comprueba el programa con
   sondas; el modelo no se autoverifica.
3. **Encuadre definitivo:** el artefacto verificado se presenta como conocimiento
   aplicable, no como candidato a re-verificar. El encuadre de candidata cuesta
   6–8 pares.

Sin (2), el sistema es vulnerable a un placebo verificado (0/12, fallo seguro). Sin
(3), el modelo desaprovecha un artefacto correcto (3–4/12). Sin (1), ni el oráculo
funciona (2/12 en 5 pasos).

## 5. Límites

- Piloto de 12 tareas, una semilla, un modelo. M11 y M12 (réplica de 24 tareas)
  siguen abiertas.
- El placebo comparte `double` con el motivo; es parcialmente pertinente.
- La etiqueta es una frase del prompt; el experimento demuestra que no basta, pero no
  sustituye una verificación criptográfica o firmada.
- El oráculo es una fuga deliberada; no es una condición de memoria.
- Las tareas empiezan por el motivo; es reutilización favorable.
- El análisis no corrige por comparaciones múltiples.

## 6. Reproducir

```powershell
$env:PYTHONPATH="src"
python -m ohmem.v7_transfer --n 12 --support 2 --suffix 0 `
  --session1-examples 12 --exact-ops `
  --conditions clone,memory,memory_verified,placebo,placebo_verified,history,oracle `
  --model gpt-6-luna --effort low --timeout 120 `
  --out resources/investigation/mem-004/results/pilot-depth2-verified-placebo.json
python resources/investigation/mem-004/analyze.py
```
