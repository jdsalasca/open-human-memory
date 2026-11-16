# Prototipo 004-A — Auditoría de validez del aprendizaje de macros

**Fecha:** 16 de noviembre de 2026
**Estado:** resultado **negativo** para la hipótesis fuerte del 003.
**Protocolo congelado:** `protocolo-congelado.md` (SHA-256 en
`results/protocolo.sha256`, verificado por `reproduce.py` antes de medir).
**Código:** `src/ohmem/v4_experiment.py` sobre `v3_solver.py`, `v3_library.py`,
`v3_tasks.py`.
**Tests:** `tests/test_v4.py` (10 tests negativos).

## 1. La pregunta

El Prototipo 003 afirmó que la experiencia producía una capacidad nueva: resolver
programas de profundidad 3 con un solucionador limitado a profundidad 2. La
auditoría mostró que esa capacidad desaparece si se permite buscar profundidad 3.

El 004-A no añade mecanismos. Añade los **ocho controles** que la auditoría exigió
y mide si queda algún efecto atribuible al aprendizaje.

## 2. Condiciones (mismo solucionador, mismos ejemplos, mismo lenguaje)

| ID | Biblioteca | Profundidad | Historial |
|---|---|---|---|
| `A0-nolearn-d2` | 4 primitivas | 2 | No |
| `A1-nolearn-d3` | 4 primitivas | 3 | No |
| `A2-random-same-lang-d2` | 4 primitivas + 3 macros del **mismo lenguaje**, elegidas al azar | 2 | No |
| `A3-learned-d2` | 4 primitivas + macros aprendidas | 2 | Sí |
| `A4-learned-d3` | 4 primitivas + macros aprendidas | 3 | Sí |

Evaluación: **las 64 combinaciones** de tres primitivas (`DEPTH3_GRID`), una
instancia por programa. Ya no tres programas elegidos. Media de 3 semillas.

## 3. Resultado principal

| Condición | Aciertos /64 | Candidatos | Ops primitivas | Tareas con macro | Candidatos por acierto |
|---|---|---|---|---|---|
| A0 sin memoria, prof. 2 | **33 (51,6 %)** | 876 | 4.548 | 0 | 26,6 |
| A1 sin memoria, prof. 3 | **64 (100 %)** | 1.761 | 12.513 | 0 | 27,5 |
| A2 azar, mismo lenguaje, prof. 2 | 50,7 (79,3 %) | 1.543 | 10.848 | 25,7 | 30,5 |
| A3 macros aprendidas, prof. 2 | **54 (84,4 %)** | 1.448 | 10.023 | 33 | 26,8 |
| A4 macros aprendidas, prof. 3 | **64 (100 %)** | 2.247 | 18.951 | 33 | 35,1 |

**D1 se cumple.** `A1-nolearn-d3` (100 %) ≥ `A3-learned-d2` (84,4 %). Sin
historial, con búsqueda de tres pasos y el mismo solucionador, se resuelve **todo**
el problema. La afirmación del 003 —«la experiencia produce una capacidad que no
existía»— **queda retirada**.

**D7 se cumple.** La biblioteca aprendida resuelve 54/64: es una **compilación con
pérdida**. Diez programas de la rejilla no son expresables con sus tres macros y
no se recuperan a menos que se permita buscar más profundo.

## 4. Por qué el 003 veía 0 %

En la rejilla completa, `A0-nolearn-d2` resuelve **33/64 sin ninguna memoria**, no
0. La razón es equivalencia observacional: `sort_asc` dos veces es `sort_asc` una
vez; `sort_desc→sort_asc` es `sort_asc`. Muchos programas de profundidad 3 son
funcionalmente idénticos a uno de profundidad 2 sobre los tres ejemplos de soporte.

Los tres programas del 003 estaban elegidos entre los 31 que **no** tienen esa
equivalencia. El 0 % del 003 era, en parte, una propiedad de la selección.

## 5. El control `RANDOM` estaba amañado, y el nuevo control lo demuestra

Barrido exhaustivo de las **560 bibliotecas** de 3 macros sobre los 16 pares del
generador, sin usar el historial:

| Conjunto de evaluación | Acierto medio | Perfectas |
|---|---|---|
| Rejilla completa de 64 programas | **77,3 %** (mediana 78,1 %, máx. 93,8 %) | **0 / 560** |
| Los 3 programas del 003 (30 tareas) | **70,5 %** | **250 / 560** |

Dos lecturas:

1. **Reproducimos exactamente el 70,5 % y 250/560 de la auditoría**, con el mismo
   código y la misma definición de tarea. La auditoría tenía razón.
2. En la rejilla completa **ninguna** biblioteca arbitraria es perfecta, pero
   **124/560 (22 %)** igualan o superan el 84,4 % de la biblioteca aprendida, y el
   máximo (93,8 %) la supera con claridad.

El criterio de aprendizaje —contar pares frecuentes— **no selecciona nada
especial**. El 003 comparó contra macros de `reverse`/`negate`, que ni siquiera
pertenecen al lenguaje del generador. El control válido es el barrido, y deja a la
biblioteca aprendida en la media alta de una distribución, no por encima.

## 6. La única ganancia real: presupuesto bajo

Comparación a **igual número de candidatos por tarea**:

| Presupuesto | A3 aprendida, prof. 2 | A1 sin memoria, prof. 3 |
|---|---|---|
| 20 | **54,7 %** | 51,6 % |
| 40 | **78,1 %** | 70,3 % |
| 60 | 84,4 % | **89,1 %** |
| 80 | 84,4 % | **96,9 %** |
| 84 | 84,4 % | **100 %** |

El cruce está entre 40 y 60 candidatos. Con presupuesto muy bajo, la biblioteca
aprendida es un **prior útil**: encuentra soluciones antes. Desde 60 candidatos, la
búsqueda profunda la domina y termina resolviendo todo.

Y si se permite profundidad 3, la biblioteca **encarece** la búsqueda: 2.247
candidatos frente a 1.761 (**+27,6 %**), porque añade ramas sin añadir cobertura.
Es el efecto que la auditoría predijo: la biblioteca puede destruir su propia
ventaja.

Por acierto, la comparación es un empate: 26,8 candidatos (A3) frente a 27,5 (A1),
con 10 aciertos menos. El ahorro del 37 % que calculó la auditoría correspondía a
sus 30 programas elegidos; en la rejilla completa el ahorro es **17,8 % de
candidatos** y **2,6 % por acierto**. No es el mismo denominador y no conviene
mezclarlos.

## 7. La curva de adquisición se satura en 6 experiencias

| Experiencias | Macros | Aciertos /64 |
|---|---|---|
| 0–3 | 0 | 51,6 % |
| 4 | 1 | 65,6 % |
| 5 | 2 | 79,7 % |
| 6 | 3 | 84,4 % |
| 8–60 | 3 | 84,4 % |

**D5 se cumple.** Las 54 experiencias restantes no aportan nada. No hay aprendizaje
acumulativo: hay adquisición de tres macros en un universo cerrado y saturación
inmediata. Las tres semillas repiten la misma estructura, así que no son tres
pruebas independientes de generalización.

Coste compartido del entrenamiento: 760 candidatos (coincide con la reproducción
de la auditoría). Ese coste lo pagan ambas arquitecturas, porque las tareas hay que
resolverlas igual; el coste **incremental** de la biblioteca es el factor de
ramificación: de 4 a 7 operaciones, el espacio de profundidad 2 pasa de 20 a 56
candidatos por tarea.

## 8. Reglas de decisión congeladas, todas aplicadas

| ID | Regla | Resultado |
|---|---|---|
| D1 | `acc(A1) >= acc(A3)` → retirar «capacidad nueva» | **Se cumple** |
| D2 | Déficit de cobertura | **15,6 pp** |
| D3 | Ahorro de candidatos | **17,8 %** |
| D4 | `perfectas/560 > 0,05` → control `RANDOM` inválido | **Se cumple (250/560)** |
| D5 | Saturación en `n <= 6` → sin aprendizaje acumulativo | **n = 6** |
| D6 | A igual presupuesto, gana la búsqueda profunda | **Sí, desde 60** |
| D7 | A3 falla tareas que A1 resuelve → compilación con pérdida | **10 tareas** |
| D8 | La biblioteca encarece la búsqueda en profundidad 3 | **+27,6 %** |

## 9. Qué queda en pie

Una frase, más pequeña y defendible:

> Aprender tres macros de dos pasos a partir de la experiencia reduce un 17,8 % los
> candidatos examinados en una rejilla de 64 programas de profundidad 3, a cambio
> de un 15,6 % menos de cobertura. Con presupuesto ≤ 40 candidatos por tarea, esa
> biblioteca resuelve más problemas que la búsqueda profunda; con presupuesto ≥ 60,
> la búsqueda profunda la supera.

Y una hipótesis para el 005, no un resultado:

> Las abstracciones compiladas pueden funcionar como **prior barato** cuando el
> cómputo por decisión está acotado, no como ampliación de capacidad.

## 10. Qué NO prueba el 004

- No implementa DreamCoder, Stitch ni LILO. Los cita como antecedentes y como
  comparación pendiente, no como línea base ejecutada.
- No hay tareas adversariales (ruido, ambigüedad, deriva, macros perjudiciales).
  `harmful_macro_tasks = 0` significa que, en este universo, una macro incorrecta
  nunca produjo una respuesta incorrecta: el solucionador solo acepta programas
  compatibles con los tres ejemplos. Ese cero es una propiedad del generador, no
  una virtud del mecanismo.
- No hay actualización online durante la evaluación (Experimento C).
- No hay LLM ni transferencia entre modelos.
- El barrido de 560 bibliotecas cubre solo el lenguaje del generador. Fuera de él,
  la conclusión no se extiende.

## 11. Reproducir

```bash
python resources/investigation/prototipo-004-validez/reproduce.py
PYTHONPATH=src python -m unittest discover -s tests -v
```

`reproduce.py` verifica el SHA-256 del protocolo y aborta si cambió. Python 3.13,
sin dependencias externas. Tiempo: ~6 s para las 3 semillas.

## 12. Archivos

```
prototipo-004-validez/
├── README.md
├── protocolo-congelado.md
├── reproduce.py
└── results/
    ├── protocolo.sha256
    ├── seed-0.json
    ├── seed-1.json
    ├── seed-2.json
    └── summary.json
```
