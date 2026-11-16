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
| `retrieved` (una tarea resuelta de la misma transformación) | 16/24 | 66,7 % | +8,3 pp | −12,5 a +33,3 |
| `tool` (intérprete disponible, sin exigir uso) | 10/24 | 41,7 % | no usado | ver nota |
| `tool-forced` (uso exigido y verificado por transcript) | 14/24 | 58,3 % | 0,0 pp | −29,2 a +29,2 |

Pares discordantes frente a `base`: `more_examples` 7 mejora / 5 empeora;
`vocabulary` 3 / 2; `retrieved` 5 / 3; `tool-forced` **6 / 6**.

### Nota sobre `tool`: disponibilidad no es uso, y archivos no son ejecución

La primera versión de la condición con intérprete dio **10/24 (41,7 %)**, *peor* que
`base`, con tiempos idénticos (7,2 s vs 8,8 s) y **13 de 24 respuestas
byte-idénticas**. El agente **no usó la herramienta**. Se retira como evidencia
sobre herramientas; solo muestra que «tener un intérprete» no implica «ejecutar».

La segunda versión exigió escribir y ejecutar un script. El transcript de Codex
confirma `python .\solution.py` con código 0 y salida correcta, y la latencia subió
a **29,4 s** (3,3×). Sin embargo, el chequeo de archivos dio 0/24: el sandbox es
efímero y no persiste lo escrito. Por tanto, **la verificación válida es el
transcript, no los archivos**.

Resultado: **14/24 (58,3 %), idéntico a `base`**, con 6 tareas que mejoran y 6 que
empeoran, y 5 respuestas vacías (el script no llegó a reproducir los ejemplos y el
agente se rindió).

### Lectura

1. **Ninguna intervención se distingue de cero.** Con 24 tareas, el IC es de ±20 pp.
   Para detectar +8 pp con confianza harían falta ~150 tareas pareadas.
2. **La memoria recuperada y más ejemplos dan el mismo +8,3 pp.** Eso es
   exactamente el confundidor que la auditoría señaló: una experiencia resuelta
   *es* información adicional. Con este diseño no se puede atribuir la mejora a
   memoria en vez de a información.
3. **Nombrar el lenguaje de operaciones casi no ayuda** (+4,2 pp): el fallo no es
   de representación.
4. **El intérprete, usado de verdad, no mejora nada** (0,0 pp) y cuesta 3,3× más
   tiempo. El fallo tampoco es de cálculo exacto.
5. **El agente sigue fallando 8/24 con una tarea resuelta delante y 10/24 con un
   script ejecutado.** El patrón es de **identificación del programa**: con tres
   ejemplos hay muchas transformaciones compatibles, y el agente elige una que
   falla en la consulta.

Conclusión del diagnóstico: el cuello de botella del agente en este banco es
**inducir la transformación correcta**, no recordar, ni representar, ni ejecutar.
La consecuencia para el 007 es que la memoria solo puede ayudar si entrega un
**procedimiento verificado** —no más ejemplos ni un intérprete—, y que su valor
debe medirse contra el clon sin historial, no contra el agente sin ayuda.



## 8. Reproducir

```bash
$env:PYTHONPATH="src"
python -m ohmem.llm_ceiling --n 64 --model gpt-6-luna --effort low `
  --out resources/investigation/prototipo-006-agente-llm/results/gpt-6-luna-low-seed0.json
```

Requiere `codex` autenticado. Coste aproximado: 64 llamadas, ~7 s cada una.
