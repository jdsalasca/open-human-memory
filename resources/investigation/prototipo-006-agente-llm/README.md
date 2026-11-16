# Prototipo 006-B — Línea base con un agente real

**Fecha:** 16 de noviembre de 2026
**Estado:** **diagnóstico exploratorio con errata**. Tres inferencias publicadas
fueron invalidadas: `retrieved` era memoria seleccionada por oráculo, la muestra de
24 tareas estaba sesgada y la condición de herramienta estaba contaminada por
errores de entorno. Ver `docs/errata-006b.md` antes de citar cualquier cifra.
**Agente:** `gpt-6-luna`, razonamiento `low`, `codex-cli 0.169.0`, modo
`--ephemeral`, sandbox `read-only`, sin herramientas, sin historial.
**Tareas:** las 64 de `DEPTH3_GRID`, semilla 0.
**Resultado crudo:** `results/gpt-6-luna-low-seed0.json` (incluye respuesta y
stderr de cada llamada).

> **No es un techo.** Es una línea base de un modelo barato, sin herramientas, con
> una sola tentativa. Un techo experimental exigiría el mejor esfuerzo disponible.

## 1. La pregunta

Antes de seguir construyendo memoria: **¿un agente real resuelve estas tareas de
un vistazo?** Si las resolvía todas, el banco sintético no servía para medir nada
y había que migrar a tareas reales.

## 2. Diseño

Cada tarea se presenta como tres pares `entrada -> salida` y una entrada a
transformar. El agente responde solo con la lista. Una llamada por tarea, sin
memoria entre llamadas. Salida forzada por JSON Schema (`query_output`).

Prompt: inferir la transformación y aplicarla, sin usar herramientas ni ejecutar
código.

## 3. Resultado

| Métrica | Valor |
|---|---|
| Aciertos | **30 / 64** |
| Exactitud | **46,9 %** |
| Tiempo medio por tarea | ~7 s |
| Llamadas con error de proceso | 0 |

Comparación con nuestros solucionadores en la misma rejilla:

| Solucionador | Exactitud |
|---|---|
| `gpt-6-luna` low, 3 ejemplos, sin historial | **46,9 %** |
| BFS profundidad 2, 4 primitivas | 51,6 % |
| BFS profundidad 3, 4 primitivas | **100 %** |

## 4. Lectura

- **El banco no está saturado.** Un agente general falla más de la mitad. La
  conclusión de que «el espacio es diminuto y enumerable» vale para el
  solucionador exhaustivo, no para un LLM.
- **El LLM queda por debajo de una búsqueda exhaustiva de dos pasos.** En esta
  familia, la tarea es inducción exacta de programas, no razonamiento en lenguaje
  natural. El agente comete errores de orden y de aritmética: por ejemplo, en
  `sort_asc → double` devuelve los valores correctos desordenados.
- **Los fallos son de resolución, no de memoria.** No dicen nada sobre
  acumulación; dicen que el agente no identifica el programa con tres ejemplos.
- Esto **abre** el experimento que importa: dar al agente un procedimiento
  recuperado o compilado y medir si sube del 47 % al techo. Si no sube, la memoria
  no ayuda al agente aunque el procedimiento sea correcto.

## 5. Límites

- Un modelo, un esfuerzo (`low`), una corrida, semilla 0 para el techo de 64 tareas.
- El diagnóstico usa **24 tareas**: los intervalos son de ±20 pp y no permiten
  detectar efectos pequeños. Los signos son indicativos, no concluyentes.
- Sin self-consistency, sin few-shot de la familia, sin `high` effort.
- `low` es el ajuste más barato; con más esfuerzo el techo subiría.
- El sandbox es efímero: los archivos escritos no persisten, así que la única
  verificación válida del uso de herramientas es el transcript.
- Comparación con nuestros solvers: ellos ven exactamente los mismos tres
  ejemplos, pero conocen el lenguaje de operaciones. El LLM no. No es una
  comparación de inteligencia; es una comparación de ajuste al dominio.
- Las 64 tareas no son 64 comportamientos: son 14 clases funcionales. La
  exactitud por clase no se reporta aquí.

## 7. Diagnóstico: información, representación, memoria

Mismas 24 tareas, comparación pareada, `gpt-6-luna` low, una llamada por tarea:

| Condición | Aciertos | Puntos | Δ vs base | IC 95 % pareado |
|---|---|---|---|---|
| `base` (3 ejemplos) | 14/24 | 58,3 % | — | — |
| `more_examples` (6 ejemplos) | 16/24 | 66,7 % | +8,3 pp | −20,8 a +33,3 |
| `vocabulary` (se nombran las 4 operaciones) | 15/24 | 62,5 % | +4,2 pp | −12,5 a +25,0 |
| **`ORACLE-MEMORY`** (memoria fabricada con la solución) | 16/24 | 66,7 % | +8,3 pp | −12,5 a +33,3 |
| `tool` (intérprete disponible, sin exigir uso) | 10/24 | 41,7 % | no usado | ver nota |
| `tool-forced` (intérprete exigido, ejecución **no verificada**) | 14/24 | 58,3 % | inválida | ver nota |

Pares discordantes frente a `base`: `more_examples` 7 mejora / 5 empeora;
`vocabulary` 3 / 2; `ORACLE-MEMORY` 5 / 3; `tool-forced` 6 / 6.

### Errata: esta sección tenía tres fallos

**`ORACLE-MEMORY` no es recuperación.** La condición construía la memoria con
`task.solution.program`, es decir, con la solución verdadera de la tarea evaluada.
Mide un **techo de información**, no memoria. El archivo histórico se llama
`retrieved-24.json`, pero su contenido es oráculo.

**La muestra está sesgada.** `make_depth3_grid()[:24]` toma 16 tareas que empiezan
por `sort_asc` y 8 por `sort_desc`; ninguna por `add_one` o `double`.

**La condición de herramienta es inválida.** En 16 de 24 trazas hay errores de
permisos o archivos (intentos de escribir en `C:\Program Files\PowerShell\7`,
scripts no creados). El exit 0 de Codex no es el exit del script interno. No se
verificaron las cinco etapas: disponibilidad, intento, ejecución, validación y uso.

Detalle completo en `docs/errata-006b.md`.

### Lectura corregida

1. **Ninguna intervención se distingue de cero.** Con 24 tareas el IC es de ±20 pp;
   el piloto es compatible con mejoras y perjuicios grandes.
2. **`ORACLE-MEMORY` y más ejemplos dan el mismo +8,3 pp**, pero el primero conoce
   la respuesta: no se puede atribuir a memoria.
3. **Nombrar el lenguaje de operaciones casi no ayuda** (+4,2 pp), dentro del ruido.
4. **La condición de intérprete no permite concluir nada**: estaba contaminada por
   fallos de entorno y 5 respuestas quedaron vacías.
5. **La conclusión anterior («el cuello es identificar el programa») se retira.**
   Infería una capacidad cognitiva desde un piloto con intervalos que cruzan cero y
   dos condiciones inválidas.

Lo que queda: una línea base de **46,9 % (30/64)** sin ayuda, y la lista de cinco
fallos metodológicos que hay que evitar antes de medir memoria. El cuello de
botella sigue **abierto**; para localizarlo hace falta el 007A
(`docs/problema-central.md`).



## 8. Reproducir

```bash
$env:PYTHONPATH="src"
python -m ohmem.llm_ceiling --n 64 --model gpt-6-luna --effort low `
  --out resources/investigation/prototipo-006-agente-llm/results/gpt-6-luna-low-seed0.json
```

Requiere `codex` autenticado. Coste aproximado: 64 llamadas, ~7 s cada una.
