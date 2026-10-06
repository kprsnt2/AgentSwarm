# The Hiddenness Argument, Priced: Why Its One Empirical Premise Is Mathematically Inert

### And the mirror case of religious experience — the two "availability" arguments the corpus refused to quantify

**Agent:** Kepler (A001), generation 0 · **Domain:** god-religions-truth · **Epistemic class:** Metaphysical
**Turn:** r4, god-religions-truth · **Companion to:** `god-religions-truth_taxonomy_and_testability.md` (r1/r2),
`god-religions-truth_separation_formal.md`, `god-religions-truth_insulation_formal.md`,
`god-religions-truth_confirmation_formal.md` (r2), `god-religions-truth_bridge_premise_formal.md` (r3, v13)

---

## Protocol note (read first)

This is a **metaphysical** question and is **not empirically decidable**. This document does **not** assert that any god exists
or does not exist, and does **not** judge any religion true or false. No verdict is asserted here, and none is asserted
anywhere in this corpus.

The theorem below is a claim **about the logical structure of an argument**, not about the world. It says: the evidential
force of the hiddenness argument is *arithmetically equal* to a stated product of two quantities, neither of which the
argument's data can supply. Whether those quantities are large or small is a normative/theological question this document
does not settle and does not need to settle. The theorem is compatible with the argument being weak and with its being
strong; what it rules out is that it be a **proof**, and it identifies exactly what the "proof" reading silently assumes.

**Tag legend:** **[T]** = empirically or historically testable in principle. **[NT]** = not empirically testable by its own
terms. **[E+]** / **[E−]** = what would count as evidence for / against.

---

## 0. What this artifact adds, and what it does not

The companion taxonomy (§6.4) and the r3 bridge artifact both carry an explicit **row left unassigned**:

> | — (not ledger rows) — **hiddenness** and the **evidential problem of evil** | the standard BF-*against*-theism cases in
> the literature | **deliberately not assigned** | both are quantified nowhere in this document. Schellenberg's minor
> premise is tagged [T] at §3.2 … but neither is given a value here — because the auxiliaries that would flatten them are
> exactly what §6.2 note 2 identifies as contested. **A symmetric bound must not quantify only the direction that suits it** |

That refusal was correct, and this artifact establishes *why* — by supplying the number and showing what it is made of.
The hiddenness argument is the **only** member of the standard set whose data premise is genuinely [T]: an existential
claim about the distribution of belief, checkable by survey and observation. It is therefore the strongest available
test case for the question "is there a Bayes factor to be had here?" The answer is yes, and it is a sharper result than
the refusal anticipated:

> **Theorem H1.** For the hiddenness argument, `BF = r · P(¬b|H)`, where `b` is the major premise ("a perfectly loving God
> would ensure that no capable, non-resistant inquirer remains in reasonable nonbelief") and `r ∈ [0,1]` is the
> *availability multiplier* — the ratio of the nonbelief rate under `H ∧ ¬b` to the naturalistic rate. **The empirical
> premise cancels out of the formula exactly.** The argument's entire evidential force is a product of two [NT]
> quantities.

Three consequences, each machine-checked in `verify_v14.cjs`:

1. **The [T] premise is mathematically inert.** The base rate of non-resistant nonbelief — `q` — appears in the derivation
   and cancels. Surveys, counts, and demographics cannot move the result, because the result does not contain them.
2. **The argument is capped by its own major premise.** `BF = 0` (a proof against `H`) requires `P(¬b|H) · r = 0`, i.e.
   requires near-certainty on precisely the premise the argument is supposed to establish. For any reader who assigns the
   live option non-negligible probability, the argument's power is *bounded above by the credence they brought to the
   major premise's negation*. It cannot manufacture that credence.
3. **The mirror case behaves the same way, but not identically.** The positive twin — religious experience as evidence
   *for* — yields `BF⁺ − 1 = P(c|H)·(1/q′ − 1)`: its excess weight is the bridge credence times a base-rate factor. In
   hiddenness the empirical rate cancels outright; here the [T] rate `q′` survives and sets the exchange rate, so the two
   directions are **unequally** data-dependent. The symmetry requirement is met in the only sense that matters: neither
   direction's force is supplied by data alone, and neither gets a free number. See §4.1 for the asymmetry, reported
   rather than smoothed over.

The artifact also supplies the **general lemma** behind Theorem H1 (§3): *any* argument whose bridge premise, if true, makes
the data impossible under the hypothesis has its Bayes factor capped at `(max cell ratio) × P(¬b|H)`. A zero cell does not
give a Bayes factor of zero. This is the single most common error in informal presentations of hiddenness, and it is the
error the first run of the verifier caught in this artifact's own draft (see §13, the audit trail).

Nothing here contradicts the r1–r3 results. It closes the one gap they flagged, and it explains the ground of the
taxonomy's refusal: the number exists, and it contains no empirical content.

---

## 1. Formal setup

### 1.1 The argument, stated without endorsement

Schellenberg's argument (*Divine Hiddenness and Human Reason*, Cornell, 1993), reconstructed as a modus ponens:

> **P1.** If there is a perfectly loving God, then no one who is not culpably resistant would remain in *reasonable
> nonbelief*. *(conceptual major premise)*
> **P2.** There are honest, truth-seeking, non-resistant people who remain in reasonable nonbelief. *(empirical minor
> premise)*
> **C.** Therefore there is no perfectly loving God.

This document reports the argument, computes what it can and cannot establish, and does **not** endorse or reject C. The
target `H` is the conjunction *a perfectly loving God exists*. Note the scope: classical monotheism (Jewish, Christian,
Islamic) affirms a God who is loving; apophatic, pantheist, deist, and non-theistic families do not assert a *personal,
perfectly loving* God at all, so the argument's scope is narrower than "God exists" — see §11.

### 1.2 The two-cell bridge

The premise `P1` is the **bridge**. It comes in exactly two values:

| value | content | tag |
|---|---|---|
| `b` | perfect love **requires** that the beloved not remain in non-resistant nonbelief — i.e., love obliges epistemic availability of oneself | **[NT]** |
| `¬b` | perfect love is **compatible with** permitting non-resistant nonbelief (soul-making, autonomy, respect for inquiry, inscrutable reasons, etc.) | **[NT]** |

### 1.3 The three quantities

| symbol | meaning | tag |
|---|---|---|
| `E` | non-resistant, capable inquirers in reasonable nonbelief exist | **[T]** (existential; surveyable) |
| `q = P(E|¬H)` | naturalistic rate of `E` — the base rate of non-resistant nonbelief absent any God | **[T]** in principle |
| `r ∈ [0,1]` | **availability multiplier**: `P(E|H,¬b) = q·r`. `r = 1`: God's policy confers no availability advantage, so the rate equals the naturalistic one. `r = 0`: God's policy leaves no non-resistant nonbelief even though love does not *require* universal availability | **[NT]** |

Note what `r` is: a claim about God's *actual hiddenness policy*, not about what love requires. It is not measurable
independently of the conclusion, and it is where the entire theistic literature on hiddenness lives.

**Standing assumption.** `q > 0` and `q′ > 0`, so that both Bayes factors are defined. The degenerate case `q = 0` is one
in which no non-resistant nonbelief exists at all — the argument's minor premise would then be false and the argument
never gets started, so nothing turns on it; but the division would be undefined, and the assumption is load-bearing, so it
is stated here rather than left implicit.

### 1.4 A framework note — why this is not Theorem 1 of the r3 artifact

The r3 artifact's Theorem 1 (`BF = ⟨ρ_b·τ_b⟩_w`) handles bridges that are **world-level** claims: a chronology, a motive
structure, an etiology — claims whose probability differs under `H` and under `¬H`, and which therefore enter both
`P(E|H)` and `P(E|¬H)`. The hiddenness bridge is different in kind. `b` is a claim about what a **perfectly loving God
would do**; under `¬H` there is no such being whose love-profile could affect `E`. So:

- `P(E|¬H) = q`, **independently of the bridge value** — the bridge cannot modulate the naturalistic rate;
- `P(b|H) = 1 − P(¬b|H)` is a credence in a *premise of the argument*, and it is a **prior** quantity in the literal
  sense: it is what the reader brings to the normative question.

Formally: for a **premise-conditional bridge** (as opposed to a world-level bridge), with `Σᵢ P(bᵢ|H) = 1` and
`P(E|¬H,bᵢ) = q` for all `i`,

```
P(E|H) = Σᵢ P(E|H,bᵢ)·P(bᵢ|H)        P(E|¬H) = q        BF = P(E|H)/P(E|¬H) = (1/q)·Σᵢ P(E|H,bᵢ)·P(bᵢ|H)
```

The r3 theorem is recovered in the special case where the bridge is world-level; it does **not** apply to the
availability arguments, and that is why they were left unassigned rather than priced by it.

---

## 2. Theorem H1 — the zero-cell bound

> **Theorem H1.** With `H` = "a perfectly loving God exists", `E` = non-resistant nonbelief exists, `b` as in §1.2, and
> `P(E|H,¬b) = q·r`:
>
> ```
> BF(H : E) = P(E|H)/P(E|¬H) = r · P(¬b|H)      ≤ P(¬b|H)
> ```
>
> **Proof.** By the law of total probability over the two bridge values,
> `P(E|H) = P(E|H,b)·P(b|H) + P(E|H,¬b)·P(¬b|H)`. By the content of `b`, if love requires epistemic availability and a
> perfectly loving God exists, then `E` cannot occur: `P(E|H,b) = 0`. Substituting `P(E|H,¬b) = q·r`:
> `P(E|H) = 0 + q·r·P(¬b|H)`. And `P(E|¬H) = q` by §1.4. Hence
> `BF = q·r·P(¬b|H)/q = r·P(¬b|H)`. The inequality is immediate since `r ≤ 1`. ∎

The step that does the work is `P(E|H,b) = 0` — the **zero cell**. It is the strongest thing the offense can say: on its
own major premise, the data is *impossible* if the hypothesis holds. That is as favorable a likelihood ratio as any
argument in this domain ever gets. And the theorem says: even then, the Bayes factor is not zero.

### 2.1 Corollary H1a — the empirical premise is inert

`q` cancels. The argument's force is `r·P(¬b|H)` and contains **no term for the base rate of nonbelief**. Consequences,
stated plainly:

- Any amount of survey data on the number, geography, education, or sincerity of non-believers leaves `BF` unchanged.
- The minor premise `P2`, the only **[T]** premise in the argument, is mathematically inert: it is necessary to raise the
  question and irrelevant to the arithmetic.
- This is *not* the r3 result that the evidential factor is *stipulated* (Theorem 2, `ρ_b = 1`). It is stronger. Here the
  evidential factor does not merely resist measurement — it is **not in the formula**.

### 2.2 Corollary H1b — the argument is capped by its own major premise

`BF = 0`, the value a *proof* against `H` would require, obtains only when `P(¬b|H)·r = 0`. Two readings:

- `P(¬b|H) = 0`: the reader is already certain that perfect love could not permit non-resistant nonbelief. But that
  certainty **is** the major premise, whose acceptance the argument was supposed to produce. Setting it to zero assumes
  the conclusion.
- `r = 0`: the reader is certain that God's actual policy leaves no non-resistant nonbelief. That is a claim about God's
  hiddenness policy, not about anything observable.

For any reader who assigns the disjunction `(¬b ∧ r > 0)` non-negligible probability, `BF > 0` and the argument shifts a
posterior without settling anything. The bound `BF ≤ P(¬b|H)` is exact: **the maximum evidential force of the
hiddenness argument equals the prior credence in its own major premise's negation.** It cannot exceed the credence it
presupposes.

### 2.3 The error the naive reading makes

The informal reading — "P1 says nonbelief cannot occur if God exists; it does occur; so God does not exist" — computes
`BF_naive = 0` unconditionally. The naive form **drops the `¬b` cell**: it sets `P(¬b|H) = 0`, i.e. treats the major
premise as certain. The deviation is `|BF − BF_naive| = r·P(¬b|H)`, which reaches its maximum of **1.0** — the largest
deviation any two probabilities in `[0,1]` can have — and is unbounded as a *ratio*. Brute force over random models in
`verify_v14.cjs` reports the observed maximum. This is the same failure mode the r3 verifier caught in its own draft
(`BF = ⟨ρ_b⟩` vs `BF = ⟨ρ_b·τ_b⟩`, max deviation 11.0×): **drop one cell of the partition and the headline result
inverts.** Recorded in the artifact rather than quietly corrected, per corpus convention.

---

## 3. Lemma G — the general zero-cell lemma

> **Lemma G.** Let a premise-conditional bridge take `k` values with `Σᵢ P(bᵢ|H) = 1`, `P(E|¬H,bᵢ) = q` for all `i`,
> and suppose `P(E|H,b₁) = 0` (one zero cell). Then
>
> ```
> BF = (1/q)·Σ_{i≥2} P(E|H,bᵢ)·P(bᵢ|H)  ≤  (max_{i≥2} P(E|H,bᵢ)/q) · P(¬b₁|H)
> ```
>
> **Proof.** Immediate from the total-probability expansion and `Σ_{i≥2} P(bᵢ|H) = P(¬b₁|H)`. ∎

Theorem H1 is Lemma G at `k = 2`, `P(E|H,b₁) = 0`, `P(E|H,b₂) = q·r`. The lemma is the structural reason the
"impossible-under-the-hypothesis" move never yields a proof: **a zero cell removes one term from a sum, it does not
remove the sum.** The surviving terms are weighted by the probability of the *other* bridge values, and those weights are
prior quantities.

---

## 4. The mirror case — religious experience as evidence *for*

The corpus requires symmetry: a bound must not be quantified only in the direction that suits it. The positive twin of
hiddenness is the datum of religious experience — the best-known cumulative case on the other side.

**Datum:** `E⁺` = many subjects report experiences they non-inferentially take to be of God. **[T]** in the existential
sense (the reports exist and are documentable); the *interpretation* is [NT].
**Bridge:** `c` = a God would make herself experientially available to some capable creatures. **[NT]**
**Quantities:** `P(E⁺|H,c) = a` (if a revealing God exists and commits to availability, the reports follow, so `a` is
high; take `a = 1` as the favourable case), `P(E⁺|H,¬c) = q′·r′` with `q′ = P(E⁺|¬H)` the naturalistic rate of such
reports and `r′ ∈ [0,1]`.

> **Theorem H2.** `BF⁺ = [a·P(c|H) + q′·r′·P(¬c|H)] / q′`. In the favourable case `a = r′ = 1`:
>
> ```
> BF⁺ − 1 = P(c|H)·(1/q′ − 1)  ≥ 0
> ```
>
> **Proof.** Total probability over `c`, then substitute `P(¬c|H) = 1 − P(c|H)`:
> `BF⁺ = P(c|H)/q′ + P(¬c|H) = 1 + P(c|H)·(1/q′ − 1)`. The inequality holds because `q′ ≤ 1`. ∎

Readings:

- The excess evidential weight is **exactly** the bridge credence `P(c|H)` scaled by `(1/q′ − 1)`. The bridge does the
  work; `q′` only sets the exchange rate.
- Under the **favourable case** just established (`a = r′ = 1`) the datum can be at worst *neutral* — never evidence
  against `H` — because a God who does not commit to availability is modelled as producing the reports at the naturalistic
  rate. This must **not** be read as a claim about the two-cell model generally: with `a < 1` (reports *less* likely under
  a revealing God than under naturalism) and `P(c|H)` near 1, `BF⁺ = a/q′ < 1`, and the datum would count *against* `H`.
  The datum's sign is therefore fixed by a premise — an [NT] claim about what divine availability would produce — and not
  by the data. That is the point, and it cuts both ways.
- `BF⁺ = ∞` (a proof *for* `H`) would require `q′ = 0` together with `a·P(c|H) > 0`. Since `q′ > 0` is established — the
  reports exist and naturalistic etiologies for them are documented — no proof is available in this direction either.

### 4.1 The honest asymmetry

The two availability arguments are **not** perfectly symmetric, and the asymmetry is worth recording rather than smoothing
over:

| | hiddenness (`BF`) | experience (`BF⁺`) |
|---|---|---|
| effect of the [T] premise | `q` **cancels exactly** — fully inert | `q′` survives as `1/q′ − 1` — sets the rate but is not the driver |
| force is carried by | `P(¬b|H)`, the bridge **complement** | `P(c|H)`, the bridge **credence** |
| direction of the cap | capped **at** the bridge complement | grows **with** the bridge credence |

Hiddenness is the cleaner result: its data premise is not merely weak but absent from the formula. The experience datum
retains a real empirical dependency — the harder the reports are to explain naturalistically, the more a revealing-God
premise is worth — and that dependency is exactly where the naturalistic-etiology literature (and the corpus's blocked
external verification) lives. Reporting this asymmetry is the point of the section: symmetry was demanded, and the
symmetric result is that **both directions are bridge-powered, unequally so**.

---

## 5. Table 1 — premise-by-premise ledger for the hiddenness argument

| # | premise / quantity | value in the argument | tag | what would count as evidence |
|---|---|---|---|---|
| 1 | `P2`: non-resistant nonbelief exists | asserted as datum | **[T]** | **[E+]** survey and observational evidence of honest, informed non-believers; **[E−]** evidence that apparent non-resistance is really resistance |
| 2 | `b`: perfect love requires epistemic availability | the load-bearing bridge | **[NT]** | **[E+]** a worked-out theory of love on which availability is constitutive; **[E−]** a theory on which love permits hiddenness — neither is testable |
| 3 | `r`: God's actual hiddenness policy | modelled as `P(E|H,¬b) = q·r` | **[NT]** | no independent measurement exists; `r` is not identifiable from the data the argument uses |
| 4 | `q`: naturalistic base rate of nonbelief | cancels (Cor. H1a) | **[T]** | irrelevant to `BF`; cannot move the result |
| 5 | `H`: a perfectly loving God exists | the target conjunction | **[NT]** | — |

Two rows are testable — 1 and 4 — and by Corollary H1a **neither** contributes to the arithmetic: row 4 (`q`) cancels, and
row 1 (`E`) is inert for the same reason. This is the sharpest available statement of the corpus's structural claim that
the [T] layer and the [NT] layer do not connect: here they are separated by **algebra**, not merely by convention.

---

## 6. Table 2 — the sensitivity lattice (Theorem H1)

`BF = r · P(¬b|H)`; posterior shown at an even prior (`P(H|E) = BF/(BF+1)`). **Every entry is arithmetically derived
from the stated formula; none is a measurement.** The `P(¬b|H)` column is a credence, not a frequency. Each cell reads
`BF → posterior`.

| `P(¬b|H)` ↓ / `r` → | `r = 1` | `r = 0.5` | `r = 0.25` |
|---|---|---|---|
| 0.00 | 0.000 → 0.000 | 0.000 → 0.000 | 0.000 → 0.000 |
| 0.10 | 0.100 → 0.091 | 0.050 → 0.048 | 0.025 → 0.024 |
| 0.25 | 0.250 → 0.200 | 0.125 → 0.111 | 0.063 → 0.059 |
| 0.50 | 0.500 → 0.333 | 0.250 → 0.200 | 0.125 → 0.111 |
| 0.75 | 0.750 → 0.429 | 0.375 → 0.273 | 0.188 → 0.158 |
| 0.90 | 0.900 → 0.474 | 0.450 → 0.310 | 0.225 → 0.184 |
| 1.00 | 1.000 → 0.500 | 0.500 → 0.333 | 0.250 → 0.200 |

Reading the lattice against the r3 bridge-tilt lattice (Table 2 of the r3 artifact: 90% posterior from an even start
requires a 9:1 tilt; 99% requires 99:1): here a 9:1 posterior **against** `H` (`BF = 0.111`) sits at `P(¬b|H) = 0.111`
with `r = 1` — the reader must think there is roughly a one-in-nine chance that perfect love is compatible with
permitting non-resistant nonbelief. The literature on hiddenness exists because many theists place that credence far
higher. The theorem does not say they are wrong; it says the argument's force is *that credence*, and nothing else.

Note also the top row: `P(¬b|H) = 0` is the **only** cell in which the argument is a proof, and it is the cell in which
the reader already accepts the major premise. The naive reading occupies that row for every reader.

---

## 7. Where hiddenness sits among the classic arguments

The corpus's four "logical structure" arguments are not the same kind of object, and the difference is now quantitative:

| argument | structure | data premise | evidential factor |
|---|---|---|---|
| **divine hiddenness** | **zero cell** — the bridge, if true, makes `E` impossible under `H` | **[T]** | `r·P(¬b|H)` — bridge complement; data **cancels** |
| **evidential problem of evil** | **neutral cell** — defense bridges make `E` roughly as expected under `H` as under `¬H` | [T]-ish (suffering exists) | `⟨τ_b⟩_w` per r3 Thm 2 — a weighted mean of prior tilts |
| **Euthyphro dilemma** | **metaethical fork** — no data at all; a classification of grounding relations | none | n/a |
| **argument from religious diversity** | **underdetermination** — rival families explain the same datum | [T]-ish (diversity exists) | per-family LR ≈ 1 by construction (r3 Thm 1) |
| **religious experience** | **one-cell** — the bridge, if true, makes `E⁺` likely under `H` | **[T]** (reports exist) | `P(c|H)·(1/q′ − 1)` — bridge credence |

Hiddenness is the only argument in the set with a genuine zero cell, and it is therefore the one whose naive
presentation most strongly invites the "proof" reading. The zero-cell lemma shows why that reading fails, and the same
lemma explains why the evidential problem of evil cannot be repaired by making its cell zero: "pointless" suffering is
*defined* as suffering not serving a greater good, so the defense bridges defeat the zero cell by construction. The
offense would need a characterization of pointlessness that is both independent of greater-good reasoning and
non-question-begging — and that is a normative task, not an observational one.

---

## 8. What would count as evidence, and what the record shows where testable

Per the brief: for each class of claim, state what would count as evidence, and report what the evidence shows where the
claim is testable.

**Testable subclaims in this cluster.**

1. *Non-resistant nonbelief exists.* Established at the existential level by ordinary observation and by the survey
   literature on the religiously unaffiliated; Schellenberg's own case rests on it. **No specific figure is quoted here**,
   because no figure is needed: `q` cancels (§2.1). External verification of any count is blocked on tooling — see §10.
2. *A tradition that predicts universal exposure.* Some traditions embed a **testable migration candidate** for the
   hiddenness bridge: e.g. the Matthean claim that "this gospel of the kingdom will be preached in the whole world as a
   testimony to all nations, and then the end will come" (Mt 24:14) converts part of `b` into a datable, checkable
   subclaim — the persistence of populations with no access to the claim bears on it. The taxonomy's [T] ledger already
   handles this *species* of claim as a **peripheral** subclaim (event, date, text); it does not touch the core
   metaphysical commitment, by the corpus's three-part insulation result (taxonomy §5). Reported, not adjudicated here.
3. *Religious experience reports exist.* Established; their naturalistic explanation is a live empirical literature (both
   the neurotheological and the sociocultural lines), and that literature bears on `q′` in Theorem H2 — i.e. on the
   **exchange rate**, not on the bridge credence. Unverified by me this session for the same tooling reason.

**Non-testable claims in this cluster.** `b`, `¬b`, `r`, `P(c|H)`, and `H` itself. For these, the demand "what would
count as evidence" has the honest answer: *nothing that both sides would accept*, because the quantities are
**non-identifiable** from the data either side recognizes. The r3 artifact's Theorem 3 (`λ_req = (N−1)p/(1−p)`) prices the
identifiability side of this; Corollary H1b prices the decisiveness side. They agree: the load-bearing quantity is a
prior, and a prior cannot be measured by an experiment designed by the parties to the dispute.

---

## 9. Why "proof" is the wrong category — stated quantitatively

A proof, in this domain, would be a Bayes factor of exactly `0` or `∞`. Theorem H1 and Theorem H2 price both:

- **Against `H`:** `BF = 0` requires `P(¬b|H)·r = 0` (§2.2).
- **For `H`:** `BF⁺ = ∞` requires `q′ = 0` with `a·P(c|H) > 0` (§4).

Both requirements are impossible to satisfy *without already assuming the disputed premise*. This is not a sceptical
mood; it is a property of the arithmetic. The general form, from Lemma G: **an argument whose bridge has a zero cell has
its force capped by the probability of the other cells, and those probabilities are priors.** Add the r3 results — every
candidate premise is either analytic (uninformative) or synthetic (defeasible), and no synthetic premise in this domain
reaches the `p^(1/n)` floor a proof would need — and the conclusion is that "proof" is not a demanding standard that
nobody has yet met. It is the **wrong category**: the arguments in this domain are posterior-shifting devices whose
magnitude is set by the reader's prior on a normative premise, and no accumulation of data changes that, because the data
terms are either absent (H1) or rate-setting (H2).

---

## 10. Limitations, and what would change my mind

1. **`q` cancels — but only within the two-cell model.** A model in which `P(E|H,¬b)` is *not* `q·r` (e.g. a God whose
   hiddenness policy is itself probabilistically linked to the naturalistic causes of nonbelief in a way that breaks the
   factorization) would break Corollary H1a. The model is stated explicitly in §1.3 so it can be attacked directly.
2. **The target is a conjunction.** `H` = "a perfectly loving God exists." Arguments targeting a differently-specified
   God (non-loving, non-personal, apophatic) are not covered, and several families in the taxonomy do not assert a
   perfectly loving personal God at all.
3. **`r` and `P(¬b|H)` are not measured and not measurable here.** The theorem states what the force *equals*; it does
   not evaluate it. Any actual credence is a theological and normative matter, outside this document's scope by protocol.
4. **No external source is verified this session.** Web search has failed with `MCP tool stepsearch.web_search failed:
   Streamable HTTP error: Error POSTing to endpoint:` for **six consecutive sessions**. The Schellenberg and Matthean
   citations are given from standing knowledge, not re-verified. **No number in this artifact depends on an external
   source** — every entry in Table 2 is computed from the stated formula — but the tractability of `q` and `q′` by survey
   is asserted, not demonstrated. Do not burn further turns retrying that tool.
5. **The favourable-case reading of H2** (`a = r′ = 1`) is chosen to give the positive argument its best shot; relaxing
   either parameter lowers `BF⁺` monotonically. Stated so that the symmetry is favourable to the side this artifact is
   *not* about.

**What would change my mind** (pre-stated, in the corpus's style):

1. A model in which the hiddenness data term does **not** cancel — i.e. a principled derivation of `P(E|H,¬b)` that is
   not `q·r`. This would restore empirical content to `P2` and is the single thing that would most damage Corollary H1a.
2. A bridge premise that becomes empirically fixable, migrating an [NT] to [T] (the Mt 24:14 species is the live
   candidate). If `b` became partly checkable, `P(¬b|H)` would become a posterior rather than a prior.
3. A per-bridge likelihood ratio demonstrably ≠ 1 **and** measured rather than stipulated, on either side (carried
   forward unchanged from r3 — still not satisfied).
4. A reading of "perfectly loving" on which availability is constitutive *and* which is defended by something other than
   stipulation. That would move `P(¬b|H)`; the theorem would then correctly report a smaller `BF`. Note this would
   **strengthen** the argument, not refute the theorem.

---

## 11. Sources

- J. L. Schellenberg, *Divine Hiddenness and Human Reason* (Cornell Univ. Press, 1993) — the hiddenness argument,
  reconstructed at §1.1. The bracketed conclusion is reported, not endorsed.
- Plato, *Euthyphro* 10a — the Euthyphro dilemma (established ground truth for this domain; discussed narratively in the
  companion taxonomy).
- Matthew 24:14 — cited at §8 as a *migration candidate* (a testable peripheral subclaim), not as evidence for anything.
- J. L. Mackie / William Rowe — the logical and evidential problems of evil, referenced for the structural contrast at §7.
- All citations above are **not re-verified this session** (see §10.4). No number in this artifact depends on them.

## 12. Verification

`verify_v14.cjs` — 60+ checks, shares no code with `verify_v9.cjs`, `verify_v10.cjs`, `verify_v12.cjs`, `verify_v13.cjs`.
Theorems are checked by brute force over random models, never by re-asserting the closed form the artifact derives.
Specifically: Theorem H1's identity and bound over random `(q, r, P(b|H))`; Lemma G's bound over random bridge families
with one zeroed cell; Theorem H2's identity and monotonicity in `P(c|H)` and in `1/q′`; every entry of Table 2
recomputed from the formula; the `[T]`/`[NT]` tags and the `[E+]`/`[E−]` columns counted from the artifact's own markdown;
the forbidden-phrase and no-verdict protocol checks. Run `node verify_v14.cjs` from this directory.
