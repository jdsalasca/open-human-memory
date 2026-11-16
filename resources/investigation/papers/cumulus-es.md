# CUMULUS: conocimiento procedimental acumulativo sin reentrenamiento

### Una arquitectura agnóstica al modelo para el autoaprendizaje y la autocolaboración

**Juan David Salas Camargo** — Massachusetts Institute of Technology (MIT)  
**DeepSeek** — Modelo de lenguaje

*Documento de trabajo · v0.1 · noviembre de 2026 · no arbitrado*

> **Revisión mayor (v0.2).** Las afirmaciones de novedad de esta v0.1 están
> superadas. Zep Agent Skills (Chalef et al., 2026), MSCE (Tang et al., 2026),
> Trace2Skill (Ni et al., 2026) y AFTER (Belikova et al., 2026) ya compilan
> trazas verificadas en habilidades transferibles y gobernadas. Ver
> [`cumulus-revision-v0.2.md`](cumulus-revision-v0.2.md) para el alcance
> corregido y el protocolo de evaluación.

---

## Resumen

¿Puede un agente acumular conocimiento procedimental durante meses, transferirlo
entre modelos de lenguaje distintos y mejorar sin reentrenar el modelo? Los
sistemas de memoria actuales guardan hechos y episodios; rara vez compilan
procedimientos verificados y casi nunca miden si un procedimiento sobrevive a un
cambio de modelo. Sostenemos que la respuesta es sí, pero solo bajo tres
condiciones: representar los procedimientos como **artefactos ejecutables
agnósticos al modelo**, **compilarlos a partir de trazas verificadas mediante
ablación causal** en lugar de resumirlos, y gobernar su promoción con
**verificación ciega entre modelos** dentro de un protocolo social. Proponemos
CUMULUS, una arquitectura de cinco capas —Traza, Forja, Canon, Pod y Puente— que
separa la semántica del procedimiento de la sintaxis del modelo, trata la
portabilidad como una propiedad medida y no supuesta, y gestiona las habilidades
con un ciclo de vida de validación, decaimiento, revisión y retiro. Formulamos
una hipótesis falsable de portabilidad acumulativa, derivamos subhipótesis
comprobables y especificamos un benchmark longitudinal con verificadores
ejecutables, tres familias de modelos y criterios de muerte explícitos. La
contribución no es una afirmación de conciencia ni de inteligencia general: es
un diseño institucional para hacer acumulativa la experiencia cuando el modelo
está congelado.

**Palabras clave:** memoria procedimental, aprendizaje continuo, transferencia
entre modelos, sociedades de agentes, compilación de habilidades, gobernanza de
la memoria.

---

## 1. Introducción

Un modelo de lenguaje está congelado al desplegarse. Puede razonar sobre lo que
vio en entrenamiento, pero no puede aprender de un proyecto nuevo salvo que algo
fuera de sus pesos cambie. Hoy ese "algo" es la ventana de contexto, un índice de
recuperación o un montón de notas. Estos mecanismos ayudan a recordar hechos. No
hacen de forma fiable que el agente sea **más competente** en el trabajo
recurrente.

Imaginemos un equipo que usa agentes durante meses. Aparece la misma clase de
bug, se requiere la misma migración, se olvida la misma verificación de
despliegue. Un equipo humano acumularía un runbook: un procedimiento con
precondiciones, pasos, ramas de fallo y un historial de lo que funcionó. Un
equipo de agentes, en cambio, acumula transcripciones. Cuando el contexto se
compacta, el runbook se disuelve en un resumen. Cuando se cambia el modelo, el
resumen puede no encajar ni con la sintaxis de herramientas del nuevo modelo.

La pregunta de este trabajo es estrecha y empírica:

> **¿Puede un agente desarrollar conocimiento procedimental acumulativo durante
> meses, transferible entre modelos distintos, de modo que su rendimiento mejore
> sin reentrenar el LLM?**

Respondemos: **sí, en principio, bajo condiciones que los sistemas actuales no
cumplen.** Las condiciones son arquitectónicas, no mágicas. Se derivan de lo que
los sistemas de memoria ya hacen bien en la biología y en las organizaciones:
codificar rápido, consolidar despacio, verificar socialmente, olvidar de forma
selectiva y transmitir con alta fidelidad.

El trabajo hace cuatro contribuciones:

1. Una formulación precisa del **conocimiento procedimental acumulativo** con
   pesos congelados, incluido qué contaría como evidencia y qué sería un
   factor de confusión.
2. **CUMULUS**, una arquitectura de cinco capas que compila experiencia en
   habilidades portables y gobierna su ciclo de vida.
3. Un protocolo de **aprendizaje ciego** para la autocolaboración: agentes con
   roles intercambian artefactos tipados y se verifican sin ver el razonamiento
   del autor.
4. Un **benchmark longitudinal** que mide acumulación, transferencia entre
   modelos, interferencia y retención en conjunto, con criterios de muerte
   pre-registrados.

La afirmación es deliberadamente modesta. No sostenemos que un agente pueda
mejorar sin límite en todo. Sostenemos que un subconjunto acotado y verificable
del conocimiento procedimental puede acumularse, y que el cuello de botella es
la representación y la gobernanza, no el tamaño del modelo.

## 2. Por qué la pregunta es difícil

### 2.1 Tres confusiones

La literatura suele confundir tres cosas:

- **Memoria de hechos** (qué pasó, quién dijo qué).
- **Memoria de casos** (una situación pasada parecida y su resultado).
- **Memoria procedimental** (una rutina condicional que se puede ejecutar).

La generación aumentada por recuperación aborda sobre todo la primera. El
razonamiento basado en casos aborda la segunda (Memento; Zhou et al., 2025). Las
bibliotecas de habilidades abordan la tercera, pero normalmente en un solo
entorno y con un solo modelo (Voyager; Wang et al., 2023; SkillWeaver; Zheng et
al., 2025).

El conocimiento procedimental acumulativo requiere las tres, más un mecanismo de
promoción que decida cuándo una rutina es lo bastante confiable para reutilizarse.

### 2.2 El problema de la transferencia

Un procedimiento aprendido por el modelo A está enredado con los hábitos del
modelo A: cómo llama herramientas, cómo formatea pasos intermedios, qué hace
cuando una llamada falla. Mover el procedimiento al modelo B puede romper tres
cosas:

1. **Sintaxis**: nombres de herramientas, esquemas de argumentos, formatos.
2. **Política**: el nuevo modelo puede necesitar otra descomposición o
   instrucciones más explícitas.
3. **Competencia**: el nuevo modelo puede simplemente ser peor en un subpaso.

La mayoría de las bibliotecas de habilidades guardan procedimientos como código
o prompts, lo que los hace portables solo dentro del mismo runtime y la misma
familia de modelos. Un procedimiento que no sobrevive a un cambio de modelo no
es conocimiento acumulativo; es un prompt en caché.

### 2.3 El problema de la evaluación

Los benchmarks existentes miden recall en conversaciones largas (LoCoMo;
Maharana et al., 2024; LongMemEval; Wu et al., 2025) o éxito en una única suite
de tareas. No miden:

- si el rendimiento **mejora durante meses** con pesos fijos,
- si una habilidad aprendida por un modelo **se transfiere** a otro,
- si las ganancias **sobreviven a un reinicio de contexto**,
- si el sistema **olvida** lo que debería retener,
- si la mejora se debe al procedimiento o a recuperar casos parecidos.

Sin esas mediciones, "agente que se auto-mejora" es una narrativa, no un
resultado.

### 2.4 El problema de la interferencia

Holton et al. (2026) muestran que humanos y redes neuronales comparten un
trade-off: las tareas parecidas producen más transferencia y más interferencia;
las disímiles producen menos de ambas. Una biblioteca que ignore esto se
fragmentará en rutinas inútilmente específicas o colapsará en un procedimiento
sobre-generalizado que corrompe todo lo que toca. Las políticas por dominio y el
seguimiento de transferencia negativa no son opcionales.

## 3. Lo que dice la evidencia

Resumimos la base de investigación que motiva CUMULUS; una síntesis acompañante
contiene la revisión completa.

### 3.1 Neurología: dos velocidades y olvido selectivo

El marco de sistemas complementarios (McClelland, McNaughton y O'Reilly, 1995;
Kumaran, Hassabis y McClelland, 2016) distingue un sistema episódico rápido y
disperso (hipocampo) de uno semántico lento y distribuido (neocórtex). La
consolidación durante el sueño hace replay y **selecciona**; no copia (Stickgold
y Walker, 2013). La recuperación reconsolida y puede modificar la huella (Nader,
Schafe y LeDoux, 2000). El olvido es adaptativo y a menudo es un cambio de
accesibilidad, no un borrado (Richards y Frankland, 2017; Ryan y Frankland,
2022).

**Implicación de diseño:** dos almacenes, un compilador offline y una política de
olvido que archiva en lugar de eliminar.

### 3.2 Aprendizaje procedimental: chunking con feedback de resultado

Los ganglios basales compilan secuencias de acción repetidas en hábitos
(Graybiel, 2008), mientras el control prefrontal mantiene metas y anula el hábito
cuando la situación cambia (Miller y Cohen, 2001). El control basado en modelo y
el habitual coexisten (Daw et al., 2011). Un procedimiento no es un texto: es una
política condicional con un historial de éxito.

**Implicación de diseño:** las habilidades necesitan precondiciones,
postcondiciones, ramas de fallo y estadísticas por contexto.

### 3.3 Aprendizaje social: la fidelidad es el recurso escaso

Las orcas transmiten ecotipos, dialectos y técnicas de caza por matrilinas; las
hembras post-reproductivas actúan como custodias del conocimiento ecológico
(Brent et al., 2015), y la enseñanza puede ser intencional y costosa (Guinet y
Bouvier, 1995). Primates y córvidos muestran tradiciones y conductas de
enseñanza. En todos los taxones, la **transmisión de alta fidelidad** es lo que
hace acumulativa la cultura (Tomasello, 1999; Henrich, 2015).

**Implicación de diseño:** compartir una transcripción es emulación de baja
fidelidad. Enseñar debe ser una operación explícita con verificación de que el
aprendiz puede ejecutar.

### 3.4 Insectos sociales: estigmergia y quórum

Las hormigas coordinan mediante trazas que decaen (Grassé, 1959; Goss et al.,
1989) y se comprometen con una opción cuando los encuentros superan un quórum
(Pratt et al., 2002). La división del trabajo emerge de umbrales individuales
(Bonabeau, Theraulaz y Deneubourg, 1996).

**Implicación de diseño:** trazas compartidas con evaporación, promoción por
quórum y enrutamiento por umbrales.

### 3.5 Organizaciones: legitimidad y jaula de hierro

La burocracia de Weber es una tecnología de memoria: jurisdicción, jerarquía, el
expediente (*Akten*), reglas e impersonalidad (Weber, 1922). Hace la memoria
duradera y auditable, pero la racionalización puede convertirse en una "jaula de
hierro" que conserva la estructura a costa del sentido.

**Implicación de diseño:** cada habilidad necesita procedencia, dueño, régimen de
validez y cláusula de caducidad.

### 3.6 Psicología: reconstrucción y contaminación

La memoria es reconstructiva (Bartlett, 1932), vulnerable a información
posterior (Loftus y Palmer, 1974) y sujeta a falsos recuerdos (Roediger y
McDermott, 1995). La recuperación puede inhibir a los competidores (Anderson,
Bjork y Bjork, 1994). Los grupos recuerdan menos ítems únicos que la suma de los
individuos (Weldon y Bellinger, 1997) y pueden adoptar contagiosamente recuerdos
falsos (Roediger, Meade y Bergman, 2001). El sesgo de confirmación y la disonancia
empujan a defender las decisiones existentes (Festinger, 1957; Nickerson, 1998).

**Implicación de diseño:** separar fuente de interpretación, usar verificación
ciega, mantener buffers individuales y forzar la contraevidencia.

### 3.7 Aprendizaje humano vs. máquina

Los humanos aprenden patrones con menos ejemplos (Kühl, 2022) y explotan
estructura causal y composicional (Lake et al., 2017). Las máquinas compensan con
escala. El aprendizaje continuo en redes sufre interferencia catastrófica
(McCloskey y Cohen, 1989; French, 1999), mitigada con replay y regularización
(Kirkpatrick et al., 2017; Rolnick et al., 2019). Holton et al. (2026) muestran
que el trade-off transferencia/interferencia es compartido, no un caso especial
humano.

**Implicación de diseño:** no prometer eliminar la interferencia; gestionarla por
dominio y medirla.

## 4. Hipótesis

### 4.1 La hipótesis de portabilidad acumulativa

> **H1.** Con pesos de modelo congelados, una capa de artefactos procedimentales
> agnósticos al modelo que compila trazas verificadas en habilidades ejecutables,
> las valida mediante ejecución ciega entre modelos y las gobierna con un ciclo
> de vida, produce mejora acumulativa positiva en familias de tareas recurrentes
> y verificables, y transferencia positiva a modelos no vistos.

"Positiva" no es una impresión. Se define a continuación.

### 4.2 Esquema formal

Sea \(F\) una familia de tareas, \(m\) un modelo y \(C_t\) el canon en el ciclo
\(t\). Sea \(S(F, m, C_t) \in [0,1]\) el éxito en instancias reservadas.

- **Acumulación:** \(S(F, m, C_t)\) tiene pendiente positiva en \(t\) después de
  controlar por dificultad, y la ganancia sobrevive a un reinicio de contexto.
- **Retención:** la ganancia persiste tras \(k\) ciclos sin repaso para las
  habilidades canónicas, y decae para las no canónicas sin uso.
- **Transferencia:** para una habilidad \(s\) aprendida con el modelo \(m\),
  \[
  T(s, m \to m') = \frac{S(F, m', C \cup \{s\}) - S(F, m', C)}
  {S(F, m, C \cup \{s\}) - S(F, m, C)}
  \]
  con \(T > 0\) si la habilidad ayuda al nuevo modelo.
- **Portabilidad:** \(P(s, m')\) es el éxito esperado de \(s\) con \(m'\). Un
  buen estimador de portabilidad predice la transferencia (AUC ≥ 0,7 en el
  benchmark propuesto).
- **Atribución:** eliminar el Canon devuelve el rendimiento a la línea base sin
  habilidades, lo que confirma que las ganancias viven en los artefactos y no en
  actualizaciones ocultas de pesos.

### 4.3 Subhipótesis

| # | Hipótesis | Métrica primaria | Umbral propuesto |
|---|---|---|---|
| H1a | Las habilidades se acumulan entre ciclos | Pendiente de éxito en familias recurrentes | ≥ 10% de ganancia relativa sobre la mejor línea base |
| H1b | Las habilidades se transfieren entre modelos | Coeficiente de transferencia \(T\) | ≥ 0,5 para ≥ 50% de las canónicas |
| H1c | Las ganancias sobreviven a reinicio y cambio de modelo | Retención tras reinicio/cambio | ≥ 80% de la ganancia pico |
| H1d | Las ganancias son artefactuales | Ablación del Canon | Retorno a la línea base dentro del ruido |
| H1e | Compilar supera a resumir | Éxito con igual presupuesto de tokens | ≥ 10% relativo sobre playbooks tipo ACE |
| H1f | La verificación ciega reduce la contaminación | Tasa de falsas promociones | ≥ 50% de reducción vs. auto-revisión |
| H1g | Los artefactos tipados superan al chat libre | Calidad por 1k tokens | ≥ 20% de mejora |

Estos umbrales son objetivos de diseño para el primer experimento, no
afirmaciones empíricas.

### 4.4 Hipótesis nula y confusores

La nula es que cualquier ganancia se explique por:

- recuperación de casos pasados parecidos (memoria de casos),
- prompts más largos o mejor curados (ingeniería de contexto),
- deriva del evaluador o filtración de tareas,
- mayor presupuesto de inferencia.

El benchmark debe incluir líneas base y ablaciones que aíslen cada factor.

## 5. La arquitectura CUMULUS

### 5.1 Vista general

CUMULUS tiene cinco capas:

```
┌─────────────────────────────────────────────────────────────┐
│  POD        roles, auditoría ciega, quórum, disenso, directorio │
├─────────────────────────────────────────────────────────────┤
│  CANON      habilidades validadas, versiones, matriz de portabilidad │
├─────────────────────────────────────────────────────────────┤
│  FORJA      traza → núcleo causal → SIR → tests → candidata  │
├─────────────────────────────────────────────────────────────┤
│  TRAZA      log inmutable: tarea, acciones, resultados        │
├─────────────────────────────────────────────────────────────┤
│  PUENTE     renderizadores, adaptadores, detección de deriva  │
└─────────────────────────────────────────────────────────────┘
```

El nombre evoca acumulación. Las capas no son un pipeline; son un metabolismo.
La Traza alimenta la Forja; la Forja propone al Canon; el Pod gobierna; el Puente
ejecuta y mide.

### 5.2 Traza: la capa episódica

Cada episodio es un registro inmutable:

```yaml
episode:
  id: ep_...
  task: {family, instance, goal, domain}
  actor: {agent_id, model_id, model_version, role}
  context: {tools, repo, constraints, budget}
  steps:
    - {action, tool, args, observation, latency, cost}
  outcome: {status, verifier, score, artifacts}
  salience: {novelty, reward, surprise, threat, social}
  provenance: {parent_episodes, skill_versions_used}
```

Reglas de diseño:

- **Inmutable.** Las correcciones son episodios nuevos enlazados al viejo, no
  ediciones. Es el "expediente" de Weber y la restricción de reconsolidación de
  la memoria.
- **Procedencia completa.** Cada habilidad se puede rastrear hasta los episodios
  que la produjeron.
- **Redacción en la frontera.** Los secretos se eliminan antes de almacenar; la
  privacidad es una propiedad de la traza, no un filtro posterior.

### 5.3 Forja: compilar experiencia en habilidades

La Forja es la novedad central. No resume una traza: la **compila**.

**Paso 1 — Segmentar.** Identificar puntos de decisión y fronteras de
herramientas. Un punto de decisión es un paso cuya eliminación cambia el
resultado; una frontera es una llamada con entradas y salidas tipadas.

**Paso 2 — Abstraer.** Reemplazar valores concretos por parámetros tipados. Una
ruta `src/auth/session.ts` se convierte en `target_file: Path`; un comando de
test se convierte en `verify: Command`. El objetivo es preservar el *rol* de cada
valor, no su instancia.

**Paso 3 — Ablacionar.** En un sandbox, eliminar cada paso y volver a ejecutar la
postcondición. El **núcleo causal** es el conjunto mínimo de pasos cuya
eliminación rompe el éxito. Esto es diagnóstico diferencial, no imitación.
Responde: *¿qué partes de lo que pasó importaron de verdad?*

**Paso 4 — Inferir contratos.** Del estado previo, derivar precondiciones
(archivos, herramientas, permisos). Del estado posterior, derivar postcondiciones
ejecutables (tests, esquema, salida). De trazas casi exitosas, derivar ramas de
fallo y reparaciones.

**Paso 5 — Emitir SIR.** La Representación Intermedia de Habilidad es un DAG
tipado:

```yaml
skill:
  id: sk_...
  goal: "arreglar el test de auth sin cambiar la API pública"
  domain: code_repair
  preconditions:
    - tests: {command: "...", expected: failing}
    - files: ["src/auth/*"]
  inputs: {target_file: Path, failing_test: TestId}
  steps:
    - id: s1
      action: inspect
      capability: read_file
      args: {path: "${target_file}"}
    - id: s2
      action: patch
      capability: edit_file
      args: {path: "${target_file}", strategy: "minimal"}
      on_failure: [s2a]
    - id: s3
      action: verify
      capability: run_tests
      args: {test: "${failing_test}"}
  postconditions:
    - tests_pass: "${failing_test}"
    - api_unchanged: true
  invariants:
    - "sin dependencias nuevas"
  provenance: [ep_..., ep_...]
  stats:
    per_model: {m1: {n: 12, success: 0.83}, m2: {...}}
  status: candidate
  version: 0.1.0
```

**Paso 6 — Probar.** Generar o recuperar instancias reservadas; ejecutar la
habilidad con el modelo autor y al menos otro modelo; puntuar con verificadores
ejecutables. Una candidata sin postcondición se rechaza: si no se puede
comprobar, no se puede compilar.

**Paso 7 — Nominar.** Si la candidata pasa el quórum y la auditoría ciega, va al
Canon como `validated`; si no, se archiva con el motivo. El archivo es datos de
entrenamiento para la Forja: los fallos enseñan qué abstracciones están mal.

### 5.4 Canon: la capa institucional

El Canon es una biblioteca versionada de habilidades SIR, no un prompt. Cada
entrada tiene:

- **Estado:** candidata → validada → canónica → deprecada → archivada.
- **Evidencia:** episodios, suites de tests, ejecuciones entre modelos.
- **Matriz de portabilidad:** éxito por (habilidad, modelo, dominio).
- **Dueño:** un agente curador responsable de las revisiones.
- **Intervalo de validez:** las habilidades pueden caducar; una fecha de
  caducidad fuerza la revisión.
- **Contradicciones:** las habilidades incompatibles coexisten con un enlace y
  evidencia; no se promedian.
- **Perfil de costo:** tokens, latencia y llamadas por éxito.

El Canon es deliberadamente pequeño. La promoción es cara; la mayoría de las
candidatas nunca llegan a canónicas. Es el "quórum" de las hormigas y el
"expediente" de Weber: la memoria no es lo que pasó, es lo que ha sido
**instituido**.

### 5.5 Pod: la autocolaboración como protocolo

El Pod no es una sala de chat. Es un conjunto de roles que intercambian
artefactos tipados.

| Rol | Función | Análogo biológico |
|---|---|---|
| Explorador | Detecta una necesidad recurrente; propone una familia de tareas | Hormiga exploradora |
| Herrero | Ejecuta la tarea; produce una traza | Obrera |
| Auditor | Verifica ciegamente una candidata | Sistema inmune |
| Curador | Mantiene el Canon, programa revisiones, enseña | Matriarca orca |
| Historiador | Audita procedencia, contradicciones y deriva | Funcionario weberiano |
| Crítico | Argumenta contra la promoción; preserva el disenso | Control prefrontal |

**Mensajes tipados** (sin compartir contexto libre):

- `CLAIM`: "la familia F es recurrente; aquí está la evidencia."
- `EVIDENCE`: traza, resultado del verificador, costo.
- `PROCEDURE`: una candidata SIR.
- `CHALLENGE`: un contraejemplo o una replicación fallida.
- `VERDICT`: promover / rechazar / falta evidencia.
- `TEACH`: una habilidad renderizada más un andamiaje para el aprendiz.

**Auditoría ciega.** El Auditor ve el SIR, los tests y la evidencia, no la
identidad del autor, su razonamiento ni su modelo. Esto evita la autopreferencia,
la adulación y el contagio social documentado por la psicología. El Auditor puede
ejecutar la habilidad con otro modelo; el desacuerdo se registra, no se resuelve
por votación.

**Quórum.** La promoción requiere \(k\) ejecuciones exitosas independientes en al
menos dos modelos y un conjunto reservado del dominio. El tamaño del quórum es un
dial: más alto significa precisión, más bajo significa velocidad.

**Registro de disenso.** Una habilidad rechazada no se borra. Sus contraejemplos
quedan enlazados para que evidencia futura pueda revivirla o retirarla
definitivamente. Es el antídoto contra el pensamiento de grupo y contra la "jaula
de hierro" de la sobre-consolidación.

### 5.6 Puente: ejecución agnóstica al modelo

El Puente es lo que hace portable la arquitectura.

- **Abstracción de capacidades.** Las habilidades se refieren a capacidades
  (`read_file`, `run_tests`, `search_web`), no a herramientas de un proveedor.
  Cada runtime aporta un adaptador.
- **Renderizador.** Para cada familia de modelos, un renderizador compila el SIR
  al formato de prompt, esquema de herramientas y presupuesto de contexto del
  modelo. El renderizador está versionado; cambiarlo dispara una corrida de
  conformidad.
- **Suite de conformidad.** Una batería fija de tareas por habilidad, ejecutada
  por cada modelo soportado. El resultado actualiza la matriz de portabilidad.
- **Score de portabilidad.** Una estimación Beta-Binomial por (habilidad,
  modelo), actualizada tras cada ejecución. El enrutamiento usa muestreo de
  Thompson sobre la utilidad esperada: probabilidad de éxito × valor − costo, con
  un bono de exploración para pares no probados.
- **Detección de deriva.** Cuando cambia una versión de modelo o una API de
  herramientas, el Puente rerun la suite. Una habilidad cuya portabilidad cae por
  debajo del umbral se marca, se re-forja o se retira.

Esta es la respuesta arquitectónica al problema de transferencia: **separar lo
que la habilidad significa de cómo un modelo lo dice.**

## 6. El bucle de autoaprendizaje

```
1. Llega una tarea.
2. El enrutador elige (habilidad, modelo) por utilidad esperada + exploración.
3. Ejecutar; registrar Traza.
4. Si el éxito es novedoso o incierto:
     La Forja redacta o actualiza una candidata SIR por ablación causal.
5. El Auditor corre tests ciegos en instancias reservadas y ≥2 modelos.
6. Si pasa el quórum: el Canon promueve. Si no: archiva con motivo.
7. El Curador programa repasos espaciados; las habilidades sin uso decaen; las
   canónicas reciben fecha de caducidad.
8. El Historiador registra procedencia y contradicciones; el Puente actualiza
   portabilidad.
```

Dos propiedades importan:

- **Sin actualizaciones de pesos.** El bucle solo escribe artefactos,
  estadísticas y políticas de enrutamiento.
- **Crecimiento acotado.** La promoción es cara y el decaimiento es activo, así
  que el Canon no crece sin límite. El sistema olvida por diseño.

### 6.1 Qué cuenta como "aprender"

Distinguimos:

- **Adaptación dentro de una tarea**: cambios de prompt/contexto. No es
  acumulativo.
- **Memoria de casos**: recuperar un episodio pasado parecido. Útil, pero no
  procedimental.
- **Adquisición de habilidad**: una rutina condicional reutilizable entra al
  Canon. Es la unidad de aprendizaje acumulativo.
- **Refinamiento de habilidad**: una habilidad canónica mejora con evidencia
  nueva. Es la unidad de progreso.

La hipótesis trata de las dos últimas.

## 7. El protocolo de autocolaboración

La autocolaboración suele implementarse como varios agentes charlando. Eso escala
tokens, no competencia. CUMULUS usa **colaboración mediada por artefactos**:

1. **Descomponer** la tarea en subtareas con contratos tipados (entradas, salidas,
   postcondiciones).
2. **Asignar** roles por el directorio transactivo (quién ha tenido éxito en ese
   dominio), no por turnos.
3. **Intercambiar artefactos**, no transcripciones. Cada artefacto lleva
   procedencia y evidencia.
4. **Verificar a ciegas**: el Auditor no sabe quién produjo el artefacto.
5. **Registrar el disenso**: un `CHALLENGE` bloquea la promoción hasta que la
   evidencia lo resuelva, no la mayoría.
6. **Enseñar**: el Curador renderiza la habilidad para un agente novato con
   andamiaje; el novato ejecuta; la fidelidad se mide y se retroalimenta.

Por qué debería funcionar:

- Reduce la inflación de contexto: los artefactos son comprimidos, tipados y
  reutilizables.
- Reduce la contaminación: auditoría ciega y evidencia independiente.
- Explota la especialización: el directorio enruta a la competencia, no a la
  verbosidad.
- Preserva el conocimiento minoritario: el disenso es un activo, no ruido.

## 8. Transferencia entre modelos

### 8.1 Qué se transfiere

Una habilidad SIR se transfiere si:

- sus capacidades existen en el runtime destino (posiblemente vía adaptadores),
- sus precondiciones y postcondiciones son expresables,
- sus pasos no dependen de peculiaridades del modelo,
- el modelo destino puede ejecutar cada paso por encima de un piso de
  competencia.

El Puente mide cada condición. La transferencia no se supone: se estima.

### 8.2 Qué no se transfiere

- Habilidades que dependen de la gramática de llamadas de un modelo específico.
- Habilidades que dependen de un layout de contexto o un prompt oculto.
- Habilidades cuya postcondición es un juicio subjetivo sin rúbrica.
- Habilidades que codifican una reparación específica de un modelo ("cuando el
  modelo X entra en bucle, dile Y").

El último caso es importante: algunas "habilidades" son en realidad parches de
modelo. CUMULUS debe clasificarlas como **adaptadores**, no como canon. Los
adaptadores viven en el Puente; se versionan con el modelo, no con el
procedimiento.

### 8.3 La portabilidad como métrica de primera clase

La mayoría de las bibliotecas reporta éxito con el modelo que aprendió la
habilidad. CUMULUS reporta la **matriz de portabilidad**:

```
              m1     m2     m3
habilidad A   0.82   0.74   0.61
habilidad B   0.91   0.88   0.84
habilidad C   0.55   0.31   0.22
```

La habilidad B es candidata a canon; la C es específica de dominio o frágil. El
enrutamiento usa esta matriz. La investigación la usa para probar H1b.

## 9. Evaluación

### 9.1 CUMULUS-Bench

Un benchmark longitudinal con:

- **5 dominios:** reparación de código, pipelines de datos, síntesis de
  documentos, respuesta a incidentes y orquestación de herramientas.
- **10 familias de tareas por dominio**, cada una con 20 instancias y un
  verificador ejecutable (tests, esquemas, rúbrica con doble puntuación).
- **3 familias de modelos** con sintaxis de herramientas y límites de contexto
  distintos.
- **6 ciclos** (simulando 12 semanas), 150 tareas por ciclo.
- **Cambio de modelo** en los ciclos 3 y 5 para probar transferencia.
- **Reinicio de contexto** en cada ciclo para probar retención.
- **Holdouts ocultos** por familia para detectar sobreajuste al verificador.

### 9.2 Condiciones

| Condición | Descripción |
|---|---|
| C0 | Zero-shot, sin memoria |
| C1 | RAG sobre episodios pasados |
| C2 | Feedback verbal tipo Reflexion |
| C3 | Biblioteca de habilidades en código tipo Voyager (un modelo) |
| C4 | Playbook evolutivo tipo ACE |
| C5 | Memoria de casos tipo Memento |
| C6 | CUMULUS sin Puente (un solo modelo) |
| C7 | CUMULUS completo |

### 9.3 Métricas

- **Tasa de éxito** en instancias reservadas por ciclo.
- **Pendiente de acumulación** (modelo de efectos mixtos con dificultad como
  covariable).
- **Retención** tras reinicio y tras cambio de modelo.
- **Coeficiente de transferencia** \(T\) y tasa de **transferencia negativa**.
- **AUC de portabilidad**: ¿la matriz predicha ordena bien las habilidades?
- **Costo por éxito** (tokens, latencia, llamadas).
- **Fidelidad**: conformidad del procedimiento (pasos ejecutados como se
  especifican).
- **Contaminación**: falsas habilidades promovidas; habilidades que pasan tests
  pero fallan en holdouts.
- **Tiempo hasta competencia** para un modelo o agente nuevo.

### 9.4 Ablaciones

Quitar la Forja (usar resúmenes), la auditoría ciega (usar auto-revisión), el
Puente (un solo modelo), el decaimiento (guardar todo), los artefactos tipados
(chat libre) y la procedencia del Canon (sin enlaces a trazas). Cada ablación
prueba una afirmación específica.

### 9.5 Criterios de muerte

Tras 6 ciclos, CUMULUS debe:

- superar a la mejor línea base en ≥10% relativo en al menos 2 de 4 métricas
  primarias (éxito, retención, transferencia, costo), y
- alcanzar un coeficiente de transferencia ≥0,5 para al menos la mitad de las
  habilidades canónicas, y
- mostrar AUC de portabilidad ≥0,7.

Si no, la hipótesis falla para este diseño. La respuesta correcta es simplificar,
no añadir módulos.

## 10. Trabajo relacionado

**Memoria de agentes.** MemGPT/Letta pagina contexto entre memoria principal y
externa (Packer et al., 2023). Generative Agents recupera por recencia,
importancia y relevancia (Park et al., 2023). Mem0 extrae y consolida hechos
(Chhikara et al., 2025). Zep/Graphiti añade validez temporal a un grafo
(Rasmussen et al., 2025). HippoRAG usa indexado hipocámpico y propagación en
grafo (Gutiérrez et al., 2024, 2025). MemoryBank aplica decaimiento de Ebbinghaus
(Zhong et al., 2024). Estos sistemas guardan conocimiento; CUMULUS guarda
procedimientos.

**Bibliotecas de habilidades y experiencia.** Voyager acumula habilidades
ejecutables en Minecraft (Wang et al., 2023). SkillWeaver sintetiza habilidades
web reutilizables como APIs (Zheng et al., 2025). Agent Workflow Memory induce
flujos reutilizables (Wang, Fried y Neubig, 2024). ExpeL extrae ideas en lenguaje
natural de la experiencia (Zhao et al., 2024). Reflexion usa feedback verbal
(Shinn et al., 2023). ACE evoluciona un playbook textual (Zhang, Q., et al., 2025).
Memento usa memoria de casos sin actualizar pesos (Zhou et al., 2025). CUMULUS se
diferencia por su compromiso con una representación ejecutable agnóstica al
modelo, la compilación causal, la verificación ciega entre modelos y la
portabilidad como propiedad medida.

**Auto-mejora.** La Darwin Gödel Machine modifica su propio código y selecciona
variantes por rendimiento en benchmarks (Zhang, J., et al., 2025). Es
auto-modificación a nivel de código; CUMULUS es auto-modificación a nivel de
artefactos procedimentales, con un espacio de búsqueda mucho más pequeño y
auditable.

**Aprendizaje continuo.** EWC (Kirkpatrick et al., 2017) y el replay (Rolnick et
al., 2019) protegen los pesos. CUMULUS no toca los pesos; su estabilidad viene de
la gobernanza del Canon y su plasticidad de la Forja.

## 11. Limitaciones, seguridad y gobernanza

### 11.1 Límites de la afirmación

- **No crea competencia latente.** Si un modelo no puede ejecutar un paso, una
  habilidad no puede inventar la capacidad. CUMULUS amplifica y organiza
  competencia; no la crea.
- **Cuello de botella del verificador.** Las habilidades necesitan
  postcondiciones comprobables. Los dominios sin verificadores requieren rúbricas
  o humanos, lo que frena la acumulación.
- **Meses simulados.** Una simulación de 12 semanas no es un año de deriva de
  APIs, deprecaciones de modelos y cambio organizacional. La prueba real es el
  despliegue longitudinal.
- **La transferencia es parcial.** Algunas habilidades serán específicas del
  modelo. La arquitectura debe reportarlo con honestidad, no esconderlo.

### 11.2 Riesgos de seguridad

- **Envenenamiento de habilidades.** Un adversario puede inyectar una traza que
  compile en una habilidad dañina o interesada. Mitigaciones: procedencia, Canon
  con permisos, auditoría ciega, holdouts y rollback.
- **Juego del verificador.** Las habilidades pueden sobreajustarse a los tests.
  Mitigaciones: holdouts ocultos, tests adversariales, múltiples verificadores.
- **Reward hacking en el enrutamiento.** El sistema puede preferir habilidades
  que parecen baratas pero fallan fuera de distribución. Mitigaciones:
  portabilidad calibrada, éxito ajustado por costo, auditorías periódicas.
- **Opacidad.** Un Canon creciente puede volverse una burocracia ilegible.
  Mitigación: resúmenes legibles, revisiones de caducidad y un campo explícito de
  "porqué".

### 11.3 Gobernanza

La memoria es un común (Ostrom, 1990). CUMULUS necesita:

- **Permisos de escritura**: quién puede promover al Canon.
- **Procedencia**: cada habilidad rastreable a episodios.
- **Política de contradicción**: las habilidades incompatibles coexisten con
  evidencia.
- **Política de caducidad**: las canónicas expiran si no se revalidan.
- **Privacidad**: redacción en la frontera de la traza; local-first por defecto.
- **Auditoría**: un lector externo puede reconstruir por qué existe una
  habilidad.

## 12. Conclusión

La pregunta era si un agente puede acumular conocimiento procedimental durante
meses, transferirlo entre modelos y mejorar sin reentrenar. La respuesta que
defendemos es condicional: **sí, si la unidad de aprendizaje es un artefacto
portable y verificado, no un prompt ni una transcripción.**

CUMULUS hace tres apuestas:

1. **Apuesta de representación:** los procedimientos se pueden separar de la
   sintaxis del modelo.
2. **Apuesta de verificación:** la ejecución ciega entre modelos es mejor puerta
   de promoción que la auto-revisión.
3. **Apuesta institucional:** una biblioteca de habilidades necesita gobernanza,
   custodios, decaimiento y disenso para seguir siendo útil durante meses.

Si las apuestas se sostienen, el resultado no es un modelo más inteligente. Es
una **institución de memoria**: un sistema que convierte experiencia en
competencia, conserva lo que funciona, retira lo que no, y puede entregar su
conocimiento a un modelo que nunca ha visto.

---

## Referencias

Anderson, M. C., Bjork, R. A., & Bjork, E. L. (1994). Remembering can cause
forgetting. *Journal of Experimental Psychology: Learning, Memory, and
Cognition, 20*(5), 1063–1087.

Bartlett, F. C. (1932). *Remembering*. Cambridge University Press.

Bonabeau, E., Theraulaz, G., & Deneubourg, J.-L. (1996). Quantitative study of
the fixed threshold model for the regulation of division of labour in insect
societies. *Proceedings of the Royal Society B, 263*(1376), 1565–1569.

Brent, L. J. N., et al. (2015). Ecological knowledge, leadership, and the
evolution of menopause in killer whales. *Current Biology, 25*(6), 746–750.

Chhikara, P., et al. (2025). *Mem0: Building production-ready AI agents with
scalable long-term memory*. arXiv:2504.19413.

Daw, N. D., Gershman, S. J., Seymour, B., Dayan, P., & Dolan, R. J. (2011).
Model-based influences on humans' choices and striatal prediction errors.
*Neuron, 69*(6), 1204–1215.

Festinger, L. (1957). *A theory of cognitive dissonance*. Stanford University
Press.

French, R. M. (1999). Catastrophic forgetting in connectionist networks.
*Trends in Cognitive Sciences, 3*(4), 128–135.

Goss, S., Aron, S., Deneubourg, J.-L., & Pasteels, J. M. (1989). Self-organized
shortcuts in the Argentine ant. *Naturwissenschaften, 76*, 579–581.

Grassé, P.-P. (1959). La reconstruction du nid et les coordinations
interindividuelles chez les termites. *Insectes Sociaux, 6*, 41–80.

Graybiel, A. M. (2008). Habits, rituals, and the evaluative brain. *Annual
Review of Neuroscience, 31*, 359–387.

Guinet, C., & Bouvier, J. (1995). Development of intentional stranding hunting
techniques in killer whale calves at Crozet Archipelago. *Canadian Journal of
Zoology, 73*(1), 27–33.

Gutiérrez, B. J., et al. (2024). HippoRAG: Neurobiologically inspired long-term
memory for large language models. *NeurIPS, 37*.

Henrich, J. (2015). *The secret of our success*. Princeton University Press.

Holton, E., Braun, L., Thompson, J. A. F., Grohn, J., & Summerfield, C. (2026).
Humans and neural networks show similar patterns of transfer and interference
during continual learning. *Nature Human Behaviour, 10*, 111–125.

Kirkpatrick, J., et al. (2017). Overcoming catastrophic forgetting in neural
networks. *PNAS, 114*(13), 3521–3526.

Kühl, N. (2022). Human vs. supervised machine learning: Who learns patterns
faster? *Cognitive Systems Research*.

Kumaran, D., Hassabis, D., & McClelland, J. L. (2016). What learning systems do
intelligent agents need? *Trends in Cognitive Sciences, 20*(7), 512–534.

Lake, B. M., Ullman, T. D., Tenenbaum, J. B., & Gershman, S. J. (2017).
Building machines that learn and think like people. *Behavioral and Brain
Sciences, 40*, e253.

Loftus, E. F., & Palmer, J. C. (1974). Reconstruction of automobile destruction.
*Journal of Verbal Learning and Verbal Behavior, 13*(5), 585–589.

Maharana, A., et al. (2024). Evaluating very long-term conversational memory of
LLM agents. *ACL 2024*.

McClelland, J. L., McNaughton, B. L., & O'Reilly, R. C. (1995). Why there are
complementary learning systems in the hippocampus and neocortex.
*Psychological Review, 102*(3), 419–457.

McCloskey, M., & Cohen, N. J. (1989). Catastrophic interference in connectionist
networks. *Psychology of Learning and Motivation, 24*, 109–165.

Miller, E. K., & Cohen, J. D. (2001). An integrative theory of prefrontal cortex
function. *Annual Review of Neuroscience, 24*, 167–202.

Nader, K., Schafe, G. E., & LeDoux, J. E. (2000). Fear memories require protein
synthesis in the amygdala for reconsolidation after retrieval. *Nature, 406*,
722–726.

Nickerson, R. S. (1998). Confirmation bias: A ubiquitous phenomenon in many
guises. *Review of General Psychology, 2*(2), 175–220.

Ostrom, E. (1990). *Governing the commons*. Cambridge University Press.

Packer, C., et al. (2023). *MemGPT: Towards LLMs as operating systems*.
arXiv:2310.08560.

Park, J. S., et al. (2023). Generative agents: Interactive simulacra of human
behavior. *UIST 2023*.

Pratt, S. C., Mallon, E. B., Sumpter, D. J. T., & Franks, N. R. (2002). Quorum
sensing, recruitment, and collective decision-making during colony emigration by
the ant *Leptothorax albipennis*. *Behavioral Ecology and Sociobiology, 52*,
117–127.

Rasmussen, P., et al. (2025). *Zep: A temporal knowledge graph architecture for
agent memory*. arXiv:2501.13956.

Richards, B. A., & Frankland, P. W. (2017). The persistence and transience of
memory. *Neuron, 94*(6), 1071–1084.

Roediger, H. L., & McDermott, K. B. (1995). Creating false memories. *Journal of
Experimental Psychology: Learning, Memory, and Cognition, 21*(4), 803–814.

Roediger, H. L., Meade, M. L., & Bergman, E. T. (2001). Social contagion of
memory. *Psychonomic Bulletin & Review, 8*(2), 365–371.

Rolnick, D., Ahuja, A., Schwarz, J., Lillicrap, T., & Wayne, A. (2019).
Experience replay for continual learning. *NeurIPS, 32*.

Ryan, T. J., & Frankland, P. W. (2022). Forgetting as a form of adaptive engram
cell plasticity. *Nature Reviews Neuroscience, 23*(3), 173–186.

Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K., & Yao, S. (2023).
Reflexion: Language agents with verbal reinforcement learning. *NeurIPS, 36*.

Stickgold, R., & Walker, M. P. (2013). Sleep-dependent memory triage. *Nature
Neuroscience, 16*(2), 139–145.

Tomasello, M. (1999). *The cultural origins of human cognition*. Harvard
University Press.

Wang, G., et al. (2023). *Voyager: An open-ended embodied agent with large
language models*. arXiv:2305.16291.

Wang, Z. Z., Mao, J., Fried, D., & Neubig, G. (2024). *Agent Workflow Memory*.
arXiv:2409.07429.

Weber, M. (1922). *Wirtschaft und Gesellschaft*.

Weldon, M. S., & Bellinger, K. D. (1997). Collective memory: Collaborative and
individual processes in remembering. *Journal of Experimental Psychology:
Learning, Memory, and Cognition, 23*(5), 1160–1175.

Wu, D., et al. (2025). LongMemEval: Benchmarking chat assistants on long-term
interactive memory. *ICLR 2025*.

Zhang, J., Hu, S., Lu, C., Lange, R., & Clune, J. (2025). *Darwin Gödel Machine:
Open-ended evolution of self-improving agents*. arXiv:2505.22954.

Zhang, Q., et al. (2025). *Agentic Context Engineering: Evolving contexts for
self-improving language models*. arXiv:2510.04618.

Zhao, A., Huang, D., Xu, Q., Lin, M., Liu, Y.-J., & Huang, G. (2024). ExpeL: LLM
agents are experiential learners. *AAAI 2024*.

Zheng, B., et al. (2025). *SkillWeaver: Web agents can self-improve by
discovering and honing skills*. arXiv:2504.07079.

Zhong, W., Guo, L., Gao, Q., Ye, H., & Wang, Y. (2024). MemoryBank: Enhancing
large language models with long-term memory. *AAAI 2024*.

Zhou, H., et al. (2025). *Memento: Fine-tuning LLM agents without fine-tuning
LLMs*. arXiv:2508.16153.
