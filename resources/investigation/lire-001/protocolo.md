# LIRE-001 — Representación de una competencia conocida

**Fecha:** 16 de noviembre de 2026
**Estado:** **piloto exploratorio**. Un modelo, ocho casos, cinco representaciones.
**Modelo:** `gpt-6.1-terra`, `reasoning_effort = medium`.
**Código:** `src/ohmem/lire_001.py`.
**Resultado:** `results/terra-medium.json`.

## 1. La pregunta

> ¿La representación de una misma competencia cambia su coste real en tokens y la
> fidelidad con que el agente la aplica?

No es la pregunta de aprendizaje acumulativo. Es la primera mitad: **representar
bien una competencia conocida**. Sin esto, no tiene sentido estudiar si se conserva.

## 2. Diseño

Una regla de **cuatro ramas** con condiciones y excepciones:

1. Duplicados y primer elemento par → orden ascendente y +1.
2. Duplicados y primer elemento impar → orden descendente.
3. Sin duplicados y último negativo → invertir y duplicar.
4. Otro caso → invertir, +1 y quitar el último.

Cinco representaciones de la misma regla:

| ID | Representación |
|---|---|
| `es` | Español, prosa completa |
| `en` | Inglés, prosa completa |
| `zh` | Chino mandarín escrito |
| `es_concise` | Español conciso, sin redundancia |
| `dsl` | DSL simbólico de cuatro ramas |

La instrucción es idéntica en inglés para todas. Solo cambia la regla.

Ocho casos, dos por rama, con la misma instrucción y el mismo esquema de salida.

## 3. Métricas

- **Acierto exacto** en la lista resultante.
- **Tokens reales** de entrada y salida, leídos de los eventos `turn.completed` de
  Codex. No se estiman con caracteres.
- Caracteres, bytes y palabras de la regla, como diagnóstico secundario.
- Latencia.

## 4. Hipótesis y falsadores

| ID | Hipótesis | Falsador |
|---|---|---|
| L1 | La representación cambia los tokens reales de entrada | Diferencia ≤ 0 entre la más larga y la más corta |
| L2 | La fidelidad se conserva en las cinco representaciones | Alguna representación baja el acierto |
| L3 | El DSL conserva el acierto con menos tokens | El DSL no ahorra tokens o pierde acierto |

## 5. Controles y límites

- **Mismo modelo, misma instrucción, mismo esquema, mismos casos.**
- **Sin LLMLingua-2**: no se ejecutó la línea base de compresión establecida. Se
  declara como deuda.
- El `input_tokens` incluye el arnés de Codex (~30k). La comparación válida es la
  **diferencia entre representaciones**, no el valor absoluto.
- Ocho casos no permiten generalizar; es un piloto.
- El chino se evalúa como texto; no se afirma nada sobre los estados internos del
  modelo.
- No hay condición latente ni acústica. Este piloto es solo texto.

## 6. Reproducir

```powershell
$env:PYTHONPATH="src"
python -m ohmem.lire_001 --model gpt-6.1-terra --effort medium `
  --out resources/investigation/lire-001/results/terra-medium.json
```

## 7. Resultados

Ver `README.md` de esta carpeta cuando cierre la corrida.
