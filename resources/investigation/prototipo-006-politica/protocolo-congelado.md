# Protocolo del Prototipo 006 — Política de activación

**Congelado:** 16 de noviembre de 2026, **antes** de ejecutar las semillas 1 y 2.
La semilla 0 se usó para desarrollar el diseño y **no cuenta** como confirmación.

## 1. Pregunta

¿Puede una política aprendida decidir, tarea a tarea, si conviene usar la
biblioteca o buscar desde cero?

## 2. Diseño congelado

- Biblioteca aprendida de la familia A (profundidad 2, frecuencia ≥ 2) y
  **congelada**: 3 macros.
- Tres acciones: `memory` (profundidad 2), `memory_first` (profundidad 2, macros
  primero), `search` (profundidad 3, **sin biblioteca**).
- Presupuesto: 120 pasos primitivos ejecutados por tarea.
- Features: sesgo, **probe de aplicabilidad centrado** (−1 si ninguna macro encaja
  como prefijo o sufijo con una primitiva, +1 si alguna encaja) y éxito reciente
  de la memoria.
- Aprendizaje: puntuador lineal, ε-greedy con ε=1,0 la primera época y decaimiento
  hasta 0,03; 20 épocas sobre 32 tareas mezcladas.
- Control: `policy-blind`, idéntica pero con el probe forzado a cero.
- Conjuntos: `similar` (24 tareas de la familia A, instancias nuevas), `novel` (24
  tareas sin ningún par de la biblioteca como adyacente), `mixed` (48).
- Semillas de evaluación: **1 y 2**. Semilla 0: desarrollo.

## 3. Hipótesis y reglas de decisión

| ID | Predicción | Se refuta si |
|---|---|---|
| **P1 — cambio** | En `mixed`, `learned-policy` ≥ mejor acción fija en acierto | la política empata con una acción fija |
| **P2 — señal** | En `novel`, `learned-policy` ≥ `memory` + 5 pp | no recupera nada al buscar |
| **P3 — control** | `policy-blind` < `policy-applicability` en `mixed` | el probe no aporta |
| **P4 — costo** | En `similar`, `learned-policy` usa menos pasos que `search` | usa más o igual |

## 4. Cláusula de congelamiento

Se congelan: el código de `v6_policy.py`, `v3_solver.py`, `v3_library.py`,
`v3_tasks.py`, `v4_experiment.py`, este protocolo y la huella de datos de las
semillas 1 y 2. `reproduce.py` verifica los hashes y aborta si algo cambió.

Cualquier mejora posterior va al Prototipo 007. No se reejecuta esta evaluación
con cambios.

Huellas: `results/frozen.sha256`.
