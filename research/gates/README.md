# Gate records

| Gate | Status | Record |
|---|---|---|
| G1 | PASSED | `G1.md` |
| G2 | PARTIAL PASS (full text blocked) | `G2.md` |
| G3 | PASSED | `g3_han_episodes.py`, `g3_han_episodes.out` |
| E0 (SSH) | REPRODUCED (Han's Table 3, real clients) | `E0_ssh.out` |
| G4 | INSTRUMENT READY and pre-registered; no model episodes run (model weights unreachable under network policy) | `../harness/`, `../manifests/preregistration_G4.md` |
| G5 | OPEN, non-blocking | PROPOSAL.md §21 |

To reproduce G3, clone the artifact, then run the script against it:

```bash
git clone https://github.com/hanzunye/pq_repo
python3 research/gates/g3_han_episodes.py ./pq_repo
```
