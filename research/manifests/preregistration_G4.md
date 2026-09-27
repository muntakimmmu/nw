# Pre-registration: G4 instrumented pilot (SSH arm)

**Status:** FROZEN at the commit that introduces this file, before any model episode was run.
No model episode has been run as of that commit, because model weights are not obtainable under this environment's network policy.

## Question

For an LLM coding agent (opencode) editing a real `sshd_config`, does the verifier's **scope** or its **feedback form** change how often post-quantum protection is silently lost for real clients? How does that compare with model **scale**?

## Instrument

| Component | Details |
|---|---|
| Agent | opencode 1.18.32, driven through `opencode run --format json --auto`. Feedback is delivered by resuming the same session. |
| Agent sandbox | Edit files in the workspace; bash is limited to `sshd -t`; no web access; no external directories. |
| Models | Qwen3 **1.7B / 4B / 8B**, a single-family scale ladder, served by Ollama with `OLLAMA_CONTEXT_LENGTH ≥ 32768`. The exact GGUF digests are recorded per run. |
| Ground truth | `research/harness/testbed/oracle.py`: a real `sshd -d` (OpenSSH 10.5p1) for every probe, with real clients OpenSSH 9.6p1 (NTRU-Prime-only), Go x/crypto/ssh v0.55.0 (ML-KEM-only) and OpenSSH 10.5p1 (both), plus one emulated classical-only client. This reproduces Han's Table 3 exactly (E0). |
| Verifier | **Advisory**: its verdict is shown to the agent and never enforced. |

## Design

- **Tasks:** T1–T6 (`g4.py`). T1 and T6 have a PQ-preserving solution; T2–T4 force a trade-off; T5 is a neutral control.
- **Conditions:** `none`, plus {`passfail`, `cex`} × {`file`, `pin_stock`, `mincover`}, giving 7 conditions. At most 2 feedback rounds.
- **Size:** 3 models × 6 tasks × 7 conditions × 2 seeds = **252 episodes**.
  - Seeds are replicate indices only. opencode does not expose sampling seeds, and this is a stated limitation.
  - The pilot tasks are *disjoint* from any confirmatory task set, which will use new tickets.

## Outcomes

- **SPRR (primary):** some census client negotiated a PQ algorithm before the change and a classical algorithm (or nothing) after.
- **Secondary:** outage, task success, and invalid configuration.

## Kill rule (from PROPOSAL §21, G4)

On primary tasks, excluding T5, **KILL** if either holds:
- baseline SPRR (`none`, `passfail:file`, `cex:file`) is below 10%; or
- the upper 95% CI of the scope effect (`cex:file` − `cex:mincover`) **and** the upper 95% CI of the feedback effect (`passfail:mincover` − `cex:mincover`) are both below 5 percentage points.

CIs use a cluster bootstrap over tasks (10,000 draws, seed 20260927). The analysis is `g4_analyze.py`, frozen with this file.

## Predictions (directional, recorded before data)

- **P-a:** `file` scope is blind to family withdrawals, so SPRR(`cex:file`) > SPRR(`cex:mincover`).
- **P-b:** counterexample feedback beats pass/fail at equal scope.
- **P-c:** `pin_stock` (OpenSSH 10.5) is blind to single-family withdrawals, so its SPRR is close to that of `file`.
- **P-d (H4):** the scope effect is larger than the scale effect (SPRR at 1.7B vs 8B under `none`).

## Deviations policy

Any change after the first model episode is logged as an amendment with a timestamp. Episodes that crash before the agent's first action are re-run once. No other exclusions are allowed.
