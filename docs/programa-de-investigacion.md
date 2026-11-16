# Programa de investigación: memoria útil y lenguaje útil

**Fecha:** 16 de noviembre de 2026
**Estado:** programa rector tras la auditoría de LIRE-001b y 007B.

## 0. La lección que obliga a reescribir el programa

LIRE-001b parecía una habilidad de 120 reglas y 8.000 caracteres. Una sola fórmula
la reconstruía: `S{código}` si `importe < código`. **La longitud del texto no mide la
información independiente.** El experimento midió el seguimiento de una tabla
redundante, no memoria.

De ahí salen dos reglas para todo lo que sigue:

1. **Todo experimento de información necesita un control sin información.** Si el
   control acierta, la tarea no exige lo que creemos.
2. **La métrica principal debe estratificarse.** En LIRE-001b, responder siempre
   `NONE` acertaba la mitad de los casos. El acierto total ocultaba que la tabla no
   se usaba.

## 1. El problema de la memoria

**Definición operativa.** Un artefacto de memoria es útil si cambia las decisiones
del agente en una tarea reservada, a un coste menor que volver a derivar la
información. No es útil si solo añade contexto, si el agente no puede aplicarlo o si
un placebo produce el mismo efecto.

**Cuatro condiciones que hay que medir por separado:**

| Condición | Pregunta | Control |
|---|---|---|
| **Necesidad** | ¿La información está en el artefacto y no en los ejemplos? | Clon sin artefacto; historial de origen |
| **Aplicabilidad** | ¿El agente puede aplicar el procedimiento? | Oráculo con el programa completo; intérprete determinista |
| **Recuperación** | ¿Lo encuentra y lo usa en el momento? | Placebo; posición y longitud del recuerdo |
| **Atribución** | ¿La ganancia sobrevive a los controles y al coste? | Pares por tarea; coste de adquisición y verificación |

**Lo que mostró el 007B.** Con el programa completo, `luna` low resuelve 2/12 tareas
de cinco pasos (réplica 3/12). La condición de **aplicabilidad** falla. Por eso el
resultado del 007 —memoria 3/12, placebo 6/12— no se interpreta como falta de
memoria: mide una tarea que el modelo no aplica de forma fiable. No se identifica el
mecanismo (ejecución, interpretación de las operaciones, instrucciones o heurística).

**El orden correcto:**

1. **EXEC-001:** mapa de aplicación por profundidad y **complejidad funcional mínima**
   (no longitud nominal). Incluye programa simbólico, programa en lenguaje natural,
   pasos intermedios e intérprete determinista.
2. **MEM-002:** elegir una tarea donde el clon **aplique** pero **no identifique** el
   procedimiento. Comparar memoria, historial, placebo y oráculo, con coste total.
3. **Retención y transferencia:** reinicio, familia reservada, cambio de superficie.
   Métricas `E` (experiencias hasta umbral), `K` (conocimiento transferido) y `P`
   (desempeño), no solo acierto.

**Error que no se repetirá:** elegir una familia donde el clon falla puede fabricar
una ventaja trivial; hay que demostrar que el artefacto aporta información que el
clon no tiene **y** que el agente puede usar.

**Lo que aún no se ha probado:** la pregunta de “mil experiencias”. El 007 es una
sola adquisición y un solo reinicio; no mide acumulación a lo largo de muchas
experiencias. MEM-002 debe incluir un ciclo longitudinal y reportar `E` (experiencias
hasta el umbral), `K` (conocimiento transferido) y `P` (desempeño), además del
acierto puntual.

## 2. El problema del lenguaje

**Definición operativa.** Una representación es mejor si transmite más **bits
relevantes para la decisión por token** y el receptor los usa. Los caracteres, las
palabras y el ratio de compresión miden el soporte, no la información.

**Qué se mide:**

- **Información independiente:** longitud de descripción mínima de la tabla (en
  LIRE-002, ~3.759 bits).
- **Necesidad:** control sin tabla. Si acierta, la tabla no era necesaria.
- **Fidelidad estratificada:** casos positivos como métrica principal; negativos,
  frontera, excepción y códigos inexistentes como secundarios.
- **Coste incremental pareado:** `input_tokens` de la representación menos
  `input_tokens` del control sin tabla **en el mismo caso**. Cancela el arnés.
- **Tasa de información usable:** acierto positivo por 1.000 tokens incrementales.
- **Estructura frente a idioma:** español, inglés y chino no se comparan como
  culturas; se comparan como formatos. JSON y tabla TSV separan estructura de prosa.

**Lo que LIRE-002 puede establecer:** si una representación estructurada conserva
los casos positivos con menos tokens que la prosa. **Lo que no puede establecer:**
que el chino sea causalmente superior; longitud, sintaxis, redundancia e idioma
siguen confundidos. Para eso hace falta un factorial (LIRE-003), no una correlación
de 12 casos.

**Resultado (LIRE-002).** Sin tabla, 0/7 positivos. Con tabla, la recuperación
funciona (6–7/7), pero la **condición** falla: el modelo devuelve el estado cuando el
importe no cumple el umbral o pierde la excepción. El chino no ahorra tokens (2.949
vs 2.841 del español) ni acierta más (11 vs 10): la ventaja de LIRE-001b era un
artefacto. La tabla TSV ahorra 51 % de tokens y baja a 8/12; el conciso ahorra 48 % y
se queda en 10/12. **El problema del lenguaje no es el idioma: es la estructura y la
aplicación de la condición.**

**La pregunta de fondo:** ¿una representación **crea** una abstracción que el modelo
no tenía, o solo **comprime** información que ya podía derivar? LIRE-002 mide
compresión y recuperación. La creación se prueba con comunicación aprendida.

## 3. Comunicación aprendida (COMM-001)

Dos agentes con información parcial deben resolver una tarea conjunta bajo una
restricción de ancho de banda. Condiciones:

1. Lenguaje natural.
2. Código discreto diseñado a mano.
3. Código discreto **aprendido** por los agentes.
4. Binario empaquetado.

Se miden acierto, bits transmitidos, coste de entrenamiento, transmisión y
decodificación, y generalización a tareas y socios nuevos. **El código debe ser
aprendido, no diseñado**, y la información transmitida debe ser necesaria para la
tarea. Si el código aprendido no supera al lenguaje natural a igual coste, no hay
evidencia de un lenguaje mejor; solo de compresión.

## 4. Orden, dependencias y criterios de muerte

| Paso | Criterio de muerte |
|---|---|
| **F0** reproducir un baseline externo | No se avanza a comparaciones propias sin una línea base replicada |
| **LIRE-002** información independiente | Ninguna representación supera el control sin tabla en positivos → la tabla no se usa |
| **EXEC-001** aplicación | Ninguna profundidad alcanza 10/12 con el oráculo → el modelo no aplica; bajar profundidad o cambiar de modelo |
| **MEM-002** memoria útil | La memoria no supera al historial y al placebo a igual coste → no hay evidencia de memoria |
| **COMM-001** lenguaje aprendido | El código aprendido no supera al lenguaje natural a igual bits/coste → no hay evidencia de lenguaje mejor |

## 5. Lo que no se hará

- Más tablas redundantes disfrazadas de habilidades largas.
- Más tareas de memoria en una familia con suelo o techo.
- Afirmar superioridad de un idioma con 12 casos y confundidores.
- Comunicación latente o “cetácea” antes de demostrar un código aprendido que
  transmita información necesaria.
- Presentar una métrica de longitud (caracteres, tokens, compresión) como métrica de
  información.
