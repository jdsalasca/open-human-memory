# Teoría y marco

**Fecha:** 16 de noviembre de 2026
**Estado:** documento central. Absorbe `problema-central.md` y la parte teórica de
`revision-de-rumbo.md`. Si algo contradice este documento, se corrige lo otro.

---

## 0. La pregunta

> Si mañana este agente reinicia su contexto, cambia de tarea y encuentra un
> problema que nunca ha visto, ¿qué aprendizaje adquirido en sus experiencias
> anteriores modifica realmente su manera de comprenderlo y resolverlo?

Hoy podemos responderla **en parte**. En tareas que el modelo no puede aplicar, no hay
evidencia: el 007 pedía cinco operaciones y el oráculo mismo acertaba 2/12. En una
tarea de **dos operaciones efectivas**, un artefacto verificado y presentado como
conocimiento aplicable se usa (10–11/12 frente a 3–5/12 del clon), pero eso es **uso de
memoria**, no expansión de competencia: la tarea es enumerable y la memoria ahorra
identificarla. La expansión sigue sin medirse. Este documento explica qué se afirma,
por qué canales, qué lo refutaría y por qué los experimentos anteriores no podían
responderla.

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

**Qué es un clon.** Mismo modelo, mismas herramientas iniciales, mismo presupuesto y
la misma información de la tarea actual. La única diferencia es el historial. Si la
intervención recibe artefactos derivados del historial, el clon debe recibir el
mismo coste de adquisición o declararse que se mide el **paquete completo**, no el
mecanismo de memoria.

---

## 2. Los cinco canales

Toda explicación de «la experiencia mejora al agente» pasa por uno de estos cinco
canales. Confundirlos produjo nuestros resultados ambiguos.

| Canal | Qué transporta | Predicción característica |
|---|---|---|
| **Información** | Episodios, ejemplos, documentos | El efecto desaparece si el clon recibe la misma información |
| **Representación** | Conceptos, vocabulario, relaciones | Transfiere a otra superficie sin traducción humana |
| **Política** | Qué buscar, cuándo parar, qué activar | Puede cambiar coste y, bajo presupuesto fijo, la cobertura alcanzable |
| **Herramientas** | Procedimientos compilados y verificados | Amplía lo que el agente puede hacer con el mismo presupuesto |
| **Parámetros** | Pesos del modelo | No transferible entre modelos sin reentrenar |

Nuestros experimentos tocaron, como mucho, **política** (006) y **herramientas**
(003–005), siempre en el mismo universo. El 007/MEM añadió **retención y uso** de un
procedimiento verificado en 2 operaciones; LIRE-002 probó **representación** como
coste/fidelidad, no como expansión. Información y parámetros siguen sin probar.

**No son una descomposición causal identificada.** Los canales se solapan: una
herramienta contiene información, cambia la representación y puede modificar la
política. Sin una regla operacional para asignar efectos, sirven para diseñar
condiciones, no para atribuir causas.

**Línea LIRE (ejecutada, negativa).** El canal de representación se estudió en
`../resources/investigation/lire-001/`: la misma regla de cuatro ramas en español,
inglés, chino, español conciso y DSL simbólico, con **tokens reales** del modelo.
Las prosas conservaron 8/8; el DSL falló 1/8. El chino usó 64 % menos caracteres y
**+2 tokens** de mediana. Los caracteres no predicen los tokens. No se demostró
ahorro; se demostró que la escala del arnés domina.

---

## 3. La proposición del espacio explorable

> Sea `O` finito, `L` una profundidad y `B` un presupuesto. Si el solucionador
> enumera todos los programas de longitud `≤ L` dentro de `B` **y la tarea es
> identificable** —todas las hipótesis compatibles con los ejemplos coinciden en la
> consulta—, su cobertura es **1 por construcción**. En ese régimen la memoria no
> puede aumentar la cobertura; solo reordenar la búsqueda y reducir coste.

**La identificabilidad no es un detalle.** Enumerar candidatos no garantiza
acertar la consulta: si dos programas compatibles divergen en ella, el solucionador
devuelve el primero y puede fallar. Ejemplo mínimo: con entradas constantes,
`sort_asc` y `sort_desc` son indistinguibles; la consulta las separa. Nuestro
propio 006-A lo muestra: con presupuesto de 120 pasos, el conjunto mixto rinde
**83,3 %**, no 100 %. El 64/64 del 004-A se obtuvo **sin** ese presupuesto.

**Segunda precisión: candidatos no es coste.** `4 + 16 + 64 = 84` programas no son
84 pasos: cada candidato se comprueba contra tres ejemplos y puede costar hasta
nueve aplicaciones. Bajo 120 pasos el espacio puede no recorrerse entero. La
proposición vale para el espacio **explorado**, no para el espacio **enumerado**.

**Tercera precisión: el término.** No es un «universo no enumerable». Es un espacio
**no explorable exhaustivamente bajo el presupuesto**. Con `|O| = 6` y `L = 6` son
55.986 programas: siguen siendo finitos; lo que cambia es que no caben en `B`.

**Corolario 1.** El «100 % en D3» del 003 no era capacidad del agente: era el
experimentador bajándole la profundidad a 2 por decreto, en tres programas
identificables.

**Corolario 2.** Los negativos de 004, 005 y 006 son predicciones de la teoría
**solo en el régimen identificable y presupuestado**. Fuera de él, la teoría no
dice nada; no se puede usar para cerrar la línea.

**Corolario 3.** Para probar expansión basta con que el espacio no quepa en `B`:
una tarea **identificable** cuya solución aparezca después del corte puede
resolverse con una herramienta que la mueva dentro del presupuesto. La ambigüedad
es un problema **adicional**, no una condición necesaria.

**Supuestos de realizabilidad.** La proposición asume que existe al menos un
programa correcto, que la enumeración alcanza la longitud pertinente, que los
operadores y el verificador son correctos, y que `B` incluye los costes que se
comparan. Bajo esos supuestos es una consecuencia de la definición, no una teoría
general de memoria. Con `executed_steps` medido, el exceso máximo observado es de
6 pasos sobre 120: el presupuesto es un corte antes del candidato, no un límite
estricto.

---

## 4. Las siete capacidades

Un fallo puede venir de siete sitios. Hasta ahora los tratamos como uno.

| Capacidad | Pregunta | Prueba mínima | Estado |
|---|---|---|---|
| **Inferencia** | ¿Identifica un programa compatible? | Tareas con solución única | Parcial: 2 ops, clon 3–5/12 (MEM-002/004) |
| **Desambiguación** | ¿Reconoce varias hipótesis vivas? | ≥2 programas compatibles con consultas divergentes | **Sin medir** |
| **Experimentación** | ¿Sabe qué ejemplo pedir? | Ejemplos aleatorios vs informativos | **Sin medir** |
| **Ejecución** | ¿Aplica bien una hipótesis dada? | Dar el programa y pedir la salida | Parcial: 2 ops 86 %, 3 ops 44 %, 5 ops 0–33 % (EXEC-001) |
| **Verificación** | ¿Rechaza una hipótesis falsa? | Inyectar contraejemplo | Parcial/negativa: aplica un placebo verificado (0/12) en vez de rechazarlo (MEM-004) |
| **Memoria** | ¿Usa experiencia sin conocer la respuesta? | `ACTUAL-RETRIEVAL` vs clon | Parcial: retención/uso verificado 10–11/12 vs clon 3–5/12 en 2 ops; no es recuperación (MEM-003/004) |
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

**H.** La historia puede actuar por **cualquiera de los cinco canales**. El programa
no declara un ganador de antemano: mide cuál reduce `E(F)` a igual `K` en cada
familia, y en qué forma. Excluir la representación o los conceptos antes de medirlos
sería convertir una hipótesis de implementación en un límite de la investigación.

| ID | Predicción | Se refuta si |
|---|---|---|
| **P1** | En un espacio no explorable bajo `B`, una herramienta compilada amplía la cobertura a igual presupuesto | La cobertura no sube, o sube también sin historial |
| **P2** | A igual información, un procedimiento verificado bate a un episodio recuperado | Empatan |
| **P3** | La ventaja de adquisición es mayor cuando las familias comparten **estructura** que cuando solo comparten vocabulario | La ventaja es igual o mayor con vocabulario compartido y estructura distinta |
| **P4** | **Discriminante:** si la ventaja es informacional, dar los mismos ejemplos al clon la elimina; si es de herramienta o política, **persiste** | Persiste con la misma información y no hay herramienta ni política distinta |
| **P5** | El efecto sobrevive a un cambio de modelo | Desaparece al cambiar de LLM |
| **P6** | Elegir la **forma** del conocimiento (episodio, procedimiento, herramienta, concepto) según utilidad futura bate a cualquier forma fija a igual coste | Una forma fija iguala o supera a la selección |

**P6 es la hipótesis nueva del programa** y se desarrolla en el §7.1.

### 7.1 Las tres comparaciones que separan canales

| Comparación | Qué identifica |
|---|---|
| Misma información, distinto historial de aprendizaje | Efecto de capacidades o políticas adquiridas |
| Mismo solucionador, distinta información disponible | Efecto de evidencia adicional |
| Misma información y herramientas, distinta política | Efecto de aprender a seleccionar acciones |

Ninguna resuelve toda la identificación —aprender cambia cómo se interpreta la
información—, pero evitan predicciones que contradicen el mecanismo declarado.

### 7.2 La forma del conocimiento

Un agente que conserva todo como episodio paga contexto; uno que conserva todo como
procedimiento pierde los casos que el procedimiento no cubre; uno que conserva todo
como herramienta paga verificación y mantenimiento. La pregunta no es «qué forma es
mejor», sino **qué forma asignar a cada experiencia**.

Eso es un problema de **selección de representación**, no de almacenamiento:

- mismas experiencias, cuatro formas posibles;
- misma información disponible para el clon;
- mismo presupuesto de contexto y cómputo;
- métrica: `E(F)`, `K(F)` y `P(F)` por separado;
- cota superior: un oráculo que conoce la forma óptima por tarea.

Si la selección aprendida se acerca al oráculo y supera a toda forma fija, hay una
contribución. Si no, **ese resultado no respalda la ventaja del selector**; las
formas todavía podrían diferir entre tareas.

**Advertencia de identificación.** Las cuatro formas no conservan la misma
información: una herramienta ejecutable incorpora el resultado de su verificación;
un concepto puede ser una abstracción inferida que no estaba literal en las
experiencias. Por eso se separan dos preguntas:

- **Representación:** dada una competencia ya conocida, ¿qué forma la conserva con
  mayor fidelidad, menor coste y mejor transferencia? Esto mide P6.
- **Adquisición:** dadas experiencias, ¿qué mecanismo descubre conocimiento nuevo?
  Eso es P1–P3, no P6.

No se presenta P6 como evidencia de aprendizaje: mide cómo se conserva, no cómo se
descubre.

### 7.3 Regla de cierre

Un resultado negativo cierra **la afirmación específica contrastada**, no el
fenómeno general. Si P1 falla en un espacio de seis operadores, queda refutado ese
mecanismo en esa familia con esos recursos. La línea de aprendizaje acumulativo
sigue abierta hasta que fallen las seis predicciones en varias familias.

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

1. **La verificación operacional es imprescindible y ya existe.** Proof-Gated:
   **538** aserciones de verificación de teachers, **52** confirmadas por ejecución,
   **486** fabricaciones rechazadas. Eso desafía el componente de **verificación**
   de JANUS; **no** resuelve su pretensión de **identificación causal**, que es otro
   problema.
2. **Las bibliotecas de skills degradan al crecer.** *Skill shadowing*: hasta
   **−21 %** con 202 skills.
3. **Entregar no es usar.** MemUse: 8.000 episodios, resolve **±0,4 pp** del
   baseline sin memoria; **23,2 %** de los usos beneficiosos igual fallaron.
4. **El coste del contexto está estimado, no medido en producción.** STRATUM
   calcula el coste **hipotético** de representar mil millones de tokens como estado
   KV (**~298 TB**) frente a texto (**~4 GB**). No demuestra que un sistema real
   mantenga ese contexto activo. La afirmación válida: el conocimiento externo
   puede ser mucho más barato en almacenamiento. Que preserve la capacidad de
   decidir con menor coste total sigue sin demostrarse.
5. **Existen benchmarks de transferencia de procedimientos.** EvoAgentBench (4
   dominios, ability graphs) y SelfImprove-Bench (capacidad vs ajuste).
6. **Los estudios no son intercambiables.** SkillsBench mide skills curadas;
   MemUse, memoria episódica en código; ContinualSkillBench, un flujo con
   biblioteca. Sus resultados no se refutan entre sí: responden a condiciones
   distintas. La pregunta correcta es condicional —qué conocimiento, qué agente,
   qué presupuesto—, no un agregado.

Nuestros negativos coinciden con los del campo. El hueco no es un mecanismo: es una
medición longitudinal con clon, canales separados y coste total. Pero el hueco se
estrecha: EvoAgentBench y SelfImprove-Bench ya miden partes de la pregunta.

---

## 10. Estado de la evidencia

| Afirmación | Nivel | Estado |
|---|---|---|
| En espacio enumerable, la memoria no amplía cobertura | E0 + 004/006 | Sostenida |
| La biblioteca de macros reduce coste con continuidad | E2 local | Sostenida (41,8 %) |
| La política aprendida no supera una regla simple | E2 local | Nuestra hipótesis, refutada |
| La aplicación con el programa dado cae con la longitud efectiva | E2 local | Sostenida: 2 ops 86 %, 3 ops 44 %, 5 ops 0–33 % (EXEC-001) |
| La memoria verificada se usa en 2 operaciones | E2 local | Sostenida local: 10–11/12 vs 3–5/12 del clon (MEM-003/004) |
| El encuadre de candidata reduce el uso | E2 local | Sostenida local: 4/12 vs 11/12 (MEM-003) |
| La etiqueta «verificado» basta sin contenido | E2 local | **Refutada**: placebo verificado 0/12 (MEM-004) |
| Con información independiente, la recuperación funciona y falla la condición | E2 local | Sostenida local: 6–7/7 positivos, 2–5/5 secundarios (LIRE-002) |
| El chino conserva mejor la información | E2 local | **Refutada**: no ahorra tokens ni acierta más (LIRE-002) |
| La memoria recuperada ayuda a un LLM | — | **Sin evidencia** (oráculo; no es `ACTUAL-RETRIEVAL`) |
| Un intérprete fiable ayuda | — | **Sin evidencia** (condición inválida) |
| La historia reduce `E(F)` en familias nuevas | — | **Sin medir** |
| Transferencia entre modelos | — | **Sin medir** |
| Expansión de competencia | — | **Sin evidencia** |

Ninguna alcanza E3 (varias distribuciones) ni E4 (reproducción con tareas reales).

**El resultado positivo no contradice la proposición.** En MEM-003/004 la tarea es de
2 operaciones, enumerable e identificable; el artefacto verificado reduce el coste de
identificarla, no amplía la cobertura. La proposición predice exactamente eso: en el
espacio enumerable la memoria solo puede reordenar la búsqueda y reducir coste. Para
probar expansión hace falta una tarea **identificable pero no enumerable bajo el
presupuesto**, y que el modelo pueda **aplicar**. EXEC-001 muestra que la segunda
condición falla en 3–5 operaciones; por eso la expansión sigue sin medirse.

---

## 11. Qué cambiaría de opinión

- Si P1 falla en varias familias y espacios, ese mecanismo queda refutado; la
  pregunta general sigue abierta hasta que fallen P1–P6 en varias distribuciones.
- Si `ACTUAL-RETRIEVAL` iguala al clon pero `ORACLE-MEMORY` gana, el problema es el
  recuperador.
- Si `E(F)` no baja en familias reservadas (P3 falsa), no hay metaprendizaje.
- Si el efecto desaparece al cambiar de modelo (P5 falsa), CUMULUS no tiene objeto.

---

## 12. Lo que este documento no es

No es una arquitectura. No es una revisión de literatura
(`../resources/investigation/revision-sistematica/`). No es un plan (`plan.md`). Es la afirmación que el plan
debe poner a prueba, con sus canales, rivales y falsadores.





