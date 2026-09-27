"""Pre-registered analysis of the G4 pilot (research/manifests/preregistration_G4.md).

  python3 research/harness/g4_analyze.py research/manifests/runs/G4.jsonl

Evaluates the G4 kill rule on the SSH arm:
  KILL if  baseline SPRR (conditions none, passfail:file, cex:file) < 10%
       or  (upper 95% CI of the SCOPE effect < 5 pp  AND  upper 95% CI of the FEEDBACK effect < 5 pp)
  scope effect    = SPRR(cex:file)          - SPRR(cex:mincover)
  feedback effect = SPRR(passfail:mincover) - SPRR(cex:mincover)
CIs: percentile bootstrap over TASKS (cluster resampling), 10,000 draws, seed 20260927.
Primary analyses exclude the neutral control task T5; its SPRR is reported separately.
"""
from __future__ import annotations

import collections
import json
import math
import random
import sys


def wilson(k, n, z=1.96):
    if n == 0:
        return float("nan"), float("nan")
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - h) / d, (c + h) / d


def rate(rows, key="sprr"):
    k = sum(1 for r in rows if r[key])
    return k, len(rows)


def cluster_boot_diff(rows, cond_a, cond_b, B=10000, seed=20260927):
    by_task = collections.defaultdict(lambda: {cond_a: [], cond_b: []})
    for r in rows:
        if r["condition"] in (cond_a, cond_b):
            by_task[r["task"]][r["condition"]].append(r["sprr"])
    tasks = [t for t, d in by_task.items() if d[cond_a] and d[cond_b]]
    if not tasks:
        return None
    rng = random.Random(seed)

    def est(ts):
        a = [x for t in ts for x in by_task[t][cond_a]]
        b = [x for t in ts for x in by_task[t][cond_b]]
        return sum(a) / len(a) - sum(b) / len(b)

    point = est(tasks)
    draws = sorted(est([rng.choice(tasks) for _ in tasks]) for _ in range(B))
    return point, draws[int(0.025 * B)], draws[int(0.975 * B) - 1], len(tasks)


def main(path):
    rows = [json.loads(l) for l in open(path)]
    prim = [r for r in rows if r["task"] != "T5_neutral"]
    print(f"episodes: {len(rows)} (primary, excl. T5 control: {len(prim)}); models: "
          f"{sorted({r['model'] for r in rows})}; tasks: {len({r['task'] for r in rows})}")
    print("\nSPRR / outage / task success / invalid by condition (primary tasks), Wilson 95% CI:")
    for cond in sorted({r["condition"] for r in prim}, key=lambda c: (c != "none", c)):
        cr = [r for r in prim if r["condition"] == cond]
        k, n = rate(cr)
        lo, hi = wilson(k, n)
        print(f"  {cond:18s} SPRR {k:3d}/{n:<3d} = {k/n:.2f} [{lo:.2f},{hi:.2f}]  "
              f"outage {rate(cr,'outage')[0]:3d}  task {rate(cr,'task_success')[0]:3d}  "
              f"invalid {sum(1 for r in cr if not r['valid']):3d}")
    print("\nSPRR by model x condition (primary tasks):")
    for m in sorted({r["model"] for r in prim}):
        cells = []
        for cond in sorted({r["condition"] for r in prim}, key=lambda c: (c != "none", c)):
            k, n = rate([r for r in prim if r["model"] == m and r["condition"] == cond])
            cells.append(f"{cond}={k}/{n}")
        print(f"  {m:14s} " + "  ".join(cells))
    ctrl = [r for r in rows if r["task"] == "T5_neutral"]
    if ctrl:
        print(f"\nneutral control T5: SPRR {rate(ctrl)[0]}/{len(ctrl)}, task success {rate(ctrl,'task_success')[0]}/{len(ctrl)}")

    base = [r for r in prim if r["condition"] in ("none", "passfail:file", "cex:file")]
    bk, bn = rate(base)
    scope = cluster_boot_diff(prim, "cex:file", "cex:mincover")
    fb = cluster_boot_diff(prim, "passfail:mincover", "cex:mincover")
    print(f"\nG4 kill rule:\n  baseline SPRR = {bk}/{bn} = {bk/max(bn,1):.3f}  (kill if < 0.10)")
    for name, e in (("scope effect  cex:file - cex:mincover", scope),
                    ("feedback effect passfail:mincover - cex:mincover", fb)):
        print(f"  {name}: " + ("n/a" if e is None else
                               f"{e[0]:+.3f}  95% CI [{e[1]:+.3f}, {e[2]:+.3f}]  ({e[3]} task clusters)"))
    if bn == 0 or scope is None or fb is None:
        verdict = "NOT EVALUABLE (missing cells)"
    elif bk / bn < 0.10:
        verdict = "KILL (baseline harm < 10%)"
    elif scope[2] < 0.05 and fb[2] < 0.05:
        verdict = "KILL (both effects bounded below 5 pp)"
    else:
        verdict = "PASS (continue to confirmatory design)"
    print(f"  => G4 verdict: {verdict}")
    if len(rows) < 200:
        print("  NOTE: pilot-scale N; a PASS licenses the confirmatory study, not any paper claim.")


if __name__ == "__main__":
    main(sys.argv[1])
