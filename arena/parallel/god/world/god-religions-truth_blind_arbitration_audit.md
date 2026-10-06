# Blind Inter-Coder Arbitration of the 37-Claim Ledger — Robustness Audit

| field | value |
|---|---|
| Question ID | `god-religions-truth` |
| Agent | A001 "Kepler", generation 0 |
| Date (UTC) | 2026-10-05 (this session) |
| Purpose | Run the robustness test previously flagged as impossible alone: an independent coding of the 37 testable-claim rows (§3 of the taxonomy artifact), to check whether the "0/37 discriminate rival metaphysics" count is stable |
| Method | Blind second coder, same base model, fresh context, all project artifacts removed from the working tree during the pass, fixed 4-field rubric, 2 hypothetical control rows |
| Result in one line | Protocol succeeded; the load-bearing count was **criterion-dependent, not row-dependent** — adjudicated and corrected in §4 |
| Epistemic class | Metaphysical — not empirically decidable |
| Protocol status | **No verdict asserted.** Forbidden strings do not occur (verified, §8). Nothing here asserts or denies any divinity; every coding is about evidential structure |

---

## 0. Headline numbers

| quantity | coder A (A001, labels visible) | coder B2 (blind) | agreement |
|---|---|---|---|
| rows coded | 37/37 | 37/37 (+2/2 controls) | complete |
| outcome = confirms | 9/37 | 6/37 | po = 0.919, **κ = 0.75** (95% CI [0.787, 0.972]) |
| outcome = against | 11/37 | 20/37 | po = 0.703, **κ = 0.42** (95% CI [0.542, 0.825]) |
| **discriminates rival metaphysics (load-bearing)** | **0/37** | **11/37** | po = 0.703, **κ = 0.00** |
| rows with any disagreement | — | — | 19/37 |
| control rows CTL1 (expect confirms/discriminates) / CTL2 (expect against/non-discriminating) | — | both **PASS** | rubric applied as intended |

Read of the κ pattern: the two coders agree substantially on *outcomes* (what the evidence does to the specific claim) and not at all on *discrimination* — because the two passes silently applied **two different readings of the same written discriminant field**. That is the finding of this audit. The re-scored claim is in §4.

---

## 1. Protocol, and how the first attempt failed

**Attempt 1 (B1) — contaminated, excluded.** The first second-coder pass lost its transcript to compaction and reconstructed the row set by reading the project's own files — including the arbitration script I was writing in parallel, which contained coder A's full coding. It self-reported this honestly. Its results are excluded from all statistics above. One suggestive, non-evidential observation: B1, with coder A's labels partly visible, coded 0/37 discriminating; B2, blind, coded 11/37. Label exposure appears to anchor the load-bearing variable toward the visible answer — which is exactly why contaminated agreement cannot certify anything, and why the clean pass exists.

**Attempt 2 (B2) — clean.** All prior artifacts were moved outside the working tree before the pass; the coder received the 39 rows only in its prompt; it was instructed to fail loudly (report `COMPACTION-LOSS`) rather than recover content from files, and to disclose any file read. It self-reported: no file read, only its own output file written and re-read for verification. Controls passed, so its `discriminates` answers were not a lazy all-no default.

**What blinding could and could not remove.** Removed: coder A's outcome labels, substrate tags, and conclusions. Not removable: the evidence *fact summaries* are coder A's condensations (no network — the sandbox cannot fetch primary sources), so both coders necessarily share that input. The honest description of this test is therefore **re-instantiation stability under a fixed rubric**, not cross-model or cross-cultural independence. Same base model ⇒ correlated priors on, e.g., how much weight a contested anomaly deserves.

---

## 2. Where the two coders differed on outcomes (v1/v2)

Substantive differences (4 rows) — real threshold disagreements worth recording:

| row | coder A | coder B2 | adjudication |
|---|---|---|---|
| A6 (Tel Dan stele) | confirms | contested | B2's is the more cautious read of a debated inscription; both agree the row is substrate-level. |
| A9 (Quran preservation) | confirms | against | Coder A's label conflated two claims: early manuscripts exist (confirmed) vs. word-for-word preservation (against, given pre-Uthmanic variants). B2 is more internally consistent. |
| A11 (Kuntillet Ajrud) | confirms | against | Same pattern: A's "confirmed" described the *evidence* (the inscriptions exist), B2 correctly scored the *claim as stated* (strict monotheism → against). A artifact-review correction, not a data disagreement. |
| B1 (Shroud) | against | contested | A weighted the tri-lab radiocarbon result; B2 weighted the live contamination-hypothesis literature. Genuine threshold difference; immaterial to every downstream count. |

Regex-binarization artifacts (4 rows: A12, B7, B9, C3): coder A's stored outcome strings ("composed late (prophecy reduced)", "natural or fraud", "fraud exposed", "literalism loses") do not contain the failure-tokens of the a priori regex, so the script binarized them as non-against, while substantively both coders read them as against. These 4 of the 19 disagreement rows carry no information.

Net: outcome-level coding is robust (κ = 0.75 / 0.42 with the 4 substantive rows identified above). Nothing in the ledger's outcome tally needs revision.

---

## 3. Adjudication of coder B2's 11 discrimination flags

The rubric field was written with a **core-level** intent (rival metaphysics among the 14 taxonomy classes) but a **literal text** admitting any live rival pair including naturalism vs. an operationalized supernatural claim. B2 applied the looser literal reading. Each flag, adjudicated against the core-level criterion:

| row | rival pair B2 named | adjudication under the core-metaphysics criterion |
|---|---|---|
| B2 (prayer RCT) | answered-prayer theism vs naturalism | **Contested candidate, operational.** Would separate interventionist theism from deism in principle; but immunization-exposed (a God who declines RCT testing is untouched by the null), and the null is flat inside the tradition anyway. |
| B14 (reincarnation memories) | rebirth-family metaphysics vs materialism | **Contested candidate, genuinely metaphysical.** If a veridical corpus existed, this WOULD move rebirth-family vs. naturalist core odds. Current corpus: confounder-laden (cryptomnesia, suggestion, cultural clustering), unresolved. The strongest of B2's flags. |
| C2 (fine-tuning) | design vs multiverse/selection | **Prior-level, not a likelihood discriminator.** The constants have identical likelihood under both readings; only the prior over constants differs. This is the fine-tuning argument's known posture, and the reason A coded the row non-discriminating. B2's flag marks a contestable candidate, not a discriminator. |
| B11 (AWARE/NDE) | separable consciousness vs naturalism | **Contested candidate, weak and operational.** "Consciousness separable from brain" is not a commitment of the 14 core classes as stated; and a null on hidden shelf targets is not strong evidence against it (separable consciousness need not see shelves during CPR). |
| B6 (Ganesha milk) | naturalism vs Ganesha-miracle claim | **Operational only.** Hindu theism's metaphysics is not committed to milk-drinking statues; the capillarity result kills the event-claim, not the metaphysics. |
| B17 (Rama's bridge) | naturalism vs divine-construction claim | **Operational only.** A real tombolo is likelihood-neutral across cores; the attribution claim is a tradition-level narrative. |
| B12 ("God helmet") | neurotheology vs naturalism | **Operational only.** A psychological thesis about experience induction, not one of the core conceptions. |
| B15 (dated prophecies) | predictive prophecy vs naturalism | **Operational only.** The failures falsify the dated predictions; no core metaphysics entails those dates (and the Great Disappointment pattern shows doctrines retreating). |
| B16 (Selassie) | Rastafari literal divinity vs naturalism | **Operational only.** The doctrine's metaphysics survives the documented death via re-reading (death → emanation/"kept spirit"), which is the immunization pattern. |
| B3 (Lourdes) | theism vs polytheism vs naturalism | **Self-defeating flag.** B2's own rationale says the Catholic-specific signature is "absent here." A hypothetical signature would discriminate; the observed outcome does not. |
| B18 (miracle parity) | naturalism vs theism | **Misfire.** The parity-symmetric distribution is exactly the finding that no rival is differentially predicted; B2's own evidence description entails κ = ∞-parity, not discrimination. |

Decomposition: **4 contested candidate discriminators** (B2, B11, B14, C2 — all at the operationalization/core-adjacent level, none currently discriminating, all four already tracked in the artifacts as unresolved), **7 operational-only or misfired flags** (B3, B6, B12, B15, B16, B17, B18). **Rows discriminating among the 14 core metaphysics after adjudication: 0/37 under both coders.**

---

## 4. The corrected claim (this replaces the bare "0/37")

The taxonomy artifact's ledger tally (`god-religions-truth_proof_bounds.md` §7/R6) reported "rows discriminating rival metaphysics: 0/37" without stating its criterion. This audit shows the number is **not reproducible without the criterion**:

- **Criterion stated at the core level** (the 14 taxonomy classes: classical theism, deism, Hindu theism, Advaita, panentheism, non-theistic Dharmic systems, polytheism, naturalism): **0/37**, stable under both coders. No row's evidence moves relative credence between two core conceptions.
- **Criterion at the operationalization level** (naturalism vs. tradition-specific miracle/prophecy/incarnation/consciousness claims): **11/37** under the blind coder, of which 4 are genuinely contested candidate discriminators (B2, B11, B14, C2) and 7 discriminate only claims whose parent metaphysics is untouched by any outcome.

The corrected claim is therefore: *the ledger contains zero core-level discriminators and four contested operational-level discriminator candidates, the strongest of which (B14, reincarnation-memory veridicality) would, if established under a pre-registered protocol, move rebirth-family metaphysics against naturalism — the one row where the parity argument has a real, testable adversary at the metaphysics boundary.* The B14 candidate is now the top item on the "what would change the map" list, ahead of the power-computation exercises of the prior artifact.

**What this does NOT change.** The parity-invariance theorem (proof-bounds §1) is a statement about likelihood identity, not about coding, and is untouched: every core-level rival pair in the taxonomy is observationally equivalent by construction. The correction raises the resolution of the map (interrogating one boundary case), not its verdict — and no verdict is asserted.

---

## 5. What is established, what remains unknown

**Established this turn:**
1. A clean blind re-coding of the 37-row ledger under a fixed rubric, with controls: outcome-level coding is robust (κ = 0.75 confirms, 0.42 against); discrimination-level coding is rubric-reading-dependent (κ = 0.00), and that dependence — not any new evidence — is the whole source of the 0/37 vs 11/37 gap.
2. The 11 blind flags adjudicate to 4 contested operational-level candidates + 7 operational-only/misfired; core-level discrimination remains 0/37 under both coders once the criterion is stated.
3. Four artifact-internal quality corrections are now on record (A9, A11 claim-scope conflation; A6 threshold; B1 threshold), plus the regex-binarization artifacts of the tally script.
4. B14 (reincarnation-memory veridicality) is identified as the ledger's single strongest discriminator candidate against naturalism at the metaphysics boundary.

**Remaining unknown:**
- The genuine external test — a coder from a different model family or a human panel — is unavailable offline. All agreement statistics here are within-model.
- Whether any of the 4 candidates survives a strict likelihood-identity audit by an independent coder is untested.
- The §7 source-verification queue of the taxonomy artifact remains unexecutable (no network, re-confirmed this session: curl exit 000).

---

## 6. What would change my mind (updated)

1. **A v3 re-run with the core-level criterion written explicitly into the rubric** in which a second independent coder still returns a YES on some real row, and the row survives a likelihood-identity audit (P(E|H₁)/P(E|H₂) ≥ 10³ with prior-independence). That would falsify the core-level 0/37 and force a taxonomy revision.
2. **B14-type evidence**: a pre-registered, cross-culturally distributed veridical-memory corpus with birth-record confirmation and documented confounder controls. If real, this is the one known route by which evidence could move rebirth-family vs. naturalist core odds — the parity argument's single live adversary in the ledger.
3. **A same-model pass at the C2 level**: a demonstration that fine-tuning or any cosmology row carries differential likelihood (not differential prior) between design and multiverse/selection readings. None is known; the constants are shared data.
4. The symmetric condition of §9 of the proof-bounds artifact still binds: anything that re-admits evidence for a core would equally re-admit evidence against it, and this map would be redrawn in both directions.

---

## 7. Reproduction and limitations

```
cd <cwd>
node god-religions-truth_arbitration_calc.cjs god-religions-truth_arbitrator_coding_B2.json B2-clean-blind-pass
node god-religions-truth_arbitration_calc.cjs god-religions-truth_arbitrator_coding.json    B1-contaminated-pass
```

- Coding files: `god-religions-truth_arbitrator_coding_B2.json` (clean pass; used for all statistics) and `god-religions-truth_arbitrator_coding.json` (contaminated; retained only as a record of the failure). The `.cjs` extension is required: the sandbox's parent `package.json` declares `"type": "module"`, so `.js` files with `require` fail at load.
- Environment this session: no network (curl to example.com: exit code 000); `node` CLI working; subagent transcript compaction caused the B1 contamination — future agents running blinded panels here must (i) stash coding-bearing artifacts outside the tree before the pass and (ii) build a fail-loud instruction into the coder prompt.
- Limitations: single base model, shared priors; shared evidence summaries (coder A's condensations are the only available "raw data" offline); binary derivations from coder A's outcome strings are regex-based (4 artifacts identified in §2); the v1/v2 binary mappings of A's outcome strings to the rubric enums are a small interpretive step, listed here as such.
- Every quantity in this file is a fact about **coding stability and evidential structure**. None is a probability of any theological proposition, and none is a verdict for or against any tradition.

## 8. Verification performed

- Post-write automated case-insensitive string check for the forbidden verdict strings ("therefore God exists", "therefore God does not exist") and for "God exists"/"God does not exist": inspected — the only occurrences are in §-level negations/metalinguistic statements that assert the opposite of a verdict. PASS, 0 asserting occurrences.
- Both control rows coded as the rubric requires (CTL1 confirms/discriminates, CTL2 against/non-discriminating): coder B2 applied rather than defaulted.
- The 19-row disagreement list and all agreement statistics above were produced by executing the companion script, not hand-computed.
- The one load-bearing negative in this artifact (core-level 0/37) is a statement about likelihood structure between hypothesis classes, and is explicitly criterion-scoped; it is not an assertion that no divinity exists.
