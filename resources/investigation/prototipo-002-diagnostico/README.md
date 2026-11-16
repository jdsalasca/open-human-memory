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
| MEM-B retrieval | 0.553 | 0.513 | 0.027 |
| MEM-C oráculo | 1.000 | 1.000 | 1.000 |
| MEM-D primitiva | 1.000 | 1.000 | 0.000 |
| MEM-E composición | 1.000 | 1.000 | 1.000 |

## 4. Lectura

- **Retrieval no basta.** MEM-B queda cerca del azar en D1/D2 (0.55/0.51)
  porque la superficie no identifica la regla; la información está en los
  ejemplos, no en la familia.
- **Una primitiva inducida resuelve D1/D2.** MEM-D llega al techo cuando la
  regla es una sola operación vista.
- **La composición es el discriminador.** MEM-D falla D3 (0.00) porque su espacio
  de hipótesis no incluye composiciones; MEM-E acierta (1.00) porque las busca.
- **El oráculo confirma el techo.** MEM-C acierta todo, incluida la composición.

Esto sí es un diagnóstico de **transferencia composicional**, no de
reconocimiento de etiquetas. Lo que muestra es que el espacio de hipótesis
importa: sin composición, no hay transferencia a una composición nueva.

## 5. Qué NO prueba

- No usa un LLM.
- No mide descubrimiento conceptual abierto: las primitivas y las composiciones
  están predefinidas en el espacio de búsqueda.
- No mide costo real de consolidación, verificación o entrenamiento.
- No mide aprendizaje longitudinal \(G(n)\) con 100–10,000 experiencias.
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
    └── summary.json
```

## 8. Siguiente paso

Prototipo 003: sustituir las primitivas sintéticas por un agente LLM y tareas con
estructura latente, medir \(G(n)\) y separar reconocimiento, recuperación,
procedimiento y composición. Antes de eso, no se justifica JANUS-C ni otra capa.
