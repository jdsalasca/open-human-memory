# Registro de afirmaciones

**Fecha:** 16 de noviembre de 2026
**Para qué:** evitar que el proyecto gire en círculos. Cada afirmación tiene estado,
nivel de evidencia y falsador. Si una afirmación no está aquí, no existe.

**Niveles** (definidos en `precedentes/09`, sección 9.5): E0 idea, E1 mecanismo
implementado, E2 comparación controlada local, E3 varias distribuciones, E4
reproducción independiente con tareas reales, E5 longitudinal y transferencia.

**Estados:** sostenida, refutada, abierta, inválida (no interpretable), declarada
(afirmación de terceros, no replicada) y no demostrada (nuestra, sin prueba). Una
afirmación **sostenida (local)** no es una ley: es un resultado de una muestra,
modelo y semilla. El resumen de totales está al final; el verificador
`docs/verificar_afirmaciones.py` comprueba que los documentos citen el mismo total.

**Retractaciones:** la sección I (LIRE-001b) está parcialmente retractada; la
sección L incluye el resultado positivo condicionado de MEM-003/004 y la sección N
las réplicas pendientes. Las afirmaciones negativas del 007 se conservan; su lectura
cambia con el diagnóstico de EXEC-001.

---

## A. Afirmaciones metodológicas

| ID | Afirmación | Estado | Evidencia |
|---|---|---|---|
| M1 | El 001 filtraba la regla en la superficie (target leakage) | Refutada como evidencia | `prototipo-001` |
| M2 | El 002 no usaba el historial: `MEM-A0` empata con `MEM-E` | Sostenida | `prototipo-002`, 3 semillas |
| M3 | El «100 % en D3» del 003 era artefacto del límite de profundidad 2 | Sostenida | 004-A: 64/64 sin memoria |
| M4 | El control `RANDOM` del 003 estaba ama­ñado (usaba `reverse`/`negate`) | Sostenida | 004-A: 250/560 perfectas del mismo lenguaje |
| M5 | La muestra `[:24]` del 006-B está sesgada (16 `sort_asc`, 8 `sort_desc`) | Sostenida | `errata-006b.md` |
| M6 | La condición `retrieved` del 006-B era oráculo, no recuperación | Sostenida | usaba `task.solution.program` |
| M7 | La condición `tool-forced` del 006-B no es interpretable | Sostenida | 16/24 trazas con errores de entorno |
| M8 | La ausencia de significación no es ausencia de efecto | Sostenida | IC ±20 pp |

## B. Afirmaciones sobre el mecanismo (macros)

| ID | Afirmación | Estado | Nivel | Falsador |
|---|---|---|---|---|
| H1 | Una biblioteca de macros reduce candidatos | Sostenida | E2 | — |
| H2 | Esa reducción es del 17,8 % en la rejilla completa | Sostenida | E2 | — |
| H3 | La reducción viene con 15,6 pp menos de cobertura | Sostenida | E2 | — |
| H4 | Con profundidad 3 permitida, la biblioteca encarece la búsqueda (+27,6 %) | Sostenida | E2 | — |
| H5 | La cobertura conductual de la biblioteca es 9/14 | Sostenida | E2 | — |
| H6 | La adquisición satura en 6 experiencias | Sostenida | E2 | — |
| H7 | El ahorro por acierto es 2,6 % | Sostenida | E2 | — |
| H8 | Las macros del 003 amplían la cobertura máxima en su D3 | **Refutada** | — | 004-A |
| H9 | La memoria puede mejorar competencia efectiva bajo presupuesto limitado | **Abierta** | — | P1, P2 |

## C. Afirmaciones sobre el valor de la memoria

| ID | Afirmación | Estado | Nivel | Falsador |
|---|---|---|---|---|
| V1 | Con continuidad 1,0, igual cobertura con 41,8 % menos pasos | Sostenida | E2 | — |
| V2 | Con continuidad 0,0, el mismo trabajo rinde 22,1 pp menos | Sostenida | E2 | — |
| V3 | Congelar lo aprendido ahorra 26,2 % de trabajo con igual precisión | Sostenida | E2 | — |
| V4 | Seguir acumulando empeora (−8,7 pp) | Sostenida | E2 | Política distinta que no empeore |
| V5 | El desalojo por uso arregla la acumulación | **Refutada** | — | −10,8 pp |
| V6 | La memoria recuperada ayuda a un LLM | **Inválida** | — | `ORACLE-MEMORY` |
| V7 | Un intérprete fiable ayuda a un LLM | **Abierta** | — | Condición inválida |

## D. Afirmaciones sobre la política

| ID | Afirmación | Estado | Nivel | Falsador |
|---|---|---|---|---|
| P1 | Una política lineal aprende a cambiar entre memoria y búsqueda | Sostenida | E2 | — |
| P2 | Esa política supera a una regla de una línea | **Refutada** | — | −1,0 pp, IC −3,1 a 0 |
| P3 | El probe de aplicabilidad aporta información | Sostenida | E2 | +5,2 pp sobre barajada, IC 1,0–9,4 |
| P4 | El probe paga su coste | **Refutada** | — | 41 pasos vs 29 ahorrados |
| P5 | Un controlador con más acciones ayudaría | **Abierta** | — | Sin evidencia |

## E. Afirmaciones teóricas

| ID | Afirmación | Estado | Nivel | Falsador |
|---|---|---|---|---|
| T1 | En espacio **explorable, identificable y dentro del presupuesto**, la memoria no amplía cobertura | Sostenida **con condiciones** | E0 + 004/006 | Un contraejemplo que cumpla las tres condiciones |
| T2 | En espacio no explorable bajo el presupuesto, una herramienta compilada amplía cobertura | **Abierta** (P1) | — | Cobertura igual sin historial |
| T3 | A igual información, un procedimiento bate a un episodio | **Abierta** (P2) | — | Un intervalo de equivalencia con margen fijado descarta una ventaja superior al mínimo relevante |
| T4 | La ventaja de adquisición es **mayor** con estructura compartida que con solo vocabulario compartido | **Abierta** (P3) | — | No hay interacción estructura × vocabulario |
| T5 | El efecto sobrevive a cambiar de modelo | **Abierta** (P5) | — | Desaparece |
| T6 | Elegir la **forma** del conocimiento según utilidad futura bate a una forma fija | **Abierta** (P6) | — | Una forma fija iguala o supera |

## F. Afirmaciones sobre las fuentes

| ID | Afirmación | Estado |
|---|---|---|
| F1 | DreamCoder, Stitch y LILO cubren aprendizaje de bibliotecas | Sostenida (lectura) |
| F2 | CEGIS y Angluin cubren aprendizaje activo y contraejemplos | Sostenida (lectura) |
| F3 | MemDev-Bench muestra que la memoria puede romper tareas antes resolubles | **Sostenida y verificada** |
| F4 | La neurociencia y la sociología han aportado hipótesis comprobables | **Refutada**: solo analogías |
| F5 | Se ha ejecutado una revisión sistemática exhaustiva | **Refutada**: estructurada, una base, un revisor |
| F6 | Se ha reproducido un competidor | **Refutada**: ninguno |
| F7 | Existe una revisión estructurada con búsquedas y cribado registrados | **Sostenida** (`revision-sistematica/`) |
| F8 | La verificación independiente de skills ya está implementada y es imprescindible | **Declarada por terceros; no replicada** |
| F9 | Las bibliotecas de skills degradan al crecer | **Declarada por terceros; no replicada** |
| F10 | El lift agregado de retrieval no implica uso efectivo | **Declarada por terceros; no replicada** |
| F11 | La memoria episódica no mejora el resolve rate en código | **Declarada por terceros; no replicada** |
| F12 | Solo tres filas de la revisión están verificadas documentalmente; el resto son declaradas por los autores | **Sostenida** (extraccion.md) |
| F13 | Ninguna cifra de la revisión está replicada | **Sostenida** |

## G. Retención y transferencia (Prototipo 007)

> **Evidencia:** `gpt-6-luna` low, 12 tareas por condición. Las cifras de
> `gpt-6.1-terra` medium son exploratorias y no cuentan como evidencia.

| ID | Afirmación | Estado | Nivel | Falsador |
|---|---|---|---|---|
| G1 | Con 6 ejemplos, `luna` no produjo un artefacto verificado y el 007 abortó antes de la sesión 2 | Sostenida (local) | E2 local | Un prompt o motivo que sí verifique |
| G2 | Con 12 ejemplos y «exactamente 2 operaciones», `luna` verifica el motivo (`double → sort_asc`) | Sostenida (local) | E2 local | Un motivo que no verifique con ese prompt |
| G3 | Con 1 ejemplo de soporte, el clon queda en 0/12 y la familia no discrimina (memoria 0/12, placebo 2/12) | Sostenida (local) | E2 local | Clon entre 20 % y 80 % |
| G4 | Con 2 ejemplos de soporte, la memoria real no supera al placebo (3/12 vs 6/12; 4 pares a favor del placebo, 1 a favor de la memoria) | Sostenida (local) | E2 local | Repetición donde la memoria supere al placebo de forma estable |
| G5 | La transferencia del procedimiento retenido no está demostrada con el modelo de experimentos | Abierta | — | 007B con una familia que tenga margen |
| G6 | Con el motivo de 4 operaciones y 2 ejemplos de soporte, la respuesta de la consulta está determinada por los ejemplos en las 12 tareas analizadas | Sostenida (local) | E2 local | Alguna tarea con más de una respuesta posible |
| G7 | Con `luna` low, el control `oracle` (programa completo) acierta ≥ 10/12: la ejecución no es el cuello | **Refutada** | E2 local | `oracle` 2/12 (réplica 3/12) |
| G8 | La memoria verificada de 2 operaciones supera al clon en ≥ 3 tareas pareadas | Sostenida (local) | E2 local | Menos de 3 pares a favor |
| G9 | La memoria verificada supera al historial de origen (mismas experiencias, sin programa explícito) | **Refutada** | E2 local | Memoria 3/12 vs historial 4/12; 1 par a favor y 2 en contra |
| G10 | La memoria verificada supera al placebo de la misma longitud | **Refutada** | E2 local | Memoria 3/12 vs placebo 6/12; 4 pares a favor del placebo y 1 de la memoria |
| G11 | `luna` low no adquiere motivos de 3 o 4 operaciones desde 12 o 24 ejemplos y la verificación los rechaza | Sostenida (local) | E2 local | Un motivo de 3–4 operaciones que verifique |

## H. Representación (LIRE-001)

> **Exploratorio.** Cifras de `gpt-6.1-terra` medium; no cuentan como evidencia.

| ID | Afirmación | Estado | Nivel | Falsador |
|---|---|---|---|---|
| L1 | La representación cambia los tokens reales de entrada | **No demostrada** | E2 local | No se aisló el coste incremental; el arnés varió entre llamadas |
| L2 | La fidelidad se conserva en las cinco representaciones | **Abierta** | E2 local | Se observó 1 error DSL y 0 en prosas sobre 8 casos; no estima la diferencia |
| L3 | El DSL conserva el acierto con menos tokens | **Abierta** | E2 local | No se demostró conjuntamente ahorro y fidelidad |
| L4 | Menos caracteres implican menos tokens | **Abierta** | E2 local | El experimento no aisló los tokens de la regla; el universal exige contraejemplo medido |

## I. Representación con skill larga (LIRE-001b)

> **Parcialmente retractada.** La tabla de 120 reglas es redundante: una fórmula la
> reconstruye; el verificador no comprueba la pertenencia del código y el orden de
> los casos no está aleatorizado. B1–B7 describen el seguimiento de esa tabla, no
> información independiente. Ver `docs/errata-lire-001b.md` y LIRE-002.

| ID | Afirmación | Estado | Nivel | Falsador |
|---|---|---|---|---|
| B1 | Con skill larga, la representación cambia los tokens de entrada (0,5–6,1 %) | Sostenida (local) | E2 local | Diferencia ≤ 500 tokens entre la más larga y la más corta |
| B2 | El chino usa menos tokens que el español (−389) y acierta más (11/12 vs 8/12) | Sostenida (local) | E2 local | Chino ≥ español o no supera el acierto |
| B3 | El español conciso usa menos tokens que el español (−1.716) | Sostenida (local) | E2 local | Conciso ≥ español |
| B4 | El DSL conserva el acierto con la skill larga | **Refutada** | E2 local | 7/12; falla cuatro `NONE` y un caso válido |
| B5 | Las prosas conservan el acierto | **Refutada parcialmente** | E2 local | Español 8/12, inglés 10/12, chino 11/12 |
| B6 | Una sola llamada estima el coste de la representación | **Refutada** | E2 local | Smoke 14,8 % vs 1,4 % con 12 casos y mínimo |
| B7 | Los fallos son de evaluación del umbral, no de búsqueda | Sostenida (local) | E2 local | Alguna respuesta devuelve un código de regla distinto del correcto |
| B8 | Las 120 reglas de LIRE-001b se reconstruyen con una fórmula: `S{código}` si importe < código | Sostenida (local) | E0 inspección | Una regla que no siga la fórmula |
| B9 | El verificador de LIRE-001b no comprueba que el código exista: `C999` devuelve `S999` | Sostenida (local) | E0 inspección | Una comprobación de pertenencia en el código |
| B10 | El orden de casos de LIRE-001b no está aleatorizado: 6 positivos y 6 negativos | Sostenida (local) | E0 inspección | Un orden aleatorio en el código |
| B11 | LIRE-001b no mide información independiente; sus diferencias no se atribuyen a retención | Sostenida (local) | E2 local | Una tabla no redundante con el mismo resultado |

## J. Información independiente (LIRE-002)

> **Ejecutado con `gpt-6-luna` low, 12 casos.** La corrida principal usa la
> instrucción que define `NONE`; el piloto sin esa instrucción se conserva como
> ablación.

| ID | Afirmación | Estado | Nivel | Falsador |
|---|---|---|---|---|
| L5 | Sin la tabla, el modelo acierta ≤ 1 de los 7 casos positivos | Sostenida (local) | E2 local | Control sin tabla ≥ 2/7 |
| L6 | Al menos una representación acierta ≥ 6/7 casos positivos con menos tokens incrementales que el español | Sostenida (local) | E2 local | Ninguna representación logra 6/7 o ninguna ahorra tokens |
| L7 | La tabla TSV normalizada usa el menor número de tokens incrementales | Sostenida (local) | E2 local | Otra representación usa menos |
| L8 | La tabla TSV o el JSON no pierden más de un caso positivo frente al español | Sostenida (local) | E2 local | Pierden ≥ 2 casos en la misma corrida |
| L9 | Las diferencias de acierto entre español, inglés y chino no se establecen con 12 casos | Sostenida (local) | E2 local | Un intervalo que excluya cero con el diseño actual |

## K. Aplicación de programas (EXEC-001)

> **Ejecutado con `gpt-6-luna` low, 12 tareas por profundidad, condición simbólica.**
> `steps` y `nl` pendientes.

| ID | Afirmación | Estado | Nivel | Falsador |
|---|---|---|---|---|
| E1 | Con el programa completo, `luna` acierta ≥ 10/12 en profundidad 2 | Sostenida (local) | E2 local | < 10/12 |
| E2 | El acierto disminuye al aumentar la profundidad nominal | **Refutada** | E2 local | Profundidad 4 (8/12) supera a 3 (7/12) |
| E3 | Pedir los estados intermedios mejora la aplicación en la profundidad de cruce | Abierta | E2 local | `steps` ≤ `symbolic` |
| E4 | La longitud mínima equivalente separa el acierto mejor que la profundidad nominal | Sostenida (local, cualitativa) | E2 local | La nominal predice mejor en una muestra mayor |

## L. Memoria en el régimen aplicable (MEM-002, piloto)

> **Pre-registrado antes del piloto.** 3 operaciones, 12 tareas, `gpt-6-luna` low.

| ID | Afirmación | Estado | Nivel | Falsador |
|---|---|---|---|---|
| M1 | La memoria **candidata** de 2 operaciones supera al clon en ≥ 3 pares | **Refutada** | E2 local | 1 par a favor, 0 en contra |
| M2 | La memoria **candidata** supera al placebo en ≥ 3 pares | **Refutada** | E2 local | 2 a favor y 4 en contra |
| M3 | La memoria **candidata** supera al historial en ≥ 3 pares | **Refutada** | E2 local | 1 a favor y 2 en contra |
| M4 | El oráculo de 3 operaciones acierta ≥ 7/12 | Sostenida (local) | E2 local | 8/12 |

> **Observación exploratoria (2 operaciones, no pre-registrada):** memoria 7/12 vs
> clon 5/12 y placebo 4/12; historial 9/12; oráculo 11/12. La memoria supera al clon
> y al placebo, pero el historial y el oráculo la superan. Motiva MEM-003; no se usa
> como confirmación.

## M. Encuadre de la memoria (MEM-003)

> **Pre-registrado antes de la corrida.** 2 operaciones, 12 tareas, `gpt-6-luna` low.

> **Alcance:** las 12 tareas son identificables desde los 2 ejemplos; el clon tiene la
> información y el artefacto entrega el programa explícito. El resultado mide
> **inferir frente a recibir**, no memoria de un hecho desconocido. MEM-004 vs clon
> p = 0,0625; los valores p no corrigen por comparaciones múltiples.

| ID | Afirmación | Estado | Nivel | Falsador |
|---|---|---|---|---|
| M5 | `memory_verified` supera a `memory_candidate` en ≥ 3 pares | Sostenida (local) | E2 local | 7 pares a favor, 0 en contra (p = 0,016) |
| M6 | `memory_verified` acierta ≥ 10/12 | Sostenida (local) | E2 local | 11/12 |
| M7 | `history` supera a `memory_candidate` en ≥ 2 pares | Sostenida (local) | E2 local | 6 pares a favor, 0 en contra (p = 0,031) |
| M8 | `memory_verified` supera al placebo en ≥ 3 pares | Sostenida (local) | E2 local | 8 pares a favor, 0 en contra (p = 0,008) |
| M9 | `oracle` acierta ≥ 10/12 | Sostenida (local) | E2 local | 12/12 |

## N. Placebo verificado y réplica (MEM-004)

> **Pre-registrado antes de la corrida.** El control crítico: un programa falso con
> el mismo encuadre definitivo que la memoria verificada.

| ID | Afirmación | Estado | Nivel | Falsador |
|---|---|---|---|---|
| M10 | `memory_verified` supera a `placebo_verified` en ≥ 3 pares | Sostenida (local) | E2 local | 10 pares a favor, 0 en contra (p = 0,002) |
| M11 | En 24 tareas, `memory_verified` acierta ≥ 20/24 | Abierta | E2 local | < 20/24 |
| M12 | En 24 tareas, `memory_verified` supera a `memory_candidate` en ≥ 6 pares | Abierta | E2 local | < 6 pares |

## O. Factorial de contenido, estado e instrucción (MEM-005)

> **Pre-registrado antes de la corrida.** 2 operaciones, 12 tareas, semilla 1,
> 10 condiciones con orden aleatorizado por tarea.

| ID | Afirmación | Estado | Nivel | Falsador |
|---|---|---|---|---|
| M13 | Con contenido correcto, estado verificado e instrucción de aplicar, el contenido correcto supera al placebo en ≥ 3 pares | Sostenida (local) | E2 local | 11 pares a favor, 0 en contra (p = 0,001) |
| M14 | Con contenido correcto e instrucción de aplicar, el estado verificado supera a la candidata en ≥ 3 pares | Sostenida (local) | E2 local | 3 pares a favor, 0 en contra (p = 0,25; direccional, no significativo) |
| M15 | Con contenido correcto y estado verificado, la instrucción de aplicar supera a la de verificar en ≥ 3 pares | Sostenida (local) | E2 local | 4 pares a favor, 0 en contra (p = 0,125; direccional, no significativo) |
| M16 | El programa escrito por un programador queda a ≤ 2 pares del programa aprendido verificado | Sostenida (local) | E2 local | 12/12 vs 12/12; cero pares discordantes; la adquisición no añade nada en esta tarea |
| M17 | La condición correcta+verificada+aplicar acierta ≥ 9/12 en la semilla 1 | Sostenida (local) | E2 local | 12/12 |

> **Lectura:** el efecto grande solo aparece en la celda verificado+aplicar
> (12 vs 1). El programa escrito por un programador rinde igual que el aprendido
> (12/12 vs 12/12), pero el control cambia procedencia y orden: **no hay evidencia de
> ventaja de adquisición en esta tarea**, no una prueba de que la procedencia sea
> irrelevante. La interacción triple es 0,50 con bootstrap 95 % [−0,17, 1,17], que
> incluye cero; el resultado bien respaldado es verificado+aplicar frente a su
> placebo. La formulación defendible es «entregar el procedimiento correcto como
> instrucción autoritativa mejora la ejecución local en una transformación
> identificable», no «la memoria acumulativa funciona».
>
> **Límites metodológicos:** protocolo, código, resultados y análisis entraron en el
> mismo commit (exploratorio, no pre-registro independiente); no se guardaron tokens
> por condición; la instrucción de verificar sugiere completitud que con `suffix=0` no
> existe.

---

## Lo que este registro dice del proyecto

- **65 sostenidas**: 60 propias (casi todas E2 locales) y 5 declaradas por terceros,
  no replicadas.
- **18 refutadas**, incluidas nuestras dos hipótesis principales, tres de LIRE y las
  tres hipótesis de memoria en 3 operaciones.
- **17 abiertas, inválidas o no demostradas**, y son justo las que responderían la
  pregunta del proyecto.
- **0 en E3, E4 o E5 propias.**
- **0 competidores reproducidos.**

El patrón es claro: somos buenos refutando nuestros propios mecanismos y malos
construyendo evidencia acumulativa. La causa está en `docs/teoria.md`: seis
prototipos en el mismo régimen enumerable, donde la teoría predice que no puede
haber expansión. La revisión de antecedentes confirma que el campo ya pasó por
donde nosotros estamos: bibliotecas con aplicabilidad y terminación, verificación
por ejecución, benchmarks de transferencia y resultados negativos a escala.

## Regla de mantenimiento

1. Toda afirmación nueva entra aquí **antes** del experimento, con su falsador.
2. Un resultado negativo cambia el estado; no se borra la fila.
3. Un cambio de estado exige enlace al resultado crudo.
4. Las filas `inválida` se conservan: son lecciones metodológicas.




