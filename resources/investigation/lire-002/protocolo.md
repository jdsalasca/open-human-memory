# LIRE-002 — Información independiente, no longitud

**Fecha:** 16 de noviembre de 2026
**Estado:** protocolo pre-registrado; piloto de 2 casos ejecutado, corrida completa en
curso.
**Modelo:** `gpt-6-luna`, `reasoning_effort = low`.
**Código:** `src/ohmem/lire_002.py`.
**Datos:** `results/luna-low-12cases.json`.

## 1. Por qué

LIRE-001b usaba 120 reglas de la forma `C{i}` / umbral `{i}` / `S{i}`. Una sola
fórmula las reconstruye, así que no medía información retenida. LIRE-002 construye
una tabla cuya información **no se puede reconstruir sin la tabla**:

- código aleatorio de 4 caracteres;
- umbral aleatorio, independiente del código;
- estado aleatorio de 12 etiquetas, independiente de ambos;
- 12 reglas con una excepción independiente y prioritaria;
- casos con códigos inexistentes, frontera, excepción y negativos.

## 2. Diseño

**Tabla:** 120 reglas. Información aproximada: **3.759 bits** (código 20 bits,
umbral 6,6, estado 3,6; excepción 11,1 bits en 12 reglas). Es una cota de la
descripción de la tabla **tal como se presenta**; el generador y la semilla no están
en el prompt.

**Casos:** 12, aleatorizados una vez y usados en el mismo orden por todas las
representaciones. Estratos:

| Estrato | n | Esperado |
|---|---|---|
| Positivo normal | 4 | estado de la regla |
| Positivo frontera (`amount = threshold - 1`) | 1 | estado |
| Positivo con excepción | 2 | estado de excepción |
| Negativo frontera (`amount = threshold`) | 1 | `NONE` |
| Negativo normal | 2 | `NONE` |
| Código inexistente | 2 | `NONE` |

**Métrica principal:** acierto en los **7 casos positivos**. Una estrategia de
responder siempre `NONE` acierta los 5 negativos/inexistentes, pero no los positivos;
por eso la métrica principal no es el acierto total. La instrucción define
explícitamente que se devuelva `NONE` cuando no aplica o el código no existe.

**Corrección tras el piloto:** la primera corrida completa no definía `NONE` en la
instrucción; sus casos negativos/inexistentes no son interpretables y se conservan
como `luna-low-12cases-pilot-instruction.json`. La corrida de evidencia usa la
instrucción corregida.

**Representaciones:** español, inglés, chino, español conciso, DSL, JSON compacto y
tabla TSV normalizada. **Control:** sin tabla.

**Aleatorización:** para cada caso se baraja el orden de las 8 condiciones. Así el
deterioro temporal del servicio afecta a todas por igual.

**Coste:** `input_tokens` de Codex. El coste de la habilidad se mide como la
**diferencia pareada** contra la llamada sin tabla en el mismo caso, que cancela el
arnés (~25.000–29.000 tokens). Se reportan mediana y mínimo de las diferencias.

**Tasa de información usable:** acierto positivo por 1.000 tokens incrementales.

## 3. Criterios de decisión (fijados antes de la corrida completa)

| Observación | Lectura |
|---|---|
| Control sin tabla ≥ 2/7 positivos | Hay fuga o el modelo adivina; la tarea no sirve. |
| Ninguna representación ≥ 6/7 positivos | La tabla no se usa; el experimento falla. |
| Una representación ≥ 6/7 y menos tokens que el español | Candidata a mejor representación; replicar. |
| Tabla/JSON pierden ≥ 2 positivos frente al español | La compacidad cuesta fidelidad. |
| Español, inglés y chino difieren en ≤ 1 positivo | No se establece superioridad de idioma. |

## 4. Piloto (2 casos, no evidencia)

| Representación | Positivos | Tokens incrementales (mediana) |
|---|---|---|
| Español | 2/2 | 2.837 |
| Inglés | 2/2 | 2.563 |
| Chino | 2/2 | 2.468 |
| Conciso | 2/2 | 1.915 |
| DSL | 2/2 | 2.479 |
| JSON | 2/2 | 1.901 |
| Tabla TSV | 1/2 | **945** |
| Sin tabla | 0/2 | 0 |

El control falla como se espera. La tabla TSV es la más barata y la única que falló
un caso (excepción): el piloto ya insinúa el compromiso entre compacidad y fidelidad.

## 5. Límites

- Un modelo, una semilla, 12 casos; sin repetición por caso.
- Idioma, longitud, redundancia y sintaxis siguen confundidos: no es un factorial.
  La tabla y el JSON son estructuras no lingüísticas; eso separa algo de sintaxis,
  no todo.
- La tabla es sintética y regular en su formato, aunque su contenido sea aleatorio.
- El control sin tabla puede **negarse** a responder en vez de adivinar; eso también
  es información (el modelo no inventa una tabla que no tiene).
- Los tokens incrementales incluyen el texto de la habilidad y cualquier variación
  del arnés; la mediana pareada reduce, no elimina, esa variación.
- No se ejecutó LLMLingua-2 ni otro compresor establecido; queda como control
  pendiente.
