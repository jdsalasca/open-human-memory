# LIRE-001b — Skill larga: el ahorro existe, pero el arnés lo diluye

**Fecha:** 16 de noviembre de 2026
**Estado:** ejecutado. Un modelo, 120 reglas, 6 casos, 30 llamadas.
**Modelo:** `gpt-6.1-terra`, `reasoning_effort = medium` (corrida principal).
Réplica con `gpt-6-luna` low en curso, según la política de experimentos.
**Código:** `src/ohmem/lire_001b.py`.
**Datos:** `results/terra-medium.json`.

## 1. Qué se midió

Una skill de **120 reglas** con código, umbral y estado. Seis casos: tres cumplen el
umbral (`Sxxx`) y tres no (`NONE`). Cinco representaciones de la misma skill.

La métrica principal es el **mínimo** de `input_tokens` por representación, no la
media: algunas llamadas incluyen ~4.500 tokens extra del arnés y contaminan la
comparación.

## 2. Resultados

| Representación | Acierto | Caracteres | Bytes | Tokens (mín.) | Δ vs español |
|---|---|---|---|---|---|
| Español | **6/6** | 9.267 | 9.388 | 28.859 | — |
| Inglés | **6/6** | 9.034 | 9.034 | 28.745 | −114 (−0,4 %) |
| Chino | **6/6** | **4.258** | 8.412 | 28.513 | **−346 (−1,2 %)** |
| Español conciso | **6/6** | **3.052** | **3.295** | **27.175** | **−1.684 (−5,8 %)** |
| DSL simbólico | **6/6** | 4.963 | 4.963 | 27.652 | **−1.207 (−4,2 %)** |

Las cinco representaciones acertaron los seis casos, incluidos los tres `NONE`.
El DSL no falló esta vez.

## 3. El smoke mentía

En la calibración de un solo caso, el español marcó 33.455 tokens y el chino
28.519: una diferencia del **14,8 %**. Con seis casos y el mínimo por representación,
la diferencia es de **346 tokens (1,2 %)**.

La llamada española del smoke había caído en la ruta de ~33k del arnés. **La cifra
del 14,8 % se retira.** Es el mismo error que la auditoría advirtió: una sola
llamada no estima el coste de la representación.

## 4. Lectura

1. **El ahorro es real pero pequeño en la llamada completa.** El español conciso
   ahorra 1.684 tokens; el DSL, 1.207; el chino, 346. Sobre una llamada de ~28.000,
   eso es 1–6 %.
2. **Sobre el coste de la skill, el ahorro es grande.** La skill española ocupa
   ~9.300 caracteres (~2.300 tokens); la concisa, ~3.000 (~760). El ahorro de 1.684
   tokens es del orden del 60–70 % del coste de la propia skill. El arnés lo diluye.
3. **Los caracteres no predicen los tokens, otra vez.** El chino usa 54 % menos
   caracteres y ahorra 1,2 % de tokens. La relación no es lineal ni proporcional.
4. **La fidelidad se conservó en las cinco formas**, incluido el DSL. El fallo del
   DSL en LIRE-001 (1/8) no se replicó; con seis casos no se distingue de variación.
5. **La representación importa más cuanto más pesada es la skill respecto al
   arnés.** Con 28k de arnés, el efecto es marginal; en un agente con arnés pequeño,
   el mismo ahorro relativo sería mucho mayor.

## 5. Límites

- Un modelo, seis casos, una corrida; no hay repetición por caso.
- La skill es sintética y regular; no es una skill real de dominio.
- Sin LLMLingua-2 ni compresión establecida como control.
- Longitud, idioma, redundancia y sintaxis siguen confundidos: el diseño no es
  factorial. El chino es más corto *y* distinto; no se atribuye la diferencia solo
  al idioma.
- El mínimo de tokens es una estimación de la ruta limpia del arnés, no una medición
  del tokenizador de la regla.
- No es pre-registrado: el piloto se diseñó tras ver el techo de LIRE-001.

## 6. Reproducir

```powershell
$env:PYTHONPATH="src"
python -m ohmem.lire_001b --model gpt-6.1-terra --effort medium `
  --out resources/investigation/lire-001b/results/terra-medium.json
```
