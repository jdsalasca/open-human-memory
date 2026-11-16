# Prototipo 003 — Aprendizaje real de macros desde la experiencia

**Fecha:** 15 de noviembre de 2026  
**Estado:** prototipo sintético con aprendizaje verificable.  
**Código:** `src/ohmem/v3_tasks.py`, `v3_library.py`, `v3_solver.py`,
`v3_experiment.py`  
**Tests:** `tests/test_v3.py`  
**Resultados:** `results/seed-0.json`, `seed-1.json`, `seed-2.json`,
`summary.json`.

## 1. La pregunta que corrige al 002

El Prototipo 002 tenía un problema de validez: `MEM-E` no usaba el historial.
`MEM-A0`, el mismo solucionador composicional sin experiencias, empataba con
`MEM-E` en todas las distribuciones. Por tanto, el 002 medía un **solucionador**,
no aprendizaje.

El 003 introduce un mecanismo que **sí depende de la experiencia**:

1. El agente empieza con cuatro primitivas.
2. Resuelve tareas de entrenamiento con un solucionador de profundidad 2.
3. Cuando un programa de dos pasos se repite (≥2 veces), lo **encapsula como
   macro** en su biblioteca.
4. En evaluación, las macros cuentan como un solo paso, lo que permite resolver
   programas de profundidad 3.
5. La ablación elimina las macros y debe perder la capacidad.

## 2. Condiciones (misma información, mismo solucionador)

| Condición | Biblioteca | Historial |
|---|---|---|
| **NOLEARN** | 4 primitivas | No |
| **RANDOM** | 4 primitivas + 3 macros distractoras (`reverse`, `negate`) | No |
| **LEARNED** | 4 primitivas + macros aprendidas | Sí |
| **ABLATED** | 4 primitivas, macros eliminadas tras entrenar | Sí, pero borrado |

Todas usan los mismos ejemplos de soporte, el mismo solucionador y el mismo
límite de dos pasos. La única diferencia es la biblioteca.

## 3. Diseño

- **Entrenamiento:** 60 tareas con programas de profundidad 2 (`sort_asc→double`,
  `add_one→sort_desc`, `double→add_one`).
- **D1:** instancias nuevas con una primitiva.
- **D2:** familia nueva, profundidad 2.
- **D3:** profundidad 3, usando como prefijo una macro aprendida.
- **Ablación:** se borran las macros después de entrenar.

## 4. Resultados

Media de 3 semillas, 60 de entrenamiento, 30 de evaluación.

| Condición | D1 | D2 | D3 (profundidad 3) |
|---|---|---|---|
| NOLEARN | 1.000 | 1.000 | **0.000** |
| RANDOM | 1.000 | 1.000 | **0.000** |
| LEARNED | 1.000 | 1.000 | **1.000** |
| ABLATED | 1.000 | 1.000 | **0.000** |

Coste medido (media por distribución):

| Condición | D3 candidatos | D3 operaciones |
|---|---|---|
| NOLEARN | 600 | 1.080 |
| RANDOM | 1.680 | 4.500 |
| LEARNED | 740 | 1.680 |
| ABLATED | 600 | 1.080 |

## 5. Lectura

- **La capacidad se adquiere del historial.** Solo `LEARNED` resuelve D3.
- **La ablación la elimina.** `ABLATED` vuelve a 0.000. Es la respuesta directa a
  la pregunta de la auditoría: si borras la experiencia, ¿qué capacidad pierdes?
  La respuesta es D3.
- **No es solo "más operaciones".** `RANDOM` tiene el mismo tamaño de biblioteca
  que `LEARNED` (7 operaciones), pero sus macros son distractoras; falla D3 y
  gasta más búsqueda (1.680 candidatos vs 740).
- **Hay un coste real.** En D2, `LEARNED` gasta 460 candidatos frente a 310 de
  `NOLEARN`: la biblioteca crece y la búsqueda se encarece. La ganancia en D3 no
  es gratis.

## 6. Qué NO prueba

- No usa un LLM.
- Las macros son composiciones de primitivas **ya conocidas**; no descubre
  operaciones nuevas.
- D3 está diseñado para que el prefijo sea una macro aprendida; es transferencia
  composicional diseñada, no descubrimiento abierto.
- No hay ejemplos ambiguos, funciones equivalentes, ruido ni transferencia
  negativa.
- Los costes son nodos de búsqueda, no wall-clock ni memoria.
- No mide aprendizaje a largo plazo con deriva.

## 7. Reproducir

```bash
python resources/investigation/prototipo-003-aprendizaje/reproduce.py
PYTHONPATH=src python -m unittest discover -s tests -v
```

En PowerShell:

```powershell
$env:PYTHONPATH="src"
python -m unittest discover -s tests -v
python resources/investigation/prototipo-003-aprendizaje/reproduce.py
```

Python 3.13.15, sin dependencias externas.

## 8. Archivos

```
prototipo-003-aprendizaje/
├── README.md
├── reproduce.py
└── results/
    ├── seed-0.json
    ├── seed-1.json
    ├── seed-2.json
    └── summary.json
```

## 9. Siguiente paso

Prototipo 004: ambigüedad (varias hipótesis compatibles), funciones
observacionalmente equivalentes, transferencia negativa y tareas con estructura
latente más rica. Después, con un LLM real y `COMP-A..D`.
