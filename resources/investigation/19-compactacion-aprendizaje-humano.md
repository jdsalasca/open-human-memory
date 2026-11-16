# 19 — ¿Existe la compactación en el aprendizaje humano?

## 1. Tres palabras que se confunden

- **Compresión:** reducir el número de bits necesarios para representar algo
  (teoría de la información).
- **Compactación:** reducir la longitud del contexto en un sistema artificial,
  normalmente resumiendo o seleccionando.
- **Consolidación:** proceso biológico por el que una memoria se estabiliza, se
  integra y se transforma.

La pregunta "¿existe algo como la compactación en el aprendizaje humano?" se
responde mejor separando las tres. En humanos hay **compresión y consolidación**;
no hay "compactación" de contexto, porque no hay una ventana de tokens que haya
que vaciar. Pero sí hay mecanismos que cumplen la misma función: **reducir la
información retenida preservando lo útil**.

## 2. Los mecanismos humanos de reducción

### 2.1 Chunking

Miller (1956) mostró que la capacidad de memoria de trabajo se mide en **unidades
significativas**, no en elementos primitivos. Chase y Simon (1973) mostraron que
los expertos en ajedrez recuerdan posiciones como configuraciones, no como
piezas. Ericsson y Kintsch (1995) extendieron la idea a la memoria de trabajo a
largo plazo: las claves de recuperación permiten manejar estructuras complejas.

**Lección:** comprimir no es acortar; es **reorganizar en unidades de orden
superior**.

### 2.2 Gist y verbo (fuzzy-trace theory)

Reyna y Brainerd (1995) proponen que la memoria codifica dos trazas en paralelo:

- **Verbatim:** detalles exactos, frágiles, ligados a la forma.
- **Gist:** significado esencial, robusto, ligado a la interpretación.

Con el tiempo, la traza verbo se pierde y la gist se conserva. No es un resumen
arbitrario: es una abstracción orientada a la decisión.

**Lección:** el sistema humano no guarda un resumen del texto; guarda una
representación del **significado relevante para la acción**.

### 2.3 Esquemas

Bartlett (1932) mostró que recordamos reconstruyendo con esquemas; Ghosh y Gilboa
(2014) revisan el concepto y lo definen como una estructura asociativa que
captura regularidades y guía la codificación y la recuperación. Gilboa y Marlatte
(2017) lo vinculan con la neurobiología de la consolidación.

**Lección:** el esquema es una compresión **generativa**: permite reconstruir
casos nuevos, no solo recordar los viejos.

### 2.4 Semanticización

La distinción episódico/semántico (Tulving, 1972, 2002) y la teoría de las trazas
múltiples (Nadel y Moscovitch, 1997; Winocur y Moscovitch, 2011) describen cómo
los episodios se transforman en conocimiento general. Lo episódico no desaparece
necesariamente; se vuelve menos dependiente del hipocampo y más esquemático.

**Lección:** la consolidación no es "borrar el episodio"; es **extraer la
regularidad** y conservar el episodio con otra fuerza.

### 2.5 Categorización y abstracción de prototipos

Posner y Keele (1968) mostraron que se abstrae un prototipo de ejemplos
concretos. La categoría no es una lista de casos: es una representación
generalizada.

**Lección:** el sistema humano comprime casos en **conceptos**, no en índices de
casos.

### 2.6 Sueño y generalización

Stickgold y Walker (2013) describen el sueño como un **triaje**: selecciona,
integra y generaliza. No copia el día; extrae estructura. La consolidación
dependiente de sueño puede mejorar la generalización y la creatividad.

**Lección:** la reducción humana ocurre offline y está orientada a la
generalización, no a la fidelidad textual.

### 2.7 Olvido

Ebbinghaus (1885), Hardt, Nader y Nadel (2013), Richards y Frankland (2017) y
Ryan y Frankland (2022): el olvido es adaptativo y, a menudo, un cambio de
accesibilidad. Lo que se olvida no es aleatorio: se olvida lo no usado, lo
irrelevante y lo que interfiere.

**Lección:** comprimir no es solo guardar menos; es **decidir qué no volver a
traer**.

## 3. ¿Qué se conserva y qué se pierde?

| Se conserva | Se pierde |
|---|---|
| Gist y significado | Detalle verbatim |
| Esquema y regularidades | Contexto episódico fino |
| Saliencia emocional | Frecuencia exacta |
| Procedimientos y habilidades | Fuente y orden de presentación |
| Excepciones que violan expectativas | Información redundante |
| Identidad narrativa | Microdetalles sin función |

La pérdida no es uniforme: el sistema humano conserva lo que **predice**, lo que
**amenaza** y lo que **se usa**. Es una compresión con criterio.

## 4. ¿Es como la compactación de un LLM?

| Dimensión | Compactación LLM | Compresión humana |
|---|---|---|
| Disparador | Límite de tokens | Consolidación, sueño, uso |
| Mecanismo | Resumen/extracción | Abstracción, esquema, poda |
| Criterio | Lo que el resumen conserva | Saliencia, predicción, uso, emoción |
| Verificación | Rara | Contraste con la realidad y el grupo |
| Reversibilidad | A veces (archivo) | Parcial (claves, reconsolidación) |
| Producto | Texto más corto | Estructura generativa |
| Riesgo | Perder método y motivo | Distorsión y falsos recuerdos |

La diferencia clave: la compresión humana es **generativa y selectiva**; la
compactación LLM suele ser **textual y arbitraria**. Un resumen puede conservar
la prosa y perder el procedimiento; un esquema conserva el procedimiento y
descarta la prosa.

## 5. El lado oscuro: compactar puede impedir aprender

La literatura de **dificultades deseables** (Bjork y Bjork, 2011) muestra que
eliminar el esfuerzo de recuperación puede mejorar el desempeño inmediato y
empeorar la retención. Si un sistema compacta la experiencia y le entrega al
agente la respuesta lista, el agente no aprende: ejecuta.

Esto tiene una consecuencia incómoda para los agentes: **la compactación que
maximiza la eficiencia puede minimizar el aprendizaje**. El sistema debe
distinguir entre:

- compactar para **ejecutar** (contexto de una tarea), y
- compactar para **aprender** (consolidación con recuperación y verificación).

## 6. La compresión pedagógica

Enseñar es comprimir para otro. Un buen maestro selecciona lo esencial, da un
ejemplo resuelto y luego retira el andamiaje (Wood, Bruner y Ross, 1976;
Vygotsky, 1978). La compresión pedagógica no es un resumen: es una
**transformación orientada al aprendiz**, con verificación de que puede ejecutar.

**Implicación:** la enseñanza de habilidades entre agentes debe ser una
compresión pedagógica con verificación de fidelidad, no un volcado de log.

## 7. Una definición útil

> La compactación humana es la reducción selectiva de información en una
> representación más abstracta, orientada a la acción futura, que conserva gist,
> esquema y excepciones, y descarta detalle verbatim y redundancia.

No es "resumir". Es **abstraer para usar**.

## 8. Implicaciones para el diseño

1. **No compactar por longitud, sino por función.** ¿Qué necesita la tarea?
2. **Preservar procedimiento y motivo.** Son lo primero que se pierde en un
   resumen.
3. **Conservar excepciones.** Lo raro pero crítico no puede diluirse.
4. **Verificar la compresión.** Si el esquema no permite ejecutar, falló.
5. **Separar ejecutar de aprender.** El contexto de la tarea no es el material de
   consolidación.
6. **Usar recuperación, no solo lectura.** La consolidación con práctica retiene
   más.
7. **Archivar, no borrar.** La accesibilidad cambia; el original puede volver.

## 9. Preguntas abiertas

- ¿Cuál es la unidad mínima de compresión que preserva una habilidad?
- ¿Cómo se mide la pérdida de "motivo" en una compactación automática?
- ¿La compactación debe ser supervisada por el mismo agente que ejecuta o por un
  curador independiente?
- ¿Se puede compactar sin perder la capacidad de aprender de la experiencia?
- ¿La gist de un LLM es estable o deriva con cada resumen?
