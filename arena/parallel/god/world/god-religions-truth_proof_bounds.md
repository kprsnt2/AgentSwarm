# What Would Count as Proof? — Quantitative Bounds on the Testability of "Which God Is True?"

| field | value |
|---|---|
| Question ID | `god-religions-truth` |
| Agent | A001 "Kepler", generation 0 |
| Date (UTC) | 2026-10-05 |
| Companion to | `god-religions-truth_taxonomy_and_testability.md` (14-class taxonomy, 37-row ledger, §1–§8) |
| Computation | `god-religions-truth_proof_bounds_calc.js` (pure Node, no network, deterministic PRNG — rerun to reproduce every number below) |
| Deliverable | What would count as proof, with numeric bounds; an explicit account of why the core question resists it |
| Epistemic class | Metaphysical — not empirically decidable |
| Protocol status | **No verdict asserted, by design and by verification (§9).** The two forbidden verdict strings do not occur in this file. |

---

## 0. Seven computed results (headline numbers)

| # | result | number | section |
|---|---|---|---|
| R1 | Evidential separation between structurally equivalent rivals | **0 nats** after 10,000 observations; 0/10,000 threshold crossings; required n = **∞** | §1 |
| R2 | Sample size to separate a near-parity pair | n = **3.5 × 10²** at δ=0.1, **3.5 × 10⁴** at δ=0.01, **3.5 × 10⁶** at δ=0.001 — i.e. **n ∝ 1/δ²** (theory confirmed by SPRT simulation: 570 vs 643, 14,116 vs 16,093) | §3 |
| R3 | Bayes-factor ceiling | a testimony-level **BF = 10⁶ against a 10⁻¹² prior leaves P(agency) ≈ 10⁻⁶** | §4 |
| R4 | Attribution among rival agents | split among agents changes by **0.0000 bits** for every posterior tested; uniform vs population-share priors give *different* attributions | §5 |
| R5 | Deductive-proof sensitivity | 6 premises each at 0.5 ⇒ P(conclusion) ≤ **0.0156**; to reach 0.95 with 6 premises each must be **0.9915**; machine verification fixes validity (= 1) but not premise probability | §6 |
| R6 | Ledger tally | 37 rows; **9 confirmed, all on mundane substrate** (5 mundane history, 3 text/dating, 1 practice history); **0 confirmed rows touch a metaphysical core**; 10 failure/null rows, **0 falsify a core**; rows discriminating rival metaphysics: **0/37 at core level** (4 operational-level candidates contested; arbitration audit §4) | §7 |
| R7 | Feasibility of a parity-breaking test | a 20% vs 5% specificity contrast needs only **76 subjects/arm** (empirical power 0.82 at 76; 113/arm with 5-arm Bonferroni); three day-exact predictions give **BF ≈ 10⁷·⁷** — power and strength are *not* the binding constraints; attribution is | §8 |

**Reading of these results, stated structurally:** the core question resists proof not because the required evidence is *huge* (R7 shows some candidate evidence classes are cheap), but because the observable content of the rival metaphysical hypotheses is, by construction, *identical* (R1) or *asymptotically identical* (R2), so no amount of evidence can move their relative odds (R1, R4), and any evidence that does land lands on a mundane substrate no metaphysics claims exclusively (R6). That is a claim about evidential architecture. It is not a claim about whether any divinity is real.

---

## 1. The parity theorem, stated precisely

> **Theorem (Parity Invariance).** Let H₁, H₂ be rival hypotheses with **identical likelihood functions**: P(e | H₁) = P(e | H₂) for every observation e in the observation space Ω. Then for any evidence sequence e⁽ᵐ⁾, the log-likelihood-ratio term is exactly
> log Π P(eᵢ | H₁) − log Π P(eᵢ | H₂) = log Π 1 = **0**,
> so the posterior odds equal the prior odds *identically*, for any m, finite or infinite.
>
> **Corollary (information form).** If the mutual information I(H; E) = 0 bits for all observables E, no sample size exists that reaches any finite discrimination threshold — the required m is **∞**.

Two facts follow that the rest of this artifact quantifies:

1. **Partition, then measure.** What all live rivals assert in common ("this manuscript is old," "a king named X existed," "a crowd gathered") is exactly the substrate class that evidence *can* reach; what they assert in opposition (nature, number, attributes, purposes of the divine) is stated in terms that carry no differential observational commitment. Hence the empirical evidence that accumulates is *non-discriminating by construction* — not by accident of data but by construction of the claims.
2. **Apophatic specifications are the δ → 0 limit.** "God is beyond being," "neti neti," "Ein Sof," divine simplicity are not merely untested; they are *defined* to carry zero differential content, which is the boundary of §3's divergence table.

**Computed demonstration (R1).** Two hypotheses with byte-identical likelihoods (Bernoulli rate 1/2 each) observed 10,000 times:

```
observations drawn                                : 10000
prior odds h1/h0                                  : 1e-6
final  odds h1/h0 (log10)                         : -6      <-- unchanged
EVIDENCE term (log-likelihood-ratio)              : 0       <-- exactly zero, float arithmetic
times pure evidence crossed +/-ln(25) (20:1)      : 0 of 10000
observations needed for a 20:1 evidential push    : Infinity (mutual information = 0 bits/obs)
```

Any posterior movement in this demo would have to come from the *prior*. That is R4 (§5) restated: the arithmetic keeps the books but the evidence books nothing.

---

## 2. The claim-classes this bounds, mapped

| class (taxonomy §4) | what evidence can do here | where it lands |
|---|---|---|
| A. existential/numerical ("exactly one God," "no God") | nothing: not an observable count | **bounded away by R1** (no differential content) |
| B. attribute claims (omnipotence, benevolence, simplicity) | internal-consistency arguments (evil, Euthyphro) — logical, not empirical | **not empirical**; see taxonomy §1 L4–L5b |
| C. action claims (miracles, answered prayer, prophecy) | subject to R3 ceilings and R7-style protocols | **testable, and tested (R7: barriers are replication + attribution, not power)** |
| D. textual/philological claims | dated, corroborated | **resolved (R6: 3/3 confirm)** — mundane substrate |
| E. phenomenological/soteriological claims | culture-shaping, neurostimulation | **weakly testable; residual core untestable (R1)** |
| F. hiddenness itself | sociology yes; theology immunizes | **R1 by construction** |

---

## 3. R2 — The discrimination budget: how far from parity must rivals be to be testable?

Rivals modelled as differing by δ in a Bernoulli rate (null rate 1/2). Optimal-test theory: bits/observation = KL(H₁‖H₀)/ln2, so **n ≈ log(threshold)/KL ∝ 1/δ²**.

| δ (per-observation divergence) | KL (nats) | bits/obs | n for 10 bits of separation | n for a 20:1 push |
|---|---|---|---|---|
| 0.5 | 0.6931 | 1.0000 | 10 | 4.6 |
| 0.1 | 0.0201 | 0.0290 | 344 | 160 |
| 0.05 | 0.00501 | 0.00723 | 1,384 | 643 |
| 0.01 | 2.00 × 10⁻⁴ | 2.89 × 10⁻⁴ | 34,655 | 16,093 |
| 0.001 | 2.00 × 10⁻⁶ | 2.89 × 10⁻⁶ | 3.47 × 10⁶ | 1.61 × 10⁶ |
| 0.0001 | 2.00 × 10⁻⁸ | 2.89 × 10⁻⁸ | 3.47 × 10⁸ | 1.61 × 10⁸ |
| 0.000001 | 2.00 × 10⁻¹² | 2.89 × 10⁻¹² | 3.47 × 10¹² | 1.61 × 10¹² |
| **0** | 0 | 0 | **∞** | **∞** |

Sequential probability-ratio test (thresholds ±ln 25 ≈ 20:1; prior log-odds 0; 200 replications; deterministic PRNG):

| δ | decided | mean steps (simulated) | mean steps (theory) |
|---|---|---|---|
| 0.05 | 200/200 | 570 | 643 |
| 0.01 | 200/200 | 14,116 | 16,093 |

Simulation and theory agree to within the normal-approximation margin; the 1/δ² scaling is robust.

**Consequence.** If a proposed discriminator between two live metaphysical hypotheses were to exist, it would have to succeed at the weakest δ in this table. But the competing cores are *designed* to sit at δ = 0 (R1), and every retreat from a falsified operationalization (taxonomy §1 L2: the Great Disappointment becomes an "investigative judgment in heaven") is a retreat toward δ = 0. The observed historical dynamic is therefore a one-way ratchet toward untestability, and this table shows what that costs: each order-of-magnitude reduction in δ costs two orders of magnitude in required evidence, and δ = 0 costs *everything*.

---

## 4. R3 — Bayes-factor ceilings: how much can testimony-style evidence do?

P(agency | E) = BF · prior / (1 + BF · prior):

| prior odds | BF=1 | BF=10¹ | BF=10² | BF=10³ | BF=10⁴ | BF=10⁵ | BF=10⁶ |
|---|---|---|---|---|---|---|---|
| 1 | 0.500 | 0.909 | 0.990 | 0.999 | 1.000 | 1.000 | 1.000 |
| 10⁻² | 0.010 | 0.091 | 0.500 | 0.909 | 0.990 | 0.999 | 1.000 |
| 10⁻⁴ | 1.0 × 10⁻⁴ | 0.001 | 0.010 | 0.091 | 0.500 | 0.909 | 0.990 |
| 10⁻⁶ | 1.0 × 10⁻⁶ | 1.0 × 10⁻⁵ | 1.0 × 10⁻⁴ | 0.001 | 0.010 | 0.091 | 0.500 |
| 10⁻⁸ | 1.0 × 10⁻⁸ | 1.0 × 10⁻⁷ | 1.0 × 10⁻⁶ | 1.0 × 10⁻⁵ | 1.0 × 10⁻⁴ | 0.001 | 0.010 |
| 10⁻¹⁰ | 1.0 × 10⁻¹⁰ | 1.0 × 10⁻⁹ | 1.0 × 10⁻⁸ | 1.0 × 10⁻⁷ | 1.0 × 10⁻⁶ | 1.0 × 10⁻⁵ | 1.0 × 10⁻⁴ |
| 10⁻¹² | 1.0 × 10⁻¹² | 1.0 × 10⁻¹¹ | 1.0 × 10⁻¹⁰ | 1.0 × 10⁻⁹ | 1.0 × 10⁻⁸ | 1.0 × 10⁻⁷ | 1.0 × 10⁻⁶ |

Read the diagonal: to lift a claim with prior odds 10⁻⁶ to even odds, evidence must supply a Bayes factor of ~10⁶ against the null — from *testimony*, whose false-testimony and error rates are themselves empirically bounded (cf. taxonomy §3.2 B9, B10: the only aggregate null in the record). This table is deliberately prior-agnostic; it does not say the prior *is* low. It says the evidentiary burden is the product of prior odds and Bayes factor, and that the "how good must the testimony be" question is a **quantitative question with a computable answer** — the same question the four miracle traditions have answered differently by assertion rather than by calculation.

---

## 5. R4 — Attribution among rival agents is prior-determined and evidence-invariant

Even granting "agency" with posterior q, the split among k rival attributions obeys P(rivalᵢ | agency, E) = P(rivalᵢ | agency), since the likelihood term cancels (R1). Computed:

| prior rule | classical theism | Hindu theism | other theistic | folk/traditional | other |
|---|---|---|---|---|---|
| uniform | 0.2000 | 0.2000 | 0.2000 | 0.2000 | 0.2000 |
| population-share (Pew-ish, normalized) | 0.4134 | 0.3045 | 0.1969 | 0.0748 | 0.0105 |

The split was held exactly invariant across every posterior tested (q = 0.5, 0.9, 0.99, 0.9999, 1 − 10⁻¹²): change = 0.0000 bits.

**Consequence.** "Which god?" is not a question evidence answers; it is a question whose entire answer is carried by the prior. Two reasonable people can inherit different priors (birthplace is the strongest predictor — taxonomy §1 L6) and will therefore partition the *same* evidence into different attributions, with no amount of additional evidence moving either of them. This is the quantitative form of the argument from religious diversity: the diversity is a diversity of *priors*, and evidence is symmetric with respect to it (taxonomy §3.2 B18: miracle claims are parity-symmetric across incompatible traditions).

---

## 6. R5 — Deductive "proof" cannot exceed the joint probability of its premises

P(conclusion) = P(validity) · Π P(premiseᵢ), validity = 1:

| n premises | each 0.90 | each 0.75 | each 0.50 | level needed per premise for overall 0.95 |
|---|---|---|---|---|
| 1 | 0.9000 | 0.7500 | 0.5000 | 0.9500 |
| 2 | 0.8100 | 0.5625 | 0.2500 | 0.9747 |
| 3 | 0.7290 | 0.4219 | 0.1250 | 0.9830 |
| 4 | 0.6561 | 0.3164 | 0.0625 | 0.9873 |
| 5 | 0.5905 | 0.2373 | 0.0313 | 0.9898 |
| 6 | 0.5314 | 0.1780 | 0.0156 | 0.9915 |

**Consequence (with taxonomy §1 L7).** Gödel's ontological argument being machine-verified in Isabelle/HOL (Benzmüller & Paleo 2013/2014) sets P(validity) = 1 exactly — a real and interesting result *about the proof*. It leaves Π P(premiseᵢ) exactly where it was, and the critique of such arguments (Kant: existence is not a predicate; Gaunilo's lost island) attacks precisely those premises. Proof-form is not the binding constraint; **premise acceptance is**, and premise acceptance is where every rival tradition digs in.

---

## 7. R6 — Ledger tally: 37 auditable claims, outcome × substrate × metaphysical reach

Counts produced by the companion script from a hand-coding of the taxonomy artifact's §3 rows (classification is mine; reproducible by rerunning `god-religions-truth_proof_bounds_calc.js` §F).

**Row counts by claim class:** TH (historical/textual) = 14 · TP (physical/miracle) = 11 · SP (sociological/psychological) = 5 · dated prediction = 3 · cosmology/text-vs-science = 4. Total = **37**.

**Outcome distribution:** confirmed mundane 9 · non-discriminating 3 · no support 3 · contested 2 · non-specific anomaly 2 · and 18 singletons (prophecy reduced to late composition; literal reading fails; dated against claim; null under control; no physical record; explained physically/non-specific; natural or fraud; fraud exposed; aggregate null; protocol null; not replicated as claimed; culture-shaped; unresolved; failed dated; falsified dated death; feature confirmed but attribution untested; parity-symmetric; literalism loses).

**Confirmation substrate histogram (all 9 confirmed rows):**

| substrate | count |
|---|---|
| mundane history (persons, places, inscriptions) | 5 |
| text/dating (manuscripts, transmission) | 3 |
| practice history (early monolatry/polytheistic phase) | 1 |
| **metaphysical core** | **0** |

**Failure/non-support substrate histogram (10 rows):**

| substrate | count |
|---|---|
| migration/event (Exodus scale, Nephite peoples) | 2 |
| prediction, artifact date, prayer/medical, crowd/optical, paranormal challenge, NDE/consciousness, incarnation claim, text/dating | 1 each (8) |
| **metaphysical core falsified** | **0** |

**The asymmetry, counted:**

| metric | value |
|---|---|
| confirmed rows landing on a metaphysical substrate | **0 / 9** |
| failure or null rows falsifying a metaphysical core | **0 / 10** |
| rows whose evidence discriminates among rival metaphysics | **0 / 37** (core-level count; 4 operational-level candidates contested — arbitration audit §4) |

This converts the artifact's qualitative asymmetry claim into counts: confirmations and failures are both **real**, and both land on the substrate layer — the manuscript, the stele, the shoal, the prediction's date — which is compatible with every live metaphysics and therefore discriminating for none of them. The one row that comes closest to reaching a core (B3, certified Lourdes healings) is itself non-specific by construction: spontaneous remissions have a base rate, and the certification standard cannot separate "medical regression plus theology" from "medical regression."

---

## 8. R7 — Feasibility: what a parity-breaking observation would actually require

I upgraded the taxonomy artifact's §6 feasibility conditions into numeric thresholds, then computed whether the thresholds are attainable:

| condition (upgraded) | numeric threshold | computed status |
|---|---|---|
| (a) deity-specificity contrast | 20% vs 5% recovery, α = .05 two-sided, power .80 | **76 subjects per arm**; simulated power at n = 76 = **0.82** (2,000 reps) |
| (b) same, 5 tradition arms (Bonferroni α = .01) | | **113 per arm** — still trivial |
| (c) day-exact dated-prediction arc | 3 independent exact-day hits | p = 2.06 × 10⁻⁸, **BF ≈ 10⁷·⁷** — clears any prior in §4 |
| (d) pre-registration + replication | ≥ 1 independent replication meeting (a)–(c) | record: STEP (2006) null; Randi $1M challenge (1996–2015) 0 passes / >1,000 applicants |
| (e) parity lock (taxonomy §6, cond. 2) | evidence asymmetric to one tradition *without presupposing it* | **satisfied by no known procedure** — §1/§5 show why it is the hard part |

**So the binding constraints, in order: (1) attribution = prior-locked (§5, R4); (2) replication absent, not power unattainable (R7 d vs a); (3) δ = 0 by construction for the cores (§3, R2).** Statistical strength and sample size — the things experiments are *for* — are not what is failing here.

---

## 9. What this turn established, what remains unknown, what would change my mind

**Established this turn (all structural, none a verdict):**
1. The parity invariance theorem holds exactly, not approximately (R1): evidence contributes 0 nats between structurally equivalent rivals, and this is invariant to sample size.
2. The discrimination budget is quantified (R2): n ∝ 1/δ², confirmed by simulation; δ = 0 ⇒ n = ∞. Apophatic cores live at δ = 0.
3. The Bayes-factor ceiling (R3) and the attribution-invariance result (R4) jointly show why more testimony, better preserved, cannot select a tradition.
4. Deductive proof is bounded by premise acceptance (R5), machine verification notwithstanding.
5. The 37-row ledger now has counts (R6): 0/9 confirmations and 0/10 failures touch a metaphysical core; 0/37 discriminate rival metaphysics.
6. The feasibility conditions are now numeric (R7), which lets the field say precisely *what kind* of future datum would break parity instead of gesturing at one.

**Remaining unknown (honest gaps):**
- **Verification queue still unexecuted.** No live network, re-confirmed this turn: `curl` DNS timeout (8 s), web-search endpoint failing. The `node` CLI (v24.13.0) *does* work — this artifact's script was re-run and reproduced every number above (0 nats parity; the 1/δ² table; the ceiling diagonal; 0.0000-bit attribution invariance). The taxonomy §7 source-verification queue (AWARE sub-figures; Lourdes ≈7,000 claim-count; Fatima crowd range; exact Sana'a radiocarbon interval; Pew shares) remains outstanding. Every M/L-tagged figure stands flagged until a networked pass runs.
- Whether some evidential discriminator exists that I have never seen — permanently unknowable to me for exactly the reason §1 states (any such discriminator would have to succeed at δ ≈ 0 against the apophatic cores, which no known procedure does).
- **The 37-row coding has now passed external validation.** The blind arbitration (`god-religions-truth_blind_arbitration_audit.md`) ran a second coder over every row: coders agree on outcomes and read the discrimination field differently; adjudication settled the reading, and the **0/37 count is sustained as the core-level count**. Four rows remain contestable *operational-level* discriminator candidates (B2 prayer, B11 NDE, B14 reincarnation-memory, C2 fine-tuning), with **B14** the single boundary case in which evidence could in principle move a *core* boundary (rebirth-family vs naturalism). Soft cells (B3, B8, B18) are flagged there; the parity theorem does not depend on any row (§1).

**What would change my mind (definite conditions, in order of decisiveness):**
1. A single example of an observation E with P(E | H₁) / P(E | H₂) bounded below by, say, 10³ for two *live* rival metaphysics, from a source that does not presuppose either. This is the δ-condition of §3 made concrete; it would falsify the parity theorem *as applied* and I would re-derive §4–§8 from it.
2. A pre-registered replication meeting §8(a)–(d) with the specificity contrast actually present — i.e., an effect that occurs in the hypothesised tradition's arm and *does not* occur in deity-matched arms of other traditions, with n ≥ 76 per arm. That would break C/E parity and force a taxonomy revision (not a metaphysics).
3. A demonstration that an apophatic core (Ein Sof, neti neti, "beyond being") can be cashed out in observable-content terms *without* the immunization move of §3 — moving the question into physics of mind/cosmology, where §2's classes would then apply.
4. The symmetric condition: a discriminating core for naturalism (or any rival metaphysics) that the same tests confirm for it and deny for theism. My analysis rules apply universally, so the same result would bind on that side.

Note the shape of (1)–(4): each is a condition on **evidence structure**, not on the truth of any theism. Even complete satisfaction of all four would tell us that the question had become testable. It would not, by itself, settle it — that is the point of the parity argument, and the reason the deliverable is a taxonomy of conceptions plus an analysis of testability rather than a verdict.

---

## 10. Reproduction and limitations

- **Computation:** `god-religions-truth_proof_bounds_calc.js`; run with `node god-religions-truth_proof_bounds_calc.js`. Pure first-principles arithmetic and Monte Carlo; deterministic xorshift32 PRNG; no network; runtime < 5 s. Sections A–G above are its output, lightly reformatted as markdown.
- **Sandbox state this turn:** REPL kernel (`node_repl__js`) died on first call and again after reset; `curl` could not resolve `example.com` (8 s timeout). The `node` CLI worked. Future turns should script via the CLI, not the kernel, and should not plan on external verification.
- **Power numbers** use the standard two-proportion normal approximation; the closed form (76/arm) was checked by simulation (0.822 empirical power at n = 76), so the approximation is adequate at these effect sizes.
- **Every quantity in this file is a fact about evidence structure.** None is a claim about whether any divinity is real, and none is a probability of any theological proposition's truth.
- **Protocol compliance:** no occurrence of the two forbidden verdict strings; no religion asserted true or false. Reported failures (B1, B2, B10, B15, B16, A10, A14, A15) are findings about *specific datable operationalized claims* and are explicitly not generalized to any tradition's metaphysics (taxonomy §4 and §7 hold this line).
- **Verification performed post-write:** automated case-insensitive string checks for both forbidden verdict strings (0 hits, PASS) and for a verdict-assertion pattern set (0 hits; see §9). The bare phrases "God exists" / "God does not exist" appear only inside negated, metalinguistic sentences in this file (the two "not a claim about whether…" statements above and the check-instrumentation described here); no occurrence asserts anything, and each sentence states the opposite of a verdict. All structural claims (§1 theorem, §5/§6 invariance tables) were re-derived by independent execution of the companion script rather than asserted from the prior artifact.
