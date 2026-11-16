# Addendum al protocolo del Prototipo 006-A

**Fecha:** 16 de noviembre de 2026.
**Motivo:** el protocolo congelado no contabilizó el costo del probe de
aplicabilidad. No se modifica ningún resultado; se corrige la conclusión
económica.

## 1. Qué se omitió

El presupuesto y los contadores miden solo pasos de búsqueda. El probe se ejecuta
**antes** de cada decisión y también aplica primitivas: hasta 3 macros × 4
primitivas × 2 orientaciones × 3 ejemplos.

Medición post hoc (`probe_cost.py`, cota superior con cortocircuito):

| Conjunto | Coste medio |
|---|---|
| Similar | 96,0 pasos/tarea |
| Novel | 122,4 pasos/tarea |

Las predicciones `P1`–`P4` se refieren a acierto y a pasos de búsqueda, y se
mantienen tal como se congelaron. Lo que no se puede afirmar es que la política
sea económicamente ventajosa: **ahorra 28,9 pasos y gasta 96**.

## 2. Consecuencia

La conclusión válida es doble:

1. El mecanismo de decisión funciona: la política aprende a cambiar y domina a las
   acciones fijas en acierto.
2. La economía no funciona: con el probe contabilizado, la política es la peor
   opción en cómputo total.

Para el 007, el probe debe ser barato (cacheado por firma, calculado una vez por
familia o sustituido por un índice) antes de repetir esta comparación. Sin eso, la
política no justifica su costo.

## 3. Qué no cambia

- Los archivos `results/seed-{1,2}.json` y `summary.json` no se tocan.
- Los hashes de `frozen.sha256` siguen siendo válidos: el código congelado no se
  modificó, y `probe_cost.py` es un script separado.
