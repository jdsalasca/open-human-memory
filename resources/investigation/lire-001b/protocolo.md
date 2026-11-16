# LIRE-001b — Skill larga: la representación pesa cuando el arnés no la tapa

**Fecha:** 16 de noviembre de 2026
**Estado:** piloto ejecutado. Un modelo, 120 reglas, 6 casos.
**Modelo:** `gpt-6.1-terra`, `reasoning_effort = medium`.
**Código:** `src/ohmem/lire_001b.py`.
**Resultado:** `results/terra-medium.json`.

## 1. Por qué existe

LIRE-001 midió una regla de 133–385 caracteres. El arnés de Codex aporta ~26.000
tokens, así que la representación cabía dentro del ruido: el chino ahorraba 64 %
de caracteres y **+2 tokens** de mediana.

La conclusión fue: para medir representación hay que superar el ruido. Eso es lo
que hace este piloto.

## 2. Diseño

**Skill de 120 reglas.** Cada regla tiene un código único, un umbral y un estado:

```
Si el código es C003 y el importe es menor que 3, devuelve S003.
```

**Seis casos:** tres cumplen el umbral (devuelven `Sxxx`) y tres no lo cumplen
(devuelven `NONE`). Así se prueba **lookup + evaluación de condición**, no solo
encontrar una línea.

**Cinco representaciones de la misma skill:**

| ID | Representación |
|---|---|
| `es` | Español, prosa completa |
| `en` | Inglés, prosa completa |
| `zh` | Chino mandarín escrito |
| `es_concise` | Español conciso |
| `dsl` | DSL simbólico |

**Métrica principal:** `input_tokens` reales de Codex. Se reporta el **mínimo** por
representación, que es la ruta más limpia del arnés, además de la mediana.

## 3. Predicciones

| ID | Predicción | Falsador |
|---|---|---|
| B1 | Con skill larga, la representación cambia los tokens de entrada | Diferencia ≤ 500 tokens entre la más larga y la más corta |
| B2 | El chino usa menos tokens que el español | Chino ≥ español |
| B3 | El español conciso usa menos tokens que el español | Conciso ≥ español |
| B4 | El DSL conserva el acierto | El DSL falla algún caso |
| B5 | Las prosas conservan el acierto | Alguna prosa falla |

## 4. Límites

- Un modelo, seis casos, una corrida.
- Skill sintética y regular; no es una skill real de dominio.
- Sin LLMLingua-2; no se compara con compresión establecida.
- El `input_tokens` incluye el arnés; se compara por diferencia y mínimo.
- No es pre-registrado: se diseñó después de ver el techo de LIRE-001.

## 5. Reproducir

```powershell
$env:PYTHONPATH="src"
python -m ohmem.lire_001b --model gpt-6.1-terra --effort medium `
  --out resources/investigation/lire-001b/results/terra-medium.json
```
