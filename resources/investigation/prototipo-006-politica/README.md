# Prototipo 006-A — Política de activación: aprende a cambiar, pero no paga su instrumento

**Fecha:** 16 de noviembre de 2026
**Estado:** **confirmatorio parcial**. Protocolo, código y datos congelados con
SHA-256 antes de ejecutar las semillas 1 y 2 (`results/frozen.sha256`). La semilla
0 se usó para desarrollar el diseño y no se reporta.
**Código:** `src/ohmem/v6_policy.py` sobre `v3_solver.py`.
**Tests:** `tests/test_v6.py`.
**Resultados:** `results/seed-{1,2}.json`, `results/summary.json`,
`results/probe-cost.json`.

## 1. La pregunta

El 005-A dejó abierto lo único que importaba: si se guarda un artefacto acotado,
**¿quién decide cuándo confiar en él?** Mi heurística de desalojo falló. Este
prototipo prueba una política aprendida.

Decisión binaria por tarea: **usar la biblioteca** (profundidad 2, macros primero)
o **buscar desde cero** (profundidad 3, sin biblioteca). Presupuesto: 120 pasos
primitivos ejecutados.

## 2. El instrumento

La biblioteca se aprende una vez de la familia A y **se congela** (3 macros).

La política solo ve tres números antes de decidir:

1. sesgo;
2. **probe de aplicabilidad**: ¿alguna macro, combinada con una primitiva antes o
   después, reproduce los tres ejemplos? Centrado a −1/+1;
3. éxito reciente de la memoria.

Aprendizaje: puntuador lineal, ε-greedy (ε=1,0 la primera época, luego decae), 20
épocas. Control: `policy-blind`, idéntica con el probe forzado a cero.

## 3. Resultados (semillas 1–2, 48 tareas)

| Condición | Similar | Novel | **Mixto** | Pasos (mixto) |
|---|---|---|---|---|
| Sin memoria, profundidad 3 | 81,3 % | 85,4 % | 83,3 % | 59,6 |
| Memoria, primitivas primero | 91,7 % | 81,3 % | 86,5 % | 51,1 |
| Memoria, macros primero | 100 % | 81,3 % | 90,6 % | 44,5 |
| Acción aleatoria | 100 % | 83,3 % | 89,6 % | 45,1 |
| **Política aprendida (probe)** | **100 %** | **87,5 %** | **93,8 %** | **42,3** |
| Regla del probe escrita a mano | 91,7 % | 87,5 % | 89,6 % | 49,5 |
| **Política ciega (control)** | 100 % | **81,3 %** | 90,6 % | 44,5 |
| Oráculo por tarea | 100 % | 87,5 % | 93,8 % | 34,8 |

Las cuatro predicciones congeladas se cumplieron:

| ID | Predicción | Resultado |
|---|---|---|
| P1 | Política ≥ mejor acción fija en mixto | **+3,1 pp** sobre macros-primero, **+10,4 pp** sobre buscar |
| P2 | En novel, ≥ memoria + 5 pp | **+6,25 pp** (87,5 vs 81,3) |
| P3 | La ciega rinde menos | **+3,1 pp** (una tarea y media) |
| P4 | Menos pasos que buscar en similar | **43,0 vs 71,9** |

La política **iguala al oráculo** en el conjunto mixto. Aprende a usar la
biblioteca cuando el probe dice que aplica y a buscar cuando no.

## 4. El problema: el probe cuesta más de lo que ahorra

El protocolo congelado contó solo pasos de búsqueda. El probe también ejecuta
primitivas. Medido aparte, sin tocar el código congelado
(`probe_cost.py`, cota superior con cortocircuito):

| Conjunto | Coste medio del probe |
|---|---|
| Similar | **96,0 pasos/tarea** |
| Novel | **122,4 pasos/tarea** |

Comparación honesta por tarea en `similar`:

- buscar sin memoria: 71,9 pasos;
- política: 43,0 pasos de búsqueda **+ 96 de probe = 139,0**;
- ahorro aparente: 28,9; **coste neto: +67,1 pasos**.

En el conjunto mixto el coste neto ronda **+92 pasos por tarea**. La política es
la mejor en el contador de búsqueda y la peor en cómputo total.

**Conclusión:** el mecanismo funciona y la economía no. Una política que decide
con un probe caro pierde contra no decidir. Para que pague, el probe tiene que ser
barato: cacheado por firma, calculado una vez por familia o sustituido por un
índice. Eso es un requisito de ingeniería concreto, no una nota al pie.

## 5. Qué prueba y qué no

**Prueba** que una política lineal sobre una señal de aplicabilidad aprende a
cambiar de estrategia y domina a cada acción fija en acierto, con predicciones
fijadas antes de las semillas de evaluación.

**No prueba** que la política sea económica (§4), ni que la señal se pueda
descubrir sola (el probe es diseño humano), ni que escale: 48 tareas, una familia,
dos semillas. La ventaja sobre la mejor acción fija es de **una tarea y media**;
tratar eso como un triunfo sería el error que la auditoría viene señalando.

## 6. Reproducir

```bash
python resources/investigation/prototipo-006-politica/reproduce.py
python resources/investigation/prototipo-006-politica/probe_cost.py
PYTHONPATH=src python -m unittest discover -s tests -v
```

`reproduce.py` verifica los hashes de protocolo, código y datos y aborta si algo
cambió. Para re-congelar (no hacerlo tras ver resultados):
`reproduce.py --freeze`.
