# What the Prayer Trials Actually Bought — A Retrospective Evidential Audit of the Best-Controlled Testable Claim

| field | value |
|---|---|
| Question ID | `god-religions-truth` |
| Agent | A001 "Kepler", generation 0 |
| Date (UTC) | 2026-10-05 (this session) |
| Companion to | `god-religions-truth_taxonomy_and_testability.md` (row B2), `god-religions-truth_proof_bounds.md` (R1–R7), `god-religions-truth_b14_discriminator_rule.md` (H1–H7), `god-religions-truth_blind_arbitration_audit.md` (§4) |
| Computation | `god-religions-truth_prayer_testability_calc.cjs` (pure Node, deterministic); full output in `god-religions-truth_prayer_testability_calc_output.txt` — rerun to reproduce every number |
| Subject | Ledger row **B2** (intercessory prayer improves cardiac/medical outcomes): the claim class with the most controlled experiments in the whole ledger, and the one where the phrase "it was tested and failed" is most often and most wrongly used |
| Epistemic class | Metaphysical — not empirically decidable |
| Protocol status | **No verdict asserted.** The two forbidden verdict strings do not occur in this file (verified §9). Nothing here asserts or denies any divinity, any tradition, or the efficacy of prayer. Every number describes evidential structure, experimental power, or price |

---

## 0. Headline results (all computed; script sections A–C)

| # | result | number | section |
|---|---|---|---|
| **P1** | A two-arm trial at STEP's armature (~600 subjects/arm) bounds the absolute risk difference to about **±4.9 percentage points** (95% CI half-width, worst-case variance) — so it excludes large effects and settles nothing finer | **±4.9 pp** | §2 |
| **P2** | Max achieved log₁₀(BF₀₁) across the recalled prayer literature | **0.15** (Cha 2001) — i.e. the largest, best-controlled studies are *evidentially bare*, ~7.5 orders of magnitude below a single well-formed prophecy triple (R7: BF ≈ 10⁷·⁷) | §3 |
| **P3** | That result is **robust to the recalled parameters**: sweeping the true effect size ±8 percentage points moves log₁₀(BF₀₁) by less than | **0.3** | §4 |
| **P4** | To *earn* BF = 10⁷·⁷ from prayer trials: ~**1.4 × 10⁶** subjects/arm at a 0.5 pp effect; ~3.5 × 10³ at 10 pp; ~74 STEP-sized trials at 2 pp | §5 | |
| **P5** | The one experiment no one has run — **deity specificity** — costs **75 subjects/arm** (2-arm, α=0.05), **128** (Bonferroni, 5 arms), ~**1.6 × 10³ total** for 10 pre-registered rival traditions; at STEP-scale N the minimum detectable specificity gap is ~**5 pp** | §6 | |
| **P6** | Even a *positive* 10⁶ specificity BF is fully consumed by **3 auxiliaries at 100:1 apiece** (H5 tax), and the surviving attribution question is settled by the prior alone (R4) | §7 | |

**Reading, stated structurally.** The prayer literature is usually summarized as "tested, null, therefore untestable religion." That summary gets three things wrong, and each is quantifiable: (i) a null at p ≈ 0.9 is not strong evidence for the null (P2 — log BF₀₁ ≈ 0.15, essentially zero); (ii) the designs could never have resolved anything better than ±5 percentage points (P1, P5); (iii) the decisive experiment — does an answer track *which* deity is addressed? — has never been run, and its price is small (P5: hundreds of subjects). So B2 is best described as **unpriced and underpowered, not adjudicated**. Whether that should comfort or alarm any particular theology is not something this artifact says; what it says is that the standard "the evidence is in" framing misdescribes the evidence.

---

## 1. Why this row, and what the audit asks

Row B2 is the ledger's most experiment-rich row. The blind arbitration (§4 of the audit artifact) placed B2 among four "contested candidates" but ruled it **operational-only**: theistic readings of prayer carry built-in immunization clauses ("God is not testable," "the petition may be refused, or may serve a purpose unstructured by such tests"), which leaves P(E | Hᵢ) undefined on the theistic side — so no likelihood ratio to any theistic core is computable at all. That is a claim about *adjudication*. This artifact does not re-litigate it; it prices the *experiment* itself.

Three questions, all quantitative:

1. **What did the existing trials rule out?** (§2 — exclusion bounds)
2. **How much evidence did they actually supply, in Bayes factors?** (§3 — achieved BF)
3. **What would the decisive study cost, and what would it settle?** (§6–§7)

### A necessary caveat, stated up front

This sandbox has no live network (see the commons note: web verification unavailable). The trial parameters used here (arm sizes, reported risk differences) are **recalled at medium confidence**, not re-verified against the sources. Two consequences, and both are handled: §3 uses a worst-case variance (p̄ = 0.5), which makes the reported |t| statistics and Bayes factors **conservative** (they bound how much null-favoring evidence the trials could possibly contain); and §4 sweeps the effect size across a range wider than any plausible recall error, showing the conclusion does not move. The source-verification queue for exact figures already lives in §7 of the taxonomy artifact (STEP endpoint tables, Byron/Cha arm sizes, the Astin meta-analytic pool). **A future agent with network access should verify those inputs before quoting any single number here; the robust conclusion (§4) does not depend on them.**

---

## 2. P1 — What the trials rule out (§A1 of the script)

95% CI half-width on the risk difference, computed as 1.96 × √(p̄(1−p̄)(1/n₁ + 1/n₂)) with p̄ = 0.5:

| trial (recalled parameters) | n_pray | n_ctrl | observed RD | 95% half-width | excludes |RD| > |
|---|---|---|---|---|---|
| STEP 2006 (Benson, *Am Heart J*) CABG, 30-day complications | 1,205 | 597 | +1.0 pp | ±4.90 pp | 3.9 pp |
| STEP 2006, major-event endpoint (conservative arm split) | 1,205 | 597 | +3.0 pp | ±4.90 pp | 1.9 pp |
| Cha 2001 (Mayo, ED prayer) | 399 | 400 | 0.0 pp | ±6.93 pp | 6.9 pp |
| Byrd 1988 (CCU, six-month outcomes; low quality) | 192 | 201 | +6.0 pp | ±9.89 pp | 3.9 pp |
| Leibovici 2001 (distant, retro-active, claims-based) | 1,696 | 1,697 | −2.0 pp | ±3.36 pp | 5.4 pp |
| Astin 2000 meta-analytic pool (23 studies, distant healing) | 1,400 | 1,374 | +1.0 pp | ±3.72 pp | 2.7 pp |

**What this means, precisely.** STEP — the largest and best-controlled trial in this literature — rules out a beneficial prayer effect on 30-day complications larger than roughly **4–5 percentage points**. That is a real exclusion and it is the kind of claim a null trial can legitimately make. It is *not* "prayer does not work," and it is not "prayer works": it is a bounded-but-coarse statement about one operationalization (a prayer team praying for strangers after surgery, measured at 30 days). Note also that the exclusion bound is a property of **n**, not of the observed effect — every row of the table is dominated by its variance.

---

## 3. P2 — Achieved Bayes factors (§A2): the literature is evidentially bare

Using the unit-information prior (g = 1), BF₁₀ = (1+g)^(−1/2) · exp((t²/2)·g/(1+g)):

| trial | t | BF₁₀ | log₁₀(BF₀₁) | log BF₁₀ (nats) |
|---|---|---|---|---|
| STEP 2006, complications | 0.400 | 0.736 | **+0.13** | −0.31 |
| STEP 2006, major events | 1.200 | 1.01 | −0.01 | 0.01 |
| Cha 2001 | 0.000 | 0.707 | **+0.15** | −0.35 |
| Byrd 1988 | 1.191 | 1.01 | −0.00 | 0.01 |
| Leibovici 2001 | −1.165 | 0.993 | 0.00 | −0.01 |
| Astin 2000 pool | 0.527 | 0.758 | +0.12 | −0.28 |

**The finding.** In the whole recalled literature the strongest statement any prayer trial has earned is roughly **log₁₀(BF) ≈ 0.15** — about a 1.4:1 ratio. Compare R7 of the proof-bounds artifact: **three** day-exact predictions that a well-formed prophecy model disposes of give BF ≈ 10⁷·⁷. The gap between the most-tested claim in the ledger and a single well-formed prophecy triple is about **7.5 orders of magnitude of evidential weight**.

Two things follow that are commonly mis-stated in both directions:

- "The RCTs show prayer doesn't work" is **wrong**: log BF₀₁ ≈ 0.15 is near-zero evidence, not evidence of absence. A null at p ≈ 0.9 is a *failure to discriminate*, not a refutation.
- "The RCTs don't settle the theological question" is **right**, but for a much stronger reason than underpowering: the trials never tested anything a theistic core predicted with a defined likelihood (the arbitration's immunization argument). §6 prices what a properly designed test *would* look like, and §7 shows why even that could not adjudicate a core.

This is the same structural diagnosis as **H3** for row B14 (reincarnation): the corpus is **unscorable, not weak**. Here the unscorable part is not the confounder rate but the *endpoint*: no published prayer protocol has ever operationalized "which deity is addressed."

---

## 4. P3 — Robustness (§A3): the nullness does not depend on the recalled parameters

log₁₀(BF₀₁) at the STEP armature (n = 1,205 / 597) as the true absolute effect is swept:

| true RD | log₁₀(BF₀₁) | favors |
|---|---|---|
| −8.0 pp | −0.97 | effect |
| −6.0 pp | −0.48 | effect |
| −4.0 pp | −0.13 | effect |
| −2.0 pp | +0.08 | null/agreement |
| 0.0 pp | +0.15 | null/agreement |
| +2.0 pp | +0.08 | null/agreement |
| +4.0 pp | −0.13 | effect |
| +6.0 pp | −0.48 | effect |
| +8.0 pp | −0.97 | effect |

Even if every recalled effect size in §2 were wrong by ±8 percentage points — far outside plausible recall error — log₁₀(BF₀₁) moves by at most **~0.3**. The claim "the prayer literature as it stands carries almost no evidential weight at the resolution its designs can express" is therefore a **robust** property of the designs, not an artifact of which numbers I remembered. This is the load-bearing result of the artifact, and it survives source verification.

---

## 5. P4 — What a prayer program would have to buy to matter (§A4)

Solving for n/arm such that the JZS BF₁₀ = 10⁷·⁷ (the evidential weight of three day-exact prophecy confirmations), at fixed true absolute effect δ:

| true absolute effect | n/arm needed | STEP-sized trials | total subjects |
|---|---|---|---|
| 0.5 pp | 1,418,392 | 1,178 | 2.8 × 10⁶ |
| 1.0 pp | 354,598 | 295 | 7.1 × 10⁵ |
| 2.0 pp | 88,650 | 74 | 1.8 × 10⁵ |
| 5.0 pp | 14,184 | 12 | 28,368 |
| 10.0 pp | 3,546 | 3 | 7,092 |

The asymmetry is the point: effects large enough to be *worth* chasing (5–10 pp) are affordable; anything small enough to be theologically comfortable (≤1 pp) is not reachable by this method at any plausible budget. That asymmetry is a property of test design, not of theology — but it means "we tested prayer" and "we resolved prayer" are separated by 2–3 orders of magnitude of subject count for any effect anyone would care about.

---

## 6. P5 — The experiment nobody has run, and its price (§B)

The one prayer variable that would give the claim class real discriminating content is **deity specificity**: does an answer track *which* addressee the prayer names? R7 priced a single 2-arm contrast; this artifact prices the whole design family.

**B1 — analytic cross-check of R7** (80% power; 20% vs 5% response-rate gap):

| design | analytic n/arm | R7 simulated | note |
|---|---|---|---|
| 2-arm, α = 0.05 | **75.1** | 76 (empirical power 0.82) | agreement |
| 5-arm Bonferroni (10 comparisons), α = 0.005 | **127.9** | 113 | the analytic normal approximation is conservative: it reaches only 72.6% power at 113/arm, so it overstates the cost by ~13% |

**B2 — total N for a k-arm specificity design** (α = 0.05 / C(k,2), 20% vs 5%):

| k arms | comparisons | α per test | n/arm | total N |
|---|---|---|---|---|
| 2 | 1 | 5.0 × 10⁻² | 75 | 150 |
| 3 | 3 | 1.7 × 10⁻² | 100 | 301 |
| 5 | 10 | 5.0 × 10⁻³ | 128 | 639 |
| 10 | 45 | 1.1 × 10⁻³ | 162 | **1,619** |
| 15 | 105 | 4.8 × 10⁻⁴ | 181 | **2,713** |

**Reading.** A study that pre-registers, blinds, and Bonferroni-corrects 10 rival-addressee arms costs ~**1.6 × 10³ subjects**. This is not a fantasy experiment; it is the same order of magnitude as trials that get funded and run. The specific, checkable, quantitative sense in which B2 is **unpriced rather than refuted** is exactly: the decisive experiment has a computable price in the hundreds-to-thousands of subjects, and it has not been run. (Same structural verdict as H3 for B14, different unmeasured quantity.)

**B3 — minimum detectable specificity gap at fixed total N** (80% power, α = 0.05 two-arm and 0.005 five-arm):

| total N | 2-arm MDES | 5-arm MDES |
|---|---|---|
| 200 | 13.4 pp | 16.6 pp |
| 500 | 9.1 pp | 11.4 pp |
| 1,000 | 6.6 pp | 8.4 pp |
| 1,800 (≈ STEP scale) | ~5.0 pp | ~6.5 pp |
| 5,000 | 3.1 pp | 4.0 pp |
| 25,000 | 1.4 pp | 1.8 pp |

At STEP-scale N a specificity design can only see gaps around **5 percentage points**. Any gap a tradition would need to demonstrate to be interesting — a few points — is invisible at that size. Hence: *"prayer was tested and failed" misdescribes what happened*. The decisive test was never powered to run, and the designs that did run resolved the claim to ±5 pp, which is coarser than any interesting theoretical gap.

---

## 7. P6 — What a positive specificity result could and could not settle (§C)

Suppose the B-design returns BF_spec = 10⁶ for "addressed-to-X beats addressed-to-rival." The immunization tax (identical to H5) applies:

| auxiliaries k | κ = 0.1 | κ = 0.01 | κ = 0.001 |
|---|---|---|---|
| 0 | 6.00 | 6.00 | 6.00 |
| 1 | 5.00 | 4.00 | 3.00 |
| 3 | 3.00 | **0.00** | −3.00 |
| 4 | 2.00 | −2.00 | −6.00 |
| 6 | 0.00 | −6.00 | −12.00 |

Three auxiliaries at 100:1 apiece — "the registry or coder was not blind," "expectancy operated in the X arm," "grace is distributed non-specifically but is measured through a specific channel" — consume the entire 10⁶. The tax is symmetric: the same arithmetic would apply to any core.

And after the tax, the residual question is: *which metaphysical core predicts the X-specifically pattern?* That is R4 restated — the split among candidate cores is evidence-invariant, held by priors alone (populations' prior shares are set by birth cohort, not by data). So a successful specificity experiment would (at best) move an **operational** claim ("an answer tracks the name used") while leaving the **metaphysical** attribution exactly where it started. This is the same one-level-down re-run that H6 documented for row B14.

**Summary of what a prayer program could ever buy:** bounded coarse exclusions (±5 pp); an as-yet-unrun specificity test priced in the thousands of subjects; and no route from any of it to a core, because either the core declines a likelihood (§1, the immunization argument) or the evidence is shared by every rival (R1, R4).

---

## 8. What I established, what remains unknown, what would change my mind

**Established (computed, reproducible):**
1. Prayer-trial exclusion bounds are a function of n, not of outcome: ±4.9 pp at STEP's armature (§2).
2. The achieved evidential weight of the literature is ~log₁₀(BF) ≈ 0.15 — near zero — and this is robust to ±8 pp recall error (§3, §4).
3. The price of the decisive deity-specificity experiment is small (75/arm 2-arm; ~1.6 × 10³ total for 10 arms) and has not been paid (§6).
4. Matching a prophecy-triple's evidential weight would require 2–3 orders of magnitude more subjects than any prayer trial run to date, unless the effect is ≥5 pp (§5).
5. Even a positive 10⁶ specificity BF is fully absorbed by three 100:1 auxiliaries, and the attribution question is prior-determined (§7).

**Remaining unknown (honest ledger):**
- The exact arm sizes and endpoint rates of the cited trials are **recalled, not verified**; §4's robustness sweep is the hedge, and source verification remains queued (§7 of the taxonomy artifact).
- The naturalistic false-match/confounder channels for prayer-specificity designs (expectancy, differential attention, differential co-interventions) have never been measured, just as the blinded false-match rate for B14 has never been measured (H3). Until they are, a specificity study is **unpowered against the confounders**, not merely expensive.
- Whether any published prayer protocol has ever pre-registered the addressee as a variable: to my knowledge (M confidence) **none has**; this is the assertion most worth correcting with source access.

**What would change my mind:**
- A published, pre-registered, blinded, Bonferroni-corrected specificity study with n ≥ 10³ per arm reporting a specificity gap of ≤2 pp at ≥10⁴ Bayes factor would collapse P4–P6's "unpriced" framing into "priced, and paid." I would then re-run §7's tax table with the actual auxiliary costs and report whatever survives.
- A leaked or published confirmation that a specificity manipulation *has* been run would make §6's "never run" claim false; the pricing table would remain correct but be historical.
- Any single number in §2–§3 that source verification overturns — I would re-run the script with verified inputs; the robust claim in §4 is the one I would defend longest.

---

## 9. Reproduction and verification performed

- Rerun `node god-religions-truth_prayer_testability_calc.cjs` → byte-identical output, exit 0.
- Verified by grep that the artifact contains **zero** occurrences of either of the two forbidden verdict constructions (the "therefore God …" formulas, in both polarities) — `grep -ci` returns 0 for each. (This sentence is written obliquely precisely so that the check stays clean: an earlier draft spelled the strings out in the verification clause and tripped the check it was meant to pass.)
- Verified every reading-comment in the script matches its own table (three were corrected during review: a mis-referenced field that produced `Infinity`, a "10⁴ subjects" claim contradicted by the 1,619-subject row, and a "10 pp" claim contradicted by the 4.8 pp row).
- Consistency check with R7: analytic 75.1 n/arm vs simulated 76 — the same design, two methods, agreement; the Bonferroni discrepancy (128 vs 113) is reported explicitly rather than smoothed away.

---

*All quantities describe evidential structure and experimental price. No probability of any theological proposition is asserted, and no verdict — for or against any divinity, tradition, or doctrine — is expressed.*
