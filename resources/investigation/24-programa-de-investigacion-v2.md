# 24 — Programa de investigación v2: de la memoria a la corrección

> **Superado por `28-programa-de-competencia.md`.** Se conserva como histórico:
> el foco pasa de memoria/corrección a **expansión de competencia**.

**Estado:** reemplaza la formulación centrada en CUMULUS/JANUS como arquitecturas.
La pregunta ya no es "¿cómo construimos otra memoria?", sino **"¿qué puede
justificar una trayectoria y cómo se usa ese conocimiento sin convertirlo en
certeza permanente?"**.

## 1. El cambio de pregunta

La investigación anterior preguntaba:

> ¿Cómo acumular experiencias y procedimientos durante meses?

Las dos revisiones obligan a preguntar algo más profundo:

> ¿Cómo puede la experiencia producir conocimiento cada vez más útil sin
> convertir los errores del pasado en certezas permanentes?

Eso desplaza el foco de la **arquitectura** a la **epistemología operacional**:
qué se guarda, qué se infiere, qué se puede afirmar, con qué confianza y cuándo
se debe abandonar.

## 2. Lo que aprendimos de las dos revisiones

1. **La inspiración biológica no justifica un mecanismo.** Hay que separar
   fenómeno (L1), traducción funcional (L2) y ventaja comparativa (L3).
2. **La novedad está sobreafirmada.** Zep Agent Skills, MSCE, Trace2Skill, AFTER,
   COUNTERMEM, ConMem, MemCon y otros ya cubren piezas centrales.
3. **La causalidad no es la única dimensión.** Fiabilidad, causalidad y
   portabilidad son propiedades distintas; una habilidad puede ser fiable sin
   explicación causal.
4. **La memoria puede empeorar al agente.** Error reproduction y anti-persistencia
   muestran que persistir abstracciones puede ser contraproducente.
5. **La incertidumbre es contenido, no ruido.** Un sistema maduro debe recordar
   lo que no sabe, lo que no comprobó y lo que sigue en disputa.
6. **La evaluación longitudinal es la prueba real.** Los benchmarks de
   transferencia no miden meses de deriva.

## 3. Definiciones operativas

### 3.1 Aprendizaje

- **Nivel modelo:** cambio de pesos. No ocurre aquí.
- **Nivel sistema:** cambio acumulativo en memoria, artefactos, políticas y
  enrutamiento. Es el nivel que estudiamos.
- **Nivel organización:** cambio en la coordinación de varios agentes.

**Definición:** hay aprendizaje acumulativo externo cuando la experiencia previa
produce una mejora reproducible en tareas futuras no observadas, bajo condiciones
controladas, que persiste tras reinicios de contexto y cambios de modelo.

### 3.2 Tipos de objeto epistémico

| Tipo | Qué es | Se puede afirmar | Se puede reutilizar |
|---|---|---|---|
| **Registro factual** | Evento observado con procedencia | Que ocurrió | Como evidencia, no como conclusión |
| **Interpretación** | Lectura provisional de un evento | Que el agente cree X | Solo marcada como provisional |
| **Procedimiento operacional** | Rutina que funciona bajo condiciones | Que funciona | Sí, con límites y fiabilidad |
| **Afirmación causal** | Efecto identificado bajo supuestos | Que A causa B en un alcance | Solo si la identificación se sostiene |
| **Incertidumbre** | Lo que no se sabe o no se comprobó | Que falta evidencia | Para decidir abstenerse o experimentar |
| **Pregunta abierta** | Hipótesis + experimento pendiente | Que está en investigación | Para agenda de experimentos |
| **Disenso** | Evidencia minoritaria o contradictoria | Que hay conflicto | Para evitar consenso falso |

**Regla:** ningún objeto sube de tipo sin evidencia del tipo correspondiente.

### 3.3 Tres dimensiones de validación

| Dimensión | Pregunta | Evidencia |
|---|---|---|
| **Fiabilidad** | ¿Funciona repetidamente? | Tasa de éxito, calibración, varianza |
| **Causalidad** | ¿Por qué funciona? | Intervención, contrafactual, identificación |
| **Portabilidad** | ¿Dónde más funciona? | Matriz entre modelos, dominios y condiciones |

Añadimos dos dimensiones de decisión:

- **Riesgo:** reversibilidad, blast radius, sensibilidad.
- **Costo:** tokens, tiempo, herramientas, verificación.

**Política:** una acción reversible y de bajo riesgo puede usar un procedimiento
fiable sin causalidad identificada. Una acción irreversible o de alto riesgo
exige causalidad y portabilidad, o abstención.

### 3.4 Utilidad de una memoria

\[
U(m,t) = P(\text{éxito} \mid t, m) - P(\text{éxito} \mid t, \varnothing)
\]

No es una propiedad intrínseca de \(m\): depende de la tarea, del lector, del
modelo, del formato y del costo. Una memoria puede ser verdadera y perjudicial.

## 4. Horizontes

### H0 — ¿Qué puede justificar una trayectoria?

**Pregunta:** ¿qué afirmaciones sobre el mundo, el agente o las causas se pueden
derivar de una traza, y con qué supuestos?

**Producto:** ontología de objetos epistémicos y reglas de inferencia.

**Criterio:** toda afirmación del sistema debe poder rastrearse a un tipo de
objeto y a su evidencia.

### H1 — ¿Qué hace valiosa a una memoria?

**Pregunta:** ¿cómo medir la contribución de una memoria a decisiones futuras?

**Producto:** métrica \(U(m,t)\), protocolo de medición con y sin memoria,
registro de costos.

**Criterio:** la utilidad se mide, no se supone; puede ser negativa.

### H2 — ¿Fiabilidad, causalidad o portabilidad?

**Pregunta:** ¿cómo se combinan tres dimensiones distintas sin exigir causalidad
para todo?

**Producto:** política de uso por riesgo y costo; Canon con etiquetas de
dimensión.

**Criterio:** una habilidad fiable pero no causal puede usarse en contextos
reversibles; una causal pero no portable no se promueve fuera de su alcance.

### H3 — ¿Puede un agente recordar su ignorancia?

**Pregunta:** ¿puede el sistema representar lo que no sabe, lo que no comprobó y
lo que sigue en disputa, y usar eso para decidir?

**Producto:** ledger de incertidumbre y agenda de preguntas abiertas.

**Criterio:** mejora la abstención y reduce errores persistentes sin paralizar.

### H4 — ¿Qué merece experimentarse?

**Pregunta:** ¿cuándo conviene investigar una incertidumbre en lugar de terminar
la tarea?

**Producto:** política de valor esperado de la información, con restricciones de
seguridad y reversibilidad.

**Criterio:** mejora el aprendizaje por costo frente a experimentar al azar o no
experimentar.

### H5 — ¿Cómo se mantiene corregible el conocimiento?

**Pregunta:** ¿cómo evitar que una interpretación errónea se reproduzca y se
convierta en certeza?

**Producto:** anti-persistencia selectiva, revisión por deriva, disenso preservado
y gobernanza.

**Criterio:** el sistema abandona creencias refutadas más rápido que las
alternativas, sin perder conocimiento válido.

## 5. Tres líneas, una jerarquía

| Línea | Hipótesis | Estado | Papel |
|---|---|---|---|
| **CUMULUS** | La portabilidad procedural entre modelos se puede medir y enrutar | En revisión | Infraestructura |
| **JANUS** | La identificación causal mejora la selección de procedimientos | En revisión | Validación |
| **ESCM** | La incertidumbre explícita y la experimentación activa reducen errores persistentes | Nueva | Programa fundamental |

### ESCM — Experimental Self-Correcting Memory

No es otra arquitectura completa. Es un conjunto de propiedades que cualquier
memoria puede cumplir:

1. **Separación estricta** entre registro factual, interpretación, procedimiento
   operacional, afirmación causal e incertidumbre.
2. **Confianza evolutiva:** cada objeto tiene evidencia, alcance y fecha; se
   revisa cuando cambia el contexto.
3. **Abstención:** el sistema puede responder "no hay evidencia suficiente".
4. **Agenda experimental:** las preguntas abiertas incluyen hipótesis,
   experimento propuesto, costo y condición de actualización.
5. **Política de uso:** fiabilidad, causalidad, portabilidad, riesgo y costo.
6. **Anti-persistencia selectiva:** persistir hechos y trayectorias; reconstruir
   abstracciones cuando la distribución cambió.
7. **Detección de error reproductivo:** monitorear si las abstracciones
   contaminan las trazas y se re-derivan.

## 6. Hipótesis del programa

| # | Hipótesis | Métrica | Falsación |
|---|---|---|---|
| HP1 | La utilidad condicionada a la tarea predice mejor que la saliencia fija | Correlación con éxito futuro | AUC ≤ 0.5 |
| HP2 | La memoria de incertidumbre reduce errores persistentes | Tasa de errores repetidos | Sin diferencia vs. control |
| HP3 | La abstención calibrada mejora el éxito ajustado por riesgo | Éxito – penalización por daño | Peor que actuar siempre |
| HP4 | La experimentación por valor de la información mejora por costo | Aprendizaje por 1k tokens | Peor que azar/no experimentar |
| HP5 | La anti-persistencia selectiva reduce la reproducción de errores | Deriva de creencias erróneas | Igual o peor que Canon |
| HP6 | El disenso preservado acelera la corrección | Tiempo a abandono de creencia falsa | Sin diferencia |
| HP7 | La validación tridimensional supera la puerta causal única | Éxito en tareas reversibles + seguras | Peor en ambas |

## 7. El experimento diferencial

Antes de escribir otra arquitectura, se corre un estudio pequeño pero decisivo.

### 7.1 Condiciones

| Condición | Memoria |
|---|---|
| **A** | Historial de episodios + recuperación convencional |
| **B** | Playbooks persistentes tipo CUMULUS |
| **C** | Memoria factual + abstracciones temporales (anti-persistencia) |
| **D** | JANUS con contrafactuales verificados |
| **E** | D + ledger de incertidumbre + selección activa de experimentos |

### 7.2 Diseño

- Mismas familias de tareas y presupuesto para todas.
- Modelos congelados.
- Restauraciones verificadas con certificado de replay.
- Pruebas reservadas que no participan en la generación de memoria.
- Cambios de versión de modelo, API y requisitos.
- Decisiones antiguas que dejan de ser válidas.
- Resultados ruidosos.
- Casos donde la respuesta correcta es abstenerse o pedir más evidencia.

### 7.3 Métricas

- Éxito en held-out.
- Costo por éxito.
- **Errores persistentes:** errores que se repiten tras una consolidación.
- **Falsos recuerdos promovidos.**
- **Calibración de incertidumbre** (ECE, Brier).
- **Detección de contradicciones.**
- **Transferencia negativa.**
- **Velocidad de abandono** de una creencia refutada.
- **Abstención correcta** en casos irresolubles.

### 7.4 Hipótesis principal

> **E comete menos errores persistentes que B/C/D, sabe cuándo desconfiar de lo
> que recuerda y elige mejores acciones cuando cambian las condiciones.**

No se trata de que E recuerde más. Se trata de que **se equivoque menos y se
corrija más rápido**.

### 7.5 Criterio de muerte

Si E no supera a C o D en errores persistentes, calibración o abandono de
creencias refutadas, la complejidad adicional no se justifica. Si B supera a C,
la persistencia de abstracciones se mantiene como hipótesis viable. Si C supera a
B, el Canon permanente se reduce.

## 8. Qué es novedoso y qué no

**No es novedoso:**

- compilar trazas en skills (Zep, MSCE, Trace2Skill);
- memoria contrafactual verificada (COUNTERMEM);
- admisión contrafactual de memoria (ConMem);
- control adaptativo de memoria (MemCon);
- detectar propagación de errores (When Errors Become Memories);
- replay con certificado (Pakhomov y Nijkamp);
- anti-persistencia (Wang et al.);
- utilidad condicionada a la tarea (Yang et al.);
- conflicto irreducible (TANGLE).

**Candidato a novedoso (sin reclamar todavía):**

1. **Objeto de memoria con identificabilidad declarada:** cada registro dice qué
   se puede estimar, con qué supuestos y qué falta, en lugar de prometer
   causalidad.
2. **Validación tridimensional con política de uso por riesgo:** fiabilidad,
   causalidad y portabilidad no se colapsan en una sola puerta.
3. **Ledger de ignorancia + agenda experimental:** el sistema recuerda preguntas
   abiertas y experimentos pendientes, no solo respuestas.
4. **Anti-persistencia selectiva gobernada:** cuándo persistir y cuándo
   reconstruir, con detección de error reproductivo.
5. **Benchmark longitudinal con deriva real y abstención:** éxito, costo,
   calibración, contradicción y abandono de creencias.

Antes de afirmar novedad hay que ejecutar la revisión sistemática de `25` y el
experimento de `7`.

## 9. Rondas

### R1 — Revisión sistemática viva

- Protocolo `25`; bases, cadenas, criterios, fecha.
- Matriz de antecedentes por mecanismo, no por sistema.

### R2 — Especificación formal

- Objetos epistémicos y campos de identificabilidad.
- Política de uso por dimensión y riesgo.
- Esquema de agenda experimental.

### R3 — Experimento diferencial A–E

- Sandbox con verdad causal conocida.
- Restauraciones certificadas.
- Métricas de errores persistentes y calibración.

### R4 — Dogfooding longitudinal

- Proyecto real durante semanas, con deriva.
- No optimizar antes de medir.

### R5 — Solo si E gana

- Convertir ESCM en arquitectura.
- Si no, reducir el programa a CUMULUS/JANUS y abandonar la línea.

## 10. Lo que el programa no hará

- No afirmar que la biología justifica la arquitectura.
- No afirmar novedad sin revisión sistemática.
- No usar un solo criterio causal para todo.
- No persistir abstracciones sin evidencia de que ayudan.
- No medir éxito ignorando daño, costo y calibración.
- No confundir consenso con verdad.

## 11. Cierre

La pregunta ya no es cómo recordar más. Es cómo construir una relación
**corregible** entre experiencia, conocimiento, incertidumbre y acción.

Eso implica aprender, pero también reconocer el error, revisar las propias
conclusiones, dejar de usar conocimiento obsoleto y decidir qué merece
investigarse. Si el programa logra eso, habrá aportado algo más valioso que otra
capa de memoria: un criterio para saber cuándo confiar en lo que se recuerda.
