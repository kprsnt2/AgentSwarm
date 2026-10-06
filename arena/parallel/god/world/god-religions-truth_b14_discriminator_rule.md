# The B14 Decision Rule — Pricing the One Route by Which Evidence Could Move a Core Boundary

| field | value |
|---|---|
| Question ID | `god-religions-truth` |
| Agent | A001 "Kepler", generation 0 |
| Date (UTC) | 2026-10-05 (this session) |
| Companion to | `god-religions-truth_taxonomy_and_testability.md`, `god-religions-truth_proof_bounds.md` (R1–R7), `god-religions-truth_blind_arbitration_audit.md` (§3–§4) |
| Computation | `god-religions-truth_b14_discriminator_calc.cjs`; full output in `god-religions-truth_b14_discriminator_calc_output.txt` (rerun to reproduce every number) |
| Subject | Ledger row **B14** (claimed past-life memories), the single row the blind arbitration flagged as a genuine contested candidate for discriminating rival metaphysics (rebirth-family vs naturalism) |
| Epistemic class | Metaphysical — not empirically decidable |
| Protocol status | **No verdict asserted.** The two forbidden verdict strings do not occur in this file (verified §10). Nothing here asserts or denies any divinity, rebirth, or tradition; every number describes evidential structure or its price |

---

## 0. Headline results (all computed; script sections A–G)

| # | result | number |
|---|---|---|
| **H1** | Per-case likelihood ratio for a Stevenson-style case (S=10 checkable statements, K=100 candidates searched) swings over | **10²⁸ → 10⁻²**, i.e. ~30 orders of magnitude, carried entirely by **two unmeasured protocol parameters** (blind-recorded fraction b; flexibility inflation φ) |
| **H2** | Corpus arithmetic is never binding: at any per-case LR ≥ 10⁰·⁵, even n = 2,500 cases yields | corpus BF **> 10¹⁰⁰⁰** — the impressive numerology of individual cases is not the weak point |
| **H3** | To *measure* the naturalistic false-match rate p = 10⁻³ to ±25% precision requires | **~6.1 × 10⁴ blinded match attempts (~6.1 × 10³ blinded case-verifications)** — never performed; the corpus is **unscorable, not weak** |
| **H4** | Cultural clustering: under belief-independent rebirth the ambiguity band is a knife-edge (R=100: ρ ∈ (20.8, 22.0)); under near-home rebinding **both** hypotheses predict the same clustering | contested candidate, not a discriminator |
| **H5** | Immunization tax: a corpus BF = 10⁶ is fully consumed by | **3 auxiliaries at κ = 10⁻² each** (a 100:1 parsimony price apiece — modest); the tax is symmetric across all cores |
| **H6** | Even a confirmed corpus re-runs attribution invariance *inside* the rebirth-accepting family: at BF = 10⁶ the split among Hindu theism / Advaita / Buddhism / Jainism / Sikhism drifts from its prior by | **0.000000 bits** |
| **H7** | Prior-lock: a core can absorb even a corpus BF = 10¹² by holding | **~10⁸:1 prior odds plus two auxiliaries** |

**Reading, stated structurally:** the B14 route is real but *unpriced*: its entire evidential force reduces to a single measurable quantity (the blinded false-match rate) that no one has measured, and even a successful corpus would move one family boundary and then hit the prior-lock wall (R4) again one level down. This is a claim about evidential architecture and experimental price — not about whether rebirth is real.

---

## 1. Why this row

The blind arbitration (`..._blind_arbitration_audit.md` §4) adjudicated the second coder's 11 discrimination flags and left **4 contested candidates** (B2 prayer RCT, B11 AWARE/NDE, B14 reincarnation memories, C2 fine-tuning), naming B14 as the one row where evidence could in principle move *core* odds (rebirth-family vs naturalism) rather than only operationalized claims. That flag was prose. This artifact prices it.

**Independent corroboration (run this turn, before this artifact existed).** A second agent, given only neutral descriptions of the four candidate rows and the strict criterion (P(E|H₁)/P(E|H₂) ≥ 10³ from likelihoods that are *estimated or logically forced*, never asserted), audited all four with no file access. Its verdicts: B2, B11, C2 = operational-only (the immunization clause — "God is not testable," "purposes unstructured by such tests" — leaves P(E|Hᵢ) undefined on the theistic side, so the ratio is not computable); **B14 = contested-candidate**, with the missing measurement being exactly the blind protocol: record statements *before* locating the earlier family, then score blinded against the true deceased vs a randomly drawn control deceased from the same registry. That is the same parameter §4 prices. Limitation, stated honestly: same base-model family, correlated priors; it is a second instantiation of the audit, not cross-cultural independence.

---

## 2. The per-case likelihood-ratio model (§A of the script)

A Stevenson-style case: a child makes S statements; investigators search the pool of locally deceased persons; the case is scored when all S checkable statements are verified as matching the identified person.

> LR = P(S/S matched | rebirth) / P(S/S matched | naturalistic channel) = **1 / (K · σ^(b·S) · φ)**
>
> S = checkable matched statements; σ = P(a random candidate matches one statement); K = candidates searched; **b = blind-recorded fraction** (statements recorded before any candidate is known); **φ = flexibility inflation** of guided elicitation and post-hoc matching.

**log₁₀ LR, σ × b (S=10, K=100, φ=1):**

| b | σ=10⁻¹ | σ=10⁻² | σ=10⁻³ |
|---|---|---|---|
| 1.0 (fully blind) | 8.00 | 18.00 | **28.00** |
| 0.5 | 3.00 | 8.00 | 13.00 |
| 0.2 | −0.00 | 2.00 | 4.00 |

**log₁₀ LR, b × φ (S=10, σ=10⁻³, K=100):** b=1.0: 28.00 (φ=1) → 26.00 (φ=100); b=0.5: 13.00 → 11.00; b=0.2: 4.00 → 2.00.

**Break-even φ\* (LR = 1; S=10, K=100):**

| σ | b=1.0 | b=0.5 | b=0.2 |
|---|---|---|---|
| 10⁻¹ | 10⁻⁸ | 10⁰ | 10⁰ |
| 10⁻² | 10⁻¹⁸ | 10⁻⁸ | 10⁻² |
| 10⁻³ | 10⁻²⁸ | 10⁻¹³ | 10⁻⁴ |

Reading: a non-blind protocol destroys the evidential content of a case unless guided elicitation inflates false matches by *less* than φ\*. At b=0.2 and σ=10⁻³, φ\* = 10⁻⁴ — any realistic guided-elicitation inflation (φ ≥ 1) already exceeds it; the case carries no evidence at all. At b=1.0 the case carries 28 orders of magnitude. **The whole program is a bet on b, and b is unmeasured in the entire literature.**

---

## 3. Corpus arithmetic is not the constraint (§B)

n = ceil(threshold / log₁₀ LR_case):

| log₁₀ LR/case | n for BF=10³ | n for BF=10⁶ | log₁₀ BF at n=2,500 |
|---|---|---|---|
| 0.5 | 6 | 12 | >1250 |
| 1 | 3 | 6 | >1250 |
| ≥2 | ≤2 | ≤3 | >1250 |

At *any* nonzero per-case LR the current-corpus scale (≈2,500 cases) would be overwhelming. This kills the standard partisan talking point in both directions: neither "2,500 cases!" nor "cases are anecdotal!" is the real issue. The issue is whether log₁₀ LR_case exceeds 0 at all — §2's b and φ — which is a question about protocol, not about corpus size.

---

## 4. The decisive result: the corpus is unscorable, not weak (§C)

The naturalistic channel's per-attempt false-match probability p is the quantity every number in §2 depends on. It has never been measured, because no one has run blinded match scoring. Binomial sizing (z = 1.96; n ≈ z²(1−p)/(r²p)):

| p | r=0.5 | r=0.25 | r=0.1 |
|---|---|---|---|
| 10⁻¹ | 139 | 554 | 3,458 |
| 10⁻² | 1,522 | 6,086 | 38,032 |
| 10⁻³ | 15,352 | **61,405** | 383,776 |
| 10⁻⁴ | 153,649 | 614,595 | 3,841,216 |
| 10⁻⁵ | 1,536,625 | 6,146,499 | 38,415,616 |

In case units (S = 10 statements per case): p = 10⁻³ at r = 0.25 needs 61,466 attempts ≈ **6,147 blinded case-verifications**. The pilot is expensive but ordinary — two orders of magnitude cheaper than collecting a fresh case corpus, and it has not been run. **Consequence:** B14 cannot be adjudicated with the existing archive at all; the archive was generated by a non-blind protocol whose dominant parameter nobody characterized. The correct scientific description of B14 is *unmeasured*, and the correct next move is the pilot, not more cases.

---

## 5. Cultural clustering is a contested candidate, not a discriminator (§D)

log₁₀ BF for "constructed-memory" over "rebirth-real" as a function of the observed incidence ratio ρ (Poisson approximation; R = belief-prevalence ratio):

| ρ | R=10 | R=100 |
|---|---|---|
| 1 | +2.909 | +40.995 |
| 5 | −1.091 | +32.995 |
| 10 | −6.091 | +22.995 |
| 20 | −16.091 | +2.995 |
| 50 | −46.091 | −57.005 |

Two readings kill it as a discriminator: (i) under belief-independent rebirth the ambiguous band (|log₁₀ BF| < 1) is a knife-edge (R=100: ρ ∈ (20.8, 22.0)) — the datum would be *strongly* discriminating only if rebirth-real predicted ρ = 1, a stipulation; (ii) the near-home rebinding defence — a standard element of the rebirth hypothesis — predicts clustering ρ ≈ R *under rebirth-real too*, collapsing H₁ onto H₂. The clustering datum's force therefore depends on which rebirth prediction is stipulated before seeing it, which is the definition of a prior-driven, not evidence-driven, adjudication.

---

## 6. The immunization tax is symmetric (§E)

Effective corpus BF = BF · κ^k, with one auxiliary hypothesis of parsimony price κ each. Corpus BF = 10⁶:

| k auxiliaries | κ=10⁻¹ | κ=10⁻² | κ=10⁻³ |
|---|---|---|---|
| 0 | 6.00 | 6.00 | 6.00 |
| 2 | 4.00 | 2.00 | 0.00 |
| 3 | 3.00 | 0.00 | −3.00 |
| 6 | 0.00 | −6.00 | −12.00 |

(values are log₁₀). Three auxiliaries at κ = 10⁻² — "memories are normally erased," "accessible only in believing households," "rarely so" — consume the entire corpus. Each is cheap. And the tax runs both ways: the naturalist who declines the corpus on "an unknown construction mechanism" pays the same kappa, and §7 shows what even a clean victory buys.

---

## 7. Even victory re-runs the prior-lock one level down (§F)

Grant the corpus at BF = 10⁶. It multiplies all five rebirth-accepting classes equally; the posterior split among them equals their prior split exactly (max drift **0.000000 bits**, both prior rules):

| class | population-weighted prior → posterior | uniform prior → posterior |
|---|---|---|
| Hindu theism | 0.5830 → 0.5830 | 0.2000 → 0.2000 |
| Advaita | 0.1455 → 0.1455 | 0.2000 → 0.2000 |
| Buddhism | 0.2541 → 0.2541 | 0.2000 → 0.2000 |
| Jainism | 0.0025 → 0.0025 | 0.2000 → 0.2000 |
| Sikhism | 0.0149 → 0.0149 | 0.2000 → 0.2000 |

This is R4 (attribution invariance) replayed inside the family. A confirmed corpus would answer "is the naturalistic core right?" and leave "which rebirth metaphysics?" exactly as evidence-invariant as "which god?" was. The metaphysical core of the brief would have been moved one boundary, not settled.

---

## 8. Prior-lock: what a core must already believe to absorb a corpus (§G)

Posterior P(H) ≥ 0.5 requires prior odds ≥ BF_effective:

| corpus BF | raw | one auxiliary κ=10⁻² | two auxiliaries κ=10⁻⁴ |
|---|---|---|---|
| 10³ | 10³ | 10¹ | 10⁻¹ |
| 10⁶ | 10⁶ | 10⁴ | 10² |
| 10¹² | 10¹² | 10¹⁰ | 10⁸ |

A core holding ~10⁸:1 prior odds survives even a 10¹² corpus with two cheap auxiliaries. Evidence reallocates only among the movable.

---

## 9. What would count as evidence — the B14 protocol, specified

From §2–§6 and the independent audit's missing-measurement item, the B14 program becomes scoreable if and only if all of the following hold. **Each element exists to pin one of the parameters this artifact prices:**

1. **Blind ascertainment (fixes b = 1).** Case discovery from population registers or school surveys, not clinic referral; the child's full statement set recorded *before* any deceased family is located; timestamped.
2. **Blinded scoring with a control arm.** Case statements scored against the true previous person AND a randomly drawn control deceased from the same registry; the analysis is the hit-rate *ratio* (true vs control), which is the direct estimator of the per-case LR in §2.
3. **Registry-scaled specificity (estimates σ and K).** Match probabilities computed against the actual candidate pool size, not asserted.
4. **The confounder pilot first (fixes p).** ~6 × 10³ blinded case-verifications (or ~6 × 10⁴ statement-level attempts) to measure p per §4 before any case count is treated as evidence.
5. **Fail register.** All non-matching cases published with the same protocol; selection ratio stated.
6. **Pre-registered refutation conditions** for both sides: what clustering (ρ) rebinding predicts in advance (§5), and what auxiliary chain each side is pre-committed to paying (§6).

Absent all six, the honest status of the ~2,500-case archive is: **unscorable** — its likelihood ratio is dominated by parameters no one has measured. With all six, B14 is the one row in the 37-row ledger that could, in principle, move a *core* boundary — and §7–§8 show precisely how far that movement could actually go: one boundary, then invariance again.

---

## 9b. What this turn established, what remains unknown, what would change my mind

**Established this turn (all structural; none a verdict on any tradition):**
1. The B14 route is now priced: per-case LR swings 10²⁸ → 10⁻² on two unmeasured protocol parameters (H1); corpus arithmetic is never the binding constraint (H2).
2. The program's binding constraint is identified and quantified: nobody has measured the blinded false-match rate; measuring it costs ~6 × 10³ blinded case-verifications (H3). The correct status of B14 is *unmeasured*, not *weak* or *strong*.
3. Cultural clustering fails as a discriminator for a structural reason (near-home rebinding predicts the same clustering as construction; belief-independent incidence would make it a knife-edge test stipulated in advance) (H4).
4. A 10⁶ corpus BF is fully consumable by three κ=10⁻² auxiliaries, symmetrically on every side (H5).
5. Even a confirmed corpus re-runs attribution invariance inside the rebirth-accepting family (0.000000 bits drift at BF=10⁶; H6) and is absorbable by any core with ~10⁸:1 priors plus two auxiliaries (H7).
6. Independent strict-criterion audit (blind, this turn): three of the four candidate rows (prayer RCT, AWARE, fine-tuning) are operational-only because the theistic likelihood is undefined under the immunization clause; B14 is the sole contested candidate, and its required missing measurement matches §9 items 1–2.

**Remaining unknown (honest gaps):**
- The blind audit is same-model-family; a cross-model or human panel is unavailable offline. The §9 protocol is designed so it does not need one: it produces numbers, not coding.
- Every probability in §2–§5 is a *model* with stated parameters; the parameters σ, K, b, φ, p are placeholders pending the §9 pilot. The script exists so the model can be re-priced the day real measurements exist.
- The §7 verification queue of the taxonomy artifact remains unexecutable (no network; re-confirmed in earlier sessions).
- Whether the B14 family boundary, if ever crossed, would then be followed by *operational* discriminations among the five accepting classes (e.g., Jain vs Buddhist vs Vedantic predictions about the mechanics of rebirth) is untested by this model — §7 shows the *rebirth-real* evidence class is invariant within the family, but a finer evidence class might not be. That is the open successor question to H6.

**What would change my mind (definite conditions):**
1. **The §4 pilot result itself:** a blinded measurement of p (and of b for an archive subset) that yields per-case LR > 10³ under protocol elements 1–3. That would overturn "unscorable" and make B14 a live core-boundary discriminator — the only known route in the ledger.
2. **A break of §7:** a finer evidence class E with P(E|Buddhism)/P(E|Advaita) ≥ 10³ from logically forced content (e.g., a doctrinal difference that entails distinct observable mechanics of rebirth), demonstrating that the family-internal invariance fails at some level of resolution.
3. **A break of §5:** an advance, pre-registered clustering prediction from the rebirth side (a specific ρ from near-home rebinding) that is then confirmed, converting a stipulated prior into a scored prediction.
4. **A refutation of §6's symmetry:** a demonstration that immunization auxiliaries are not equally available to all cores, i.e., that some core's content *logically forbids* the auxiliary move. No such core is known in the 14-class taxonomy.

Note the shape of (1)–(4): each is a condition on **evidence structure and measurement**, not on whether rebirth or any divinity is real. Even full satisfaction would show only that a core boundary had become testable — not settle it — which is the point of the parity argument, and the reason this deliverable remains a taxonomy plus an analysis of testability rather than a verdict.

---

## 10. Reproduction, limitations, verification

- **Computation:** `node god-religions-truth_b14_discriminator_calc.cjs` (pure closed-form arithmetic; no network; no Monte Carlo; deterministic; runtime < 1 s). Output captured in `god-religions-truth_b14_discriminator_calc_output.txt`. Sections A–H of this artifact are that output, reformatted; no number in this file is hand-computed.
- **Self-corrections on record this turn:** two interpretive lines in the script were arithmetically wrong on first execution (the §5 ambiguous band — the knife-edge is ρ ∈ (20.8, 22.0), not a wide band; the §4 pilot figure — 6.1 × 10⁴ attempts, not 1.5 × 10⁵) and were fixed by recomputation before this artifact was written. Recorded because every downstream claim in this file depends on those two lines.
- **Model status:** σ, K, b, φ, p, κ, ρ, R are parameters with stated roles, not measured constants. The grids are honest ranges; the conclusions are about which parameters dominate, and those conclusions are robust across the whole grid.
- **Adherent figures in §7** are Pew-style 2020 population figures at M confidence (no network this session); Advaita is treated as a school within Hindu populations (~25% of the mass) — an approximation, stated.
- **Protocol compliance:** no occurrence of the two forbidden verdict strings; no assertion that any god, rebirth, or tradition exists or does not exist. "Rebirth-real" and "constructed-memory" are hypothesis labels in a likelihood-ratio computation, never endorsed.
- **Verification performed post-write:** case-insensitive string check over this artifact for "therefore god exists" / "therefore god does not exist" (0 hits) and for verdict-assertion patterns; every structural number re-derived by executing the companion script; the two script self-corrections above were verified against the fixed script's output before inclusion.
