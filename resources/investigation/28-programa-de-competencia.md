# 28 — Programa de competencia v3: de la memoria a la expansión de capacidad

**Estado:** reemplaza la formulación centrada en memoria (CUMULUS/JANUS) como
objetivo final. La memoria pasa a ser un medio; el objeto de estudio es la
**competencia acumulativa**.

## 1. Tres objetivos que no son lo mismo

| Objetivo | Pregunta | Qué lo demuestra |
|---|---|---|
| **Continuidad** | ¿El sistema conserva lo útil al reiniciar, compactar o cambiar de modelo? | Retención tras reset y cambio de modelo |
| **Competencia acumulativa** | ¿Cada experiencia mejora el desempeño futuro? | Curva \(G(n)\) positiva |
| **Expansión de capacidad** | ¿Puede resolver clases de problemas que antes no resolvía? | Transferencia a familias estructuralmente nuevas |

CUMULUS y JANUS atacan los dos primeros. El tercero —el más importante— no tenía
teoría ni programa experimental. Este documento lo define.

## 2. Lo que enseñan las arquitecturas clásicas

### 2.1 Soar: chunking y subobjetivos

Soar (Newell, 1990; Laird, 2012) introduce **espacios de problemas**, **impasses**
y **subobjetivos**. Cuando el agente se atasca, crea un subobjetivo; al resolverlo,
el **chunking** compila la experiencia en una regla de producción reutilizable.

**Qué resolvió:** convertir una deliberación resuelta en una regla que evita
repetirla. Eso es exactamente "una tarea resuelta modifica los mecanismos para la
siguiente".

**Qué falló:** las reglas compiladas pueden ser rígidas, interferir entre sí y
no generalizar a problemas estructuralmente distintos. El chunking no descubre
nuevas abstracciones; compila la que ya se usó.

**Qué exigir a CUMULUS:** una SIR debe explicar qué aporta frente a una regla de
producción con condiciones y efectos. Si no aporta nada, es una regla con otro
nombre.

### 2.2 ACT-R: activación, no similitud

ACT-R (Anderson et al., 2004) separa memoria declarativa y procedimental. La
activación de un chunk combina frecuencia, recencia y asociación contextual.

**Qué resolvió:** modelar **qué conocimiento se activa** en un momento, no solo
qué se almacena.

**Qué implica:** el cuello de botella puede no ser el almacenamiento, sino la
**selección**. Un archivo enorme con mala activación rinde peor que uno pequeño
con buena activación.

**Pregunta para el proyecto:** ¿el problema es la memoria o la política de
activación?

### 2.3 Dyna: aprender, planear y actuar en un ciclo

Dyna (Sutton, 1990) integra experiencia real, modelo del entorno y planificación
con experiencias simuladas.

**Qué resolvió:** usar lo aprendido para Explorar consecuencias sin esperar a
vivirlas.

**Qué implica para JANUS:** no basta con almacenar contrafactuales; hay que
cambiar el **ciclo de decisión**. El agente debe planificar con su memoria, no
solo consultarla.

### 2.4 Darwin Gödel Machine y AlphaEvolve: auto-modificación y búsqueda

- **DGM** (Zhang et al., 2025) modifica el código del agente, evalúa variantes y
  conserva las mejores en un archivo abierto.
- **AlphaEvolve** (Novikov et al., 2025) usa generación y evaluación automática de
  programas para descubrir algoritmos.

**Qué resolvieron:** mejorar el **programa** del agente, no solo su memoria.

**Qué implica:** CUMULUS conserva habilidades, pero no estudia cómo **inventar**
mejores procedimientos, herramientas o estrategias. La expansión de capacidad
requiere un motor de descubrimiento, no solo un Canon.

### 2.5 Sleep Framework y Nested Learning: la actualización paramétrica

Google Research (2026) propone fases de actividad y consolidación offline que
actualizan parámetros de módulos de memoria neuronal, con expertos de baja
dimensión, destilación y ejemplos sintéticos. Nested Learning (2025) estudia
componentes que aprenden a distintas frecuencias.

**Qué cuestionan:** la decisión de congelar los pesos para siempre. Es una
restricción práctica para APIs cerradas, no una ley del problema.

**Qué implica:** el programa debe comparar tres modalidades con igual presupuesto:

1. memoria externa;
2. actualización paramétrica;
3. híbrido.

No se puede afirmar que la memoria externa es superior sin medir el costo de
entrenamiento, mantenimiento y evaluación de las otras.

### 2.6 Benchmarks de competencia acumulativa

- **MemoryArena** (ICML 2026): tareas interdependientes entre sesiones; la memoria
  conversacional no predice el desempeño en acción.
- **Continual Learning Exam** (2026): 120 tareas en cinco niveles; los niveles
  posteriores dependen de competencias anteriores. La mejor configuración completó
  47,7% de los niveles y terminó los cinco niveles en 23,3% de las tareas.
- **AgentMemoryBench** (2026): aprendizaje online, retención, transferencia y
  reparación bajo feedback erróneo.

**Qué implican:** hay que medir **dependencia acumulativa**, no mil tareas
independientes.

### 2.7 La cuarta ola (2026): expansión, meta-memoria y uso real

- **Mem²Evolve** (Cheng et al., ACL 2026): Experience Memory + Asset Memory;
  crea herramientas y agentes expertos a partir de la experiencia. +18,53% sobre
  LLM, +11,80% sobre experiencia sola, +6,46% sobre activos solos. Es el
  competidor más directo en expansión de capacidad.
- **MemSkill** (Zhang et al., 2026): aprende y evoluciona las **operaciones de
  memoria** con controller–executor–designer; el metaprendizaje del gestor ya
  existe.
- **VibeMemBench** (Fan et al., 2026): 111 tareas de 90 repos; la experiencia
  verificada ayuda, pero 11 de 12 sistemas de memoria no superan la línea base
  sin memoria.
- **MemUse** (Xu et al., 2026): entrega ≠ uso; muchas memorias recuperadas no
  cambian la acción.
- **PaMER** (2026): el estado oculto previo a la acción predice compresión y
  recall; el contexto reciente conserva la mayor parte de la señal.
- **MDSKILL** (Jin et al., 2026): internaliza skills en la política con
  multi-view distillation; +7,1% ALFWorld, +8,1% WebShop.
- **SkillsBench** (2026, arXiv:2602.12670v2; 86 tareas, 11 dominios): skills curadas +16,2 pp; autogeneradas sin beneficio medio.
- **How Well Do Agentic Skills Work in the Wild** (Liu et al., 2026): con 34.198 skills, el beneficio cae al exigir selección y adaptación.
- **ContinualSkillBench** (2026): conservar contexto y feedback compite con mantener una biblioteca explícita de habilidades.
- **SkillLearnBench** (2026): el beneficio de las habilidades autogeneradas no es uniforme y hay deriva al depender del propio feedback.
- **DreamCoder / Stitch / LILO**: aprenden bibliotecas de funciones reutilizables con compresión y búsqueda adaptativa. Son la línea base real del aprendizaje de abstracciones; el 004-A mostró que contar pares frecuentes no basta.

**Lectura:** el campo ya se mueve de "recordar" a "expandir capacidades,
gestionar la memoria, internalizar y medir uso". Open Human Memory no puede
reclamar esas ideas; su espacio es el **diagnóstico controlado de transferencia
composicional** y la **curva longitudinal**.

## 3. Por qué CUMULUS/JANUS no bastan

La secuencia de CUMULUS es:

```
Experiencia → Memoria → Habilidad → Reutilización
```

Mejora la información disponible para el razonamiento, pero no necesariamente el
**mecanismo** de razonamiento. Un sistema completo necesita estudiar:

- representación del problema,
- abstracción,
- planificación,
- exploración,
- metacognición,
- aprendizaje,
- transferencia.

CUMULUS tiene piezas para algunas; no tiene una teoría de sus interacciones.

## 4. La paradoja del contexto

> Cuanta más experiencia acumula un agente, más conocimiento potencial tiene;
> pero cuanto más introduce en el contexto operativo, mayor es el costo, la
> interferencia y la dificultad de seleccionar.

Formalmente:

\[
\max_{\pi,\phi} \mathbb{E}_{t\sim D}\left[R(t,\pi(\phi(M,t)))\right]
\quad \text{s.a.} \quad \operatorname{Tokens}(\phi(M,t)) \le B
\]

La representación óptima depende de la **distribución de tareas futuras**. No hay
compresión universal.

### 4.1 Compresión funcional orientada a decisiones

La pregunta no es "¿cuántos tokens eliminamos conservando información?", sino:

> **¿Cuál es la representación más pequeña que conserva la capacidad de tomar
> decisiones correctas sobre una familia de tareas?**

El resultado puede ser un resumen, pero también una taxonomía, una regla
ejecutable, una máquina de estados o una prueba.

**Hipótesis:** después de muchos incidentes, no se necesitan N procedimientos;
se necesita una taxonomía de causas y un algoritmo de diagnóstico, revisable
cuando aparece una causa nueva.

## 5. Cuatro paradojas

### 5.1 Cuello de botella de von Neumann

Memoria y procesamiento separados; el traslado es un límite. En agentes, el
equivalente funcional es recuperar, procesar e incorporar al contexto.

**Pregunta:** ¿cuánto conocimiento debe estar fuera y cuánto incorporado a
mecanismos que se activen sin reconstruir texto?

### 5.2 Paradoja de Moravec

La capacidad es desigual: un modelo puede resolver matemáticas y fallar en una
condición práctica. Almacenar más no elimina la desigualdad.

**Implicación:** evaluación multidimensional, no una puntuación global.

### 5.3 Paradoja de Rogers

Si copiar es barato, demasiados individuos dejan de aprender del entorno; la
población depende de conocimiento antiguo y produce menos información nueva.

**Implicación para los Pods:** la memoria colectiva puede aumentar la conformidad
y reducir la innovación. Hay que preservar diversidad y exploración independiente.

### 5.4 Paradoja de la auto-mejora

Si el agente necesita competencia para evaluar mejoras a su propia arquitectura,
¿cómo mejora de forma fiable? La generación de ideas es barata; **distinguir
mejoras reales de éxitos aparentes** es el límite.

**Implicación:** el evaluador debe evolucionar y auditarse independientemente.

## 6. Cuellos de botella

| Cuello | Gravedad | ¿Lo resuelve CUMULUS/JANUS? |
|---|---|---|
| Representación de tareas nuevas | Muy alta | Parcial |
| Verificación y calidad del feedback | Muy alta | Parcial |
| Generalización entre familias | Muy alta | Insuficiente |
| Selección de conocimiento | Muy alta | Parcial |
| Planificación y recursos | Alta | Poco |
| Nuevas estrategias de razonamiento | Muy alta | Poco |
| Interferencia y obsolescencia | Alta | Mejor en v0.2 |
| Transferencia entre modelos | Alta | Hipótesis |
| Costo de consolidación | Alta | Pendiente |
| Pérdida de estado | Alta | Identificada |

## 7. Arquitectura objetivo (conceptual)

1. **Modelo de situación:** objetivos, restricciones, entidades, relaciones,
   incertidumbres.
2. **Memoria multinivel:** episodios, hechos, modelos conceptuales,
   procedimientos, metaconocimiento.
3. **Controlador de memoria y contexto:** decide qué recuperar, cuánto, con qué
   representación y cuándo prescindir. Minimiza
   \(C_{\text{inferencia}} + C_{\text{memoria}} + C_{\text{verificación}} +
   \lambda C_{\text{error}}\).
4. **Motor de descubrimiento conceptual:** detecta estructuras, formula
   hipótesis, propone abstracciones, busca contraejemplos y valida transferencia.
5. **Aprendizaje de procedimientos y estrategias:** skills, reglas, algoritmos,
   herramientas, políticas.
6. **Consolidación paramétrica opcional:** adaptadores o módulos entrenables, en
   una línea separada.

No se implementa todo. El MVP es el **diagnóstico** de qué capa importa.

### 7.1 Mecanismos de inducción, composición y revisión

Un motor conceptual no es un resumidor. Necesita:

1. **Espacio de hipótesis:** programas, reglas o grafos candidatos; no texto.
2. **Inducción:** elegir la hipótesis más simple que explica los ejemplos
   (MDL/occam), con soporte y contraejemplos.
3. **Composición:** combinar primitivas y verificar que la composición explica
   los datos; el Prototipo 002 muestra que sin composición en el espacio de
   hipótesis, D3 es imposible.
4. **Analogía:** mapear estructura relacional entre dominios, no vocabulario.
5. **Contraejemplos:** buscar activamente casos que refuten la abstracción.
6. **Validación:** predictiva (nuevos casos), explicativa (por qué), y
   transferencia (nuevas familias).
7. **Revisión:** dividir una abstracción demasiado general o fusionar varias
   demasiado específicas; registrar la versión y el motivo.

Métricas: compresión (MDL), transferencia, tasa de contraejemplos, tiempo a
revisión y daño de una abstracción incorrecta. Una abstracción que no mejora la
predicción o la transferencia no entra al Canon.

## 8. El riesgo de aprender a equivocarse mejor

Si el agente modifica procedimientos y estrategias, un error puede propagarse:

```
experiencia errónea → regla → decisiones → nuevas experiencias sesgadas →
refuerzo → estrategia general
```

El error deja de estar en un recuerdo y se incorpora a la política.

**Regla:** ninguna modificación duradera de una política general se promueve solo
porque mejoró las tareas que usaron esa misma política para generar la
experiencia. Debe probarse fuera de muestra, en tareas antiguas, nuevas y
adversariales, con versiones y rollback.

## 9. La pregunta reformulada

> ¿Puede un agente, mediante interacción continuada con entornos verificables,
> desarrollar representaciones conceptuales, procedimientos y políticas
> progresivamente más generales, conservar sus mejoras a través de reinicios y
> cambios de modelo, y aumentar de forma sostenida su competencia en familias de
> tareas no observadas sin un crecimiento proporcional de su contexto operativo?

Incluye aprendizaje, generalización, persistencia, economía, transferencia,
autocorrección y expansión.

## 10. Prioridades inmediatas

1. Incorporar Soar, ACT-R, Dyna, DGM, AlphaEvolve, Sleep/Nested Learning,
   MemoryArena, CLE y AgentMemoryBench.
2. Distinguir aprendizaje recurrente, transferencial y conceptual.
3. Construir el **experimento diagnóstico A–E** antes de otra arquitectura.
4. Medir \(G(n)\) y las tres distribuciones.
5. Separar costos de ejecución, recuperación, consolidación, entrenamiento,
   verificación y mantenimiento.
6. Solo después, implementar la capa que el diagnóstico indique.
