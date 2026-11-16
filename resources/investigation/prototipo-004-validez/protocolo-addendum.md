# Addendum al protocolo del Prototipo 004-A

**Fecha:** 16 de noviembre de 2026.
**Motivo:** dos correcciones señaladas por la auditoría del commit `fb00e7d`. No se
modifica ningún resultado publicado; se corrige la interpretación.

## 1. `primitive_ops` es una cota superior, no una medición

El contador del 004-A multiplica `len(expanded) × len(support_inputs)` por cada
candidato, como si toda comprobación ejecutara todos los ejemplos. La
implementación usa `all(...)`, que corta en el primer contraejemplo.

Consecuencia: las cifras de `primitive_ops` del 004-A **sobreestiman** el trabajo.
Se conservan por trazabilidad. La medición con cortocircuito está en
`v3_solver.SolveResult.executed_steps` y es la que usa el Prototipo 005.

## 2. `D8` se añadió después del congelamiento

El protocolo congelado fija siete reglas (`D1`–`D7`). La tabla de resultados del
004-A incluye una octava:

> `D8` — la biblioteca encarece la búsqueda cuando se permite profundidad 3.

Es un análisis **post hoc**, observado al ver la condición `A4`. No estaba en el
protocolo y no debe presentarse como confirmatorio. Se conserva porque es
aritmética verificable sobre los mismos datos, pero se etiqueta como exploratorio.

## 3. Lo que no cambia

- Las cifras de acierto no dependen de los contadores.
- `D1`–`D7` se fijaron antes de la corrida y se cumplieron.
- La conclusión negativa del 004-A se mantiene, y el 005 la refuerza sobre
  comportamientos: 64 sintaxis son 14 funciones.
