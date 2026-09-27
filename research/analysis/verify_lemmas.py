"""Brute-force sanity checks for the theoretical claims in research/paper/PROPOSAL.md.

These are NOT experiments on the proposed method. They check that the small
combinatorial / statistical lemmas the proposal relies on are actually true on
exhaustively enumerated or simulated small instances. Stdlib only.

Run:  python3 research/analysis/verify_lemmas.py
"""
from __future__ import annotations

import itertools
import math
import random
from collections import Counter, deque

SEED = 20260927
C, P, S = "x25519", "mlkem768x25519", "sntrup761x25519"
ALGS = (C, P, S)
PQ = {P, S}


# ---------------------------------------------------------------- model
def neg(a_client: frozenset, a_server: frozenset, pref_server: tuple):
    """Responder-chooses negotiation (TLS 1.3 / SSH server-preference style)."""
    for alg in pref_server:
        if alg in a_client and alg in a_server:
            return alg
    return None


def avail(a_u, a_v):
    return bool(a_u & a_v)


def all_subsets(xs):
    xs = list(xs)
    for r in range(len(xs) + 1):
        yield from itertools.combinations(xs, r)


# ---------------------------------------------------------------- L1/L2
def check_product_condition(trials=4000):
    """L2: a wave (async per-node application) preserves availability on every
    interleaving  <=>  every edge is available on the product of {old,new}
    states of its endpoints.  L1 (widening-only waves are safe if the old
    state was safe) follows as a corollary and is checked separately."""
    rng = random.Random(SEED)
    nonempty = [frozenset(s) for s in all_subsets(ALGS) if s]
    mismatches = widen_violations = 0
    for _ in range(trials):
        n = rng.randint(2, 5)
        edges = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < 0.6]
        old = [rng.choice(nonempty) for _ in range(n)]
        # ensure old state is available
        if not all(avail(old[u], old[v]) for u, v in edges):
            continue
        wave = [v for v in range(n) if rng.random() < 0.6]
        widen_only = rng.random() < 0.5
        new = list(old)
        for v in wave:
            new[v] = old[v] | rng.choice(nonempty) if widen_only else rng.choice(nonempty)
        # explicit interleavings: every permutation, every prefix
        explicit_ok = True
        for perm in itertools.permutations(wave):
            for k in range(len(perm) + 1):
                cur = list(old)
                for v in perm[:k]:
                    cur[v] = new[v]
                if not all(avail(cur[u], cur[v]) for u, v in edges):
                    explicit_ok = False
        product_ok = all(
            avail(a, b)
            for u, v in edges
            for a in {old[u], new[u]}
            for b in {old[v], new[v]}
        )
        mismatches += explicit_ok != product_ok
        if widen_only and not explicit_ok:
            widen_violations += 1
    return mismatches, widen_violations


# ---------------------------------------------------------------- L3
def pq_dominant_widening_preserves_Q(trials=4000):
    """L3: adding algorithms ranked below *every* PQ algorithm the responder
    offers cannot flip a PQ negotiation to classical.  Ranking the addition
    below only the *best* PQ algorithm is NOT enough: a client that shares
    only a lower-ranked PQ family (incomparable classes) gets flipped.  Both
    the sound condition and the unsound 'below best' condition are checked."""
    rng = random.Random(SEED + 1)
    safe_violations, counterexamples, below_best_violations = 0, 0, 0
    for _ in range(trials):
        client = frozenset(rng.sample(ALGS, rng.randint(1, 3)))
        server = frozenset(rng.sample(ALGS, rng.randint(1, 3)))
        pref = tuple(rng.sample(ALGS, 3))
        if neg(client, server, pref) not in PQ:
            continue
        add = rng.choice([a for a in ALGS if a not in server] or [None])
        if add is None:
            continue
        new_server = server | {add}
        pq_ranks = [pref.index(a) for a in server if a in PQ]
        dominated = pref.index(add) > max(pq_ranks)
        below_best = pref.index(add) > min(pq_ranks)
        flipped = neg(client, new_server, pref) not in PQ
        if below_best and not dominated and flipped:
            below_best_violations += 1
        if dominated and flipped:
            safe_violations += 1
        if not dominated and flipped:
            counterexamples += 1
    return safe_violations, counterexamples, below_best_violations


# ---------------------------------------------------------------- L4
def zero_outage_feasible(n, edges, no_dual):
    """BFS over global states. Normal nodes: {c} -> {c,p} -> {p}.
    no_dual nodes: {c} -> {p} (cannot hold the widened state).
    A step = any nonempty set of nodes each advancing one stage, applied
    asynchronously (product condition). Goal: every node at {p}."""
    stages = {
        False: [frozenset({C}), frozenset({C, P}), frozenset({P})],
        True: [frozenset({C}), frozenset({P})],
    }
    last = [len(stages[v in no_dual]) - 1 for v in range(n)]
    start, goal = tuple([0] * n), tuple(last)
    seen, q = {start}, deque([start])
    while q:
        st = q.popleft()
        if st == goal:
            return True
        movable = [v for v in range(n) if st[v] < last[v]]
        for wave in all_subsets(movable):
            if not wave:
                continue
            nxt = list(st)
            for v in wave:
                nxt[v] += 1
            ok = all(
                avail(stages[u in no_dual][a], stages[v in no_dual][b])
                for u, v in edges
                for a in {st[u], nxt[u]}
                for b in {st[v], nxt[v]}
            )
            t = tuple(nxt)
            if ok and t not in seen:
                seen.add(t)
                q.append(t)
    return False


def min_vertex_cover_size(nodes, edges):
    for r in range(len(nodes) + 1):
        for cover in itertools.combinations(nodes, r):
            cs = set(cover)
            if all(u in cs or v in cs for u, v in edges):
                return r
    return len(nodes)


def check_vertex_cover_lemma(trials=300):
    """L4: a zero-outage migration exists iff G[S] has no edge; the minimum
    number of translating proxies (a proxy turns its node into a dual-stack
    node) equals the minimum vertex cover of G[S]."""
    rng = random.Random(SEED + 2)
    bad = 0
    for _ in range(trials):
        n = rng.randint(2, 6)
        edges = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < 0.5]
        no_dual = {v for v in range(n) if rng.random() < 0.5}
        es = [(u, v) for u, v in edges if u in no_dual and v in no_dual]
        feasible = zero_outage_feasible(n, edges, no_dual)
        if feasible != (len(es) == 0):
            bad += 1
            continue
        # min proxies by brute force over proxy sets inside S
        best = None
        for r in range(len(no_dual) + 1):
            for prox in itertools.combinations(sorted(no_dual), r):
                if zero_outage_feasible(n, edges, no_dual - set(prox)):
                    best = r
                    break
            if best is not None:
                break
        if best != min_vertex_cover_size(sorted(no_dual), es):
            bad += 1
    return bad


# ---------------------------------------------------------------- L5
def han_incomparable_classes():
    """Reproduces the *logic* of Han (arXiv 2609.07849): with incomparable
    client capability classes, every single-peer probe misses one withdrawal,
    while a check over the observed class set catches both."""
    server = frozenset({P, S, C})
    pref = (P, S, C)
    classes = {
        "mlkem_only_pq": frozenset({P, C}),
        "sntrup_only_pq": frozenset({S, C}),
        "classical": frozenset({C}),
    }
    regressions = {"drop_mlkem": server - {P}, "drop_sntrup": server - {S}}

    def pq_lost(cls, new):
        return neg(cls, server, pref) in PQ and neg(cls, new, pref) not in PQ

    single_peer = {
        name: [r for r, new in regressions.items() if pq_lost(cls, new)]
        for name, cls in classes.items()
    }
    population = sorted(
        r for r, new in regressions.items() if any(pq_lost(c, new) for c in classes.values())
    )
    return single_peer, population


# ---------------------------------------------------------------- L6
def gt_upper_bound(counts: Counter, delta: float) -> float:
    """Hypothesised high-probability upper bound on the missing mass:
    n1/N + sqrt(2 ln(2/d)/N) [McDiarmid on n1/N] + sqrt(ln(2/d)/N)
    [upper-tail concentration of missing mass; constant to be verified
    against McAllester & Ortiz 2003 / Berend & Kontorovich 2013]."""
    n = sum(counts.values())
    n1 = sum(1 for c in counts.values() if c == 1)
    return n1 / n + math.sqrt(2 * math.log(2 / delta) / n) + math.sqrt(math.log(2 / delta) / n)


def missing_mass_calibration(runs=200, delta=0.05):
    """L6: coverage of the narrowing certificate.  i.i.d. Zipf peers -> bound
    should hold w.p. >= 1-delta.  Periodic peers whose period exceeds the
    observation window -> bound is expected to FAIL (the falsification
    boundary R* = T / period predicted in the proposal)."""
    rng = random.Random(SEED + 3)
    k = 60
    w = [1 / (i + 1) ** 1.1 for i in range(k)]
    z = sum(w)
    p = [x / z for x in w]
    results = {}
    for regime in ("iid", "periodic_T_lt_period", "periodic_T_ge_period"):
        covered = covered_bare = 0
        for _ in range(runs):
            n = 20000
            sample = rng.choices(range(k), weights=p, k=n)
            if regime == "iid":
                true_missing = sum(p[c] for c in range(k) if c not in set(sample))
            else:
                # a batch-job class with 8% of monthly traffic appears only once
                # per period; window covers it iff T >= period.
                periodic_mass = 0.08
                in_window = regime == "periodic_T_ge_period"
                if in_window:
                    sample += [k] * int(periodic_mass * n)
                seen = set(sample)
                true_missing = (1 - periodic_mass) * sum(
                    p[c] for c in range(k) if c not in seen
                ) + (0 if in_window else periodic_mass)
            cnt = Counter(sample)
            covered += true_missing <= gt_upper_bound(cnt, delta)
            covered_bare += true_missing <= sum(1 for c in cnt.values() if c == 1) / sum(cnt.values())
        results[regime] = {"bound": covered / runs, "bare_GT": covered_bare / runs}
    return results


if __name__ == "__main__":
    m, wv = check_product_condition()
    print(f"L2 product-condition vs explicit interleavings: mismatches={m}")
    print(f"L1 widening-only waves that broke availability: {wv}")
    sv, ce, bb = pq_dominant_widening_preserves_Q()
    print(f"L3 widening ranked below ALL PQ algs flipping PQ->classical: {sv}; "
          f"not-below-all counterexamples: {ce} (of which ranked below best PQ only: {bb})")
    print(f"L4 vertex-cover proxy lemma violations: {check_vertex_cover_lemma()}")
    sp, pop = han_incomparable_classes()
    print(f"L5 single-peer probe catches: {sp}")
    print(f"L5 population (observed-class-set) check catches: {pop}")
    print(f"L6 narrowing-certificate coverage (target >= 0.95): {missing_mass_calibration()}")
