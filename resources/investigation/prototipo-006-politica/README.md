# Prototipo 006-A — Política de activación (retirada y corregida)

**Fecha:** 16 de noviembre de 2026
**Estado:** la versión congelada **queda retirada**. La auditoría de dirección
encontró cinco fallos de implementación; corregidos, el resultado es **negativo**.
Este documento es el vigente.
**Código:** `src/ohmem/v6_policy.py`.
**Resultados corregidos:** `results/corrected/seed-{1,2}.json`,
`results/corrected/summary.json`.
**Resultado congelado (histórico):** `results/` — se conserva como archivo, y
`reproduce.py` se niega a reejecutarlo con el código nuevo, a propósito.

## 1. Los cinco fallos que la auditoría encontró

| # | Fallo | Efecto |
|---|---|---|
| 1 | `random-action` usaba `explore=True`, que explora con ε≈0,03 | No era aleatoria: usaba la política entrenada el 97 % del tiempo |
| 2 | El estado de éxitos recientes se limpiaba antes de una condición pero no de la siguiente | Contaminación entre condiciones |
| 3 | `probe-rule` elegía `memory_first` pero resolvía sin `macro_first` | La regla manual competía en desventaja |
| 4 | El conjunto mixto concatenaba similar y luego novel | No probaba intercalado impredecible |
| 5 | `probe_cost.py` calculaba una cota superior | Se presentó como medición |

Además, el coste del probe no se contabilizaba en el presupuesto de la política.

## 2. Correcciones

- `probe` devuelve el valor **y** las aplicaciones primitivas ejecutadas de verdad,
  con cortocircuito dentro de cada comprobación.
- `uniform-random` (uniforme sobre las dos acciones) y `shuffled-policy` (mismas
  frecuencias que la política, asignadas ignorando la tarea) sustituyen al falso
  aleatorio.
- Cada condición reinicia el estado de evaluación.
- `probe-rule` aplica `macro_first` cuando elige memoria.
- El conjunto mixto intercala similar y novel.
- Todas las condiciones devuelven resultados por tarea; las comparaciones son
  pareadas con bootstrap sobre tareas.

## 3. Resultado corregido (semillas 1–2, 48 tareas por conjunto)

| Condición | Mixto | Búsqueda | Probe | **Total** |
|---|---|---|---|---|
| Buscar sin memoria | 83,3 % | 59,5 | — | **59,5** |
| Memoria, primitivas primero | 86,5 % | 51,1 | — | **51,1** |
| Memoria, macros primero | 90,6 % | 44,5 | — | **44,5** |
| Aleatoria uniforme | 85,4 % | 56,9 | — | **56,9** |
| Barajada (mismas frecuencias) | 87,5 % | 49,4 | — | **49,4** |
| **Regla del probe (una línea)** | **93,8 %** | 42,2 | 41,2 | **83,5** |
| **Política aprendida** | 92,7 % | 43,1 | 41,2 | **84,3** |
| Política ciega (paga el probe y lo ignora) | 90,6 % | 44,5 | 41,2 | **85,7** |
| Oráculo por tarea | 93,8 % | 34,5 | — | **34,5** |

Diferencias pareadas (bootstrap sobre 96 tareas, IC 95 %):

| Comparación | Diferencia | IC |
|---|---|---|
| Política vs macros primero | +2,1 pp | 0,0 a +5,2 |
| Política vs buscar | **+9,4 pp** | +3,1 a +15,6 |
| Política vs regla del probe | **−1,0 pp** | −3,1 a 0,0 |
| Política vs barajada | +5,2 pp | +1,0 a +9,4 |

## 4. Lectura

1. **La política no supera a una regla de una línea.** Pierde 1,0 pp, y el
   intervalo no cruza el cero a su favor. El aprendiz no aporta sobre el criterio
   que ya conocemos.
2. **La señal de aplicabilidad sí contiene información**: +5,2 pp sobre el control
   barajado, que conserva las mismas frecuencias de acción pero ignora la tarea.
   Es el único efecto que sobrevive a los controles.
3. **La economía es negativa.** El probe cuesta 41,2 pasos por tarea y el ahorro
   frente a buscar es de 29. Con el probe contabilizado, la política total cuesta
   **1,42× la búsqueda sin memoria** (84,3 vs 59,5) y **1,89× macros primero**
    (84,3 vs 44,5). Además, el presupuesto no descuenta el probe durante la
    búsqueda: la comparación es de coste ex post, no de presupuesto total igual.
    El exceso de pasos del solucionador es de 0 a 6 por tarea
    (`results/budget-overshoot.json`).
4. **La versión congelada estaba inflada por sus propios controles defectuosos.**
   El 93,8 % frente a 90,6 % de la corrida congelada no resiste la corrección.

Conclusión: **no hay evidencia de que una política aprendida de activación aporte
ventaja.** Se retira la afirmación.

## 5. Qué sobrevive

- El probe de aplicabilidad es una señal real (efecto +5,2 pp sobre el control
  barajado), pero demasiado cara tal como está implementada.
- La comparación pareada con IC es el estándar desde ahora.
- El diseño de acciones (memoria vs búsqueda) es correcto; lo que falla es el
  aprendiz y la economía.

## 6. Reproducir

```bash
# Resultado vigente (corregido)
python resources/investigation/prototipo-006-politica/reproduce_corrected.py

# Resultado congelado (histórico): el script verifica hashes y aborta con el código nuevo
python resources/investigation/prototipo-006-politica/reproduce.py
```
