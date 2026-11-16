# LIRE-001b — Skill larga: el ahorro se paga en fidelidad

> **Retractado como medida de información (16 de noviembre de 2026).** Las 120
> reglas son una sola fórmula (`S{código}` si importe < código), el verificador no
> comprueba la pertenencia del código y el orden de casos no está aleatorizado. Las
> cifras se conservan como observación del seguimiento de una tabla redundante, no
> como evidencia de información retenida. Ver
> [`docs/errata-lire-001b.md`](../../../docs/errata-lire-001b.md) y **LIRE-002**.

**Fecha:** 16 de noviembre de 2026
**Estado:** ejecutado con `gpt-6-luna` low. La corrida con terra queda como
exploratoria y no se usa como evidencia.
**Modelo:** `gpt-6-luna`, `reasoning_effort = low`, `codex-cli 0.169.0`.
**Código:** `src/ohmem/lire_001b.py`.
**Datos:** `results/luna-low-12cases.json` (evidencia principal),
`results/luna-low.json` (6 casos, réplica), `results/terra-medium.json`
(exploratorio).

## 1. Qué se midió

Una skill de **120 reglas** con código, umbral y estado. Doce casos: seis cumplen
el umbral (`Sxxx`) y seis no (`NONE`). Cinco representaciones de la misma skill.

Métrica de tokens: **mínimo** de `input_tokens` por representación, para evitar las
llamadas con decenas de miles de tokens extra del arnés.

## 2. Resultados con luna low

| Representación | 6 casos | **12 casos** | Caracteres | Bytes | Tokens (mín.) | Δ vs español |
|---|---|---|---|---|---|---|
| Español | 4/6 | **8/12 (66,7 %)** | 9.267 | 9.388 | 28.250 | — |
| Inglés | 6/6 | **10/12 (83,3 %)** | 9.034 | 9.034 | 28.100 | −150 (−0,5 %) |
| Chino | 6/6 | **11/12 (91,7 %)** | **4.258** | 8.412 | 27.861 | **−389 (−1,4 %)** |
| Español conciso | 4/6 | **8/12 (66,7 %)** | **3.052** | **3.295** | **26.534** | **−1.716 (−6,1 %)** |
| DSL simbólico | 4/6 | **7/12 (58,3 %)** | 4.963 | 4.963 | 27.009 | −1.241 (−4,4 %) |

## 3. Dónde falla cada forma

Los doce casos incluyen seis `NONE` (el importe **no** cumple el umbral). Los fallos
se concentran en esa condición, pero no todos son del mismo tipo:

| Representación | Fallos | Detalle |
|---|---|---|
| Español | 4 | Cuatro falsos positivos: devuelve `Sxxx` en casos `NONE` |
| Inglés | 2 | Dos falsos positivos |
| **Chino** | **1** | Un falso positivo |
| Español conciso | 4 | **Dos falsos negativos** (devuelve `NONE` cuando tocaba `Sxxx`) + dos falsos positivos |
| DSL | 5 | **Un falso negativo** + cuatro falsos positivos |

La forma compacta no solo acepta lo que no debe: también **rechaza casos válidos**.
Eso es peor que un fallo de búsqueda, porque el agente deja de actuar cuando debía.

## 4. Lectura

> **Aviso:** estas lecturas describen el seguimiento de una tabla redundante. No
> establecen que una representación conserve mejor información independiente.

1. **El chino es el mejor compromiso en esta muestra:** 11/12 y −1,4 % de tokens.
   No es la forma más barata, pero es la más fiel.
2. **El ahorro es real y pequeño sobre la llamada:** 0,5–6,1 %. Sobre la skill es
   grande: la concisa ocupa un tercio de la española.
3. **Las formas más baratas son las menos fieles:** conciso y DSL ahorran 4–6 % y
   fallan 4–5 de 12, incluyendo casos válidos.
4. **Los caracteres no predicen los tokens:** el chino usa 54 % menos caracteres y
   ahorra 1,4 % de tokens.
5. **La réplica de 6 casos coincide en dirección:** chino e inglés arriba; español,
   conciso y DSL abajo.
6. **La corrida con terra (6/6 en todas) no replica.** Terra es más capaz; por eso
   los experimentos van con luna y terra solo analiza.

## 5. Límites

- `gpt-6-luna` low, 12 casos, una corrida; sin repetición por caso.
- Las diferencias de acierto son de 1–4 casos: no permiten significación.
- La skill es sintética y regular.
- Sin LLMLingua-2 ni compresión establecida como control.
- Longitud, idioma, redundancia y sintaxis siguen confundidos; no se atribuye la
  diferencia solo al idioma.
- El mínimo de tokens es una estimación de la ruta limpia del arnés.
- Algunas llamadas de la forma concisa incluyeron 60–90k tokens de arnés; el mínimo
  y la mediana las aislan, pero muestran la variabilidad del servicio.
- No es pre-registrado: se diseñó tras el techo de LIRE-001.

## 6. Reproducir

```powershell
$env:PYTHONPATH="src"
python -m ohmem.lire_001b --model gpt-6-luna --effort low `
  --out resources/investigation/lire-001b/results/luna-low-12cases.json
```

## Apéndice. Corrida exploratoria con terra

`results/terra-medium.json`: 6/6 en las cinco representaciones con 6 casos; ahorro
0,4–5,8 %. No se usa como evidencia. Confirma que el ahorro de tokens es estable
entre modelos, pero la fidelidad no: terra conserva la condición, luna no siempre.
