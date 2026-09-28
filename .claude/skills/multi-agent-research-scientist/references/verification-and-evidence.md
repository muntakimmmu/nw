# Verification, evidence and scoring

## Contents
1. The nine verification tiers
2. Pre-GO gates (form and examples)
3. Evidence pyramid
4. Baseline fairness protocol
5. Experiment matrix rules
6. Statistics checklist
7. Idea scoring and the consensus protocol
8. Stop conditions

---

## 1. The nine verification tiers

No idea proceeds to implementation until it passes all nine tiers.

| Tier | Gate | What passing requires |
|---|---|---|
| 1 | **Source** | Every important claim has a real, labelled source: title, authors, year, venue, DOI/arXiv, and the exact contribution. For P\*, the label must be `[FULL TEXT]`; if full text is blocked, ask the user to upload it. |
| 2 | **Novelty** | Closest paper P\* = argmin over papers P of D(P, proposal), with the difference stated in one sentence. If the difference cannot be stated clearly, the proposal fails. |
| 3 | **Functional (the Δ test)** | "What capability disappears if Δ is removed?" A strong answer is a lost guarantee, calibration, detection, a complexity class, robustness, or transfer. "Accuracy drops 0.3%" is a weak answer, and the Δ is rejected. |
| 4 | **Mechanism** | Δ → mechanism variable → outcome, with the mechanism variable measured *separately* from the outcome. If the outcome improves but the mechanism variable does not move, reconsider the explanation. Watch for mechanisms that hold *by construction*: they explain nothing. |
| 5 | **Competitive** | Beat, or honestly match, all of these: the strongest classical baseline, the strongest recent neural or agentic baseline, the closest prior method, the **simplest reasonable baseline (including the practitioner's one-line rule)**, the same model without Δ, a parameter-matched control, and a compute-matched control. |
| 6 | **Statistical** | Multiple seeds, CIs, paired tests, effect sizes, and power computed at the level of the *independent unit* (usually tasks or datasets, not episodes). |
| 7 | **Generalization** | In-domain, cross-domain, stress condition, and an external dataset where possible. |
| 8 | **Falsification** | Find the boundary R\* where Δ stops helping. Failure boundaries are results, so report them. |
| 9 | **Reproducibility** | Seeds, splits, preprocessing, dataset versions, search spaces, initialization, environment, hardware, stopping rules, checkpoints and tests, all regenerable from one run manifest. |

## 2. Pre-GO gates

When the verdict is MODIFY, write gates with this structure:

| Field | Content |
|---|---|
| Gate | A short name (G1, G2, …) |
| Action | The concrete thing to do: read, measure, reproduce, pilot |
| Kill / redirect condition | Explicit and pre-committed. For effects, use an upper-confidence-bound futility rule, e.g. "KILL if the upper 95% CI of effect X is below 5 pp". |
| Depends on | The other gates it needs |
| Status | Not started / PASSED / PARTIAL / BLOCKED (on what) / KILLED, with a link to the evidence file |

**Well-formedness checks** (each of these defects occurred in practice):
- The kill logic matches intent. A gate should kill only on the finding that actually invalidates the plan; an AND that should be an OR is a classic mistake.
- A gate that needs code must not sit behind a "no code until GO" rule. Separate *instrument* code (testbed, harness, baselines, the frozen scorer) from *method* code.
- The data source is feasible. If the closest paper already tried the same data collection and it failed its sample floor, don't repeat it. Use their released data instead.
- The statistics are unambiguous: say "upper CI bound < x", not "CI excludes x".
- A pilot's tasks and seeds are disjoint from the confirmatory ones.
- A "gate" with no kill condition is a claim limiter. Label it as one.

**Typical gates:**
- read P\* in full;
- resolve citation or ID conflicts;
- re-analyse P\*'s released artifact to answer a reviewer objection empirically;
- reproduce P\*'s key result on your own instrument (E0);
- an instrumented pilot with a futility rule;
- secure a real data source.

## 3. Evidence pyramid

| Layer | Question |
|---|---|
| 1. Sanity | Can the implementation reproduce known baselines or P\*'s key table? |
| 2. Main effect | Does M + Δ beat M? |
| 3. Ablation | Compare M, M + Δ₁, M + Δ₂, M + Δ₁ + Δ₂. |
| 4. Mechanism | Does the variable the theory predicts actually change? A dose-response (vary the amount of Δ) is strong evidence. |
| 5. Robustness | Under noise, imbalance, shift, scarcity, perturbation and adversarial inputs. |
| 6. Generalization | Across multiple datasets, domains or protocols. Include a **negative control** where the theory predicts no effect. |
| 7. Efficiency | Parameters, FLOPs, memory, latency, training or inference time, cost. |
| 8. Statistics | CIs and effect sizes. |
| 9. Failure analysis | When does Δ stop helping? |

## 4. Baseline fairness protocol

- Use the strongest reasonable implementation of every baseline, and never under-tune one on purpose.
- Match epochs, preprocessing, augmentation, compute and parameter count where applicable.
- Separate the gain due to architecture from the gain due to compute. Report gain per FLOP and gain per parameter when meaningful.
- If you wrote the tasks yourself, say so, and prefer real tasks from the field: public corpora, P\*'s released tickets, real traces. Author-written traps that baselines are designed to fail are leakage.

## 5. Experiment matrix rules

Use this table shape:

| Exp | Claim | Hypothesis | Baseline | Proposed | Metric | Expected evidence |
|---|---|---|---|---|---|---|

- Every experiment maps to a claim in `claims.yaml`, and every claim maps to at least one experiment. Remove orphans on either side.
- The minimum set is: main effect, mechanism, ablation, shift or robustness, scarcity or failure regime, external data, efficiency, and falsification.
- Report harm and progress **together**, so that "block everything" or "do nothing" cannot look like a win.

## 6. Statistics checklist

- **Unit of analysis and effective n.** Episodes nested in tasks, and tasks in models, are not independent. Bootstrap over clusters, or use mixed-effects models with random effects for the clustering unit.
- **Power.** Compute it, for example with a normal approximation or by simulation from pilot intraclass correlation. Never assert a power figure you didn't calculate.
- **Multiplicity.** Use Holm–Bonferroni across the pre-registered primary contrasts.
- **Report** risk differences or odds ratios with CIs, plus Cliff's δ or Cohen's d where appropriate. Report all seeds.
- **Non-inferiority.** For progress and utility metrics, declare the margin in advance.
- **Pre-registration.** Freeze hypotheses, metrics, contrasts, exclusions and stopping rules in a committed file before any Δ run.
- **Don't overclaim.** Never claim superiority when the CIs overlap the null.

## 7. Idea scoring and the consensus protocol

**Q = I × F × C × E × G**, each factor scored 0–1:

| Factor | Meaning |
|---|---|
| I | Importance |
| F | Strength of the demonstrated failure |
| C | Causal link between Δ and the failure |
| E | Feasibility of producing the evidence |
| G | Generality |

**Novelty vector N = (N_P, N_M, N_T, N_E)**: problem, method, theory, and empirical/insight novelty. Reject a proposal if all four are weak. Report this vector honestly: v1 of the proposal that shaped this skill scored (medium, low, low, low) and was killed.

**Consensus.** Each candidate gets an independent vote vector V = [novelty, importance, mechanism, evidence] from the novelty, domain, method and reviewer agents. Do not select by majority vote. Evidence overrides consensus. A single FATAL collision report must be investigated before anything proceeds.

## 8. Stop conditions (redesign, do not code)

| Failure | Condition |
|---|---|
| Novelty | Δ ≈ an existing paper, or ≈ an existing production practice |
| Mechanism | No measurable reason explains the expected gain |
| Evidence | The hypothesis cannot be isolated experimentally |
| Benchmark | The benchmark is trivial or saturated |
| Baseline | Δ only beats weak baselines |
| Generalization | The effect appears in only one favourable configuration |
| Complexity | The gain comes only from much more compute |
