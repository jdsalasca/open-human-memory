# LIRE-001b — Skill larga: el ahorro se paga en fidelidad

**Fecha:** 16 de noviembre de 2026
**Estado:** ejecutado con `gpt-6-luna` low (política de experimentos). La corrida con
terra queda como exploratoria y no se usa como evidencia.
**Modelo:** `gpt-6-luna`, `reasoning_effort = low`, `codex-cli 0.169.0`.
**Código:** `src/ohmem/lire_001b.py`.
**Datos:** `results/luna-low.json` (evidencia) y `results/terra-medium.json`
(exploratorio).

## 1. Qué se midió

Una skill de **120 reglas** con código, umbral y estado. Seis casos: tres cumplen el
umbral (`Sxxx`) y tres no (`NONE`). Cinco representaciones de la misma skill.

Métrica principal: **mínimo** de `input_tokens` por representación, para evitar las
llamadas con ~4.500 tokens extra del arnés.

## 2. Resultados con luna low (evidencia)

| Representación | Acierto | Caracteres | Bytes | Tokens (mín.) | Δ vs español |
|---|---|---|---|---|---|
| Español | **4/6** | 9.267 | 9.388 | 28.230 | — |
| Inglés | **6/6** | 9.034 | 9.034 | 28.107 | −123 (−0,4 %) |
| Chino | **6/6** | **4.258** | 8.412 | 27.868 | **−362 (−1,3 %)** |
| Español conciso | **4/6** | **3.052** | **3.295** | **26.532** | **−1.698 (−6,0 %)** |
| DSL simbólico | **4/6** | 4.963 | 4.963 | 27.009 | **−1.221 (−4,3 %)** |

## 3. El hallazgo: los fallos son de condición, no de búsqueda

Los seis casos incluyen tres `NONE` (el importe **no** cumple el umbral). **Todos los
fallos son exactamente esos tres tipos**: el modelo encuentra la regla correcta y
devuelve su estado **sin comprobar el umbral**.

| Representación | Fallos | Caso |
|---|---|---|
| Español | 2 | C051 (60 ≥ 51) y C078 (90 ≥ 78) devuelven `S051`/`S078` |
| Español conciso | 2 | C027 y C051 |
| DSL | 2 | C051 y C078 |
| Inglés | 0 | — |
| Chino | 0 | — |

No es un fallo de lookup —el código se encuentra— sino de **evaluación de la
condición**. La forma compacta ahorra tokens y pierde la excepción.

## 4. Lectura

1. **El ahorro es real pero pequeño en la llamada completa:** 0,4–6,0 %. La skill
   española ocupa ~9.300 caracteres; la concisa, ~3.000. El ahorro absoluto
   (1.698 tokens) es grande **sobre la skill** y pequeño **sobre la llamada**.
2. **El chino es el mejor compromiso en esta muestra:** 6/6 y −1,3 % de tokens. No
   es el más corto en tokens, pero conserva la condición.
3. **El español conciso y el DSL ahorran más y fallan más.** La compresión se paga
   en los casos frontera, que es exactamente donde el umbral importa.
4. **Los caracteres no predicen los tokens:** el chino usa 54 % menos caracteres y
   ahorra 1,3 % de tokens.
5. **La corrida con terra (6/6 en todas) no replica.** Terra es más capaz; por eso
   los experimentos van con luna y terra solo analiza.

## 5. Límites

- `gpt-6-luna` low, seis casos, una corrida; sin repetición por caso.
- Los fallos de condición son 2/6 por representación: el patrón es consistente, pero
  la muestra no permite significación.
- La skill es sintética y regular.
- Sin LLMLingua-2 ni compresión establecida como control.
- Longitud, idioma, redundancia y sintaxis siguen confundidos; no se atribuye la
  diferencia solo al idioma.
- El mínimo de tokens es una estimación de la ruta limpia del arnés.
- No es pre-registrado: se diseñó tras el techo de LIRE-001.

## 6. Reproducir

```powershell
$env:PYTHONPATH="src"
python -m ohmem.lire_001b --model gpt-6-luna --effort low `
  --out resources/investigation/lire-001b/results/luna-low.json
```

## Apéndice. Corrida exploratoria con terra

`results/terra-medium.json`: 6/6 en las cinco representaciones; ahorro 0,4–5,8 %.
No se usa como evidencia. Confirma que el ahorro de tokens es estable entre modelos,
pero la fidelidad no: terra conserva la condición, luna no.
