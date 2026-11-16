# 06 — Competidores directos (2026): lo que ya hace CUMULUS

Este documento existe por una razón incómoda: la revisión externa encontró
cuatro trabajos de 2026 que cubren buena parte de lo que CUMULUS presentaba como
novedad. Ignorarlos sería deshonesto. La conclusión no es que la idea muera, sino
que la **afirmación de novedad debe reducirse** y el hueco debe redefinirse.

## 1. Zep Agent Skills — *Learning by Doing* (Chalef et al., 2026)

**Qué hace.** Servicio de producción que convierte trazas verificadas en skills
versionadas. Cada intento se registra como Trace con eventos ordenados, resultado
y **fuerza de verificación** (ninguna, auto-reportada, independiente). Un
compilador con roles Reflector y Curator convierte trazas en contratos de skill
con citas por evento, gates de admisión, versiones inmutables, escaneos de
seguridad y un ranking de búsqueda actualizado por uso verificado. Entrega vía
MCP en el formato abierto Agent Skills (SKILL.md).

**Resultados.** Protocolo teacher–executor: un modelo fuerte resuelve; las skills
se compilan y se dan a modelos más débiles. Mejora la tasa de éxito de tres
ejecutores (GPT-6 Luna, Claude Haiku 5.5, DeepSeek V4.1 Flash) entre 4,5 y 18,8
puntos, en 26 configuraciones, con reducción de tokens de hasta 45% en algunos
benchmarks. En ALFWorld, Qwen3-8B mejora 32,6 puntos sin entrenamiento.

**Lo que ya cubre de CUMULUS.** Traza, Forja (compilación), Canon (versiones,
admisión, citas), Puente (formato abierto, MCP, transferencia entre modelos),
gobernanza (escaneos, borrado, namespace).

**Lo que no hace.** No valida causalmente: sus gates comprueban estructura,
citas y seguridad, no que el procedimiento sea la causa del éxito. El propio
paper reconoce que no demuestra que cada skill admitida sea verdadera o inocua.
La transferencia a tareas nuevas no es el foco de los benchmarks principales.

## 2. MSCE — *From Memory to Skills* (Tang et al., 2026)

**Qué hace.** Framework training-free de co-evolución memoria–habilidad con tres
niveles: L1 trazas de decisión, L2 políticas procedurales (trigger, pasos,
verificación, límites de aplicabilidad) y L3 cognición del entorno (hechos y
restricciones). "Cristaliza" políticas con ganancia estimada positiva en skills
llamables con evidencia, límites, guía y confiabilidad. Backfilling de valor
ponderado por reflexión para propagar feedback escaso.

**Resultados.** Mejora agregada en EvoAgentBench y LoCoMo, transferencia
cross-domain positiva (+3,93 puntos promedio en seis pares) y mejora continua.

**Lo que ya cubre de CUMULUS.** Compilación de experiencia en políticas, evidencia
ligada, límites de aplicabilidad, verificación, gobernanza de promoción,
transferencia entre dominios.

**Lo que no hace.** Sus propios autores lo dicen: las ganancias son **estimaciones
heurísticas, no efectos causales**; no garantizan que una política promovida
cause el éxito bajo intervención contrafactual. Este es el hueco de JANUS.

## 3. AFTER — *Managing Procedural Memory in LLM Agents* (Belikova et al., 2026)

**Qué hace.** Benchmark de 382 tareas empresariales, seis roles profesionales y
22 habilidades procedurales. Evalúa transferencia de skills entre tareas, roles y
**model backbones**. Estudia control, adaptación y evaluación de la memoria
procedural.

**Lo que ya cubre de CUMULUS.** La pregunta por la transferencia entre modelos y
roles deja de ser original; ya tiene benchmark y evidencia empírica.

**Lo que no hace.** No propone una arquitectura de memoria; mide.

## 4. Demystifying Agent Skills (Jiang et al., 2026)

**Qué hace.** Experimentos controlados sobre cuándo ayudan las skills, por qué
funcionan y dónde fallan. Taxonomía de tres categorías y doce modos de uso;
documenta degradación de recuperación cuando crece la biblioteca. "Procedural
anchoring" explica 65,7% de los casos, frente a 4,5% de inyección de conocimiento
explícito.

**Lo que implica para CUMULUS.** Más skills no es mejor. La selección y la
recuperación son un cuello de botella de primer orden. CUMULUS trataba el Canon
como si promocionar fuera el problema; también lo es **elegir**.

## 5. Trace2Skill (Ni et al., 2026)

**Qué hace.** Destila trayectorias amplias en un directorio de skills declarativo
mediante analistas paralelos y consolidación. Las skills destiladas de un modelo
transferen a otras escalas, familias y tareas out-of-distribution. Las
trayectorias de error son una señal confiable por defecto.

**Lo que ya cubre de CUMULUS.** La transferencia de procedimientos entre modelos y
familias, y la idea de compilar desde trazas.

**Lo que no hace.** No resuelve la validación causal ni la gobernanza institucional.

## 6. Verify by Doing (Lin et al., 2026)

**Qué hace.** Co-evoluciona Actor y Evaluador con pesos fijos; el Evaluador
inspecciona artefactos y estado con herramientas, y sus hallazgos guían la
selección y la actualización de procedimientos de ejecución y verificación.

**Lo que implica para CUMULUS.** La verificación activa y la evolución del
evaluador son un frente vivo; un "auditor ciego" estático puede quedarse corto.

## 7. Mining Agent Skills from Production Traces (Kang et al., 2026)

**Qué hace.** Estudia cómo el muestreo de trazas, el acceso a etiquetas de éxito y
la forma de la skill (workflow vs ontología) afectan el rendimiento en benchmarks
empresariales. Los beneficios dependen del dominio; las etiquetas importan.

**Lo que implica para CUMULUS.** No hay una forma única de skill; la evidencia de
entrenamiento y la forma deben tratarse como variables experimentales.

## 8. CoALA (Sumers et al., 2023/2024)

**Qué hace.** Marco conceptual de arquitecturas cognitivas para agentes de
lenguaje: memoria de trabajo y largo plazo (semántica, episódica, procedural),
espacio de acciones internas/externas y ciclo de decisión.

**Lo que implica.** CUMULUS no inventa la distinción de memorias; la hereda. La
contribución debe estar en el mecanismo, no en la taxonomía.

## Matriz de competidores

| Sistema | Trazas | Verificación | Skill formal | Multi-modelo | Causal | Social | Longitudinal | Formato abierto |
|---|---|---|---|---|---|---|---|---|
| Zep Agent Skills | Sí | Fuerte (externa) | Contrato + citas | Sí (teacher–executor) | No | Namespace | Uso verificado | Agent Skills / MCP |
| MSCE | Sí (L1) | Reglas + evidencia | Política L2 + skill | Parcial | No (heurístico) | No | Evolución online | No |
| AFTER | Benchmark | Verificadores | 22 skills | Sí (backbones) | No | Roles | No | No |
| Trace2Skill | Sí | Éxito/error | Directorio declarativo | Sí (escalas/familias) | No | No | No | No |
| Verify by Doing | Sí | Evaluador activo | Procedimientos | Parcial | No | No | No | No |
| CUMULUS v0.1 | Sí | Quórum + ciega | SIR | Sí | Pretendida | Pod | Propuesto | Propuesto |
| JANUS | Sí + contrafactuales | Jerarquía causal | SIR + claim causal | Sí | Sí (propuesto) | Pod | Propuesto | Propuesto |

## Qué queda realmente abierto

1. **Validación causal de procedimientos.** Ninguno de los sistemas anteriores
   identifica el efecto causal de una habilidad; todos usan éxito observado,
   ganancia heurística o verificación de estructura. MSCE lo admite; Zep no lo
   promete.
2. **Contrafactuales como memoria.** Nadie guarda alternativas y resultados
   potenciales para asignar crédito.
3. **Deriva longitudinal real.** AFTER y Agent Skills prueban transferencia, no
   meses de cambios de modelo, API, requisitos y distribución.
4. **Selección bajo bibliotecas grandes.** Demystifying muestra que la
   recuperación se degrada; falta una política de selección calibrada.
5. **Gobernanza con errores correlacionados.** El quórum de agentes que comparten
   modelo y sesgos no es independencia.

## Consecuencia para CUMULUS

La afirmación "proponemos una arquitectura que convierte trazas verificadas en
habilidades portables y gobernadas" **ya no es defendible como novedad**. Zep
Agent Skills lo hace en producción; MSCE lo hace con gobernanza; Trace2Skill lo
hace con transferencia entre modelos.

CUMULUS debe reposicionarse como:

- un **protocolo de investigación** que replica y compara esos mecanismos con
  presupuesto igualado,
- una **especificación formal** de contrato ejecutable (SIR) y auditoría ciega,
- y, sobre todo, el **sustrato de JANUS** para la validación causal.

La novedad real se desplaza a JANUS: memoria contrafactual y promoción causal.
