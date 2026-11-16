# Extracción de evidencia

**Fecha:** 16 de noviembre de 2026. Cifras tomadas del resumen indexado en OpenAlex
salvo donde se indica. `[título]` = identificado pero no extraído.

## A. Benchmarks y evaluaciones (9)

| ID | Trabajo | Año | Qué mide | Resultado verificado | Límite |
|---|---|---|---|---|---|
| B1 | **SkillsBench** (arXiv:2602.12670) | 2026 | Skills curadas vs sin skills | **87 tareas, 8 dominios, 18 configuraciones; 33,9 % → 50,5 % (+16,6 pp)**; ≤3 módulos mejor que bundles grandes | La auditoría reporta 86 tareas/11 dominios/+16,2 pp para otra versión: **hay versiones** |
| B2 | **MemDev-Bench** (arXiv:2610.27524) | 2026 | Memoria sobre historiales de repo con relevancia anotada | **555 tareas base + 4.869 históricas**; mejora localización/edición; **también causa fallos en tareas antes resolubles** | Preprint |
| B3 | **VibeMemBench** (arXiv:2609.23570) | 2026 | Memoria en tareas ejecutables de repo | **111 objetivos, 90 repos, 3.634 trayectorias**; experiencia verificada por ejecución y transferida a **5 solvers held-out** | Preprint |
| B4 | **ContinualSkillBench** (arXiv:2608.03874) | 2026 | Aprendizaje continuo de skills en flujo | **5 dominios × 100 tareas**; contexto+feedback ≈ biblioteca explícita; GPT-4o acumula más y reutiliza menos | Preprint |
| B5 | **SkillLearnBench** (arXiv:2604.20087) | 2026 | Métodos de generación de skills | **20 tareas, 15 subdominios**; todos mejoran sobre no-skill; **ningún método gana en todo**; más backbone no ayuda | Preprint |
| B6 | **MemCalib** (arXiv:2609.24259) | 2026 | Uso adecuado de la memoria | Modelos frontera **sobre/infrautilizan**; GRPO y self-distillation mejoran una dirección y empeoran la otra | Preprint |
| B7 | **MemUse** (arXiv:2611.01718) | 2026 | Uso en el punto de entrega | **8.000 episodios SWE-bench Verified, 3 sistemas**; resolve ±0,4 pp del baseline sin memoria; mayoría de entregas irrelevantes; **23,2 % de usos beneficiosos igual fallaron; 5/16 usos dañinos igual acertaron** | Preprint |
| B8 | **MemoryArena** (arXiv:2602.16313) | 2026 | Memoria-acción en multi-sesión interdependiente | Memoria y acción acopladas, no aisladas | Preprint |
| B9 | **AgentCL** (arXiv:2606.02461) | 2026 | Evaluación rigurosa de aprendizaje continuo | Dependencias cross-task en streams; crítica a benchmarks que reciclan datasets | Preprint |

## B. Sistemas de memoria y auto-evolución (8)

| ID | Trabajo | Año | Mecanismo | Resultado verificado | Límite |
|---|---|---|---|---|---|
| S1 | **Mem²Evolve** (ACL 2026) | 2026 | Experience Memory + Asset Memory | **+18,53 % vs LLM, +11,80 % vs solo experiencia, +6,46 % vs solo activos**; 6 categorías, 8 benchmarks | Código en preparación según la auditoría; sin transferencia de modelo |
| S2 | **MemEvolve** (arXiv:2512.18746) | 2025 | Meta-evolución de la arquitectura de memoria | La arquitectura de memoria también se adapta | Preprint |
| S3 | **MUSE-Autoskill** (arXiv:2605.27366) | 2026 | Ciclo de vida de skills | Supera a Hermes/Codex/Claude Code; **skills autocreadas superan a humanas en el subconjunto cubierto de SkillsBench** | Contradice parcialmente a B1 |
| S4 | **Trace2Skill** (EMNLP 2026) | 2026 | Destila lecciones de trayectorias | Consolida trayectorias en un directorio de skills | — |
| S5 | **SkillGen** (arXiv:2605.10999) | 2026 | Inducción contrastiva éxito/fracaso | Skill única, auditable, generada desde trayectorias | — |
| S6 | **CoEvoSkills** | 2026 | Skills auto-evolutivas con verificación co-evolutiva | `[título]` | — |
| S7 | **SkillOpt** | 2026 | Estrategia ejecutiva para skills | `[título]` | — |
| S8 | **Proof-Gated Skill Compilation** (NeurIPS 2026 workshop) | 2026 | Solo persisten programas ejecutados por el harness contra ground truth | **538 aserciones de verificación de teachers; 52 confirmadas; 486 fabricaciones rechazadas; 98,9 % en 90 tareas derivadas de ARC-AGI-2** | Workshop; benchmark pequeño |

## C. Aprendizaje continuo y transferencia (5)

| ID | Trabajo | Año | Qué mide | Resultado verificado | Límite |
|---|---|---|---|---|---|
| C1 | **EvoAgentBench** (EMNLP Findings 2026) | 2026 | Transferencia de **procedimientos**, no información | 4 dominios; ability graphs; cada tarea de test respaldada por entrenamiento verificado | Muy reciente |
| C2 | **SelfImprove-Bench** (arXiv:2611.02797) | 2026 | Ganancia de capacidad vs ajuste al escenario | Separa Explorar/Planificar/Razonar; escenarios no vistos | Preprint |
| C3 | **SWE-Bench-CL** (arXiv:2507.00014) | 2025 | Streams cronológicos de issues | Acumulación, transferencia y olvido catastrofico | Preprint |
| C4 | **Skill Following** (EMNLP Findings 2026) | 2026 | Uso efectivo de skills con RAE | **Lift agregado positivo pero RAE negativo** en varios modelos; 17 LLMs | Preprint/Findings |
| C5 | **Agent Self-Improvement with Frozen Weights** (arXiv:2611.11342) | 2026 | Notas de fallos con modelo congelado | **+4,0 pp** vs notas sin fallos; **~60 %** de la mejora viene del proceso de seleccionar; en conversaciones completas **sin mejora demostrada** | Un modelo, un dominio |

## D. Fallos, deriva y límites (6)

| ID | Trabajo | Año | Hallazgo | Cifra |
|---|---|---|---|---|
| F1 | **More Skills, Worse Agents?** (arXiv:2605.24050) | 2026 | *Skill shadowing*: la biblioteca degrada al crecer | **hasta −21 %** al pasar a 202 skills |
| F2 | **Contextual Agentic Memory is a Memo** (arXiv:2604.27707) | 2026 | Retrieval no es memoria; techo de generalización composicional | Argumento, sin cifra |
| F3 | **SkillEvoReg** (arXiv:2609.30861) | 2026 | Sobreajuste de la evolución de skills; validación por contraejemplos | — |
| F4 | **RSE-Bench** (arXiv:2610.19910) | 2026 | El ruido no adversarial durante el aprendizaje **persiste** en las reglas | 4 dominios, 6 benchmarks |
| F5 | **Skill Drift** (arXiv:2605.10990) | 2026 | Deriva como violación de contrato de entorno | Contratos ejecutables |
| F6 | **Bemula** (arXiv:2610.18052) | 2026 | Olvido a petición | 50 diálogos, 135 peticiones, 1.742 preguntas |

## E. Coste y estructura (3)

| ID | Trabajo | Año | Hallazgo | Cifra |
|---|---|---|---|---|
| E1 | **STRATUM** (2026) | 2026 | Coste de representar conocimiento | **~4 GB texto vs ~298 TB KV fp16** por 1e9 tokens (70B); mediana de fix: 2 archivos; cierre de imports 2,7–9,9 % del repo |
| E2 | **Measure Before You Manage** (arXiv:2608.31057) | 2026 | Heterogeneidad de la memoria de trabajo | 55 trayectorias; objetos con perfiles distintos |
| E3 | **MemEvoBench** (arXiv:2604.15774) | 2026 | Deriva por memoria contaminada | 7 dominios, 36 tipos de riesgo, 20 entornos |

## F. Fundacionales (10)

| ID | Trabajo | Año | Aporte | Canal |
|---|---|---|---|---|
| G1 | DreamCoder | 2021 | Biblioteca + política de búsqueda | Herramientas + política |
| G2 | Stitch | 2023 | Library learning por compresión top-down | Herramientas |
| G3 | LILO | 2024 | Compresión + documentación | Herramientas + representación |
| G4 | CEGIS / SyGuS | 2013 | Aprender de contraejemplos | Representación |
| G5 | Angluin | 1987 | Consultas que discriminan | Información |
| G6 | LPA* / D* Lite | 2004 | Reutilizar búsqueda | Herramientas |
| G7 | Options | 1999 | Inicio, política, terminación | Política |
| G8 | MAML | 2017 | Adaptación rápida | Parámetros |
| G9 | Information Bottleneck | 1999 | Comprimir preservando lo relevante | Representación |
| G10 | Metarrazonamiento | 1991 | Valor neto de decidir | Política |

## Nota de verificación

- **B1**: la versión indexada (consultada 2026-11-16) declara 87 tareas/8
  dominios/+16,6 pp. La auditoría reporta 86/11/+16,2 para la versión arXiv que
  consultó. **Se cita la versión consultada y se deja constancia del desacuerdo.**
- **S1**: los porcentajes están en el resumen del ACL Anthology; la cifra de GAIA
  (+57,84 %) que citaba nuestro documento **no aparece** en el resumen y se retira.
- **AdaMem** se excluyó: controla qué **escribir**, no la adquisición de
  competencia. La descripción de la auditoría («memoria adaptativa durante la
  ejecución») no coincide con su resumen.
