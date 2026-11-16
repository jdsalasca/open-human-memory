# CUMULUS: Portable Procedural Memory Under an Attention Budget

**Juan David Salas Camargo** — Massachusetts Institute of Technology (MIT)  
**DeepSeek 4.1 Flash** — Language model

*Working paper · v1.0 · November 2026 · not peer-reviewed*

---

## Abstract

Procedural memory for agents already exists: Zep Agent Skills, MSCE, and
Trace2Skill compile verified traces into versioned skills and transfer them
across models. This work does not claim that idea as new. It proposes a
**model-agnostic executable-contract specification (SIR)** and an
**equal-attention-budget comparison protocol** to answer a narrow question: does
a formal representation with blind audit and portability-aware routing
outperform the 2026 systems and a simple Markdown + tests + retriever baseline?
The thesis rests on three decisions: separate procedure semantics from model
rendering; validate along three dimensions—reliability, causality,
portability—with a risk-sensitive use policy; and measure cost per success
including KV cache, latency, and verification, not tokens alone. The result is
not a demonstrated architecture but a falsifiable program with kill criteria.

**Keywords:** procedural memory, portability, efficient attention, blind audit,
three-dimensional validation.

## 1. Introduction

An agent working for months accumulates experience, but not necessarily
competence. Traditional memory stores facts and episodes; 2026 systems began
compiling traces into skills. Zep Agent Skills does this in production with
event citations, admission gates, and teacher–executor transfer. MSCE adds
governance and applicability boundaries. Trace2Skill distills trajectories that
transfer across model scales and families. AFTER measures transfer across tasks,
roles, and backbones.

The remaining question is not "can a skill be compiled?" It is narrower: **which
representation and which validation regime make a skill portable, reliable, and
safe under a real attention budget?**

## 2. What changed since v0.1

v0.1 claimed that nobody compiled verifiable procedures or measured cross-model
transfer. That is false. Table 1 summarizes the competitors and the gap they
leave.

| System | What it does | What it does not solve |
|---|---|---|
| Zep Agent Skills | Verified traces → versioned skills, citations, admission, MCP | No causal validation; task replay |
| MSCE | L1 traces → L2 policies → skills with evidence and boundaries | Heuristic gain, not causal |
| Trace2Skill | Trajectory distillation; cross-model transfer | No causality or governance |
| AFTER | Transfer benchmark across roles and backbones | Not an architecture |
| COUNTERMEM | Local alternatives verified with world models | Hidden state; longitudinal |
| ConMem | Memory admission via counterfactual probes | Sequential effects |
| MemCon | Adaptive memory control | Consolidation/forgetting unproven |
| More Memory, Worse Agents | Error reproduction; anti-persistence | Persistence policy |

**Consequence:** CUMULUS cannot sell "compiling skills". Its possible
contribution is the **shape of the contract**, the **independence of the audit**,
the **portability routing**, and **attention-cost measurement**. None of it is
demonstrated.

## 3. Evidence and translation levels

Neuroscience and sociology support the need for a lifecycle—encode, consolidate,
forget, transmit—not an algorithm. Following `23-marco-de-validez.md`:

- **L1 phenomenon:** brains consolidate, forget, and transmit; orcas have
  dialects and custodians; ants use quorum.
- **L2 translation:** two stores, an offline compiler, a Canon, a Pod.
- **L3 advantage:** not demonstrated. This program must measure it.

An `[A]` in the evidence table means "the phenomenon exists", not "the component
works".

## 4. Hypotheses

**H1 (portability).** An SIR representation with preconditions, postconditions,
and abstract capabilities transfers across models better than a text or code
package tied to a runtime, measured by success on held-out tasks.

**H2 (blind audit).** An audit that does not see the author or their reasoning
reduces spurious skill promotion compared with self-review.

**H3 (three dimensions).** Validating reliability, causality, and portability
separately, with a risk-sensitive use policy, improves success on reversible
tasks without increasing harm on irreversible ones, compared with a single causal
gate.

**H4 (anti-persistence).** Under distribution drift, reconstructing abstractions
on demand reduces error reproduction compared with a permanent Canon, without
losing stable skills.

**H0 (simple rival).** All of the above must beat a Markdown repository of
procedures + tests + retriever under the same budget.

## 5. Architecture

### 5.1 Trace

Immutable episode log: task, agent, model, context, actions, observations,
outcome, salience, provenance. Corrections are new linked episodes, not edits.

### 5.2 Forge

It does not summarize: it **compiles and screens**.

1. Segment decisions and capabilities.
2. Abstract values into typed parameters.
3. Test local necessity of each step.
4. Detect redundancies and interactions.
5. Infer preconditions, postconditions, and invariants.
6. **Abstain** if trace coverage is insufficient.

Causal identification is not done here; it is delegated to JANUS. Forge produces
candidates, not truths.

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

### 5.3 Minimal operational semantics

A field without a verifier is documentation, not a contract. Every SIR field needs
a check:

| Field | Verifier |
|---|---|
| `preconditions.files` | `stat` / glob |
| `postconditions.tests_pass` | run the test |
| `postconditions.api_unchanged` | OpenAPI diff, compatibility test, or signature analysis |
| `invariants.no_new_dependencies` | lockfile diff |
| `steps[].capability` | runtime adapter |

Composition rules: a step's postconditions must satisfy the next step's
preconditions; side effects are declared; silent failure is forbidden.

**Portability** means SIR preserves verifiable properties when compiled for
another runtime, not merely that the model completes the task.

### 5.4 Canon

Versioned library with status, evidence, owner, validity, contradictions, and
cost. The Canon is small: promotion is expensive and most candidates never make
it.

### 5.5 Pod

Roles with typed artifacts: proposer, executor, counterfactual auditor, causal
auditor, curator, critic. The audit is blind. Quorum is coordination, not truth:
evaluator correlation is modeled.

### 5.6 Bridge

Per-model renderers, capability adapters, conformance suite, portability matrix,
and drift detection. Portability is measured, not assumed.

## 6. The attention budget

The DeepSeek line changes the cost calculus:

- **MLA** (DeepSeek-V2) compresses the KV cache by 93.3% and multiplies
  throughput.
- **DeepSeek-V3** activates 37B of 671B parameters; total capacity is not active
  capacity.
- **NSA** selects blocks natively and speeds decoding up to 11.6× at 64K.
- **FlashAttention** shows the bottleneck is memory/IO, not only FLOPs.

CUMULUS therefore reports an **observable cost vector**, not a scalar with
arbitrary weights:

\[
C = (\text{USD}, \text{latency}, \text{tokens}, \text{KV cache},
\text{compute}, \text{storage})
\]

When a utility is needed, an operating scenario is defined and weights are
calibrated; physical units are never summed without saying so. If the provider
does not expose KV cache, it is reported as unobservable.

If native attention already handles 128K, external memory must prove it
**selects better**, not merely that it fits.

## 7. Evaluation

Protocol `08-hipotesis-y-experimentos.md` v2.0:

- primary metric: success on held-out instances of recurring families;
- equal budget of tokens, KV, calls, and time;
- simple rival: Markdown + tests + retriever;
- competitors: Zep Agent Skills, MSCE, Trace2Skill;
- 8 cycles with model, API, and requirement drift;
- pilot-based power; multiplicity control;
- executable verifiers + judges from different families + human audit;
- calibration, persistent errors, and belief abandonment.

**Kill criterion:** if CUMULUS does not beat the simple rival on the primary
metric with a 95% CI excluding zero, the architecture adds nothing.

### 7.1 Empirical note: prototypes 003 and 004-A (macro learning)

Prototype 002 turned out to be a **solver benchmark**: `MEM-A0`, the same
compositional solver with no history, matched `MEM-E` on D1/D2/D3.

Prototype 003 learned macros from repeated programs and appeared to gain a new
capability (100% at depth 3). Prototype 004-A re-ran the design with a frozen
protocol and the missing controls: the full 64-program lattice, a no-memory
depth-3 baseline, and a sweep over all 560 same-language libraries. Mean of 3
seeds:

| Condition | Solved /64 | Candidates | Candidates per solve |
|---|---|---|---|
| No memory, depth 2 | 33 (51.6%) | 876 | 26.6 |
| **No memory, depth 3** | **64 (100%)** | 1,761 | 27.5 |
| Random, same language, depth 2 | 50.7 (79.3%) | 1,543 | 30.5 |
| Learned macros, depth 2 | 54 (84.4%) | 1,448 | 26.8 |
| Learned macros, depth 3 | 64 (100%) | 2,247 | 35.1 |

Findings:

- **No new capability.** Without history and with depth 3, everything is solved.
  The depth-2 limit was imposed by the experiment.
- **The library is a lossy compilation:** 17.8% fewer candidates and 15.6 pp less
  coverage; per solve the saving is 2.6%.
- **When depth 3 is allowed, the library makes search 27.6% more expensive.**
- **The 003 random control was rigged:** 250/560 arbitrary same-language
  libraries were perfect on its evaluation set, and 124/560 match or beat the
  learned one on the full lattice.
- **The curve saturates at 6 experiences.**
- **The only defensible gain:** with a budget of ≤40 candidates per task the
  library solves more; from 60 upward, deeper search overtakes it.

Conclusion for this paper: macro learning as implemented is a **cheap prior under
a tight compute budget**, not competence expansion. CUMULUS cannot cite it as
evidence of portability or expansion. This is a synthetic result, not an LLM one.

Prototype 005-A adds the missing condition. Measured by behaviour, the grid is
**14 functions**, not 64. At full continuity between past and future the library
matches coverage with **41.8% fewer executed steps**; at zero continuity the same
work yields **22.1 pp less**. In a 96-task stream with drift, **freezing what was
learned saves 26.2% of the work at equal accuracy**, while keeping on accumulating
drops accuracy by 8.7 pp. For CUMULUS that is a hypothesis about bounded
artefacts —useful while the distribution holds—, not a validation of portability.

### 7.2 What the antecedent review changes

The structured review of 31 works (November 2026, `../revision-sistematica/`) forces
three corrections:

1. **Skills already have the shape CUMULUS describes**, with applicability
   conditions, execution policies and termination criteria (SoK, 2026), and are
   generated from trajectories (Trace2Skill, SkillGen). CUMULUS cannot claim the
   format.
2. **Execution-based verification already exists and is essential.** Proof-Gated:
   **52 of 538** asserted verifications confirmed by execution. CUMULUS would have
   to show that its representation survives a model change, not that the gate
   works.
3. **The cost is measured.** STRATUM: **~4 GB of text versus ~298 TB of KV state**
   per 1e9 tokens. Portability must report tokens and maintenance, not only
   artefact size.

Conclusion: CUMULUS stands as a **representation and portability hypothesis without
evidence of its own**. Its question —does a structured representation preserve
utility across models and domains?— remains open and is the only one it can claim.

## 8. Limits and safety

- Transfer may be partial; report it.
- Compilation and verification may cost more than they save.
- Blind audit can be theater if it shares model and biases.
- The Canon can degrade retrieval as it grows (Demystifying Agent Skills).
- Persisting abstractions can reproduce errors (More Memory, Worse Agents).
- Shared memory raises privacy, poisoning, and deletion concerns.

## 9. Conclusion

CUMULUS v1.0 is not a proven architecture. It is a **specification and a
protocol** for comparing procedural representations under a real attention
budget. Its value, if any, lies in the shape of the contract, the independence of
the audit, and the measurement of portability. The larger scientific bet remains
JANUS: memory that knows what it can assert and what it cannot.

---

## References

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

