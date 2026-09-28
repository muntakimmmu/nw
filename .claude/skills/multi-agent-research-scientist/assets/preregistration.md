# Pre-registration: <study name>

**Status:** FROZEN at the commit that introduces this file, before any Δ or confirmatory run.

## Question
<one paragraph>

## Instrument
- Ground-truth oracle, which decides from real behaviour and never from the model's own account: <…>
- Baselines, including the practitioner's one-line rule: <…>
- Versions and hashes of the models, tools and data: <…>

## Design
- Conditions: <…>
- Tasks or datasets: <…>, disjoint from any pilot.
- Seeds and replicates: <…>
- Total N: <…>
- Effective n (the independent unit): <…>

## Outcomes
- Primary: <…>
- Secondary: <…>
- Harm and progress are reported together.

## Analysis
- Model or test: <e.g. mixed-effects logistic model; cluster bootstrap over tasks, 10,000 draws, fixed seed>
- Multiplicity: Holm–Bonferroni across <k> primary contrasts.
- Power: <computed value and method>.
- Kill / futility rule: <e.g. KILL if the upper 95% CI of the effect is < 5 pp>.

## Predictions (directional, recorded before any data)
- P-a: <…>
- P-b (negative control): <…>

## Exclusions and deviations
- Only pre-declared exclusions are allowed.
- Any change after the first confirmatory run is logged as a timestamped amendment.
