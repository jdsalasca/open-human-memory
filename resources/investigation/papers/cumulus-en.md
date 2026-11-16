# CUMULUS: Cumulative Procedural Knowledge Without Retraining

### A model-agnostic architecture for self-learning and self-collaboration

**Juan David Salas Camargo** — Massachusetts Institute of Technology (MIT)  
**DeepSeek** — Language model

*Working paper · v0.1 · November 2026 · not peer-reviewed*

> **Major revision (v0.2).** The claims of novelty in this v0.1 are superseded.
> Zep Agent Skills (Chalef et al., 2026), MSCE (Tang et al., 2026), Trace2Skill
> (Ni et al., 2026), and AFTER (Belikova et al., 2026) already compile verified
> traces into transferable, governed skills. See
> [`cumulus-revision-v0.2.md`](cumulus-revision-v0.2.md) for the corrected scope
> and the evaluation protocol.

---

## Abstract

Can an agent accumulate procedural knowledge over months, transfer it across
different language models, and improve without retraining the underlying model?
Current agent memory systems store facts and episodes; they rarely compile
verified procedures, and almost never measure whether a procedure survives a
change of model. We argue that the answer is yes, but only under three
conditions: procedures must be represented as **model-agnostic executable
artifacts**, they must be **compiled from verified traces by causal ablation**
rather than summarized, and their promotion must be governed by **blind
cross-model verification** inside a social protocol. We propose CUMULUS, an
architecture with five layers — Trace, Forge, Canon, Pod, and Bridge — that
separates procedural semantics from model-specific rendering, treats
portability as a measured property rather than an assumption, and manages
skills through a lifecycle of validation, decay, revision, and retirement. We
state a falsifiable cumulative-portability hypothesis, derive testable
sub-hypotheses, and specify a longitudinal benchmark with executable verifiers,
three model families, and explicit kill criteria. The contribution is not a
claim of consciousness or general intelligence: it is an institutional design
for making experience cumulative when the model is frozen.

**Keywords:** procedural memory, continual learning, cross-model transfer, agent
societies, skill compilation, memory governance.

---

## 1. Introduction

A language model is frozen at deployment. It can reason about what it has seen
in training, but it cannot learn from a new project unless something outside its
weights changes. Today, that "something" is the context window, a retrieval
index, or a growing pile of notes. These mechanisms help an agent remember
facts. They do not reliably make it **more competent** at recurring work.

Consider a team that uses agents for months. The same class of bug appears, the
same migration is required, the same deployment check is forgotten. A human team
would accumulate a runbook: a procedure with preconditions, steps, failure
branches, and a history of what worked. An agent team, in contrast, accumulates
transcripts. When the context is compacted, the runbook dissolves into a
summary. When the model is swapped, the summary may not even fit the new
model's tool syntax.

The question of this paper is narrow and empirical:

> **Can an agent develop cumulative procedural knowledge over months,
> transferable across different models, such that performance improves without
> retraining the LLM?**

We answer: **yes, in principle, under conditions that current systems do not
meet.** The conditions are architectural, not magical. They follow from what
memory systems already do well in biology and organizations: encode fast,
consolidate slowly, verify socially, forget selectively, and transmit with high
fidelity.

The paper makes four contributions:

1. A precise formulation of **cumulative procedural knowledge** under frozen
   weights, including what would count as evidence and what would be a
   confound.
2. **CUMULUS**, a five-layer architecture that compiles experience into portable
   skills and governs their lifecycle.
3. A **blind apprenticeship** protocol for self-collaboration: role-bound agents
   exchange typed artifacts and verify each other without seeing the author's
   reasoning.
4. A **longitudinal benchmark** that measures accumulation, cross-model
   transfer, interference, and retention together, with pre-registered kill
   criteria.

The claim is deliberately modest. We do not argue that an agent can become
unboundedly better at everything. We argue that a bounded, verifiable subset of
procedural knowledge can compound — and that the bottleneck is representation
and governance, not model size.

## 2. Why the question is hard

### 2.1 Three conflations

The literature often conflates three different things:

- **Memory of facts** (what happened, who said what).
- **Memory of cases** (a similar past situation and its outcome).
- **Procedural memory** (a conditional routine that can be executed).

Retrieval-augmented generation mostly addresses the first. Case-based reasoning
addresses the second (Memento; Zhou et al., 2025). Skill libraries address the
third, but usually in a single environment and with a single model (Voyager;
Wang et al., 2023; SkillWeaver; Zheng et al., 2025).

Cumulative procedural knowledge requires all three, plus a promotion mechanism
that decides when a routine is trustworthy enough to reuse.

### 2.2 The transfer problem

A procedure learned by model A is entangled with model A's habits: how it calls
tools, how it formats intermediate steps, what it does when a call fails. Move
the procedure to model B and three things can break:

1. **Syntax**: tool names, argument schemas, message formats.
2. **Policy**: the new model may need different decomposition or more explicit
   instructions.
3. **Competence**: the new model may simply be worse at a sub-step.

Most skill libraries store procedures as code or prompts, which makes them
portable only within the same runtime and model family. A procedure that cannot
survive a model swap is not cumulative knowledge; it is a cached prompt.

### 2.3 The evaluation problem

Existing benchmarks measure recall over long conversations (LoCoMo; Maharana et
al., 2024; LongMemEval; Wu et al., 2025) or success on a single task suite. They
do not measure:

- whether performance **improves over months** at fixed weights,
- whether a skill learned by one model **transfers** to another,
- whether gains **survive context resets**,
- whether the system **forgets** what it should retain,
- whether improvement is due to procedure or to retrieving similar cases.

Without these measurements, "self-improving agent" is a narrative, not a result.

### 2.4 The interference problem

Holton et al. (2026) show that humans and neural networks share a trade-off:
similar tasks produce more transfer and more interference; dissimilar tasks
produce less of both. A skill library that ignores this will either fragment
into uselessly specific routines or collapse into one overgeneralized procedure
that corrupts everything it touches. Domain policies and negative-transfer
tracking are not optional.

## 3. What the evidence says

We summarize the research base that motivates CUMULUS; a companion synthesis
provides the full review.

### 3.1 Neurology: two speeds and selective forgetting

The complementary learning systems framework (McClelland, McNaughton, &
O'Reilly, 1995; Kumaran, Hassabis, & McClelland, 2016) distinguishes a fast,
sparse, episodic system (hippocampus) from a slow, distributed, semantic system
(neocortex). Consolidation during sleep replays and **selects**; it does not copy
(Stickgold & Walker, 2013). Retrieval reconsolidates and can modify the trace
(Nader, Schafe, & LeDoux, 2000). Forgetting is adaptive and often a change in
accessibility rather than erasure (Richards & Frankland, 2017; Ryan &
Frankland, 2022).

**Design implication:** two stores, an offline compiler, and a forgetting policy
that archives rather than deletes.

### 3.2 Procedural learning: chunking under outcome feedback

The basal ganglia compile repeated action sequences into habits (Graybiel,
2008), while prefrontal control maintains goals and overrides habits when the
situation changes (Miller & Cohen, 2001). Model-based and model-free control
coexist (Daw et al., 2011). A procedure is not a text: it is a conditional
policy with a success history.

**Design implication:** skills need preconditions, postconditions, failure
branches, and per-context statistics.

### 3.3 Social learning: fidelity is the scarce resource

Orcas transmit ecotypes, dialects, and hunting techniques through matrilines;
post-reproductive females act as custodians of ecological knowledge (Brent et
al., 2015), and teaching can be intentional and costly (Guinet & Bouvier, 1995).
Primates and corvids show traditions and teaching-like behavior. Across taxa,
**high-fidelity transmission** is what makes culture cumulative (Tomasello,
1999; Henrich, 2015).

**Design implication:** sharing a transcript is low-fidelity emulation. Teaching
must be an explicit operation with verification that the learner can execute.

### 3.4 Social insects: stigmergy and quorum

Ants coordinate through decaying traces (Grassé, 1959; Goss et al., 1989) and
commit to a choice when encounters exceed a quorum (Pratt et al., 2002).
Division of labor emerges from individual thresholds (Bonabeau, Theraulaz, &
Deneubourg, 1996).

**Design implication:** shared traces with evaporation, quorum-based promotion,
and threshold-based routing.

### 3.5 Organizations: legitimacy and the iron cage

Weber's bureaucracy is a memory technology: jurisdiction, hierarchy, the file
(*Akten*), rules, and impersonality (Weber, 1922). It makes memory durable and
auditable, but rationalization can become an "iron cage" that preserves
structure at the expense of meaning.

**Design implication:** every skill needs provenance, an owner, a validity
regime, and a sunset clause.

### 3.6 Psychology: reconstruction and contamination

Memory is reconstructive (Bartlett, 1932), vulnerable to post-event
information (Loftus & Palmer, 1974), and subject to false memories (Roediger &
McDermott, 1995). Retrieval can inhibit competitors (Anderson, Bjork, & Bjork,
1994). Groups recall fewer unique items than the sum of individuals (Weldon &
Bellinger, 1997) and can contagiously adopt false memories (Roediger, Meade, &
Bergman, 2001). Confirmation bias and dissonance push agents to defend existing
decisions (Festinger, 1957; Nickerson, 1998).

**Design implication:** separate source from interpretation, use blind
verification, keep individual buffers, and force counter-evidence.

### 3.7 Human vs. machine learning

Humans learn patterns from fewer examples (Kühl, 2022) and exploit causal and
compositional structure (Lake et al., 2017). Machines compensate with scale.
Continual learning in networks suffers catastrophic interference (McCloskey &
Cohen, 1989; French, 1999), mitigated by replay and regularization (Kirkpatrick
et al., 2017; Rolnick et al., 2019). Holton et al. (2026) show that the
transfer/interference trade-off is shared, not a human special case.

**Design implication:** do not promise to eliminate interference; manage it by
domain and measure it.

## 4. Hypothesis

### 4.1 The cumulative-portability hypothesis

> **H1.** With frozen model weights, a model-agnostic procedural artifact layer
> that compiles verified traces into executable skills, validates them through
> blind cross-model execution, and governs them through a lifecycle, produces
> positive cumulative improvement on recurring verifiable task families and
> positive transfer to unseen models.

"Positive" is not a vibe. It is defined below.

### 4.2 Formal sketch

Let \(F\) be a task family, \(m\) a model, and \(C_t\) the canon at cycle \(t\).
Let \(S(F, m, C_t) \in [0,1]\) be success on held-out instances.

- **Accumulation:** \(S(F, m, C_t)\) has a positive slope in \(t\) after
  controlling for task difficulty, and the gain survives a context reset.
- **Retention:** the gain persists after \(k\) cycles without rehearsal for
  canonical skills, and decays for unused non-canonical skills.
- **Transfer:** for a skill \(s\) learned with model \(m\),
  \[
  T(s, m \to m') = \frac{S(F, m', C \cup \{s\}) - S(F, m', C)}
  {S(F, m, C \cup \{s\}) - S(F, m, C)}
  \]
  with \(T > 0\) meaning the skill helps the new model.
- **Portability:** \(P(s, m')\) is the expected success of \(s\) under \(m'\).
  A good portability estimator predicts transfer (AUC ≥ 0.7 in the proposed
  benchmark).
- **Attribution:** removing the canon returns performance to the no-skill
  baseline, confirming that gains live in artifacts, not in hidden weight
  updates.

### 4.3 Sub-hypotheses

| # | Hypothesis | Primary metric | Threshold (proposed) |
|---|---|---|---|
| H1a | Skills accumulate over cycles | Success slope on recurring families | ≥ 10% relative gain over best baseline |
| H1b | Skills transfer across models | Transfer coefficient \(T\) | ≥ 0.5 for ≥ 50% of canonical skills |
| H1c | Gains survive context reset and model swap | Retention after reset/swap | ≥ 80% of peak gain |
| H1d | Gains are artifact-borne | Ablation of Canon | Return to baseline within noise |
| H1e | Compilation beats summarization | Success at equal token budget | ≥ 10% relative gain over ACE-style playbooks |
| H1f | Blind verification reduces contamination | False-promotion rate | ≥ 50% reduction vs. self-review |
| H1g | Typed artifacts beat free chat | Skill quality per 1k tokens | ≥ 20% improvement |

These thresholds are design targets for the first experiment, not empirical
claims.

### 4.4 Null hypothesis and confounds

The null is that any observed gain is explained by one of:

- retrieval of similar past cases (case-based memory),
- longer or better-curated prompts (context engineering),
- evaluator drift or task leakage,
- increased inference budget.

The benchmark must include baselines and ablations that isolate each.

## 5. The CUMULUS architecture

### 5.1 Overview

CUMULUS has five layers:

```
┌─────────────────────────────────────────────────────────────┐
│  POD        roles, blind audit, quorum, dissent, directory  │
├─────────────────────────────────────────────────────────────┤
│  CANON      validated skills, versions, portability matrix  │
├─────────────────────────────────────────────────────────────┤
│  FORGE      trace → causal core → SIR → tests → candidate   │
├─────────────────────────────────────────────────────────────┤
│  TRACE      immutable event log: task, actions, outcomes    │
├─────────────────────────────────────────────────────────────┤
│  BRIDGE     renderers, capability adapters, drift detection │
└─────────────────────────────────────────────────────────────┘
```

The name evokes accumulation. The layers are not a pipeline; they are a
metabolism. Trace feeds Forge; Forge proposes to Canon; Pod governs; Bridge
executes and measures.

### 5.2 Trace: the episodic layer

Every episode is an immutable record:

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

Design rules:

- **Immutable.** Corrections are new episodes linked to the old one, not edits.
  This is the "file" of Weber and the reconsolidation constraint of memory.
- **Provenance-complete.** Every skill can be traced to the episodes that
  produced it.
- **Redacted at the boundary.** Secrets are removed before storage; privacy is
  a property of the trace, not a later filter.

### 5.3 Forge: compiling experience into skills

Forge is the core novelty. It does not summarize a trace; it **compiles** it.

**Step 1 — Segment.** Identify decision points and tool boundaries in the
trace. A decision point is a step whose removal changes the outcome; a tool
boundary is a call with typed inputs and outputs.

**Step 2 — Abstract.** Replace concrete values with typed parameters. A path
`src/auth/session.ts` becomes `target_file: Path`; a test command becomes
`verify: Command`. The goal is to preserve the *role* of each value, not its
instance.

**Step 3 — Ablate.** In a sandbox, remove each step one at a time and re-run the
postcondition. The **causal core** is the minimal set of steps whose removal
breaks success. This is differential diagnosis, not imitation. It answers:
*which parts of what happened actually mattered?*

**Step 4 — Infer contracts.** From the pre-state, derive preconditions (files
present, tools available, permissions). From the post-state, derive executable
postconditions (tests pass, schema validates, output matches). From near-miss
traces, derive failure branches and repairs.

**Step 5 — Emit SIR.** The Skill Intermediate Representation is a typed DAG:

```yaml
skill:
  id: sk_...
  goal: "fix failing auth test without changing public API"
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
    - "no new dependencies"
  provenance: [ep_..., ep_...]
  stats:
    per_model: {m1: {n: 12, success: 0.83}, m2: {...}}
  status: candidate
  version: 0.1.0
```

**Step 6 — Test.** Generate or retrieve held-out instances; run the skill with
the author model and at least one other model; score with executable
verifiers. A candidate with no postcondition is rejected: if you cannot check
it, you cannot compile it.

**Step 7 — Nominate.** If the candidate passes quorum and blind audit, it goes
to Canon as `validated`; otherwise it is archived with the failure reason. The
archive is training data for Forge: failures teach which abstractions are
wrong.

### 5.4 Canon: the institutional layer

Canon is a versioned library of SIR skills, not a prompt. Each entry has:

- **Status:** candidate → validated → canonical → deprecated → archived.
- **Evidence:** episodes, test suites, cross-model runs.
- **Portability matrix:** success per (skill, model, domain).
- **Owner:** a curator agent accountable for revisions.
- **Validity interval:** skills can expire; a sunset date forces review.
- **Contradictions:** incompatible skills coexist with a link and evidence;
  they are not averaged.
- **Cost profile:** tokens, latency, tool calls per success.

Canon is deliberately small. Promotion is expensive; most candidates never
become canonical. This is the "quorum" of the ants and the "expediente" of
Weber: memory is not what happened, it is what has been **instituted**.

### 5.5 Pod: self-collaboration as a protocol

The Pod is not a chat room. It is a set of roles exchanging typed artifacts.

| Role | Function | Biological analogue |
|---|---|---|
| Scout | Detects a recurring need; proposes a task family | Ant explorer |
| Smith | Executes the task; produces a trace | Worker |
| Auditor | Blindly verifies a candidate skill | Immune system |
| Curator | Maintains Canon, schedules reviews, teaches | Orca matriarch |
| Historian | Audits provenance, contradictions, drift | Weberian clerk |
| Critic | Argues against promotion; preserves dissent | Prefrontal control |

**Typed messages** (no free-form context sharing):

- `CLAIM`: "task family F recurs; here is evidence."
- `EVIDENCE`: trace, verifier result, cost.
- `PROCEDURE`: a SIR candidate.
- `CHALLENGE`: a counterexample or a failed replication.
- `VERDICT`: promote / reject / needs more evidence.
- `TEACH`: a rendered skill plus a learner-specific scaffold.

**Blind audit.** The Auditor sees the SIR, the tests, and the evidence — not
the author's identity, reasoning, or model. This prevents self-preference,
sycophancy, and the social contagion documented in psychology. The Auditor may
run the skill with a different model; disagreement is recorded, not resolved by
vote.

**Quorum.** Promotion requires \(k\) independent successful executions across
at least two models and one domain holdout. Quorum size is a dial: higher means
precision, lower means speed.

**Dissent ledger.** A rejected skill is not deleted. Its counterexamples remain
linked, so future evidence can revive or definitively retire it. This is the
antidote to groupthink and to the "iron cage" of over-consolidation.

### 5.6 Bridge: model-agnostic execution

Bridge is what makes the architecture portable.

- **Capability abstraction.** Skills refer to capabilities (`read_file`,
  `run_tests`, `search_web`), not vendor-specific tools. Each runtime provides
  an adapter.
- **Renderer.** For each model family, a renderer compiles SIR into the model's
  prompt format, tool schema, and context budget. The renderer is versioned;
  changing it triggers a conformance run.
- **Conformance suite.** A fixed battery of tasks per skill, executed by every
  supported model. The result updates the portability matrix.
- **Portability score.** A Beta-Binomial estimate per (skill, model), updated
  after each execution. Routing uses Thompson sampling over expected utility:
  success probability × value − cost, with an exploration bonus for untested
  pairs.
- **Drift detection.** When a model version or tool API changes, Bridge reruns
  the conformance suite. A skill whose portability drops below threshold is
  flagged, re-forged, or retired.

This is the architectural answer to the transfer problem: **separate what the
skill means from how a model says it.**

## 6. The self-learning loop

```
1. Task arrives.
2. Router selects (skill, model) by expected utility + exploration.
3. Execute; log Trace.
4. If success is novel or uncertain:
     Forge drafts or updates a SIR candidate by causal ablation.
5. Auditor runs blind tests on held-out instances and ≥2 models.
6. If quorum passes: Canon promotes. Else: archive with failure reason.
7. Curator schedules spaced reviews; unused skills decay; canonicals get
   sunset dates.
8. Historian records provenance and contradictions; Bridge updates portability.
```

Two properties matter:

- **No weight updates.** The loop only writes artifacts, statistics, and
  routing policies.
- **Bounded growth.** Promotion is expensive and decay is active, so the Canon
  does not grow without limit. The system forgets by design.

### 6.1 What counts as "learning"

We distinguish:

- **Adaptation within a task**: prompt/context changes. Not cumulative.
- **Case memory**: retrieving a similar past episode. Useful, but not
  procedural.
- **Skill acquisition**: a reusable, conditional routine enters Canon. This is
  the unit of cumulative learning.
- **Skill refinement**: a canonical skill improves through new evidence. This
  is the unit of progress.

The hypothesis is about the last two.

## 7. The self-collaboration protocol

Self-collaboration is often implemented as multiple agents chatting. That
scales tokens, not competence. CUMULUS uses **artifact-mediated collaboration**:

1. **Decompose** the task into sub-tasks with typed contracts (inputs, outputs,
   postconditions).
2. **Assign** roles by the transactive directory (who has succeeded in this
   domain), not by turn-taking.
3. **Exchange artifacts**, not transcripts. Each artifact carries provenance and
   evidence.
4. **Verify blindly**: the Auditor does not know who produced the artifact.
5. **Record dissent**: a `CHALLENGE` blocks promotion until resolved by
   evidence, not by majority.
6. **Teach**: the Curator renders the skill for a novice agent with scaffolding;
   the novice executes; fidelity is measured and fed back.

Why this should work:

- It reduces context bloat: artifacts are compressed, typed, and reusable.
- It reduces contamination: blind audit and independent evidence.
- It exploits specialization: the directory routes to competence, not
  verbosity.
- It preserves minority knowledge: dissent is an asset, not noise.

## 8. Cross-model transfer

### 8.1 What transfers

A SIR skill transfers if:

- its capabilities exist in the target runtime (possibly via adapters),
- its preconditions and postconditions are expressible,
- its steps do not depend on model-specific quirks,
- the target model can execute each step above a competence floor.

Bridge measures each condition. Transfer is not assumed; it is estimated.

### 8.2 What does not transfer

- Skills that rely on a specific model's tool-call grammar.
- Skills that rely on a specific context layout or hidden prompt.
- Skills whose postcondition is a subjective judgment with no rubric.
- Skills that encode a model-specific failure repair ("when model X loops, say
  Y").

The last case is important: some "skills" are really model patches. CUMULUS
should classify them as **adapters**, not canon. Adapters live in Bridge; they
are versioned with the model, not with the procedure.

### 8.3 Portability as a first-class metric

Most skill libraries report success on the model that learned the skill. CUMULUS
reports the **portability matrix**:

```
              m1     m2     m3
skill A      0.82   0.74   0.61
skill B      0.91   0.88   0.84
skill C      0.55   0.31   0.22
```

Skill B is a candidate for canon; skill C is either domain-specific or brittle.
Routing uses this matrix. Research uses it to test H1b.

## 9. Evaluation

### 9.1 CUMULUS-Bench

A longitudinal benchmark with:

- **5 domains:** code repair, data pipelines, document synthesis, incident
  response, tool orchestration.
- **10 task families per domain**, each with 20 instances and an executable
  verifier (tests, schema checks, rubric with double scoring).
- **3 model families** with different tool syntax and context limits.
- **6 cycles** (simulating 12 weeks), 150 tasks per cycle.
- **Model swap** at cycle 3 and cycle 5 to test transfer.
- **Context reset** every cycle to test retention.
- **Hidden holdouts** per family to detect overfitting to the verifier.

### 9.2 Conditions

| Condition | Description |
|---|---|
| C0 | Zero-shot, no memory |
| C1 | RAG over past episodes |
| C2 | Reflexion-style verbal feedback |
| C3 | Voyager-style code skill library (single model) |
| C4 | ACE-style evolving playbook |
| C5 | Memento-style case-based memory |
| C6 | CUMULUS without Bridge (single model) |
| C7 | CUMULUS full |

### 9.3 Metrics

- **Success rate** on held-out instances per cycle.
- **Accumulation slope** (mixed-effects model with task difficulty as covariate).
- **Retention** after reset and after model swap.
- **Transfer coefficient** \(T\) and **negative transfer** rate.
- **Portability AUC**: does the predicted matrix rank skills correctly?
- **Cost per success** (tokens, latency, tool calls).
- **Fidelity**: procedure conformance (steps executed as specified).
- **Contamination**: false skills promoted; skills that pass tests but fail
  holdouts.
- **Time-to-competence** for a new model or agent.

### 9.4 Ablations

Remove Forge (use summaries), blind audit (use self-review), Bridge (single
model), decay (keep everything), typed artifacts (free chat), and Canon
provenance (no trace links). Each ablation tests a specific claim.

### 9.5 Kill criteria

After 6 cycles, CUMULUS must:

- beat the best baseline by ≥10% relative on at least 2 of 4 primary metrics
  (success, retention, transfer, cost), and
- achieve a transfer coefficient ≥0.5 for at least half of canonical skills,
  and
- show portability AUC ≥0.7.

If not, the hypothesis fails for this design. The correct response is to
simplify, not to add modules.

## 10. Related work

**Agent memory.** MemGPT/Letta pages context between main and external memory
(Packer et al., 2023). Generative Agents retrieve by recency, importance, and
relevance (Park et al., 2023). Mem0 extracts and consolidates facts (Chhikara et
al., 2025). Zep/Graphiti adds temporal validity to a knowledge graph (Rasmussen
et al., 2025). HippoRAG uses hippocampal indexing and graph propagation
(Gutiérrez et al., 2024, 2025). MemoryBank applies Ebbinghaus decay (Zhong et
al., 2024). These systems store knowledge; CUMULUS stores procedures.

**Skill libraries and experience.** Voyager accumulates executable skills in
Minecraft (Wang et al., 2023). SkillWeaver synthesizes reusable web skills as
APIs (Zheng et al., 2025). Agent Workflow Memory induces reusable workflows
(Wang, Fried, & Neubig, 2024). ExpeL extracts natural-language insights from
experience (Zhao et al., 2024). Reflexion uses verbal feedback (Shinn et al.,
2023). ACE evolves a textual playbook (Zhang, Q., et al., 2025). Memento uses
case-based memory without weight updates (Zhou et al., 2025). CUMULUS differs in
its commitment to a model-agnostic executable representation, causal
compilation, blind cross-model verification, and portability as a measured
property.

**Self-improvement.** The Darwin Gödel Machine modifies its own code and
selects variants by benchmark performance (Zhang, J., et al., 2025). That is
self-modification at the code level; CUMULUS is self-modification at the
procedural-artifact level, with a much smaller and auditable search space.

**Continual learning.** EWC (Kirkpatrick et al., 2017) and replay (Rolnick et
al., 2019) protect weights. CUMULUS does not touch weights; its stability
comes from Canon governance and its plasticity from Forge.

## 11. Limitations, safety, and governance

### 11.1 Limits of the claim

- **No new latent competence.** If a model cannot execute a step at all, a
  skill cannot conjure the ability. CUMULUS amplifies and organizes competence;
  it does not create it.
- **Verifier bottleneck.** Skills need checkable postconditions. Domains
  without verifiers require rubrics or humans, which slows accumulation.
- **Simulated months.** A 12-week simulation is not a year of API drift, model
  deprecations, and organizational change. The real test is longitudinal
  deployment.
- **Transfer is partial.** Some skills will be model-specific. The architecture
  should report this honestly, not hide it.

### 11.2 Safety risks

- **Skill poisoning.** An adversary can inject a trace that compiles into a
  harmful or self-serving skill. Mitigations: provenance, permissioned Canon,
  blind audit, holdout tests, rollback.
- **Verifier gaming.** Skills can overfit to tests. Mitigations: hidden
  holdouts, adversarial tests, multiple verifiers.
- **Reward hacking at the routing level.** The system may prefer skills that
  look cheap but fail in distribution. Mitigations: calibrated portability,
  cost-adjusted success, periodic audits.
- **Opacity.** A growing Canon can become an unreadable bureaucracy. Mitigation:
  human-readable summaries, sunset reviews, and an explicit "why" field.

### 11.3 Governance

Memory is a commons (Ostrom, 1990). CUMULUS needs:

- **Write permissions**: who can promote to Canon.
- **Provenance**: every skill traceable to episodes.
- **Contradiction policy**: incompatible skills coexist with evidence.
- **Sunset policy**: canonical skills expire unless revalidated.
- **Privacy**: redaction at the trace boundary; local-first by default.
- **Audit**: an external reader can reconstruct why a skill exists.

## 12. Conclusion

The question was whether an agent can accumulate procedural knowledge over
months, transfer it across models, and improve without retraining. The answer
defended here is conditional: **yes, if the unit of learning is a portable,
verified artifact rather than a prompt or a transcript.**

CUMULUS makes three bets:

1. **Representation bet:** procedures can be separated from model syntax.
2. **Verification bet:** blind cross-model execution is a better promotion gate
   than self-review.
3. **Institutional bet:** a skill library needs governance, custodians, decay,
   and dissent to remain useful over months.

If the bets hold, the result is not a smarter model. It is a **memory
institution**: a system that turns experience into competence, keeps what
works, retires what does not, and can hand its knowledge to a model it has
never met.

---

## References

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
