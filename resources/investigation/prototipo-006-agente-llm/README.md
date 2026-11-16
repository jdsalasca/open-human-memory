# Prototipo 006-B — Test de techo con un agente real

**Fecha:** 16 de noviembre de 2026
**Estado:** diagnóstico exploratorio, una sola corrida.
**Agente:** `gpt-6-luna`, razonamiento `low`, `codex-cli 0.169.0`, modo
`--ephemeral`, sandbox `read-only`, sin herramientas, sin historial.
**Tareas:** las 64 de `DEPTH3_GRID`, semilla 0.
**Resultado crudo:** `results/gpt-6-luna-low-seed0.json` (incluye respuesta y
stderr de cada llamada).

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

- Un modelo, un esfuerzo (`low`), una corrida, semilla 0.
- Sin self-consistency, sin herramientas, sin few-shot de la familia.
- `low` es el ajuste más barato; con más esfuerzo el techo subiría.
- Comparación con nuestros solvers: ellos ven exactamente los mismos tres
  ejemplos, pero conocen el lenguaje de operaciones. El LLM no. No es una
  comparación de inteligencia; es una comparación de ajuste al dominio.
- Las 64 tareas no son 64 comportamientos: son 14 clases funcionales. La
  exactitud por clase no se reporta aquí.

## 6. Reproducir

```bash
$env:PYTHONPATH="src"
python -m ohmem.llm_ceiling --n 64 --model gpt-6-luna --effort low `
  --out resources/investigation/prototipo-006-agente-llm/results/gpt-6-luna-low-seed0.json
```

Requiere `codex` autenticado. Coste aproximado: 64 llamadas, ~7 s cada una.
