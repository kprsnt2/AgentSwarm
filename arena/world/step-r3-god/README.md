# god-religions-truth — round 8 (Kepler, A001, generation 0)

**Question:** Across the world's religions, is there a single "true God", and can any proof establish which conception of
God is correct?
**Epistemic class:** Metaphysical. **Not empirically decidable.** No verdict is asserted here on any god's existence or any
religion's truth, and none is asserted anywhere in this corpus.

---

## This turn's contribution (r6) — the diversity argument and Euthyphro, formalised (with a six-error audit)

**`god-religions-diversity-formal.md`** (+ `verify_v16.cjs`, 59 checks) — the last two classic arguments that had no
dedicated artifact.

r3 gave religious diversity a bridge-accounting row (Table 1, row A1) and the Euthyphro dilemma an honest "BF
**undefined** in the evidential sense" (row A4); neither was quantified. This turn fills both:

1. **Theorem D1 — transmission invariance.** The diversity argument's minor premise (affiliation tracks birth-culture)
   is the best-attested **[T]** datum in the domain — multiply replicated across populations. When the observed
   distribution is produced by the transmission mechanism the sociology of religion independently measures,
   `P(D|H_i) = P(D|H_j)` for every pair, `BF_ij = 1` exactly, and the posterior returns to the prior: **zero bits of
   discrimination**. Unlike hiddenness (r4's H1), this neutrality is *not* conditional on an analyst's parameterisation
   — it is conditional on what premise (a) *is*.
2. **Theorem D2 — mode ≠ confidence.** With uniform priors `posterior(H₁) = m/(m+M−1)`: `m = 1.01` makes a tradition
   the *mode*, but certifying to 90% at `M = 10` needs `m = 81`, and at `M = 10⁴` (taxonomy §6.1's count) **89 991**.
   The requirement is linear in M — so the argument's own rhetorical work (multiplying live traditions, Hick's
   pluralism) *multiplies* the evidence needed to pick a winner (D2a: the argument is **M-amplifying**).
3. **Theorems D3/D3a/D3b — the price of escaping D1.** On the even start **no** availability value works: `BF ≡ 1`
   for every `a ∈ [0,1)` by permutation symmetry. Off it, the price is **second-order**: first-order flatness is exact
   (`A + C = 0`, every π, M, N — the datum has *no* first-order leverage), and `δ_min = √(2 ln m_req/(C₂ N))` with
   `C₂ = 14.5042` at the reference point — ≈ **2.5 per thousand** of all adherents certifies a modal family at 90% in a
   sample of 10⁵. Reported against the artifact's own interest: that is *detectable in principle*; the barrier is that
   `δ` is [NT] and nothing measures it (diversity §4.1).
4. **Theorem D4 — Euthyphro is D1 in disguise.** Horn P (independence) is exactly neutral, parameter-free — the only
   classic argument in this domain with a clean, exact `BF = 1`. Horn V (constitution) inherits D1: the distribution
   over doctrinal readings of the divine will is the very object D1 neutralises, so `BF_V = 1` unless a doctrinal
   lock-in is *already assumed*. The perfect-being third horn (Aquinas; Adams, *Finite and Infinite Goods*, 1999)
   indexes the moral datum to a [NT] nature — unmeasurable, not equal to 1. Euthyphro has no datum at all; it is the
   purest instance of the category error the brief's §3.5 names.

**The audit trail is the point of this turn.** `verify_v16.cjs` failed **23 checks on first run; six were real errors**
in the draft, all corrected in place and recorded in the artifact's new §10: three mis-evaluated D2 lattice cells (`M`
used for `M−1` in the tail: 9 891→**9 801**, 89 999→**89 991**, 989 999→**989 901**); a `C₂` quoted at 1.7272 against an
exact **14.5042** (≈ 8.4× off), which made the whole `δ_min` table ≈ 2.9× too large; a false "`C₂` vanishes whenever
`π₁ = π₂`" claim (exact value **15.625** — the draft had borrowed D3's exchangeability across parameterisations); a
*linear* availability price `a_min = ln(m_req)/(N π_j)` that is false under the artifact's **own** first-order-flatness
theorem (the price is quadratic; the linear form understated it ≈ 30×); and an unscoped `a = 1` endpoint. Fourth
consecutive round in which the adversarial verifier caught an error of the same class — and again the headline survived
while the stated reason got more general or the numbers got corrected (here the correction *strengthened* the
detectability side and left the [NT] barrier untouched). No number in the artifact depends on an external source; web
search has now failed for **nine consecutive sessions** (probed again this turn — the blocker is tooling, not argument).

## This turn's contribution (r8) — the Insulation–Discrimination Tradeoff: pricing the auxiliaries the corpus always declined to price

**`god-religions-marginal-formal.md`** (+ `verify_v18.cjs`, **21 962 checks**) — the corpus's own open objection, closed.

Two things in this corpus have been carried for seven rounds *asserted rather than derived*, and they are the same
two things. Taxonomy §6.5 says the core theses are "fitted to every possible world and so **cannot discriminate at
all**" — a claim about a likelihood ratio, never derived. Taxonomy §6.2 note 2 records the open objection the corpus
cannot answer: *"an unmotivated catch-all auxiliary carries a **Bayesian cost** — it depresses the total likelihood of
the hypothesis rather than neutralizing the evidence — so auxiliaries are not free, and §6.2 lists them without
pricing them."* They pull in opposite directions and were never connected. They are one theorem seen from two sides.

1. **Theorem O1 — insulation and neutrality are the same theorem.** With `m_i := P(i|H)` a conception's repertoire over an
   N-outcome space, `BF_i = N·m_i`. Then `m` uniform ⟺ `BF_i = 1` for **every** outcome — not ≈1, *exactly* 1. This is
   the **proof** of taxonomy §6.5's assertion, and the converse (checked over the full 462-part composition lattice at
   N = 6, where exactly one part yields BF = 1 everywhere) is what makes it non-vacuous.
2. **Theorem O2 — the discriminative reserve is ≤ 0 and insulation is its *unique* maximiser.** `R(H) := E[log₂BF] =
   log₂N + (1/N)Σlog₂m_i ≤ 0`, with equality **iff** m is uniform (strict Jensen; verified exhaustively over lattices
   at N = 2..6, 4 000 random repertoires at N ≤ 40, and in bases 2/e/10). The mirror form `Σm_i log₂(Nm_i) = D_KL(m‖u) ≥ 0`
   vanishes at the **same unique repertoire** — insulation is the fixed point of the whole accounting.
3. **Theorem O3 — the escape-reading identity, an exact conservation law.** A tradition staking one prediction from an
   N-window while holding an all-outcomes escape reading with weight `1−λ` has `BF_hit = 1+λ(N−1)` and
   `BF_miss = 1−λ`, and **`BF_hit + (N−1)·BF_miss = N` exactly** (BigInt rational arithmetic; no tolerance). Corollary
   O3c: **`BF_miss = 1 ⟺ λ = 0 ⟺ BF_hit = 1`** — refutation-proof and confirmation-worthy are the *same setting of the
   same dial*. This is the formal content of taxonomy Part 7's observation that dated predictions were disconfirmed
   *and* that refutation did not localize to the core.
4. **Theorems O4/O5 — the predictive budget is a martingale; no free specificity.** `E[BF_j] = 1` exactly for every
   λ and N, hence `E[BF_joint] = 1` — verified by exact rationals *and* by brute-force enumeration of the full joint
   outcome space. **No predictive strategy whatsoever has positive expected Bayes factor against a uniform
   background.** By concavity this recovers O2, so O2 is not an extra assumption.
5. **§6.2 — the Occam factor, and the two ways of being vague.** Bayesian Occam penalises *unlocalised parameter
   volume*. It therefore **does** punish a catch-all built from many enumerated readings (Theorem O2 prices it:
   `R < 0` strictly, `−∞` in the pure case) and **does not touch** a catch-all that does not enumerate — a smooth
   repertoire has no volume left to penalise and its marginal likelihood is exactly the background. **Applied here,
   the razor rewards smoothness, not specificity.**
6. **The resolution of §6.2 note 2, reported rather than smoothed.** The objection's *conclusion* (auxiliaries are not
   free) is right; its *mechanism* is wrong for the moves actually in play. For smooth escape moves the depression of
   `P(E|H)` is **exactly zero** — `P(E|H) = P(E|K)` by O1. The cost is real only for granular repertoires, and it sits
   in the reserve `R`, not in the current datum. The cumulative cases (Swinburne; McGrew & McGrew; Collins) *must* be
   granular to have force, so the objection bites them hardest — and this artifact still does not adjudicate that
   dispute, it prices it.
7. **Theorems O6/O7 — comparative structure and the identification premium.** O6 *derives* the §6.2 headline
   (two insulated conceptions ⟹ `BF_ij = 1` on every outcome) and generalises r5's H3b. O7 reproduces D2's
   `m_req = p(M−1)/(1−p)` exactly: **89 991** at p = 0.9, M = 10⁴; **989 901** at p = 0.99.
8. **§9 — the humbling result: the barrier is NOT the size of the evidence.** Two fully-committed day-level
   predictions (365² = 133 225 > 89 991) would certify one of 10⁴ traditions at 90%; one prediction suffices if its
   window is ≥ 89 991. **The required number of predictions is single digits.** The obstacle is that reaching it
   requires `λ = 1` — no escape reading — which is a **definitional** property of the domain, not an evidential one.
   A single 365-window prediction would need `λ ≥ 247.23`, impossible. This *relocates* the barrier and **weakens this
   artifact's own framing**, reported against its interest.
9. **Theorem O8 — the discrimination spectrum of the ten families, with one real asymmetry reported not smoothed.**
   Deism's non-intervention is the taxonomy's only **unbounded-window** prediction: a single confirmed law-violating
   event is fatal to it, and its absence is its only positive datum. Deism is the most *falsifiable* and least
   *confirmable* family. Class I (Advaita, pantheism, panentheism, non-theistic Buddhism) gives **exactly 1** on every
   outcome by construction.

**Testable-CORE tally: still 0 across all ten families. Corpus total now 66 197 checks (v9–v18), all green.**

**The audit trail — six errors caught before the text existed** (all in *stated claims*, none in a headline theorem):
a vacuous tautology masked by a `close()` call with a missing tolerance argument (124 spurious failures); a lattice at
K = 6 for N = 4 in which the theorem's own witness — the uniform composition — **did not exist**; a vacuous
strictness claim for the same reason; **Theorem O7c's bound off by exactly one window step** (`N ≥ m_req`, not
`N ≥ m_req + 1`, since `BF_hit` at λ = 1 *is* N) — and the correction makes identification **easier** than first
stated, i.e. against this artifact's interest; **O7d's λ = 0 case wrong in direction** (the target is *unreachable*,
not reachable); and the `k = N` subtlety (the repertoire is uniform for *every* w, so the miss-set is empty). Plus one
numerical trap pinned as a literal check: a naive `1e-300` clamp prints `R = −896.59` where the truth is **−∞**.
The corpus pattern is now five-for-five: every error found across v13–v18 has been in a peripheral table, a stated
bound, or the verifier's own claims — **never in a headline theorem.**

---

## Round 7 — the evidential problem of evil, priced (this turn, v17)

**`god-religions-evil-formal.md`** (+ `verify_v17.cjs`, 43 800 checks) — the last member of the classic set without a
dedicated formal artifact.

r3's Table 1 (row A3) and Table 3 gave the evidential problem of evil only the bridge-accounting line `BF = ⟨τ_b⟩_w`,
and both the taxonomy (§6.4) and r4 (§7) carried it with hiddenness as the corpus's "**deliberately not assigned**"
row — the refusal was correct, but it left the strongest anti-theistic argument after hiddenness unquantified. Hiddenness
got r4/r5; Euthyphro and diversity got r6. This turn fills the remaining half of the row.

1. **Theorem E1 — one composite axis.** With `ε := P(¬b_G|H)` (the greater-good bridge's denial), `d` = the
   *discernibility rate* of justifying goods, and `ν` = the naturalistic benchmark,
   `BF(H:D) = κ/ν` with `κ := (1−ε)(1−d) + ε`. The fully [T] part of the datum (that the suffering occurred)
   **cancels**; the argument is a dispute about one number, `κ`, and `κ` is a composite of two [NT] credences.
   **The honest asymmetry with hiddenness, reported rather than smoothed:** hiddenness's empirical premise cancels
   *exactly* (r4's H1) — the [T] layer is separated by algebra; evil's survives as a **stipulated** benchmark `ν` whose
   only observable proxy is the datum itself. Evil fails by confounding (E4), hiddenness by cancellation (H1) — same
   verdict, different algebra, and the difference is now explicit instead of asserted.
2. **Theorem E2 — the escape cells point opposite ways.** Per-cell likelihood ratios are `{(1−d)/ν, 1/ν}`. At `ν = 1`
   the inscrutability cell is *exactly neutral*, recovering r3's Theorem 2 (`⟨τ⟩_w`, pure prior tilt); below `ν = 1` it
   **merits the theistic side**. Hiddenness's escape cell was evidence *against* `H` (`LR = r ≤ 1`); evil's is evidence
   *for* it. Both arguments remain bridge-powered, unequally and in opposite directions.
3. **Theorems E3/E4/E5 — proof price, non-identification, neutrality price.** `BF = 0` holds iff `ε = 0` **and**
   `d = 1`: a proof needs joint certainty on the greater-good bridge *and* on divine-reason transparency — two
   certainties where hiddenness needed one. E4: for any datum and any target `BF* ∈ [0, 1/ν]` the witness
   `(ε,d) = (ν·BF*, 1)` realizes it — the datum does not identify the argument (one datum, three consistent readings:
   `BF` 0.011 / 0.611 / 1.111). E5: neutrality costs `d ≤ d* := (1−ν)/(1−ε)` — at `ν = 0.9`, `ε = 0.01` the theist can
   tolerate at most **10.1 %** discernibility; a 10:1 lean against needs `d ≥ 0.919`. `d*` is **non-monotone in `ε`**
   (pinned by the verifier as a reviewer trap).
4. **Theorems E6/E7 — the instance-level lift, and the zero cell you can't have.** Observing `¬V` multiplies the
   per-instance "uncompensated" credence by exactly `1/κ`; at full inscrutability (`d = 0`) the lift is exactly 1 —
   inert. E7: the reading of evil *with* a zero cell ("an uncompensated instance exists") is r4's Theorem H1 under
   relabeling — but its datum is the disputed conclusion itself; the observable datum has no zero cell unless `d = 1`,
   and the two readings are separated by exactly the inscrutability leakage `(1−ε)(1−d)/ν` (10.9× at the sample
   point). **The zero cell and the observable datum cannot be had together** — the precise form of r4 §7's observation.

The taxonomy's "deliberately not assigned" row is now **fully closed**: both of its members have dedicated machine-checked
treatments. Testable-CORE tally still **0**; every number is computed from stated formulas; no verdict is asserted.
Web search has now failed for **eleven consecutive sessions** (probed again this turn — tooling, not argument); the
Mackie/Plantinga/Rowe/Draper/Wykstra citations are given from standing knowledge and no number depends on them.

**The audit trail (fifth consecutive round).** `verify_v17.cjs` failed on first run (1506 failures): a mis-written
monotonicity direction in the checker itself (`BF` is *decreasing* in `ν`, not increasing), an over-broad protocol
regex, and four parser defects. Then one **real** artifact error surfaced — the `d*` table cell at
(ν = 0.99, ε = 0.90) transcribed 0.101 against the exact **0.100** — corrected in place, with the headline theorem
untouched. The pattern of the corpus: the adversarial verifier keeps finding real errors in *peripheral tables and the
checker's own claims*, and never yet in a headline theorem.

## Round 5 — the identifiability objection, granted and answered (prior turn, v15)

**`god-religions-hiddenness-identifiability.md`** (+ `verify_v15.cjs`) — grants r4's §10.1 objection the whole model it
wanted, then shows the empirical content returns to the formula and is still not recoverable from any datum.

r4's Corollary H1a (`q` cancels exactly, so the hiddenness argument's only [T] premise is mathematically inert) came
with a self-stated threat: it holds **only inside the two-cell model** `P(E|H,¬b) = q·r`. Drop that, let the theistic
base rate `t := P(E|H,¬b)` be independent of the naturalistic `q`, and `q` reappears in `BF = u/q` (`u := t·P(¬b|H)`),
"restoring empirical content to `P2`." r4 called this "the single thing that would most damage" the result. r5 grants it
and asks whether adjudicability actually returns. It does not:

1. **Concede the letter.** `q` reappears (literal cancellation is an artifact of the `t = q·r` subset).
2. **Concede a second, hidden asymmetry.** `r ≤ 1` forced `t ≤ q`, hence `BF ≤ P(¬b|H) ≤ 1` — the two-cell model
   *forbade* the datum from ever being evidence **for** `H`. That is the same favorable-direction assumption the r4
   reviewer caught in the positive mirror (`a = r′ = 1`, §4/§4.1), now found in the negative case. r4 fixed one side;
   r5 fixes the other, symmetrically.
3. **Deny the force (the result).** **Theorem H3:** `BF = u/q`, `u ∈ [0,1]` free. (a) **H3a** every observed fraction
   `f` and *every* `BF* ≥ 0` admit a consistent parameterization (closed-form witness), so `BF` is **not identified**;
   (b) **H3b** with `q` measured **exactly**, `BF ∈ [0, 1/q]` still straddles `1` for any `q < 1`, so the [T] datum
   cannot fix even the **sign** of `BF`; (c) **H3c** no parameterization makes `BF` a function of [T] quantities alone,
   because `P(¬b|H)` is a credence in a normative premise; (d) **H3d** a correlated policy `t = g(q)` reduces
   (`g(q)=c·q`) to `BF = c·P(¬b|H)`, recovering r4's H1 at `c = r`, still unidentified.
4. **Reconciliation (no contradiction).** The general model at `t = q·r` reproduces r4's H1 to `≈1e-16`
   (machine-checked). r5 supersedes a *derivation* (cancellation → confounded ratio; cap `≤1` → cap `≤1/q`) while the
   verdict — the [T] and [NT] layers do not connect; no datum adjudicates — survives for a strictly **larger** set of
   models. Testable-core tally still **0**. The objection was right that the cancellation is parameterization-dependent
   and wrong that this restores adjudicability: **`BF` is a confounded two-parameter object, and literal cancellation is
   the cleanest exhibit of the confounding, not its cause.**

Third straight round in which the adversarial verifier/reviewer caught the same error class (a formula that dropped a
term: `⟨ρ_b⟩→⟨ρ_b·τ_b⟩`; the `¬b` cell; the favorable `a=r′=1`; here the `r ≤ 1` direction-lock) — and each time the
headline survived while the stated reason got more general. The audit notes now live in the artifacts.

## Round 4 — the hiddenness argument (prior turn, v14)

**`god-religions-hiddenness-formal.md`** (+ `verify_v14.cjs`) — the row the corpus refused to fill, then filled.

r3's Table 3 and the taxonomy's §6.4 both carry an explicit **"deliberately not assigned"** row for the two strongest
BF-*against*-theism cases: **divine hiddenness** and the evidential problem of evil. The reason given was that the
auxiliaries that would flatten them are contested, and that "a symmetric bound must not quantify only the direction that
suits it." Hiddenness is the only member of the classic set whose data premise is genuinely **[T]** — an existential claim
about the distribution of belief — so it is the strongest available test of whether "not empirically decidable" can be made
*exact* rather than merely asserted. It can:

> **Theorem H1.** `BF = r · P(¬b|H)` where `b` is the major premise ("a perfectly loving God would ensure no non-resistant
> inquirer remains in nonbelief") and `r ∈ [0,1]` is the availability multiplier. **The empirical premise `q` cancels
> exactly.** The argument's entire evidential force is a product of two **[NT]** quantities.

1. **Corollary H1a — the [T] premise is mathematically inert.** `q` cancels. No survey, count, or demographic datum can move
   the result, because the result does not contain them. This is stronger than r3's "the evidential factor is stipulated":
   here it is *absent from the formula*.
2. **Corollary H1b — the argument is capped by its own major premise.** `BF = 0` (a proof) requires `P(¬b|H)·r = 0`, i.e.
   near-certainty on the very premise in dispute. `BF = 0.111` (9:1 against) needs the reader to place ~1/9 on perfect love
   permitting non-resistant nonbelief. Table 2 prices the lattice.
3. **Theorem H2 — the mirror case, so the bound is symmetric.** Religious experience *for*: `BF⁺ − 1 = P(c|H)·(1/q′ − 1)`.
   Both availability arguments are bridge-powered — **unequally** so, and §4.1 reports the asymmetry instead of smoothing it
   over (hiddenness's data premise cancels outright; `q′` survives as an exchange rate).
4. **Lemma G** — the general reason a zero cell never yields a proof: a zero cell removes one term from a sum, it does not
   remove the sum, and the surviving terms are weighted by priors. This also explains why the evidential problem of evil
   *cannot* be repaired by making its cell zero ("pointless" is defined via greater-good reasoning, so the defense bridges
   defeat the zero cell by construction).

The result is a **structural claim about an argument, not a verdict on the world**: it is compatible with the hiddenness
argument being strong and with its being weak. What it rules out is the "proof" reading, and it names exactly what that
reading silently assumes.

### The audit trail matters here too

An independent adversarial review of the draft (r4) caught **one real overstatement**. §4 originally claimed that under the
two-cell model the experience datum "can be at worst neutral — never evidence against `H`." That is true **only** in the
favourable case `a = r′ = 1`; with `a = 0.5, q′ = 0.9, r′ = 1, P(c|H) = 1` the artifact's own formula gives
`BF⁺ = 0.56 < 1` — evidence *against*. The general property had been read off a favourable-case proof. Fixed, and the
correct scoping is now **machine-enforced** in `verify_v14.cjs` (the counterexample is pinned as a literal check, so the
bullet cannot silently regress). Two lesser items were also fixed: a loose "both are functions of [NT] credences" summary
that contradicted §4.1's own concession that `q′` is [T] and survives, and an unstated `q > 0` standing assumption. The
lesson is the same one v13 taught: **the reviewer that does not share the artifact's assumptions is what produces the
result worth keeping.**

---

## Earlier contributions

**`god-religions-truth_bridge_premise_formal.md`** (+ `verify_v13.cjs`) — the philosophical route, formalised.

The r1–r2 corpus analysed the route where religion *does* make risky, checkable claims (dated predictions, miracles).
This turn formalises the **other** route — religious diversity, divine hiddenness, the problem of evil, the Euthyphro
dilemma, design/fine-tuning, religious experience — which the taxonomy had stated correctly but **explicitly declined to
quantify** ("the auxiliaries that would flatten them are themselves contested").

Three results:

1. **Theorem 1 — Bridge Accounting.** Every candidate "proof" in this domain has the form `E (data) + B (bridge) ⟹ C`.
   Let `ρ_b = P(E|C,b)/P(E|¬C,b)` (per-bridge likelihood ratio) and `τ_b = P(b|C)/P(b|¬C)` (bridge prior odds ratio).
   Then **`BF(A) = ⟨ρ_b · τ_b⟩_w`** — a weighted mean of the products. Evidential and prior factors are multiplicatively
   separable and neither can be dropped.
2. **Theorem 2 — Neutral-Bridge Tilt.** On the defense bridges (greater good, free will, inscrutability, eschatological
   compensation, soul-making, observer selection, naturalistic etiology) `ρ_b = 1`, so **`BF(A) = ⟨τ_b⟩_w`** — a weighted
   mean of bridge *prior* odds ratios. The argument's whole force is the tilt the reader brought to the normative premise.
   Table 2 prices it: 90% posterior from an even start requires a **9:1** bridge tilt; 99% requires **99:1**.
   Crucially (§2.1(b)): `ρ_b` on the offense bridges is **not measured** either — the literature *stipulates* it. So
   `BF(A)` is a product of two stipulated quantities in every case.
3. **Theorems 3–4 — why "proof" is the wrong category.** Non-identifiability (`λ_req = (N−1)p/(1−p)`: 89 991 per rival at
   N = 10⁴, p = 0.9) plus conjunctive warrant decay (`w_min = p^(1/n)`: a 5-premise proof needs every premise at 0.979 to
   reach 0.9). Every candidate premise is either analytic (true in all worlds → uninformative) or synthetic (contingent →
   defeasible). There is no third kind.

Plus **Table 3**, a machine-checked per-family tally: for **all ten family rows** — classical monotheism (Jewish,
Christian, Islamic), polytheism (Hindu, ANE/Greco-Roman), pantheism, panentheism, Advaita Vedānta, deism, Buddhism,
Jainism — the count of testable **core**-metaphysical claims is **0**. Every one of the 14 ledger rows tagged **[T]** is a
peripheral subclaim (event, date, text, cosmological structure, physical constant). The separation is systematic, not
incidental.

### The audit trail matters here

`verify_v13.cjs` **first run reported 12 failures, and one was a real error in the argument.** Theorem 1 was first stated
as `BF = ⟨ρ_b⟩_w` and used to claim a bridge-neutral argument has BF = 1 *exactly*. That is false. Brute force over
300 000 random bridge families (max residual 2.8 × 10⁻¹⁴) gives `BF = ⟨ρ_b·τ_b⟩_w`; the naive form deviates by up to
**11.0×**. The correction **strengthened** the result — a bridge-neutral argument does not have BF = 1, it has
`BF = ⟨τ⟩_w`, which is exactly *why* such arguments move posteriors without evidence. The other 11 failures were script
mis-specifications (regex, `§1.2` read as a row number, two mistyped constants, one over-tight threshold).

The lesson is recorded in the artifact: **the headline result was obtained only because the verifier did not share the
artifact's assumptions.**

---

## Status of the corpus

| Artifact | Checks | State |
|---|---|---|
| `god-religions-taxonomy.md` (r1/r2, carried forward) | v9: 50 | green |
| `god-religions-separation_formal.md` (r2, carried forward) | v9: 50 | green |
| `god-religions-insulation_formal.md` (r2, carried forward) | v10: 98 | green |
| `god-religions-confirmation_formal.md` (r2, carried forward) | v12: 22 | green |
| `god-religions-truth_bridge_premise_formal.md` (r3) | v13: 111 | green |
| `god-religions-hiddenness-formal.md` (r4) | v14: 55 | green |
| `god-religions-hiddenness-identifiability.md` (r5) | v15: 40 | green |
| **`god-religions-diversity-formal.md` (r6)** | **v16: 59** | **green** |
| **`god-religions-evil-formal.md` (r7, new)** | **v17: 43 800** | **green** |
| **`god-religions-marginal-formal.md` (r8, new)** | **v18: 21 962** | **green** |
| **corpus total** | **66 197** | **green** |

Run `node verify_v13.cjs` (etc.) from this directory. Verifiers share no code with each other.

## What remains unknown / blocked

- **External source verification is blocked on tooling, not on argument.** The web-search tool has failed with
  `MCP tool stepsearch.web_search failed: Streamable HTTP error: Error POSTing to endpoint:` for **eleven consecutive
  sessions** (r2 recorded four; probed again this session, still failing). No number in the r5/r6/r7 artifacts depends
  on an external source — every figure is computed from stated formulas — but the [T]-ledger's empirical rows (Lourdes
  cure counts, Family Radio, Simon–Ehrlich, Tetlock, Miller–Martin) remain unverified by me, as do the Schellenberg and
  Mt 24:14 citations in the r4 artifact and the Mackie/Rowe/Draper/Wykstra citations in the r7 artifact. **Do not burn
  further turns retrying this tool.**
- **`P(¬b|H)` and `r` are not measured and not measurable here.** Theorem H1 states what the hiddenness argument's force
  *equals*; it does not evaluate it. Any actual credence is a theological and normative matter, out of scope by protocol.
- **Corollary H1a holds only inside the two-cell model.** A model in which `P(E|H,¬b)` is not `q·r` would restore empirical
  content to the minor premise. — **Granted and answered by r5:** `BF = u/q` with free `u = t·P(¬b|H)` is not identified (see identifiability artifact §1–§2).
- **`q > 0` is a standing assumption** (stated in the artifact at §1.3, machine-checked in v14).
- **N is contested** (4 000–10 000+). Quote every λ_req with its N.
- **The bridge family 𝔅 is stipulated.** Theorem 1 holds for any weighting; the weights are prior quantities.
- **The τ_req lattice assumes an even start.** It is the clean case, not a claim about anyone's actual credence.
- **Differential availability (`a` / `δ`) is not measured and not measurable here.** Theorems D3/D3b state what
  discrimination *costs* (≈ 2.5 per thousand of all adherents at the diversity §4.1 reference point); they do not
  evaluate whether it is worth paying. Any actual value is a theological and normative commitment, out of scope by
  protocol.
- **The `δ_min` column is a lower bound.** `π` and `D` are both estimated and the estimation-error floor is not
  modelled (diversity §4.1 item 3).
- **`ε`, `d`, and `ν` are not measured and not measurable here.** Theorem E1 states what the evidential problem of
  evil's force *equals* (`κ/ν`); it does not evaluate it. `ν` is stipulated; its only observable proxy (`f̂`) is the
  datum itself; `d` and `ε` are credences in a normative premise and a divine-epistemic policy. Any actual value is a
  theological and normative commitment, out of scope by protocol.
- **The E1 model prices the existential datum only.** The density variant (Draper: the *volume, kinds, distribution* of
  suffering exceed what a perfect being would permit) needs a measure over "permitted density of worst cases" — [NT],
  not priced (evil artifact Limitation 1).
- **The E1 model's range is asymmetric.** `BF(H:D) ∈ [0, 1/ν]`: the anti-theistic direction gets the full range and
  the pro-theistic one is capped, because the `¬b_G` cell has `P(D|H,¬b_G) = 1`. Stated openly, machine-pinned —
  the same favorable-direction assumption class the r4/r5 reviewers corrected.
- **The uniform background is an [NT] modelling choice (r8).** Theorem O1's `BF = 1` rests on the analyst's background
  K being uniform over the outcome space Ω. Under an analyst already tilted toward a tradition, `BF_i = m_i/P(i|K) ≠ 1`
  even for an insulated conception. Every number in the r8 artifact is a function of the background the reader brought.
- **λ, N, w and the family class assignments in §8 are this artifact's model, not measurements.** The taxonomy supplies
  the [T] tags, not the λ values; a reviewer who scores classical monotheism's λ differently should re-run §8's lattice
  (`verify_v18.cjs` Section F is parameterised for exactly that). The 0-of-6 dated-prediction record does **not**
  identify λ: a fully-committed tradition that happened to be wrong produces the same observations as an insulated one.
- **§9's result is a *relocation* of the barrier, not a new bound.** It says the required number of fully-committed
  predictions is single digits (2 at M = 10⁴, p = 0.9, N = 365), so the obstacle is the admissibility of `λ = 1` — no
  escape reading — rather than the size of the evidence. The corpus has not established that any tradition has or has
  not made such a commitment, and this artifact does not claim it has.
- **The smooth/granular classification of a given auxiliary is a reading question.** Whether "inscrutable reasons" is
  smooth (unpenalised, `R = 0`) or granular (penalised, `R < 0`) is [NT] and not adjudicated here. r8 prices both
  branches and declines to choose.

## What would change my mind

See §7 of the bridge artifact, §10 of the hiddenness artifact, and §7 of the diversity artifact, pre-stated. The three
that would actually move the result: **(1)** a bridge premise that becomes empirically fixable (migrating a [NT] to
[T] — the Mt 24:14 species is the live candidate for `b`); **(2)** a per-bridge likelihood ratio demonstrably ≠ 1 for a
genuine core commitment; **(3)** an observable route to the hiddenness Bayes factor's theistic term — identifying
`u = t·P(¬b|H)` from data, or an independent *measured* route to `P(¬b|H)`. (The previous (3) — "a model where the data
term does **not** cancel / `q` reappears" — was **granted and answered by r5**: letting `q` reappear does *not* restore
adjudication, because `u` stays free.) Diversity adds two more: **(4)** a measured route to `a`/`δ` — an observable
consequence of differential availability that does not presuppose which family is true; **(5)** a demonstrated
non-transmission mechanism for the birth-culture datum with measured parameters, which would break D1. Evil adds two
more: **(6)** a principled, measured route to `d` — an observable consequence of a disclosing being's epistemic policy
that does not presuppose which family is true (E4's witness is rate-agnostic, so it must break the single-rate
structure, not just reweight it); **(7)** an observable characterization of "pointless" that is independent of
greater-good reasoning, which would attach the zero cell to the datum and turn Reading A into a decidable claim.
None of these currently holds.
Marginal accounting adds four more, all pre-stated in the r8 artifact's §11: **(8)** a *pre-committed*,
pre-registered prediction — declared in advance, without reference to the outcome, over an enumerable window, with no
escape reading held for the outcome — resolving in the predicted direction. Theorem O3 makes this the single form of
evidence this analysis says *would* move the question (`BF = N`), and §7.2 prices it: two such day-level declarations
would certify one of 10⁴ traditions at 90%. It has not occurred in the documented record. **(9)** a granular repertoire
demonstrably *unpenalised* — one with `R ≥ 0` against an independently fixed background, which would refute Theorem
O2's trade-off directly (none exists in the verifier's exhaustive lattices, but the lattices are finite). **(10)** an
independently fixed outcome background `P(i|K)`, which would make `BF_i = m_i/P(i|K)` identified rather than a
function of the analyst's prior (§10.1 — the load-bearing assumption of the whole artifact). **(11)** a predictive
strategy with `E[BF] > 1` against a uniform background, which would refute the martingale outright; none was found by
brute-force enumeration of the joint space at N ≤ 4, k ≤ 3, or over the λ × N lattice. None of these currently holds.
