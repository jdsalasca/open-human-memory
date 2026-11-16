# Prototipo 005-A — Memoria bajo presupuesto: continuidad, orden y acumulación

**Fecha:** 16 de noviembre de 2026
**Estado:** **exploratorio**. No es confirmatorio: el protocolo no se congeló con
hash antes de medir, y lo digo aquí para que nadie lo cite como pre-registro. El
005-B sí deberá congelarse.
**Código:** `src/ohmem/v5_experiment.py` sobre `v3_solver.py`.
**Tests:** `tests/test_v5.py` (10 tests, 7 negativos).
**Resultados:** `results/seed-{0,1,2}.json`, `results/summary.json`.

## 1. Las tres preguntas que dejó abiertas el 004-A

La auditoría del 004-A formuló tres objeciones que este prototipo mide:

1. «64 programas» son 64 sintaxis, no 64 comportamientos.
2. El valor de una biblioteca depende de cuánto se parezca el futuro al pasado, y
   el 004-A evaluó con una distribución uniforme que castiga la frecuencia.
3. El costo publicado era una cota superior, no una medición: la comprobación se
   cortocircuita en el primer contraejemplo.

Se añade una cuarta, que es la que interesa al problema real de los agentes: **qué
pasa cuando el agente aprende en línea y tiene que decidir qué conservar**.

## 2. Contabilidad honesta

`v3_solver.solve` ahora devuelve dos contadores:

| Contador | Qué mide | Uso |
|---|---|---|
| `primitive_ops` | Cota superior: cada candidato × cada primitiva × 3 ejemplos | Congelado en el 004-A |
| `executed_steps` | Aplicaciones primitivas realmente ejecutadas hasta el primer contraejemplo | Todo el 005 |

El 004-A **no se modificó**. Su README lleva una fe de erratas: `primitive_ops` es
una cota, no una medición, y `D8` se añadió después del congelamiento.

## 3. La rejilla no tiene 64 problemas: tiene 14

Firmando cada programa por su salida sobre 40 entradas de prueba:

| Sintaxis | Comportamientos distintos |
|---|---|
| 64 | **14** |

Cobertura sobre los 14 representantes:

| Condición | Cobertura conductual |
|---|---|
| Sin memoria, profundidad 3 | **14/14 (100 %)** |
| Macros aprendidas, profundidad 2 | **9/14 (64,3 %)** |

El 004-A ya insinuaba esto (33/64 sin memoria), pero el número correcto es más
duro: **dos tercios de la «rejilla exhaustiva» eran el mismo comportamiento escrito
de otra forma**. La conclusión negativa del 004-A se mantiene, y sobre
comportamientos también.

## 4. La continuidad decide: curvas medidas

Definimos **continuidad** como la fracción de tareas de evaluación que contienen un
motivo de dos pasos presente en el entrenamiento. Cinco niveles, 5 sorteos de 16
tareas por nivel, 3 semillas.

### 4.1 Sin tope de cómputo

| Continuidad | Sin memoria d3 | Macros d2 |
|---|---|---|
| 0,00 | 100 % · 58,0 pasos | 78 % · 57,8 pasos |
| 0,25 | 100 % · 66,5 | 88 % · 51,5 |
| 0,50 | 100 % · 81,1 | 80 % · 63,1 |
| 0,75 | 100 % · 88,4 | 93 % · 56,9 |
| **1,00** | **100 % · 91,0** | **100 % · 52,9** |

Dos lecturas:

- **Con continuidad total, misma cobertura y 41,8 % menos trabajo.** Es la primera
  comparación limpia del programa: no se pierde nada y se ahorra cómputo.
- **Con continuidad cero, el mismo trabajo rinde 22,1 pp menos.** La biblioteca no
  es gratis: paga ramas que no sirven.

### 4.2 Con presupuesto fijo de 120 pasos ejecutados por tarea

| Continuidad | Sin memoria d3 | Macros d2 |
|---|---|---|
| 0,00 | **86 %** | 78 % |
| 0,25 | 82 % | **86 %** |
| 0,50 | 75 % | **80 %** |
| 0,75 | 72 % | **88 %** |
| 1,00 | 73 % | **94 %** |

Aquí el cruce es visible y es lo que la auditoría predijo: **bajo presupuesto, la
memoria gana desde continuidad ≈ 0,25 y amplía la ventaja hasta +21 pp**. Sin
presupuesto, solo empata en cobertura y gana en trabajo. Son dos regímenes
distintos y no conviene mezclarlos.

## 5. El orden no es gratis

Misma biblioteca, misma profundidad, mismo presupuesto, continuidad 1,0:

| Orden | Acierto | Pasos |
|---|---|---|
| Primitivas antes que macros | **93,8 %** | 51,5 |
| Macros antes que primitivas | 89,2 % | **44,7** |

La auditoría había medido que priorizar macros reduce candidatos sin cambiar
aciertos (1.192 vs 1.448). Con contador honesto y presupuesto, **sí cambia el
acierto**: un candidato con macro cuesta el doble de pasos que uno primitivo, así
que priorizarlas quema presupuesto antes de explorar. El orden es una política con
su propio costo, no un ajuste neutral.

## 6. Seleccionar mejor sobre lo visto no generaliza

Barrido de las 560 bibliotecas del mismo lenguaje. Se elige la mejor en la mitad
par de la rejilla y se evalúa en la impar:

| Criterio de selección | Acierto en reserva |
|---|---|
| Perfecta en desarrollo (100 %) | 73,8 % |
| Frecuencia (la del 003) | **81,3 %** |
| Azar, mismo lenguaje | 54,4 % |

Elegir la biblioteca que mejor ajusta lo ya visto **empeora** frente a contar
frecuencias. Con 560 candidatas y 32 tareas de desarrollo, el mejor ajuste es
sobreajuste. El cuello de botella no es el criterio de selección: es la cobertura
del mecanismo.

## 7. Aprender en línea: el resultado que importa para los agentes

Flujo de 96 tareas en 4 fases con deriva controlada:

- **P1:** motivos A.
- **P2:** motivos B (distintos).
- **P3:** vuelve A.
- **P4:** motivos C nuevos.

Presupuesto: 120 pasos ejecutados por tarea. `NOLEARN` busca profundidad 3;
las políticas con memoria buscan profundidad 2 (la memoria compila profundidad).

| Política | P1 | P2 | P3 | P4 | Global | Pasos | Competencia | Biblioteca |
|---|---|---|---|---|---|---|---|---|
| `NOLEARN` | 79 % | 83 % | 74 % | 67 % | 76,0 % | 6.877 | 15 | 4 |
| `FROZEN` (aprende en P1 y se congela) | 63 % | 92 % | 96 % | 54 % | 76,0 % | **5.074** | 20 | 8 |
| `ONLINE` (aprende siempre) | 63 % | 90 % | 63 % | 54 % | 67,0 % | 5.621 | 20 | 12 |
| `GATED` (tope 5 + desalojo por uso) | 46 % | 74 % | 83 % | 58 % | 64,6 % | 5.562 | 28 | 9 |

Lo que se sostiene:

- **Congelar lo aprendido ahorra 26,2 % de trabajo con la misma precisión**
  (76,0 % vs 76,0 %; +0,35 pp). Noventa y seis tareas vistas, ocho macros
  conservadas: ese es el artefacto acotado que sustituye al historial.
- **Acumular sin criterio empeora: −8,7 pp.** Doce macros son peores que ocho.
  Más memoria no es más mente.
- **Mi controlador de desalojo falló: −10,8 pp y competencia más tardía.** La
  hipótesis de que un tope con desalojo por uso arreglaría la acumulación **no se
  cumple** en este entorno. Hay que decirlo, no maquillarlo.
- La memoria **no acelera** la competencia inicial: 20 tareas frente a 15. Ayuda
  después, cuando el motivo se repite.
- En P4, con motivos nuevos, ninguna política pasa del 67 %. **La memoria no
  sustituye al razonamiento**: sin continuidad no hay nada que transferir.

Advertencia de diseño: `NOLEARN` usa profundidad 3 y las políticas con memoria
profundidad 2. No es una ablación limpia de «memoria»; es la comparación de dos
diseños bajo el mismo presupuesto de pasos. La diferencia de expresividad es
justamente lo que se está midiendo.

## 8. Qué significa para el problema del contexto

El historial completo de 96 tareas no cabe en una ventana. Ocho macros sí. En este
entorno, ese artefacto de ocho elementos:

- reproduce el 76 % de acierto del solucionador sin memoria,
- con 26 % menos cómputo,
- pero solo mientras el futuro se parezca al pasado.

Eso es la forma de una solución al problema del contexto: **un artefacto validado y
acotado, más una política que sepa cuándo confiar en él**. Tenemos el artefacto y
la curva que dice cuándo sirve. **La política sigue faltando**: mi primer intento
la empeoró.

## 9. Qué NO prueba

- No usa un LLM ni tareas reales.
- La continuidad se induce por construcción, no se estima en línea.
- El controlador `GATED` es una heurística, no una política aprendida.
- No hay contraejemplos, ambigüedad, ruido ni macros perjudiciales.
- No hay comparación ejecutada con Stitch, DreamCoder o LILO.
- Una sola familia de tareas; el resultado es local.

## 10. Reproducir

```bash
python resources/investigation/prototipo-005-presupuesto/reproduce.py
PYTHONPATH=src python -m unittest discover -s tests -v
```

Python 3.13, sin dependencias. Tiempo: ~5 s para las 3 semillas.

## 11. Archivos

```
prototipo-005-presupuesto/
├── README.md
├── reproduce.py
└── results/
    ├── seed-0.json
    ├── seed-1.json
    ├── seed-2.json
    └── summary.json
```
