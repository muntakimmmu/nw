# Gate records

| Gate | Status | Record |
|---|---|---|
| G1 | PASSED | `G1.md` |
| G2 | PARTIAL PASS (full text blocked) | `G2.md` |
| G3 | PASSED | `g3_han_episodes.py`, `g3_han_episodes.out` |
| G4 | BLOCKED on user (API keys and budget) | PROPOSAL.md §21 |
| G5 | OPEN, non-blocking | PROPOSAL.md §21 |

To reproduce G3, clone the artifact, then run the script against it:

```bash
git clone https://github.com/hanzunye/pq_repo
python3 research/gates/g3_han_episodes.py ./pq_repo
```
