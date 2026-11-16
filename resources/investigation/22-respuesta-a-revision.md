# 22 — Respuesta a la revisión mayor de CUMULUS

**Revisión recibida:** dictamen preliminar *Major Revision* sobre la primera parte
de la investigación y el paper CUMULUS.  
**Respuesta:** aceptada. No se defiende la versión anterior; se corrige el marco,
se retiran afirmaciones y se redefine la contribución.

Este documento responde punto por punto y registra qué cambió en el repositorio.

## 1. Diagnóstico aceptado

La revisión identifica tres fallas que comparto:

1. **Inspiración biológica presentada como justificación computacional.** La
   evidencia de que el cerebro consolida no prueba que una arquitectura de
   consolidación mejore a un LLM.
2. **Literatura amplia pero insuficientemente crítica.** Se reunieron disciplinas
   sin demostrar la transferibilidad de sus resultados.
3. **Diseño experimental sin identificación causal suficiente.** Aun ganando un
   benchmark, no se sabría qué mecanismo produjo la mejora.

Acepto también las consecuencias: la novedad de CUMULUS estaba sobreafirmada, y
la comparación con trabajos de 2026 exige reducir el alcance.

## 2. Cambios introducidos

| Objeción | Cambio | Artefacto |
|---|---|---|
| Neurociencia instrumental | Marco de tres niveles: fenómeno, traducción, ventaja comparativa | `23-marco-de-validez.md` |
| Novedad sobreafirmada | Matriz de competidores 2026 y retiro de la afirmación de novedad amplia | `precedentes/06-competidores-directos-2026.md` |
| Traducciones injustificadas | Correcciones explícitas en retrieval practice, quórum y Weber | docs 03, 05, 07, 09 |
| Información vs. evidencia vs. conocimiento | Ontología de objetos y teoría del error | `23-marco-de-validez.md` |
| Forja sin base causal | La ablación se degrada a "cribado"; la identificación pasa a JANUS | `23`, `papers/cumulus-revision-v0.2.md` |
| Diseño experimental débil | Protocolo único, métrica primaria, potencia, multiplicidad, deriva, evaluadores independientes | `08-hipotesis-y-experimentos.md` (reescrito) |
| "Aprendizaje" ambiguo | Tres niveles y definición operacional | `23` y `08` |
| Generalizaciones humanas | Hipótesis mecanismo-específicas, no extrapolaciones | docs 05 y 07 |
| Capa social confundida con cómputo | Comparación con presupuesto igualado y errores correlacionados | `08` y `22` |
| Seguridad incompleta | Modelo de amenazas y clases de retención | `22`, sección 10 |
| Afiliación y autoría | Declaración explícita y pendiente de verificación | `papers/cumulus-revision-v0.2.md` |

## 3. Respuesta punto por punto

### 3.1 Sobre la neurociencia instrumental

**Aceptado.** CUMULUS confundía tres preguntas:

- ¿el mecanismo existe en neurociencia? (L1)
- ¿hay un equivalente computacional? (L2)
- ¿ese equivalente supera alternativas simples? (L3)

La documentación desarrollaba L1, proponía L2 y no demostraba L3. El nuevo marco
(`23`) exige evidencia separada para cada nivel. Además, se incorpora el matiz de
que la consolidación no es solo lenta: los esquemas previos permiten una vía
rápida (Tse et al., 2007; van Kesteren et al., 2012). La analogía de dos
velocidades se mantiene como hipótesis, no como ley.

### 3.2 Sobre la originalidad

**Aceptado, y es la corrección más importante.** La afirmación "los sistemas
actuales no compilan procedimientos verificables ni comprueban su transferencia"
es falsa en noviembre de 2026. Los competidores:

- **Zep Agent Skills** (Chalef et al., 2026): trazas verificadas → skills
  versionadas con citas por evento, gates de admisión, transferencia
  teacher–executor entre modelos y entrega MCP.
- **MSCE** (Tang et al., 2026): trazas L1 → políticas L2 → skills con evidencia,
  límites, verificación y confiabilidad; transferencia cross-domain.
- **AFTER** (Belikova et al., 2026): benchmark de transferencia de skills entre
  tareas, roles y modelos.
- **Trace2Skill** (Ni et al., 2026): destilación de trayectorias en skills que
  transfieren entre escalas y familias de modelos.
- **Demystifying Agent Skills** (Jiang et al., 2026): cuándo ayudan y cuándo
  fallan; degradación de recuperación al crecer la biblioteca.

**Consecuencia:** se retira la afirmación de novedad amplia. CUMULUS ya no se
presenta como "la arquitectura que compila habilidades portables". Se presenta
como un **protocolo de investigación y una especificación** que replica y compara
esos mecanismos con presupuesto igualado, y como sustrato de JANUS.

La novedad que queda es más estrecha y debe probarse:

1. contrato ejecutable agnóstico al modelo (SIR) con precondiciones,
   postcondiciones y capacidades abstractas;
2. auditoría ciega entre modelos como puerta de promoción;
3. cálculo de portabilidad con enrutamiento, no solo medición;
4. validación causal (JANUS), que los competidores dejan explícitamente abierta.

### 3.3 Sobre las traducciones entre disciplinas

**Aceptado en los tres casos.**

**a) Práctica de recuperación.** Incrementar un contador no es práctica de
recuperación. Un LLM con pesos congelados no fortalece representaciones por
recuperar. El refuerzo artificial puede crear un ciclo rico-se-hace-más-rico.
Corrección: se trata como **hipótesis** con control anti-monopolio (cuotas de
diversidad, exploración forzada), no como mecanismo validado.

**b) Quórum de hormigas.** El quórum mide acuerdo, no verdad. Cinco agentes con
el mismo modelo, prompt y datos no son independientes. Corrección: modelar
correlación entre evaluadores, exigir diversidad de modelo/herramienta y separar
consenso de exactitud. El quórum baja a hipótesis de coordinación, no de
validación epistémica.

**c) Weber.** La legitimidad no es verdad. La tipología tradicional/carismática/
racional-legal describe creencias de dominación, no criterios epistemológicos.
Corrección: se conserva la **trazabilidad del expediente** (autor, fecha, norma,
estado), que sí tiene traducción técnica; se retira la idea de que los regímenes
de legitimidad validan recuerdos.

### 3.4 Sobre información, evidencia y conocimiento

**Aceptado.** Una traza no es una explicación causal. Se introduce una ontología
explícita (`23`):

- observación, afirmación, evidencia, inferencia, hipótesis, conocimiento
  validado.

Reglas:

- una afirmación sin evidencia es hipótesis;
- una inferencia sin supuestos es opinión;
- una observación sin procedencia es rumor;
- solo el conocimiento validado bajo condiciones explícitas se reutiliza.

También se añade una teoría del error: falsos positivos de verificación, trazas
incompletas, verificadores defectuosos, contaminación, evaluadores
correlacionados, sesgo de supervivencia y Goodhart.

### 3.5 Sobre la Forja

**Aceptado.** La ablación de un paso no identifica una causa:

- con acciones redundantes, quitar una no rompe el resultado;
- con interacciones, quitar una rompe pero la causa es la conjunción;
- sin restauración de estado, la repetición mide otro entorno;
- sin intervención, la correlación se confunde con causa.

Corrección:

- la Forja pasa a ser **cribado causal**: propone candidatos y pruebas de
  necesidad local;
- la identificación se delega a JANUS (resultados potenciales, intervenciones,
  experimentos naturales, simulación);
- si no hay identificación, el procedimiento se guarda como **correlacional** y no
  se promueve al Canon;
- se añade abstención explícita: la Forja puede negarse a compilar si la
  cobertura de la traza es insuficiente.

### 3.6 Sobre el diseño experimental

**Aceptado.** Se reescribe `08`:

- **una métrica primaria:** éxito en instancias reservadas de familias
  recurrentes;
- **potencia:** cálculo con varianza piloto, efecto mínimo de interés y 80% de
  potencia; N por celda justificado;
- **multiplicidad:** una primaria; secundarias jerarquizadas con Holm–Bonferroni;
- **transferencia:** se reportan deltas absolutos y relativos, no un cociente con
  denominador inestable; el coeficiente \(T\) solo se usa si el denominador está
  acotado lejos de cero;
- **deriva:** no basta simular 12 semanas; se introducen cambios programados de
  modelo, API, requisitos y distribución;
- **protocolo único:** una sola definición de C0, versionada;
- **evaluadores:** verificadores ejecutables primero; jueces LLM de familias
  distintas, ciegos, con auditoría humana por muestreo y acuerdo reportado;
- **presupuesto igualado:** tokens, llamadas y tiempo capados por condición;
- **modelo rival simple:** repositorio Markdown + tests + recuperador. Si CUMULUS
  no le gana, no hay contribución.

### 3.7 Sobre el concepto de aprendizaje

**Aceptado.** Se distinguen tres niveles:

- **modelo:** no aprende; los pesos están congelados;
- **sistema:** memoria + herramientas + artefactos; puede mejorar de forma
  acumulativa;
- **organización:** varios agentes; puede mejorar por coordinación.

Definición operacional adoptada:

> Hay aprendizaje acumulativo externo cuando la experiencia previa produce una
> mejora reproducible en tareas futuras no observadas, bajo condiciones
> controladas, y persiste tras reinicios de contexto y cambios de modelo.

CUMULUS y JANUS solo reclaman este nivel. No reclaman aprendizaje paramétrico ni
conciencia.

### 3.8 Sobre las generalizaciones del aprendizaje humano

**Aceptado.** Intercalar dominios o replicar sueño no se deduce de la evidencia
humana. Se formulan como hipótesis mecanismo-específicas:

- ¿la mejora viene de la repetición, del muestreo, de la selección de ejemplos,
  de la simulación contrafactual o de la actualización de representaciones?
- ¿el intercalado ayuda o produce abstracciones superficiales?

Cada una se mide por separado; "consolidación semejante al sueño" no agrupa
procedimientos sin explicar cuál es responsable.

### 3.9 Sobre la capa social

**Aceptado.** Un Pod con más agentes gasta más inferencia. La comparación debe
igualar presupuesto. Además, los errores pueden estar correlacionados: el quórum
no es independencia.

Corrección:

- comparación con presupuesto igualado;
- simulación de errores correlacionados;
- métricas de diversidad de evidencia;
- los Pods se tratan como hipótesis, no como mejora asumida;
- la pregunta se reformula: ¿bajo qué condiciones una comunidad produce
  conocimiento más fiable que un sistema centralizado con el mismo presupuesto,
  herramientas y evidencia?

### 3.10 Sobre seguridad y privacidad

**Aceptado.** Falta un modelo de amenazas. Se añaden clases de retención:

| Clase | Qué guarda | Borrado |
|---|---|---|
| Operativa | Trazas de tarea | Retención corta, redacción |
| Histórica | Decisiones y evidencia | Archivo auditable |
| Sensible | Secretos, datos personales | No se guarda o se cifra |
| Efímera | Contexto de sesión | Se descarta al cerrar |

Se distinguen olvido funcional (deja de recuperarse), archivo (se conserva para
auditoría) y eliminación irreversible (derecho al olvido). Se añaden amenazas:
inyección de instrucciones en trazas, envenenamiento de skills, fuga entre
tenants, y se exige aislamiento por namespace.

### 3.11 Sobre las preguntas de investigación

**Aceptado.** Se descompone la pregunta principal en seis:

1. ¿Qué información de una trayectoria predice su utilidad futura?
2. ¿Se pueden inducir procedimientos reutilizables mediante intervenciones
   causales?
3. ¿Qué hace portable una habilidad entre modelos?
4. ¿Cuándo ayuda o perjudica la consolidación selectiva?
5. ¿La validación colectiva supera a la individual con igual presupuesto?
6. ¿Las mejoras persisten cuando cambian entorno, modelo y distribución?

### 3.12 Sobre la afiliación y la autoría

Se declara:

- la afiliación MIT es la declarada por el autor humano y debe verificarse antes
  de cualquier envío;
- DeepSeek figura como coautor/modelo según la decisión del autor;
- antes de un envío académico se debe declarar la participación de IA conforme a
  las normas del venue;
- este repositorio es un documento de trabajo, no una publicación arbitrada.

## 4. Lo que se retira

- "CUMULUS es una arquitectura novedosa." → Es un protocolo de investigación y
  una especificación; su novedad específica está por demostrar.
- "La ablación causal identifica causas." → Es cribado; la identificación requiere
  JANUS.
- "El quórum valida la verdad." → Mide acuerdo; la independencia hay que
  diseñarla.
- "Los regímenes de Weber validan recuerdos." → Solo se conserva la trazabilidad.
- "La práctica de recuperación justifica el refuerzo artificial." → Es una
  hipótesis con riesgo de monopolio.
- "Doce semanas simuladas demuestran durabilidad." → No; falta deriva real.
- "La capa social mejora el aprendizaje." → Es una hipótesis con confusor de
  cómputo.

## 5. Lo que se afirma ahora

1. El problema —reincidencia de errores y pérdida de competencia en agentes
   longevos— es real y está mal medido.
2. La comparación honesta es contra Zep Agent Skills, MSCE, Trace2Skill, AFTER y
   el rival simple (Markdown + tests + recuperador).
3. CUMULUS puede aportar una **especificación formal** y un **protocolo de
   comparación**; no una superioridad demostrada.
4. JANUS es la hipótesis novedosa: sin contrafactuales, los sistemas actuales
   confunden éxito con causalidad. MSCE lo admite en sus limitaciones; Zep no lo
   promete. Ese es el espacio.

## 6. Lo que falta

- Ejecutar el protocolo de `08`.
- Implementar el ledger de decisiones y la jerarquía de evidencia de JANUS.
- Comparar con Zep Agent Skills y MSCE en presupuesto igualado.
- Medir errores correlacionados en Pods.
- Probar deriva real durante meses, no ciclos simulados.

## 7. Cierre

La revisión tenía razón en lo esencial. CUMULUS no estaba demostrado y su novedad
estaba sobreafirmada. La respuesta no es defenderlo: es reducir la arquitectura
hasta que cada componente pague su costo, y mover la apuesta científica al lugar
donde ningún competidor ha llegado: **la memoria de lo que no pasó**.
