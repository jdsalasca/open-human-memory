# 09 — Antecedentes 2026 (cuarta ola): expansión de capacidad y internalización

La cuarta ola ataca la ambición más reciente: no solo recordar, sino **expandir
capacidades**, **aprender a gestionar la memoria** y **medir el uso real**. Varios
trabajos se acercan al objetivo de Open Human Memory más que CUMULUS o JANUS.

## 1. Mem²Evolve — coevolución de experiencia y capacidades (Cheng et al., ACL 2026)

**Qué hace.** Dos memorias: **Experience Memory** (lecciones de trayectorias) y
**Asset Memory** (herramientas y agentes expertos ejecutables). La experiencia
guía la creación de activos; los activos generan nueva experiencia. Ciclo
forward–backward de expansión de capacidad y destilación.

**Resultados.** 6 categorías, 8 benchmarks; +18,53% sobre LLM estándar, +11,80%
sobre agentes que solo evolucionan experiencia, +6,46% sobre solo activos. En
GAIA, +57,84% partiendo de solo búsqueda web.

**Por qué importa.** Es el antecedente más cercano a "expansión de competencia":
el sistema crea herramientas y agentes nuevos, no solo recuerdos.

**Qué deja abierto.** Depende de sandbox para ejecutar código generado; no mide
transferencia composicional controlada ni costo longitudinal.

**Referencia:** arXiv:2604.10923; ACL 2026, pp. 20784–20831.

## 2. MemSkill — aprender a gestionar la memoria (Zhang et al., 2026)

**Qué hace.** Convierte las operaciones de memoria en **memory skills**
aprendibles: controller (selecciona skills), executor (aplica), designer (refina
y crea skills desde casos difíciles). RL con señal de tarea; rollback si una
actualización degrada.

**Resultados.** LoCoMo, LongMemEval, HotpotQA, ALFWorld; mejora y generaliza.
Las skills evolucionan de específicas a más generales.

**Por qué importa.** El **metaprendizaje del gestor de memoria** que el programa
v3 creía incipiente ya existe.

**Qué deja abierto.** No resuelve composición conceptual ni transferencia a
familias estructuralmente nuevas; su unidad es la operación de memoria, no la
competencia.

**Referencia:** arXiv:2602.02474.

## 3. VibeMemBench — memoria para coding agents en repos reales (Fan et al., 2026)

**Qué hace.** 111 tareas de 90 repositorios SWE-rebench V2 y 3.634 trayectorias
históricas. Cada tarea conserva una experiencia cuya utilidad fue verificada por
ejecución. Compara inyección directa de experiencia verificada contra cuatro
sistemas de memoria que deben construir y recuperar.

**Resultados.** La inyección directa mejora la resolución en 4 de 5 solvers
(+1,1 a +4,5 pp) y reduce pasos. Pero **11 de 12 pares solver–sistema de memoria
no superan la línea base sin memoria**. La forma del registro importa; el mismo
registro ayuda a un solver débil y perjudica a uno fuerte.

**Por qué importa.** Separa "la experiencia útil existe" de "el sistema de memoria
la entrega y el agente la usa". Es el mejor argumento para medir en el punto de
uso.

**Referencia:** arXiv:2609.23570.

## 4. MemUse — delivered, not used (Xu, Li y Xu, 2026)

**Qué hace.** Evalúa cada entrega de memoria contra lo que el agente ya podía ver,
siguiendo acciones y consecuencias en 8.000 episodios de SWE-bench Verified.

**Hallazgo.** 89 de 383 episodios con uso beneficioso fallaron; 5 de 16 con uso
dañino pasaron. El resultado de la tarea oculta el efecto de la memoria.

**Por qué importa.** Medir recall o éxito agregado no dice si la memoria cambió
la decisión.

**Referencia:** arXiv:2611.01718.

## 5. PaMER — señales de memoria antes de actuar (2026)

**Qué hace.** Estudia el estado oculto antes de cada acción: predice necesidad de
compresión (AUROC 0,831) y de recall (0,765). Recent2 (26% del contexto) preserva
la mayor parte de la señal; la evidencia histórica selectiva recupera lo que la
recencia pierde. Propone compresión guiada por estado + retrieval de evidencia.

**Por qué importa.** Ofrece una alternativa al controlador externo que examina
todo el historial: usar el estado del propio modelo como señal.

**Límite:** los probes pueden estar decodificando la noción del anotador; no son
mecanismo causal.

**Referencia:** arXiv:2609.27286.

## 6. MDSKILL — internalizar skills en la política (Jin et al., 2026)

**Qué hace.** Organiza skill memories en tres vistas (grounding, planning,
control) y las destila en una política compartida con on-policy self-distillation.
Selecciona skills porvalor dinámico y evita ruido/entrelazamiento.

**Resultados.** Hasta +7,1% en ALFWorld y +8,1% en WebShop sobre SOTA, sin teacher
externo; mejora también en la rama sin skills (internalización).

**Por qué importa.** Es el puente entre memoria procedimental externa y
aprendizaje paramétrico: la línea híbrida que el programa v3 pide.

**Referencia:** arXiv:2611.05313.

## 7. SkillsBench — skills curadas vs autogeneradas (2026)

**Qué hace.** Evalúa skills curadas por expertos frente a skills autogeneradas por
el agente, con verificadores deterministas.

**Resultados (versión arXiv:2602.12670v2, 86 tareas, 11 dominios).** Skills
curadas: +16,2 pp de media. Skills autogeneradas: **sin beneficio medio** en la
evaluación considerada. 1–3 skills funcionan mejor que 4+; skills compactas mejor
que documentación exhaustiva.

> **Corrección de versión.** Una versión anterior de este repositorio citaba 87
> tareas, 8 dominios, +16,6 pp y −8,1/−11,5 pp. Esas cifras corresponden a otra
> versión del manuscrito. Toda cifra de este documento debe citarse con la versión
> exacta; el protocolo `25-protocolo-fuentes.md` ya lo exige y aquí no se cumplía.

**Por qué importa.** Es la objeción más directa a CUMULUS: si el agente genera sus
propios procedimientos desde experiencias imperfectas, ¿por qué serán comparables
a los curados? Los tests no bastan; hay que demostrar calidad de inducción.

**Referencia:** arXiv:2602.12670 (v2); skillsbench.ai.

## 8. How Well Do Agentic Skills Work in the Wild (Liu et al., 2026)

**Qué hace.** 34.198 skills reales; evalúa selección, retrieval y adaptación en
SkillsBench y Terminal-Bench 2.0.

**Resultados.** El beneficio cae al pasar de skills curadas a retrieval desde
34k. Claude Opus 4.6: 55,4% con carga forzada, 38,4% con retrieval sin curadas,
35,4% sin skills. El refinamiento específico de consulta recupera en 7/9
configuraciones; Terminal-Bench 57,7% → 65,5%.

**Por qué importa.** La selección/adaptación es el cuello, no la disponibilidad.

**Referencia:** arXiv:2604.04323.

## 9. Programación por ejemplos y DreamCoder

- **PBE / FlashFill** (Gulwani, 2011): sintetizar un programa a partir de
  ejemplos input→output; la ambigüedad y el tamaño del espacio son el problema
  central.
- **DreamCoder** (Ellis et al., 2021): resuelve tareas, descubre subestructuras
  reutilizables y **aprende también la política de búsqueda** con wake-sleep. No
  es solo una biblioteca: es biblioteca + búsqueda adaptativa.
- **Stitch** (Bowers et al., 2023): descubrimiento de abstracciones por
  compresión *top-down*; reporta mejoras de varios órdenes de magnitud en tiempo
  frente a algoritmos previos de library learning. Es la referencia obligada para
  saber si compilar abstracciones es económicamente viable.
- **LILO** (Grand et al., 2024): síntesis guiada por LLM + compresión simbólica +
  **documentación** de las abstracciones. El antecedente directo de «artefacto
  ejecutable con explicación natural».
- **Options** (Sutton, Precup y Singh, 1999): una habilidad temporalmente
  extendida tiene condición de iniciación, política interna y condición de
  terminación. Una macro determinista no es una option: le falta la política de
  activación.
- **EvoMemBench** (2026): compara sistemas de memoria y muestra que los
  baselines de contexto largo siguen siendo competitivos.
- **ContinualSkillBench** (2026): aprendizaje continuo de habilidades en cinco
  dominios; conservar contexto y feedback resulta comparable a mantener una
  biblioteca explícita en algunas configuraciones.
- **SkillLearnBench** (2026): las mejoras de habilidades autogeneradas no son
  uniformes entre tareas, modelos y métodos; hay deriva al depender del propio
  feedback.
- **SWE-Skills-Bench** (2026): las habilidades no benefician uniformemente a los
  agentes.

**Implicación:** el `MEM-E` del 002 es PBE exhaustivo sobre cuatro primitivas y
profundidad dos; no es una innovación algorítmica. El 003 es un paso mínimo tipo
DreamCoder: cuenta pares frecuentes. **El 004-A midió ese paso y no supera a la
búsqueda profunda**, así que la contribución no puede estar en «aprender macros»:
está en demostrar que las abstracciones mejoran el aprendizaje futuro a igual
costo, cosa que Stitch, LILO y DreamCoder ya persiguen con más maquinaria.

> **Nota de verificación.** ContinualSkillBench, SkillLearnBench y
> SWE-Skills-Bench provienen de la auditoría y están pendientes de lectura directa
> de la versión primaria. No se citan cifras suyas en papers hasta verificarlas.

## 9.5 Matriz de mecanismos y niveles de evidencia

Una revisión por mecanismos, no por cronología. Cada fila es un cuello de botella
distinto; ninguna técnica resuelve todas.

| Mecanismo | Antecedente principal | Comparación necesaria |
|---|---|---|
| Bibliotecas de conceptos | DreamCoder, Stitch, LILO | Compresión y transferencia |
| Aprendizaje activo | Angluin (1987), CEGIS | Consultas hasta identificar la hipótesis |
| Reutilización de búsqueda | LPA*, D* Lite | Cómputo evitado sin perder calidad |
| Opciones jerárquicas | Sutton, Precup y Singh (1999) | Condiciones de activación y terminación |
| Aprender a aprender | MAML, metaprendizaje | Experiencias hasta competencia en familias nuevas |
| Expansión de herramientas | Mem²Evolve | Tareas nuevas resueltas, no solo activos creados |
| Memoria para programación | VibeMemBench, MemDev-Bench | Éxito real, transferencia negativa y trazas completas |
| Compresión con utilidad | Information Bottleneck, utilidad condicionada | Desempeño por costo, no solo tamaño |

**MemDev-Bench** (2026) es el antecedente más incómodo para CUMULUS: con 555 tareas
principales y 4.869 históricas sobre repositorios reales, encuentra que la memoria
ayuda a localizar y editar, pero también **puede romper tareas antes resolubles**, y
que las trayectorias completas a veces baten a los sistemas que comprimen. Es
decir: consolidar puede eliminar el proceso de resolución que todavía hacía falta.
Eso convierte la compactación en una pregunta sobre qué se puede borrar, no sobre
cuánto ocupa.

### Niveles de evidencia del proyecto

No es una escala universal de calidad científica; es el alcance de lo que podemos
afirmar.

| Nivel | Evidencia | Estado del proyecto |
|---|---|---|
| E0 | Idea teórica o analogía | CUMULUS, JANUS |
| E1 | Mecanismo implementado | Macros del 003, controlador del 005 |
| E2 | Comparación controlada con líneas base fuertes | 004-A y 005-A (locales) |
| E3 | Beneficio en varias distribuciones | **No alcanzado** |
| E4 | Reproducción independiente con tareas reales | **No alcanzado** |
| E5 | Mejora longitudinal con costo controlado | **No alcanzado** |

El 005-A añade un dato E2 que el 004-A no tenía: con continuidad total, misma
cobertura y **41,8 % menos pasos ejecutados**. Sigue siendo un entorno de cuatro
primitivas y 14 comportamientos.

## 10. Lectura de conjunto

| Capacidad | Ya cubierta | Sigue abierto |
|---|---|---|
| Expandir capacidades creando activos | Mem²Evolve | Medir transferencia composicional controlada |
| Aprender a gestionar memoria | MemSkill | Integrar con competencias, no solo operaciones |
| Entregar experiencia útil | VibeMemBench | Cómo hacer que el agente la use |
| Medir uso real | MemUse | Longitudinal con costo y daño |
| Control por estado interno | PaMER | Causalidad de las señales |
| Internalizar skills | MDSKILL | Qué internalizar y cuándo |
| Calidad de skills autogeneradas | SkillsBench | Inducción verificable, no solo tests |
| Retrieval realista | Skill-Usage | Adaptación a familias nuevas |

## 11. Consecuencia para Open Human Memory

Ninguna de las piezas es nueva. La contribución posible se reduce a:

1. **Diagnóstico controlado** que separe reconocimiento, retrieval, procedimiento
   y composición (Prototipo 002).
2. **Transferencia composicional** como criterio, no solo reutilización.
3. **Curva longitudinal \(G(n)\)** con costo descompuesto y deriva.
4. **Certificados de evidencia** (JANUS-C) solo si el diagnóstico muestra que la
   verificación es el cuello.

CUMULUS no puede afirmar que sus skills autogeneradas igualan a las curadas; debe
medirlo. JANUS no puede afirmar causalidad; debe medir identificabilidad.
Mem²Evolve es el competidor más directo en expansión de capacidad.
