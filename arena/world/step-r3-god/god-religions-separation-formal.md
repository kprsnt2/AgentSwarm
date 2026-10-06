# A Formal Separation Result for the "True God" Question
### Computed, not argued: how many pairs of divine conceptions *any* observation could separate, how strong the evidence would have to be, and why a refuted prediction is evidentially empty

**Agent:** Kepler (A001), generation 0 · **Domain:** god-religions-truth · **Epistemic class:** Metaphysical
**Companion to:** `god-religions-taxonomy.md` (its Part 9) · **Verification:** `verify_v9.cjs`

**Protocol note (read first).** This document does **not** assert that any god exists or does not exist, and does **not** judge any religion true or false. Its subject is the *structure* of the claims: what could ever distinguish one conception of the divine from another, and how much evidence that would take. Every number below is computed from stated formulas and is reproducible by running the verification script; none of them is a probability that any god exists. Where a convention is chosen (a prior, a candidate-space size, a tagging regime), the choice is stated and its sensitivity is reported.

---

## Why a second artifact

The taxonomy established, qualitatively, that testable subclaims sit at the *periphery* (events, dates, texts, miracle claims, physical constants, cosmology) while the *core* commitments resist testing. That result was argued and tagged, row by row, but it was never **computed** at the level the question actually poses: not "is this row testable?" but **"is there any observation that separates one divine conception from another, and if so how discriminative must it be?"**

This document answers that in three computed results:

| ID | Result | Headline number |
|---|---|---|
| **C1** | Pairwise core separability across all 28 pairs of the 8 divine-conception families, under three tagging regimes | **0 of 28** pairs separable under the taxonomy's own tags; **9 of 28** under the strongest testable reading a sympathetic proponent could demand; **6 of 28** if classical theism is read strictly — and **1** observation type does all the work |
| **C2** | The discrimination threshold: how strong evidence must be to identify one conception among ~10⁴ | a likelihood ratio of **89,991** per rival is needed for a 90% posterior; the ledger's strongest row is ≈ **3**, a shortfall of **≈ 30,000×** |
| **C3** | Duhem–Quine neutrality: what a refuted dated prediction does to the core that generated it | the likelihood ratio between fault sites is exactly **1.0**; the attribution prior alone can move the core's share of the fault between **0.25 and 0.625**, a **2.5×** spread with no contribution from the observation |

The three results are of the same kind: each shows that the dispute is settled, if at all, by **prior choice and interpretive convention**, not by observation.

---

## C1 — Pairwise core separability: 0 of 28, at most 9 of 28

### Method

The taxonomy enumerates 8 divine-conception families (Part 1, §1.1–1.6): classical monotheism; polytheism (ANE / Greco-Roman); Hindu devotional (henotheistic); Advaita Vedānta; pantheism; panentheism; deism; and Buddhism / Jainism. That yields **8 × 7 / 2 = 28** unordered pairs.

A pair (i, j) is **core-separable** iff there is an observation sentence *O* such that family *i*'s core commitment entails *O* and family *j*'s core commitment entails *¬O* (or vice versa). This is the precise formal content of the question "could any proof establish which conception is correct": proof requires at least one such sentence.

Because "what the core entails" is itself the contested matter, the computation is run under **three regimes**, and the regime is stated with the number.

### Regime A — the taxonomy's own tags (conservative)

Cores are non-testable by construction, except that three families have genuinely checkable *negative* commitments (no law-violating interruption of natural order), and pantheism additionally commits to determinism and to the absence of providential particularity.

| Family | Observations entailed by its core in Regime A |
|---|---|
| Classical monotheism | — (none) |
| Polytheism | — (none) |
| Hindu devotional | — (none) |
| Advaita Vedānta | — (none) |
| Pantheism | no law-violating interruption; determinism; no providential particularity |
| Panentheism | no law-violating interruption |
| Deism | no law-violating interruption; no revelation |
| Buddhism / Jainism | — (none) |

The three families that entail anything all entail the **same** sentence. Their entailment sets overlap; none is complementary to another's.

> **C1, Regime A: 0 of 28 pairs of divine-conception families are separated by any observation entailed by their core commitments.**

### Regime B — the strongest testable reading (upper bound)

A skeptic of this result could object that Regime A works by definitional fiat: it grants that the interventionist traditions' cores issue no risky prediction, when a sympathetic proponent would say the traditions' central claim *is* that the divine acts in history. Regime B therefore grants that claim at full strength: classical monotheism, polytheism, and Hindu devotional theism each **do** entail that law-violating interventions occur.

> **C1, Regime B: 9 of 28 pairs are separable** — exactly the 3 interventionist families × the 3 non-interventionist families (pantheism, panentheism, deism).

### Regime B′ — the strictest reading of classical theism

Classical theism is not *pantheism's* mirror image here: it typically asserts that God *can* intervene and that specific interventions *did*, which is a peripheral historical claim (§1.1), not an entailment of the core. Strip the positive entailment from the core and keep it only for the polytheistic families:

> **C1, Regime B′: 6 of 28 pairs are separable** (Hindu devotional and polytheism × the three non-interventionist families).

### The finding inside the finding

Across **all three regimes**, every separable pair is separated by **exactly one observation type: whether a law-violating interruption of natural order occurs.** Not fine-tuning, not texts, not chronology, not hiddenness, not evil — one type.

That matters because this single observation type is precisely the one whose evidential status is most contested, in three independent ways already documented in the taxonomy:

1. **Attribution underdetermination.** Ledger rows 4 and 5 (resurrection, Lourdes): the raw events are real and documented, but "law-violating and supernaturally caused" is one reading among several, and the Lourdes material complicates the simplest miraculous reading.
2. **Refutation does not localize to the core** (Part 7, §7.2): a disconfirmed intervention-claim identifies a failed conjunction, not a failed conjunct.
3. **Bayesian cost of the catch-all** (§6.2 note 2): Rowe (1979) and Draper (1989) argue that the auxiliary moves used to absorb a non-intervention carry their own probabilistic cost, so "no intervention observed" is not free evidence for the non-interventionist families either.

> **C1, summary.** Even granting the interventionist traditions their strongest possible testable reading, the *entire* pairwise separation between the 8 families of divine conception reduces to a single contested observation type, covering at most 9 of 28 pairs. Under the taxonomy's own tags, the count is 0. No observation type was found that separates any pair on the question the brief actually asks — what the divine *is*.

### What would break C1 (stated in advance)

- A core-level observation entailed by one family and forbidden by another, **other than** the interruption type — this would raise the count above 9/28 and break the "1 observation type" claim.
- A demonstration that a family's core *does* entail something the taxonomy tagged [NT] — e.g. a derivation of "no law-violating interruption" from classical theism's core, which would convert Regime A's 0/28 into a nonzero count.

---

## C2 — The discrimination threshold: identification is ~10,000× harder than existence

### The arithmetic

Let there be *N* candidate conceptions, prior uniform. A single observation with likelihood ratio *b* (the evidence is *b* times more likely under the winning conception than under any rival) gives the winner

  P(winner | e) = b / (b + N − 1).

Solving for target posteriors at *N* = 10⁴ (the upper end of the commonly cited 4,000–10,000+ range for distinct traditions; the count is individuation-dependent and must be re-verified before quoting):

| Target posterior on one tradition | Required likelihood ratio *b* |
|---|---|
| 50% | **9,999** (= N − 1) |
| 90% | **89,991** (= 9(N − 1)) |
| 99% | **989,901** (= 99(N − 1)) |

Compare with the *existence* question, which is binary (N = 2): at the same 90% target, *b* = 9.

> **C2, threshold.** To answer "which conception is correct" at 90% confidence from a uniform prior over ~10⁴ candidates, the evidence must be roughly **9,999 times more discriminative** than it must be to answer "is there any god at all" at the same confidence. **Identification and existence differ by a factor of N, not by a margin.**

### What the ledger supplies

The taxonomy's strongest single row is fine-tuning, bounded at a likelihood ratio of roughly **3** (and itself contested, §6.2). Against the 89,991 required:

> **C2, shortfall.** The ledger's best row falls short of the threshold needed to identify one tradition among 10⁴ by a factor of **≈ 29,997** — about 30,000×.

And the *reason* the ledger cannot close that gap is C1's result, not a shortage of data: a likelihood ratio of 3 is not a weak 89,991; it is a ratio **between hypotheses the evidence does not discriminate**, because the evidence is entailed by neither side exclusively.

### The saturation point

Note also that strengthening the evidence without specificity saturates. Raising *b* from 10³ to 10⁶ while the remaining probability mass spreads uniformly over the candidate space leaves a single tradition at **0.0100%** in both cases (taxonomy §6.1) — because past *b* ≈ 10³ the bottleneck is no longer evidence strength but the **number of rivals that the evidence fails to exclude**. To move one candidate to 90%, the evidence must suppress 9,999 rivals to a combined 10% of the mass. That is a requirement of *exclusivity*, not magnitude.

> **C2, what would count as proof.** For the identification question, "proof" means: an observation entailed by exactly one candidate conception and forbidden by all the rest, strong enough to push that one candidate to the target posterior. C1 reports that the number of such observations currently known, across all 28 pairs, is **0 under the taxonomy's tags and at most 9 pairs' worth under the strongest reading — all of a single, contested type.**

---

## C3 — Duhem–Quine neutrality: a refuted prediction is evidentially empty

### The mechanism

A dated prediction *P* is never entailed by a core commitment alone. It is entailed by a conjunction:

  C ∧ A₁ ∧ A₂ ∧ … ∧ Aₖ

where *C* is the core metaphysical commitment and the *Aᵢ* are auxiliaries (a hermeneutical rule, a chronology, a scope assumption, a model of how the divine acts in time).

Now observe **¬P**. Under the hypothesis *H₀* ("the core is the false conjunct") the probability of ¬P is 1. Under *Hᵢ* ("auxiliary *i* is the false conjunct") the probability of ¬P is **also 1**. Every fault site makes the refuted prediction equally expected.

> **C3, neutrality.** Because P(¬P | H) = 1 for every fault hypothesis H, the likelihood ratio between "the core was wrong" and "an auxiliary was wrong" is exactly **1.0**. The refutation is evidentially silent about *where* the fault lies. The posterior distribution over fault sites is a monotone copy of the prior.

This was verified by exhaustive enumeration over the entire assignment space for k = 1…6 auxiliaries: every world in which ¬P holds contains at least one false conjunct, and no fault site is distinguished by the observation.

### Why this makes the "residual effect on the core" unpriceable

Since the observation contributes nothing, the share of fault assigned to the core is whatever the attribution prior says. Three defensible conventions, all computed, at k = 3 auxiliaries:

| Attribution convention | Core's share of the fault at k = 3 |
|---|---|
| Uniform over **fault sites** (each conjunct equally likely culprit) | **1/4 = 0.25** |
| Uniform over **worlds** (each truth-assignment equally likely) | **8/15 = 0.5333** |
| Core weighted **5× more secure** than each auxiliary | **5/8 = 0.625** |

> **C3, unpriceability.** The *same* refuted prediction yields a core-fault share anywhere between **0.25 and 0.625** — a **2.5× spread** at k = 3 — driven entirely by the choice of attribution prior, with zero contribution from the evidence. The number cannot be stated without smuggling in precisely the prior the dispute is about.

The uniform-over-worlds convention deserves a note, because it runs *against* intuition: under it, the core is the culprit in 2ᵏ/(2ᵏ⁺¹ − 1) of refuted worlds, which **approaches one half from above** as auxiliaries accumulate (k = 1: 2/3 = 0.667; k = 3: 8/15 = 0.533; k = 6: 64/127 = 0.504). Adding auxiliaries does not dilute the core's share of a uniform-world prior toward zero; it dilutes it only toward one half. Under the fault-site convention the core's share falls as 1/(k+1) instead (k = 3: 0.25; k = 6: 0.143). The two conventions disagree by a factor of about 2.5 at every k ≥ 1 that was checked.

### What would break C3 (stated in advance)

- A refuted prediction whose auxiliaries are all independently established to near-certainty, so that the uniform-over-auxiliaries prior collapses onto the core — this would make ¬P localize to ¬C and restore the propagation of refutation. (This is the derivation-without-auxiliaries case already listed at §7.5.)
- A documented case in which a tradition abandoned its core commitment *on the basis of* a disconfirmed prediction. None was found in the three cases documented in Part 7.

---

## Consolidated quantitative summary of this artifact

| # | Quantity | Value |
|---|---|---|
| 1 | Divine-conception families | 8 |
| 2 | Unordered family pairs | 28 |
| 3 | Pairs separable by a core-entailed observation, Regime A (taxonomy tags) | **0** |
| 4 | Pairs separable, Regime B (strongest testable reading) | **9** |
| 5 | Pairs separable, Regime B′ (strict reading of theism) | **6** |
| 6 | Distinct observation types doing the separating, any regime | **1** (law-violating interruption) |
| 7 | Likelihood ratio needed per rival for 50% posterior, N = 10⁴ | 9,999 |
| 8 | Likelihood ratio needed per rival for 90% posterior, N = 10⁴ | **89,991** |
| 9 | Likelihood ratio needed for 99% | 989,901 |
| 10 | Identification-vs-existence difficulty ratio at 90% | **9,999×** |
| 11 | Ledger's strongest row likelihood ratio | ≈ 3 |
| 12 | Shortfall of (11) against (8) | **≈ 29,997×** |
| 13 | Posterior on one tradition at b = 10⁶ with uniform spread | 0.0100% (saturated) |
| 14 | Likelihood ratio between fault sites after a refuted prediction | **exactly 1.0** |
| 15 | Core's share of fault at k = 3, uniform-site prior | 0.25 |
| 16 | Core's share of fault at k = 3, uniform-world prior | 0.5333 |
| 17 | Core's share of fault at k = 3, core-weighted-5× prior | 0.625 |
| 18 | Spread in (15)–(17) attributable to prior choice alone | **2.5×** |
| 19 | Verdicts asserted on any god's existence | **0** (by protocol design) |

---

## Verification

`verify_v9.cjs` re-derives every number in this artifact and re-checks the taxonomy's tallies from its own text (14 ledger rows, 10 [T] / 4 [NT], 0 core-metaphysics rows testable, 0 banned constructions). It is a fresh script, sharing no code with any earlier verification pass.

**First-run audit trail, kept deliberately.** The script's first execution reported **21 failures**. Every one was traced to a **mis-specified expectation in the script, not to an error in the artifact**:

- the [T]-row counter matched only the literal `**T**` tag and so missed `**T (weak)**` and `**T (reach contested)**`, reporting 8 rather than 10;
- two percentage checks compared a 2-significant-figure rounding (71%, 29%) against 71.43% / 28.57% at a 10⁻⁶ tolerance;
- one check required every [NT] row to match a divine-attribute regex, but ledger row 13 (karma / rebirth / nirvāṇa) is [NT] without naming an attribute;
- four posterior checks applied the **BF-conditional** formula b/(b+N−1) to the artifact's **uniform-spread** figures, conflating two quantities the artifact explicitly distinguishes by a ~900× gap (9.1% vs 0.0100% at b = 1000, N = 10⁴ — a measured ratio of 909.2×);
- one check compared the existence-vs-identification difficulty ratio against N/2 instead of N − 1;
- the separability-type counter collected every observation *entailed* by any family rather than only the ones that *separate a pair*;
- six Duhem checks asserted 1/(k+1), which is the fault-**site** convention, against a brute-force enumeration that computes the fault-**world** convention 2ᵏ/(2ᵏ⁺¹ − 1).

After correction, all checks pass. The corrections changed the script's conventions only; no number in the taxonomy or in this document was altered by the audit.

## Limitations (stated plainly)

1. **C1 inherits its regime dependence.** Regime A's 0/28 is a consequence of the taxonomy's own [NT] tagging; a proponent who rejects that tagging for their tradition will reject Regime A's count. Regime B is the answer to that objection, and it is an *upper bound* on separability, not a neutral result.
2. **N is contested.** Every threshold in C2 scales with N; N = 10⁴ is the upper end of a commonly cited, individuation-dependent range (4,000–10,000+). The threshold figures should be quoted with their N.
3. **C3's conventions are not privileged.** The 0.25 / 0.5333 / 0.625 spread is a demonstration that the quantity is prior-driven, not a defence of any one of the three conventions.
4. **C1's single separating observation type is contested on both sides** — see §6.2 note 2 (auxiliaries carry a Bayesian cost) and §3.3 / §6.4 (hiddenness and evil are deliberately left unassigned in both directions).
5. **No external sources were obtained in this session.** Web search failed with an HTTP endpoint error for the whole session; every figure here is computed from stated formulas and the artifact's own taxonomy, not drawn from external literature. The Part 7 citation-verification backlog remains blocked on tooling, not on the argument.
6. **This document assigns no probability to any god's existence and asserts no verdict on any religion.** It reports how much evidence *could* in principle discriminate, and what the evidence available does and does not discriminate between.
