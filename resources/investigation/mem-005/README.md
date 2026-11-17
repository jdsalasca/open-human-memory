# MEM-005 — Factorial: contenido, estado e instrucción

**Fecha:** 16 de noviembre de 2026
**Estado:** **ejecutado; el resultado positivo de MEM-003/004 queda reencuadrado.**
**Modelo:** `gpt-6-luna`, `reasoning_effort = low`, `codex-cli 0.169.0`.
**Código:** `src/ohmem/mem_005.py`. **Protocolo:** `protocolo.md`.
**Análisis:** `analyze.py`. **Datos:** `results/factorial-seed1.json`.

## 1. Pregunta

MEM-003/004 cambiaron dos cosas a la vez: el **estado comunicado** (candidata vs
verificada) y la **instrucción operativa** (verificar vs aplicar). También faltaba el
control de un **programa escrito por un programador** sin sesión previa. MEM-005
separa las variables en un factorial 2×2×2 y añade ese control.

## 2. Resultados

2 operaciones, 12 tareas, semilla 1, orden de condiciones aleatorizado por tarea.

| Condición | Acierto |
|---|---|
| Clon | 6/12 |
| Correcto · candidata · verificar | 8/12 |
| Correcto · candidata · aplicar | 9/12 |
| Correcto · verificada · verificar | 8/12 |
| **Correcto · verificada · aplicar** | **12/12** |
| Placebo · candidata · verificar | 6/12 |
| Placebo · candidata · aplicar | 4/12 |
| Placebo · verificada · verificar | 6/12 |
| **Placebo · verificada · aplicar** | **1/12** |
| **Escrito por un programador · verificada · aplicar** | **12/12** |

**Factorial (correcto / placebo):**

| Estado | Instrucción | Correcto | Placebo |
|---|---|---|---|
| Candidata | Verificar | 8 | 6 |
| Candidata | Aplicar | 9 | 4 |
| Verificada | Verificar | 8 | 6 |
| **Verificada** | **Aplicar** | **12** | **1** |

Pares clave:

| Comparación | Acierta A / falla B | Acierta B / falla A | p |
|---|---|---|---|
| Verificada+aplicar vs placebo verificado+aplicar | **11** | 0 | **0,001** |
| Verificada+aplicar vs candidata+aplicar | 3 | 0 | 0,25 |
| Verificada+aplicar vs verificada+verificar | 4 | 0 | 0,125 |
| Verificada+aplicar vs clon | **6** | 0 | **0,031** |
| **Aprendido vs escrito por un programador** | **0** | **0** | **1,0** |

## 3. Hallazgos

1. **El efecto grande está en una sola celda.** El contenido correcto supera al
   placebo 12 a 1 cuando el estado es verificado y la instrucción es aplicar (11
   pares, p = 0,001). En candidata+verificar el contenido apenas separa (8 vs 6; 3/1,
   p = 0,625). **No es un efecto general del contenido ni de la etiqueta: es la
   combinación de estado definitivo e instrucción de aplicar.**
2. **Los efectos individuales son direccionales, no significativos.** Verificada vs
   candidata, con instrucción de aplicar: 12 vs 9 (3/0, p = 0,25). Aplicar vs
   verificar, con estado verificado: 12 vs 8 (4/0, p = 0,125). La muestra no los
   establece; el factorial muestra que la interacción es lo que produce el 12/12.
3. **El programa escrito por un programador acierta lo mismo que el aprendido**
   (12/12 vs 12/12, cero pares discordantes). **La adquisición previa no añade nada
   en esta tarea.** El resultado es del contenido correcto más la instrucción
   definitiva, no de la memoria ni del proceso de aprendizaje.
4. **La autoridad aplicada a contenido falso es peligrosa.** Placebo+verificada+aplicar
   acierta 1/12: el modelo aplica el programa falso porque la etiqueta dice
   «verificado». Es **obediencia a la autoridad declarada**, no verificación.
5. **Las tareas ya eran identificables desde los dos ejemplos.** El clon acierta
   6/12; el artefacto entrega el programa explícito. El resultado mide **inferir
   frente a recibir**, no memoria de un hecho desconocido.

## 4. Qué cambia en la interpretación

MEM-003/004 mostraron una diferencia grande entre «candidata» y «verificada». MEM-005
muestra que esa diferencia **no era un efecto limpio de la memoria**:

- el contenido correcto solo despega en la celda verificado+aplicar;
- el mismo programa escrito por un programador rinde igual;
- la adquisición previa no aporta;
- el estado y la instrucción están confundidos en el contraste original.

**La formulación defendible es:** *en doce instancias de una transformación
identificable, entregar el procedimiento correcto como instrucción autoritativa y
aplicable mejora la ejecución frente a pedir que se infiera o que se verifique.* Es
una observación de **ingeniería de instrucciones**, no una demostración de memoria
acumulativa.

## 5. Lo que sigue

- **MEM-006:** varias memorias, recuperación autónoma, selección entre candidatos,
  tareas donde el evaluador no entregue el artefacto.
- **META-001:** ciclo longitudinal con familias nuevas, menos experiencias para el
  umbral, artefactos obsoletos y contradictorios.
- **Verificación y procedencia:** cómo establecer el ámbito, la obsolescencia y la
  confianza sin la función verdadera del generador.
- **Réplica:** 24 tareas, varias semillas, segundo modelo.

## 6. Límites

- Una semilla, 12 tareas, un modelo; no es confirmatorio.
- El programa escrito es el motivo `sort_asc → double`; el aprendido puede ser una
  variante equivalente (`double → sort_asc`). La comparación es de procedencia, no de
  contenido.
- Las tareas son de 2 operaciones e identificables desde los dos ejemplos.
- Los valores p no corrigen por comparaciones múltiples.
- El placebo comparte `double` con el motivo; es parcialmente pertinente.
- El orden se aleatorizó por tarea, pero el servicio puede variar.

## 7. Reproducir

```powershell
$env:PYTHONPATH="src"
python -m ohmem.mem_005 --n 12 --seed 1 --support 2 --session1-examples 12 `
  --exact-ops --model gpt-6-luna --effort low --timeout 120 `
  --out resources/investigation/mem-005/results/factorial-seed1.json
python resources/investigation/mem-005/analyze.py
```
