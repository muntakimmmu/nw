# Final report template (exact section order)

Save the report to `research/paper/PROPOSAL.md` unless the user asks otherwise.

## Header

Start the file with:
- the title;
- the date;
- a status line, e.g. "PROPOSAL, NOT YET VERIFIED", later revised to "REVISED after adversarial review";
- an epistemic-label legend: KNOWN / OBSERVED / HYPOTHESIZED / PROPOSED / NOT YET VERIFIED, and `[FULL TEXT]` / `[V-snippet]` / `[U]`.

## Sections, in this exact order

1. **Topic Interpretation.** The problem, primary and secondary readings, marked ASSUMPTIONS, why it matters, and the precise research question you isolate.
2. **Frontier Literature Map.** 10–30 papers in tables grouped by *methodological relationship*, not chronology. Give each a short key, such as `[Han26]`, and a verification label.
3. **Mathematical Ancestors.** The existing equations and models (A1, A2, …).
4. **Closest Prior Work.** P\*, with a side-by-side table (object, main result, scope, guarantee) and the single-sentence difference. If P\* is later read in full and this changes, add a visible CORRECTION block here.
5. **Assumption–Regime Matrix.**
6. **Candidate Unsolved Problems.** At least five, with an R_gap table.
7. **Selected Failure Regime.** Why it matters.
8. **Failure Mechanism.** For each failure (F1, F2, …): observed failure → measurable cause → the variable to measure → hypothesis.
9. **Candidate Functional Modifications.** At least five Δs, in a table with the selection rationale.
10. **Novelty Collision Report.** Each candidate against the literature and industry practice, plus the red-team queries you ran.
11. **Selected Contribution.** The exact mathematical formulation: setting, baseline loop, the modified operation only, theory (propositions with status OBSERVED by check, proof sketch, or NOT YET VERIFIED), and what you deliberately do not claim.
12. **Novelty Contract.** The contract text, plus the two formulas and the one-sentence test (templates below).
13. **Expected Scientific Insight.** What researchers learn even if the gains are modest.
14. **Strongest Competitors.** The baselines table, including the simplest practitioner rule and the matched controls.
15. **Experiment Matrix.** Main, mechanism (dose-response), ablation, robustness, generalization with a negative control, efficiency, and falsification, each mapped to a claim.
16. **Statistical Testing Plan.** Unit of analysis, tests, multiplicity, computed power, pre-registration.
17. **Reproducibility Plan.** Manifest, pinned artifacts, determinism, baseline-first, release.
18. **Adversarial Reviewer Report.** From Agent H: scores, recommendation, decisive objections.
19. **Author Rebuttal Simulation.** A table with columns: reviewer point | response (concede or rebut) | evidence. Only evidence-supported rebuttals are allowed, and the section ends with the objections you cannot rebut.
20. **Contribution Scorecard.** The block below, plus the Q-score and novelty vector for each candidate version.
21. **GO / MODIFY / KILL.** The verdict, what was killed and why, what survives, the pre-GO gates table (see verification-and-evidence.md §2), and the one-sentence test for the surviving version.

## Appendices

- **A. Lemma-check output.** Verbatim output, with caveats about what the checks do not show.
- **B. Research-integrity ledger.** What has not been run; what is snippet-verified only; every correction and deviation.

## Novelty Contract

> Existing method **M** assumes **A**. Under important regime **R**, assumption **A** breaks, causing measurable failure **F**. We introduce **Δ**, a targeted modification designed specifically to address **F**. Δ changes **mechanism Z**, producing property **P**. Unlike closest prior methods **B1…Bn**, the proposed approach uniquely provides **X**. We test this through controlled experiments **E1…Ek**, including ablations, mechanism tests, cross-domain validation, statistical testing and explicit failure analysis.

Then state:

- M + A --R--> F
- M + Δ --R--> P

If the contract cannot be written convincingly, do not proceed.

## One-sentence test

> Existing method **M** performs well when **A** holds, but we show that it systematically fails under important regime **R** because of mechanism **F**. We introduce **Δ**, a minimal principled modification that directly alters **Z**, enabling previously unavailable property **P**. Across controlled comparisons, mechanism tests, ablations, external datasets and stress conditions, the evidence supports both **when** and **why** Δ works.

If the sentence is not compelling, keep researching instead of coding.

## Scorecard block

```text
Importance:
Novelty:
Mechanistic clarity:
Technical depth:
Evidence potential:
Generalization:
Reproducibility:
Computational feasibility:
Risk of prior-art collision:
Overall research potential:
```

When a framing is killed and redesigned, score the two versions side by side (v1 vs v2), and give projected scores explicitly conditional on the gates.

## Verdict rules

| Verdict | When |
|---|---|
| **GO** | Every tier passes and the one-sentence test is compelling. Only GO unlocks method code. |
| **MODIFY** | Promising, but list the specific problems and the gates, each with a kill condition. |
| **KILL** | A prior-art collision, including with production practice; weak significance; an untestable hypothesis; or insufficient differentiation. |

Never continue a weak idea because of sunk effort.

## Paper architecture (after GO)

| Part | What it contains |
|---|---|
| Title | Mechanism + problem + new property. No hype. |
| Abstract | Problem → limitation → principle → contribution → evidence → main result |
| Introduction | Importance → existing success → unresolved failure → why it fails → Δ → evidence |
| Related work | Organised by methodological relationship |
| Problem formulation | X, Y, θ, L, R |
| Method | The baseline maths first, then only the changed operation |
| Theory | Meaningful analysis only |
| Experiments | One claim per experiment |
| Discussion | Why, when, when not, implications |
| Limitations | The real ones |
