# 10 — Matriz de antecedentes

**Fecha:** 16 de noviembre de 2026
**Estado:** lectura directa de 17 trabajos, **no** una revisión sistemática. Las
cifras dudosas están marcadas `[verificar]`. La diferencia importa: esto es un mapa
para decidir qué reproducir, no evidencia de originalidad.

---

## 1. Por qué una matriz y no una cronología

Una lista de papers responde «qué se ha publicado». Una matriz responde «qué
mecanismo resuelve qué cuello de botella, bajo qué condiciones, y qué tendríamos
que hacer para saber si aportamos algo». Solo la segunda sirve para diseñar.

Las columnas son las del modelo de canales de `docs/teoria.md`: información,
representación, política, herramientas, parámetros.

---

## 2. Matriz

| Mecanismo | Trabajo representativo | Qué demuestra | Condiciones | Código | Canal | Qué nos falta para compararnos |
|---|---|---|---|---|---|---|
| Biblioteca de conceptos + búsqueda adaptativa | DreamCoder (Ellis et al., 2021) | Aprende abstracciones y una política de búsqueda; resuelve tareas que el lenguaje inicial no alcanza | Dominios formales, currículo, mucho cómputo | Sí | Herramientas + política | Reproducir un resultado suyo, no citarlo |
| Descubrimiento de abstracciones por compresión | Stitch (Bowers et al., 2023) | Library learning tratable; órdenes de magnitud más rápido que alternativas | Corpus de programas | Sí | Herramientas | Reproducir su benchmark y medir coste |
| Síntesis + compresión + documentación | LILO (Grand et al., 2024) | Bibliotecas interpretables con LLM + compresión simbólica | Dominios de síntesis | Sí | Herramientas + representación | Ver si la documentación mejora el uso |
| Síntesis guiada por contraejemplos | CEGIS (Solar-Lezama) | El verificador corrige hipótesis; aprende de fallos, no solo de éxitos | Lenguaje y verificador dados | Parcial | Representación | Memoria de contraejemplos vs soluciones |
| Aprendizaje activo por consultas | Angluin (1987) | Elegir la consulta que discrimina reduce el número de ejemplos | Estructuras formales | — | Información | Comparar ejemplos aleatorios vs informativos |
| Reutilización de búsqueda | LPA*, D* Lite (Koenig et al.) | Conservar estados y cotas evita recalcular | Entornos que cambian poco | Sí | Herramientas | Reutilizar estados, no solo macros |
| Opciones jerárquicas | Sutton, Precup y Singh (1999) | Una habilidad tiene inicio, política y terminación | RL | — | Política | Macros condicionales vs secuencias fijas |
| Metaprendizaje | MAML (Finn et al., 2017) | Adaptación rápida con pocos datos | Pesos | Sí | Parámetros | `E(F)` con y sin familias previas |
| Memoria de experiencias + activos | Mem²Evolve (ACL 2026) | Coevolución de experiencia y herramientas; +18,53 % sobre LLM `[verificar]` | Benchmarks de agentes | En preparación según la auditoría | Herramientas | Su resultado, con su código |
| Memoria adaptativa en ejecución | AdaMEM (ICML 2026) | Adapta la memoria durante la tarea | Agentes LLM | `[verificar]` | Información + política | Si supera a historial completo |
| Memoria para agentes de código | MemDev-Bench (2026) | 555 tareas + 4.869 históricas; la memoria ayuda y **también rompe** tareas antes resolubles | Repositorios reales | `[verificar]` | Información | Es el banco natural del 007 |
| Entrega vs uso de memoria | VibeMemBench (2026) | 11 de 12 sistemas no superan la línea base sin memoria `[verificar]` | 111 tareas, 90 repos | `[verificar]` | Información | Confirma que «disponible ≠ usado» |
| Skills curadas vs autogeneradas | SkillsBench (2026, v2) | Curadas +16,2 pp; autogeneradas sin beneficio medio | 86 tareas, 11 dominios | `[verificar]` | Herramientas | La objeción directa a CUMULUS |
| Aprendizaje continuo de habilidades | ContinualSkillBench (2026) | Contexto y feedback compiten con biblioteca explícita `[verificar]` | 5 dominios | `[verificar]` | Herramientas + información | Si la biblioteca aporta sobre historial |
| Métodos de generación de habilidades | SkillLearnBench (2026) | Beneficio no uniforme; deriva con auto-feedback `[verificar]` | Tareas reales | `[verificar]` | Herramientas | Deriva y retirada |
| Calibración de memoria | MemCalib (2026) | Sobreuso e infrauso de recuerdos `[verificar]` | LLM | `[verificar]` | Política | Cuándo confiar |
| Memoria en uso | MemUse (2026) | Muchas memorias recuperadas no cambian la acción `[verificar]` | Agentes | `[verificar]` | Política | Métrica de uso, no de entrega |

---

## 3. Qué cubre cada uno y qué no

Ninguno de los trabajos de la matriz hace, a la vez:

1. Medir **`E(F)`** (experiencias hasta competencia) en familias **estructuralmente
   reservadas**.
2. Comparar contra un **clon** con el mismo modelo y presupuesto.
3. Separar **cinco canales** (información, representación, política, herramientas,
   parámetros).
4. Reportar **coste total** (adquisición, verificación, recuperación,
   mantenimiento) y no solo latencia.
5. Medir **deriva** (cuándo el conocimiento deja de servir).
6. Verificar el uso de **herramientas por tarea** en cinco etapas.

Ese conjunto es el hueco. No es un mecanismo nuevo: es una **medición**. Y es
defendible precisamente porque los mecanismos ya existen y nadie los ha comparado
así.

**Lo que no podemos decir:** que seamos los primeros en nada. DreamCoder ya aprende
bibliotecas y políticas; CEGIS ya aprende de contraejemplos; MAML ya mide
adaptación rápida; MemDev-Bench ya mide memoria en código real.

---

## 4. Lo que no hemos leído

Declararlo es parte del método:

- No hemos leído los 17 trabajos completos; varios son resúmenes de la auditoría.
- No hemos ejecutado ninguno.
- No hay revisión sistemática: no hay cadenas de búsqueda ejecutadas, ni conteo de
  cribados, ni PRISMA.
- No hay ninguna comparación numérica en condiciones propias.

`docs/plan.md` exige cerrar esta deuda **antes** del 007.

---

## 5. Reproducción mínima: qué haría primero

No reproducir DreamCoder completo: exige un currículo y mucho cómputo. Orden por
coste/beneficio:

| Paso | Qué | Coste | Qué aprende el proyecto |
|---|---|---|---|
| 1 | **Stitch** sobre un corpus de programas pequeños | Medio | Si el library learning es tratable y con qué métricas |
| 2 | **CEGIS** mínimo (generar, verificar, corregir) sobre nuestro banco | Bajo | Si los contraejemplos baten a las soluciones |
| 3 | **Retrieval** convencional sobre MemDev-Bench o VibeMemBench | Medio | Cuál es la línea base real de la industria |
| 4 | **DreamCoder** a escala reducida | Alto | Si la política aprendida aporta sobre la biblioteca |

**Criterio de éxito de una reproducción:** obtener el mismo orden de magnitud en la
métrica principal del trabajo, no el mismo número exacto. Si no se consigue, se
documenta el fallo: también es información.

---

## 6. Regla de citación

1. Toda cifra lleva versión y, si es posible, tabla o figura.
2. Lo que proviene de una auditoría y no de lectura propia se marca `[verificar]`.
3. No se cita un trabajo para justificar una arquitectura; se cita por lo que
   demuestra y bajo qué condiciones.
4. Si no se ha reproducido, se dice.
