# 007B — El cuello es la ejecución, no la memoria

**Fecha:** 16 de noviembre de 2026
**Estado:** **ejecutado, resultado negativo con diagnóstico útil.**
**Modelo:** `gpt-6-luna`, `reasoning_effort = low`, `codex-cli 0.169.0`.
**Código:** `src/ohmem/v7_transfer.py` (condiciones `history` y `oracle`).
**Protocolo:** `protocolo.md`. **Análisis:** `analyze_conditions.py`.
**Datos:** `results/luna-low-support2-history-oracle.json` (corrida limpia),
`results/luna-low-support2-history-oracle-attempt1.json` (réplica reconstruida),
combinados con
`../prototipo-007-transferencia/results/luna-low-support2-12ex.json`.

## 1. La pregunta

El 007 mostró que la memoria verificada no supera a un placebo, pero no explicó
**por qué**. El 007B separa tres cosas que el 007 confundía:

1. **Información:** ¿el artefacto aporta algo que el clon no tiene?
2. **Instrucción:** ¿importa que sea un programa verificado y no las experiencias
   crudas?
3. **Ejecución:** ¿el modelo puede resolver la tarea cuando **ya conoce** el
   programa completo?

## 2. Diseño

**Motivo (2 operaciones):** `sort_asc → double`. Sesión 1 con 12 pares y
«exactamente 2 operaciones»; verificación con 60 sondas. `luna` devolvió
`double → sort_asc`, conductualmente equivalente.

**Sesión 2.** 12 tareas de **5 pasos**: el motivo más tres operaciones aleatorias.
Dos ejemplos de soporte. Cinco condiciones pareadas:

| Condición | Qué recibe |
|---|---|
| `clone` | Solo la tarea |
| `memory` | El programa verificado de 2 operaciones |
| `placebo` | Un programa falso de 2 operaciones (`sort_desc → double`) |
| `history` | Los 12 pares de la sesión 1 (experiencias de origen) |
| `oracle` | El programa completo de 5 operaciones (**fuga; control de ejecución**) |

Las tres primeras condiciones ya estaban medidas en el 007 (soporte 2). Esta corrida
añade `history` y `oracle` con la misma semilla, tareas y soporte.

## 3. Resultados

| Condición | Acierto | Réplica |
|---|---|---|
| `clone` | 1/12 | — |
| `memory` | 3/12 | — |
| `placebo` | **6/12** | — |
| `history` | 4/12 | 3/12 |
| `oracle` | **2/12** | 3/12 |

Pares discordantes (corrida limpia):

| Comparación | Acierta A / falla B | Acierta B / falla A | p (signos) |
|---|---|---|---|
| `memory` vs `clone` | 3 | 1 | 0,63 |
| `memory` vs `placebo` | 1 | **4** | 0,38 |
| `memory` vs `history` | 1 | 2 | 1,00 |
| `oracle` vs `clone` | 0 | 1 | 1,00 |
| `placebo` vs `oracle` | **5** | 1 | 0,22 |
| `history` vs `oracle` | 3 | 1 | 0,63 |

Caracteres medios del prompt: `history` 856, `oracle` 406. El historial es más
largo; la comparación iguala información, no longitud.

## 4. Lectura

1. **El oráculo está en el suelo.** Con el programa completo, `luna` acierta **2/12**
   (réplica 3/12). No es un problema de memoria ni de información: el modelo **no
   ejecuta** composiciones de 5 pasos de forma fiable. Los errores están en la
   aplicación del programa (permutaciones, operaciones saltadas), no en su
   identificación: el programa se le dio completo.
2. **La memoria no supera al historial.** 3/12 vs 4/12; un par a favor y dos en
   contra. El programa verificado no aporta sobre las experiencias crudas.
3. **La memoria no supera al placebo.** 3/12 vs 6/12; cuatro pares a favor del
   placebo. El contenido verificado no explica la diferencia.
4. **La memoria sí supera al clon, pero poco.** Tres pares a favor y uno en contra
   (p = 0,63): una señal débil, compatible con ruido.
5. **El resultado del 007 se reinterpreta.** No es evidencia contra la retención:
   es evidencia de que la familia de 5 pasos está **fuera del alcance de ejecución**
   de `luna` low. Cualquier intervención de memoria está acotada por ese techo.

## 5. Adquisición de motivos largos (fallo)

Se intentó un artefacto de 3–4 operaciones para cubrir más pasos. `luna` low no lo
adquiere:

| Motivo | Ejemplos | Programa devuelto | ¿Verifica? |
|---|---|---|---|
| `sort_asc → double → add_one → negate` | 12 | `negate → double → reverse → add_one` | No |
| `sort_asc → double → add_one → negate` | 24 | `negate → double → add_one → sort_desc` | No |
| `double → add_one → negate` | 12 | `negate → double → add_one` | No |
| `double → add_one → negate` | 24 | `double → negate → add_one` | No |

Los cuatro motivos son identificables: la enumeración exhaustiva deja 1–4 programas
consistentes, todos conductualmente equivalentes. El fallo es de **búsqueda**, no de
información. No se relajó la verificación.

## 6. Qué sigue

- **F1 primero:** medir la capacidad de ejecución por profundidad y clase. Elegir una
  profundidad donde el clon ejecute (no el suelo) y donde el procedimiento no sea
  inferible de dos ejemplos.
- **Después, memoria:** con una tarea que el clon pueda ejecutar pero no identificar,
  comparar memoria, historial y placebo. Sin ese margen, el experimento mide
  ejecución, no memoria.
- **No escalar el motivo:** 3–4 operaciones tampoco se adquieren con `luna` low.

## 7. Límites

- Una semilla, 12 tareas, un modelo. Los conteos no permiten significación.
- **Sesgo de construcción:** las tareas empiezan por el motivo; es reutilización
  favorable, no transferencia a una familia independiente.
- El historial tiene más tokens que el artefacto; no se iguala longitud.
- `oracle` es una fuga deliberada y se etiqueta como tal.
- La réplica se reconstruyó de los directorios temporales tras un fallo de escritura
  (la corrida original no guardó el JSON); el orden de las llamadas es el de creación
  de los directorios.
- La corrida limpia usó un timeout de 120 s; no hubo timeouts.
- El análisis pareado no corrige por comparaciones múltiples.

## 8. Reproducir

```powershell
$env:PYTHONPATH="src"
python -m ohmem.v7_transfer --model gpt-6-luna --effort low --timeout 120 `
  --n 12 --support 2 --session1-examples 12 --exact-ops `
  --conditions history,oracle `
  --out resources/investigation/prototipo-007b-transferencia/results/luna-low-support2-history-oracle.json
python resources/investigation/prototipo-007b-transferencia/analyze_conditions.py
```
