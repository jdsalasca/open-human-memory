# LIRE-001 — Representación de una competencia conocida (piloto)

**Fecha:** 16 de noviembre de 2026
**Estado:** **ejecutado, resultado negativo y con un hallazgo útil.**
**Modelo:** `gpt-6.1-terra`, `reasoning_effort = medium`, 40 llamadas.
**Código:** `src/ohmem/lire_001.py`. **Protocolo:** `protocolo.md`.
**Datos:** `results/terra-medium.json`.

## 1. Qué se probó

Una regla de **cuatro ramas** con condiciones y excepciones, representada de cinco
formas. Ocho casos, dos por rama. La instrucción es idéntica; solo cambia la regla.

## 2. Resultados

| Representación | Acierto | Caracteres | Bytes | Tokens entrada (mediana) | Tokens salida | Tiempo |
|---|---|---|---|---|---|---|
| Español | **8/8** | 385 | 389 | 26.074 | 54,9 | 8,13 s |
| Inglés | **8/8** | 363 | 363 | 26.060 | 49,2 | 8,01 s |
| Chino | **8/8** | **139** | 381 | 26.076 | 55,5 | 7,17 s |
| Español conciso | **8/8** | 133 | **146** | 26.018 | 53,6 | 7,45 s |
| DSL simbólico | **7/8** | 200 | 200 | 26.041 | 53,6 | 6,82 s |

Mediana, no media: algunas llamadas incluyeron ~4.500 tokens extra del arnés y
distorsionan la media. El rango de medianas entre representaciones es de **61
tokens**.

## 3. Hallazgos

1. **Los caracteres no predicen los tokens.** El chino usa **64 % menos caracteres**
   que el español (139 vs 385) y, sin embargo, la mediana de tokens es **2 tokens
   mayor** (26.076 vs 26.074). En este modelo y este texto, la ventaja de caracteres
   del chino **no se traduce en ventaja de tokens**.
2. **Los bytes tampoco.** El chino ocupa 381 bytes frente a 389 del español: un 2 %
   menos. La frase china es corta en caracteres y casi idéntica en bytes (UTF-8, tres
   bytes por carácter).
3. **La representación no mueve la aguja a esta escala.** El arnés aporta ~26.000
   tokens; la regla aporta entre 20 y 70. Cualquier diferencia de representación
   queda dentro del ruido del arnés. **No se puede afirmar ahorro de tokens.**
4. **El DSL perdió un caso.** En `[9,4,1,-3]` debía invertir y duplicar
   (`[-6,2,8,18]`) y respondió `[-2,2,5]`: aplicó la rama equivocada. La
   representación compacta **no conservó la fidelidad**.
5. **Las prosa conservaron el 100 %.** Español, inglés, chino y español conciso
   acertaron los ocho casos. La compacidad del chino no costó precisión.

## 4. Lectura

- La hipótesis «el chino ahorra tokens» **no se sostiene** en este piloto. Ahorra
  caracteres; los tokens son casi idénticos.
- La hipótesis «un DSL compacto conserva la competencia con menos coste» **tampoco**:
  no ahorra tokens medibles y pierde un caso.
- El experimento **sí valida el método**: tokens reales, condiciones pareadas,
  cuatro ramas, control de fidelidad. Y muestra que la escala es el problema: para
  medir representación hay que superar el ruido del arnés.
- La conclusión útil es negativa y corrige una intuición: **más corto no es más
  barato, y más compacto no es más fiel.**

## 5. Qué haría falta para medir de verdad

1. **Aislar el prompt:** contar tokens del prompt con el tokenizador del modelo, o
   usar una tarea cuyo prompt sea el 90 % del total (regla de miles de palabras).
2. **Igualar el arnés:** misma sesión, mismo sistema, misma herramienta.
3. **Añadir LLMLingua-2** como línea base de compresión; no ejecutado.
4. **Fidelidad adversarial:** casos que distingan ramas cercanas, no solo cuatro
   ramas bien separadas.
5. **Repetir** con otro modelo y con el mismo prompt.

## 6. Límites

- Un modelo, ocho casos, una corrida.
- La regla es corta: 133–385 caracteres. El arnés domina.
- Sin LLMLingua-2, sin condición latente, sin condición acústica.
- El chino se evalúa como texto; no se afirma nada sobre estados internos.
- No es pre-registrado: las ramas y los casos se diseñaron para este piloto.

## 7. Reproducir

```powershell
$env:PYTHONPATH="src"
python -m ohmem.lire_001 --model gpt-6.1-terra --effort medium `
  --out resources/investigation/lire-001/results/terra-medium.json
```
