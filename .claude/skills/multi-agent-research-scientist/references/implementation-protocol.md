# Implementation protocol

Method code starts only after a GO verdict. *Instrument* code (testbed, harness, baselines, frozen scorer) may be built earlier to run a pre-GO gate.

## Directory layout

```text
research/
├── configs/      preprocessing/  baselines/   proposed/    experiments/
├── ablations/    robustness/     statistics/  analysis/    figures/
├── tests/        manifests/      paper/       gates/       harness/
└── claims.yaml
```

- `gates/` holds one evidence file per gate: `G1.md`, `g3_*.py` with its `.out`, `E0_*.out`.
- `harness/` holds instruments used before GO.

## Every run stores

Record these fields for every run, in append-only JSONL under `research/manifests/runs/<experiment_id>.jsonl`. The schema is in `assets/run_manifest.schema.yaml`.

```text
experiment_id  run_id  git_commit  dataset_version  seed  configuration_hash
model / model_parameters  hardware  training_or_wall_time  tokens/cost  metrics  timestamp
```

## Baseline-first rule

1. Reproduce the baseline, and ideally P\*'s key table, on your own instrument (E0).
2. Verify it against the reported numbers. Use the authors' audit scripts if they ship any.
3. Freeze the evaluation pipeline and commit it, together with a pre-registration (`assets/preregistration.md`).
4. Only then implement Δ.

Never change baseline preprocessing after seeing the proposed method's results unless every experiment is rerun.

## Claim-first experimentation

Maintain `research/claims.yaml` (template in `assets/claims.yaml`). A claim needs experiments, and an experiment needs a claim. Update each claim's status (HYPOTHESIZED / SUPPORTED / REFUTED / WITHDRAWN) with a pointer to the evidence file. Keep killed claims in an audit-trail section rather than deleting them.

## Engineering hygiene learned in practice

- **Score artifacts, not narratives.** The oracle should decide from the produced artifact and real behaviour (real handshakes, executions, parsers), never from the agent's or model's account of what it did.
- **Sanity-check sandboxed agent harnesses** before real runs. Run a scripted stand-in model through the real agent binary to validate the plumbing. Label such runs "plumbing only" and keep them out of the results files.
- **Make runners resumable**: skip cells already recorded. Record exact model, tool and container versions.
- **Keep secrets out of the repository.** Private keys, tokens and generated host keys go in a `.gitignore`, as do large binaries.
- **Network policy.** If a required host is blocked (model registries, paper servers), tell the user exactly which host is denied and how to allow it, or give a command to run on their own machine. Do not route around the policy through mirrors or alternate registries.
- **Integrity labels in every artifact** (KNOWN / OBSERVED / HYPOTHESIZED / PROPOSED / NOT YET VERIFIED). No fabricated results. Never claim that runs happened when they did not.
