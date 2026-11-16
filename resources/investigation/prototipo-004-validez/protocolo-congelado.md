# Protocolo confirmatorio — Prototipo 004-A

**Congelado:** 16 de noviembre de 2026, antes de ejecutar la evaluación principal.
**Origen:** auditoría externa del Prototipo 003 (commit `eff641e`).
**Código bajo prueba:** `src/ohmem/v4_experiment.py`, sobre `v3_solver.py`,
`v3_library.py`, `v3_tasks.py`.

## 1. Qué se pone a prueba

El Prototipo 003 afirmó que la experiencia produce una capacidad nueva: resolver
programas de profundidad 3 sin poder buscarlos. La auditoría mostró que la
capacidad desaparece si se permite buscar profundidad 3. Este protocolo mide si
queda **algún** efecto atribuible al aprendizaje de macros.

**Hipótesis nula (H0).** La biblioteca de macros no aporta nada que un
solucionador idéntico sin historial y con búsqueda más profunda no consiga.

**Hipótesis alternativa (H1).** La biblioteca reduce el cómputo necesario para
un rendimiento comparable, aunque no amplíe la cobertura.

## 2. Condiciones (mismo solucionador, mismos ejemplos, misma biblioteca inicial)

| ID | Biblioteca | Profundidad |
|---|---|---|
| `A0-nolearn-d2` | 4 primitivas | 2 |
| `A1-nolearn-d3` | 4 primitivas | 3 |
| `A2-random-same-lang-d2` | 4 primitivas + 3 macros del mismo lenguaje, sin historial | 2 |
| `A3-learned-d2` | 4 primitivas + macros aprendidas | 2 |
| `A4-learned-d3` | 4 primitivas + macros aprendidas | 3 |

`A2` es el control que faltaba: mismo tamaño, mismo lenguaje de 16 pares, misma
profundidad, cero información del historial.

## 3. Tareas

- Entrenamiento: 60 tareas con tres programas de dos pasos.
- Evaluación: **las 64 combinaciones** de tres primitivas (`DEPTH3_GRID`), una
  instancia por programa, familia `delta`. Ya no tres programas elegidos.
- Semillas: 0, 1, 2.

## 4. Métricas

- `accuracy` = aciertos / 64.
- `candidates` = programas examinados por el solucionador.
- `primitive_ops` = aplicaciones primitivas **× ejemplos de soporte** (la
  auditoría señaló que el contador anterior subestimaba).
- `macro_tasks` = tareas resueltas usando al menos una macro.
- `harmful_macro_tasks` = tareas con respuesta incorrecta y macro usada.
- `abstained` = tareas sin programa compatible.
- `sweep` = las 560 bibliotecas de 3 macros sobre los 16 pares del generador.

## 5. Reglas de decisión (fijadas de antemano)

| ID | Condición observada | Decisión |
|---|---|---|
| **D1** | `accuracy(A1) >= accuracy(A3)` | Se retira la afirmación «las macros amplían la capacidad». El 003 pasa a resultado negativo. |
| **D2** | `accuracy(A3) < accuracy(A1)` | Se reporta el déficit de cobertura como coste de compilar. |
| **D3** | `candidates(A3) < candidates(A1)` | Se permite afirmar ahorro de búsqueda, con el porcentaje medido. |
| **D4** | `sweep.perfect / 560 > 0.05` | El control `RANDOM` del 003 queda invalidado; la línea base honesta es el barrido. |
| **D5** | `accuracy` saturada en `n_train <= 6` | No hay aprendizaje acumulativo; 60 experiencias son redundantes. |
| **D6** | Con presupuesto igual por tarea, `accuracy(A1) >= accuracy(A3)` | La búsqueda profunda domina en costo equivalente. |
| **D7** | `A3` falla tareas que `A1` resuelve | La biblioteca es una compilación con pérdida; CUMULUS no puede citarla como expansión. |

## 6. Cláusula de congelamiento

El código de evaluación, la rejilla de 64 tareas, las condiciones, las métricas,
las semillas y los umbrales de la sección 5 quedan fijos en este commit. Cualquier
mejora exploratoria posterior va en `prototipo-005` y **no puede sustituir** esta
evaluación. Si un resultado contradice la hipótesis, se publica tal cual.

Huella del protocolo: `results/protocolo.sha256`.
