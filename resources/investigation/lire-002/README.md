# LIRE-002 — El idioma no era el problema; la condición sí

**Fecha:** 16 de noviembre de 2026
**Estado:** **ejecutado, resultado mixto con un hallazgo metodológico y uno
sustantivo.**
**Modelo:** `gpt-6-luna`, `reasoning_effort = low`, `codex-cli 0.169.0`.
**Código:** `src/ohmem/lire_002.py`. **Protocolo:** `protocolo.md`.
**Datos:** `results/luna-low-12cases.json` (evidencia corregida),
`results/luna-low-12cases-pilot-instruction.json` (piloto sin instrucción de `NONE`).

## 1. Qué se midió

Una tabla de **120 reglas con información independiente**: código aleatorio de 4
caracteres, umbral aleatorio, estado aleatorio de 12 etiquetas y 12 excepciones con
prioridad. La tabla tiene ~**3.759 bits** de información **tal como se presenta**; el
generador y la semilla no están en el prompt. No se reconstruye con una fórmula a
partir del texto.

Doce casos: **7 positivos** (4 normales, 1 frontera, 2 excepciones) y **5
negativos/inexistentes** (1 frontera negativa, 2 negativos, 2 códigos que no existen).
La métrica principal son los 7 positivos: responder siempre `NONE` acierta los 5
secundarios pero **0/7** positivos.

Siete representaciones + **control sin tabla**. El coste se mide como diferencia
pareada de `input_tokens` contra el control en el mismo caso, lo que cancela el
arnés de Codex.

## 2. Resultados (corrida corregida)

| Representación | Positivos | Secundarios | Total | Caracteres | Tokens incr. | Positivos/1k | Bits/token |
|---|---|---|---|---|---|---|---|
| Español | 6/7 | 4/5 | 10/12 | 8.331 | 2.841 | 0,30 | 1,32 |
| Inglés | **7/7** | **5/5** | **12/12** | 8.197 | 2.605 | 0,38 | 1,44 |
| Chino | **7/7** | 4/5 | 11/12 | **4.342** | **2.949** | 0,34 | 1,27 |
| Español conciso | **7/7** | 3/5 | 10/12 | **2.884** | **1.477** | **0,68** | 2,55 |
| DSL | **7/7** | **5/5** | **12/12** | 6.578 | 2.490 | 0,40 | 1,51 |
| JSON | 6/7 | 2/5 | 8/12 | 8.117 | 2.356 | 0,36 | 1,60 |
| Tabla TSV | 6/7 | 2/5 | 8/12 | **2.245** | **1.400** | 0,61 | **2,69** |
| Sin tabla | **0/7** | 5/5 | 5/12 | 26 | 0 | — | — |

**Réplica (piloto, instrucción sin `NONE`):** los positivos fueron 7/7 en español,
inglés, chino, DSL y JSON; 6/7 en conciso; 5/7 en tabla; **0/7 sin tabla**. Los
secundarios del piloto no son interpretables (la instrucción no definía `NONE`).
El cambio de instrucción movió los secundarios de 0/5 a 2–5/5, pero **no eliminó los
fallos de condición**.

## 3. Hallazgos

### 3.1 El control sin tabla es 0/7 positivos

Responder siempre `NONE` acierta los 5 secundarios y da un 41,7 % de acierto total.
**La métrica estratificada es imprescindible:** el acierto total habría hecho parecer
que el control “sabe” algo. No sabe nada; solo explota la distribución de respuestas.

### 3.2 El modelo recupera las reglas, pero no comprueba la condición

Los positivos se resuelven 6–7/7 en todas las representaciones con tabla. La
recuperación funciona. Los fallos se concentran en los **secundarios**, donde el
modelo debe decidir que la regla **no** aplica:

- devuelve el estado de la regla cuando el importe es mayor o igual que el umbral
  (p. ej. `EPSILON`, `BETA`, `ZETA`);
- falla la prioridad de la excepción y devuelve el estado normal;
- en el código inexistente, a veces devuelve una etiqueta en vez de `NONE`.

Es el mismo patrón de LIRE-001b, ahora con información independiente: **el cuello no
es almacenar la regla, es evaluar la condición.** El inglés y el DSL aciertan 5/5
secundarios en esta corrida; el español, el chino, el conciso, el JSON y la tabla
fallan 1–3. Con 12 casos no se establece que el idioma sea la causa.

### 3.3 El chino no ahorra tokens ni acierta más

El chino usa **2.949** tokens incrementales frente a **2.841** del español: **cuesta
más**, aunque usa 48 % menos caracteres (4.342 vs 8.331). Acierta 11/12 frente a
10/12; dos casos a favor y uno en contra (p = 1,0). **No se replica la ventaja del
chino de LIRE-001b.** Aquella ventaja era un artefacto de una tabla redundante y de
medir el mínimo de tokens del arnés, no el coste incremental.

### 3.4 La compresión ahorra tokens y cuesta fidelidad

- **Tabla TSV:** 1.400 tokens (−51 % vs español), 8/12. Es la más barata y la que más
  fallos de condición acumula.
- **Conciso:** 1.477 tokens (−48 %), 10/12; conserva 7/7 positivos y pierde 2
  secundarios.
- **JSON:** 2.356 tokens (−17 %), 8/12; no compensa.
- **Inglés y DSL:** 2.605 y 2.490 tokens, **12/12**. Son las mejores en fidelidad.

No hay una representación que domine en las tres dimensiones (fidelidad, tokens y
condición). La elección depende de si el caso de uso tolera perder excepciones.

### 3.5 Las diferencias entre idiomas no se establecen

Inglés 12/12 vs español 10/12: dos pares a favor del inglés, cero en contra
(p = 0,5). Chino 11/12 vs español 10/12: dos a favor, uno en contra (p = 1,0). Con 12
casos y una sola corrida, el orden es inestable: en el piloto español, inglés y chino
empataron 7/7 en positivos; en la corrida corregida el español falló un positivo.
**No se atribuye la diferencia al idioma.**

## 4. Lectura

1. **La tabla es necesaria:** sin ella, 0/7 positivos en las dos corridas.
2. **La recuperación no es el cuello:** las reglas se encuentran.
3. **La condición es el cuello:** el modelo devuelve el estado sin comprobar el
   umbral, o falla la excepción.
4. **El idioma no es la variable principal:** el chino no ahorra tokens ni acierta
   más; las diferencias de 1–2 casos no se sostienen.
5. **La estructura ayuda al coste, no a la condición:** JSON y TSV ahorran tokens y
   fallan más condiciones.
6. **La representación óptima depende de la restricción:** si la fidelidad es
   obligatoria, inglés/DSL; si se tolera perder excepciones, conciso o tabla.

## 5. Límites

- Un modelo, una semilla, 12 casos; los cambios de 1–2 casos no son estables entre
  las dos corridas.
- Idioma, longitud, sintaxis y estructura siguen confundidos; no es un factorial.
- La tabla es sintética y regular en su formato, aunque su contenido sea aleatorio.
- El control sin tabla usa la estrategia de responder `NONE`; por eso el acierto
  total no sirve y se reporta el estratificado.
- Los tokens incrementales incluyen variación del arnés; la mediana pareada la
  reduce, no la elimina.
- La instrucción de `NONE` se añadió tras el piloto; el piloto se conserva y se
  reporta como ablación, no como evidencia principal.
- No se ejecutó LLMLingua-2 ni otro compresor establecido.

## 6. Reproducir

```powershell
$env:PYTHONPATH="src"
python -m ohmem.lire_002 --model gpt-6-luna --effort low --timeout 120 `
  --out resources/investigation/lire-002/results/luna-low-12cases.json
python resources/investigation/lire-002/analyze.py
```
