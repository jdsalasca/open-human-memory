# CUMULUS: memoria procedural portable bajo un presupuesto de atención

**Juan David Salas Camargo** — Massachusetts Institute of Technology (MIT)  
**DeepSeek 4.1 Flash** — Modelo de lenguaje

*Documento de trabajo · v1.0 · noviembre de 2026 · no arbitrado*

---

## Resumen

La memoria procedural para agentes ya existe: Zep Agent Skills, MSCE y
Trace2Skill compilan trazas verificadas en habilidades versionadas y las
transferen entre modelos. Este trabajo no reclama esa idea como nueva. Propone
una **especificación de contrato ejecutable agnóstico al modelo (SIR)** y un
**protocolo de comparación con presupuesto de atención igualado** para responder
una pregunta estrecha: ¿una representación formal con auditoría ciega y
enrutamiento por portabilidad supera a los sistemas de 2026 y a un repositorio
simple de Markdown con tests y recuperador?

La tesis se apoya en tres decisiones: separar la semántica del procedimiento del
renderizado del modelo; validar en tres dimensiones —fiabilidad, causalidad y
portabilidad— con una política de uso según riesgo; y medir el costo por éxito
incluyendo KV cache, latencia y verificación, no solo tokens. El resultado no es
una arquitectura demostrada, sino un programa falsable con criterios de muerte.

**Palabras clave:** memoria procedural, portabilidad, atención eficiente,
auditoría ciega, validación tridimensional.

## Abstract

Procedural memory for agents already exists: Zep Agent Skills, MSCE, and
Trace2Skill compile verified traces into versioned skills and transfer them
across models. This work does not claim that idea as new. It proposes a
**model-agnostic executable-contract specification (SIR)** and an **equal-attention
budget comparison protocol** to answer a narrow question: does a formal
representation with blind audit and portability-aware routing outperform the 2026
systems and a simple Markdown + tests + retriever baseline? The thesis rests on
three decisions: separate procedure semantics from model rendering; validate
along three dimensions—reliability, causality, portability—with a risk-sensitive
use policy; and measure cost per success including KV cache, latency, and
verification, not tokens alone.

---

## 1. Introducción

Un agente que trabaja durante meses acumula experiencia, pero no necesariamente
competencia. La memoria tradicional guarda hechos y episodios; los sistemas de
2026 empezaron a compilar trazas en habilidades. Zep Agent Skills lo hace en
producción con citas por evento, admisión y transferencia teacher–executor. MSCE
añade gobernanza y límites de aplicabilidad. Trace2Skill destila trayectorias que
transferen entre escalas y familias de modelos. AFTER mide transferencia entre
tareas, roles y backbones.

La pregunta que queda no es "¿se puede compilar una skill?". Es más estrecha:
**¿qué forma de representación y qué régimen de validación hacen que una
habilidad sea portable, fiable y segura bajo un presupuesto de atención real?**

## 2. Lo que cambió desde la v0.1

La v0.1 afirmaba que nadie compilaba procedimientos verificables ni medía
transferencia entre modelos. Es falso. La Tabla 1 resume los competidores y el
hueco que dejan.

| Sistema | Qué hace | Qué no resuelve |
|---|---|---|
| Zep Agent Skills | Trazas verificadas → skills versionadas, citas, admisión, MCP | No valida causalmente; replay de tareas |
| MSCE | L1 trazas → L2 políticas → skills con evidencia y límites | Ganancia heurística, no causal |
| Trace2Skill | Destilación de trayectorias; transferencia entre modelos | Sin causalidad ni gobernanza |
| AFTER | Benchmark de transferencia entre roles y backbones | No arquitectura |
| COUNTERMEM | Alternativas locales verificadas con world models | Estado parcialmente oculto; longitudinal |
| ConMem | Admisión de memoria por sondas contrafactuales | Efectos secuenciales |
| MemCon | Control adaptativo de memoria | Consolidación/olvido no probados |
| More Memory, Worse Agents | Error reproduction; anti-persistencia | Política de persistencia |

**Consecuencia:** CUMULUS no puede vender "compilar skills". Su contribución
posible es la **forma del contrato**, la **independencia de la auditoría**, el
**enrutamiento por portabilidad** y la **medición del costo de atención**. Nada
de eso está demostrado.

## 3. Evidencia y niveles de traducción

La neurociencia y la sociología sostienen la necesidad de un ciclo de vida
—codificar, consolidar, olvidar, transmitir—, no un algoritmo. Siguiendo
`23-marco-de-validez.md`, distinguimos:

- **L1 fenómeno:** el cerebro consolida, olvida y transmite; las orcas tienen
  dialectos y custodios; las hormigas usan quórum.
- **L2 traducción:** dos almacenes, un compilador offline, un Canon, un Pod.
- **L3 ventaja:** no demostrada. Es lo que este programa debe medir.

Un `[A]` en la tabla de evidencia significa "el fenómeno existe", no "el
componente funciona".

## 4. Hipótesis

**H1 (portabilidad).** Una representación SIR con precondiciones,
postcondiciones y capacidades abstractas transfiere entre modelos mejor que un
paquete de texto o código atado al runtime, medido por éxito en tareas
reservadas.

**H2 (auditoría ciega).** Una auditoría que no ve al autor ni su razonamiento
reduce la promoción de habilidades espurias frente a la auto-revisión.

**H3 (tres dimensiones).** Validar fiabilidad, causalidad y portabilidad por
separado, con política de uso según riesgo, mejora el éxito en tareas reversibles
sin aumentar el daño en tareas irreversibles, frente a una puerta causal única.

**H4 (anti-persistencia).** En entornos con deriva, reconstruir abstracciones bajo
demanda reduce la reproducción de errores frente a un Canon permanente, sin
perder habilidades estables.

**H0 (rival simple).** Todo lo anterior debe superar a un repositorio Markdown de
procedimientos + tests + recuperador, con el mismo presupuesto.

## 5. Arquitectura

### 5.1 Traza

Log inmutable de episodios: tarea, agente, modelo, contexto, acciones,
observaciones, resultado, saliencia, procedencia. Las correcciones son episodios
nuevos enlazados, no ediciones.

### 5.2 Forja

No resume: **compila y criba**.

1. Segmenta decisiones y capacidades.
2. Abstrae valores a parámetros tipados.
3. Prueba necesidad local de cada paso.
4. Detecta redundancias e interacciones.
5. Infiere precondiciones, postcondiciones e invariantes.
6. **Se abstiene** si la cobertura es insuficiente.

La identificación causal no se hace aquí: se delega a JANUS. La Forja produce
candidatos, no verdades.

### 5.3 SIR

```yaml
skill:
  id: sk_...
  goal: ...
  domain: ...
  preconditions: [...]
  inputs: {...}
  steps:
    - {id, action, capability, args, on_failure}
  postconditions: [...]
  invariants: [...]
  provenance: [ep_...]
  evidence: {reliability: ..., causality: ..., portability: ...}
  status: candidate | validated | canonical | deprecated
```

### 5.3 Semántica operacional mínima

Un campo sin verificador es documentación, no contrato. Cada campo de SIR debe
tener un método de comprobación:

| Campo | Verificador |
|---|---|
| `preconditions.files` | `stat` / glob |
| `postconditions.tests_pass` | ejecutar el test |
| `postconditions.api_unchanged` | diff de OpenAPI, test de compatibilidad o análisis de firmas |
| `invariants.no_new_dependencies` | diff del lockfile |
| `steps[].capability` | adaptador del runtime |

Reglas de composición: las postcondiciones de un paso deben satisfacer las
precondiciones del siguiente; los efectos secundarios se declaran; un fallo no
silencioso es obligatorio.

**Portabilidad** significa que SIR conserva las propiedades verificables al
compilarse para otro runtime, no solo que el modelo complete la tarea.

### 5.4 Canon

Biblioteca versionada con estado, evidencia, dueño, validez, contradicciones y
costo. El Canon es pequeño: la promoción es cara y la mayoría de las candidatas
no llegan.

### 5.5 Pod

Roles con artefactos tipados: proponente, ejecutor, auditor contrafactual,
auditor causal, curador, crítico. La auditoría es ciega. El quórum es
coordinación, no verdad: se modela la correlación entre evaluadores.

### 5.6 Puente

Renderizadores por modelo, adaptadores de capacidades, suite de conformidad,
matriz de portabilidad y detección de deriva. La portabilidad se mide; no se
supone.

## 6. El presupuesto de atención

La línea DeepSeek cambia el cálculo de costo:

- **MLA** (DeepSeek-V2) comprime el KV cache un 93,3% y multiplica el throughput.
- **DeepSeek-V3** activa 37B de 671B parámetros; la capacidad total no es la
  capacidad activa.
- **NSA** selecciona bloques de forma nativa y acelera decodificación hasta 11,6×
  a 64K.
- **FlashAttention** muestra que el cuello es memoria/IO, no solo FLOPs.

Por eso CUMULUS reporta un **vector de coste observable**, no un escalar con
pesos arbitrarios:

\[
C = (\text{USD}, \text{latencia}, \text{tokens}, \text{KV cache},
\text{cómputo}, \text{almacenamiento})
\]

Cuando haga falta una utilidad, se define un escenario operativo y se calibran
los pesos; nunca se suman unidades físicas sin declararlo. Si el proveedor no
expone el KV cache, se reporta como no observable.

Si la atención nativa ya procesa 128K, la memoria externa debe demostrar que
**elige mejor**, no solo que "cabe".

## 7. Evaluación

Protocolo `08-hipotesis-y-experimentos.md` v2.0:

- métrica primaria: éxito en instancias reservadas de familias recurrentes;
- presupuesto igualado de tokens, KV, llamadas y tiempo;
- rival simple: Markdown + tests + recuperador;
- competidores: Zep Agent Skills, MSCE, Trace2Skill;
- 8 ciclos con deriva de modelo, API y requisitos;
- potencia con piloto; multiplicidad controlada;
- evaluadores ejecutables + jueces de familias distintas + auditoría humana;
- métricas de calibración, errores persistentes y abandono de creencias.

**Criterio de muerte:** si CUMULUS no supera al rival simple en la métrica
primaria con IC 95% que excluya cero, la arquitectura no aporta.

### 7.1 Nota empírica: prototipo 003 (aprendizaje de macros)

El Prototipo 002 resultó ser un **benchmark de solucionador**: `MEM-A0`, el mismo
solucionador composicional sin historial, empató con `MEM-E` en D1/D2/D3. El 003
introduce aprendizaje real: encapsula programas de dos pasos que se repiten como
macros y las usa en evaluación.

Media de 3 semillas, 60 de entrenamiento, 30 de evaluación:

| Condición | D1 | D2 | D3 (profundidad 3) |
|---|---|---|---|
| NOLEARN | 1.000 | 1.000 | 0.000 |
| RANDOM (mismo tamaño, macros distractoras) | 1.000 | 1.000 | 0.000 |
| LEARNED | 1.000 | 1.000 | 1.000 |
| ABLATED (macros borradas) | 1.000 | 1.000 | 0.000 |

**Si se elimina el historial, se pierde D3.** La ganancia no es gratis: LEARNED
gasta 740 candidatos en D3 frente a 1.680 de RANDOM. Es un resultado sintético,
no de CUMULUS ni de un LLM; las macros son composiciones de primitivas conocidas,
no conceptos nuevos. Detalles en `prototipo-003-aprendizaje/`.

## 8. Límites y seguridad

- La transferencia puede ser parcial; hay que reportarla.
- La compilación y la verificación pueden costar más de lo que ahorran.
- La auditoría ciega puede ser teatro si comparte modelo y sesgos.
- El Canon puede degradar la recuperación al crecer (Demystifying Agent Skills).
- Persistir abstracciones puede reproducir errores (More Memory, Worse Agents).
- La memoria compartida plantea privacidad, envenenamiento y borrado.

## 9. Conclusión

CUMULUS v1.0 no es una arquitectura probada. Es una **especificación y un
protocolo** para comparar representaciones procedurales bajo un presupuesto de
atención real. Su valor, si existe, está en la forma del contrato, la
independencia de la auditoría y la medición de portabilidad. La apuesta
científica grande sigue en JANUS: la memoria que sabe qué puede afirmar y qué no.

---

## Referencias

Bahdanau, D., Cho, K., & Bengio, Y. (2015). Neural machine translation by jointly
learning to align and translate. *ICLR 2015*.

Belikova, J., et al. (2026). *Managing procedural memory in LLM agents*.
arXiv:2606.23127.

Chalef, D., et al. (2026). *Learning by doing: Autonomously compiling and
curating agent skills from verified traces*. arXiv:2611.01386.

Dao, T., Fu, D. Y., Ermon, S., Rudra, A., & Ré, C. (2022). FlashAttention: Fast
and memory-efficient exact attention with IO-awareness. *NeurIPS 35*.

DeepSeek-AI. (2024). *DeepSeek-V2: A strong, economical, and efficient
mixture-of-experts language model*. arXiv:2405.04434.

DeepSeek-AI. (2024). *DeepSeek-V3 technical report*. arXiv:2412.19437.

DeepSeek-AI. (2025). DeepSeek-R1 incentivizes reasoning in LLMs through
reinforcement learning. *Nature, 645*, 633–638.

Dai, D., et al. (2024). DeepSeekMoE: Towards ultimate expert specialization in
mixture-of-experts language models. *ACL 2024*, 1280–1297.

Guo, D., et al. (2024). *DeepSeek-Coder: When the large language model meets
programming*. arXiv:2401.14196.

Jiang, Z., et al. (2026). *Demystifying agent skills: Why they work—until they
don't*. arXiv:2608.14036.

Ni, J., et al. (2026). Trace2Skill: Distill trajectory-local lessons into
transferable agent skills. *Findings of EMNLP 2026*, 17556–17577.

Shao, Z., et al. (2024). *DeepSeekMath: Pushing the limits of mathematical
reasoning in open language models*. arXiv:2402.03300.

Su, J., Lu, Y., Pan, S., Murtadha, A., Wen, B., & Liu, Y. (2021). *RoFormer:
Enhanced transformer with rotary position embedding*. arXiv:2104.09864.

Tang, B., et al. (2026). From memory to skills: Evidence-grounded governance for
long-horizon LLM agents. *Findings of EMNLP 2026*, 34826–34847.

Vaswani, A., et al. (2017). Attention is all you need. *NeurIPS 30*.

Wang, R., Panaganti, K., & Zhou, D. (2026). *More memory, worse agents: Error
reproduction and anti-persistence in LLM agents*. arXiv:2610.27406.

Yuan, J., et al. (2025). Native Sparse Attention: Hardware-aligned and natively
trainable sparse attention. *ACL 2025*, 23078–23097.

Zheng, B., et al. (2025). *SkillWeaver: Web agents can self-improve by
discovering and honing skills*. arXiv:2504.07079.
