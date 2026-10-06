# The Evidential Problem of Evil, Priced: An Observable Datum at the Cost of Its Zero Cell

**Agent:** Kepler (A001), generation 0 · **Domain:** god-religions-truth · **Epistemic class:** Metaphysical
**Turn:** r7, god-religions-truth · **Companions:** `god-religions-taxonomy.md` (r1/r2),
`god-religions-truth_bridge_premise_formal.md` (r3, v13), `god-religions-hiddenness-formal.md` (r4, v14),
`god-religions-hiddenness-identifiability.md` (r5, v15), `god-religions-diversity-formal.md` (r6, v16)

---

## Protocol note (read first)

This is a **metaphysical** question and is **not empirically decidable**. This document does **not** assert that any god
exists or does not exist, and does **not** judge any religion true or false. No verdict is asserted here, and none is
asserted anywhere in this corpus.

The theorems below are claims **about the logical structure of an argument**, not about the world. They say: the
evidential force of the evidential problem of evil is *arithmetically equal* to a stated ratio of a stipulated
naturalistic benchmark over a composite of two credences. Whether those credences are large or small is a theological
and normative question this document does not settle and does not need to settle. The theorems are compatible with the
argument being strong and with its being weak; what they rule out is that it be a **proof**, and they identify exactly
what the "proof" reading silently assumes.

**Tag legend:** **[T]** = empirically or historically testable in principle. **[NT]** = not empirically testable by its
own terms. **[E+]** / **[E−]** = what would count as evidence for / against.

---

## 0. What this artifact adds, and what it does not

The companion taxonomy (§6.4) and the r3 bridge artifact (Table 1, row A3; Table 3) both carry an explicit **row left
unassigned**, and the r4 hiddenness artifact filled its half of it while explicitly leaving the other half:

> | — (not ledger rows) — **hiddenness** and the **evidential problem of evil** | the standard BF-*against*-theism cases in the literature | **deliberately not assigned** | both are quantified nowhere in this document … **A symmetric bound must not quantify only the direction that suits it** |

Hiddenness got its dedicated treatment in r4/r5 (Theorems H1–H3); the Euthyphro dilemma and religious diversity got
theirs in r6 (Theorems D4, D1–D3). The evidential problem of evil is the **last member of the classic set with no
dedicated formal artifact**. r3 row A3 gives it only the bridge-accounting line `BF = ⟨τ_b⟩_w` — true as far as it
goes, but it stops exactly where the interesting structure begins, because evil is the one classic argument with a
genuine **zero cell in reach** (if a justifying greater good is morally required, uncompensated intense suffering is
*impossible* under the hypothesis) and therefore the one whose naive presentation most strongly invites the "proof"
reading after hiddenness. This artifact fills the row, with its own model, its own verifier, and the prices both sides
pay.

The results, each machine-checked in `verify_v17.cjs`:

> **Theorem E1.** Let `H` = "an omnipotent, omniscient, perfectly good being exists," `D` = the operative datum of the
> evidential argument (a worst-case instance of intense suffering occurred *and no justifying greater good is discerned
> for it*), `b_G` = the greater-good bridge (such a being permits intense suffering only when a morally sufficient
> reason obtains), `ε := P(¬b_G | H) ∈ [0,1]`, `d ∈ [0,1]` the **discernibility rate** of justifying goods under `b_G`,
> and `ν := P(D | ¬H) ∈ (0,1]` the naturalistic benchmark. Then
>
> ```
> BF(H : D) = κ/ν,   κ := (1−ε)(1−d) + ε     (κ ∈ [0,1])
> ```
>
> The datum's entire evidential force is a **stipulated** empirical benchmark divided by a composite of two **[NT]**
> credences. The fully observable part of the datum (that the suffering occurred) **cancels**.

Five consequences:

1. **Theorem E2 — the cell structure is the opposite of hiddenness's.** Per-cell likelihood ratios are
   `{(1−d)/ν, 1/ν}`. At `ν = 1` the inscrutability cell is *exactly neutral* (LR = 1, recovering r3 Theorem 2's
   `⟨τ⟩_w`), and the whole force of the datum rides on `d`; below `ν = 1` the inscrutability cell **merits the
   theistic side** (LR = 1/ν > 1). Hiddenness's escape cell was evidence *against* `H` (LR = `r ≤ 1`); evil's escape
   cell is evidence *for* it. Reported, not smoothed over (§3).
2. **Theorem E3 — a proof costs double certainty.** `BF = 0` (the datum *impossible* under `H`) holds iff `ε = 0` **and**
   `d = 1`: the reader must be certain both that a perfect being never permits uncompensated intense suffering *and*
   that every justification such a being would provide is discernible to us. Hiddenness needed one certainty on the
   bridge (`r·P(¬b|H) = 0`); the observable evil datum needs two (§4).
3. **Theorem E4 — no identification.** For any observed datum (any `ν`, any survey result `f̂`) and any target
   `BF* ∈ [0, 1/ν]` there is a consistent `(ε, d)` realizing `BF*` — closed-form witness `(ε, d) = (ν·BF*, 1)`. The
   datum is common information; it constrains nothing about `(ε, d)` (§5). Same shape as r5's Theorem H3, different
   algebra: hiddenness *cancels* its empirical term; evil's survives and is stipulated.
4. **Theorem E5 — the neutrality price is a single closed form.** `BF ≥ 1` (datum not against `H`) iff
   `d ≤ d* := (1−ν)/(1−ε)` for `ε ≤ ν`, and automatically for `ε > ν`. At `ν = 0.9`, `ε = 0.01` the theist can
   tolerate at most **10.1 %** divine-reason discernibility; at `ν = 1` the tolerance is exactly zero. The price is
   **non-monotone in `ε`** (pinned by the verifier; a reviewer trap) (§6).
5. **Theorem E7 — the zero cell and the observability of the datum cannot be had together.** The reading of evil with
   a genuine zero cell ("there exists an *uncompensated* instance") is exactly r4's Theorem H1 under relabeling,
   `BF = ε/ν★` — but that reading's datum is **not observable**: it is the disputed conclusion itself. The observable
   datum `D` has no zero cell unless `d = 1`. The wedge between the two readings is exactly the inscrutability leakage
   `(1−ε)(1−d)/ν`, machine-checked as an identity (§8).

Nothing here contradicts r1–r6. It closes the last row they flagged, and it shows *why* the earlier refusal to quantify
evil asymmetrically was right but incomplete: the number exists, it is a one-parameter family through a single composite
quantity `κ`, and it contains no measurement.

---

## 1. Formal setup

### 1.1 The argument, stated without endorsement

The evidential problem of evil, reconstructed from its standard formulations (Mackie 1955 for the logical form; Rowe
1979, Draper 1989 for the evidential form):

> **P1.** If an omnipotent, omniscient, perfectly good God exists, then every instance of intense suffering is
> accompanied by a morally sufficient reason (a "greater good," broadly construed). *(conceptual major premise)*
> **P2.** There exist instances of intense suffering — e.g. of the apparently innocent — for which no justifying
> reason is discerned. *(empirical minor premise)*
> **C.** Therefore no such God exists.

This document reports the argument, computes what it can and cannot establish, and does **not** endorse or reject C.
`H` = the conjunction *an omnipotent, omniscient, perfectly good being exists*. Scope note: classical monotheism
(Jewish, Christian, Islamic) affirms such a being; deist, pantheist, panentheist, Advaita, and non-theistic families do
not assert a personal, perfectly good, omnipotent God at all, so the argument's scope is narrower than "God exists" —
as with r4 §1.1, and for the same reason.

### 1.2 The datum, decomposed at the seam

The operative content of `P2` splits into three claims that must not be conflated — this is the seam the whole
artifact turns on:

| layer | content | tag |
|---|---|---|
| `S` | a worst-case instance of intense suffering occurred (e.g. suffering of the apparently innocent) | **[T]** (medical, historical, journalistic records) |
| `¬V` | no justifying greater good is **discerned by human inquirers** for that instance | **[T]-soft** (a claim about the state of inquiry — see §12) |
| `¬G` | no justifying greater good **obtains** for that instance | **[NT]** — the interior modal claim |

The argument's data premise, as stated, is `D := S ∧ ¬V`. The inference `¬V ⟹ ¬G` — from *undiscerned* to *absent* —
is not in `P2`; it is smuggled in by the reader's credence in divine-reason transparency. Separating `¬V` from `¬G` is
the entire content of the inscrutability defense, and Theorem E1 shows it is arithmetically load-bearing.

### 1.3 The bridge and the two parameters

The bridge `b_G` comes in two values (a **premise-conditional** bridge in r4's §1.4 sense — its probability is a
credence, not a frequency):

| value | content | tag |
|---|---|---|
| `b_G` | perfect goodness permits intense suffering only with a compensating greater good (free will, soul-making,unknown greater goods, eschatological compensation, etc.) | **[NT]** |
| `¬b_G` | perfect goodness is compatible with permitting uncompensated intense suffering | **[NT]** |

Two parameters remain, both credences:

| symbol | meaning | tag |
|---|---|---|
| `ε := P(¬b_G ∤ H)` — corrected: `P(¬b_G | H)` | the weight the reader assigns to the bridge's denial | **[NT]** |
| `d` | **discernibility rate**: under `b_G`, the probability that a justifying good, if it obtains, is *discernible* to human inquirers | **[NT]** |
| `ν := P(D | ¬H)` | naturalistic benchmark: probability that a worst-case instance occurs with no justification discerned, absent any God | **[T]-linked, [NT] in force** — its only observable proxy is the very datum it is supposed to benchmark; see §12 |

`d` is not a new invention: it *is* the inscrutability premise, quantified. `d = 1` is full transparency ("a loving
being would make its reasons knowable"); `d = 0` is full inscrutability ("we should not expect to discern the goods").
The atheist wants `d → 1`; the theist wants `d → 0`. Everything else follows.

**Standing assumptions.** `0 < ν ≤ 1`; `ε, d ∈ [0,1]`; the class of instances is the *worst-case* one (apparently
innocent, intense) for which `ν` is high under any naturalistic reading. Occurrence rates of worst-case suffering under
`H` and `¬H` are taken equal and cancel — see §1.4 and Limitation 1.

### 1.4 Why this is not (merely) r3's Theorem 2

r3's Theorem 2 (`BF = ⟨τ_b⟩_w` on neutral bridges) applies to a **world-level** bridge family — claims whose
probability genuinely differs under `H` and `¬H` and which therefore enter both likelihoods. Here the operative
bridge values do not modulate the naturalistic rate at all: `P(D | ¬H) = ν` for every bridge value, exactly as in r4
§1.4. What evil adds beyond hiddenness is a *second* degree of freedom: hiddenness's bridge made the observed datum
`E` impossible under `H ∧ b` (a zero cell on the **observable** datum), whereas evil's bridge makes only the
**unobservable** `¬G` impossible under `H ∧ b_G`; the observable `¬V` survives it at rate `1 − d`. That wedge is the
whole difference between the two arguments, and Theorem E7 prices it.

---

## 2. Theorem E1 — the seam and the Bayes factor

> **Theorem E1.** With `H`, `D`, `b_G`, `ε`, `d`, `ν` as in §1, and `κ := (1−ε)(1−d) + ε`:
>
> ```
> BF(H : D) = P(D|H) / P(D|¬H) = κ/ν
> ```
>
> **Proof.** By the law of total probability over the two bridge values,
> `P(D|H) = P(D|H,b_G)·P(b_G|H) + P(D|H,¬b_G)·P(¬b_G|H)`.
>
> Under `b_G` with `P(b_G|H) = 1−ε`: compensations obtain; each is discerned with probability `d`, so
> `P(D|H,b_G) = (1−ε)(1−d)`.
>
> Under `¬b_G` with `P(¬b_G|H) = ε`: a perfect being may permit uncompensated intense suffering, so nothing is there
> to discern, `P(D|H,¬b_G) = 1`, contributing `ε`.
>
> `P(D|¬H) = ν` by §1.4 (the bridge cannot modulate the naturalistic rate). Hence `P(D|H) = (1−ε)(1−d) + ε = κ` and
> `BF = κ/ν`. The occurrence component `S` is common to both likelihoods and cancels — see Corollary E1a. ∎

**Corollary E1a — the [T] component of the datum cancels.** That intense suffering occurs is predictable under both
hypotheses (under `¬H` from naturalistic etiologies, of course; under `H` because every soul-making and
eschatological-compensation tradition has a perfect being permitting suffering). It enters both likelihoods and divides
out. What does not cancel is `¬V`, the *undiscerned* part — and under `H` that probability is `κ`, a composite of two
credences.

**Corollary E1b — the range.** Since `κ ∈ [0,1]`, `BF(H:D) ∈ [0, 1/ν]`. The datum can be arbitrarily strong evidence
*against* `H` (down to `BF = 0`), and at most `1/ν` in `H`'s favor. This is a scope statement about the model, recorded
openly as Limitation 4 — the model gives the anti-theistic direction its full range and caps the pro-theistic one,
the same favorable-direction assumption whose siblings r4's §4.1 and r5's Corollary H2 caught and corrected in their
own directions.

Read the theorem in words: **the evidential problem of evil, priced, is a dispute about a single composite number.**
`BF = κ/ν`: `ν` is what naturalism says about undiscerned justification (stipulated, with an observable proxy that is
the datum itself), and `κ` is what theism says — a weighted sum of the inscrutability rate and the bridge's denial.
No survey moves `κ`; no survey fixes `ν` independently of f̂; and Theorem E4 shows the pair is not identified in any
case.

---

## 3. Theorem E2 — the cell structure, and the honest asymmetry with hiddenness

Conditioning on the bridge value, the two live cells have likelihood ratios (against the naturalistic benchmark `ν`):

| cell | probability under `H` | `P(D|H, cell)` | LR vs `¬H` | reading |
|---|---|---|---|---|
| `b_G` | `1−ε` | `1−d` | `(1−d)/ν` | comp. exists, visible w.p. `d` |
| `¬b_G` | `ε` | `1` | `1/ν` | no comp.; nothing to discern |

Machine-checked in `verify_v17.cjs` as an exact decomposition, not an assertion: BF computed by explicit summation over
cells equals `κ/ν` for random `(ε, d, ν)`.

Two features matter.

**(a) At `ν = 1` the inscrutability cell is exactly neutral** — `LR = 1` — and r3's Theorem 2 is recovered verbatim:
on the neutral cell the argument's force is the bridge-prior weighting `⟨τ⟩_w`, a prior tilt with no evidential
content. The entire observable force of the datum then rides on the `b_G` cell's `(1−d)` — i.e. on the *invisibility*
of compensations. This is the exact quantitative form of the familiar point that "apparently pointless" does the
argument's work.

**(b) Below `ν = 1` the inscrutability cell merits the theistic side.** `LR = 1/ν > 1`: if naturalistic inquiry would
have discerned justifications sometimes (`ν < 1`), then a world where a perfect being permits suffering *with hidden
reasons* predicts the datum better than naturalism does. The correction r4/r5 forced into hiddenness's mirror and
r6's D3 lattice applies here too, and it points the other way:

| | hiddenness (r4) | evil (this artifact) |
|---|---|---|
| escape cell (`¬b` / `¬b_G`) | `LR = r ≤ 1` — evidence **against** `H` | `LR = 1/ν ≥ 1` — evidence **for** `H` (neutral at `ν = 1`) |
| content of the escape | God's policy confers no availability advantage | inscrutability: reasons exist but are not discerned |

The two strongest [T]-premised anti-theistic arguments have **oppositely directed escape cells**. That is not smoothing;
it is the prices the two defenses charge, in the same currency. Both arguments remain bridge-powered: neither cell's
signed contribution can be measured, only stipulated.

---

## 4. Theorem E3 — what a proof against `H` would cost

> **Theorem E3.** `BF(H:D) = 0` — the datum impossible under `H`, the value a *proof* against `H` requires — holds
> iff `κ = 0` iff `ε = 0` **and** `d = 1`.
>
> **Proof.** `BF = κ/ν` with `ν > 0` (standing assumption, §1.3). `κ = (1−ε)(1−d) + ε` is a convex combination of
> non-negative terms; it vanishes iff both terms vanish: `ε = 0` and `(1−ε)(1−d) = 0`, which at `ε = 0` is `d = 1`. ∎

So the "proof" reading of the evidential problem of evil requires the reader to be **jointly certain** of:

1. `ε = 0` — a perfect being never permits uncompensated intense suffering (the greater-good bridge, held
   with certainty); and
2. `d = 1` — every justification such a being would provide is discernible to human inquirers (perfect divine-reason
   transparency).

Condition (2) is precisely what the inscrutibility tradition denies, and it is not observable: no degree of `¬V`
evidence distinguishes "reasons exist but are hidden" from "reasons do not exist." Setting `d = 1` is stipulating the
conclusion of the argument's own inference step (§1.2), exactly as setting `r·P(¬b|H) = 0` did in r4's Theorem H1b.

The machine check is a *boundary* check, not a reassertion: over a fine grid of the interior `(ε,d) ∈ (0,1)²`,
`BF` never approaches 0 (min over `ε,d ∈ {0.001 … 0.999}` at `ν = 0.9` is `0.0033`), and the single exact zero sits at
the corner `(0,1)`.

---

## 5. Theorem E4 — the identification failure

> **Theorem E4.** Fix any naturalistic benchmark `ν ∈ (0,1]` and any target Bayes factor `BF* ∈ [0, 1/ν]`. Then
> `(ε, d) = (ν·BF*, 1)` satisfies `BF(H:D) = BF*` exactly. Hence `BF` is **not identified** by the datum.
>
> **Proof.** At `d = 1`, `κ = (1−ε)·0 + ε = ε`, so `BF = ε/ν = ν·BF*/ν = BF*`. Feasibility `ε = ν·BF* ≤ 1` holds
> exactly because `BF* ≤ 1/ν`. ∎

This is r5's Theorem H3 in evil's algebra. The datum — an observed fraction `f̂` of worst-case instances with no
discerned justification — is common information about the world; under `¬H` it calibrates `ν ≈ f̂`, and under `H` the
*same* `f̂` must be explained by some `(ε, d)`. Three pairs realize three radically different arguments from one datum:

| `ν = 0.9` | `(ε, d)` | `κ` | `BF(H:D)` | posterior at even prior | reading |
|---|---|---|---|---|---|
| same datum | `(0.01, 1.00)` | 0.010 | **0.011** | 0.011 | ≈ 90:1 against `H` |
| same datum | `(0.10, 0.50)` | 0.550 | **0.611** | 0.379 | ≈ 1.6:1 against `H` |
| same datum | `(0.50, 0.00)` | 1.000 | **1.111** | 0.526 | datum mildly *favors* `H` |

All three are internally consistent with every survey anyone can run. The theorem does not say the first row is wrong;
it says nothing in the [T] layer selects among the rows. Identical structure, different direction, from r3's
non-identifiability theorem `λ_req = (N−1)p/(1−p)` and r5's H3a: the load-bearing quantities live on the [NT] side.

The witness `(ν·BF*, 1)` shows something sharper than underdetermination-in-principle: the *entire* disagreement
between theodicies and Rowe's argument can be carried on two credences that no experiment in this domain can price.
`ε` is the weight of the greater-good bridge; `d` is the weight of inscrutability. The literature is a debate about
where to set them.

---

## 6. Theorem E5 — the neutrality price, in closed form

> **Theorem E5.** `BF(H:D) ≥ 1` (the datum does not favor `¬H`) iff `d ≤ d* := (1−ν)/(1−ε)`, when `ε ≤ ν`; and
> holds for **all** `d ∈ [0,1]` when `ε > ν`.
>
> **Proof.** `BF ≥ 1 ⟺ κ ≥ ν ⟺ (1−ε)(1−d) ≥ ν − ε`. If `ε ≤ ν`, divide by `1−ε > 0`:
> `d ≤ 1 − (ν−ε)/(1−ε) = (1−ν)/(1−ε) = d*`. Since `ν − ε ≤ 1 − ε`, `d* ≤ 1` always. If `ε > ν` the RHS
> `ν − ε < 0 ≤ (1−ε)(1−d)`, so the inequality holds for every `d`. ∎

Prices, computed from the closed form (verifier recomputes each entry):

| `ν` | max discernibility `d*` compatible with neutrality | | | | | |
|---|---|---|---|---|---|---|
| | `ε = 0.01` | `ε = 0.05` | `ε = 0.10` | `ε = 0.30` | `ε = 0.50` | `ε = 0.90` |
| `0.90` | 0.101 | 0.105 | 0.111 | 0.143 | 0.200 | 1.000 |
| `0.99` | 0.0101 | 0.0105 | 0.0111 | 0.0143 | 0.0202 | 0.100 |
| `1.00` | 0 | 0 | 0 | 0 | 0 | 0 |

Read the middle row: if naturalistic inquiry would have discerned justifications for 1 % of worst-case suffering, the
theist neutralizes the datum by placing at most **1.01 %** credence in divine-reason transparency — i.e. by being ~99 %
inscrutable. Read the bottom row: if `ν = 1` (naturalism also predicts no discernible justification for the worst
cases), neutrality demands `d = 0` exactly — total inscrutability — and any `d > 0` makes the datum evidence against
`H`. The inscrutability defense is not a rhetorical flourish; it is the only thing standing between the datum and
`BF = (1−d)`.

Two remarks the verifier pins as literal checks, because both are traps:

- **`d*` is non-monotone in `ε`** (increasing on `[0, ν)`: `∂d*/∂ε = (1−ν)/(1−ε)² > 0`). A *higher* credence that
  perfect goodness might permit uncompensated suffering makes the datum *more* expected under `H` and therefore
  *raises* the tolerable transparency. The reader who assumes the theistic price falls with theistic confidence reads
  the table backwards.
- **Symmetric anti-theistic price.** `BF ≤ 0.1` (a 10:1 lean against `H` from an even start, posterior 0.091)
  requires `κ ≤ 0.1ν`: at `ν = 0.9`, `ε = 0.01` it needs `d ≥ 0.919` — the atheist must be ≥ 92 % certain of
  divine-reason transparency *and* ≥ 99 % certain of the greater-good bridge. Infeasible for any `ε > 0.1ν`. The whole
  dispute is a bet on one number, `d`, and `d` is [NT].

---

## 7. Theorem E6 — the posterior lift: what the datum does to "this instance is pointless"

The datum's global Bayes factor is not the only thing it moves. Within `H`, observing `¬V` for a particular instance
raises the credence that *that instance* is uncompensated:

> **Theorem E6.** `P(¬G | ¬V, H) = ε/κ`, so the lift factor is exactly `1/κ ≥ 1`: `L := P(¬G|¬V,H)/P(¬G|H) = 1/κ`.

**Proof.** Bayes within `H`: `P(¬G|¬V,H) = P(¬V|¬G,H)·P(¬G|H) / P(¬V|H) = 1·ε/κ`. ∎ (Machine-checked by direct
numeration over a fine `(ε,d)` grid, complement identity `P(b_G | ¬V, H) = (1−ε)(1−d)/κ` included.)

The datum cannot raise the instance-level "pointlessness" credence beyond what inscrutability allows: at full
inscrutability (`d = 0`, `κ = 1`) the lift is **exactly 1** — the datum is inert on the per-instance question, which
is r4's Lemma G in per-instance form. Sample prices (verifier recomputes):

| `(ε, d)` | `κ` | `P(¬G \| ¬V, H)` | lift `1/κ` |
|---|---|---|---|
| `(0.01, 0)` | 1.000 | 0.0100 | 1.0000 |
| `(0.01, 0.5)` | 0.505 | 0.0198 | 1.9802 |
| `(0.01, 0.9)` | 0.109 | 0.0917 | 9.1743 |
| `(0.50, 0.5)` | 0.750 | 0.6667 | 1.3333 |

Note what this table *is*: the informal argument — "this child suffered and no reason is visible, so this suffering
serves no greater good" — is the claim that the lift is large. The lift is `1/κ`, and `κ` is the theist's price. The
sentence looks like an observation; arithmetically it is a credence.

---

## 8. Theorem E7 — the zero cell and the observable datum cannot be had together

Two readings of evil's data premise compete, and they trade a zero cell for observability:

**Reading A (unobservable, zero-celled):** the datum is `¬G` itself — an uncompensated instance *exists*. Then `P(¬G|H,b_G) = 0` (the bridge forbids exactly this), and by r4's Lemma G with one surviving cell,

```
BF(H : ¬G) = P(¬G|H)/P(¬G|¬H) = ε/ν★        (ν★ := P(¬G|¬H))
```

This is **r4's Theorem H1 under relabeling** (`E ↦ ¬G`, `b ↦ b_G`, `r ↦ 1`, `q ↦ ν★`) — the cleanest possible
anti-theistic structure. Its price: its datum is the argument's conclusion. Nobody observes `¬G`; the inscrutability
question *is* the question whether `¬V` ever warrants `¬G`. The verifier confirms the relabeling reproduces H1's form
and confirms the zero cell `P(¬G|H,b_G) = 0` by construction.

**Reading B (observable, no zero cell unless `d = 1`):** the datum is `D = S ∧ ¬V`, Theorem E1's object. Under
`b_G` the datum occurs at rate `1 − d`; no zero cell.

**Theorem E7 (the wedge).** The two readings are separated by exactly the inscrutability leakage:

```
BF(H : D) = BF(H : ¬G) + (1−ε)(1−d)/ν     [taking ν★ = ν for comparability]
```

**Proof.** Substitute `κ = ε + (1−ε)(1−d)` into `BF(H:D) = κ/ν` and split. The verifier checks the identity to
machine precision over random `(ε,d,ν)`, checks the leak term is non-negative (so Reading B is always at least as
favorable to `H` as Reading A), and checks monotonicity in `d`. ∎

Sample numbers (verifier pins these): at `ε = 0.01, d = 0.9, ν = 1`, Reading A gives `BF = 0.010` and Reading B gives
`BF = 0.109` — the observable datum is **10.9× weaker** evidence against `H` than the conclusion it stands in for.
The gap is the inscrutability premise, priced.

This is the structural reason the evidential problem of evil "cannot be repaired by making its cell zero" (r4 §7's
observation, now quantified): the zero cell attaches to Reading A, whose premise is [NT]; the observable Reading B
attaches to no zero cell. Hiddenness was the unusual case that had both an observable datum *and* a zero cell —
because its bridge (`love requires availability`) bore directly on the observed thing (nonbelief). Evil's bridge bears
on the thing itself (justification), one inferential step behind the observation.

---

## 9. Table 1 — premise-by-premise ledger for the evidential problem of evil

| # | premise / quantity | role in the argument | tag | what would count as evidence |
|---|---|---|---|---|
| 1 | `S`: worst-case intense suffering occurs | occurrence component of `D` | **[T]** | **[E+]** medical/historical records (established); **[E−]** none live. Cancels from `BF` (Cor. E1a) |
| 2 | `¬V`: no justification discerned | operative part of `D` | **[T]-soft** | **[E+]** a documented, scoured justificatory literature yielding nothing for the class; **[E−]** a candidate justification that survives scrutiny — but that is row 3's bridge, not a datum |
| 3 | `b_G`: perfect goodness ⇒ compensating good or no permission | the major premise | **[NT]** | **[E+]** a defended theory of goodness; **[E−]** the inscrutability tradition — neither is testable |
| 4 | `ε := P(¬b_G | H)` | bridge-complement credence | **[NT]** | no independent measurement; Theorem E4's witness family shows it is not identified |
| 5 | `d`: discernibility of justifying goods | inscrutability, quantified | **[NT]** | no independent measurement; the entire dispute lives here (Theorems E5–E7) |
| 6 | `ν := P(D \| ¬H)`: naturalistic benchmark | denominator of `BF` | **[T]-linked, [NT] in force** | proxy only (`f̂`, row 7); counterfactual in force; stipulated in the model |
| 7 | `f̂`: observed fraction without discerned justification | calibrates `ν` | **[T]** in principle | survey of the suffering/justification literature — externally blocked this session (§12); and by Theorem E4 it fixes `ν` at most, never `(ε,d)` |
| 8 | `H`: an omnipotent, omniscient, perfectly good being exists | the target conjunction | **[NT]** | — |

Two rows are testable — 1 and 7 — and **neither** contributes to the adjudication: row 1 cancels (Corollary E1a), and
row 7 only calibrates the stipulated benchmark (Theorem E4). The load-bearing quantities (rows 3–5) are credences. The
testable-CORE tally remains **0**, as for every family in the taxonomy.

---

## 10. Table 2 — the sensitivity lattice

`BF(H:D) = κ/ν` with `κ = (1−ε)(1−d) + ε`. Posteriors at an even prior (`P(H|D) = BF/(1+BF)`). **Every entry is
arithmetically derived from the formula; none is a measurement.** The `ε` column is a credence, not a frequency; the
`d` row is a credence, not a frequency. Cells read `BF → posterior`.

**At `ν = 0.9`** (naturalism would discern justifications for 10 % of worst-case instances):

| `ε` ↓ / `d` → | `0` | `0.1` | `0.5` | `0.9` | `0.99` | `1` |
|---|---|---|---|---|---|---|
| 0.001 | 1.111 → 0.526 | 1.000 → 0.500 | 0.556 → 0.357 | 0.112 → 0.101 | 0.012 → 0.012 | 0.001 → 0.001 |
| 0.01 | 1.111 → 0.526 | 1.001 → 0.500 | 0.561 → 0.359 | 0.121 → 0.108 | 0.022 → 0.022 | 0.011 → 0.011 |
| 0.05 | 1.111 → 0.526 | 1.006 → 0.501 | 0.583 → 0.368 | 0.161 → 0.139 | 0.066 → 0.062 | 0.056 → 0.053 |
| 0.10 | 1.111 → 0.526 | 1.011 → 0.503 | 0.611 → 0.379 | 0.211 → 0.174 | 0.121 → 0.108 | 0.111 → 0.100 |
| 0.25 | 1.111 → 0.526 | 1.028 → 0.507 | 0.694 → 0.410 | 0.361 → 0.265 | 0.286 → 0.222 | 0.278 → 0.217 |
| 0.50 | 1.111 → 0.526 | 1.056 → 0.514 | 0.833 → 0.455 | 0.611 → 0.379 | 0.561 → 0.359 | 0.556 → 0.357 |
| 1.00 | 1.111 → 0.526 | 1.111 → 0.526 | 1.111 → 0.526 | 1.111 → 0.526 | 1.111 → 0.526 | 1.111 → 0.526 |

**At `ν = 0.99`** (BF only — naturalism almost never discerns a justification):

| `ε` ↓ / `d` → | `0` | `0.1` | `0.5` | `0.9` | `0.99` | `1` |
|---|---|---|---|---|---|---|
| 0.001 | 1.010 | 0.909 | 0.506 | 0.102 | 0.011 | 0.001 |
| 0.01 | 1.010 | 0.910 | 0.510 | 0.110 | 0.020 | 0.010 |
| 0.05 | 1.010 | 0.914 | 0.530 | 0.146 | 0.060 | 0.051 |
| 0.10 | 1.010 | 0.919 | 0.556 | 0.192 | 0.110 | 0.101 |
| 0.25 | 1.010 | 0.934 | 0.631 | 0.328 | 0.260 | 0.253 |
| 0.50 | 1.010 | 0.960 | 0.758 | 0.556 | 0.510 | 0.505 |
| 1.00 | 1.010 | 1.010 | 1.010 | 1.010 | 1.010 | 1.010 |

Readings, against r4's hiddenness lattice (Table 2 there: a 9:1 posterior against needed `P(¬b|H) = 1/9`):

- The left column (`d = 0`, full inscrutability) never drops below `BF = 1.111 > 1` at `ν = 0.9`: under full
  inscrutability the datum mildly *favors* `H`, because a hidden-reasons theism predicts undiscerned justification
  slightly *better* than naturalism does. At `ν = 1` it is exactly 1.
- A 5:1 lean against `H` (`BF = 0.2`, posterior 0.167) sits at, e.g., `ε = 0.01`, `d ≈ 0.91` — the reader must place
  ~91 % on divine-reason transparency. A 10:1 lean needs `d ≥ 0.919` at the same `ε` (Theorem E5).
- The bottom row is the total-inscrutability-insensitive region: `ε = 1` collapses every column to `1.111` — if the
  reader is certain the bridge fails, the datum says nothing beyond naturalism's own benchmark.
- `d = 1` column: `BF = ε/ν` exactly — the column in which Reading A (§8) is observable, and it exists only for
  readers already at full transparency.

---

## 11. Where evil sits among the classic arguments

Updating r4's §7 table with this artifact's row:

| argument | structure | data premise | evidential factor (this corpus) |
|---|---|---|---|
| **divine hiddenness** | **zero cell** on the *observed* datum | **[T]** | `r·P(¬b|H)` — bridge complement; data **cancels** (r4 H1); confounded form `u/q` (r5 H3) |
| **evidential problem of evil** | **zero cell only on the *unobserved* datum** (`¬G`); observable datum `¬V` leaks through the inscrutability cell | **[T]-soft** (suffering exists; *undiscerned* justification is inquiry-relative) | `κ/ν = [ε + (1−ε)(1−d)]/ν` — this artifact, Thm E1; Reading A (`¬G`) is H1 relabeled |
| **Euthyphro dilemma** | **metaethical fork** — no datum at all | none | none (r6, D4) |
| **religious diversity** | **many-hypothesis posterior simplex** | **[T]** (affiliation tracks birth-culture) | `BF_ij = 1` under the measured transmission mechanism (r6, D1) |
| **religious experience** | **one-cell** | **[T]** (reports exist) | `P(c|H)·(1/q′ − 1)` (r4, H2) |
| **design / fine-tuning** | **one-cell + measure sensitivity** | **[T]** | `⟨ρ_b·τ_b⟩_w`, measure not fixed (r3, Thms 1–2; row A5) |

The table now shows the family resemblance that makes the corpus's single structural claim: in every row the
evidential factor is either a product of [NT] credences, a stipulated ratio, or exactly 1. Evil's row is the only one
whose zero cell attaches to an unobserved proposition, and Theorem E7 is the precise sense in which that is the price
of having anything observable at all.

---

## 12. What would count as evidence, and what the record shows where testable

**Testable claims in this cluster.**

1. *Worst-case intense suffering occurs.* Established at the existential level by ordinary medical and historical
   record. It cancels from `BF` (Corollary E1a), so no figure is needed and none is quoted — the same economy r4
   applied to `q`.
2. *The observed fraction `f̂` of worst-case instances without a discerned justification.* In principle measurable by a
   systematic review of the justificatory literature across the classes Rowe names. **Not quoted here**: external
   verification has been blocked by tooling failure for **ten consecutive sessions** (see §15), and — decisively — by
   Theorem E4 it calibrates `ν` at most and constrains `(ε, d)` not at all. A survey cannot decide `d`.
3. *Candidate justifications that survive scrutiny.* Genuinely testable per instance (is the compensating good real,
   and does it obtain?). Every candidate so far examined is [NT] at the point it matters — it converts the observation
   into a normative claim about what goodness permits — or peripheral (an eschatological claim is [NT] by
   construability; a datable providential claim would be a taxonomy [T]-ledger row, species "event/date", already
   carried there).

**Non-testable claims in this cluster.** `b_G`, `¬b_G`, `ε`, `d`, `ν` (in force), and `H` itself. For these, the demand
"what would count as evidence" has the honest answer *nothing that both sides would accept*, because the quantities
are non-identifiable from the data either side recognizes: Theorem E4 pins the algebraic form of that statement for
this argument, exactly as r5's H3 did for hiddenness and r3's Theorem 3 does for proof-premises generally.

---

## 13. Why "proof" is the wrong category — stated quantitatively

A proof, in this domain, would be a Bayes factor of exactly `0` or `∞`. The four prices:

- **Against `H` (evil):** `BF = 0` requires `ε = 0 ∧ d = 1` (Theorem E3) — joint certainty on the greater-good bridge
  and on divine-reason transparency, i.e. on the two premises the argument exists to establish.
- **Against `H` (hiddenness):** `BF = 0` requires `r·P(¬b|H) = 0` (r4, Theorem H1b).
- **For `H` (experience):** `BF⁺ = ∞` requires `q′ = 0` with `a·P(c|H) > 0` (r4, Theorem H2), and `q′ > 0` is
  established by the reports' existence.
- **Against `¬H` generally:** every candidate premise is analytic (true in all worlds, uninformative) or synthetic
  (contingent, defeasible) — r3's Theorems 3–4, with the conjunctive floor `w_min = p^(1/n)`.

Add Theorem E4's identification failure — for any datum and any target there is a consistent `(ε, d)` — and the
conclusion is that "proof" is not a demanding standard nobody has met. It is the **wrong category**: the arguments in
this domain are posterior-shifting devices whose magnitude is set by the reader's credence in a normative premise, and
no accumulation of data changes that, because the data terms either cancel (hiddenness), rate-set (experience), or
calibrate a stipulated benchmark (evil).

---

## 14. Limitations, and what would change my mind

1. **Occurrence cancels — the artifact prices the *existential* datum.** The quantitative variant (Draper's: the
   *volume, kinds, and distribution* of suffering exceed what a perfect being would permit) needs a measure over
   "permitted density of worst cases" — an [NT] quantity, out of the model. Rowe's existential form is the tractable
   one; the density variant inherits the same seam but is not priced here.
2. **`ν` is stipulated, not measured.** Its only observable proxy is the datum itself (circularity acknowledged);
   §12.2 says why an external fix would still not adjudicate.
3. **`ε` and `d` are not measured and not measurable here.** The theorem states what the force *equals*; it does not
   evaluate it. Any actual credence is a theological and normative matter, outside this document's scope by protocol.
4. **The model's range is asymmetric.** `BF(H:D) ∈ [0, 1/ν]`: the anti-theistic direction gets the full range and the
   pro-theistic direction is capped at `1/ν`, because the `¬b_G` cell has `P(D|H,¬b_G) = 1`. This is the same
   favorable-direction assumption the r4 §4.1 and r5 Corollary H2 reviews corrected in their own directions; it is
   stated here, pinned by the verifier, rather than discovered by a reviewer.
5. **Single discernibility rate.** One `d` for the whole worst-case class; a non-uniform, instance-correlated `d`
   would change the lattice's shape but not its identification failure (the witness `(ν·BF*, 1)` is rate-agnostic).
6. **`d = 0` and `d = 1` are idealizations.** They are the clean boundary cases; the closed forms hold on the closed
   interval and the verifier checks the interior grid separately.
7. **No external source is verified this session.** Web search has failed with `MCP tool stepsearch.web_search failed:
   Streamable HTTP error: Error POSTing to endpoint:` for **ten consecutive sessions** (probed again this turn). The
   philosophical citations are given from standing knowledge. **No number in this artifact depends on an external
   source** — every entry is computed from the stated formulas. Do not burn further turns retrying that tool.

**What would change my mind** (pre-stated, in the corpus's style):

1. A principled, *measured* route to `d` — an observable consequence of a disclosing being's epistemic policy that
   does not presuppose which family is true. (r6's Theorem D3b prices the same species of quantity for the diversity
   argument — the discernibility of reasons, there across traditions rather than for theodicies; the two prices are
   structurally parallel but not formally identified, and I do not claim they are the same parameter.)
2. A model in which `P(D | H, b_G)` is not `1 − d` — i.e. a derivation of the observable cell that breaks the
   single-rate simplification in a way that *creates* empirical content (a correlation between `d` and an observable
   would do it).
3. A benchmark `ν` fixed independently of `f̂` by something other than stipulation. This would not restore
   identification (Theorem E4's witness survives any `ν`), but it would move the argument from stipulated to measured
   and is worth having on the record.
4. A characterization of "pointless" that is both independent of greater-good reasoning *and* observable — this would
   attach the zero cell to the datum and would genuinely strengthen Reading A into a decidable claim (r4's §7 names
   the same requirement; it remains unmet).
5. A demonstrated per-instance route to `¬G` — establishing, for a specific case, that *no* compensating good obtains,
   by something other than the failure to discern one. Unmet.

---

## 15. Sources

- J. L. Mackie, "Evil and Omnipotence," *Mind* 64 (1955) — the logical problem of evil.
- Alvin Plantinga, *God, Freedom, and Evil* (1974) — the free-will defense.
- William L. Rowe, "The Problem of Evil and Some Varieties of Atheism," *American Philosophical Quarterly* 16 (1979) —
  the evidential (existential) form, reconstructed at §1.1. The bracketed conclusion is reported, not endorsed.
- Paul Draper, "Pain and Pleasure: An Evidential Problem for Theists," *Noûs* 23 (1989) — the evidential (density)
  form; scoped in Limitation 1.
- Stephen J. Wykstra, "The Humean Obstacle to Evidential Arguments from Suffering: On Avoiding the Evils of
  'Appearance'," *International Journal for Philosophy of Religion* 15 (1984) — the inscrutability premise; `d` in
  this artifact is that premise, quantified.
- J. L. Schellenberg, *Divine Hiddenness and Human Reason* (Cornell Univ. Press, 1993) — the companion argument
  (r4/r5).
- All citations above are **not re-verified this session** (§14.7: tooling blocked for ten consecutive sessions). No
  number in this artifact depends on them.

---

## 16. Verification

`verify_v17.cjs` — 43 800 checks (third run: 0 failures), shares no code with `verify_v9.cjs` … `verify_v16.cjs`.
Every theorem is checked by brute force over random models and by Monte-Carlo
enumeration of the cell structure — **never** by re-asserting the closed form the artifact derives. Specifically:

- Theorem E1's identity `BF = κ/ν` over random `(ε, d, ν)`, by explicit summation over the two bridge cells (not by
  the closed form);
- Monte-Carlo: `P(D|H)` estimated by sampling cells at rates `(1−ε, ε)` and outcomes at rate `d`, matched against `κ`
  to within sampling tolerance;
- Corollary E1a's cancellation: rebuilding `BF` with occurrence rates `ω_H ≠ ω_N` leaves `BF` unchanged;
- Corollary E1b's range `BF ∈ [0, 1/ν]` over random models;
- Theorem E2's cell LRs `{(1−d)/ν, 1/ν}` and the neutrality recovery `LR = 1` at `ν = 1, d = 0`;
- Theorem E3: exact zero of `BF` **only** at `(ε,d) = (0,1)`; interior-grid minimum strictly positive;
- Theorem E4: witness `(ν·BF*, 1)` hits every target in a grid to `1e-12`; three explicit consistent
  parameterizations of one datum tabulated against the artifact's §5;
- Theorem E5: `BF(ε, d*) = 1` over grids; auto-neutrality for `ε > ν`; strict monotonicity of `BF` in `d`; **the
  non-monotonicity of `d*` in `ε` pinned as a literal check**; the `BF ≤ 0.1` price table recomputed;
- Theorem E6: `P(¬G|¬V,H) = ε/κ` and `L = 1/κ` by direct grid enumeration; `L = 1` exactly at `d = 0`; the §7 sample
  table recomputed;
- Theorem E7: the leakage identity `BF(H:D) = ε/ν + (1−ε)(1−d)/ν` to machine precision; non-negativity of the leak;
  monotonicity in `d`; r4's H1 form recovered under the Reading-A relabeling;
- Table 2's lattice entries **parsed back out of this artifact's own markdown** and recomputed from the formula;
- the [T]/[NT]/[E+]/[E−] tag counts read from the artifact's own markdown against the ledger's stated tally;
- the forbidden-phrase and no-verdict protocol checks. Run `node verify_v17.cjs` from this directory.

### 16.1 The audit trail (recorded per corpus convention)

`verify_v17.cjs` **failed on first run (1506 failures), then twice more**, and the failures were informative in the
usual asymmetric way — the checker's own errors outnumbered the artifact's, but the artifact did contain a real one:

1. **Verifier error (real, caught in-house):** the first script asserted `BF = κ/ν` is *increasing* in `ν`. It is
   *decreasing* — a larger naturalistic benchmark weakens the evidence against `H`. The artifact states the direction
   correctly in §1–§3 and Table 2 shows it (0.561 at `ν = 0.9` vs 0.510 at `ν = 0.99`); the check was written
   backwards. Had the artifact made the same slip, this is the channel that would have caught it.
2. **Verifier defect:** the protocol regex flagged ordinary subordinate-clause "therefore" (three prose lines).
   Narrowed to sentence-initial "Therefore" outside the §1.1 argument quote.
3. **Verifier defects:** four markdown-parser failures (bold markers in the §5 identification table, backticks in
   the §7 sample table, header rows counted as data rows in Table 2).
4. **Artifact error (real, caught by the table reparse):** the `d*` table cell at (ν = 0.99, ε = 0.90) was
   transcribed **0.101** against the exact value **0.100** — `(1−ν)/(1−ε) = 0.01/0.1`. Corrected in place. The prose
   quotes of `d*` (0.101 at ν = 0.9, ε = 0.01; 0.0101 at ν = 0.99, ε = 0.01) were and remain correct.
5. **Artifact precision defect (real, minor):** the §7 lift column was printed at 2 decimals against a 5 × 10⁻⁴
   tolerance. Tightened to 4 decimals.

Fifth consecutive round in which the adversarial verifier caught something real, and again the headline — Theorem E1's
identity, now checked by Monte-Carlo sampling of the cell structure *and* by explicit cell summation — survived
untouched; every correction was in a peripheral table or in the checker's own stated claim. The lesson recorded in the
r3–r6 audit trails repeats: **the verifier that does not share the artifact's assumptions is what produces the result
worth keeping.**

---

*End of artifact. No verdict is asserted herein on the existence of any god or the truth of any religion. The
deliverable of this domain is the taxonomy plus the analysis of testability; this artifact is the last unfilled cell
of that taxonomy's "deliberately not assigned" row, and it finds the same structure the rest of the corpus found: a
number that exists, a number that contains no measurement, and a "proof" reading that requires believing, with
certainty, the very premises the argument was supposed to establish.*
