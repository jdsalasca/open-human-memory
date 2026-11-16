# 17 — El problema del contexto: límites, causas y estrategias

## 1. Qué es el contexto en un LLM (y qué no)

En un modelo de lenguaje, el contexto es la secuencia de tokens que la atención
puede leer en una pasada. Incluye instrucciones, ejemplos, herramientas,
documentos, historial y la tarea actual. No es memoria: es **memoria de trabajo
temporal**. Al cerrar la ventana, se borra.

Tres propiedades técnicas definen el problema:

- **Costo cuadrático (o casi) de la atención:** duplicar tokens duplica o
  cuadruplica el cómputo, según la arquitectura.
- **Posición:** la información no se usa igual en el medio que en los extremos
  (Liu et al., 2023).
- **Capacidad efectiva menor que la nominal:** los modelos anuncian 128K, 1M o
  más tokens, pero su rendimiento cae antes (Hsieh et al., 2024; Li et al.,
  2024).

## 2. La evidencia empírica

### 2.1 Lost in the Middle

Liu et al. (2023) evaluaron recuperación de información y respuesta a preguntas
con documentos largos. El rendimiento es más alto cuando la información relevante
está al principio o al final del contexto, y **cae cuando está en el medio**,
incluso en modelos diseñados para contextos largos.

**Lectura:** el contexto no es un espacio homogéneo. La posición es una variable
de diseño.

### 2.2 RULER

Hsieh et al. (2024) evaluaron 17 modelos de contexto largo en 13 tareas. Casi
todos muestran caídas grandes al aumentar la longitud; solo la mitad mantiene el
rendimiento a 32K tokens, aunque anuncien ventanas mayores. Definen la **longitud
de contexto efectiva** como la longitud máxima que supera un umbral de
rendimiento.

**Lectura:** "ventana de 1M" no significa "uso efectivo de 1M".

### 2.3 LongICLBench

Li et al. (2024) evaluaron aprendizaje en contexto con muchas clases y prompts de
hasta 50K tokens. El beneficio del contexto largo se estanca alrededor de 20K
tokens y la mayoría de los modelos cae después; solo GPT-4 mantiene parte de la
ventaja.

**Lectura:** más ejemplos no siempre es mejor. El contexto tiene rendimientos
decrecientes y puede inducir confusión.

### 2.4 Otras fuentes de degradación

- **Interferencia:** ejemplos contradictorios o irrelevantes compiten con la
  señal.
- **Falta de estructura:** un texto plano largo es peor que una estructura
  tipada y segmentada.
- **Obsolescencia:** el contexto puede contener información vieja sin marcar.
- **Procedencia:** sin fuente, el modelo no distingue hecho de opinión.
- **Inyección:** el contexto es una superficie de ataque (prompt injection).

## 3. El paralelo cognitivo

La memoria de trabajo humana también es limitada: ~4 elementos (Cowan, 2001), con
componentes especializados (Baddeley y Hitch, 1974; Baddeley, 2000). La carga
cognitiva importa (Sweller, 1988). Los humanos compensan con:

- **Chunking:** agrupar elementos en unidades (Miller, 1956; Chase y Simon,
  1973).
- **Esquemas:** estructuras que organizan la información (Bartlett, 1932; Ghosh
  y Gilboa, 2014).
- **Externalización:** escribir, dibujar, usar artefactos (Clark y Chalmers,
  1998; Risko y Gilbert, 2016).
- **Selección atencional:** filtrar lo irrelevante (Desimone y Duncan, 1995).
- **Gating:** decidir qué entra y qué sale (Miller y Cohen, 2001).

**Lectura:** el problema del contexto no se resuelve "metiendo más"; se resuelve
con **estructura, selección y externalización**, igual que en humanos.

## 4. El punto de vista de la información

El contexto es un canal con capacidad limitada. La pregunta correcta no es
"¿cuántos tokens caben?" sino "¿cuánta información relevante para la tarea
transporta cada token?".

La teoría de tasa–distorsión formaliza el compromiso: para una tasa (bits por
unidad) dada, ¿cuál es la distorsión mínima en la tarea? (Shannon, 1959; Sims,
2016; Bates y Jacobs, 2020). Aplicado al contexto:

- **Tasa:** tokens disponibles.
- **Distorsión:** error en la decisión o la acción.
- **Codificación óptima:** representar lo que minimiza la distorsión de la tarea,
  no lo que "resume mejor" el texto.

Esto explica por qué un resumen "bueno" puede ser un contexto "malo": optimiza
fidelidad textual, no utilidad para la tarea.

## 5. Cinco modos de fallo del contexto

| Fallo | Qué ocurre | Señal | Mitigación |
|---|---|---|---|
| Longitud | El modelo ignora el medio o pierde precisión | Caída con >N tokens | Presupuesto y selección |
| Posición | La información clave queda en el medio | Peor recall en el centro | Reordenar por importancia |
| Interferencia | Ejemplos contradictorios compiten | Respuestas híbridas | Separar por dominio y fuente |
| Obsolescencia | Datos viejos sin marca de validez | Decisiones revocadas | Validez temporal |
| Procedencia | No se distingue hecho de opinión | Confabulación | Metadatos y evidencia |

## 6. Estrategias, de la más simple a la más estructural

### 6.1 Nivel 1: recortar y ordenar

- Presupuesto de tokens por sección.
- Ordenar por importancia (principio y final).
- Eliminar duplicados y ruido.

### 6.2 Nivel 2: recuperar

- RAG por similitud.
- Reranking por relevancia a la tarea.
- Filtros por dominio, fecha y confianza.

### 6.3 Nivel 3: estructurar

- Contexto tipado: instrucciones, hechos, procedimientos, ejemplos, restricciones.
- Separar fuente de interpretación.
- Incluir validez y procedencia.

### 6.4 Nivel 4: comprimir con verificación

- Resumir episodios en esquemas, no en prosa libre.
- Verificar que la compresión preserva las postcondiciones de la tarea.
- Mantener excepciones y contraejemplos.

### 6.5 Nivel 5: externalizar y aislar

- Memoria externa (archivos, grafos, bases).
- Subagentes con contextos separados.
- Artefactos tipados en lugar de transcripciones.

### 6.6 Nivel 6: enrutar

- Elegir el modelo y la habilidad por utilidad esperada.
- Usar modelos baratos para tareas simples y caros para las difíciles.
- Medir costo por éxito, no tokens por respuesta.

## 7. Lo que no funciona (o funciona peor de lo que parece)

- **"Más contexto = mejor".** Falso a partir de cierto punto.
- **Resumir todo.** Pierde método, motivo y procedencia.
- **Un solo índice para todos los dominios.** Interferencia.
- **Recuperar por similitud coseno solamente.** Recupera lo parecido, no lo
  pertinente.
- **Confiar en la ventana nominal.** La capacidad efectiva es menor.
- **Ignorar el orden.** La posición cambia el resultado.

## 8. Una definición operativa

> Contexto es el conjunto mínimo de representaciones —hechos, procedimientos,
> restricciones, affordances y normas— que maximiza la probabilidad de éxito de
> la tarea bajo un presupuesto de tokens y un costo de recuperación.

Es una definición **funcional**, no ontológica. El contexto no es "todo lo que
rodea"; es lo que **hace diferencia** para la tarea. El doc 18 desarrolla la
versión filosófica.

## 9. Implicaciones para el diseño

1. **El contexto se administra, no se llena.** Presupuesto por tipo.
2. **La estructura vence a la longitud.** Un contexto tipado y corto supera a
   uno plano y largo.
3. **La recuperación debe ser por utilidad, no por similitud.**
4. **La compresión debe verificar postcondiciones.** Si no, es pérdida.
5. **La procedencia es parte del contexto.** Sin fuente, no hay decisión.
6. **La validez temporal es obligatoria.** Un hecho viejo sin marca es un error
   esperando.
7. **El aislamiento por subagente reduce interferencia.** Cada uno con su
   presupuesto.
8. **El costo por éxito es la métrica.** No el tamaño del prompt.

## 10. Preguntas abiertas

- ¿Cómo se mide la "utilidad" de un fragmento de contexto sin ejecutar la tarea?
- ¿La caída en el medio es un problema de atención o de entrenamiento?
- ¿Se puede aprender una política de contexto que generalice entre modelos?
- ¿Cuál es el límite práctico de la compresión con verificación?
- ¿Cómo se defiende el contexto de la inyección sin perder utilidad?
