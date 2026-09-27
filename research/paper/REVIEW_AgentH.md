# Agent H: independent adversarial review of PROPOSAL.md (draft of 2026-09-27)

**How this review was produced.** Agent H read `PROPOSAL.md`, `verify_lemmas.py` and `verify_lemmas.out` without access to the lab's internal reasoning. It ran about 22 web searches, and its citations are labelled [verified-snippet] or [unverified]. What follows is Agent H's report, lightly condensed.

**Scores:**

| Criterion | Score |
|---|---|
| Originality | 3 |
| Technical quality | 3 |
| Significance | 4 |
| Evidence (as proposed) | 2 |
| Clarity | 6 |
| Reproducibility | 6 |

**Recommendation:** strong reject at NeurIPS/ICML/ICLR; reject at USENIX Security/CCS in current form. **Confidence:** 4/5.

## Summary (as the reviewer wrote it)

The paper builds on Han (arXiv 2609.07849), which shows that no single probe peer can soundly gate PQ delivery. It proposes a shield for LLM agents that change TLS/SSH/IKEv2 crypto configuration. The shield:
- (i) shadow-replays every client capability class seen in handshake telemetry against the candidate config (Δ1);
- (ii) allows removals only when a Good–Turing missing-mass bound is at most α and the observation window covers the longest business cycle (Δ2);
- (iii) waves through "PQ-dominant widenings" without checking them (Δ3).

The theory is five small propositions checked on toy instances. The evaluation is an unrun, author-built testbed with 72 author-written tickets.

## Strengths

- The problem is real and the relational framing is correct.
- Harm and coverage are reported together, so blocking everything cannot look safe.
- The epistemic labelling is honest.
- The falsification conditions are pre-registered.
- The list of threat baselines (B5–B8) is thoughtful.
- The P4 bound is correct in direction and its constants look sound.

## Weaknesses (most severe first)

**W1. The method collapses to a one-line operational rule.**
- For removal-only actions under first-match negotiation, neg(k,C′) = neg(k,C) whenever neg(k,C) was not removed. So Δ1 on narrowings is equivalent to "never remove an algorithm some observed client negotiated."
- With realistic handshake volumes, ε_N ≈ 0, so Δ2 reduces to "window ≥ τ_max."
- AWS removed TLS 1.0/1.1 from its FIPS endpoints "after a 30-day period during which no connections are detected" [verified-snippet].
- Δ1 is strictly *more permissive* only in corner cases. That is a coverage gain, not a safety gain.
- **Fix:** make that rule plus PQ-first ordering the primary baseline B\*, and show a material gap on real data.

**W2. P2 and Δ3 are unsound under real semantics.**
- In SSH the *client's* order decides, so adding a classical key exchange flips clients that list classical first.
- In TLS 1.3, key_share and HRR policy are part of negotiation. A client that sends only an X25519 share gets X25519 unless the server issues an HRR (Akamai [verified-snippet]).
- **Fix:** model negotiation per implementation, or send widenings through Δ1 as well.

**W3. The lemma evidence is largely vacuous.**
- In the L6 i.i.d. case the true missing mass is 0 in every run.
- The L6 periodic case is tautological.
- L5 catches both regressions by construction, and L1 holds trivially because unions are monotone.
- **Fix:** use thousands of classes, heavy tails, N comparable to the class count, and handshakes clustered by client.

**W4. Δ2 bounds the wrong quantity.**
- It bounds per-handshake, traffic-weighted mass, but operators lose on *entities* (the quarterly payroll client, the HSM, the regulator feed).
- Over a horizon, P(at least one failure) → 1 unless M₀ = 0.
- Handshakes are clustered by client, so the effective sample size is the number of distinct clients.
- Getting τ_max "from the CMDB" presupposes the peer knowledge the method is meant to supply.
- **Fix:** estimate entity-level missing mass, with a horizon-level guarantee.

**W5. The "agentic" part is not essential, and the venue is wrong.**
- Δ1–Δ3 form a deployment gate that works equally for humans or scripts.
- The only agent-specific science is H3 (counterexample feedback redirects plans) and H4 (verifier scope matters more than model scale).
- **Fix:** either move to a systems-security or measurement venue, or make H3/H4 the headline.

**W6. The evaluation has built-in leakage.**
- The telemetry and the harm metric come from the same generator, so SPRR on observed classes is 0 by construction.
- The trap tickets were written by the authors.
- **Fix:** use real traces and real tickets (for example Han's corpus of 711,923 agent-authored file changes [verified-snippet]). Parameterise the generator from measurements.

**W7. Baselines are strawmen.**
- A canary with a negotiated-PQ-share KPI (nginx `$ssl_curve`) catches silent withdrawal.
- testssl.sh `-c` already replays stored ClientHello profiles.
- **Fix:** add B\*, B5+ (a probe set derived from telemetry) and B8+ (a canary with a PQ-share KPI).

**W8. Shadow-replay fidelity is assumed, not shown.** Several features break the capability-class abstraction:
- HRR (the second ClientHello is interactive);
- client retry without PQ;
- PSK resumption, which delays outages and hides the group;
- 0-RTT;
- ECH (the outer ClientHello only);
- GREASE, which inflates n₁;
- SSH host-key ordering and strict-KEX pseudo-algorithms;
- failures outside the offered algorithm set (certificates, versions, MTU).

**Fix:** define a class as the full negotiation-relevant state, replay it with emulated client state machines, and report fidelity per feature.

**W9. The theory is textbook.**
- P1, P3, P4 and P5 are standard.
- P5's bipartite assumption fails for PLC-to-PLC links, and GOOSE/SV multicast makes the problem hypergraph vertex cover (NP-hard).

**W10. Nothing has been run, and Han26 has not been read in full.**

## Answers to the 18 questions (condensed)

1. **Already known?** The pieces are. Telemetry-gated deprecation (AWS, Azure, Mozilla, Chrome), handshake simulation (testssl.sh, SSL Labs) and Good–Turing residual risk (Böhme's STADS and FSE'21 work; arXiv 2604.05057; arXiv 2607.17061) all exist. Only the application to PQ is new.
2. **Simply A+B?** Yes.
3. **Why aren't the baselines sufficient?** Enlarged versions of B5, B6 and B8 are close to Δ.
4. **Why does each component exist?** Δ1 is justified only for reorderings and mixed changes. Δ2 matters only at small N. Δ3 is unsound.
5. **Statistics?** The effective n is 36–72 tasks, not 12k episodes, and (1|model) with 3 levels is weak. P4's constants are fine.
6. **Trivial testbed or tasks?** The containers are realistic, but the population and tickets are synthetic.
7. **Leakage?** Yes (W6).
8. **Fair comparison?** B5 and B8 are handicapped, and B\* is missing.
9. **Parameters?** Class granularity is unanalysed, and τ_max = 35 days is arbitrary.
10. **Compute?** Fine.
11. **Poorly tuned baselines?** Yes.
12. **Fails outside one dataset?** Unknown, since there is one synthetic generator.
13. **Seed robustness?** Generator hyperparameters matter more than LLM seeds.
14. **Claims broader than evidence?** Yes.
15. **Could a simpler baseline match?** Likely, on safety.
16. **Preprocessing?** Class derivation is unspecified.
17. **Merely engineering?** Mostly.
18. **Does the mechanism support the explanation?** Only by construction.

## The three changes that would most raise the score

1. Real populations and real tickets, compared against B\*, B5+ and B8+, showing a material gap and showing that unseen and periodic peers exist.
2. Correct the semantics: per-implementation negotiation, no unchecked widening, an entity- and horizon-level P4 under dependence, and per-feature replay fidelity.
3. Reframe: either a systems or measurement paper, or an ML paper whose headline is H3/H4 with task-level statistics.

## Prior art surfaced by Agent H (all [verified-snippet] unless noted)

- AWS FIPS TLS deprecation (30 days with no connections): https://aws.amazon.com/security/security-bulletins/AWS-2020-001
- AWS CloudTrail `tlsDetails`: https://aws.amazon.com/blogs/security/tls-1-2-required-for-aws-endpoints/
- Azure Storage minimum-TLS guidance: https://learn.microsoft.com/en-us/azure/storage/common/transport-layer-security-configure-minimum-version
- Mozilla TLS 1.0/1.1 removal telemetry: https://blog.mozilla.org/security/2018/10/15/removing-old-versions-of-tls/
- testssl.sh client simulation: https://testssl.sh/doc/testssl.1.html
- Cloudflare PQ to origins and Automatic Key Exchange: https://blog.cloudflare.com/post-quantum-to-origins/ and https://www.infoq.com/news/2026/09/cloudflare-automatic-key-exchang/
- Akamai on key_share and HRR: https://www.akamai.com/blog/security/post-quantum-cryptography-implementation-considerations-tls
- IBM Quantum Safe Remediator: https://www.ibm.com/docs/en/quantum-safe/quantum-safe-remediator/1.1.x?topic=overview
- SandboxAQ AQtive Guard network analyzer: https://aqtiveguard.sandboxaq.com/docs/sensors/network-analyzer/ (population-gated removal [unverified])
- Böhme, residual risk in greybox fuzzing (FSE'21): https://mboehme.github.io/paper/FSE21.pdf
- Blind-Spot Mass: https://arxiv.org/abs/2604.05057
- Singleton-fraction defect bound: https://arxiv.org/abs/2607.17061
- ssh-audit: https://github.com/jtesta/ssh-audit
- nginx PQC and `$ssl_curve`: https://blog.nginx.org/blog/pqc-nginx
