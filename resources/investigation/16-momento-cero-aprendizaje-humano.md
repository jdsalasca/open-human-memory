# 16 — Momento cero: qué puede aportar el aprendizaje humano antes de la primera acción

## 1. Definición

Llamamos **momento cero** al instante en que un agente recibe una tarea y aún no
ha interactuado con ella. Solo tiene:

- sus pesos (conocimiento previo del modelo),
- la memoria disponible (hechos, casos, procedimientos),
- la descripción de la tarea y el entorno (herramientas, restricciones).

La pregunta es si puede **mejorar su primer intento** sin entrenar el modelo. La
respuesta depende de una distinción: el aprendizaje humano no es solo acumular
experiencia; es **llegar con estructura**. Un adulto no enfrenta una tarea nueva
como un recién nacido: la enfrenta con teorías, analogías, causalidad y
metacognición.

## 2. La ventaja humana no es la velocidad, es el prior

Kühl (2022) encontró que los humanos aprenden patrones con menos ejemplos que el
aprendizaje supervisado. Lake et al. (2015) mostraron aprendizaje de conceptos
desde un solo ejemplo con inducción de programas bayesianos. La explicación no
es "el cerebro es más rápido", sino que el humano aporta **sesgos inductivos**
que reducen el espacio de hipótesis.

Tenenbaum, Kemp, Griffiths y Goodman (2011) lo formulan como inferencia
bayesiana sobre estructuras: el aprendiz no solo estima parámetros; infiere la
**forma** de la representación (árboles, gramáticas, grafos causales). Esa
inferencia estructural es lo que permite generalizar con pocos datos.

**Implicación:** el momento cero de un agente puede mejorar si la memoria le
entrega una **estructura relevante**, no un montón de texto parecido.

## 3. Siete mecanismos humanos útiles en t = 0

### 3.1 Teorías intuitivas

Desde muy temprano, los humanos organizan la experiencia en teorías de física,
psicología y biología (Carey, 2009; Gopnik y Meltzoff, 1997). No son creencias
explícitas: son marcos que dicen qué variables importan y qué relaciones son
posibles.

**Análogo artificial:** un esquema de dominio que enumera entidades, relaciones y
restricciones antes de actuar.

### 3.2 Modelos causales

Gopnik et al. (2004) muestran que los niños aprenden mapas causales y los
representan como redes bayesianas. La causalidad permite predecir el efecto de
una intervención, no solo correlacionar.

**Análogo artificial:** un grafo causal de la tarea (qué depende de qué) que
guíe la experimentación y el diagnóstico.

### 3.3 Analogía y mapeo estructural

Gentner (1983) propone que la analogía mapea **relaciones** entre un dominio
fuente y uno objetivo, no atributos superficiales. Es el mecanismo que permite
reutilizar una solución de un contexto en otro con distinta apariencia.

Yasunaga et al. (2024) mostraron que inducir ejemplos analógicos mejora el
razonamiento de los LLM frente a zero-shot CoT y few-shot manual.

**Implicación:** recuperar por estructura, no por similitud coseno. Un buen
recuerdo para el momento cero es el que comparte el **patrón causal**, aunque el
vocabulario sea distinto.

### 3.4 Composición

Fodor y Pylyshyn (1988) defendieron la composicionalidad como condición de
sistematicidad. Lake y Baroni (2018) mostraron que las redes fallan en
generalización composicional sistemática. La composición permite construir una
solución nueva a partir de piezas conocidas.

**Análogo artificial:** habilidades SIR componibles, con contratos tipados, en
lugar de prompts monolíticos.

### 3.5 Curiosidad e indagación activa

Kidd y Hayden (2015) revisan la curiosidad como un mecanismo que maximiza el
aprendizaje por muestra; Oudeyer y Kaplan (2007) la modelan como motivación
intrínseca por reducir incertidumbre. El aprendiz humano no espera datos: los
busca.

**Análogo artificial:** elegir la siguiente acción o pregunta por **ganancia
esperada de información**, no por costumbre.

### 3.6 Metacognición

Flavell (1979) define la metacognición como el conocimiento y control de los
propios procesos cognitivos; Nelson y Narens (1990) la separan en monitoreo y
control. Saber qué no se sabe cambia la estrategia: explorar, preguntar o actuar.

**Análogo artificial:** un score de confianza calibrado por dominio que decida
entre actuar, recuperar más o pedir ayuda.

### 3.7 Aprendizaje social y pedagogía

Bandura (1977) mostró que se aprende observando modelos; Tomasello (1999) y
Henrich (2015) muestran que la cultura acumulativa depende de transmisión de alta
fidelidad. En el momento cero, el humano no solo tiene su experiencia: tiene la
de su grupo.

**Análogo artificial:** dialecto del pod, ejemplos resueltos y un curador que
enseña antes de que el agente actúe.

## 4. Lo que la máquina ya hace en t = 0

### 4.1 Aprendizaje en contexto

- **In-context learning como inferencia bayesiana** (Xie et al., 2022): el modelo
  infiere un concepto latente a partir de los ejemplos del prompt.
- **Induction heads** (Olsson et al., 2022): circuitos que copian patrones
  repetidos y explican buena parte del ICL.
- **ICL como descenso de gradiente** (von Oswald et al., 2023): en tareas
  lineales, una capa de auto-atención puede implementar un paso de gradiente.
  Es una equivalencia matemática en un régimen restringido, no una teoría
  general.

**Lectura:** el contexto no es pasivo; es un mecanismo de aprendizaje temporal.
Pero ese aprendizaje se borra al cerrar la ventana.

### 4.2 Estrategias de inferencia

- **Chain-of-thought** (Wei et al., 2022) y **zero-shot CoT** (Kojima et al.,
  2022): externalizar pasos mejora tareas de razonamiento.
- **ReAct** (Yao et al., 2023): alternar razonamiento y acción con herramientas.
- **Analogías inducidas** (Yasunaga et al., 2024): generar un ejemplo análogo
  antes de resolver.
- **Self-consistency** (Wang et al., 2023): muestrear varias soluciones y votar.

**Lectura:** estas técnicas mejoran el momento cero, pero no acumulan: cada
sesión empieza de nuevo salvo que algo externo persista.

### 4.3 Memoria de procedimientos

La propuesta CUMULUS añade lo que falta: un Canon de habilidades compiladas que
se recupera antes de actuar, se renderiza para el modelo y se verifica. El
momento cero deja de ser "zero-shot" y pasa a ser "one-shot con un prior
recuperado y verificado".

## 5. Hipótesis del boost de momento cero

> **H-M0.** La capacidad de un agente para resolver una tarea en el primer
> intento, sin ejemplos específicos de esa tarea, aumenta si antes de actuar
> recupera una estructura relevante (esquema o procedimiento), la mapea
> analógicamente, genera una prueba causal de bajo costo y calibra su confianza
> para decidir si actúa o indaga.

### 5.1 Mecanismo propuesto

El boost no viene de "pensar más", sino de tres reducciones:

1. **Reducción del espacio de hipótesis:** un esquema descarta soluciones
   imposibles.
2. **Selección de representación:** una analogía elige las variables relevantes.
3. **Reducción de incertidumbre:** una prueba causal o una pregunta bien elegida
   produce la información que más discrimina.

Formalmente, si el éxito depende de \(P(\text{éxito} \mid \text{prior},
\text{representación}, \text{acciones})\), la memoria no cambia los pesos, pero
cambia el prior y la representación. Eso puede aumentar el éxito sin entrenar.

### 5.2 Predicciones

| Predicción | Comparación | Métrica |
|---|---|---|
| Recuperar esquema ayuda | con vs. sin recuperación | éxito al primer intento |
| La estructura importa más que la similitud | recuperación estructural vs. coseno | éxito y transferencia |
| La analogía ayuda | con vs. sin mapeo analógico | éxito en tareas con distinta superficie |
| La indagación ayuda | acción directa vs. prueba informativa | éxito y costo |
| La metacognición ayuda | con vs. sin gate de confianza | tasa de fallos evitables |
| El dialecto ayuda | con vs. sin glosario del pod | tiempo a competencia |

### 5.3 Ablaciones

Cada mecanismo se apaga por separado. Si el boost desaparece al quitar la
recuperación estructural, el efecto es del prior; si desaparece al quitar la
metacognición, el efecto es del control; si no desaparece con nada, probablemente
sea un artefacto del evaluador.

## 6. Por qué esto puede aumentar la capacidad sin entrenar

Hay tres sentidos de "capacidad":

1. **Capacidad latente:** lo que el modelo puede hacer con información perfecta.
   La memoria no la cambia.
2. **Capacidad efectiva:** lo que el modelo logra con el contexto y las
   herramientas disponibles. La memoria sí la cambia.
3. **Capacidad de adquisición:** cuántos ejemplos necesita para llegar a un
   nivel. La memoria también la cambia, al reducir el espacio de búsqueda.

La hipótesis del momento cero es una hipótesis sobre (2) y (3), no sobre (1). Es
por eso que puede ser cierta sin reentrenamiento y sin magia.

## 7. Límites y riesgos

- **Prior equivocado:** un esquema irrelevante ancla al agente y produce
  transferencia negativa. Mitigación: score de relevancia estructural y
  verificación temprana.
- **Analogía falsa:** la superficie comparte estructura aparente pero no causal.
  Mitigación: contrastar predicciones del mapeo antes de ejecutar.
- **Metacognición miscalibrada:** los LLM suelen ser confiados de más.
  Mitigación: calibración por dominio con resultados observados.
- **Indagación costosa:** preguntar o experimentar consume presupuesto.
  Mitigación: valor esperado de la información.
- **Sobrecontextualización:** meter demasiado contexto degrada el rendimiento
  (ver doc 17). Mitigación: presupuesto y selección.
- **Artefacto del evaluador:** el boost puede venir de un juez complaciente.
  Mitigación: verificadores ejecutables y holdouts.

## 8. Implicaciones para CUMULUS

- El **Canon** es el prior estructural del momento cero.
- El **Puente** decide cómo se presenta ese prior a cada modelo.
- El **Pod** aporta el dialecto y los ejemplos sociales.
- La **Forja** produce esquemas y procedimientos, no resúmenes.
- El **Canon** debe incluir un campo de **relevancia estructural** (a qué
  problemas se parece por causalidad, no por texto).

## 9. Preguntas abiertas

- ¿Cómo se mide "estructura compartida" sin un juez humano?
- ¿La recuperación estructural mejora el primer intento o solo acelera el
  segundo?
- ¿El boost de momento cero persiste cuando la tarea es genuinely nueva?
- ¿La metacognición de un LLM es calibrable sin feedback humano?
- ¿Cuánto del boost humano viene de la pedagogía y cuánto de la cognición
  individual?
