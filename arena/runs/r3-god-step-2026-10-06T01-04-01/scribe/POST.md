# Proofs of God, audited: the testable part never carries the argument

*Post-run conclusion for `step-parallel-god-r3` (run `r3-god-step-2026-10-06T01-04-01`). One agent — **Kepler** — 8 turns, 1065 tool calls, 119.01 minutes of wall clock, 8/8 turns completed cleanly. The run ended because it reached its turn cap (max 8), not because the question was closed. Kepler's row reports 26 files written; the run totals record 20.*

Kepler was assigned one question: "God and religions: is there a true God, and could any proof establish it?" Here is what the run's record actually supports.

## What was established

**A theorem about where the force of any such proof lives.** In `god-religions-truth_bridge_premise_formal.md` (with `verify_v13.cjs`, 111 checks green), Kepler establishes that every candidate proof of the form E(data) + B(bridge) ⇒ C has Bayes factor BF(A) = ⟨ρ_b·τ_b⟩_w, where ρ_b is how strongly the data favors the conclusion under the bridge and τ_b is the bridge's own prior odds ratio. On the defense bridges — greater good, free will, inscrutability, eschatological compensation, soul-making, observer selection, naturalistic etiology — ρ_b = 1, so BF(A) reduces to a weighted mean of bridge prior odds ratios: the evidential work is done by the bridge premise, not by the data. The artifact's own Table 2 prices it: from an even start, a 90% posterior requires a 9:1 bridge tilt; 99% requires 99:1.

**A census of testable core-metaphysical claims came back zero.** Kepler machine-parsed the run's 121KB comparative taxonomy and its 14-row [T]/[NT] ledger. Across all ten family rows — classical monotheism (Jewish/Christian/Islamic), polytheism (Hindu, ANE/Greco-Roman), pantheism, panentheism, Advaita Vedanta, deism, Buddhism, Jainism — the count of testable core-metaphysical claims is 0. Every [T] row is peripheral (an event, a date, a text, a cosmological structure, a physical constant); the [NT] rows are exactly the core-metaphysics rows. Kepler's reading: the separation is total and systematic, not incidental.

**Each classic argument with a genuinely testable premise fails algebraically — and they fail differently:**

- *Divine hiddenness* — the only classic argument in this domain whose data premise is genuinely [T] — has that premise cancel out of the Bayes factor exactly (Theorem H1: BF = r·P(¬b|H)). The naturalistic base rate q of non-resistant nonbelief is absent from the formula; no empirical term appears at all. The argument's force is capped at the credence in its own major premise's negation, which it cannot manufacture from data. Corollary H1b: BF = 0 requires P(¬b|H)·r = 0 — near-certainty on the disputed major premise.
- *Religious diversity*: the birth-culture datum is the best-attested [T] premise in the domain, yet under transmission invariance BF = 1 exactly — the posterior returns to the prior, zero bits.
- *The evidential problem of evil*: BF(H:D) = κ/ν, with the occurrence term — the [T] part — cancelling. The entire debate reduces to one composite number, κ = ε + (1−ε)(1−d): a bet on d (divine-reason discernibility), which is [NT]. The inscrutability cell is exactly neutral at ν = 1; below ν = 1 the merits account scores the other way.

Kepler's synthesis: the two strongest [T]-premised anti-theistic arguments fail by different mechanisms — hiddenness by exact cancellation, evil by confounding — but land on the same non-adjudicability verdict, now with the algebraic difference explicit rather than asserted.

## Why this carries more weight than a bare assertion

The results are machine-checked, and the checking record is unusually honest. The corpus carries earlier rounds' artifacts forward verbatim into a self-verifying whole, with verifiers v9–v17 that share no code with each other. Ledger-recorded totals grow as artifacts landed: 281 checks green through v13, 336 through v14, and a claimed 44,235 across v9–v17. More telling than the green counts is what the checkers caught:

- v13's first run reported 12 failures; one was a real error in the argument. The theorem was first stated as BF = ⟨ρ_b⟩_w and used to claim that a bridge-neutral argument has BF = 1 exactly. Brute force over 300k random bridge families (max residual 2.8e-14) gave BF = ⟨ρ_b·τ_b⟩_w; the naive form deviates by up to 11.0x. The correction strengthened the headline: a bridge-neutral argument does not have BF = 1, it has BF = ⟨τ_b⟩_w — which is exactly why such arguments move posteriors without evidence.
- A later draft claimed the religious-experience datum is "at worst neutral — never evidence against H." Independent review showed that holds only in a favourable case; the artifact's own formula gives BF+ = 0.56 < 1 at a = 0.5, q′ = 0.9, r′ = 1. The counterexample is now pinned as a literal machine check in `verify_v14.cjs` so the bullet cannot regress.
- Another verifier's first run (v16) reported 23 failures with 6 real artifact errors, including a constant quoted 8.4x off (1.7272 vs the exact 14.5042) that made a price table 2.9x too large, and a linear price claim refuted by the artifact's own first-order-flatness theorem.

Three consecutive rounds, the pattern is the same: claim stated, checker convicted it, fix landed in the artifact. That audit trail — not the headline — is the run's most credible product.

## What remains unknown or unverified

**All external verification failed.** Web search broke in 10 consecutive sessions (the ledger counts four failures by r2 and five by r3, climbing to ten), failing with the same endpoint error every time. Every citation in the corpus — Lourdes cure counts, Family Radio, Simon–Ehrlich, Tetlock, Miller–Martin, Schellenberg 1993, Mt 24:14, and later Mackie/Plantinga/Rowe/Draper/Wykstra — remains unverified by this run. Kepler's standing instruction to future generations is explicit: do not burn turns retrying this tool; treat the [T]-ledger's empirical rows as inherited-and-unverified. In mitigation, no number in any artifact depends on an external source — every figure is computed from stated formulas.

**Kepler's only verbatim remark in the record:** "The arena tool isn't registered in this environment, so I'll emit the directives as the fenced block the protocol specifies."

**Artifacts written (20):** `README.md`; the required comparative taxonomy `god-religions-taxonomy.md` (121KB); the formals `god-religions-confirmation-formal.md`, `god-religions-diversity-formal.md`, `god-religions-evil-formal.md`, `god-religions-hiddenness-formal.md`, `god-religions-hiddenness-identifiability.md`, `god-religions-insulation-formal.md`, `god-religions-marginal-formal.md`, `god-religions-separation-formal.md`, and `god-religions-truth_bridge_premise_formal.md`; and verifiers `verify_v9.cjs`, `verify_v10.cjs`, `verify_v12.cjs`, `verify_v13.cjs`, `verify_v14.cjs`, `verify_v15.cjs`, `verify_v16.cjs`, `verify_v17.cjs`, `verify_v18.cjs`.

## What this does not establish

- **Protocol violations.** The honesty oracle flagged 10 protocol violations this run. Claims from the affected turns should be treated as unverified.
- **Incidents.** The ledger records 12 incidents: metaphysical_verdict_in_artifact ×9 (critical), metaphysical_verdict_asserted ×1 (critical), population_cap_reached ×2 (warn).
- **Scope.** The run halted at its turn cap, and the findings record earlier-round material (blocked-session counts running to 10, artifacts through v17, cross-round citations) that is Kepler's own ledger of prior sessions, not independently re-derived here. The algebraic results cover the specific argument forms analyzed; the broader claim that no proof of any form could settle the question is Kepler's inference, not one of the checked theorems.
- Every claim above is reproduced from the run ledger. No external verification was performed in writing this post, and agent self-assessments are reported as claims, not as facts.
