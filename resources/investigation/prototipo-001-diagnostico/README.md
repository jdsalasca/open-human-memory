# Prototipo 001 — Diagnóstico memoria vs selección vs procedimiento vs abstracción

> **ADVERTENCIA (15 nov 2026): este prototipo está invalidado como evidencia
> científica por target leakage.** El nombre de la regla (`sort_asc`, `double`,
> etc.) aparecía en `surface`, la entrada del predictor; `Task` exponía `rule` y
> `expected`; el oráculo usaba `query.rule`. Se conserva como *smoke test* de
> infraestructura y reproducibilidad. Los resultados **no** deben citarse a favor
> o en contra de ninguna hipótesis. La versión corregida es
> [`../prototipo-002-diagnostico/`](../prototipo-002-diagnostico/).

**Fecha:** 15 de noviembre de 2026  
**Estado:** prototipo sintético, reproducible, no es un benchmark de LLM.  
**Código:** `src/ohmem/`  
**Tests:** `tests/test_experiment.py`  
**Resultados crudos:** `results/seed-0.json`, `results/seed-1.json`,
`results/seed-2.json`, `results/summary.json`.

## 1. Qué se probó

El **instrumento**, no la teoría. La pregunta era:

> ¿El diseño experimental distingue entre memoria, selección, procedimiento y
> abstracción antes de construir otra arquitectura?

Se compararon cinco condiciones sobre tareas sintéticas con una regla oculta:

| Condición | Qué recibe el agente | Qué prueba |
|---|---|---|
| **A** | Sin memoria | Línea base |
| **B** | Retrieval por similitud de superficie | Valor del acceso |
| **C** | Experiencia correcta elegida por oráculo | Techo de la información |
| **D** | Procedimiento aprendido de las trazas | Valor de compilar |
| **E** | Abstracción por familia | Valor de conceptualizar |

Tres distribuciones:

- **D1:** nuevas instancias de familias vistas (`alpha`, `beta`).
- **D2:** familia nueva con la misma estructura (`gamma`, mismas reglas que
  `alpha`, distinto vocabulario).
- **D3:** familia estructuralmente nueva (`delta`, regla compuesta
  `sort_asc_then_double`).

## 2. Cómo se ejecuta

Requisitos: Python 3.11+ (probado con 3.13.15), sin dependencias externas.

```bash
python resources/investigation/prototipo-001-diagnostico/reproduce.py
```

Eso escribe `results/seed-0.json`, `seed-1.json`, `seed-2.json` y
`summary.json` con 200 tareas de entrenamiento y 50 de evaluación por semilla.

Tests:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

En PowerShell:

```powershell
$env:PYTHONPATH="src"; python -m unittest discover -s tests -v
```

Docker:

```bash
docker build -t ohmem .
docker run --rm ohmem
```

El contenedor ejecuta la semilla 0; para las tres semillas, montar el repo y
correr `reproduce.py`.

## 3. Resultados

Media de tres semillas (0, 1, 2); entre paréntesis, mínimo–máximo.

| Condición | D1 | D2 | D3 |
|---|---|---|---|
| A sin memoria | 0.240 (0.20–0.26) | 0.507 (0.40–0.58) | 0.000 |
| B retrieval | 0.980 (0.96–1.00) | 0.993 (0.98–1.00) | 0.027 (0.02–0.04) |
| C oráculo | 1.000 | 1.000 | 0.000 |
| D procedimiento | 0.920 (0.76–1.00) | 1.000 | 0.007 (0.00–0.02) |
| E abstracción | 0.487 (0.44–0.56) | 0.000 | 0.000 |

## 4. Cómo se lee (sin exagerar)

- **El instrumento separa las condiciones.** A queda muy por debajo; C marca el
  techo; B y D se acercan al techo en D1/D2.
- **En este juguete, el retrieval es casi suficiente en D1.** C supera a B por
  poco (1.00 vs 0.98). No hay evidencia aquí de que la selección sea el cuello;
  el diseño hace que el token de regla sea muy predictivo.
- **D iguala a C en D1/D2.** Compilar un procedimiento simple puede replicar el
  techo cuando la regla es fija. No prueba que funcione en un LLM ni en tareas
  abiertas.
- **E falla en D2/D3.** La abstracción implementada es por familia; no
  transfiere a una familia nueva. Es un **placeholder**, no evidencia de que la
  abstracción sea inútil. Un motor conceptual real tendría que descubrir la
  estructura compartida.
- **D3 es cero para todas las condiciones.** La regla compuesta no está en el
  entrenamiento; ninguna condición la inventa. Eso es esperado y muestra el
  límite del juguete: no hay motor de descubrimiento.

## 5. Qué NO se probó

- Un LLM real.
- Tareas abiertas o de producción.
- Costo de consolidación, verificación o entrenamiento.
- Transferencia entre modelos.
- Aprendizaje paramétrico.
- La hipótesis \(G(n)\) con 100–10,000 experiencias; aquí solo hay un corte de
  200 tareas de entrenamiento.
- La abstracción conceptual real; E es una aproximación por familia.

## 6. Por qué es útil igual

1. Deja un **banco de pruebas ejecutable** y determinista.
2. Verifica que las condiciones se separan y que el oráculo es techo.
3. Expone el límite del diseño: sin un motor conceptual, D3 no se resuelve.
4. Permite iterar el instrumento antes de gastar en modelos.

## 7. Archivos

```
prototipo-001-diagnostico/
├── README.md          este documento
├── reproduce.py       corre 3 semillas y escribe results/
└── results/
    ├── seed-0.json
    ├── seed-1.json
    ├── seed-2.json
    └── summary.json
```

Código: `src/ohmem/tasks.py`, `memory.py`, `conditions.py`, `experiment.py`.
Tests: `tests/test_experiment.py` (10 pruebas, todas pasan).

## 8. Siguiente paso

Sustituir las tareas sintéticas por familias reales con un adaptador de política
LLM y correr A–E con presupuesto igualado. Solo si C ≫ B o D ≫ C se justifica
JANUS-C; si E ≫ D en D2/D3, la frontera es el motor conceptual.
