# Pre-registration (DRAFT — freeze and timestamp BEFORE any Δ run, after E0)

## Hypotheses
- **H1** Baseline verifier relational recall ρ equals the fraction of violation-bearing peer classes covered by its probe set; SPRR falls in proportion to ρ.
- **H2** Narrowing certificate: Pr[unseen-class failure mass > U_v] ≤ δ when T ≥ τ_max; coverage collapses when T < τ_max.
- **H3** On task family T4 ("fix handshake timeouts"), baseline agents choose PQ-removing fixes in ≥ 20% of episodes; with Δ1 counterexample feedback the PQ-preserving-fix rate rises significantly.
- **H4** Under artifact-scoped verifiers (B1–B3), the frontier model's SPRR is not lower than that of the open-weight models (equivalence margin ±5 pp).

## Primary endpoints and contrasts
- SPRR, OWE (superiority); Cov (non-inferiority, margin −5 pp).
- Contrasts: full-Δ vs {B4, B5, B6, B8, B10}; Holm–Bonferroni across 5.

## Exclusions
- Episodes with infrastructure failure before the first agent action (container crash) are re-run once; the rule is logged.
- No other exclusions. All seeds reported.

## Stopping
- Fixed design: 72 tasks × 3 models × 5 seeds (fallback 36 × 3 × 3 declared before start if budget-limited).

## Frozen artifacts (fill at freeze)
- git commit: …
- population spec hash: …
- task-suite hash: …
- container digests: …
