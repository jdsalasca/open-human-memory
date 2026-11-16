# Errata del diagnóstico 006-B

**Fecha:** 16 de noviembre de 2026
**Origen:** auditoría de rumbo sobre `b7b1c6d`.
**Alcance:** invalida tres inferencias publicadas. No cambia los archivos de
resultados; cambia lo que se puede afirmar con ellos.

---

## 1. `retrieved` no era recuperación: era memoria seleccionada por oráculo

El código construía la memoria así:

```python
memory = make_task(900, "delta", 7000 + index, task.solution.program, "mem")
```

`task.solution.program` es **la solución verdadera de la tarea evaluada**. El
sistema no buscaba un recuerdo pertinente entre experiencias disponibles: fabricaba
una experiencia cuya transformación coincide exactamente con la respuesta correcta.

Por tanto:

- **Lo que sí muestra:** un techo de información. Dar al agente un ejemplo resuelto
  de la transformación exacta produce +8,3 pp (16/24 vs 14/24), con IC −12,5 a
  +33,3 y 5 tareas que mejoran frente a 3 que empeoran.
- **Lo que no muestra:** que un recuperador autónomo encuentre ese recuerdo, ni que
  la memoria ayude cuando la selección es imperfecta.
- **Lo que no se puede decir:** «la memoria recuperada mejora al agente».

**Reetiquetado:** la condición pasa a llamarse **`ORACLE-MEMORY`** en toda la
documentación. El archivo `retrieved-24.json` se conserva como histórico con ese
nombre de archivo, pero su contenido es oráculo.

**Condición que falta:** `ACTUAL-RETRIEVAL`, donde el recuperador ve **solo** la
observación de la tarea actual (entradas, salidas de soporte, consulta) y elige un
recuerdo de un histórico previamente construido. Si el recuperador falla, el fallo
cuenta. Sin esa condición, no hay evidencia sobre memoria.

---

## 2. La muestra de 24 tareas está sesgada por el orden del producto cartesiano

`make_depth3_grid()` enumera `product(PRIMITIVES, repeat=3)` con
`PRIMITIVES = (sort_asc, sort_desc, add_one, double)`. Tomar `[:24]` da:

| Prefijo | Tareas incluidas |
|---|---|
| `sort_asc` | 16 |
| `sort_desc` | 8 |
| `add_one` | **0** |
| `double` | **0** |

La muestra **no representa el espacio definido**. Cualquier conclusión sobre «el
agente» a partir de esas 24 filas es en realidad una conclusión sobre las tareas
que empiezan por ordenamiento.

**Corrección exigida:** estratificar por **clase conductual**, no por fila. El
prototipo 005 identificó 14 clases sobre 40 sondas; una muestra equilibrada debe
tomar representantes de cada clase, con instancias numéricas nuevas.

---

## 3. `tool-forced` no es una condición válida sobre herramientas

La auditoría revisó las trazas: **16 de 24** contienen errores o indicios de
problemas de permisos y archivos (intentos de escribir en
`C:\Program Files\PowerShell\7`, scripts que no llegan a crearse). El fragmento de
`stderr` está truncado, así que 16 no es un conteo definitivo, pero basta para
invalidar la condición.

Además, el código de salida 0 de Codex **no** demuestra que el script interno
terminara bien. Se confundieron cinco etapas distintas:

| Etapa | ¿Verificada? |
|---|---|
| Disponibilidad de la herramienta | Sí |
| Intento de uso | Parcial (latencia 3,3×) |
| Ejecución exitosa del script | **No** |
| Validación de los tres ejemplos | **No** |
| Uso del resultado en la respuesta final | **No** |

**Se retira la inferencia** «ejecutar no mejora el acierto». Lo que queda es: en un
entorno con fallos de integración, el acierto fue 14/24. Eso no dice nada sobre el
efecto de un intérprete fiable.

**Corrección exigida:** registrar por tarea las cinco etapas (comando exacto, exit
code del script, salida, validación de los tres ejemplos, origen de la respuesta
final). Sin eso, ninguna condición con herramientas es interpretable.

---

## 4. Ausencia de significación no es ausencia de efecto

Los intervalos son de ±20 pp. Un IC de −20,8 a +33,3 es compatible con una mejora
grande y con un perjuicio grande. La frase correcta es:

> **El piloto no permite decidir.** No que la intervención no funcione.

La conclusión publicada («el cuello es identificar la transformación») **se
retira**. Lo que se puede afirmar:

- El agente acierta 46,9 % en 64 tareas y 58,3 % en las 24 primeras, sin ayuda.
- Ninguna de las cuatro intervenciones produce una diferencia distinguible de cero
  **en esta muestra**, con estos fallos de implementación.
- La hipótesis del cuello de botella queda **abierta**.

---

## 5. Qué sobrevive

1. **El techo de 46,9 % (30/64)** con `gpt-6-luna` low, 3 ejemplos, sin historial.
   Es una línea base, no un «techo», y arrastra la correlación entre clases
   conductuales.
2. **La tabla de costes y latencias**: el intérprete multiplica por 3,3 el tiempo.
3. **El valor metodológico**: el piloto encontró los cinco fallos que habría que
   evitar en cualquier evaluación de memoria.

## 6. Regla que se adopta

Toda condición que use información privilegiada se etiqueta `ORACLE-*`. Toda
condición con herramientas registra las cinco etapas. Toda muestra se estratifica
por clase conductual. Y ninguna conclusión sobre mecanismos se extrae de un piloto
con intervalos que cruzan cero.
