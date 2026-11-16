# Informe de revisión adversarial

**Dictamen:** ninguno de los dos pilotos identifica todavía el mecanismo que pretende estudiar. En 007, el contraste entre memoria y placebo está contaminado por la equivalencia entre programas, la inferencia de la consulta y el encuadre de las instrucciones. En LIRE-001, las mediciones de tokens corresponden a llamadas completas con un arnés variable, no al coste aislado de las representaciones. Los resultados son observaciones exploratorias útiles; varias conclusiones y estados del registro son más fuertes que esas observaciones.

## 1. Explicaciones alternativas

### Prototipo 007

1. **La tarea puede resolverse sin recuperar el programa generador.** Se evalúa únicamente la salida de una consulta. Un modelo puede inferir regularidades suficientes a partir de un ejemplo, usar sus conocimientos previos o producir una salida correcta sin reconstruir los cinco pasos. Por tanto, el acierto no demuestra composición ni reutilización de la subrutina.

2. **Cinco pasos sintácticos pueden representar una función mucho más simple.** En el generador hay operaciones idempotentes, cancelaciones y sobrescrituras: ordenar dos veces puede volver irrelevante la primera ordenación; dos negaciones se anulan; operaciones como `double` y `sort_asc` conmutan en el dominio usado. La profundidad nominal no mide la dificultad efectiva. Un horizonte de 20 pasos también podría colapsar a una función corta.

3. **El placebo no es necesariamente un control inerte.** `sort_desc → double` comparte operadores y estructura con el motivo verdadero. Los sufijos contienen ordenaciones, inversiones y negaciones que pueden hacer desaparecer o transformar la diferencia entre ambos. Su éxito puede deberse a información útil compartida, a una equivalencia conductual en ciertas tareas o a que el modelo lo ignore. No sabemos cuál.

4. **El beneficio común de memoria y placebo puede provenir de la instrucción adicional.** Ambas condiciones dicen «verifícala contra los ejemplos» y advierten que el programa puede tener más pasos; el clon recibe una nota distinta. El contraste mezcla contenido, longitud y una política explícita de resolución. Tampoco prueba que esa política haya sido usada: faltan trazas que lo distingan.

5. **El daño del programa completo es compatible con anclaje, pero no lo identifica.** La condición cambió respecto de la corrida de subrutina y también cambió el artefacto aprendido: `double → sort_asc` frente a `sort_asc → double`. Son equivalentes en este dominio, pero su presentación textual puede afectar al modelo. Además, sin trazas de decisión no puede afirmarse que el agente «aplicó la subrutina y no completó el resto» para cada error. Es una explicación plausible, no una causa observada.

6. **El techo podría ser de la métrica, no de la capacidad.** Con tres ejemplos, 12/12 en clon deja poco margen en esta muestra. Pero con un ejemplo obtiene 9/12 en una corrida y 10/12 en otra; los errores de orden observados también son compatibles con fallos de ejecución. «La familia está saturada» es excesivo sin medir dificultad por clase y repetición.

7. **La verificación selecciona un artefacto favorable.** La sesión 2 solo se ejecuta si la sesión 1 produce un programa que pasa 60 sondas. El resultado es condicional al éxito de adquisición y verificación. Un sistema completo podría fallar o consumir más recursos antes de llegar a la comparación.

8. **El motivo siempre aparece al inicio por construcción.** Esto favorece la reutilización, pero el prompt no indica que aparezca al inicio y el artefacto puede ser redundante en el comportamiento final. El experimento no separa una ayuda genuina para identificar un prefijo de una pista inespecífica sobre el tipo de solución.

### LIRE-001

1. **El 8/8 de las prosas puede reflejar una tarea demasiado fácil.** Dos casos por rama, todos de longitud cuatro, no prueban conservación de una competencia frente a listas vacías, unitarias, valores límite, duplicados con último negativo o perturbaciones que distingan prioridades.

2. **El fallo DSL puede ser variación de ejecución.** Un solo error no distingue una desventaja sistemática de la representación de una respuesta estocástica, un error aritmético, una interpretación incorrecta de la sintaxis o un fallo de rama. La salida registrada es incorrecta; la causa exacta no queda identificada.

3. **La comparación de idiomas también compara redacciones.** No hay una intervención factorial que separe idioma, longitud, redundancia, orden y sintaxis. Una diferencia futura podría deberse a cualquiera de esos factores o a su interacción con el modelo.

4. **El coste incremental puede existir y quedar oculto.** Los ~26.000 tokens son de la llamada completa y algunas llamadas incluyen unos 4.500 adicionales. La diferencia de medianas entre chino y español no permite concluir que ambas reglas cuesten prácticamente lo mismo en tokens. Las medianas se calcularon por separado sobre llamadas variables, no sobre una medición aislada y pareada del texto de la regla.

5. **La caché puede cambiar el coste económico sin cambiar el total informado.** Los resultados incluyen cantidades distintas de tokens cacheados. Precio, tokens facturados, latencia y uso de ventana no son intercambiables; ninguno queda establecido solo con la mediana de `input_tokens`.

## 2. Amenazas de validez no controladas

| Amenaza | Consecuencia para la inferencia |
|---|---|
| **No identificabilidad en 007.** Un ejemplo puede admitir varios programas que coinciden o divergen en la consulta. | Acierto no equivale a identificación del programa; error no implica incapacidad de transferir. Debe enumerarse la versión compatible con cada soporte y consulta. |
| **Selección de tareas posterior al piloto.** Se pasó a un ejemplo tras observar techo; el diseño no fue prerregistrado. | Los resultados sirven para formular hipótesis, no para confirmar una predicción elegida después. |
| **Dependencia entre casos.** Una semilla, un motivo y una sola familia; programas con equivalencias conductuales. | Las 12 tareas no representan 12 familias independientes. Más llamadas sobre la misma plantilla no sustituyen diversidad de motivos y distribuciones. |
| **Orden fijo de condiciones.** Ambos scripts recorren las condiciones en bloques. | Cambios temporales del servicio, carga o caché pueden confundirse con condición. Aleatorizar y bloquear por tarea. |
| **Una ejecución por pareja tarea-condición.** | No se separa variación de tareas de variación entre llamadas del modelo. Hay que repetir llamadas y agrupar el análisis por tarea y familia. |
| **Modelo, versión y arnés únicos.** `--ephemeral` reinicia la sesión, pero no elimina conocimientos previos del modelo ni demuestra invariabilidad del servicio. | El «clon» conserva preentrenamiento y configuración; el resultado no se extiende automáticamente a otros modelos o versiones. |
| **Prompts desiguales en 007.** | El contraste memoria-clon mezcla artefacto con una recomendación de verificar y completar. El propio README reconoce que no se igualaron tokens, aunque el diseño afirma igual longitud. |
| **Control placebo insuficiente.** | Una sola alternativa, con operadores compartidos, no caracteriza el efecto de contenido incorrecto, irrelevante o conductualmente equivalente. |
| **Costes incompletos.** 007 registra segundos, pero no tokens, llamadas de adquisición, verificación, fallos, almacenamiento ni mantenimiento. | No permite afirmar una ventaja a igual `K` ni calcular coste amortizado. |
| **Observabilidad insuficiente.** Los resultados de 007 guardan respuesta y corrección, pero no la observación completa ni trazas de razonamiento o uso del artefacto. LIRE tampoco conserva en sus filas el código de retorno que sí obtiene el ejecutor. | La reproducción y el diagnóstico de errores dependen del código y de reconstruir el entorno; no se puede atribuir con seguridad un fallo a una etapa. |
| **Métrica de salida exacta.** | Es útil como resultado final, pero confunde selección de rama, ejecución, formato y fallos del entorno. Añadir métricas diagnósticas sin sustituir el acierto final. |
| **Potencia y equivalencia.** 11/12 frente a 11/12 no establece equivalencia; 8/8 no establece fidelidad perfecta. | Se necesita un margen práctico de equivalencia o no inferioridad y un tamaño de muestra diseñado para excluir diferencias relevantes. |
| **Comparaciones múltiples y decisiones adaptativas.** | La evidencia más llamativa puede seleccionarse tras observar varios regímenes. Separar exploración de confirmación y declarar la comparación primaria. |
| **Semántica de las representaciones.** | La equivalencia de traducciones y DSL está asumida. Requiere revisión independiente y casos de fronteras antes de atribuir diferencias al formato. |

**Discrepancia auditable:** el README de 007 reporta para «programa completo» un par discordante clon/placebo a favor del clon. El [resultado agregado](../../resources/investigation/prototipo-007-transferencia/results/summary.json) y las filas crudas indican lo contrario: **0 a favor del clon y 1 a favor del placebo**. No altera el empate cualitativo de muestras pequeñas, pero sí muestra que el análisis debe generarse y comprobarse automáticamente.

## 3. Hipótesis nuevas y falsables

Los falsadores siguientes requieren márgenes y tamaños de muestra fijados antes de ejecutar; una diferencia no significativa, por sí sola, no falsaría una ventaja.

| Hipótesis | Falsador operacional propuesto |
|---|---|
| **H-A. La instrucción de verificar explica la mejora común de memoria y placebo.** | Con prompts igualados, un clon que recibe la misma instrucción de verificación queda por debajo de memoria/placebo en más de un margen predefinido, con un intervalo compatible solo con esa diferencia. |
| **H-B. La profundidad efectiva predice los fallos mejor que la longitud sintáctica.** | En tareas estratificadas por ambas, la complejidad conductual mínima no mejora la predicción fuera de muestra frente a la profundidad sintáctica, según criterio y partición fijados de antemano. |
| **H-C. El placebo comparte información útil con el motivo verdadero.** | Placebos con igual longitud y sintaxis, pero sin operadores compartidos y sin equivalencia en las sondas, rinden igual que el placebo actual dentro de un margen práctico definido. |
| **H-D. El efecto negativo de «programa completo» depende del encuadre.** | Con el mismo artefacto, tareas y presupuesto, la diferencia entre encuadres queda dentro de un margen de equivalencia previamente establecido en una muestra suficiente. |
| **H-E. Las representaciones concisas ahorran tokens incrementales, aunque el arnés oculte el ahorro en el total.** | El recuento aislado con el tokenizador correcto y las mediciones pareadas de llamadas con arnés estable no muestran un ahorro superior al umbral de interés. |
| **H-F. El coste de compresión aparece principalmente en fronteras y excepciones.** | La diferencia de error entre forma completa y comprimida no aumenta en casos de frontera respecto de casos ordinarios, dentro de un margen fijado y con suficiente precisión. |

## 4. Experimento mínimo siguiente

**Elegiría 007B, pero como experimento diagnóstico de F1, no como demostración de aprendizaje.** Antes de buscar una familia donde «el clon falle», verificaría *por qué* falla y si el artefacto contiene información pertinente que el clon no recibe.

Diseño mínimo:

- Construir una familia pequeña de transformaciones con semántica ejecutable y **clases conductuales distintas**, descartando o etiquetando composiciones que se simplifiquen.
- Separar dos tipos de tarea: **identificables** desde el soporte y **ambiguas** con hipótesis compatibles que divergen en la consulta. Publicar el conjunto de soluciones compatibles.
- En las identificables, comparar: clon con instrucción de verificar; mismo clon con pista irrelevante; artefacto correcto; y artefacto incorrecto que no sea conductualmente equivalente. Igualar la instrucción y controlar el presupuesto.
- Añadir una prueba de ejecución: entregar el programa completo correcto y medir si el modelo aplica la transformación. Así se distingue, al menos parcialmente, inferencia de ejecución.
- Usar varias semillas y motivos; asignar y bloquear el orden de llamadas por tarea; registrar fallos, tokens y costes. Reservar tareas para una corrida confirmatoria.

**Crítica de 007B:** elegir deliberadamente una familia donde el clon falle puede fabricar una ventaja trivial: basta entregar a memoria información que el clon desconoce. Eso mide el valor de información externa, no necesariamente adquisición eficiente. Hay que comparar también con un clon que recibe las experiencias de origen o un resumen equivalente, y cobrar el coste de crear y verificar el artefacto. Además, «20+ pasos» sin controlar simplificación puede reproducir el mismo problema.

**No priorizaría LIRE-001b de skill larga todavía.** Alargar la regla puede mejorar la relación señal/ruido, pero introduce posición, truncamiento, atención, redundancia y diferencias de dificultad. Primero aislaría el coste incremental de las reglas actuales con un arnés controlado y verificaría equivalencia semántica. Solo después probaría longitudes y posiciones factorialmente. Una regla larga no hace válida por sí sola la comparación.

## 5. Opciones no consideradas o insuficientemente exploradas

| Dimensión | Opción y pregunta que permitiría responder |
|---|---|
| **Representación** | Ejemplos seleccionados, tabla de decisión, árbol de condiciones, código ejecutable con intérprete, regla declarativa y resumen con contraejemplos. Comparar fidelidad y coste; no asumir que conservan la misma información. |
| **Tareas** | Contrafactuales, detección de inconsistencias, selección de una prueba informativa, abstención ante ambigüedad y transferencia entre listas, cadenas y registros. Estas tareas obligan a medir capacidades distintas de producir una salida. |
| **Selección de evidencia** | Comparar ejemplos aleatorios con ejemplos que eliminan hipótesis compatibles. Puede ser más valioso elegir mejor la experiencia que comprimirla. |
| **Recuperación** | Biblioteca con artefactos relevantes, irrelevantes y obsoletos; recuperador ciego a la solución, historial completo y oráculo etiquetado. Medir recuperación y uso por separado. |
| **Modelos** | Un modelo más débil y otro de familia o proveedor diferente, con versiones registradas. No basta bajar capacidad si también cambian tokenizador, herramientas o presupuesto. |
| **Métricas** | Acierto por clase, calibración y abstención, curva de aprendizaje, coste hasta umbral, tokens incrementales, coste facturado, latencia, fallos de herramienta y mantenimiento. Reportar efectos emparejados e intervalos. |
| **Controles** | Artefacto vacío de igual longitud, instrucción de verificación sin contenido, motivo verdadero barajado, motivo falso relevante y ejemplos originales entregados al clon. |
| **Robustez temporal** | Cambiar una regla después de aprenderla y medir tanto la detección de obsolescencia como el daño de conservar el artefacto anterior. |
| **Análisis del dominio** | Enumerar equivalencias conductuales e identificabilidad antes de llamar al modelo. Esto puede revelar que un benchmark aparentemente profundo tiene pocas funciones distintas. |

## 6. Afirmaciones del registro mal calibradas

Las referencias son al [registro de afirmaciones](../../docs/registro-de-afirmaciones.md), salvo que se indique otra cosa.

| ID | Problema | Reformulación propuesta |
|---|---|---|
| **G1** | Generaliza desde pocos casos y mezcla profundidad con dificultad efectiva. Su falsador —otro modelo o familia— no refuta una observación restringida a este modelo y familia. | «En estas muestras exploratorias, el clon acertó 12/12 con tres ejemplos y 9/12 o 10/12 en dos corridas con un ejemplo para programas nominales de cinco pasos. El smoke de profundidad 7–9 fue 4/4 por condición.» Estado: **observado localmente**, sin inferir saturación general. |
| **G2** | «Perjudica la composición» y «anclaje» atribuyen mecanismo. El contraste observado es más estrecho y el encuadre difiere entre corridas. | «En la corrida exploratoria con el artefacto presentado como programa completo, memoria acertó 2/12 y clon 10/12; hubo 8 pares a favor del clon y ninguno en sentido contrario. El mecanismo causal requiere una comparación controlada de encuadres.» |
| **G3** | «11/11» no expresa los denominadores: son **11/12 frente a 11/12**. Igualdad puntual no demuestra equivalencia. | «Con encuadre de subrutina, memoria y placebo acertaron 11/12 cada uno; cada condición acertó una tarea que la otra falló. La muestra no permite establecer equivalencia ni descartar una diferencia relevante.» |
| **L1** | El falsador y el estado mezclan una hipótesis sobre tokens incrementales con medianas del arnés. | «No se identificó el coste incremental de cada representación; los tokens de llamadas completas variaron con el arnés. La diferencia observada de medianas no estima por sí sola el coste de la regla.» |
| **L2** | «Refutada parcialmente» convierte una diferencia de una llamada en conclusión estable sobre fidelidad. | «Se observó un error en DSL y ninguno en las otras cuatro formas, sobre ocho casos por forma; no se ha estimado la diferencia de fidelidad ni demostrado equivalencia.» |
| **L3** | «Refutada» combina ahorro no medido con un fallo aislado. | «No se demostró conjuntamente ahorro incremental y conservación de fidelidad para este DSL; la hipótesis queda abierta hasta medir ambos con precisión y márgenes fijados.» |
| **L4** | La comparación de tokens completos no muestra que el texto chino use más tokens que el español. | «En estos textos el chino tiene menos caracteres; el experimento no aisló los tokens de las reglas y no puede establecer la relación entre sus costes incrementales.» La proposición universal «menos caracteres siempre implican menos tokens» exige un contraejemplo medido directamente. |
| **T3** | «Empatan» no es un falsador estadístico operativo: una igualdad puntual o ausencia de significación no prueba equivalencia. | «Para un margen y presupuesto fijados, un intervalo de equivalencia suficientemente preciso descarta una ventaja del procedimiento superior al mínimo relevante.» |
| **T4** | Dice «solo con estructura compartida», más fuerte que P3 en [teoría](../../docs/teoria.md), que predice una ventaja **mayor** con estructura compartida. | Alinear ambas: «La ventaja de adquisición es mayor con estructura compartida que con solo vocabulario compartido», especificando contraste de interacción y margen. |

También debe corregirse en el [README de LIRE](../../resources/investigation/lire-001/README.md) que el piloto «valida el método» y que «los bytes tampoco» predicen tokens. El piloto demuestra que el arnés dificulta la medición; no valida la identificación del coste incremental ni establece una relación general entre bytes y tokens.

## 7. Tres experimentos priorizados

### 1. 007B diagnóstico: ¿información, instrucción o reutilización?

- **Hipótesis:** el artefacto correcto mejora el acierto frente a un control con la misma instrucción y longitud; la ventaja persiste frente a un clon con las experiencias de origen cuando se iguala el coste total.
- **Condiciones:** clon con instrucción de verificación; placebo irrelevante; artefacto correcto; historial de origen; programa completo correcto como control de ejecución. Tareas identificables y ambiguas analizadas por separado.
- **Métricas:** acierto emparejado por clase; tasa de ejecución correcta con programa dado; tokens y llamadas de adquisición, verificación y resolución; coste hasta alcanzar un umbral fijado.
- **Criterio de muerte:** en el conjunto confirmatorio, un intervalo de equivalencia suficientemente preciso excluye una ventaja mínima práctica del artefacto frente a historial y controles, a igual presupuesto. Esto cierra **la ventaja de ese procedimiento en esa familia**, no toda memoria.

### 2. LIRE aislado: ¿cuál es el coste por fidelidad?

- **Hipótesis:** al menos una representación reduce el coste incremental de tokens sin perder más de un margen aceptable de fidelidad frente a la prosa completa.
- **Condiciones:** prosa completa, concisa, DSL y tabla; mismas reglas revisadas independientemente; casos ordinarios y adversariales; orden aleatorio, repetición y arnés estable. Medir el texto con el tokenizador correspondiente y contrastar con llamadas controladas.
- **Métricas:** tokens incrementales, tokens de entrada y salida, caché y coste facturable; acierto exacto por rama y frontera; intervalo de no inferioridad de fidelidad.
- **Criterio de muerte:** ninguna alternativa alcanza simultáneamente el ahorro mínimo y la no inferioridad previamente fijados. No extrapolar a otras reglas ni longitudes.

### 3. Transferencia con recuperación genuina y cambio de dominio

- **Hipótesis:** una representación derivada de experiencias reduce experiencias hasta umbral en una familia reservada con estructura compartida, frente a historial completo y una regla simple, a igual coste total.
- **Condiciones:** familias de entrenamiento y prueba separadas por estructura y superficie; clon, historial completo, recuperador ciego y artefacto verificado; un oráculo explícito como techo. Incluir una familia con vocabulario compartido pero estructura distinta.
- **Métricas:** `E`, `K` y `P` por separado; tasa de recuperación pertinente, uso efectivo, precisión por familia y coste amortizado. Analizar la interacción entre estructura compartida y condición.
- **Criterio de muerte:** con precisión suficiente, la mejora del sistema evaluado queda por debajo del mínimo relevante frente al mejor control a igual coste, o desaparece en familias reservadas. La conclusión se limita al mecanismo y distribuciones probados.

**Prioridad:** el primer experimento impide interpretar como transferencia lo que podría ser ejecución, ambigüedad o una instrucción adicional. El segundo repara la medición de representación. El tercero solo merece el coste después de establecer que el instrumento distingue esos mecanismos y de reproducir una línea base, como exige el propio plan.