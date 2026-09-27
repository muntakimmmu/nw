# Agentic PQC in Action for Infrastructure Security

This directory holds the multi-agent lab's research programme.

**Status:** proposal stage. Nothing has been implemented yet: per the lab protocol (§24–25), implementation begins only after a GO decision and the baseline reproduction (E0).

| Path | Contents |
|---|---|
| `paper/PROPOSAL.md` | The full 21-section research report (final output format) |
| `paper/REVIEW_AgentH.md` | Independent adversarial review |
| `claims.yaml` | Claim → experiment contract |
| `manifests/experiment_manifest.schema.yaml` | Per-run record schema |
| `manifests/preregistration.md` | Hypotheses, endpoints and contrasts, frozen before any Δ run |
| `analysis/verify_lemmas.py` | Stdlib brute-force checks of theory lemmas P1, P2, P4 (boundary) and P5 |
| `analysis/verify_lemmas.out` | Output of the lemma checks |

Reproduce the lemma checks:

```bash
python3 research/analysis/verify_lemmas.py
```

The run takes about 2 seconds and needs only the standard library.
