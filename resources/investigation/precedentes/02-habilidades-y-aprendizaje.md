# 02 — Habilidades y aprendizaje de la experiencia

## Voyager (Wang et al., 2023)

**Qué hace.** Agente abierto en Minecraft con tres piezas: currículo automático,
biblioteca de habilidades en código y autoverificación. Las habilidades exitosas
se guardan como funciones ejecutables y se recuperan por similitud.

**Qué resuelve.** Demuestra que una biblioteca de habilidades ejecutables puede
acumular competencia en un entorno abierto, sin reentrenar el modelo.

**Qué no resuelve.** Un solo entorno, un solo modelo, un solo lenguaje de
herramientas. No hay contrato de precondiciones/postcondiciones, ni validación
cruzada, ni olvido, ni gobernanza.

**Lección.** Guardar código ejecutable es mejor que guardar prosa; pero el código
sigue atado al runtime.

## Agent Workflow Memory (Wang, Mao, Fried y Neubig, 2024)

**Qué hace.** Induce *workflows* reutilizables a partir de trayectorias exitosas y
los ofrece al agente cuando la tarea se parece. Los workflows son rutinas
parametrizadas, no código.

**Qué resuelve.** Extrae la estructura repetida de la experiencia y reduce la
exploración.

**Qué no resuelve.** No hay postcondiciones ejecutables, ni verificación
independiente, ni portabilidad entre modelos. La similitud de tarea decide la
reutilización.

**Lección.** La parametrización es el primer paso de la abstracción; falta el
contrato.

## ExpeL (Zhao et al., 2024)

**Qué hace.** El agente acumula experiencias y extrae *insights* en lenguaje
natural; en inferencia recupera los insights relevantes y los usa como guía.

**Qué resuelve.** Muestra que la experiencia se puede destilar en conocimiento
reutilizable sin actualizar pesos.

**Qué no resuelve.** Los insights son texto, no procedimientos verificables. No
hay garantía de que el insight sea causalmente correcto.

**Lección.** La destilación es útil, pero sin verificación es un rumor con buena
redacción.

## Reflexion (Shinn et al., 2023)

**Qué hace.** Refuerzo verbal: el agente reflexiona sobre el fracaso, escribe una
lección y la usa en el siguiente intento.

**Qué resuelve.** Mejora en tareas episódicas sin entrenamiento.

**Qué no resuelve.** No acumula entre sesiones ni entre tareas; la lección vive
en el contexto.

**Lección.** La reflexión es una forma de aprendizaje de un solo episodio; para
que sea acumulativa necesita persistencia y verificación.

## Agentic Context Engineering / ACE (Zhang, Q., et al., 2025)

**Qué hace.** Trata el contexto como un *playbook* que evoluciona: genera,
reflexiona y cura estrategias. Acumula tácticas y correcciones sin reentrenar.

**Qué resuelve.** Es el antecedente más cercano a "memoria procedimental
textual". Demuestra que un playbook puede mejorar con el uso.

**Qué no resuelve.** El playbook es texto dependiente del modelo; no hay IR
agnóstica, ni ablación causal, ni auditoría ciega, ni portabilidad medida.

**Lección.** La evolución de contexto funciona; el siguiente paso es separar
semántica de sintaxis.

## Memento (Zhou et al., 2025)

**Qué hace.** Memoria basada en casos + planner–executor. El agente aprende de
experiencia sin actualizar pesos; recupera casos similares y los usa como
referencia.

**Qué resuelve.** Aprendizaje continuo barato y sin entrenamiento; buen
rendimiento en tareas de investigación.

**Qué no resuelve.** Los casos son episodios, no procedimientos. La similitud de
caso no garantiza transferencia estructural.

**Lección.** El case-based reasoning es un puente; falta la compilación a
procedimiento.

## SkillWeaver (Zheng et al., 2025)

**Qué hace.** Agentes web sintetizan habilidades reutilizables como APIs,
las refinan y las componen. Hay transferencia entre agentes.

**Qué resuelve.** Skill synthesis y composición en un dominio amplio (web).

**Qué no resuelve.** Dominio específico; sin contrato formal, sin validación
causal, sin portabilidad entre modelos.

**Lección.** Las habilidades como APIs son un buen formato; el contrato y la
verificación son el siguiente paso.

## Darwin Gödel Machine (Zhang, J., et al., 2025)

**Qué hace.** Modifica su propio código, evalúa variantes en benchmarks y
selecciona las mejores en un archivo abierto.

**Qué resuelve.** Auto-mejora abierta a nivel de código, con selección empírica.

**Qué no resuelve.** No es memoria: es evolución de código. El espacio de
búsqueda es enorme y el riesgo de sobreajuste al benchmark es alto.

**Lección.** La selección empírica de variantes es poderosa; en memoria, se puede
aplicar a procedimientos, no al código del agente.

## CUMULUS (propuesta de este proyecto)

**Qué propone.** Habilidades como SIR (Skill Intermediate Representation)
agnósticas al modelo; compilación desde trazas por ablación causal; Canon
versionado; auditoría ciega entre modelos; matriz de portabilidad; Pod con roles
y quórum.

**Qué aporta frente a los anteriores.** Separa semántica de sintaxis; mide
transferencia; gobierna el ciclo de vida; convierte la experiencia en artefactos
verificables.

**Qué le falta.** Validación empírica y una teoría de la causalidad: la ablación
de pasos no es lo mismo que identificar el efecto causal de una decisión.

## Lo que estos sistemas comparten

1. **La experiencia se destila en texto o código**, no en un contrato con
   precondiciones, postcondiciones y evidencia.
2. **La reutilización se decide por similitud**, no por estructura causal.
3. **La verificación es local** (el mismo agente, el mismo modelo) o inexistente.
4. **La transferencia entre modelos no se mide.**
5. **El olvido y la revisión son raros.**

## El hueco

Ninguno de estos sistemas responde:

- ¿La habilidad funcionó por causalidad o por suerte?
- ¿Qué habría pasado si se elegía otra acción?
- ¿La habilidad transfiere a otro modelo o solo a otro prompt?
- ¿Cuándo una habilidad debe retirarse?
- ¿Cómo se enseña a otro agente con fidelidad medida?

Las dos primeras son el territorio de la **memoria contrafactual**; las dos
siguientes, de la **portabilidad**; las dos últimas, de la **gobernanza**.
CUMULUS ataca portabilidad y gobernanza. La memoria contrafactual queda abierta.
