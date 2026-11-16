# Teoría: qué estamos intentando explicar

**Fecha:** 16 de noviembre de 2026
**Estado:** documento central. Los demás documentos experimentales son
consecuencias o registros; este fija qué se afirma, por qué y qué lo refutaría.

---

## 1. El fenómeno

No estudiamos memoria. Estudiamos **expansión de competencia**: el cambio en la
capacidad futura de un agente atribuible a su historia.

La distinción es operativa, no retórica. Un agente puede recordar más y no ser más
competente; puede ejecutar mejor y no haber aprendido nada; puede acumular
procedimientos y no saber cuándo usarlos. El objeto es el cambio de capacidad, y la
memoria es uno de sus canales.

Formalmente, para una familia de tareas reservada `F`:

- `E(A,F)`: experiencias hasta alcanzar el umbral `θ`.
- `K(A,F)`: cómputo, tokens y coste de mantenimiento hasta `θ`.
- `P(A,F)`: desempeño tras `N` experiencias.

La afirmación del programa es: **existe un historial `H` tal que `E(A_H,F) <
E(A_∅,F)` o `P(A_H,F) > P(A_∅,F)`, a igual `K`.** No es «la memoria ayuda». Es una
comparación contra un clon sin historial, en una distribución declarada.

---

## 2. Los cinco canales por los que la historia puede cambiar la competencia

Toda explicación de «la experiencia mejora al agente» pasa por uno de estos cinco
canales. Confundirlos es lo que ha producido nuestros resultados ambiguos.

| Canal | Qué transporta | Predicción característica |
|---|---|---|
| **Información** | Episodios, ejemplos, documentos | El efecto desaparece si el clon recibe la misma información |
| **Representación** | Conceptos, vocabulario, relaciones | Transfiere a otra superficie sin traducción humana |
| **Política** | Qué buscar, cuándo parar, qué activar | Mejora el coste, no la cobertura |
| **Herramientas** | Procedimientos compilados y verificados | Amplía lo que el agente puede hacer con el mismo presupuesto |
| **Parámetros** | Pesos del modelo | No transferible entre modelos sin reentrenar |

Nuestros seis prototipos han tocado, como mucho, **política** (006) y
**herramientas** (003-005), y siempre en el mismo universo. Información,
representación y parámetros están sin probar.

---

## 3. El argumento central: por qué nuestros resultados negativos estaban cantados

Esta es la pieza que faltaba y la que explica los círculos.

**Proposición.** Sea `O` un conjunto finito de operadores, `L` una profundidad
máxima, y `B` un presupuesto de cómputo. Si el solucionador enumera todos los
programas de longitud `≤ L` sobre `O` dentro de `B`, entonces su cobertura sobre
cualquier distribución generada por programas de longitud `≤ L` es **1 por
construcción**. En ese régimen, ninguna memoria puede aumentar la cobertura; solo
puede reordenar la búsqueda y reducir su coste.

**Comprobación en nuestro universo:** `|O| = 4`, `L = 3`, presupuesto 120 pasos.
El espacio son `4 + 16 + 64 = 84` programas. El solucionador los enumera todos. Por
eso `A1-nolearn-d3` acierta **64/64** sin historial. No es un hallazgo empírico: es
una consecuencia del tamaño.

**Corolario 1.** El «100 % en D3» del Prototipo 003 no era una capacidad nueva. El
experimento había hecho el espacio no enumerable *para ese solucionador* bajándole
la profundidad a 2 por decreto. La capacidad era del experimentador, no del agente.

**Corolario 2.** Todos nuestros resultados negativos —004, 005, 006— son
**predicciones de la teoría**, no sorpresas. En un espacio enumerable, la memoria
solo puede ser una optimización de coste. Y lo fue: 41,8 % menos pasos con igual
cobertura, y solo bajo continuidad.

**Corolario 3.** Para probar expansión hay que salir del régimen enumerable. Con
`|O| = 6` y `L = 6`, el espacio son 55.986 programas; con un presupuesto de 500
pasos se enumera menos del 1 %. Ahí una herramienta compilada de longitud 3, usada
como un paso, alcanza profundidad 6 dentro del presupuesto. **Esa es la predicción
que sí distingue memoria de búsqueda.**

Esta proposición debería haber sido el primer documento del repositorio. Llegó
después de seis prototipos, y por eso los seis giraron en el mismo sitio.

---

## 3.5 Lo que el campo ya demostró

La revisión estructurada (`resources/investigation/revision-sistematica/`) cambia
el punto de partida. Cuatro resultados ajenos que debemos incorporar:

1. **La verificación independiente es imprescindible.** Proof-Gated (NeurIPS 2026
   workshop): 538 aserciones de verificación de modelos teacher, **52 confirmadas
   por ejecución, 486 fabricaciones rechazadas**. JANUS no es nuevo.
2. **Las bibliotecas de skills degradan al crecer.** *Skill shadowing*: hasta
   **−21 %** al pasar a 202 skills.
3. **Entregar no es usar.** MemUse: 8.000 episodios, resolve a **±0,4 pp** del
   baseline sin memoria; **23,2 %** de los usos beneficiosos igual fallaron.
4. **El coste del contexto está medido.** STRATUM: **~4 GB de texto frente a ~298 TB
   de estado KV** por 1e9 tokens en un modelo de 70B.

Esto no invalida la teoría de §3; la sitúa. Nuestros negativos son locales, pero
coinciden con los del campo. El hueco defendible no es un mecanismo: es una
medición longitudinal con clon, canales separados y coste total.

## 4. Las cinco explicaciones rivales

Ninguna de nuestras observaciones es única de nuestra hipótesis. Cada rival hace
una predicción distinta, y el experimento debe separarlas.

### R1. Escala y búsqueda

*«No hace falta memoria: hace falta buscar más.»*

Predice que, igualado el presupuesto, el historial no aporta nada. **Nuestros datos
la apoyan en el régimen enumerable**: 004 y 006-A′. No dice nada fuera de él.

### R2. Información

*«La memoria es solo más contexto.»*

Predice que una experiencia recuperada y tres ejemplos más producen el mismo
efecto. **El 006-B lo insinúa** (+8,3 pp ambos), pero la condición de memoria estaba
seleccionada por oráculo y la muestra, sesgada. Sigue abierta.

### R3. Ejecución

*«El agente sabe qué hacer y lo hace mal.»*

Predice que un intérprete fiable sube el acierto. **No la hemos probado**: la
condición de herramienta tenía errores de entorno en 16 de 24 trazas. Es la
explicación rival más barata de descartar y la que más nos falta.

### R4. Representación

*«Al agente le falta el vocabulario del problema.»*

Predice que nombrar los operadores sube el acierto. **Débil señal a favor**
(+4,2 pp, IC cruza cero). No la descartamos.

### R5. Metaprendizaje

*«La historia no mejora el desempeño; mejora la velocidad de adquisición.»*

Predice `E(F)` decreciente en familias reservadas. **Sin medir.** Es la única que
responde a la pregunta del proyecto, y la única que exige un currículo
interdependiente.

---

## 5. Nuestra hipótesis, con predicciones derivadas

**H.** La historia reduce `E(F)` a igual `K` mediante **herramientas verificadas**
(canal herramientas) y **políticas de activación** (canal política), no mediante
información adicional.

De H se derivan cinco predicciones. Ninguna se ha probado todavía.

| ID | Predicción | Se refuta si |
|---|---|---|
| **P1** | Fuera del régimen enumerable, una herramienta compilada amplía la cobertura a igual presupuesto | La cobertura no sube o sube también sin historial |
| **P2** | A igual información, un procedimiento verificado bate a un episodio recuperado | Empatan |
| **P3** | `E(F)` baja tras `N` familias solo si comparten **estructura**, no vocabulario | Baja también con familias de vocabulario compartido y estructura distinta |
| **P4** | El efecto desaparece cuando el clon recibe los mismos ejemplos | Persiste sin información adicional |
| **P5** | El efecto sobrevive a un cambio de modelo | Desaparece al cambiar de LLM |

**P1 es la prueba de fuego.** Si no se cumple, la línea de expansión se cierra y
solo queda la de eficiencia, que ya está medida y es modesta.

---

## 6. Qué significa «concepto» aquí

Un concepto no es una etiqueta comprimida. Es una estructura que cambia lo que el
agente puede inferir. Operacionalmente, cuatro condiciones:

1. **Relación:** identifica qué conecta los casos, no solo cómo se llaman.
2. **Predicción:** acierta casos que no estaban en la experiencia.
3. **Contraejemplo:** reconoce uno y revisa la relación.
4. **Transferencia:** funciona con otra manifestación superficial y sin traducción
   humana.

La condición 4 es la que separa concepto de invariancia léxica. Cambiar `alpha` por
`gamma` no es conceptualizar; cambiar listas por cadenas y conservar la relación,
sí.

---

## 7. Por qué el universo de cuatro operaciones no puede decidir

No fue un error elegirlo: fue un andamio barato para aprender a medir. El error fue
seguir en él después de que la teoría dijera que no podía decidir nada.

Lo que excluye:

- **Espacio no enumerable.** Sin él, no hay expansión posible (Proposición).
- **Vocabulario abierto.** El agente no puede introducir un operador.
- **Ambigüedad genuina.** No hay un paso de pedir evidencia.
- **Herramientas y verificación.** No hay ejecución ni coste de integración.
- **Dominios.** Todo son listas de enteros.
- **Coste de adquisición.** Observar y verificar son gratis.
- **Deriva.** La distribución cambia porque la cambiamos.

Un programa que quiera responder la pregunta del proyecto necesita, como mínimo, un
universo donde la solución **no quepa** en el presupuesto.

---

## 8. Estado de la evidencia

| Afirmación | Nivel | Estado |
|---|---|---|
| En espacio enumerable, la memoria no amplía cobertura | E0 (teoría) | Sostenida por 004 y 006-A′ |
| La biblioteca de macros reduce coste con continuidad | E2 (local) | Sostenida, 41,8 % |
| La política aprendida no supera una regla simple | E2 (local) | Refutada nuestra hipótesis |
| La memoria recuperada ayuda a un LLM | — | **Sin evidencia** (oráculo) |
| Un intérprete fiable ayuda | — | **Sin evidencia** (condición inválida) |
| La historia reduce `E(F)` en familias nuevas | — | **Sin medir** |
| Transferencia entre modelos | — | **Sin medir** |

Ninguna afirmación del programa alcanza E3 (varias distribuciones) ni E4
(reproducción independiente con tareas reales).

---

## 9. Lo que cambiaría de opinión

- Si en un universo no enumerable el historial no amplía cobertura (P1 falsa), la
  hipótesis de expansión muere y queda solo la de eficiencia.
- Si `ACTUAL-RETRIEVAL` iguala al clon pero `ORACLE-MEMORY` gana, el problema es el
  recuperador, no el mecanismo.
- Si `E(F)` no baja en familias reservadas (P3 falsa), no hay metaprendizaje y el
  programa se reduce a herramientas.
- Si el efecto desaparece al cambiar de modelo (P5 falsa), no hay portabilidad y
  CUMULUS no tiene objeto.

---

## 10. Lo que este documento no es

No es una arquitectura. No es una revisión de literatura (eso está en
`precedentes/10-matriz-de-antecedentes.md`). No es un plan (eso está en
`docs/plan.md`). Es la afirmación que el plan debe poner a prueba, con sus canales,
sus rivales y sus falsadores.
