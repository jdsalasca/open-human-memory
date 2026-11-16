# Errata de LIRE-001b — La tabla no contenía información independiente

**Fecha:** 16 de noviembre de 2026
**Estado:** corrección obligatoria. Las conclusiones de LIRE-001b sobre fidelidad,
compresión e idioma quedan **retiradas como medida de información retenida**.
**Reemplazo:** `LIRE-002` (`src/ohmem/lire_002.py`).

## 1. Qué se afirmó

LIRE-001b comparó cinco representaciones de una supuesta habilidad de 120 reglas:

| Representación | Acierto | Tokens (mín.) |
|---|---|---|
| Español | 8/12 | 28.250 |
| Inglés | 10/12 | 28.100 |
| Chino | 11/12 | 27.861 |
| Español conciso | 8/12 | 26.534 |
| DSL | 7/12 | 27.009 |

Se interpretó como que la representación afecta la fidelidad con la que se conserva
una habilidad larga, y que el chino era el mejor compromiso.

## 2. Qué está mal

### 2.1 Las 120 reglas son una sola fórmula

Cada regla se genera así:

```
Regla i: si el código es C{i:03d} y el importe es menor que {i}, devuelve S{i:03d}.
```

El umbral es el número del código y el estado repite ese número. La tabla completa
se reconstruye con:

```python
def resolver(codigo, importe):
    return f"S{codigo:03d}" if importe < codigo else "NONE"
```

No hay 120 asociaciones independientes que recuperar. El experimento mide el
seguimiento de instrucciones redundantes y una comparación numérica, no la
fidelidad de una base de conocimiento.

### 2.2 El verificador no comprueba pertenencia

```python
def expected(code, amount):
    return f"S{code:03d}" if amount < code else "NONE"
```

Para `C999` con importe 1 devuelve `S999`, aunque la tabla solo contiene `C000` a
`C119`. El evaluador comparte la regularidad que vuelve redundante la tabla.

### 2.3 El orden de los casos no está aleatorizado

Los seis primeros casos son positivos y los seis últimos negativos. Cada llamada es
independiente, pero el orden temporal no está controlado.

### 2.4 El coste no está aislado

Se reporta el mínimo de `input_tokens` por representación, que incluye el arnés de
Codex (~28.000 tokens). El mínimo es un diagnóstico de la ruta limpia, no el coste
esperado. La comparación entre representaciones no está pareada por caso.

## 3. Qué sobrevive

- Las mediciones de tokens son reales; el arnés domina el coste.
- El patrón de fallo en los casos `NONE` (devolver el estado sin comprobar el
  umbral) es una observación válida sobre el seguimiento de la tabla redundante.
- La observación de que los caracteres no predicen los tokens sigue en pie.
- **No sobrevive** la interpretación de que el chino, el inglés o el DSL conservan
  mejor una habilidad larga.

## 4. Qué se retira

1. «El chino es el mejor compromiso para conservar una habilidad larga».
2. «La compresión ahorra tokens y pierde fidelidad» como afirmación sobre
   información retenida.
3. Cualquier atribución causal al idioma: longitud, redundancia, sintaxis e idioma
   siguen confundidos.

## 5. Qué lo reemplaza

**LIRE-002** corrige los cuatro defectos:

- 120 reglas con **código, umbral, estado y excepción independientes y aleatorios**;
- verificador que comprueba la existencia del código y usa los campos reales;
- 12 casos estratificados (positivos, frontera, excepción, negativos, códigos
  inexistentes) y **orden aleatorizado** por caso y representación;
- **control sin tabla** para medir qué se puede responder sin información;
- coste **pareado** contra el control en el mismo caso, que cancela el arnés;
- representaciones adicionales: JSON compacto y tabla TSV normalizada;
- métrica principal: acierto en los casos positivos, que no se puede aprobar con una
  estrategia de responder siempre `NONE`.

## 6. Lección

**Una base extensa de texto no contiene necesariamente una cantidad extensa de
información independiente.** La longitud, los caracteres y los tokens miden el
soporte, no la información. La pregunta correcta es cuánta información
independiente, necesaria para decidir, se conserva y se usa bajo un presupuesto.
