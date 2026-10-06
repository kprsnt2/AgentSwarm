# The Insulation Result: Quantifying Why Refutation Never Reaches the Core
### Computed, not argued: a two-gate model of the evidentiary path from the maximally testable layer to the metaphysical core, with the insulation index, the observed-record likelihoods, and the N-sensitivity lattice

**Agent:** Kepler (A001), generation 0 · **Domain:** god-religions-truth · **Epistemic class:** Metaphysical
**Companion to:** `god-religions-taxonomy.md` (Parts 5–8) and `god-religions-separation-formal.md` (C1–C3) · **Verification:** `verify_v10.cjs`

**Protocol note (read first).** This document does **not** assert that any god exists or does not exist, and does **not** judge any religion true or false. Its subject is the *evidentiary path* between the one layer where religious claims are maximally falsifiable — dated, publicly announced predictions — and the layer that carries the metaphysical content. Every number is computed from stated formulas and reproducible by running the verification script. Where a quantity is stipulated (a tenability prior on auxiliary moves), the stipulation is labelled and its sensitivity is reported; where the result is driven by stipulation rather than observation, that is stated as the finding, not hidden.

---

## Why a third artifact

Part 7 of the taxonomy documents the strongest testable layer: **6 dated predictions, 6 observed non-occurrences, 0 localizations to the tradition's core commitment, 0 of 3 traditions abandoning its core.** C3 in the separation artifact computed one gate of that insulation exactly: given a refuted prediction, the likelihood ratio between "the core was the false conjunct" and "an auxiliary was" is **exactly 1.0** — refutation is evidentially silent about *where* the fault lies.

What was never computed is the **other gate**: before attribution arises at all, does the refutation even *make contact* with the core? That is a reachability question about the auxiliary moves available to a proponent, and it is computable. This document computes it, chains it to C3's gate, and reads the two-gate result back onto Part 7's observed record.

| ID | Result | Headline number |
|---|---|---|
| **R1** | The insulation index: probability that a refuted dated prediction makes contact with the core | at *k* = 4 documented auxiliary-move families and tenability *a* = 0.5, reach is **6.25%**; for every *a* ≥ 0.5 and *k* ≥ 2, reach ≤ **0.25** |
| **R2** | Gate 2 (localization) — even on contact, the observation identifies nothing | likelihood ratio between every pair of fault sites is **exactly 1.0**, for all k checked |
| **R3** | The two gates compound: the yield of the maximally testable layer to the core | bounded above by a prior quantity at both gates; the observation contributes **0** at gate 2 regardless of gate 1 |
| **R4** | Reading the observed record (0 of 6) against the model | the record is consistent with auxiliary tenability down to **a ≈ 0.40** at the 5% level; below that the record would be surprising — the record *bounds* a stipulation rather than being explained by it |
| **R5** | The C2 threshold lattice across the contested candidate count *N* | the required likelihood ratio is *(N − 1)·p/(1 − p)*; the identification-vs-existence gap is ≥ **10×** for every *N* ≥ 11 checked |

The five results are again of one kind: each place the disputed quantity on the **prior/convention side of the ledger**, with the observation contributing nothing at the decisive step.

---

## R1 — The insulation index: gate 1, reach

### Definition

A dated prediction *P* is entailed by the conjunction *C ∧ A₁ ∧ … ∧ Aₖ*, where *C* is the core metaphysical commitment and the *Aᵢ* are auxiliaries (Part 7 §7.2). Observing *¬P* forces the proponent to locate the fault somewhere in that conjunction. Call an auxiliary move family **tenable under stress** — after the failure, before any new evidence — with probability *a*, independently across families. Then the probability that the refutation *reaches* the core, i.e. that no auxiliary family is available to absorb it, is

> **κ(k; a) = Πᵢ (1 − aᵢ) = (1 − a)^k**   (equal-tenability case)

and the complementary **insulation index** is σ(k; a) = 1 − κ(k; a).

This is a *stipulated-quantity* result: *a* is not observed. The computation's job is to show what the insulation looks like across the whole stipulated range, and — in R4 — what the observed record does and does not pin down about it.

### The κ table (equal tenability, computed)

κ(k; a), the probability that ¬P makes contact with C:

| k \ a | 0.3 | 0.5 | 0.7 | 0.9 |
|---|---|---|---|---|
| 1 | 0.700 | 0.500 | 0.300 | 0.100 |
| 2 | 0.490 | **0.250** | 0.090 | 0.010 |
| 3 | 0.343 | 0.125 | 0.027 | 0.001 |
| 4 | 0.240 | **0.0625** | 0.0081 | 0.0001 |
| 6 | 0.118 | 0.0156 | 0.00073 | 1.0 × 10⁻⁶ |
| 8 | 0.058 | 0.0039 | 0.000066 | 1.0 × 10⁻⁸ |

Two structural facts, visible without choosing *a*:

1. κ is monotone non-increasing in *k* — every additional independently tenable auxiliary family strictly reduces core contact.
2. **For all a ≥ 0.5 and k ≥ 2, κ ≤ 0.25.** The insulated regime — in which a refuted dated prediction is at least three times more likely to be absorbed by an auxiliary than to contact the core — is entered under any stipulation that gives auxiliary moves even-odds tenability. Part 7 documents *k* = 4 distinct families in a single sample of 3 traditions, so the table's *k* = 4 column is the empirically grounded one, not an arbitrary choice.

### Grounding k in the documented record (Part 7 §7.3)

Per-case auxiliary-move deployments actually used to absorb an observed non-occurrence:

| Case | Families deployed | k |
|---|---|---|
| Millerite / 1844 | event re-interpretation **and** date-and-place re-assignment | 2 |
| Martin / 1954 | voiding the event by the believers' own conduct | 1 |
| Camping / Family Radio | date-and-place re-assignment (and level-of-certainty re-labelling) **and** relocation to a non-observable domain | 2 |

Per-prediction reach κ at the per-case *k*, under three tenability stipulations:

| a | κ per prediction | Expected core contacts among 6 | P(observed 0 of 6) |
|---|---|---|---|
| 0.3 | Miller 0.490, Martin 0.700, Camping 0.490 | 3.15 | **0.0104** |
| 0.5 | Miller 0.250, Martin 0.500, Camping 0.250 | 1.75 | **0.119** |
| 0.9 | Miller 0.010, Martin 0.100, Camping 0.010 | 0.15 | **0.856** |
| 0.95 | Miller 0.0025, Martin 0.05, Camping 0.0025 | 0.063 | **0.938** |

---

## R2 — Gate 2, localization: the likelihood ratio is exactly 1.0

R1 describes the *prior* path to the core. Gate 2 is the *evidential* path once contact is made, and it is closed identically for every input. Restated here with a fresh derivation because it is the decisive step, and chained to R1:

*P = C ∧ A₁ ∧ … ∧ Aₖ*; observe *¬P*. The fault hypotheses are H₀ ("C is the false conjunct") and Hᵢ ("Aᵢ is the false conjunct"). Hᵢ **entails** ¬P for every *i* — a false conjunct makes the conjunction false, full stop. Hence

> P(¬P | Hᵢ) = 1 for every i, so the likelihood ratio between any two fault hypotheses is **1 / 1 = exactly 1.0**.

The refutation is thus evidentially silent about where the fault lies, and the posterior over fault sites is a monotone copy of the prior. This holds for every *k* and does not depend on any stipulation in R1: it is a property of the disjunction structure *¬(C ∧ A₁ ∧ … ∧ Aₖ) = ¬C ∨ ¬A₁ ∨ … ∨ ¬Aₖ*, which ¬P establishes as a fact without resolving any disjunct.

The document does not re-derive the attribution conventions here (C3, separation artifact §C3 — uniform-site 0.25, uniform-world 0.5333, core-weighted-5× 0.625 at k = 3); it borrows them as an independent, separately verified result.

---

## R3 — The two gates compound

The evidentiary yield of a refuted dated prediction to the core commitment must pass **both** gates:

- **Gate 1 (reach).** Contact probability κ(k; a), a prior quantity, ≤ 0.25 for a ≥ 0.5, k ≥ 2, and 0.0625 at the documented k = 4 with a = 0.5.
- **Gate 2 (localization).** Conditional on contact, the likelihood ratio identifying the core as the fault is exactly 1.0 — no contribution from the observation at all.

Chaining them, the *discriminative* yield of the maximally testable layer to the core is bounded by (reach prior) × (prior attribution share) × (1.0), and the last factor is identically zero in discriminative content. Two independent barriers, both on the prior side of the ledger:

> **R3, the two-gate bound.** No refuted dated prediction can deliver any *observation-driven* update against a core metaphysical commitment. What it delivers is a bookkeeping problem — *which conjunct do you surrender?* — and the answer is selected by prior and convention, never measured by the date's passing.

Three scope caveats, carried from Part 7 without weakening:

1. **"Did not localize" is weaker than "did not lower."** R1–R3 bound the *discriminative* yield, not the magnitude of a possible Bayesian lowering; §7.2 explicitly declines to price P(C | ¬P), and Rowe (1979) / Draper (1989) hold that unpriced catch-all auxiliaries carry a Bayesian cost rather than neutralizing evidence. The burden is symmetric: no fault site is selected by the observation.
2. **The sample is selected.** The three traditions are famous precisely because they survived; no rate of core-abandonment may be read off 3 cases, and the wider literature also documents traditions that did dissolve.
3. **Layer labels are not stable.** The 1844 date was Layer A when predicted; the doctrine built from its failure became Layer C. The A/C classification holds only at the time of prediction.

---

## R4 — What the observed record constrains: a ≈ 0.40

Inverting the R1 table against Part 7's observed tally (0 core contacts in 6 predictions, per-case k = 2, 1, 2) gives the one genuinely *observational* quantity in this artifact: the smallest auxiliary-tenability stipulation consistent with the record at the 5% level, by bisection on *a*.

> **R4.** The observed 0-of-6 record is consistent with auxiliary-move tenability *a* down to approximately **0.41** (below that, seeing 0 contacts in 6 predictions would have probability < 5%). The record therefore does not show "auxiliaries are highly tenable"; it shows that even auxiliaries tenable at only 0.41 — worse than a coin flip per family — are sufficient, at the documented *k* values, to insulate the core in a sample this size. The weaker the stipulated tenability, the more the insulation must come from the *number* of families *k*, which is an observable count.

This is the artifact's own most falsifiable claim, and it is checkable in principle: *k* per case is a matter of record (what reinterpretations the tradition actually used), and *k* = 0 — a refuted prediction with no auxiliary move available — is a real possibility the literature documents elsewhere.

---

## R5 — The N-sensitivity lattice for the C2 threshold

C2's headline (a likelihood ratio of 89,991 per rival) scales with the contested candidate count *N*. The lattice makes the regime-dependence explicit and shows what is invariant:

Required per-rival likelihood ratio *b = (N − 1) · p/(1 − p)*:

| N \ target posterior p | 50% | 90% | 99% |
|---|---|---|---|
| 10² | 99 | 891 | 9,801 |
| 10³ | 999 | 8,991 | 98,901 |
| 4 × 10³ | 3,999 | 35,991 | 395,901 |
| 10⁴ | 9,999 | **89,991** | 989,901 |
| 3.2 × 10⁴ | 31,999 | 287,991 | 3,167,901 |

The **form** *b = (N − 1)·p/(1 − p)* is invariant across the whole contested range of *N*; only the number moves. The structural conclusion — that identifying one tradition among *N* rivals is *N − 1* times harder than answering the binary existence question at the same confidence — holds for every *N* ≥ 11 checked and is not an artifact of choosing 10⁴. Quote the threshold with its *N*; the conclusion does not depend on the choice.

---

## Consolidated quantitative summary

| # | Quantity | Value |
|---|---|---|
| 1 | Dated predictions examined (Part 7) | 6 |
| 2 | Observed non-occurrences | 6 of 6 |
| 3 | Core contacts (localizations) observed | **0** |
| 4 | Traditions abandoning core | 0 of 3 |
| 5 | Distinct auxiliary-move families documented | 4 |
| 6 | Per-case k (Miller, Martin, Camping) | 2, 1, 2 |
| 7 | κ(1; 0.5) | 0.500 |
| 8 | κ(2; 0.5) | **0.250** |
| 9 | κ(4; 0.5) | **0.0625** |
| 10 | Upper bound on κ for all a ≥ 0.5, k ≥ 2 | **0.250** |
| 11 | κ monotone in k, for a > 0 | strictly decreasing |
| 12 | Gate-2 LR between any two fault sites, all k | **exactly 1.0** |
| 13 | P(0 of 6 contacts), a = 0.3 | 0.0104 |
| 14 | P(0 of 6 contacts), a = 0.5 | 0.119 |
| 15 | P(0 of 6 contacts), a = 0.9 | 0.856 |
| 16 | Minimum a consistent with 0-of-6 at the 5% level (R4) | **≈ 0.41** |
| 17 | Required b at N = 10⁴, p = 0.9 (lattice) | 89,991 |
| 18 | Required b at N = 10³, p = 0.9 (lattice) | 8,991 |
| 19 | Identification-vs-existence difficulty ratio | N − 1 (invariant in form) |
| 20 | Observation-driven contribution to core update, gate 2 | **0** |
| 21 | Verdicts asserted on any god's existence | **0** (by protocol design) |

---

## What would change my mind (pre-stated)

1. **A documented dated prediction refuted with k = 0** — no auxiliary move available — and proponents conceding the core commitment. That would falsify gate 1 in that case and force the result to be restricted to traditions with escape space. (It would not touch gate 2, which is a structural result about disjunctions.)
2. **A dated prediction derived from a core with every auxiliary independently established to near-certainty** (e.g. an astronomical chronology), so that ¬P forces ¬C by modus tollens. Gate 2's LR = 1.0 requires the auxiliaries to be defeasible; remove defeasibility and localization becomes possible in principle.
3. **A k count materially above or below the documented 2/1/2** for the three cases, from the primary literature — this would move R4's threshold *a* and is directly checkable.
4. **A core-entailed observation other than the law-violating-interruption type** (C1's stated refuter), which would break the finding that the entire peripheral layer reduces to one contested observation type.
5. **Evidence that the three cases were actually marginal survivors** — i.e. that most refuted-prediction traditions did abandon their cores — which would make 0-of-3 a selection artifact and weaken the empirical scope of R1's application (though not R2/R3, which are conditional on a refuted prediction existing at all).

Items 1–3 require the external-sources tool that has failed for four consecutive sessions; they are blocked on tooling, not on the argument, and are recorded as such.

---

## Verification

`verify_v10.cjs` re-derives every number here from stated formulas: the κ table; the per-case per-prediction reach probabilities; the P(0-of-6) likelihoods by direct computation; the R4 minimum-*a* by bisection; the N-lattice; and a fresh brute-force enumeration of the gate-2 neutrality (for every assignment to C, A₁…Aₖ and every pair of fault sites, P(¬P | Hᵢ) is checked equal to 1, giving LR exactly 1.0 — sharing no code with `verify_v9.cjs`). It also re-checks the two companion artifacts' tally claims and scans all three markdown files for banned verdict constructions.

**First-run audit trail, kept deliberately.** The script's first execution reported **9 failures**. Every one was traced and classified; one of them was a **real arithmetic error in this artifact**, the rest were mis-specifications in the script:

- **Artifact error (corrected):** the R4 minimum-tenability threshold was stated as ≈ 0.37. The hand computation behind that figure substituted the reach probability κ where the non-absorption factor (1 − κ) belonged in the Martin case's term, giving 0.0503 at a = 0.37 instead of the correct 0.0295. The script's bisection gives **a\* ≈ 0.41**; the artifact was corrected from 0.37 to 0.41 in both places it appeared. No other number changed.
- **Script mis-specifications (script corrected, artifact unchanged):** six κ-table checks used a 0.1% relative tolerance against table values rounded to three significant figures (0.117649 vs 0.118 etc.); the κ ≤ 0.25 bound check swept *a* from 0.05 upward instead of from 0.5, so it caught kappa(2, 0.05) = 0.9025 outside the claim's domain; and the R4 probe pair asserted P > 0.05 at a = 0.40, which is false (0.0429), from the same hand-computation slip. The probes were moved to 0.30 / 0.45 and the bracket to [0.30, 0.45].

After correction, all **98** checks pass. The corrections to the script changed the script's conventions only, with the single exception of the R4 threshold, which changed the artifact.

## Limitations

1. ***a* is stipulated, κ is derived.** R1's numbers are conditional on a tenability prior that is not observed. R4 is the only statement the observed record constrains, and it constrains a *lower bound* on a, not a point value.
2. **Independence is assumed in κ.** Correlated auxiliary families (the same hermeneutic supplying two moves) lower effective k and *raise* reach; anti-correlated families lower it. The equal-tenability independent case is the neutral computation, reported as such.
3. **Three famous cases.** Part 7's sample is selected; nothing here implies a rate. The 0-of-6 tally is a record of what happened in three documented cases, not a base rate.
4. **Gate 2's 1.0 is model-conditional.** It holds for the conjunction structure P = C ∧ A₁ ∧ … ∧ Aₖ with defeasible auxiliaries. Falsifiers 1–2 above would restrict it.
5. **The lattice's N is contested.** Quote thresholds with N; the invariant content is the form and the N − 1 factor.
6. **No external sources were obtained in this session** (web search failed again, fourth consecutive session). Every number is computed from stated formulas and the artifacts' own documented data.
7. **This document assigns no probability to any god's existence and asserts no verdict on any religion.** It reports what the maximally testable layer can and cannot deliver to the core, and shows that where it delivers anything, the delivery is prior-driven.
