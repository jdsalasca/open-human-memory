# Prototipo 002 — Diagnóstico sin filtración y con composición

**Fecha:** 15 de noviembre de 2026  
**Estado:** prototipo sintético corregido. Sustituye al Prototipo 001 como
evidencia del instrumento.  
**Código:** `src/ohmem/v2_tasks.py`, `v2_conditions.py`, `v2_experiment.py`  
**Tests:** `tests/test_v2.py`  
**Resultados:** `results/seed-0.json`, `seed-1.json`, `seed-2.json`,
`summary.json`.

## 1. Qué corrige del Prototipo 001

El 001 tenía **target leakage**: el nombre de la regla (`sort_asc`, `double`,
etc.) aparecía literalmente en `surface`, la entrada que veía el predictor.
Además, `Task` exponía `rule` y `expected`, y el oráculo usaba `query.rule`.

El 002 separa estrictamente:

- `Observation`: familia, superficie sin nombre de regla, tres ejemplos
  input→output y la consulta.
- `Solution`: la regla oculta, accesible solo al evaluador y al oráculo.
- El agente debe **inferir** la regla a partir de los ejemplos.

Pruebas de fuga en `tests/test_v2.py`:

- `test_surface_has_no_rule_names`
- `test_observation_has_no_solution`
- `test_support_examples_match_solution`

## 2. Diseño

| Condición | Qué hace |
|---|---|
| **MEM-A** sin memoria | Aplica una primitiva por defecto |
| **MEM-B** retrieval | Recupera la tarea más parecida y usa su regla |
| **MEM-C** oráculo | Usa la regla oculta de la tarea (techo) |
| **MEM-D** procedimiento | Infiere una **primitiva** de los ejemplos |
| **MEM-E** abstracción composicional | Busca la **composición** de primitivas que explica los ejemplos |

Distribuciones:

- **D1:** instancias nuevas de familias vistas.
- **D2:** familia nueva, mismas primitivas.
- **D3:** composición nueva de primitivas vistas (`sort_asc` → `double`), no
  presente en entrenamiento.

## 3. Resultados

Media de tres semillas (0, 1, 2); 200 tareas de entrenamiento, 50 de evaluación.

| Condición | D1 | D2 | D3 |
|---|---|---|---|
| MEM-A sin memoria | 0.240 | 0.507 | 0.000 |
| **MEM-A0 solucionador actual** | **1.000** | **1.000** | **1.000** |
| MEM-B retrieval | 0.553 | 0.513 | 0.027 |
| MEM-C oráculo | 1.000 | 1.000 | 1.000 |
| MEM-D primitiva | 1.000 | 1.000 | 0.000 |
| MEM-E composición | 1.000 | 1.000 | 1.000 |

### Coste observado (por tarea)

| Condición | memory reads | verificaciones | valores de contexto |
|---|---|---|---|
| MEM-A | 0 | 0 | 0 |
| MEM-B | 1 | 0 | 24 |
| MEM-C | 1 | 1 | 12 |
| MEM-D | 0 | 4 | 12 |
| MEM-E | 0 | 20 | 12 |

Es un **vector de coste**, no un escalar: MEM-E acierta D3 pero gasta 20
verificaciones por tarea; MEM-D gasta 4 y falla D3. El oráculo MEM-C gasta 1
porque hace trampa.

### Curva longitudinal \(G(n)\)

Con \(n = 50, 100, 200, 400\) experiencias, la ganancia de MEM-E sobre MEM-A en
D3 es 1.000 desde el primer corte; MEM-D se queda en 0.000. La curva **no
crece** porque las tareas son i.i.d. y el espacio de hipótesis ya contiene la
composición. Lo que sí aparece es **transferencia negativa**: MEM-B en D2 tiene
\(G(50) = -0.180\), porque recupera una tarea de familia parecida con regla
distinta. Resultados en `results/longitudinal-seed-*.json`.

## 4. Lectura (corregida por la auditoría)

- **MEM-A0 es la línea base decisiva.** Usa el mismo solucionador composicional
  que MEM-E, con los mismos ejemplos actuales, pero **sin historial**. Empata con
  MEM-E en D1, D2 y D3 (1.000). Por tanto, el 100% de MEM-E **no demuestra
  aprendizaje desde la memoria**: demuestra que un solucionador con composición
  en su espacio de hipótesis resuelve D3.
- **Retrieval no basta** cuando la regla está en los ejemplos y no en la
  superficie.
- **Una primitiva inducida** resuelve reglas simples.
- **La composición es el discriminador** entre MEM-D y MEM-E, pero es una
  diferencia de expresividad del solucionador, no de memoria.
- **El oráculo confirma el techo.**

Conclusión honesta: el 002 es un **benchmark de solucionador**, útil para
verificar que el instrumento separa recuperación, primitiva y composición. **No
es evidencia de aprendizaje acumulativo.** Esa prueba es el Prototipo 003, donde
las macros se aprenden de la experiencia y la ablación las elimina.

## 5. Qué NO prueba

- No usa un LLM.
- **No demuestra aprendizaje desde la memoria:** MEM-E no usa el historial; MEM-A0
  (mismo solucionador sin historial) empata con MEM-E.
- No mide descubrimiento conceptual abierto: las primitivas y composiciones están
  predefinidas en el espacio de búsqueda.
- No mide costo real de consolidación, verificación o entrenamiento.
- No mide aprendizaje longitudinal \(G(n)\) con crecimiento real: la curva se
  satura desde \(n=50\) porque las tareas son i.i.d. y el espacio de hipótesis ya
  contiene la composición. Mide transferencia composicional, no acumulación.
- No prueba que MEM-E sea una arquitectura; es un **inductor composicional
  mínimo**.
- El éxito de MEM-E está garantizado por construcción si los ejemplos
  identifican la composición; mide el valor de incluir composiciones en el
  espacio de hipótesis, no la dificultad de descubrirlas desde cero.

## 6. Reproducir

```bash
python resources/investigation/prototipo-002-diagnostico/reproduce.py
PYTHONPATH=src python -m unittest discover -s tests -v
```

En PowerShell:

```powershell
$env:PYTHONPATH="src"
python -m unittest discover -s tests -v
python resources/investigation/prototipo-002-diagnostico/reproduce.py
```

Python 3.13.15, sin dependencias externas.

## 7. Archivos

```
prototipo-002-diagnostico/
├── README.md
├── reproduce.py
└── results/
    ├── seed-0.json
    ├── seed-1.json
    ├── seed-2.json
    ├── summary.json
    ├── longitudinal-seed-0.json
    ├── longitudinal-seed-1.json
    └── longitudinal-seed-2.json
```

## 8. Siguiente paso

Prototipo 003: sustituir las primitivas sintéticas por un agente LLM y tareas con
estructura latente, medir \(G(n)\) y separar reconocimiento, recuperación,
procedimiento y composición. Antes de eso, no se justifica JANUS-C ni otra capa.
