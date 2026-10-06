# god-religions-truth: the question is structurally resistant to proof, not evidentially starved

Run `god-step-2026-10-05T21-44-57` (phase `step-parallel-god`) ran 8 turns with a single agent, Kepler, investigating whether a true God exists and whether any proof could establish it. It ended because max turns were reached. Totals: 7/8 turns completed cleanly, 381 tool calls, 16 files written, 120.25 minutes of wall clock.

## What Kepler established

Kepler's central result is a negative result about *evidence*, not about God. The question resists proof not for lack of evidential strength, but because three structural features block discrimination. These are reported as established to the extent the run's own arithmetic is credible; the underlying scripts are reproducible per Kepler's claim.

- **Parity invariance.** Structural rivals — Kepler's example is a pair T and T' with identical observable consequences — share likelihoods exactly. Measured parity invariance is 0 nats; the required evidence for such a contrast is infinite.
- **Attribution invariance.** Among rival candidate agents, attribution of an observed effect is prior-determined and evidence-invariant: 0.000000 bits of drift at a Bayes factor of 10^6.
- **Diverging sample size at the apophatic limit.** The required sample size scales as n ∝ 1/δ². For conceptions of God defined by unobservability, δ → 0 and the evidence requirement diverges.

Strength was never the bottleneck. Kepler calculated that a 20% versus 5% deity-specificity contrast needs only 76 subjects per arm (simulated power 0.82; 113 per arm with 5-arm Bonferroni), and that three day-exact predictions yield a Bayes factor of roughly 10^7.7. The binding constraints are therefore **replication and attribution**, not power or sample size.

Against this backdrop, Kepler audited 37 testable religious claims across a taxonomy of 14 divine-conception classes. The asymmetry is total: confirmations land only on the mundane substrate (stelae, manuscripts, shoals); failures land only on claims that were already operationalized (prayer RCTs, dated predictions). Nothing in the 37-row ledger discriminates among live rival metaphysics — a tally of 0/37.

**The one live adversarial route was priced, and it is stuck on a single unmeasured quantity.** The B14 veridical-memory corpus, Kepler reports, hinges entirely on the blinded false-match rate. Per-case likelihood ratios swing from 10^28 to 10^-2 depending on two unmeasured parameters (blind fraction b, flexibility φ), while the corpus arithmetic itself never binds. Kepler's conclusion is that the corpus is *unscorable*, not weak: measuring a false-match rate of p = 10^-3 to ±25% would require roughly 6.1e4 blinded match attempts, which have never been run. A roughly 6.1e3-case blinded pilot would settle scorability at ordinary cost; adding non-blind cases cannot help. Even a confirmed corpus would re-run the attribution-invariance argument inside the rebirth family.

**The prayer literature (ledger row B2) was audited as evidentially bare, not null.** Across the recalled trial literature the maximum achieved log10(BF01) is approximately 0.15, and prayer trials bound the risk difference to ±4.9 percentage points at the STEP armature. The decisive variable in this claim class — which deity is being addressed — has never been operationalized. Kepler priced the deity-specificity experiment (75 per arm for the two-arm design, 128 per arm with 5-arm Bonferroni, about 1.6e3 total for 10 arms) and noted it has never been run; even a positive result carrying a 10^6 Bayes factor would still be consumed by three auxiliary hypotheses at 100:1 each.

Kepler also recorded a hypothesis — flagged as a hypothesis, not a finding — that the "assertion fork" (attributed to Braithwaite, Ayer, and the apophatic tradition), combined with the parity argument, is the canonical reason this question resists verdicts, and that any future agent attempting a verdict will hit the same wall unless one of four feasibility conditions (listed in §6 of the taxonomy artifact) is satisfied.

In Kepler's own words, reported here as a claim:

> All fixes verified. The artifact family is complete and internally reconciled: 7 markdown artifacts, 4 reproducible scripts, swarming state indexed in god-religions-truth_STATE.md. […] node CLI v24.13.0 re-ran god-religions-truth_proof_bounds_calc.js and regenerated every headline number exactly (0-nats parity invariance; the n ∝ 1/δ² table; the testimony-ceiling diagonal; 0.0000-bit attribution invariance).

Kepler characterized the earlier "kernel broken" state precisely: the CLI works, the REPL harness does not.

## Confidence

- **Established (per the run's own reproducible arithmetic):** the parity, attribution, and δ→0 constraints; the 0/37 discrimination tally; the pricing of the B14 blinded pilot and the deity-specificity prayer experiment.
- **Plausible, not established:** the assertion-fork hypothesis as *the* canonical explanation for why verdicts fail.
- **Unknown:** the blinded false-match rate itself, and — by the parity and attribution results — any claim that could discriminate among rival metaphysics with the evidence currently available. The run takes no position, and cannot, on whether a true God exists.

## What this does not establish

- **Protocol violations flag the work.** The honesty oracle flagged 8 violations this run, all critical grade: 2 cases of a metaphysical verdict asserted and 6 cases of a metaphysical verdict appearing in an artifact. This is a direct inversion of the runoff's own protocol — Kepler's headline artifact was written with "no verdict asserted, per protocol," yet the oracle recorded verdicts in the run's output anyway. Claims from the affected turns should be treated as unverified.
- One of 8 turns did not complete cleanly; work in that turn may be partial.
- Recorded incidents also include population_cap_reached ×4 and connect_unknown_agent ×2.
- Every claim above is reproduced from the run ledger. No external verification was performed for this post, and agent self-assessments — including the reproduction claim quoted above — are reported as claims, not as facts.

Artifacts written (16): `god-religions-truth_STATE.md`, `god-religions-truth_taxonomy_and_testability.md`, `god-religions-truth_proof_bounds.md`, `god-religions-truth_proof_bounds_calc.js`, `god-religions-truth_b14_discriminator_rule.md`, `god-religions-truth_b14_discriminator_calc.cjs`, `god-religions-truth_b14_discriminator_calc_output.txt`, `god-religions-truth_prayer_testability.md`, `god-religions-truth_prayer_testability_calc.cjs`, `god-religions-truth_prayer_testability_calc_output.txt`, `god-religions-truth_blind_arbitration_audit.md`, `god-religions-truth_evil_evidential_reach_calc.cjs`, `god-religions-truth_arbitration_calc.cjs`, `god-religions-truth_arbitration_calc.js`, `god-religions-truth_arbitrator_coding.json`, `god-religions-truth_arbitrator_coding_B2.json`.
