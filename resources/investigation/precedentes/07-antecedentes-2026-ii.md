# 07 — Antecedentes 2026 (segunda ola): contrafactuales, control y anti-persistencia

La primera revisión obligó a reconocer que CUMULUS no inventaba la compilación de
trazas en skills. Esta segunda ola obliga a reconocer algo más incómodo: **JANUS
tampoco inventa la memoria contrafactual**. Varios trabajos de 2026 ya la
estudian, y uno de ellos la implementa con verificación ejecutable.

Este documento cataloga esos antecedentes y redefine el hueco.

## 1. COUNTERMEM (Pu, Tang y Zhang, 2026)

**Qué hace.** Después de una acción fallida, genera hasta cuatro alternativas
locales, las evalúa desde una copia o reset del mismo estado usando **modelos del
mundo ejecutables** (tests, proof checkers, SQL checkers, solvers). Solo guarda
las correcciones que mejoran el resultado, con:

- acción original y acción corregida;
- evidencia de la verificación;
- **condiciones de aplicabilidad**;
- estadísticas de reutilización;
- un selector DQN que decide usar o **saltar** la memoria.

**Resultados.** 12 benchmarks, 6 dominios; +12,6 pp promedio con gpt-oss-120b
sobre ReAct y Reflexion; reducción de tokens de 7,7–42,0% en cuatro dominios.
Ablaciones: sin verificación o sin almacenamiento persistente, las ganancias
caen; aplicar correcciones verificadas a decisiones no aptas **revierte** la
mejora. Eliminar la condición de aplicabilidad eleva la tasa de daño en tareas
parecidas de 11,8% a 34,2%.

**Lo que ya cubre de JANUS.** Contrafactuales verificados, condiciones de
aplicabilidad, selector de uso/skip, estado restaurado, evidencia ejecutable.

**Lo que no hace.** No mide acumulación longitudinal ni portabilidad entre
modelos; no distingue tipos de evidencia contrafactual más allá de la
verificación ejecutable; no aborda incertidumbre no resuelta ni conflicto
irreducible.

## 2. ConMem / MemAlign (Zhang et al., 2026)

**Qué hace.** Reformula la decisión de **retener** una memoria como inferencia
causal prospectiva. Genera tres sondas contrafactuales:

- **relevante:** ¿la memoria mejora una tarea futura que la necesita?
- **irrelevante:** ¿induce personalización donde no debería?
- **de riesgo:** ¿se filtra a otro contexto, entidad o tiempo?

Agrega un **Counterfactual Memory Treatment Effect (CMTE)** y decide almacenar o
no. Benchmark MemAlign: 1.079 casos, 40 personas, seis tipos de desalineación
(sobre-inferencia, atribución errónea, granularidad, privacidad, etc.). Reporta
75,16% de accuracy y 65,31% Macro-F1.

**Lo que ya cubre de JANUS.** Contrafactuales para admisión de memoria, no solo
para ejecución; auditoría de atribución; chequeos de invariancia y riesgo.

**Lo que no hace.** No identifica efectos causales de acciones en un entorno
secuencial; no mide acumulación ni transferencia entre modelos.

## 3. MemCon (Jiang et al., 2026)

**Qué hace.** Modela la gestión de memoria como un **MDP**: el controlador
decide cuándo recuperar, qué, cuánto, cuándo inyectar un plan, cuándo
re-consultar si el agente está atascado, cuándo consolidar y cuándo olvidar.
Backend-agnóstico; bandit contextual tabular con UCB; sin llamadas extra al LLM
para elegir la operación.

**Resultados.** 6 benchmarks, 3 frameworks, 3 backbones; mejoras de hasta 15,2
puntos y reducción de tokens de 5–20% en configuraciones reportadas. La ablación
del controlador solo aporta ~5,2 puntos en ALFWorld: **la política de acceso
importa independientemente del contenido**.

**Lo que implica.** Mucha de la complejidad de CUMULUS puede sustituirse por una
política de control más simple. El valor no está solo en qué se guarda, sino en
cuándo y cuánto se usa.

**Lo que no hace.** No resuelve causalidad; los propios autores dicen que los
beneficios de consolidar y olvidar no están establecidos.

## 4. When Errors Become Memories (Xiao et al., 2026)

**Qué hace.** Modelo causal estructural de propagación de errores en memoria
multi-turno. Distingue dos vías: actualización de memoria y feedback de la
pregunta. Interviene ambas y mide cuatro resultados: retención en memoria,
respuesta natural, sonda dirigida y preferencia probabilística.

**Hallazgo.** El efecto decae con la distancia, pero la vía de memoria es más
persistente; un error puede desaparecer de las respuestas naturales y seguir
latente en memoria o en la distribución. Reparar solo la memoria o solo el
diálogo deja residuo; reparar ambos casi lo elimina.

**Lo que implica.** La consolidación de una interpretación errónea no es un
detalle: se convierte en una causa persistente. La auditoría debe mirar la
memoria, no solo la salida.

## 5. Attributing Agent Failures to Their History Needs an Executed Counterfactual (Pakhomov y Nijkamp, 2026)

**Qué hace.** Propone un estándar: para atribuir una falla a la historia del
agente, hay que **ejecutar** un contrafactual desde un estado congelado,
alterando solo la historia visible, y reportar un **certificado de replay** con
la tasa de acuerdo entre la restauración y la referencia.

**Hallazgo.** Snapshots con el mismo hash, restaurados en procesos con la misma
semilla, coincidieron entre sí en 24/24 estados, pero difirieron de la
continuación viva en 9 y 20 de 24. Restaurar la posición del flujo aleatorio hizo
que los 24 coincidieran.

**Lo que implica.** JANUS no puede afirmar que identifica causas si no mide
primero si puede reproducir una trayectoria. La restauración no es un supuesto:
es una propiedad medida.

## 6. More Memory, Worse Agents (Wang, Panaganti y Zhou, 2026)

**Qué hace.** Describe el **error reproduction**: una abstracción errónea se
guarda, guía ejecuciones futuras, contamina las trazas y se re-deriva como nueva
abstracción. Propone **Anti-Persistence**: guardar trayectorias y resultados,
pero reconstruir la guía bajo demanda y descartarla después.

**Resultados.** Nueve configuraciones (3 benchmarks × 3 backbones): 59,9% de
éxito para Anti-Persistence frente a 53,5% para memoria de trayectorias, 49,0%
para abstracciones persistentes y 49,3% para ambas. Menor costo medio de llamadas
en las nueve. Los propios autores advierten que la evidencia de reproducción de
errores es asociacional.

**Lo que implica.** La apuesta de CUMULUS por un Canon permanente es una
hipótesis, no una verdad. En entornos cambiantes, persistir abstracciones puede
ser peor que reconstruirlas.

## 7. What Is This Memory Useful For? (Yang et al., 2026)

**Qué hace.** Mide la **utilidad condicionada a la tarea** de una memoria:
\(\Delta U(m,t) =\) recompensa con memoria − recompensa sin memoria, con el mismo
relleno de contexto y un lector congelado. La memoria se escribe sin ver la tarea
futura.

**Resultados.** En tareas de recall factual, las memorias que contienen la
respuesta ayudan más (+0,33 de recompensa frente a controles emparejados). Los
resúmenes y registros estructurados ayudan menos que el texto crudo. En los
benchmarks de ingeniería de software y programación científica probados, **ni
siquiera la memoria cruda tuvo efecto medible**.

**Lo que implica.** La utilidad no es una propiedad intrínseca de la memoria;
depende de la tarea, del lector y del formato. "Guardar más" no es "mejorar más".

## 8. TANGLE (Yang et al., 2026)

**Qué hace.** Benchmark de conflictos **irreducibles** en memoria personal: 541
instancias, 40 personas, tres tipos (contexto particionado, oscilación de
conducta, contradicción de fuentes). Evalúa percepción del conflicto, razonamiento
causal, calibración de confianza, búsqueda de aclaración y fidelidad.

**Hallazgo.** Los modelos detectan el conflicto mejor de lo que actúan sobre él:
hay una brecha reconocimiento–acción. Las políticas fijas (siempre preguntar,
siempre condicionar, siempre lo más reciente) fallan. Propone CAAP con acciones
`commit`, `conditionalize`, `clarify`, `verify`, `defer`, `reversible_trial`.

**Lo que implica.** Una memoria madura no solo resuelve; también **preserva lo
no resuelto** y elige una acción adecuada a la evidencia. Esto es central para la
tercera línea del programa.

## 9. Métodos de atribución contrafactual

- **Causal Agent Replay** (2026): intervención y replay para atribuir fallas a
  pasos específicos.
- **REFLECT** (2026): atribución de fallas silenciosas con intervención.
- **DoVer**, **Who&When Pro**, **AgentDebug**, **CausalFlow**, **TraceElephant**:
  re-ejecutan desde checkpoints o prefijos para probar explicaciones.

**Lectura:** el replay contrafactual ya es una línea metodológica activa. JANUS
no puede reclamarlo como nuevo; debe aportar un mecanismo de memoria que lo use
con identificación y gobernanza.

## 10. Qué queda después de esta segunda ola

| Capacidad | Ya existe | Sigue abierto |
|---|---|---|
| Compilar trazas en skills | Zep Agent Skills, MSCE, Trace2Skill | Comparación con presupuesto igualado |
| Contrafactual verificado | COUNTERMEM | Identificación bajo estado parcialmente oculto |
| Admisión contrafactual de memoria | ConMem | Efectos secuenciales y acumulación |
| Control de acceso a memoria | MemCon | Política calibrada por riesgo y costo |
| Propagación de errores | When Errors Become Memories | Detección temprana y reparación |
| Replay con certificado | Pakhomov y Nijkamp | Aplicación a memoria de agentes |
| Anti-persistencia | More Memory, Worse Agents | Cuándo persistir y cuándo reconstruir |
| Utilidad condicionada a tarea | Yang et al. | Medición en tareas procedimentales |
| Conflicto irreducible | TANGLE | Memoria que preserva y actúa bajo incertidumbre |
| Portabilidad entre modelos | AFTER, Trace2Skill, Zep | Medición longitudinal con deriva |
| Incertidumbre/ignorancia | Casi nada | Memoria de lo que no se sabe y agenda experimental |

## 11. Consecuencia para el proyecto

JANUS ya no puede presentarse como "la primera memoria contrafactual". Su
contribución debe reducirse a algo más estrecho y más difícil:

1. **Identificabilidad como propiedad del recuerdo**, no como promesa: cada
   registro declara qué se puede estimar, con qué supuestos y qué falta.
2. **Tres dimensiones de validación** —fiabilidad, causalidad, portabilidad— en
   lugar de una sola puerta causal.
3. **Memoria de la incertidumbre y de la ignorancia**, con agenda de experimentos
   pendientes.
4. **Política de uso por riesgo**: no todo requiere causalidad; lo irreversible
   sí exige más evidencia.
5. **Anti-persistencia selectiva**: persistir hechos y trayectorias; reconstruir
   abstracciones cuando el contexto cambió.
6. **Evaluación longitudinal con deriva real**, no solo ciclos simulados.

Eso es lo que se desarrolla en `24-programa-de-investigacion-v2.md` y en
`papers/janus-v0.2.md`.
