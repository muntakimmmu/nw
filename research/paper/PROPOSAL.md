# Widen Freely, Narrow with Evidence: Population-Relational Shielding for Agentic Post-Quantum Migration of Infrastructure

**Research proposal from the multi-agent lab: Agentic PQC in Action for Infrastructure Security**
Date: 2026-09-27 · Status: **PROPOSAL, NOT YET VERIFIED**. No experiment on the proposed method has been run. The only computations run so far are the lemma sanity checks in `research/analysis/verify_lemmas.py`.

> **Epistemic labels.** In this document these labels are used:
> - **KNOWN**: established in the cited literature or standards.
> - **OBSERVED**: reproduced by us, which so far means only the lemma checks.
> - **HYPOTHESIZED**: a prediction still to be tested.
> - **PROPOSED**: our design.
> - **NOT YET VERIFIED**: needs checking before submission.
>
> **Citation labels:**
> - **[V]**: title, ID and authors confirmed via search-engine index pages in this session. The full text was *not* read, because the lab's egress proxy blocked arxiv.org/eprint full text for the scouting agents.
> - **[P]**: partially confirmed (title and ID only).
> - **[U]**: unverified, from memory.
>
> Anything numeric that comes from a [V]/[P] source is abstract-level and must be re-checked against the full text (Tier-1 gate, §9 of the lab protocol).

---

## 1. Topic Interpretation

**User topic:** "Agentic PQC in Action for Infrastructure Security".

**Interpretation (ASSUMPTION).** The topic has two readings.
- **Primary reading:** autonomous, tool-using LLM agents that plan, execute and verify the migration of *deployed* infrastructure to post-quantum cryptography (PQC) and keep it crypto-agile afterwards. "Infrastructure" here means TLS/SSH/IKEv2 endpoints, PKI, gateways, enterprise IT and OT/ICS segments.
- **Secondary reading:** PQC *for* agentic infrastructure (PQ-secured MCP/A2A, agent identity).

The first wave of the lab found that the secondary reading is saturated (Agent B, C6: FATAL collision; see §10), so the proposal targets the primary reading.

**Why this matters (KNOWN):**
- Deadlines:
  - NIST IR 8547 (ipd) deprecates quantum-vulnerable public-key algorithms after 2030 and disallows them after 2035 [V].
  - U.S. EO 14412 (Jun 2026) sets 2030/2031 federal deadlines for PQ key establishment and signatures [V (snippet)].
  - The UK NCSC's milestones run to 2028, 2031 and 2035 [P].
- Deployment is uneven:
  - Hybrid PQ key exchange is the default on about 47% of measured domains, but about 70% of that comes from two CDNs. The long tail of self-managed infrastructure lags (Wickramasinghe et al., "Mind the Gap", arXiv 2607.29005 [V]).
  - Organisations are therefore turning to automation, including LLM agents, to reach the tail.

**The research question we isolate:**

> When an LLM agent changes cryptographic configuration on live infrastructure, what must its verifier quantify over for the agent's loop to be *sound*? That is: no silent PQ withdrawal and no outage for real peers, while still making migration progress.

This is narrower than "build an agent for PQC migration". The lab concluded that the broader question has no defensible novelty left (§4, §10).

---

## 2. Frontier Literature Map

The table below groups 30 items by their methodological relationship to the proposal. The first column is the reference key used in §10 and §14. Agent A contributed 35 entries, Agent B 60+ and Agent C/F about 40; this is the curated subset.

### 2.1 Agentic or LLM work on PQC (direct competitors)

| Key | Paper | Venue / ID | Label | One-line relevance |
|---|---|---|---|---|
| **Han26** | Y. Han, *Nothing Breaks: No Single Peer Can Soundly Gate Post-Quantum Delivery* | arXiv 2609.07849 (7 Sep 2026) | [V] | **P\*** (§4). PQ protection is a server × client-population relation. Shipped SSH clients form ≥2 incomparable minimal PQ classes, so no single-peer gate is sound. File checks, vendor dumps, CBOM scores and auditor exit codes all miss PQ-KEX removal. LLM agents are induced into downgrades by ordinary engineering prose. |
| **CodAg** | *Can Coding Agents Migrate to Post-Quantum Cryptography?* | arXiv ID conflicts with 2512.12989 | [P] | Go RSA→ML-DSA-44 signer, 160 agent attempts. 12 patches pass local checks but fail the external requirements. Checker feedback did not raise completion. |
| Quant25 | A. Alquwayfili, *Quantigence: multi-agent AI framework for quantum security research* | arXiv 2512.12989 | [V] | Supervisor + 4 role agents + MCP. QARS extends the Mosca inequality. Analysis only, no actuation. |
| Pall26 | J. Pallarés de Bonrostro, A. I. González-Tablas, M. I. González Vasco, *Empirical evaluation of LLMs for migration of code fragments to PQC* | arXiv 2606.07341 | [V] | ~800 fragment pairs. Fine-tuned GPT-4.1-mini reaches 92.5% dynamic functional correctness. |
| Shaw26 | A. Shaw, *Quantum-Safe Code Auditing* | arXiv 2604.00560 | [V] | Regex + LLM enrichment + risk score. Code on GitHub. |
| Hirs26 | E. Hirsch, K. Raab, T. J. Bauer, D. Loebenberger, *Detecting cryptographically relevant packages with collaborative LLMs* | arXiv 2603.07204 | [V] | Majority vote of LLMs for package-level discovery. |
| Erle26 | R. Erlemann et al., *Full-stack KG + LLM for PQ cyber readiness* | arXiv 2601.03504 | [P] | Knowledge-graph readiness scoring with Shapley attribution. |
| Jing26 | N. K. Jingar, *PG-PQMES: policy-governed PQ migration with ephemeral sidecars* | arXiv 2609.14286 | [V] | Policy governance + automatic rollback. Simulated. Not an LLM system. |
| Bala26 | H. Balaji et al., *Operationalising PQ-TLS: automated configuration profiling and hybrid deployment in financial infrastructure* | arXiv 2605.17955 / ePrint 2026/959 | [V] | 8,443 Nginx configs plus a bank proof of concept. The strongest **non-agentic** pipeline baseline. |
| MAGIQ | S. Avizheh, T. Mallick, A. Oprea, C. Nita-Rotaru, R. Safavi-Naini, *MAGIQ* | arXiv 2605.06933 | [V] | UC-secure PQ governance for multi-agent systems (secondary reading). |
| Camp26 | R. Campbell, *PQC migration for agentic AI systems* | MDPI Computers 15(7):434 | [V] | Seven migration surfaces for agent systems (secondary reading). |

### 2.2 Standards, deployment and measurement

| Key | Item | Label |
|---|---|---|
| FIPS203/204/205 | ML-KEM, ML-DSA, SLH-DSA (NIST, Aug 2024) | [V] for 203; [U] for 204/205 |
| IR8547 | NIST IR 8547 ipd, transition timeline | [V] |
| TLSHyb | draft-ietf-tls-ecdhe-mlkem: X25519MLKEM768 (0x11EC), 1,216-byte client share | [V] |
| XWing | Barbosa et al., X-Wing hybrid KEM, IACR CiC 2024 | [V] |
| Wick26 | *Mind the Gap*: 31%→47% hybrid-default; 88.8% of domains offer only X25519MLKEM768 | [V] |
| Roy26 | H. Roy, *Post-Quantum TLS Migration: A Systematization…*, ePrint 2026/1703 | [V] (this session) |
| tldr.fail | Split-ClientHello middlebox bugs; the HRR path works (AWS case, Sep 2026) | [V] (page fetched by Agent C) |
| Delg26 | Delgado, *Observability for PQ-TLS readiness: multi-surface evidence*, arXiv 2605.02978 | [V] |

### 2.3 Crypto-agility, inventory and prioritisation

| Key | Item | Label |
|---|---|---|
| CSWP39 | NIST CSWP 39, crypto agility (final Dec 2025) | [V] |
| Nath24 | Näther et al., *SoK/Systematic review of crypto-agility*, arXiv 2411.08781 | [V] |
| Mosc18 | Mosca, IEEE S&P Mag. 16(5), 2018 | [V] |
| Hasa24 | Hasan et al., *Framework for migrating to PQC: security dependency analysis*, IEEE Access 12, 2024 | [V] |

### 2.4 LLM agents for network/infra change, and safety shields

| Key | Item | Label |
|---|---|---|
| VPP23 | Mondal et al., *What do LLMs need to synthesize correct router configurations?* (HotNets'23), arXiv 2307.04945 | [V] |
| Clar25 | Mondal, Bjørner, Millstein, Tang, Varghese, *Clarify*, arXiv 2507.12443 | [V] |
| NCE24 | Wang et al., *NetConfEval*, CoNEXT 2024 | [V] |
| Asad26 | Asadli, Hoffman, Protogeros, Vanbever, *Evaluating agentic configuration repair*, arXiv 2606.06212 | [V] |
| Bila26 | Bilal, Crowcroft et al., *LLMs for agentic NetOps/AIOps: architectures, evaluation, safety*, arXiv 2605.12729 | [V] |
| NetArena | ICLR'26, arXiv 2506.03231: 13–38% success on realistic tasks | [P] |
| AgSpec | Wang, Poskitt, Sun, *AgentSpec*, ICSE 2026, arXiv 2503.18666 | [V] |
| ShAg | Chen, Kang, Li, *ShieldAgent*, ICML 2025, arXiv 2503.22738 | [V] |
| Shield18 | Alshiekh et al., *Safe RL via shielding*, AAAI 2018 | [V] |
| Mantis | arXiv 2410.20911: injected service responses steer LLM attack agents >95% of the time | [P] |

### 2.5 Cross-domain ancestors (Agent F)

| Key | Item | Label |
|---|---|---|
| Reit12 | Reitblatt et al., *Abstractions for network update*, SIGCOMM 2012 | [V] |
| McCl15 | McClurg, Hojjat, Černý, Foster, *Efficient synthesis of network updates*, PLDI 2015 | [V] |
| Bhar16 | Bhargavan et al., *Downgrade resilience in key-exchange protocols*, IEEE S&P 2016 | [V] |
| MS00 | McAllester & Schapire, *On the convergence rate of Good–Turing estimators*, COLT 2000 | [V] (this session) |
| MO03 | McAllester & Ortiz, *Concentration inequalities for the missing mass…*, NeurIPS 2002 / JMLR 2003 | [V] (this session) |
| JWI24 | *Just Wing It: near-optimal estimation of missing mass in a Markovian sequence*, arXiv 2404.05819 | [V] (this session) |
| MOh19 | Mossel & Ohannessian, *On the impossibility of learning the missing mass*, Entropy 2019 | [P] (this session: PubMed index) |
| CRC24 | Angelopoulos et al., *Conformal risk control*, ICLR 2024 | [V] |
| Tang15 | Tang et al., *Holistic configuration management at Facebook*, SOSP 2015 | [V] |

---

## 3. Mathematical Ancestors

**(A1) Mosca's inequality** [Mosc18]. Act now if $X + Y > Z$. Here $X$ is how long the data must stay secret, $Y$ is how long the migration takes, and $Z$ is the time until a cryptographically relevant quantum computer (CRQC) exists. The risk-scoring generalisation (QARS [Quant25]) is $\sum_k w_k f_k(\cdot)$.

**(A2) Hybrid KEM combiners.**
- TLS: $\mathrm{HKDF\text{-}Extract}(ss_{\mathrm{MLKEM}}\,\|\,ss_{\mathrm{X25519}})$ [TLSHyb].
- X-Wing: $\mathrm{SHA3\text{-}256}(\ell\,\|\,ss_M\,\|\,ss_X\,\|\,ct_X\,\|\,pk_X)$, which is IND-CCA if either component is secure [XWing].

**(A3) Negotiation as a function of a relation** (implicit in every handshake protocol; formalised for PQ gating by [Han26]). For an initiator with offered set and order $(A_u,\pi_u)$ and a responder $(A_v,\pi_v)$,
$$\mathrm{neg}(u,v) = \text{first element of } A_u\cap A_v \text{ under the protocol's precedence rule}, \quad\text{or } \bot.$$
- In TLS 1.3 the server selects the group, subject to key_share/HRR.
- In SSH the *client's* order decides.
- In IKEv2 the responder picks from the proposals.

Han's theorem, informally: if the population's PQ capability classes contain two incomparable minimal elements, then every fixed single-peer check $\chi_{c^*}$ misses some PQ withdrawal.

**(A4) Verifier-in-the-loop agents** [VPP23, Clar25, Asad26, Bila26]:
$$C_{k+1} = \mathrm{LLM}(C_k,\ V(C_k),\ \mathrm{ctx}), \quad \text{stop when } V(C_k)=\varnothing.$$
[CodAg] gives the counterexample $V_{\text{local}}=\varnothing \not\Rightarrow V_{\text{external}}=\varnothing$.

**(A5) Shielding** [Shield18]. $a^{\mathrm{exec}}_t = a_t$ if $a_t\in\mathrm{Safe}_\varphi(s_t)$, otherwise the shield substitutes a safe action. AgentSpec [AgSpec] and ShieldAgent [ShAg] are LLM-era rule and circuit versions.

**(A6) Consistent network updates** [Reit12, McCl15]. Every intermediate state of an asynchronous update must satisfy the invariant. The two-phase (version-stamping) construction gives per-packet consistency.

**(A7) Downgrade resilience** [Bhar16]. Against an active attacker, a negotiated mode is only as strong as the weakest mode both peers support, unless the transcript authenticator is unbroken.

**(A8) Missing mass / Good–Turing** [MS00, MO03]. With $N$ samples and $n_1$ singletons, $\hat M_0 = n_1/N$ estimates the probability mass of unseen categories. High-probability upper bounds of the form $\hat M_0 + O(\sqrt{\log(1/\delta)/N})$ exist under i.i.d. sampling. Markov-chain extensions exist [JWI24]. Without assumptions, uniform learning of the missing mass is impossible [MOh19].

---

## 4. Closest Prior Work

**P\* = [Han26], *Nothing Breaks* (arXiv 2609.07849).** Agents B and F chose it independently, Agent A ranked it second, and Agent C flagged it (M12).

| Aspect | Han26 | This proposal |
|---|---|---|
| Object | Gate surfaces for PQ delivery (file checks, vendor dumps, CBOM scores, auditor exit codes, a delivery-anchored probe) | The verifier inside an LLM agent's action loop |
| Main result | **Negative.** Only a delivery-anchored check catches all six regressions. Its verdict depends on "which peer profile it probes with — **an input nothing supplies**", and no single choice is sound. | **Constructive.** Supply that input from the responder's own handshake telemetry: quantify over the *observed* capability-class population and bound the *unobserved* remainder statistically. |
| Scope | SSH and TLS; 7 configurations; LLM agents shown to *cause* downgrades | TLS, SSH and IKEv2. Covers both failure directions: PQ withdrawal *and* classical-removal outages. Includes OT gateways. Evaluates agents end-to-end. |
| Guarantee | Impossibility for single peers | Soundness on observed classes, plus a residual-risk certificate for unseen classes with an explicit failure boundary |

**The single-sentence difference from P\*:** Han proves that a delivery-anchored check needs a peer-population input and that no fixed peer provides it. We supply that input from telemetry, turn the check into an agent shield, bound the error on the part telemetry cannot see, and measure what this does to agent outcomes.

**Collision risk: MEDIUM-HIGH, time-sensitive.** The constructive step is natural, so Han or others may publish it soon. **Mandatory before any further investment:** read Han26 in full to confirm it contains no constructive population verifier. Agent B confirmed this only at abstract level.

**Second-closest work:**
- **[CodAg]:** the agent + checker PQC benchmark with a local-vs-external verification gap.
- **[Bila26]:** a generic verification wall → staged rollout → rollback architecture.
- **[Bala26]:** a non-agentic inventory → deploy pipeline.

---

## 5. Assumption–Regime Matrix (reconciled from Agents C and A)

| Method | Assumption | Valid regime | Broken or untested regime | Importance |
|---|---|---|---|---|
| LLM PQC code migration [Pall26, CodAg] | Functional tests are an adequate oracle | Synthetic fragments; a single Go signer | Interop with a peer population; constant-time; key formats. 12/160 patches were locally correct but externally wrong. | High |
| CBOM / discovery [Hirs26, Shaw26] | Crypto is visible in code, packages or configs | Source repos | Stripped binaries; runtime-introduced crypto (Kestrel: 12 uncatalogued ML-KEM programs among 6,224 binaries [P]); asset-discovery F1 ≈ 0.75 [P] | Very high |
| **Gates and verifiers** (file lint, vendor dump, CBOM score, single probe) | **PQ status is a property of one artifact or one peer** | Homogeneous clients | **Heterogeneous, incomparable client classes**, where every gate misses PQ withdrawal [Han26] | **Very high** |
| Verifier-in-loop config agents [VPP23, Asad26] | The verifier covers the property that matters | Routing and ACLs (Batfish) | TLS/SSH/IKE negotiation outcomes are not modelled | High |
| Agentic NetOps [NetArena, Bila26] | Short horizon; trusted feedback; reversible actions | Emulated tasks | 3–38% success; 38.7% "meltdown" [P]; adversarial feedback [Mantis] | Very high |
| Hybrid PQ TLS itself | The ClientHello fits in one segment; middleboxes follow the protocol | Browser ↔ CDN | Split ClientHello dropped by Fortinet, Sophos and AWS firewalls; 0.34% of origins fail [P]. The "retry without PQ" fallback is an attacker-triggerable downgrade. | Very high |
| OT PQ framing | Per-frame PQ signatures are the goal | Paper studies | IEC 62351-6 already uses HMAC/GMAC for GOOSE. The PQ exposure is GDOI key distribution, engineering access and firmware signing [P]. | High |
| Migration planners [Quant25, Hasa24] | Assets are independent; parameters are estimable | Spreadsheets | Relational dependencies; no ground truth to validate against | Medium |

---

## 6. Candidate Unsolved Problems (R_gap = I·U·V·D; Agent C scores, adjusted after reconciliation)

| # | Setting | I | U | V | D | R_gap | Note |
|---|---|---|---|---|---|---|---|
| **U1** | **Sound verification of agent-made crypto-config changes over heterogeneous peer populations**. This merges Agent C's S1+S8 with the Han26 gap. | 0.90 | 0.75 | 0.90 | 0.80 | **0.49** | Selected |
| U2 | Path-aware PQ rollout under middlebox ossification, where fallback acts as a downgrade | 0.85 | 0.70 | 0.90 | 0.70 | 0.37 | Kept as extension Δ4 |
| U3 | Security-preserving oracle for LLM crypto code (constant-time, key formats, pinned versions) | 0.80 | 0.75 | 0.90 | 0.70 | 0.38 | Close to CodAg; deferred |
| U4 | OT migration under hard deadlines and devices that cannot dual-stack | 0.90 | 0.80 | 0.60 | 0.75 | 0.32 | Enters as corollary P5 plus the OT arm of the testbed |
| U5 | Prompt injection into the migration agent via banners, certificate fields or CBOM files | 0.80 | 0.70 | 0.95 | 0.60 | 0.32 | Robustness experiment E7 |
| U6 | Reversibility-aware planning over trust-anchor graphs | 0.90 | 0.75 | 0.70 | 0.65 | 0.31 | Future work |
| U7 | Decision quality versus inventory recall | 0.85 | 0.70 | 0.85 | 0.60 | 0.30 | Becomes the dose-response mechanism test E3 |
| U8 | HNDL-exposure-optimal migration ordering (scheduling theory) | 0.75 | 0.80 | 0.60 | 0.70 | 0.25 | A separate theory paper (Agent F Transfer B) |

---

## 7. Selected Failure Regime

**Regime R:** an LLM agent reconfigures responders or initiators (TLS servers, sshd, IKEv2 gateways, OT protocol gateways). The live peer population has heterogeneous, partly *incomparable* capability classes, including rare and periodic peers.

**Why it matters:**
1. This is where the long tail of PQ migration lives [Wick26].
2. Every existing verifier used in agent loops quantifies over a single artifact or a single peer. [Han26] proves this is unsound for PQ delivery.
3. The same regime produces *both* failure directions:
   - **silent PQ withdrawal**: removing or reordering a PQ family some class relied on;
   - **availability outages**: removing classical algorithms too early, which breaks peers nobody knew about.
4. Organisations are deploying agents into exactly this regime now ([Bila26] architecture; vendor tooling).

---

## 8. Failure Mechanism

We separate *observed failure*, *measurable cause* and *testable hypothesis*.

**F1: quantifier mismatch (logical).**
- **Observed (KNOWN, [Han26]):** gates miss PQ withdrawal, and agents induce withdrawals in 40/40 prompted episodes [V-snippet].
- **Cause:** the verifier evaluates $\chi(C_v)$ or $\chi(c^*, C_v)$ for one probe $c^*$. The property is $\forall k\in\mathcal K_v:\ \mathrm{neg}(k, C_v')\in PQ$ whenever $\mathrm{neg}(k,C_v)\in PQ$. With incomparable minimal classes, no $c^*$ decides it (reproduced as lemma L5 in `verify_lemmas.py`).
- **Measurable variable:** **relational recall** $\rho$ = the fraction of injected class-relational violations the verifier flags.
- **Hypothesis H1:** for baseline verifiers, $\rho$ is bounded by the fraction of violation-bearing classes their probe set covers. The resulting downstream silent-regression rate falls in proportion to $\rho$.

**F2: unobserved-tail risk (statistical).**
- **Observed (KNOWN):** classical-removal outages of long-tail peers are a documented operational failure. Examples: legacy-chain breakage when DST Root CA X3 expired (2021) [P]; ClientHello-size breakage [tldr.fail].
- **Cause:** narrowing $A_v$ is availability-safe only for peers that are actually compatible, and the inventory of peers is incomplete. The relevant quantity is the probability mass $M_0$ of peer classes never seen in the window.
- **Measurable variable:** the realised post-change handshake failure rate compared with the certified bound $U_v$.
- **Hypothesis H2:** $\Pr[\text{failure mass} > U_v] \le \delta$ when the window $T$ covers the longest business period $\tau_{\max}$. The guarantee collapses when $T<\tau_{\max}$ (predicted boundary; lemma L6 reproduces it in simulation).

**F3: the agent's "restore availability" drive (behavioural).**
- **Observed (KNOWN):** [Han26] reports agents downgrading from engineering prose. Agent C found that split-ClientHello timeouts invite a "retry/disable PQ" fix, and that this fix is attacker-triggerable.
- **Cause:** the agent's objective contains availability terms, and its verifier gives no PQ-preservation feedback.
- **Hypothesis H3:** on the "handshake-timeout" task family, baseline agents choose PQ-removing fixes in a substantial fraction of episodes, pre-registered at ≥20%. With relational counterexample feedback they switch to PQ-preserving fixes (HRR / key-share ordering, MSS) at a significantly higher rate.

**Mechanism chain to verify:** Δ → ↑ relational recall ρ and calibrated U → ↓ silent PQ regressions and ↓ outages, **with no loss of migration progress**.

---

## 9. Candidate Functional Modifications (Δ)

The baseline model is $M$: a verifier-in-the-loop LLM agent (A4) whose verifier $V$ is an artifact-scoped or single-peer check.

| Δ | Target failure | Mathematical change | New property | Collision | Complexity |
|---|---|---|---|---|---|
| **Δ1 Relational shield** | F1 | $V(C') = \chi(c^*, C')$ becomes $V_{\mathrm{rel}}(C') = \bigwedge_{k\in \hat{\mathcal K}_v} \big[\mathrm{Av}(k,C') \wedge (\mathrm{neg}(k,C)\in PQ \Rightarrow \mathrm{neg}(k,C')\in PQ)\big]$, with $\mathrm{neg}$ computed by **shadow replay**: a synthetic initiator emulating class $k$ performs a real handshake against a shadow responder running $C'$ | Sound on observed classes; returns a counterexample class | MEDIUM (components exist; not composed as an agent shield — §10) | Low |
| **Δ2 Residual-risk narrowing certificate** | F2 | Allow autonomous narrowing iff $U_v=\hat M_0 + \epsilon_N(\delta) \le \alpha_v$ and $T_v \ge \tau_{\max}$; otherwise escalate or keep the widened state | Bounded outage probability from unseen classes, with an explicit failure boundary | LOW-MEDIUM | Low |
| **Δ3 Widen/narrow action typing** | F1+F2, efficiency | Classify each action by set inclusion and precedence. PQ-dominant widenings (Prop. P2) are auto-safe; only narrowings and reorderings go through Δ1+Δ2. | Autonomy where it is provably safe; checking effort goes where it matters | LOW (the consistent-update analogue is new here) | Very low |
| Δ4 Discriminating path probes | U2/F3 | Probe set {PQ-first, forced-HRR, classical control, MSS-split control} over paths; Boolean group testing to localise intolerant middleboxes | Separates ossification from server faults; blocks the fallback downgrade | MEDIUM (tldr.fail practice; tomography) | Medium |
| Δ5 Conformal autonomy threshold | Agent error | CRC/LTT-calibrated $\lambda$ for "act vs ask" with a wave-shift penalty | Expected outage cost ≤ α (under exchangeability) | MEDIUM-HIGH (KnowNo, CRC for agents) | Medium |
| Δ6 HNDL-optimal ordering | Scheduling | $\min_\sigma \sum_e w_e \max(C_u,C_v)$, i.e. bipartite $1\|prec\|\sum w_jC_j$; Sidney via densest subgraph | A 2-approximate exposure-minimal order (HYPOTHESIZED; proof pending) | LOW, but a separate paper | Medium |
| Δ7 Security-preserving code oracle | U3 | dudect/ACVP/CVE-pin checks added to the code-migration oracle | Catches constant-time and format regressions | MEDIUM-HIGH ([CodAg], [Pall26]) | Medium |
| Δ8 Injection-hardened observation channel | U5 | Treat banners and certificate fields as typed data; no free-text instructions | Resistance to Mantis-style steering | HIGH (crowded) | Low |

**Selected: Δ1 + Δ2 + Δ3.** These are one conceptual change, not three components: *the verifier's quantifier moves from one artifact or peer to the observed peer population, plus a bound on the unobserved remainder.* Δ3 is the action-typing that follows from Proposition P1, and Δ2 is the part of the quantifier that cannot be discharged logically. **Δ4** is carried as a pre-registered extension experiment (E8). Δ5–Δ8 are rejected for this paper, for the reasons in §10.

---

## 10. Novelty Collision Report

| Candidate | Closest prior | Same component | Actual difference | Risk |
|---|---|---|---|---|
| Agent that migrates PQC code | Pall26, CodAg, ccPASTpqc, OSS agents | Everything | None worth a paper | **FATAL** |
| Multi-agent PQC planner with risk scores | Quant25, Erle26, Hasa24 | Roles, Mosca scores, dependency graphs | Only optimisation-plus-execution is left (Δ6) | HIGH |
| Agent reconfigures TLS/SSH with verify + rollback | Jing26, bridge-server ICISC'25, Bala26, Bila26 | Staged rollout, rollback, verification wall | The verifier's soundness: none quantifies over the peer population | HIGH as a system, MEDIUM for the shield |
| PQ for agent comms (MCP/A2A) | CA-MCPQ, MAGIQ, Camp26, QSC | Everything | Workshop-scale cost models | **FATAL** |
| **Δ1 relational shield** | Han26 (negative result); VPP23/Asad26 (verifier loops); AgSpec/ShAg (shields); pqc-flow, Delg26 (passive PQ telemetry) | Telemetry collection; shield architecture; delivery-anchored probing | The composition: *population-quantified*, replay-based PQ-and-availability invariant as the agent's shield with counterexample feedback. Han shows the need; no one we found supplies the population input. | **MEDIUM** (time-sensitive) |
| **Δ2 missing-mass certificate** | MS00/MO03 (estimators); cipher-deprecation telemetry practice (e.g., Clerk changelog 2026 [V], Mozilla bugzilla) | Telemetry-informed deprecation | A formal, calibrated bound on unseen peer-class mass as a gate on autonomous narrowing, with the periodicity boundary. No prior use found (searched: "safe deprecation cipher suite removal telemetry unseen clients Good-Turing"). | **LOW-MEDIUM** |
| **Δ3 widen/narrow typing** | Reit12 two-phase updates; the operational "dual-stack first" practice | Widen-then-narrow | Formal conditions: product condition (P1) and *PQ-dominant* widening (P2). The lemma checks showed that the "below best PQ" condition is **wrong** (23 counterexamples), so the precise condition is non-obvious. | LOW (but small on its own) |

**Red-team searches performed in this session** (beyond Agents A and B):
- `"Nothing Breaks" "No Single Peer…"`
- `Yunze Han 2609.07849 … covering set proposed check`
- `consistent update post-quantum migration … observed handshake telemetry safe removal`
- `safe deprecation cipher suite removal handshake telemetry unseen clients Good-Turing`
- `passive handshake telemetry client capability supported_groups population verify … agent shield`

None found the composed Δ. **This is "not found", not "does not exist".** Search budgets were exhausted, full texts were unread, and commercial tools (IBM Quantum Safe, SandboxAQ AQtive Guard, Keyfactor) are unverified and may implement telemetry-gated deprecation without publishing it.

---

## 11. Selected Contribution: Exact Formulation

### 11.1 Setting

**Estate and configurations.**
- The estate is a directed communication graph $G=(V,E)$. Edges go from initiator to responder, and the true $E$ is hidden.
- Node $v$ has a configuration $C_v$ that induces an *effective* offered set $A_v\subseteq\mathcal A$ and a precedence $\pi_v$.
- $\mathcal A_{PQ}\subset\mathcal A$ is the set of PQ or hybrid key-establishment algorithms.

**Observed peer population.**
- Over a window $T_v$, responder $v$ logs handshakes. Each handshake yields an initiator *capability class* $k=(A_k,\pi_k)$:
  - TLS: supported_groups, key_share, signature_algorithms;
  - SSH: KEXINIT name-lists;
  - IKEv2: SA proposals plus ADDKE (RFC 9370).
- The result is a multiset $\mathcal S_v$ with $N_v$ handshakes and $n_1$ classes seen exactly once. $\hat{\mathcal K}_v$ is the set of distinct observed classes.
- For initiator-side changes the roles are symmetric: the observed responder classes are used.

**Negotiation oracle.** $\mathrm{neg}(k, C)$ is computed by **shadow replay**: a synthetic initiator emits a handshake with class $k$'s exact offer (TLS via ClientHello replay, SSH via algorithm lists) to a sandboxed responder instance running configuration $C$ with the same software build. The oracle returns the negotiated algorithm or $\bot$. This anchors the check on delivery, per [Han26], rather than modelling library semantics.

### 11.2 The agent loop, baseline and modified

**Baseline $M$:** $C^{(i+1)} = \mathrm{LLM}(C^{(i)}, V(C^{(i)}), \mathrm{ctx})$, with $V\in\{V_{\text{file}}, V_{\text{dump}}, V_{\text{CBOM}}, V_{c^*}\}$.

**Modified $M+\Delta$.** An action $a$ proposes $C\to C'$ on a wave $W\subseteq V$ that is applied asynchronously. The shield $\Sigma$ runs these steps:

1. **Typing (Δ3).** For each $v\in W$, $a$ is a *widening* if $A'_v\supseteq A_v$ and every added algorithm ranks below **every** PQ algorithm in $\pi'_v$ (the PQ-dominance condition). Otherwise it is a *narrowing/reordering*.

2. **Relational invariant (Δ1).** For every $v\in W$ and every observed class $k\in\hat{\mathcal K}_v$, and for every pair of states $(s_u, s_v)\in\{C,C'\}^2$ over the edge's endpoints (the product condition), check:
$$\mathrm{Av}:\ \mathrm{neg}(k,s)\neq\bot,\qquad \mathrm{PQmon}:\ \mathrm{neg}(k,C)\in\mathcal A_{PQ}\Rightarrow \mathrm{neg}(k,s)\in\mathcal A_{PQ}.$$
Any violation returns the **counterexample** $(k,\ \mathrm{neg}(k,C),\ \mathrm{neg}(k,C'))$ to the agent as structured feedback.

3. **Residual-risk certificate (Δ2)**, for narrowings only:
$$U_v = \frac{n_1}{N_v} + \sqrt{\tfrac{2\ln(2/\delta)}{N_v}} + \sqrt{\tfrac{\ln(2/\delta)}{N_v}}\ \ \text{(constants NOT YET VERIFIED against MO03)},$$
accept autonomously iff $U_v\le\alpha_v$ and $T_v\ge\tau_{\max}$. Here $\tau_{\max}$ is the declared longest business cycle, taken from the CMDB or cron inventory, otherwise defaulting to 35 days. If the test fails, the agent must escalate, or keep the widened state and re-observe.

4. **Execution.** Accepted actions deploy through a graph-closed canary: both endpoints of sampled edges are included. Negotiated algorithms are then re-observed post hoc.

**Progress objective (so that "block everything" cannot look safe).** Traffic-weighted PQ coverage is $\mathrm{Cov}=\sum_e w_e\,\mathbb 1[\mathrm{neg}(e)\in\mathcal A_{PQ}]/\sum_e w_e$. Every evaluation reports the pair (harm, Cov).

### 11.3 Theory (Agent G)

These are honest, modest statements. Nothing below is claimed as deep.

- **P1 (asynchronous safety = product condition).** A wave preserves Av on every interleaving iff Av holds on $\{C_u,C'_u\}\times\{C_v,C'_v\}$ for every edge. As a corollary, widenings from an available state are safe under every interleaving. *OBSERVED:* exhaustively checked on 4,000 random instances, 0 mismatches (L1, L2). The proof is two lines: both orders of any two endpoint updates appear as permutation prefixes.

- **P2 (PQ-dominant widening preserves PQmon).** If every added algorithm ranks below all PQ algorithms in the responder's precedence, then no class negotiating PQ before negotiates non-PQ after. The condition is **tight in a useful sense**: "below the best PQ algorithm" is insufficient. Classes sharing only a lower-ranked PQ family are flipped (23 counterexamples, L3), which is the incomparable-class phenomenon of [Han26] again. *OBSERVED* (L3). Proof sketch: the negotiated element for class $k$ is the $\pi$-first element of $A_k\cap A'$. If $\mathrm{neg}$ was a PQ algorithm $p$ and every addition ranks after every PQ algorithm, then additions rank after $p$, so $p$ stays first.

- **P3 (soundness relative to observed classes).** If $\Sigma$ accepts, then for every $k\in\hat{\mathcal K}_v$, Av and PQmon hold in every interleaving state, *provided the shadow replay is faithful*. By construction. The content is the fidelity assumption, which E2 tests directly.

- **P4 (residual-risk certificate).** Suppose handshake classes in the window are i.i.d. from a stationary distribution $p$, and deployment traffic follows the same $p$. Then with probability $\ge 1-\delta$, the probability that the next handshake comes from a class outside $\hat{\mathcal K}_v$ is at most $U_v$. Therefore the post-narrowing failure probability is at most $U_v$, because only unseen classes can fail after Δ1 has passed.
  - *Status:* the bound's form follows MS00/MO03, but the **constants are NOT YET VERIFIED**. Stationary mixing Markov arrivals are handled via [JWI24] with a mixing-time penalty.
  - **Impossibility boundary:** without assumptions no such bound exists [MOh19]. A class with period $\tau>T$ has missing mass that is invisible to the estimator.
  - *OBSERVED (simulation L6):* coverage is 1.00 when i.i.d. and 1.00 when $T\ge\tau$, but **0.00 when $T<\tau$** (a class carrying 8% of traffic). This is the pre-registered falsification boundary. The i.i.d. setting is easy with N = 20,000 and 60 classes; realistic long-tail class distributions are E4's job.

- **P5 (OT corollary: proxy placement).** Let $S$ be the nodes that cannot hold a widened (dual-stack) state, such as constrained or fixed-firmware OT devices, which must jump $C\to P$.
  - A zero-outage migration exists iff $G[S]$ has no edges.
  - The minimum number of translating (bump-in-the-wire) proxies that restores feasibility equals the minimum vertex cover of $G[S]$. This is polynomial when $G[S]$ is bipartite (König), which holds for client/server OT.
  - *OBSERVED:* BFS over all schedules on 300 random instances (n ≤ 6), 0 violations (L4).
  - This links the agent's plan to the existing OT "bump-in-the-wire" practice with an exact placement rule.

We deliberately do **not** claim regret or convergence theorems. The agent is a black-box LLM, and such theorems would be decorative.

---

## 12. Novelty Contract

> Existing verifier-in-the-loop infrastructure agents (**M**: VPP23/Asad26/Bila26-style loops, as instantiated for PQC by [CodAg]/[Bala26]-like pipelines) assume **A**: that the correctness of a cryptographic configuration change is a property of the changed artifact, or of one probed peer. In the important regime **R**, where a live peer population has heterogeneous and partly incomparable PQ capability classes plus rare or periodic peers, **A** breaks. The result is measurable failure **F**: silent PQ withdrawal (proved unavoidable for single-peer gates by [Han26]) and outages of unobserved peers when classical algorithms are removed.
>
> We introduce **Δ**: the agent's verifier quantifies over the telemetry-observed peer classes via shadow-replayed negotiation, and gates narrowing actions with a missing-mass certificate over unobserved classes. Δ changes **mechanism Z**, the relational recall of the verifier and the calibration of residual outage risk, producing property **P**: soundness on observed classes, a bounded outage probability under stated stationarity, and counterexample feedback that redirects the agent toward PQ-preserving fixes.
>
> Unlike **B1** [Han26], which proves the need but supplies no population input; **B2** [CodAg, VPP23, Asad26], whose verifiers are artifact- or spec-local; **B3** [AgSpec, ShAg], whose generic rules carry no protocol-negotiation semantics; and **B4** [Bala26, Jing26], non-agentic pipelines with health-metric rollback, the approach uniquely provides *a population-quantified PQ-preservation and availability guarantee on agent actions with an explicit, testable failure boundary*.
>
> We test this through E1–E9 (§15): ablations, mechanism dose-response, shadow-fidelity tests, calibration and boundary tests, cross-protocol and OT generalisation, adversarial prompts, efficiency, and statistical testing.

$$M + A \xrightarrow{R} F:\quad \Pr[\text{silent PQ withdrawal}] \gg 0,\ \ \Pr[\text{unseen-peer outage}]\ \text{uncontrolled}$$
$$M + \Delta \xrightarrow{R} P:\quad \text{withdrawals on observed classes} = 0\ (\text{given replay fidelity}),\ \ \Pr[\text{outage}] \le U_v\ \text{w.p.}\ 1-\delta\ (T\ge\tau_{\max}).$$

**Final one-sentence test (§30):**
> Verifier-in-the-loop agents perform well when a change's correctness is local to an artifact. We show that PQ migration of live infrastructure systematically breaks this: correctness is a relation over a heterogeneous, partly unobserved peer population, so artifact- and single-peer verifiers let agents silently withdraw PQ protection or break unseen peers. We introduce a population-relational shield that quantifies over telemetry-observed peer classes and certifies the unobserved remainder. It enables sound-on-observed, risk-bounded autonomy with a predicted and demonstrated failure boundary, and mechanism, ablation, cross-protocol, OT and stress tests show when and why it works.

*Lab verdict on the sentence:* compelling if E1 shows a large baseline harm rate on realistic populations *and* E3 shows the dose-response. If baseline harm is rare in realistic populations, the story weakens to a measurement paper (see §21).

---

## 13. Expected Scientific Insight (valuable even if gains are modest)

1. **The soundness of an agent's safety loop is bounded by its verifier's quantifier scope, not by model capability.** We expect frontier models to downgrade just as readily as weaker ones under artifact-scoped verifiers (H4). If true, this is a general lesson for agentic operations: stronger models do not fix an under-quantified verifier.
2. **Crypto migration has a logical part and a statistical part.** Observed peers can be handled exactly. Unobserved peers can only be handled statistically, and the limit is set by *business periodicity*, not sample size. This gives operators a concrete rule: the observation window must cover the longest peer cycle.
3. **Widen/narrow asymmetry.** Widening is safe under precisely stated conditions, and "rank the new algorithm below the best PQ" is a plausible-looking condition that is wrong. This is an actionable correction for human operators and for agent prompts.
4. **In OT, where to put the bump-in-the-wire proxy is a vertex-cover problem.** This turns a practitioner heuristic into an exact rule.
5. A **benchmark and metric** (SPRR, §15) for agentic crypto change that other teams can reuse for any deprecation, e.g. TLS 1.0/1.1 removal, SHA-1 signature removal, or RSA-1024 chains.

---

## 14. Strongest Competitors (must be beaten or matched)

| # | Competitor | Role |
|---|---|---|
| B0 | Same agent, **no verifier** | Floor |
| B1 | Agent + file-scoped lint (e.g. ssh-audit/testssl-style config checks) | Simplest verifier |
| B2 | Agent + **effective-config dump** (`sshd -T`, `openssl s_client`-style) | [Han26]'s vendor-dump gate |
| B3 | Agent + **CBOM score gate** (CycloneDX CBOM + policy) | Industry practice |
| B4 | Agent + **single-peer delivery probe** (modern client) | Closest verifier-in-loop analogue; strongest per [Han26] |
| B5 | Agent + **hand-picked canonical probe set** (Han's two minimal SSH classes + a legacy classical client) | *Hardest baseline*: tests whether telemetry adds anything over expert-chosen probes |
| B6 | Agent + **AgentSpec-style rules** written by an expert ("never remove sntrup761/mlkem768", "never remove x25519 before date") | Strong generic-shield baseline |
| B7 | **Non-agentic deterministic pipeline**, [Bala26]-like: profile → hybrid-enable → health-metric rollback | Is an agent even needed? |
| B8 | B4 + **staged canary with health-metric rollback** ([Bila26]/[Jing26]) | Tests whether rollback alone suffices; it catches outages but *not* silent PQ withdrawal, since nothing "breaks" |
| B9 | Expert human script (ceiling) | Upper bound on progress |
| **B10** | Agent + **one-line log rule**: "never remove an algorithm negotiated in the last T days" | *Simplest-reasonable competitor to Δ1+Δ2.* Predicted gaps: (i) it is blind to *reorderings* that flip negotiation without removing anything (the F3 trap); (ii) it blocks classical removal while any peer still negotiates classical, even when every such class has a PQ alternative, which costs Cov; (iii) it gives no risk statement for unseen peers. If B10 matches Δ on SPRR, OWE **and** Cov, the method contribution collapses to "use your logs" (§21). |

**Matching controls.** Identical LLM, scaffold, tool set, token budget and *number of verifier invocations*. Compute-matched: B5/B6 get the same wall-clock verification budget as Δ1's replays.

---

## 15. Experiment Matrix

**Testbed "PQ-Estate" (PROPOSED).** A containerised estate (containerlab/Mininet) with the following components.
- **TLS responders:** nginx on OpenSSL 3.5 (native ML-KEM), OpenSSL 3.0 + oqs-provider, a Go 1.24+ `crypto/tls` server, and a BoringSSL server.
- **SSH:** OpenSSH across versions: 8.x (sntrup761x25519 available from 8.5 and default from 9.0), 9.9 (adds mlkem768x25519), 10.x (mlkem768x25519 default) [version facts KNOWN from memory, **re-verify**]. Dropbear and Go x/crypto/ssh PQ support are [U].
- **IKEv2:** strongSwan 6.x with ML-KEM via RFC 9370 [U, verify].
- **OT arm:** OpenPLC + Modbus/TCP behind a TLS gateway, and libiec61850 MMS over TLS. Constrained nodes that cannot dual-stack are emulated by build flags or memory caps.
- **Middleboxes:** netfilter/scapy elements that drop multi-segment ClientHellos, and MSS clamping.
- **Peer population generator:** capability classes drawn from real client builds, with Zipf frequencies, periodic batch clients (7-, 30- and 90-day cycles, time-compressed), and legacy classical-only clients.

**Task suite (PROPOSED).** 72 tickets written in operator prose, 12 each in 6 families:
- T1 enable hybrid KEM;
- T2 remove classical by a deadline;
- T3 "harden sshd per this guideline" (Han-style downgrade-inducing prose);
- T4 "fix handshake timeouts" (the ossification/fallback trap);
- T5 OT gateway migration with devices that cannot dual-stack;
- T6 benign distractors (no crypto change needed).

**Agents:** ≥2 open-weight models plus ≥1 frontier API model, all on the same scaffold.

| Exp | Claim | Hypothesis | Baselines | Proposed | Metric | Expected evidence |
|---|---|---|---|---|---|---|
| **E0** | (sanity) | The testbed reproduces [Han26]: B1–B4 miss PQ-KEX removal across its 7 configurations | B1–B4 | — | Detection matrix | Replication of the published negative result; freezes the evaluation pipeline |
| **E1** | C1 | Δ reduces silent PQ regressions and outages **without** reducing PQ coverage | B0–B10 | Δ1+Δ2+Δ3 | **SPRR** (silent PQ regression rate: episodes where some edge that negotiated PQ before negotiates classical after, without an alarm); **OWE** (traffic-weighted failed-handshake edges); **Cov** at task end | SPRR and OWE significantly lower than B4–B8 at equal or higher Cov |
| **E2** | C2 | The mechanism is relational recall and calibration | B4, B5 | Δ1 | ρ on 500 injected violating actions; shadow-replay **fidelity** (replay verdict vs live verdict agreement) | ρ(Δ1) ≈ 1 on observed classes; ρ(B4/B5) equals the class-coverage fraction; fidelity ≥ 0.99, with exceptions catalogued |
| **E3** | C2 | Dose-response: effects scale with telemetry coverage | — | Δ1 with telemetry subsampled to {5, 10, 25, 50, 100}% of the window | ρ, SPRR, OWE | Monotone curves. *If SPRR does not track ρ, the mechanism claim is rejected.* |
| **E4** | C3 | The Δ2 certificate is calibrated when T ≥ τ_max and fails when T < τ_max | — | Δ2 across T/τ ∈ {0.25, 0.5, 1, 2} and class-tail exponents | Realised unseen-class failure mass vs U_v; coverage | Coverage ≥ 1−δ for T/τ ≥ 1; collapse below 1 (**failure boundary R\***) |
| **E5** | C1, C4 | Ablation: each part carries weight | M, M+Δ1, M+Δ2, M+Δ3, M+Δ1+Δ3, full | — | SPRR, OWE, Cov, escalations, tool calls | Δ1 removes withdrawals; Δ2 removes unseen outages; Δ3 reduces escalations and checks at no harm cost |
| **E6** | C4 | Generalisation across protocols and OT | Best of B4–B8 | Full | Same metrics per protocol (TLS/SSH/IKEv2) and on the OT arm; P5 proxy count vs optimal | Effect persists per protocol; OT plans respect P5 |
| **E7** | C5 | Robustness | Best baseline | Full | SPRR under (a) Han-style downgrade prose, (b) injected banners/cert fields (Mantis-style), (c) ossifying middleboxes | Δ1 counterexamples keep SPRR low where baselines fail; report where they don't |
| **E8** | C5 (ext.) | Δ4 path probes prevent the fallback-downgrade in T4 | Full without Δ4 | Full + Δ4 | Fraction of PQ-removing "fixes"; misattribution rate | Pre-registered; reported whether positive or null |
| **E9** | C6 | Efficiency | B4, B5, B6 | Full | Shield latency per action, replays per action, tokens, wall clock, CPU | Overhead ≤ minutes per wave and small next to change windows; gain per verifier call reported |
| **E10** | C3 (falsification) | Where Δ stops helping | — | Full | (a) T<τ; (b) replay infidelity (path-dependent middleboxes, HW offload); (c) extreme class diversity leaving U_v loose → escalation explosion; (d) telemetry-blind peers (on-path sensors with ECH) | Documented boundaries R\*: all reported in the paper |

Each experiment maps to a claim (§15 of the lab protocol) and vice versa: see `research/claims.yaml`.

---

## 16. Statistical Testing Plan

- **Unit of analysis:** the episode, meaning (task, model, condition, seed).
  - Design: 72 tasks × 3 models × 12 conditions × 5 seeds = 12,960 episodes. The primary contrasts are *paired* on (task, model, seed).
  - Budget fallback: 36 tasks × 3 seeds, with a power check below.
- **Primary endpoints:** SPRR and OWE (binary per episode, or proportion). The co-primary non-inferiority endpoint is Cov (margin −5 percentage points).
- **Primary test:** mixed-effects logistic regression, `harm ~ condition + (1|task) + (1|model)`, with the contrast full-Δ vs B4, B5, B6 and B8.
  - Robustness checks: a paired cluster bootstrap over tasks (10,000 resamples, BCa CIs) and McNemar tests on paired episodes.
  - Multiplicity: Holm–Bonferroni across the 5 pre-registered primary contrasts (vs B4, B5, B6, B8, B10).
  - Non-inferiority on Cov uses a one-sided 95% CI.
- **Effect sizes:** risk difference and odds ratio with 95% CIs for binary outcomes; Cliff's δ for latency and tool-call counts.
- **Power (HYPOTHESIZED rates; unpaired two-proportion normal approximation, two-sided α = 0.01 per Holm step; computed in-session):** at 25% vs 5% SPRR, power ≈ 1.00 even at the fallback n = 324 episodes per arm. At **10% vs 5%**, power is only **≈ 0.44 at n = 324** but **≈ 0.97 at the full n = 1,080** (72 × 3 × 5). Task-level clustering lowers effective n and pairing raises it, so recompute by simulation from the E0/E1 pilot's intraclass correlation. **The fallback design is adequate only if the baseline harm rate is ≥ 20%.**
- **Calibration (E4):** empirical coverage with Clopper–Pearson CIs over ≥200 simulated windows per cell; a reliability diagram of U_v against realised mass.
- **Dose-response (E3):** Spearman ρ between telemetry fraction and SPRR, plus a monotone-trend test (Jonckheere–Terpstra).
- **Pre-registration:** hypotheses H1–H4, metrics, thresholds and exclusion rules are committed to `research/manifests/preregistration.md` *before* any Δ run (Baseline-First Rule).
- **No claim of superiority when CIs overlap zero effect.** All seeds are reported.

---

## 17. Reproducibility Plan

- **Single experiment manifest** (`research/manifests/experiment_manifest.schema.yaml`). Every run records experiment_id, git_commit, dataset_version (population spec hash), seed, configuration_hash, model id and version, API date, container image digests, hardware, training/inference time, metrics and timestamp.
- **Pinned artifacts:** container images by digest (OpenSSL, OpenSSH, strongSwan and Go versions enumerated), population generator spec, task suite (versioned YAML), and LLM prompts and tool schemas.
- **Determinism:** seeds for the population generator, class sampler, canary sampler and LLM (temperature fixed; the API seed recorded where supported). Non-determinism from the LLM API is absorbed by the multiple seeds.
- **Baseline-first:** E0 must reproduce Han26's gate-failure matrix before Δ is implemented. The evaluation pipeline and metrics are frozen after E0.
- **Release:** testbed, task suite, telemetry traces, shield code, raw episode logs, and analysis notebooks, all regenerating every figure and table from the logs.
- **Open-weight first:** the primary claims must hold on open-weight models. Frontier API results are supplementary, since API models drift.

---

## 18. Adversarial Reviewer Report

*This section is written by an independent hostile-reviewer agent (Agent H) that had not seen the lab's internal reasoning. See `research/paper/REVIEW_AgentH.md` for the full text; a summary appears below.*

> _To be filled after Agent H returns._

---

## 19. Author Rebuttal Simulation

> _To be filled after §18._

---

## 20. Contribution Scorecard

> _To be finalised after §18/§19._

---

## 21. GO / MODIFY / KILL

> _To be finalised after §18/§19._

---

### Appendix A. Lemma-check output (OBSERVED; `research/analysis/verify_lemmas.out`)

```
L2 product-condition vs explicit interleavings: mismatches=0
L1 widening-only waves that broke availability: 0
L3 widening ranked below ALL PQ algs flipping PQ->classical: 0; not-below-all counterexamples: 205 (of which ranked below best PQ only: 23)
L4 vertex-cover proxy lemma violations: 0
L5 single-peer probe catches: {'mlkem_only_pq': ['drop_mlkem'], 'sntrup_only_pq': ['drop_sntrup'], 'classical': []}
L5 population (observed-class-set) check catches: ['drop_mlkem', 'drop_sntrup']
L6 narrowing-certificate coverage (target >= 0.95): {'iid': {'bound': 1.0, 'bare_GT': 1.0}, 'periodic_T_lt_period': {'bound': 0.0, 'bare_GT': 0.0}, 'periodic_T_ge_period': {'bound': 1.0, 'bare_GT': 1.0}}
```

**Caveats:**
- These are small-instance, abstract-model checks. They do not validate shadow-replay fidelity, library semantics, or any agent behaviour.
- The L6 i.i.d. case is easy (60 classes, N = 20,000); realistic heavy tails are E4's job.

### Appendix B. Research-integrity ledger

- **No experiment on the proposed method has been run.** All E-results above are HYPOTHESIZED.
- Several 2026 arXiv items were confirmed only through search-index snippets. Every number drawn from them must be re-checked against the full text before submission.
- The arXiv ID 2512.12989 is indexed under two titles (Quantigence / "Can Coding Agents Migrate to PQC?"). Resolve this before citing.
- Agent C excluded golang/go#80573 as internally inconsistent.
- The P4 constants and the P6 scheduling claims (Δ6, Agent F) are NOT YET VERIFIED. Δ6 is excluded from this paper.
