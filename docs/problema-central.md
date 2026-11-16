# El problema central

**Fecha:** 16 de noviembre de 2026
**Estado:** análisis previo. No implementa nada. Existe para decidir qué se
construye y, sobre todo, qué no.

---

## 0. La pregunta

> Si mañana este agente reinicia su contexto, cambia de tarea y encuentra un
> problema que nunca ha visto, ¿qué aprendizaje adquirido en sus experiencias
> anteriores modifica realmente su manera de comprenderlo y resolverlo?

Hoy **no podemos responderla con un experimento**. Este documento explica por qué,
qué haría falta para responderla y qué hemos estado midiendo en su lugar.

---

## 1. El fenómeno, y lo que no es

El objeto del programa no es la memoria. Es la **transformación de la competencia
por la experiencia**. La memoria es un instrumento; el procedimiento, otro; la
política, otro.

Cuatro cosas distintas que hemos confundido:

| Verbo | Qué cambia | Cómo se falsea |
|---|---|---|
| **Recordar** | La información disponible | El agente recupera el episodio y no mejora |
| **Usar** | La decisión, dado el recuerdo | El recuerdo se entrega y el agente lo ignora |
| **Adquirir** | Una competencia nueva | Un clon sin historial la adquiere igual de rápido |
| **Aprender a adquirir** | La velocidad de adquisición | El clon necesita las mismas experiencias |

El 006 mostró que entregar y usar son cosas distintas: la herramienta estaba
disponible y el agente no la usó hasta que se le exigió. El 006-A' mostró que un
recuerdo puede estar disponible y no mejorar la decisión.

---

## 2. Por qué el universo de cuatro operaciones

**Qué representa bien:** inducción exacta de programas, ambigüedad por equivalencia
observacional, coste de búsqueda, compilación de subrutinas, contabilidad de
cómputo. Es barato, determinista y enumerable; permite aislar variables.

**Qué excluye, y es lo que importa:**

- **Escala:** 4 primitivas y profundidad 3 dan 64 sintaxis y 14 comportamientos.
  No hay espacio para que una abstracción cambie el régimen de búsqueda.
- **Vocabulario abierto:** el lenguaje de operaciones está dado. El agente no puede
  inventar un operador elemental.
- **Ambigüedad genuina:** la consulta resuelve la ambigüedad por casualidad; no hay
  un paso de «pedir más evidencia».
- **Herramientas:** no hay ejecución, verificación ni coste de integración.
- **Dominios:** todo es listas de enteros. La transferencia entre dominios es
  imposible por construcción.
- **Coste de adquisición:** no se paga por observar, etiquetar ni verificar.
- **Deriva:** la distribución cambia solo porque la cambiamos nosotros.

**Conclusión:** el universo de cuatro operaciones fue un andamio para aprender a
medir. No es el fenómeno. Seguir optimizándolo es optimizar el andamio.

---

## 3. Las siete capacidades

El fallo del agente en una tarea puede venir de siete sitios distintos. Hasta ahora
los hemos tratado como uno.

| Capacidad | Pregunta | Prueba mínima | Estado |
|---|---|---|---|
| **Inferencia** | ¿Identifica un programa compatible? | Precisión en tareas con solución única | Parcial (46,9 % base) |
| **Desambiguación** | ¿Reconoce que hay varias hipótesis vivas? | Tareas con ≥2 programas compatibles y consultas que divergen | **Sin medir** |
| **Experimentación** | ¿Sabe qué ejemplo pedir para discriminar? | Comparar ejemplos aleatorios vs elegidos por información | **Sin medir** |
| **Ejecución** | ¿Aplica bien una hipótesis ya identificada? | Dar el programa y pedir la salida | **Sin medir** |
| **Verificación** | ¿Rechaza una hipótesis falsa? | Inyectar un contraejemplo y observar el cambio | **Sin medir** |
| **Memoria** | ¿Usa experiencia pertinente sin conocer la respuesta? | `ACTUAL-RETRIEVAL` vs clon | **Sin medir** |
| **Generalización** | ¿Transfiere a otra estructura? | Familia reservada con vocabulario distinto | **Sin medir** |

**Regla:** ningún resultado sobre «el agente» puede publicarse sin decir en cuál de
las siete se está midiendo. La frase «el cuello es identificar la transformación»
se retiró porque infería una capacidad desde un piloto que no las separaba.

---

## 4. Los cinco confundidores que ya nos invalidaron algo

| # | Confundidor | Dónde ocurrió | Cómo se evita |
|---|---|---|---|
| 1 | **Fuga de la respuesta** | 001 (nombre de la regla), 006-B `retrieved` (programa verdadero) | Etiquetar `ORACLE-*`; recuperador que solo ve la observación |
| 2 | **Confusor de profundidad** | 005 (`NOLEARN` d3 vs memoria d2) | Igualar presupuesto y reportar la expresividad como variable |
| 3 | **Muestra sesgada** | 006-B (`[:24]` = 16 `sort_asc` + 8 `sort_desc`) | Estratificar por clase conductual |
| 4 | **Integración fallida** | 006-B `tool` (permisos, scripts no creados) | Registrar las cinco etapas por tarea |
| 5 | **Clases correlacionadas** | 004/005 (64 sintaxis, 14 comportamientos) | Reportar por clase, no por fila; no tratar instancias como independientes |

Añadiría un sexto, metodológico: **inferir de un piloto con IC que cruza cero**. La
ausencia de significación no es evidencia de ausencia de efecto.

---

## 5. Qué contaría como evidencia, por nivel

### Memoria

**Afirmación:** el historial cambia una decisión futura.

**Diseño:** `ACTUAL-RETRIEVAL` (recuperador ciego a la solución) vs clon, en tareas
reservadas y pareadas.

**Se refuta si:** el clon empata. Y si el oráculo tampoco mejora, el problema no es
la recuperación: es que el agente no usa lo que se le da.

### Procedimiento

**Afirmación:** un artefacto reutilizable reduce el coste con igual éxito.

**Diseño:** mismo solucionador, mismo presupuesto, con y sin el artefacto.

**Se refuta si:** el artefacto no reduce pasos, o reduce pasos perdiendo cobertura
sin que el ahorro compense.

**Ya medido:** el 004-A lo refutó para macros de dos pasos en un universo finito.

### Concepto

**Afirmación:** el agente adquiere una representación que cambia lo que puede
inferir, no solo las palabras con que lo describe.

**Criterio reforzado** (el anterior era demasiado débil):

1. Identifica una **relación** entre casos, no una etiqueta.
2. **Predice** casos nuevos que no estaban en la experiencia.
3. **Reconoce contraejemplos** y revisa la relación.
4. **Transfiere** a un contexto con manifestación superficial distinta y sin
   traducción humana.

**Se refuta si:** solo hay invariancia léxica (cambiar nombres), o si la
transferencia exige que un humano traduzca la estructura.

### Metaprendizaje

**Afirmación:** después de `N` familias, la familia `N+1` se adquiere con menos
experiencias que un clon.

**Diseño:** currículo interdependiente, familias reservadas, `E(F)` = experiencias
hasta umbral.

**Se refuta si:** `E(F)` no baja, o baja porque la familia `N+1` comparte vocabulario
con las anteriores.

---

## 6. El currículo interdependiente: principios

Sin esto, el 007 vuelve a medir un universo plano.

1. **Estructura compartida, superficie distinta.** La misma relación aparece como
   listas, luego como cadenas, luego como registros con clave. Si el agente solo
   funciona en la primera, no hay concepto.
2. **Dependencia real.** Una tarea posterior **requiere** un artefacto que solo se
   puede obtener resolviendo una anterior. No basta con que se parezcan.
3. **Familias reservadas.** Ninguna familia de evaluación interviene en el diseño
   del mecanismo.
4. **Deriva controlada.** En algún punto, un artefacto aprendido deja de ser válido.
   Se mide si el agente lo detecta y lo retira.
5. **Coste de adquisición explícito.** Observar, verificar y consolidar cuestan.
   Se reportan por separado.
6. **Tres métricas separadas**, nunca una sola:
   - `E(F)`: experiencias hasta el umbral.
   - `K(F)`: cómputo y tokens hasta el umbral.
   - `P(F)`: desempeño en tareas reservadas tras `N` experiencias.

No se agregan en un escalar hasta que un escenario fije los precios.

---

## 7. La escalera, con puertas

| Etapa | Pregunta | Entregable | Puerta para pasar |
|---|---|---|---|
| **007A** | ¿De qué capacidad viene el fallo? | Descomposición en las 7 capacidades, muestra equilibrada, sin memoria | Se identifica al menos una capacidad con efecto distinguishable |
| **007B** | ¿La recuperación autónoma ayuda? | `ACTUAL-RETRIEVAL` vs `ORACLE-MEMORY` vs clon | El recuperador supera al clon con IC que excluye cero |
| **007C** | ¿Se aprende a aprender? | Currículo interdependiente, `E(F)` en familia reservada | `E(F)` del agente < `E(F)` del clon |
| **007D** | ¿Sobrevive la deriva? | Cambio de reglas a mitad de currículo | El agente retira el artefacto obsoleto sin perder los válidos |

**No se salta de 007A a 007C.** Sin la descomposición, cualquier resultado de 007C
es ambiguo.

---

## 8. Lo que no se implementará hasta que exista evidencia

- Otra biblioteca de macros.
- Otra política de activación.
- Un controlador con más acciones.
- SIR, Canon o JANUS-C operativos.
- Una capa social.

**Motivo:** cada uno de esos módulos añade coste y preguntas metodológicas, y
ninguno ha producido todavía una ventaja que sobreviva a un control.

---

## 9. Lo que la neurociencia y las ciencias sociales aportaron

Hay que decirlo sin adornos: **hasta ahora, vocabulario y analogías, no hipótesis
comprobables**. Sirvieron para elegir qué mirar (consolidación, olvido,
interferencia, memoria colectiva), no para derivar un mecanismo que hayamos probado.

Eso no invalida la inspiración, pero impide presentarla como fundamento. La única
hipótesis de origen biológico que el programa puede formular con precisión es:

> La consolidación compila episodios en artefactos estables, y ese artefacto debe
> seguir siendo útil sin el episodio original.

Es comprobable. No está comprobada.

---

## 10. Lo que hay que dejar de hacer

- Llamar «techo» a una línea base de un modelo barato.
- Llamar «memoria» a información seleccionada con la respuesta.
- Llamar «concepto» a cambiar nombres.
- Llamar «aprendizaje» a mejorar un benchmark una vez.
- Llamar «refutado» a un intervalo que cruza cero.
- Optimizar el instrumento y llamarlo progreso.

---

## 11. La regla que queda

Antes de escribir una línea de código, responder por escrito:

1. ¿Qué capacidad de las siete estoy midiendo?
2. ¿Qué información privilegiada entra en la condición y cómo la etiqueto?
3. ¿Qué comparación podría demostrar que **no** hay efecto?
4. ¿Qué métrica (`E`, `K` o `P`) decide, y cuál es el umbral?
5. ¿Qué abandonaría si sale negativo?

Si alguna respuesta es «ya veremos», el experimento no está listo.
