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

**Qué hace.** 87 tareas, 8 dominios, 18 configuraciones modelo–harness; skills
curadas por expertos vs autogeneradas por el agente, con verificadores
deterministas.

**Resultados.** Skills curadas: 33,9% → 50,5% (+16,6 pp). Skills autogeneradas:
−8,1 a −11,5 pp en tres configuraciones. 1–3 skills funcionan mejor que 4+;
skills compactas mejor que documentación exhaustiva.

**Por qué importa.** Es la objeción más directa a CUMULUS: si el agente genera sus
propios procedimientos desde experiencias imperfectas, ¿por qué serán comparables
a los curados? Los tests no bastan; hay que demostrar calidad de inducción.

**Referencia:** arXiv:2602.12670; skillsbench.ai.

## 8. How Well Do Agentic Skills Work in the Wild (Liu et al., 2026)

**Qué hace.** 34.198 skills reales; evalúa selección, retrieval y adaptación en
SkillsBench y Terminal-Bench 2.0.

**Resultados.** El beneficio cae al pasar de skills curadas a retrieval desde
34k. Claude Opus 4.6: 55,4% con carga forzada, 38,4% con retrieval sin curadas,
35,4% sin skills. El refinamiento específico de consulta recupera en 7/9
configuraciones; Terminal-Bench 57,7% → 65,5%.

**Por qué importa.** La selección/adaptación es el cuello, no la disponibilidad.

**Referencia:** arXiv:2604.04323.

## 9. Lectura de conjunto

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

## 10. Consecuencia para Open Human Memory

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
