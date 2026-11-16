# Prototipo 003 — Aprendizaje de macros (exploratorio, superado)

**Fecha:** 15 de noviembre de 2026
**Estado:** **exploratorio y superado.** El Prototipo 004-A reejecutó este diseño
con los controles que faltaban y retiró la conclusión principal. Este documento se
conserva como registro de lo que se creyó y por qué era incorrecto:
`../prototipo-004-validez/`.
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
4. En evaluación, las macros cuentan como un solo paso, lo que permitía resolver
   programas de profundidad 3 **sin buscarlos**.
5. La ablación elimina las macros; el diseño original esperaba perder con ello la
   capacidad. El 004-A mostró que no era una capacidad: era un límite de búsqueda.

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
- **D3:** profundidad 3, usando como prefijo una macro aprendida. **Los tres
  programas fueron elegidos a mano** entre los 31 de la rejilla que no tienen una
  equivalencia de profundidad 2; el 004-A lo mide y lo corrige.
- **Ablación:** se borran las **macros compiladas**, no las experiencias. Es una
  intervención sobre la biblioteca, no sobre el historial bruto.

## 4. Resultados

Media de 3 semillas, 60 de entrenamiento, 30 de evaluación.

| Condición | D1 | D2 | D3 (profundidad 3) |
|---|---|---|---|
| NOLEARN | 1.000 | 1.000 | **0.000** |
| RANDOM | 1.000 | 1.000 | **0.000** |
| LEARNED | 1.000 | 1.000 | **1.000** |
| ABLATED | 1.000 | 1.000 | **0.000** |

Coste medido (media por distribución; `operaciones` = aplicaciones primitivas ×
3 ejemplos de soporte, contador corregido en el 004):

| Condición | D3 candidatos | D3 operaciones |
|---|---|---|
| NOLEARN | 600 | 3.240 |
| RANDOM | 1.680 | 13.500 |
| LEARNED | 740 | 5.040 |
| ABLATED | 600 | 3.240 |

## 5. Lectura (retirada por el 004-A)

La lectura original era:

> «La capacidad se adquiere del historial. Solo `LEARNED` resuelve D3. Si borras la
> experiencia, pierdes D3.»

**Esa lectura es falsa.** El 004-A añadió `A1-nolearn-d3`, el mismo solucionador
sin historial con búsqueda de tres pasos: resuelve **64/64** en la rejilla
completa. Y el 0 % del 003 era en parte artefacto de elegir tres programas sin
equivalencia de profundidad 2: en la rejilla, profundidad 2 ya resuelve 33/64.

Lo que sobrevive:

- `LEARNED` gasta **17,8 % menos candidatos** que la búsqueda profunda en la
  rejilla, pero resuelve **10 tareas menos** (54/64 frente a 64/64).
- Por acierto, el ahorro es del **2,6 %**: económicamente nulo.
- El control `RANDOM` estaba amañado: usaba `reverse`/`negate`, fuera del lenguaje
  del generador. Con bibliotecas del **mismo lenguaje**, 250/560 son perfectas en
  el D3 del 003 y **124/560 igualan o superan** a la biblioteca aprendida en la
  rejilla.
- La curva se satura en **6 experiencias**; las otras 54 no aportan nada.

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
- **La biblioteca no amplía la cobertura**: resuelve 54/64 donde la búsqueda
  profunda resuelve 64/64.
- **El control aleatorio no era comparable**: usaba operaciones ajenas al
  lenguaje del generador.
- **La ablación borra macros, no historial**: no demuestra nada sobre conservar o
  descartar episodios.

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

Ejecutado: Prototipo 004-A (`../prototipo-004-validez/`), con protocolo congelado,
`NOLEARN-depth3`, barrido de 560 bibliotecas del mismo lenguaje, rejilla completa
de 64 programas, curva de adquisición, costo compartido/incremental, registro de
uso de macros y comparación a igual presupuesto.

Pendiente para el 005: tareas adversariales (ruido, ambigüedad, equivalencias,
deriva, macros perjudiciales), actualización online durante la evaluación
(`Experimento C`) y comparación real contra DreamCoder/Stitch/LILO. Después, con un
LLM real y `COMP-T0..T3`.
