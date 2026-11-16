# Teoría y marco

**Fecha:** 16 de noviembre de 2026
**Estado:** documento central. Absorbe `problema-central.md` y la parte teórica de
`revision-de-rumbo.md`. Si algo contradice este documento, se corrige lo otro.

---

## 0. La pregunta

> Si mañana este agente reinicia su contexto, cambia de tarea y encuentra un
> problema que nunca ha visto, ¿qué aprendizaje adquirido en sus experiencias
> anteriores modifica realmente su manera de comprenderlo y resolverlo?

Hoy **no podemos responderla con un experimento**. Este documento explica qué se
afirma, por qué canales, qué lo refutaría y por qué nuestros seis prototipos no
podían responderla.

---

## 1. El fenómeno

No estudiamos memoria. Estudiamos **expansión de competencia**: el cambio en la
capacidad futura de un agente atribuible a su historia.

La distinción es operativa. Un agente puede recordar más y no ser más competente;
puede ejecutar mejor y no haber aprendido; puede acumular procedimientos y no saber
cuándo usarlos. El objeto es el cambio de capacidad; la memoria es un instrumento.

Cuatro verbos distintos, que hemos confundido:

| Verbo | Qué cambia | Cómo se falsea |
|---|---|---|
| **Recordar** | La información disponible | Recupera el episodio y no mejora |
| **Usar** | La decisión, dado el recuerdo | Se le entrega y lo ignora |
| **Adquirir** | Una competencia nueva | Un clon la adquiere igual de rápido |
| **Aprender a adquirir** | La velocidad de adquisición | El clon necesita lo mismo |

Tres métricas, nunca una sola:

- `E(A,F)`: experiencias hasta el umbral `θ` en la familia reservada `F`.
- `K(A,F)`: cómputo, tokens y mantenimiento hasta `θ`.
- `P(A,F)`: desempeño tras `N` experiencias.

La afirmación del programa: existe un historial `H` tal que `E(A_H,F) < E(A_∅,F)`
o `P(A_H,F) > P(A_∅,F)`, **a igual `K`**. No es «la memoria ayuda».

---

## 2. Los cinco canales

Toda explicación de «la experiencia mejora al agente» pasa por uno de estos cinco
canales. Confundirlos produjo nuestros resultados ambiguos.

| Canal | Qué transporta | Predicción característica |
|---|---|---|
| **Información** | Episodios, ejemplos, documentos | El efecto desaparece si el clon recibe la misma información |
| **Representación** | Conceptos, vocabulario, relaciones | Transfiere a otra superficie sin traducción humana |
| **Política** | Qué buscar, cuándo parar, qué activar | Mejora el coste, no la cobertura |
| **Herramientas** | Procedimientos compilados y verificados | Amplía lo que el agente puede hacer con el mismo presupuesto |
| **Parámetros** | Pesos del modelo | No transferible entre modelos sin reentrenar |

Nuestros seis prototipos tocaron, como mucho, **política** (006) y **herramientas**
(003–005), siempre en el mismo universo. Información, representación y parámetros
siguen sin probar.

---

## 3. La proposición del espacio enumerable

Esta es la pieza que faltaba y la que explica los círculos.

> Sea `O` un conjunto finito de operadores, `L` una profundidad máxima y `B` un
> presupuesto. Si el solucionador enumera todos los programas de longitud `≤ L`
> sobre `O` dentro de `B`, su cobertura sobre cualquier distribución generada por
> programas de longitud `≤ L` es **1 por construcción**. En ese régimen ninguna
> memoria puede aumentar la cobertura; solo reordenar la búsqueda y reducir coste.

**Comprobación:** `|O| = 4`, `L = 3`, presupuesto 120 pasos. El espacio son
`4 + 16 + 64 = 84` programas. Se enumeran todos. Por eso `A1-nolearn-d3` acierta
**64/64** sin historial.

**Corolario 1.** El «100 % en D3» del 003 no era capacidad del agente: era el
experimentador bajándole la profundidad a 2 por decreto.

**Corolario 2.** Los negativos de 004, 005 y 006 son **predicciones de la teoría**,
no sorpresas. En espacio enumerable, la memoria solo puede optimizar coste. Y lo
hizo: 41,8 % menos pasos con igual cobertura, solo bajo continuidad.

**Corolario 3.** Para probar expansión hay que salir del régimen enumerable. Con
`|O| = 6` y `L = 6` son 55.986 programas; con 500 pasos se enumera < 1 %. Ahí una
herramienta compilada de longitud 3, usada como un paso, alcanza profundidad 6
dentro del presupuesto. **Esa es la predicción que distingue memoria de búsqueda.**

---

## 4. Las siete capacidades

Un fallo puede venir de siete sitios. Hasta ahora los tratamos como uno.

| Capacidad | Pregunta | Prueba mínima | Estado |
|---|---|---|---|
| **Inferencia** | ¿Identifica un programa compatible? | Tareas con solución única | Parcial (46,9 % base) |
| **Desambiguación** | ¿Reconoce varias hipótesis vivas? | ≥2 programas compatibles con consultas divergentes | **Sin medir** |
| **Experimentación** | ¿Sabe qué ejemplo pedir? | Ejemplos aleatorios vs informativos | **Sin medir** |
| **Ejecución** | ¿Aplica bien una hipótesis dada? | Dar el programa y pedir la salida | **Sin medir** |
| **Verificación** | ¿Rechaza una hipótesis falsa? | Inyectar contraejemplo | **Sin medir** |
| **Memoria** | ¿Usa experiencia sin conocer la respuesta? | `ACTUAL-RETRIEVAL` vs clon | **Sin medir** |
| **Generalización** | ¿Transfiere a otra estructura? | Familia reservada, vocabulario distinto | **Sin medir** |

**Regla:** ningún resultado sobre «el agente» sin decir en cuál de las siete se
mide. La frase «el cuello es identificar la transformación» se retiró porque
infería una capacidad desde un piloto que no las separaba.

---

## 5. Los cinco confundidores que ya nos invalidaron algo

| # | Confundidor | Dónde ocurrió | Cómo se evita |
|---|---|---|---|
| 1 | **Fuga de la respuesta** | 001 (nombre de la regla); 006-B `retrieved` (programa verdadero) | Etiquetar `ORACLE-*`; recuperador ciego a la solución |
| 2 | **Confusor de profundidad** | 005 (`NOLEARN` d3 vs memoria d2) | Igualar presupuesto y declarar la expresividad |
| 3 | **Muestra sesgada** | 006-B (`[:24]` = 16 `sort_asc` + 8 `sort_desc`) | Estratificar por clase conductual |
| 4 | **Integración fallida** | 006-B `tool` (permisos, scripts no creados) | Verificar cinco etapas por tarea |
| 5 | **Clases correlacionadas** | 004/005 (64 sintaxis, 14 comportamientos sobre 40 sondas) | Reportar por clase; no tratar instancias como independientes |

Sexto, metodológico: **inferir de un piloto con IC que cruza cero**. Ausencia de
significación no es ausencia de efecto.

---

## 6. Los cinco rivales

| Rival | Tesis | Predicción | Estado |
|---|---|---|---|
| **R1 Escala** | «No falta memoria: falta buscar más» | Igualado el presupuesto, el historial no aporta | **Apoyada** en régimen enumerable (004, 006-A′) |
| **R2 Información** | «La memoria es más contexto» | Memoria ≈ más ejemplos | **Insinuada** (006-B, confundida) |
| **R3 Ejecución** | «Sabe qué hacer y lo hace mal» | Un intérprete fiable sube el acierto | **Sin probar**: la condición tenía errores |
| **R4 Representación** | «Le falta vocabulario» | Nombrar operadores sube el acierto | **Débil** (+4,2 pp, IC cruza cero) |
| **R5 Metaprendizaje** | «Mejora la velocidad de adquisición» | `E(F)` decreciente | **Sin medir**: la única que responde la pregunta |

---

## 7. Nuestra hipótesis y sus predicciones

**H.** La historia reduce `E(F)` a igual `K` mediante **herramientas verificadas** y
**políticas de activación**, no mediante información adicional.

| ID | Predicción | Se refuta si |
|---|---|---|
| **P1** | Fuera del régimen enumerable, una herramienta compilada amplía la cobertura a igual presupuesto | La cobertura no sube, o sube también sin historial |
| **P2** | A igual información, un procedimiento verificado bate a un episodio recuperado | Empatan |
| **P3** | `E(F)` baja tras `N` familias solo si comparten **estructura**, no vocabulario | Baja con vocabulario compartido y estructura distinta |
| **P4** | El efecto desaparece cuando el clon recibe los mismos ejemplos | Persiste sin información adicional |
| **P5** | El efecto sobrevive a un cambio de modelo | Desaparece al cambiar de LLM |

**P1 es la prueba de fuego.** Si falla, se cierra la línea de expansión y queda solo
la de eficiencia, ya medida y modesta.

---

## 8. Qué significa «concepto»

No es una etiqueta comprimida. Es una estructura que cambia lo que el agente puede
inferir. Cuatro condiciones:

1. **Relación:** identifica qué conecta los casos, no cómo se llaman.
2. **Predicción:** acierta casos que no estaban en la experiencia.
3. **Contraejemplo:** reconoce uno y revisa la relación.
4. **Transferencia:** funciona con otra manifestación superficial **sin** traducción
   humana.

La cuarta separa concepto de invariancia léxica. Cambiar `alpha` por `gamma` no es
conceptualizar; cambiar listas por cadenas conservando la relación, sí.

---

## 9. Lo que el campo ya demostró

De la revisión estructurada de 31 trabajos (`../resources/investigation/revision-sistematica/`):

1. **La verificación independiente es imprescindible.** Proof-Gated: **538**
   aserciones de verificación de teachers, **52** confirmadas por ejecución, **486**
   fabricaciones rechazadas. JANUS no es nuevo.
2. **Las bibliotecas de skills degradan al crecer.** *Skill shadowing*: hasta
   **−21 %** con 202 skills.
3. **Entregar no es usar.** MemUse: 8.000 episodios, resolve **±0,4 pp** del
   baseline sin memoria; **23,2 %** de los usos beneficiosos igual fallaron.
4. **El coste del contexto está medido.** STRATUM: **~4 GB de texto frente a ~298 TB
   de estado KV** por 1e9 tokens en un 70B.
5. **Existen benchmarks de transferencia de procedimientos.** EvoAgentBench (4
   dominios, ability graphs) y SelfImprove-Bench (capacidad vs ajuste).

Nuestros negativos coinciden con los del campo. El hueco no es un mecanismo: es una
medición longitudinal con clon, canales separados y coste total.

---

## 10. Estado de la evidencia

| Afirmación | Nivel | Estado |
|---|---|---|
| En espacio enumerable, la memoria no amplía cobertura | E0 + 004/006 | Sostenida |
| La biblioteca de macros reduce coste con continuidad | E2 local | Sostenida (41,8 %) |
| La política aprendida no supera una regla simple | E2 local | Nuestra hipótesis, refutada |
| La memoria recuperada ayuda a un LLM | — | **Sin evidencia** (oráculo) |
| Un intérprete fiable ayuda | — | **Sin evidencia** (condición inválida) |
| La historia reduce `E(F)` en familias nuevas | — | **Sin medir** |
| Transferencia entre modelos | — | **Sin medir** |

Ninguna alcanza E3 (varias distribuciones) ni E4 (reproducción con tareas reales).

---

## 11. Qué cambiaría de opinión

- Si en universo no enumerable el historial no amplía cobertura (P1 falsa), la
  expansión muere y queda la eficiencia.
- Si `ACTUAL-RETRIEVAL` iguala al clon pero `ORACLE-MEMORY` gana, el problema es el
  recuperador.
- Si `E(F)` no baja en familias reservadas (P3 falsa), no hay metaprendizaje.
- Si el efecto desaparece al cambiar de modelo (P5 falsa), CUMULUS no tiene objeto.

---

## 12. Lo que este documento no es

No es una arquitectura. No es una revisión de literatura
(`../resources/investigation/revision-sistematica/`). No es un plan (`plan.md`). Es la afirmación que el plan
debe poner a prueba, con sus canales, rivales y falsadores.

