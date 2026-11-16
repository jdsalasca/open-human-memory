# CUMULUS v0.2 — Nota de revisión y alcance corregido

**Estado:** revisión mayor recibida. Este documento sustituye las afirmaciones de
novedad de `cumulus-en.md` y `cumulus-es.md` (v0.1), que se conservan como
registro histórico.

**Autores:** Juan David Salas Camargo (MIT) y DeepSeek / DeepSeek 4.1 Flash.  
**Declaración:** documento de trabajo no arbitrado. La afiliación MIT es la
declarada por el autor humano y debe verificarse antes de un envío. La
participación de IA debe declararse conforme a las normas del venue.

---

## 1. Qué cambió y por qué

La revisión mayor señaló tres fallas:

1. inspiración biológica presentada como justificación computacional;
2. literatura amplia pero poco crítica;
3. diseño experimental sin identificación causal.

La revisión también identificó competidores directos de 2026 que cubren buena
parte de lo que v0.1 presentaba como nuevo. Este documento acepta esas
objeciones y reduce el alcance.

**Lo que se retira:**

- "CUMULUS es una arquitectura novedosa."
- "Nadie compila procedimientos verificables ni mide transferencia entre modelos."
- "La ablación causal identifica causas."
- "El quórum valida la verdad."
- "La capa social mejora el aprendizaje."

**Lo que se conserva como programa de investigación:**

- una especificación formal de contrato procedural agnóstico al modelo (SIR);
- una auditoría ciega entre modelos como hipótesis de promoción;
- un cálculo de portabilidad con enrutamiento;
- un protocolo de comparación con presupuesto igualado;
- el puente a JANUS para la validación causal.

## 2. Abstract revisado (ES)

La memoria procedural para agentes ya existe: Zep Agent Skills, MSCE y
Trace2Skill compilan trazas verificadas en habilidades versionadas y las
transferen entre modelos. Este trabajo no reclama esa idea como nueva. Propone
una especificación formal de contrato ejecutable (SIR) y un protocolo de
evaluación que compara mecanismos con presupuesto igualado, contra un rival
simple (Markdown + tests + recuperador) y contra los sistemas de 2026. La
contribución que se somete a prueba es estrecha: ¿una representación agnóstica al
modelo con auditoría ciega y enrutamiento por portabilidad supera a esos
sistemas? La validación causal se delega a JANUS, porque ninguno de los sistemas
actuales identifica el efecto causal de una habilidad.

## 3. Abstract revisado (EN)

Procedural memory for agents already exists: Zep Agent Skills, MSCE, and
Trace2Skill compile verified traces into versioned skills and transfer them
across models. This work does not claim that idea as new. It proposes a formal
executable-contract specification (SIR) and an evaluation protocol that compares
mechanisms under equal compute, against a simple rival (Markdown + tests +
retriever) and against the 2026 systems. The claim under test is narrow: does a
model-agnostic representation with blind cross-model audit and
portability-aware routing outperform those systems? Causal validation is
delegated to JANUS, because none of the current systems identifies the causal
effect of a skill.

## 4. Trabajo relacionado (2026)

| Sistema | Qué hace | Qué no hace | Relación con CUMULUS |
|---|---|---|---|
| Zep Agent Skills (Chalef et al., 2026) | Trazas verificadas → skills versionadas con citas, admisión y MCP | No valida causalmente; transferencia a tareas nuevas no es el foco | Anticipa Traza, Forja, Canon y Puente |
| MSCE (Tang et al., 2026) | L1 trazas → L2 políticas → skills con evidencia, límites y verificación | Ganancia heurística, no causal (declarado) | Anticipa gobernanza y promoción |
| AFTER (Belikova et al., 2026) | Benchmark de transferencia entre tareas, roles y modelos | No propone arquitectura | Anticipa la pregunta de portabilidad |
| Trace2Skill (Ni et al., 2026) | Destila trayectorias en skills que transfieren entre modelos | No resuelve causalidad ni gobernanza | Anticipa transferencia entre modelos |
| Demystifying Agent Skills (Jiang et al., 2026) | Cuándo ayudan y cuándo fallan; degradación de retrieval | No propone memoria causal | Anticipa el problema de selección |
| CUMULUS v0.1 | Traza → Forja → Canon → Puente + Pod | Novedad sobreafirmada; Forja no identifica causas | Este documento la reduce |
| JANUS | Contrafactuales + puerta causal | Sin validación empírica todavía | Continúa el programa |

**Consecuencia:** la contribución de CUMULUS no puede ser "compilar skills desde
trazas". Esa puerta está cerrada. Lo que queda es la **forma del contrato**, la
**independencia de la auditoría** y el **enrutamiento por portabilidad**, y todo
ello como hipótesis a comparar, no como superioridad asumida.

## 5. Especificación SIR: qué se conserva

SIR sigue siendo una representación tipada con:

- precondiciones ejecutables;
- pasos con capacidades abstractas (`read_file`, `run_tests`, `search_web`);
- postcondiciones verificables;
- invariantes;
- procedencia por episodio;
- estadísticas por modelo y dominio;
- estado y versión.

**Diferencia con Agent Skills / MSCE:** SIR separa la semántica del procedimiento
de su renderizado por modelo y exige contratos ejecutables. Agent Skills usa un
formato abierto de paquete (SKILL.md); MSCE usa políticas en lenguaje natural.
Si SIR no demuestra ventaja sobre esos formatos, no se justifica.

## 6. Forja: de "ablación causal" a "cribado causal"

La v0.1 decía que eliminar pasos y repetir la postcondición identificaba el
núcleo causal. No es cierto en general:

- con acciones redundantes, quitar una no rompe el resultado;
- con interacciones, la causa es la conjunción;
- sin restauración de estado, la repetición mide otro entorno;
- sin intervención, la correlación se confunde con causa.

**v0.2:** la Forja hace **cribado**:

1. segmenta decisiones y capacidades;
2. abstrae valores;
3. prueba necesidad local de cada paso;
4. detecta redundancias e interacciones;
5. propone candidatos;
6. **se abstiene** si la cobertura de la traza es insuficiente.

La identificación causal se delega a JANUS: resultados potenciales,
intervenciones, experimentos naturales, simulación con supuestos explícitos y
prueba de transporte.

## 7. Evaluación: protocolo único

La evaluación vigente es `08-hipotesis-y-experimentos.md` v2.0:

- una métrica primaria: éxito en instancias reservadas de familias recurrentes;
- presupuesto igualado (tokens, llamadas, tiempo);
- rival simple: Markdown + tests + recuperador;
- competidores: Zep Agent Skills, MSCE, Trace2Skill;
- 8 ciclos con deriva programada de modelo, API y requisitos;
- potencia calculada con piloto; multiplicidad controlada;
- evaluadores ejecutables + jueces de familias distintas + auditoría humana;
- criterios de muerte explícitos.

**Criterio de muerte:** si CUMULUS no supera al rival simple en la métrica
primaria con intervalo de confianza que excluya cero, la arquitectura no aporta y
se reduce a ese rival.

## 8. Lo que sigue siendo novedoso (con humildad)

1. **Contrato ejecutable agnóstico al modelo** con precondiciones,
   postcondiciones e invariantes, frente a formatos de paquete o políticas en
   lenguaje natural.
2. **Auditoría ciega entre modelos** como puerta de promoción, frente a curación
   por el mismo sistema.
3. **Enrutamiento por portabilidad** con estimación calibrada y detección de
   deriva.
4. **Validación causal (JANUS)**: el hueco que MSCE admite y Zep no promete.

Ninguna de las cuatro está demostrada. Son hipótesis.

## 9. Límites y amenazas

- La transferencia entre modelos puede ser más parcial de lo que la hipótesis
  tolera.
- El costo de compilar y verificar puede no pagarse.
- La auditoría ciega puede ser teatro si los auditores comparten modelo y sesgos.
- El Canon puede crecer hasta degradar la recuperación (Demystifying Agent
  Skills).
- La deriva real de APIs y modelos es más dura que una simulación de 8 ciclos.
- La gobernanza puede convertirse en burocracia sin mejorar la verdad.

## 10. Qué nos haría cambiar de opinión

- Que el rival simple iguale o supere a CUMULUS en la métrica primaria.
- Que la auditoría ciega no reduzca skills espurias frente a la curación normal.
- Que la portabilidad no prediga transferencia (AUC ≤ 0.5).
- Que JANUS no reduzca skills espurias frente a CUMULUS.

Si ocurre, se reduce el alcance y se abandona el componente.

## 11. Conclusión

CUMULUS v0.1 era una arquitectura con una tesis ambiciosa y una novedad
sobreafirmada. CUMULUS v0.2 es un **protocolo de investigación** con una tesis
estrecha: la forma del contrato, la independencia de la auditoría y el
enrutamiento por portabilidad pueden aportar algo, pero deben probarlo contra los
sistemas que ya existen. La apuesta científica grande se traslada a JANUS: la
memoria de lo que no pasó.
