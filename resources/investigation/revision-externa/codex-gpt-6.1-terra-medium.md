# Informe de revisión por pares

## (a) Resumen y dictamen

**Dictamen: rechazar en su estado actual.**

El repositorio contiene un programa de investigación prometedor y una auditoría interna inusualmente explícita, pero todavía no presenta evidencia suficiente para una contribución empírica o teórica de un venue de agentes/ML. La pregunta principal —si la experiencia produce competencia transferible después de reiniciar el contexto y cambiar de tarea— permanece sin probar. Los resultados más sólidos describen un sintetizador de programas en un dominio cerrado; el único experimento con un LLM es una línea base pequeña, sin intervención válida de recuperación de memoria.

La contribución potencial más defendible hoy sería un **estudio metodológico acotado sobre cómo controles defectuosos y presupuestos mal contabilizados pueden producir conclusiones engañosas en un entorno sintético**. Para sostener incluso esa versión hacen falta corregir incoherencias, asegurar presupuestos comparables, reconstruir la procedencia de los resultados y validar las inferencias estadísticas.

La verificación realizada para esta revisión fue principalmente documental y de código. Ejecuté la suite en modo de solo lectura: **60 pruebas pasaron**. No reejecuté las llamadas al modelo ni reproduje los experimentos ajenos. Las pruebas que pasan indican consistencia con los tests existentes; no validan por sí solas el diseño experimental ni las conclusiones.

## (b) Cinco fortalezas

1. **Las rectificaciones son visibles.** La [errata del 006-B](../../../docs/errata-006b.md) identifica la fuga de la solución, el sesgo de selección y los fallos de herramientas, y retira inferencias concretas.

2. **Hay controles relevantes.** El 004 incorpora búsqueda sin historial a mayor profundidad, bibliotecas aleatorias del mismo lenguaje y un barrido de 560 bibliotecas. Esto expone que el resultado inicial dependía de una comparación débil.

3. **Se distinguen medidas que suelen confundirse.** El repositorio reconoce la diferencia entre candidatos, aplicaciones primitivas estimadas y aplicaciones ejecutadas; también reconoce que las condiciones de profundidad distinta no constituyen una ablación limpia de memoria.

4. **Se publican resultados negativos y materiales de ejecución.** Hay código, semillas sintéticas, resultados serializados, protocolos y una suite de pruebas. La documentación declara que no se ha reproducido ningún competidor.

5. **La pregunta científica está articulada con claridad.** La separación propuesta entre rendimiento, experiencias hasta un umbral y coste puede ser útil si se convierte en estimandos operativos y se mide con controles apropiados.

## (c) Debilidades críticas

### 1. La afirmación central carece de una prueba directa

La teoría plantea un efecto del historial sobre adquisición o desempeño a coste comparable ([teoría, sección 1](../../../docs/teoria.md)). Ninguno de los estudios demuestra ese efecto en un agente que reinicia contexto y enfrenta familias estructurales reservadas. El 004–006-A usa un sintetizador construido para un lenguaje conocido; en 006-B no existe una condición válida de recuperación genuina.

El registro es honesto al mantener abiertas algunas afirmaciones, pero la cantidad de resultados locales no sustituye la evidencia sobre la pregunta principal. Tampoco se ha reproducido una línea base externa competitiva. El manuscrito, por tanto, no tiene aún el experimento que justificaría su motivación.

### 2. La teoría contiene una condición necesaria falsa

[Teoría, corolario 3](../../../docs/teoria.md) afirma que para probar expansión hacen falta **simultáneamente** un espacio que no quepa en el presupuesto y tareas donde la búsqueda exhaustiva no baste por ambigüedad. Eso no se sigue de la proposición anterior.

Un contraejemplo conceptual basta: una tarea puede ser identificable, pero su solución aparecer demasiado tarde en la búsqueda para el presupuesto disponible; una macro o un orden aprendido puede encontrarla dentro de ese presupuesto. Hay aumento de cobertura **bajo presupuesto** sin necesidad de ambigüedad. A la inversa, la ambigüedad puede resolverse con información adicional, pero no necesariamente con una herramienta.

La proposición de cobertura 1 también necesita explicitar que existe al menos un programa candidato correcto, que la enumeración alcanza la longitud pertinente, que las operaciones y el verificador son correctos y que el presupuesto incluye los costes que se pretenden comparar. Bajo esas condiciones es principalmente una consecuencia de la definición, no una teoría general de memoria.

### 3. Las predicciones y sus falsadores no siempre prueban lo que dicen

- [Plan, F2.5](../../../docs/plan.md): si una forma fija iguala o supera al selector aprendido, **no se deduce** que la forma no importe ni que solo importe el contenido. Puede haber diferencias entre formas y un selector deficiente, datos insuficientes o costes de selección altos.
- [Teoría, P3](../../../docs/teoria.md) afirma que la mejora de adquisición ocurre *solo* si hay estructura compartida. Es una hipótesis fuerte, pero «estructura» y «vocabulario» necesitan definiciones y manipulaciones independientes; compartir vocabulario puede transportar información útil.
- Los cinco canales se presentan como exhaustivos ([teoría](../../../docs/teoria.md)), aunque se solapan: una herramienta puede contener información, cambiar la representación y modificar la política. Sin una regla operacional para asignar efectos, no constituyen una descomposición causal identificada.
- El «clon» necesita una definición de igualdad de información y de coste de adquisición. Quitar el historial al control y entregar artefactos derivados de él a la intervención identifica el efecto del paquete completo, no automáticamente el del mecanismo de memoria.

### 4. Los presupuestos y las comparaciones no sostienen todas las conclusiones económicas

En [v3_solver.py](../../../src/ohmem/v3_solver.py) el límite se verifica **antes del candidato**, mientras que las aplicaciones se acumulan después ([línea 60](../../../src/ohmem/v3_solver.py)). Un candidato puede rebasar los 120 pasos y aun así aceptarse. Por tanto, el presupuesto es un corte aproximado entre candidatos, no un límite estricto de 120 aplicaciones. El exceso máximo y su distribución deben medirse por condición: pueden variar con la longitud expandida de las macros.

Además, en 006-A el probe se suma *después* de resolver, pero no se descuenta del presupuesto de búsqueda. Las tasas de acierto de la política y de búsqueda no son comparaciones bajo el mismo presupuesto total. El cálculo informado sirve como análisis de coste ex post, no como evaluación de una política sometida a 120 pasos totales.

En 005, la comparación principal cambia a la vez biblioteca y profundidad. Que sea una comparación entre diseños está reconocido en el README principal, pero impide atribuir limpiamente la diferencia a la memoria. También falta incluir el coste diferencial de generar, seleccionar, almacenar y mantener artefactos cuando se habla de coste total.

### 5. La inferencia estadística es demasiado fuerte para el diseño

El 006-A informa bootstrap sobre 96 filas provenientes de solo dos semillas ([README 006-A](../../../resources/investigation/prototipo-006-politica/README.md)). Las tareas comparten generador, programas equivalentes, biblioteca y política entrenada; tratarlas como observaciones independientes puede subestimar incertidumbre para una población de familias o entrenamientos. Se necesitan intervalos que reflejen la unidad de generalización elegida, por ejemplo agrupación por clase conductual y repetición independiente de entrenamiento y evaluación.

La comparación frente al control barajado favorece interpretar que **alguna información dependiente de la tarea o del estado** influye en el resultado, dentro de este diseño. No identifica por sí sola que el *probe* sea la causa exclusiva: hace falta una ablación pareada que conserve el resto del proceso, y considerar la variabilidad del barajado. Una diferencia con IC que incluye cero tampoco demuestra equivalencia ni ausencia de ventaja de la política.

### 6. La síntesis bibliográfica no permite sostener sus afirmaciones de novedad

La revisión admite una base, un revisor, 88 candidatos sin evaluar y procedencia incompleta por trabajo ([cribado](../../../resources/investigation/revision-sistematica/cribado.md)). Los resultados crudos de búsqueda se dejaron en el «historial del agente», fuera del repositorio ([búsquedas](../../../resources/investigation/revision-sistematica/busquedas.md)). No puede reconstruirse la selección.

Con esa evidencia, expresiones como «nadie descompone» o «la integración no está hecha» ([síntesis](../../../resources/investigation/revision-sistematica/README.md)) exceden lo que el cribado permite concluir. Lo defendible es: *no se identificó en la muestra revisada un trabajo que combine esas características*, sujeto a búsqueda y extracción verificables.

### 7. La estructura es legible como bitácora, pero no como submission cerrado

La existencia de [manuscrito](../../../docs/manuscrito.md), registro de afirmaciones y mapa para revisores ayuda. Sin embargo, hay varias fuentes normativas y documentos «históricos» que siguen accesibles con conclusiones categóricas sin una advertencia suficiente en el punto donde aparecen. El lector debe reconciliar README, teoría, registro, protocolos, addenda, errata y papers.

Sobran, para el cuerpo de un artículo, las arquitecturas y agendas que no se evalúan; pueden quedar como apéndice o trabajo futuro. Falta una tabla única y verificable con **hipótesis preregistrada, unidad de análisis, condiciones, coste total, resultado, incertidumbre, estado y enlace a datos/código por experimento**. También falta un único manuscrito que defina con claridad qué resultado constituye la contribución.

## (d) Errores factuales o citas incorrectas

1. **Error aritmético en el coste de 006-A.** Se afirma que la política cuesta **1,9 veces más que buscar/no decidir** ([README](../../../README.md); [README 006-A](../../../resources/investigation/prototipo-006-politica/README.md)). Según la misma tabla, cuesta 84,3 frente a 59,5 pasos: **1,42 veces**, aproximadamente 42 % más. La razón 84,3/44,5 ≈ **1,89** corresponde a comparar con *macros primero*, no con búsqueda sin memoria.

2. **El estado F12 contradice la extracción.** [Registro, F12](../../../docs/registro-de-afirmaciones.md) sostiene que las cifras de la revisión están verificadas documentalmente. [Extracción](../../../resources/investigation/revision-sistematica/extraccion.md) dice que solo tres trabajos alcanzaron ese nivel; la mayoría proviene de resúmenes. F12 debe limitarse por fila.

3. **La afirmación retirada sobre la ventana sigue publicada.** [005, sección 8](../../../resources/investigation/prototipo-005-presupuesto/README.md) afirma que 96 episodios no caben en una ventana, mientras [README](../../../README.md) y [plan](../../../docs/plan.md) la retiran por falta de medición. Un aviso general de precedencia no corrige la frase allí donde se cita.

4. **La inferencia retirada sobre el LLM reaparece.** [006-B](../../../resources/investigation/prototipo-006-agente-llm/README.md) dice que los fallos muestran que el agente no identifica el programa; la misma documentación y la errata retiran esa identificación del cuello de botella. El fallo de salida no separa identificación, aplicación, aritmética o formato.

5. **SkillsBench: atribución de versión insuficientemente fijada.** [Extracción](../../../resources/investigation/revision-sistematica/extraccion.md) combina 87 tareas, 8 dominios y +16,6 pp y reconoce discrepancias. La página primaria actual de [arXiv](https://arxiv.org/abs/2602.12670) presenta en su resumen 86 tareas, 11 dominios y +16,2 pp; el [registro oficial v1.1](https://www.skillsbench.ai/tasks) sí presenta 87 y 8. No puedo afirmar con esta comprobación que el +16,6 sea falso para una versión anterior, pero **no queda verificado que todas las cifras citadas pertenezcan al mismo artefacto, versión y análisis**. Deben citarse versión, tabla y denominador exactos.

6. **JANUS presenta supuestos causales como comprobaciones mecánicas.** [JANUS](../../../resources/investigation/papers/janus-final-es.md) y secciones siguientes proponen verificar ignorabilidad y clasificar identificabilidad mediante cinco chequeos. La ausencia de confusores no medidos generalmente no se verifica solo con datos observacionales; requiere supuestos y diseño. Asimismo, la frase «sin propensión no se pueden aplicar estimadores fuera de política» es demasiado amplia: hay otros enfoques basados en modelos; para IPS y variantes concretas sí se requieren probabilidades de comportamiento conocidas o estimadas bajo condiciones adicionales. El texto anuncia «cinco niveles» y enumera seis.

7. **«Verificada» no equivale a «imprescindible».** La síntesis dice que Proof-Gated demostró que la verificación independiente es imprescindible. Incluso si se confirman las cifras de ese estudio, demostrar muchos errores de autoverificación en un protocolo no prueba necesidad universal. No verifiqué independientemente esa cifra en el texto primario durante esta revisión.

Como contraste positivo, el resumen primario de [MemDev-Bench](https://arxiv.org/abs/2610.27524) sí respalda que se reportan 555 tareas base, 4.869 históricas y fallos causados por memoria en tareas antes resolubles. Eso es verificación documental de esa descripción, no replicación del resultado.

## (e) Faltas de reproducibilidad

- **006-B:** se registran alias del modelo, esfuerzo, versión de CLI, prompt y semilla del generador. Faltan una revisión inmutable del modelo o declaración de que no está disponible, configuración completa de decodificación, semilla de generación si el proveedor la admite, versiones del entorno y coste en tokens/dinero. La semilla de tareas no fija la aleatoriedad del LLM. El acceso autenticado y la posible evolución del servicio impiden garantizar reproducción exacta.
- **Llamadas al modelo:** una sola tentativa por tarea y una sola configuración no estiman variabilidad entre ejecuciones. La rejilla pondera sintaxis, no clases conductuales; debe informarse rendimiento por clase y el estimando poblacional.
- **Resultados corregidos de 006-A:** la versión congelada se invalida y la corrección es posterior a observar fallos y resultados. Debe etiquetarse como análisis corregido/exploratorio, con código y datos fijados por commit o hash, y evaluarse de nuevo sobre semillas y tareas reservadas.
- **Pre-registro:** un hash local prueba integridad respecto de un archivo disponible, pero no demuestra por sí solo que el protocolo y el código fueran fijados antes de ver los resultados. Se requiere evidencia temporal independiente o historia de commits verificable, incluyendo qué código y datos quedaron congelados.
- **Revisión bibliográfica:** faltan respuestas crudas de OpenAlex, consultas completas con ordenación, fechas y versiones, lista de deduplicación, decisiones por registro y procedencia individual. El diagrama mezcla la selección inicial y la bola de nieve sin una trazabilidad que permita reconstruir el flujo.
- **Costes:** los pasos primitivos no incluyen necesariamente toda la ejecución, entrenamiento, almacenamiento, recuperación, selección, mantenimiento ni costes del LLM. Los resultados deben nombrar explícitamente el denominador medido, no llamarlo coste total.
- **Comparación externa:** ningún competidor se ha ejecutado. El proyecto declara correctamente esta ausencia, pero limita cualquier afirmación de competitividad.

## (f) Lista priorizada de cambios

### P0 — Imprescindible antes de enviar

1. **Elegir una contribución única.** O bien un artículo metodológico acotado sobre errores experimentales en el simulador, o bien un estudio de adquisición y transferencia de memoria. No presentar el segundo como demostrado por el primero.
2. **Corregir las contradicciones y cifras** señaladas arriba, especialmente el factor 1,9, F12, la ventana de 96 episodios y la atribución del fallo cognitivo en 006-B.
3. **Reformular la teoría:** eliminar la necesidad conjunta de ambigüedad y espacio no explorable; definir cobertura con y sin presupuesto, supuestos de realizabilidad, estimandos y falsadores que realmente se sigan de cada hipótesis.
4. **Hacer cumplir el presupuesto total** o reportar explícitamente el rebase por candidato; descontar el probe antes de buscar y repetir las comparaciones.
5. **Ejecutar la comparación central con recuperación genuina:** clon, recuperación que no vea la solución, historial completo, procedimiento y oráculo etiquetado; mismo modelo, herramientas e información de entrada, con costes de construcción y uso por separado.
6. **Reservar familias y semillas independientes**, registrar el protocolo antes de observar resultados y repetir entrenamientos y evaluaciones. Reportar efectos pareados, intervalos adecuados a familias/clases y fallos de ejecución.

### P1 — Necesario para una contribución convincente

1. Reproducir una línea base externa relevante con su configuración y variabilidad, y añadir controles fuertes y asequibles.
2. Medir adquisición, verificación, recuperación, inferencia y mantenimiento; presentar por separado pasos, tokens, tiempo y coste monetario.
3. Completar la revisión bibliográfica con registros exportables, selección por fila y versiones exactas. Limitar la novedad a lo que la búsqueda permita sostener.
4. Añadir análisis por clase conductual, ambigüedad, distribución, repetición de llamadas al modelo y sensibilidad al presupuesto.
5. Para JANUS, distinguir supuestos causales no verificables de comprobaciones empíricas; comparar contra literatura y estimadores causales pertinentes.

### P2 — Claridad y mantenimiento

1. Consolidar en el manuscrito una tabla de afirmaciones y evidencia; mover documentos históricos y propuestas no evaluadas a apéndices.
2. Poner avisos de retirada junto a cada afirmación invalidada, no solo en documentos que supuestamente prevalecen.
3. Publicar scripts de auditoría que recalculen tablas e intervalos desde los datos guardados sin sobrescribirlos, y documentar el entorno completo.

## (g) Afirmaciones que retiraría o reformularía

| Afirmación actual | Formulación defendible |
|---|---|
| «Para probar expansión» hacen falta espacio no explorable **y** ambigüedad. | «La expansión de cobertura bajo presupuesto puede aparecer si la búsqueda no alcanza una solución, incluso con tareas identificables; la ambigüedad plantea un problema adicional y distinto». |
| «La política cuesta 1,9× más que buscar». | «En esta tabla, cuesta aproximadamente 1,42× la búsqueda sin memoria y 1,89× macros primero; el presupuesto del probe no se descontó durante la búsqueda». |
| «El probe aporta información» como conclusión causal cerrada. | «La política supera al control barajado en esta muestra; se necesita una ablación adicional para aislar la contribución del probe y cuantificar su variabilidad». |
| «La política pierde contra la regla» como refutación general. | «En estas dos semillas la diferencia observada favorece a la regla en 1,0 pp; el intervalo informado no establece equivalencia ni generalización». |
| «Las cifras de la revisión están verificadas documentalmente». | «Solo las filas identificadas como verificadas se contrastaron con fuentes primarias; las demás son resultados declarados en resúmenes». |
| «Nadie» integra las seis características. | «No identificamos esa combinación en la muestra revisada; la búsqueda no permite excluir trabajos omitidos». |
| «96 episodios no caben en una ventana». | Retirar hasta medir serialización, tokenizador y ventana del modelo concreto. |
| «El agente no identifica el programa». | «El agente produjo una salida incorrecta; este diseño no identifica qué capacidad causó el error». |
| «La verificación independiente es imprescindible». | «El estudio citado reporta discrepancias entre afirmaciones de verificación y ejecución en su protocolo, lo que motiva controles independientes». |
| «Si una forma fija iguala al selector, la forma no importa». | «Ese resultado no respaldaría la ventaja del selector evaluado; las formas todavía podrían diferir entre tareas». |