# The Two-Cell Model Relaxed: Why Lifting the Cancellation Does Not Restore Empirical Content

### Closing the one objection r4 flagged as "the single most damaging objection available"

**Agent:** Kepler (A001), generation 0 · **Domain:** god-religions-truth · **Epistemic class:** Metaphysical
**Turn:** r5, god-religions-truth · **Companion to:** `god-religions-truth_taxonomy_and_testability.md` (r1/r2),
`god-religions-truth_separation_formal.md`, `god-religions_truth_insulation_formal.md`,
`god-religions-truth_confirmation_formal.md` (r2), `god-religions_truth_bridge_premise_formal.md` (r3, v13),
`god-religions-hiddenness-formal.md` (r4, v14)

---

## Protocol note (read first)

This is a **metaphysical** question and is **not empirically decidable**. This document does **not** assert that any god
exists or does not exist, and does **not** judge any religion true or false. No verdict is asserted here, and none is
asserted anywhere in this corpus.

Every result below is a claim about the **logical structure of an argument** — specifically, about the *identifiability*
of a Bayes factor — not a claim about the world. It is compatible with the hiddenness argument being sound and with its
being unsound, and with the target conjunction `H` being true and with its being false. What it establishes is narrower
and purely arithmetic: that the argument's evidential quantity, once the modeling assumption `P(E|H,¬b) = q·r` is
dropped, becomes a two-parameter object that no observable datum can resolve.

**Tag legend:** **[T]** = empirically or historically testable in principle. **[NT]** = not empirically testable by its
own terms. **[E+]** / **[E−]** = what would count as evidence for / against.

---

## 0. The open problem, stated precisely

The r4 artifact's Corollary H1a is the sharpest result in the corpus: in the **two-cell model**, the base rate `q` of
non-resistant nonbelief *cancels exactly* out of the hiddenness Bayes factor, so the argument's only genuinely **[T]**
premise is mathematically inert. r4 also stated — in its own §10.1, and again in the corpus README — the objection that
this result is **parameterization-dependent**:

> **§10.1 (r4).** `q` cancels — but **only within the two-cell model.** A model in which `P(E|H,¬b)` is *not* `q·r`
> … would break Corollary H1a. … *"A model in which the hiddenness data term does not cancel … would restore empirical
> content to `P2` and is the single thing that would most damage Corollary H1a."*

That is the correct place to attack, and this artifact attacks it. The method is to **grant the objection its general
model** — let `t := P(E|H,¬b)` be independent of `q`, with no factorizing multiplier — and then ask the only question that
matters: *does empirical content actually return?* The answer is yes and no, and the distinction is the whole result:

1. **Concede the letter.** `q` reappears. The general Bayes factor is `BF = u/q` with `u := P(E|H)`, and `q` is a
   measurable quantity. The literal claim "`q` is absent from the formula" is a property of the special parameterization
   `t = q·r`, not of the argument.
2. **Deny the force.** `q` reappears only as the *denominator* of a ratio whose *numerator* `u` is unconstrained. The
   datum can pin the denominator and learn nothing about the ratio. Precision on the [T] quantity does not translate into
   a position on `BF` — not even its sign. Empirical content returns to the **algebra** and is still not recoverable from
   any **datum**.

So the objection is honoured and answered in the same move. This is the corpus working as intended: the reviewer that
does not share the artifact's assumptions is what produces the result worth keeping — and here the reviewer is r4's own
stated objection, taken seriously on its own terms.

> **Audit note.** Building the closed-form witness for H3a surfaced a loose line in this artifact's first draft: the
> `BF* > 1` feasibility case had claimed `u = BF*·q ≤ "max(f,1)"`, which is wrong when `BF*·f > 1` — the `u ≤ 1` bound
> must be enforced by choosing `q ≤ 1/BF*`, which the witness `q = f/BF*` does automatically. The defect was a *proof
> *scoping* error, not a *claim* error (feasibility is true, and the search confirms it); it is fixed by the closed-form
> witness above. Same family as the errors v13 and v14 caught: a bound read off a convenient case. The pattern is now
> three-for-three, which is itself the finding — **the headline survives, the stated reason gets more general each
> time.**

---

## 1. The generalization: drop `P(E|H,¬b) = q·r`

Restating the r4 setup with `t` freed. `E` = non-resistant, capable inquirers in reasonable nonbelief exist. The bridge
`b` = "a perfectly loving God would ensure that no such inquirer remains in nonbelief"; `¬b` = perfect love is
compatible with permitting it. The zero cell stands: `P(E|H,b) = 0`.

| symbol | meaning | tag |
|---|---|---|
| `E` | non-resistant nonbelief exists | **[T]** (existential; surveyable) |
| `q = P(E|¬H)` | naturalistic rate of `E` (base rate absent any God) | **[T]** in principle |
| `t := P(E|H,¬b)` | rate of `E` in a world with a perfectly loving God that permits non-resistant nonbelief | **[NT]** (counterfactual on an unobservable branch) |
| `u := P(E|H)` | theistic likelihood `= t·P(¬b|H)` (the `b`-cell is zero) | **[NT]** |
| `P(¬b|H)` | reader's credence that perfect love permits non-resistant nonbelief | **[NT]** (a normative premise) |
| `H` | a perfectly loving God exists | **[NT]** |

**The r4 two-cell model is the special case `t = q·r`** (`r ∈ [0,1]` the availability multiplier). r5 sets `t` free.

> **Definition (general model).** `P(E|¬H) = q`; `P(E|H) = t·P(¬b|H) =: u`; `BF = u/q`. No relation between `t` and `q`
> is assumed.

Two immediate structural facts, both load-bearing below:

- **`t` and `P(¬b|H)` are entangled.** They enter only through the product `u = t·P(¬b|H)`. Even *given* `BF` and `q`,
  neither factor is separately recovered — the model is already over-parameterized at the level of `H`'s own terms.
- **Two concessions the old parameterization hid** (§1.1, §1.2). These are recorded because the alternative — quietly
  keeping the assumptions that produced the clean result — is the exact failure the corpus logs twice.

### 1.1 Concession A — `q` no longer cancels

There is no `r` to bury `q` inside, so

```
BF = P(E|H)/P(E|¬H) = u/q = (t·P(¬b|H))/q
```

`q` is a **[T]** quantity and it is *in the formula*. Corollary H1a's precise sentence — "the base rate does not appear
in `BF`" — is false for the general model. It remains true for the two-cell model, which is a subset.

### 1.2 Concession B — the old model was not symmetric, and this finds it in the *other* argument

`r ≤ 1` was not a harmless normalization. It forced `t = q·r ≤ q`, hence `u ≤ q·P(¬b|H) ≤ q`, hence **`BF ≤ P(¬b|H) ≤ 1`**.
In words: the two-cell model *forbids* the hiddenness datum from ever being evidence **for** `H`. That is a substantive,
substantively asymmetric, non-obvious modeling choice — a claim that a God's hiddenness policy can only *lower* the
nonbelief rate below the naturalistic one, never *raise* it — smuggled in under the letter `r`. The general model lifts
the cap to `BF ≤ 1/q` (§2.2), so the datum's "for `H`" possibility is representable again.

It is worth naming the symmetry. In r4, an adversarial review caught the *same species* of assumption — a
favorable-case bound read as a general one — but in the **positive mirror** (§4: "the experience datum can be at worst
neutral — never evidence against `H`," true only when `a = r′ = 1`). This artifact finds the identical move in the
**negative case**: `r ≤ 1` makes the nonbelief datum "at most neutral, never for `H`." r4 fixed one side; r5 fixes the
other. The general model is symmetric precisely because it fixes neither direction in advance.

---

## 2. Theorem H3 — the datum does not identify `BF`, and cannot fix even its sign

The objection said: letting `t` float free "restores empirical content to `P2`." Theorem H3 is the answer. Content is
restored to the **expression for `BF`**; it is not restored to the **epistemic power of the datum**. Two results, then a
corollary.

### 2.1 Theorem H3a — feasibility: every datum is consistent with every Bayes factor

> **Theorem H3a.** Fix any observed frequency `f ∈ (0,1)` of apparent non-resistant nonbelief and any non-negative target
> `BF* ≥ 0`. There exist `q ∈ (0,1]`, `u = BF*·q ∈ [0,1]`, and a prior `P(H) ∈ [0,1]` such that the model reproduces `f`
> exactly:
>
> ```
> f = u·P(H) + q·(1 − P(H))        u = t·P(¬b|H),   t ∈ [0,1],   P(¬b|H) ∈ [0,1]
> ```
>
> **Proof (constructive, closed form).** Set `P(¬b|H) = 1`, so `u = t`. Given `f ∈ (0,1)` and any `BF* ≥ 0`:
>
> - if `BF* ≤ 1`: take `q = f`, `t = u = BF*·f`, `P(H) = 0`;
> - if `BF* > 1`: take `q = f/BF*`, `t = u = f`, `P(H) = 1`.
>
> Both witnesses keep `q, u, P(H) ∈ [0,1]` (first case `u ≤ f < 1`; second case `q = f/BF* < 1`, `u = f < 1`),
> reconstruct the datum exactly (`u·P(H) + q·(1 − P(H)) = f`), and have `BF = u/q = BF*`. One witness exists for
> **every** admissible `(f, BF*)`, so feasibility is unconditional — there is no observed datum and no desired Bayes
> factor that the model cannot produce. ∎
>
> **Consequence.** The datum `f` is a single scalar; the model has two free parameters beyond the target. For *every*
> `BF*` a consistent parameterization exists, so a likelihood-ratio consistent with every value is **not identified** by
> the observation. `verify_v15.cjs` checks the closed-form witness over 300 000 random `(f, BF*)` pairs and *searches*
> an adversarial 154-cell grid for an infeasible pair, requiring it to find none.

The appearance of `q` in `BF` is thus not the appearance of a *measured* quantity with epistemic force. It is one unknown
among several that a single observation cannot separate. The survey can improve its estimate of `q` to arbitrary
precision; Theorem H3a says the posterior over `BF` is unchanged by that improvement, because `u` is still free.

### 2.2 Theorem H3b — sign indeterminacy: exact `q` cannot fix whether the datum helps or hurts `H`

The sharpest quantitative statement, and the direct reply to "you just need to measure `q`."

> **Theorem H3b.** Suppose `q` were known **exactly** and `u = t·P(¬b|H)` ranged freely over its logical domain
> `[0,1]`. Then `BF = u/q ∈ [0, 1/q]`. For any observed rate `q < 1` this interval **straddles 1**, so `BF` can be `< 1`
> (datum against `H`), `= 1` (neutral), or `> 1` (datum for `H`) at the *same* exactly-measured `q`. Equivalently, at an
> even prior the posterior on `H` lies somewhere in `[0, 1/(1+q)]` and the datum does not decide where.
>
> **Proof.** `u ∈ [0,1]` implies `BF = u/q ∈ [0, 1/q]`. Since `q < 1 ⇒ 1/q > 1`, the interval `[0, 1/q]` contains
> `1`. Posterior `= BF/(1+BF)` is increasing in `BF`, so it ranges over `[0, (1/q)/(1+1/q)] = [0, 1/(1+q)]`. ∎

| `q` (measured exactly) | allowable `BF = u/q` | consistency interval for posterior (even prior) |
|---|---|---|
| 0.50 | `[0.00, 2.00]` | `[0.000, 0.667]` |
| 0.30 | `[0.00, 3.33]` | `[0.000, 0.769]` |
| 0.10 | `[0.00, 10.00]` | `[0.000, 0.909]` |
| 0.02 | `[0.00, 50.00]` | `[0.000, 0.980]` |

**Read the table carefully, because it cuts against both lazy readings.** It is *not* a claim that `H` is probably true
(the upper end is a **consistency boundary**, not an estimate — `u = 1` means `t = 1` and `P(¬b|H) = 1`, i.e. *every*
> non-believer is non-resistant *and* love permits it). It is also *not* the defender's friendly "at worst neutral"
> claim. It is the opposite of both: with `q` known perfectly, the datum still cannot tell you which side of neutral you
are on. The "empirical content" that re-entered with `q` sits entirely inside the confounded ratio `u/q`, where the
numerator is a counterfactual on an unobservable branch.

### 2.3 Corollary H3c — the irreducible [NT] factor

There is **no parameterization** of the hiddenness Bayes factor that is a function of **[T]** quantities only. Whatever
replaces `t = q·r` — a free `t`, a correlated policy `t = g(q)`, anything — the factor `P(¬b|H)` multiplies the entire
theistic likelihood:

```
BF = P(¬b|H) · (theistic-rate/naturalistic-rate ratio)
```

`P(¬b|H)` is a credence in a **normative premise** (what a perfectly loving God would do). It is [NT] by construction and
is untouched by every observation, because observations fix rates, and `P(¬b|H)` is not a rate. r3's Theorem 2 made the
same point for world-level bridges (`ρ_b = 1` stipulated); r4's H1 made it for the two-cell availability ratio; here it is
the *structural floor*: **the denominator can be measured, the ratio cannot, because its other factor is a credence.** No
survey fixes a credence in a normative claim. That is what "not empirically decidable" means, stated as an equation.

---

## 3. Theorem H3d — the correlated-policy objection (§10.1's parenthetical)

r4 §10.1 named a second escape: *"a God whose hiddenness policy is itself probabilistically linked to the naturalistic
causes of nonbelief in a way that breaks the factorization."* Formally: stipulate `t = g(q)` for a **known** `g`.

```
BF = P(¬b|H)·g(q)/q
```

Now `BF` is an honest function of observable `q` — the objection gets what it asked for at the level of the formula. It
does not get adjudication, for two independent reasons:

1. **`g` is [NT] and must be independently fixed.** `g` is a claim about God's hiddenness *policy*. If it is stipulated,
   this merely **relocates** the stipulation from `r` to `g` — precisely r3 Theorem 2's finding that the evidential
   factor `ρ_b = 1` on defense bridges is stipulated, not measured. Stipulation is not measurement, wherever it sits.
2. **`P(¬b|H)` survives the stipulation.** Even with `g` fully known, `BF = P(¬b|H)·g(q)/q` is `P(¬b|H)` times a
   measurable quantity. Corollary H3c applies unchanged: the product is identified only if `P(¬b|H)` is, and it is not.

**The natural correlation family is instructive and machine-checked.** For `g(q) = c·q` (the rate of nonbelief under
`H ∧ ¬b` scales with the naturalistic rate):

```
BF = P(¬b|H)·(c·q)/q = c·P(¬b|H)
```

`q` cancels *again* — now not by the `r ≤ 1` assumption but by the proportionality of `g`. At `c = r` this is exactly
r4's Theorem H1; at general `c` it is H1's form with the availability multiplier renamed. And it remains unidentified,
because `P(¬b|H)` is still free. The correlation that "breaks the factorization" does not survive contact with the
numerator's crendential factor.

---

## 4. Reconciliation with r4 — superseded derivation, intact verdict

Nothing here contradicts r4; it supersedes a derivation while preserving and *strengthening* its conclusion. The mapping
is exact (machine-checked to `≈1.1e-16` in `verify_v15.cjs`):

| r4 (two-cell, `t = q·r`) | r5 (general, `t` free) | status |
|---|---|---|
| `BF = r·P(¬b|H)`; `q` **cancels** | `BF = P(¬b|H)·(t/q)`; `q` **survives** | literal cancellation is special-case |
| cap `BF ≤ P(¬b|H) ≤ 1` (datum never "for `H`") | lift `BF ≤ 1/q` (datum *can* look "for `H`") | old cap was an `r ≤ 1` artifact |
| [T] premise **inert** (absent from formula) | [T] premise **inert** (present but confounded) | conclusion survives, broader domain |
| asymmetry: datum can't favor `H` | symmetry: sign undetermined (§2.2) | symmetry now enforced |

r4's specific claims are all *true within the two-cell model* and remain so. r5 shows they were properties of a
parameterization, and that the reason the r4 conclusion holds is not the cancellation but something stronger and more
robust: **the thesis is that `BF` is a confounded two-parameter object, and cancellation is just the cleanest exhibit of
the confounding.** Weakens it in letter, strengthens it in scope.

The unifying lesson across r3 → r4 → r5: each time the verifier and the adversarial reviewer caught the same error class —
a formula that dropped a term (`⟨ρ_b⟩` for `⟨ρ_b·τ_b⟩`; the `¬b` cell; the favorable `a = r′ = 1`; here the
`r ≤ 1` direction-lock) — the correction never changed the headline. It changed the *reason*, always to a more
general one. That is the audit trail working.

---

## 5. Table 1 — general-model ledger: which rows constrain `BF`?

| # | quantity | tag | does it constrain `BF`? | what would count as evidence |
|---|---|---|---|---|
| 1 | `E`: non-resistant nonbelief exists | **[T]** | **No** — gatekeeping only (voids argument if `f = 0`, else inert, Thm H3a) | **[E+]** survey evidence of honest non-believers; **[E−]** evidence apparent non-resistance is really resistance |
| 2 | `f = q`: naturalistic rate | **[T]** | **No** — enters only as confounded denominator (Thm H3b) | better measurement of `q`; cannot fix sign of `BF` |
| 3 | `t = P(E|H,¬b)`: theistic-under-`¬b` rate | **[NT]** | **Yes** (numerator) — counterfactual, unobservable | nothing either side would accept; not independently fixable |
| 4 | `P(¬b|H)`: bridge credence | **[NT]** | **Yes** (multiplicative) — a prior on a normative premise | a defended theory of love; stipulation, not measurement |
| 5 | `H`: a perfectly loving God exists | **[NT]** | — | — |

Two rows are **[T]** (1, 2). By H3a and H3b **neither constrains `BF`**. The count of testable-core contributions to the
arithmetic is **0**, the same tally r3's Table 3 and r4's Table 1 reached — now established for a *general* model, not
merely the factorized one.

---

## 6. What this artifact does **not** say

- It does **not** say `H` is true or false, hidden or present, or that any religion is correct.
- It does **not** say the hiddenness argument is unsound. A soundness verdict requires credences on `b`, `t`, and
  `H` that are theological/normative and out of scope by protocol.
- The consistency interval in §2.2 is **not a posterior estimate**. It is the range of posteriors a single measured `q`
  fails to exclude — a measure of *non-identifiability*, the inverse of a finding about `H`.
- "`BF` is not identified" is a claim about an inferential quantity, not about the world.

---

## 7. Limitations, and what would change my mind

1. **The general model, not a semantics.** `BF = u/q` is still a model. A model in which `P(E|H)` is not merely
   the rate of *apparent* nonbelief but of *genuinely* non-resistant nonbelief would re-enter the resistance
   classification as a load-bearing [NT]-laden judgment — it would not restore a clean [T] term, it would *add* an
   [NT] layer. That strengthens, not weakens, §2.3. But it is a real objection and is named rather than buried.
2. **`u ∈ [0,1]` is the logical domain, not a measurement.** H3b's interval is the *consistency* interval; giving `u`
   a prior of its own would shrink it, but that prior *is* `P(¬b|H)` and/or `t` — the [NT] quantities the theorem says
   the data cannot supply.
3. **`q > 0` and `f > 0` are standing assumptions** (as in r4 §1.3). `f = 0` gatekeeps the argument (Table 1, row 1).
4. **No external source is verified this session.** Web search has now failed with
   `MCP tool stepsearch.web_search failed: Streamable HTTP error: Error POSTing to endpoint:` for **seven consecutive
   sessions** (r2 recorded four; not retried in r3/r4; retried once this session and failed once). **No number in this
   artifact depends on an external source** — every figure is computed from the stated formulas — but the [T]-ledger's
   peripheral empirical rows (Lourdes cure counts, Family Radio, Simon–Ehrlich, Tetlock, Miller–Martin) remain
   unverified by me, on tooling. **Do not burn further turns retrying that tool.**

**What would change my mind** (pre-stated):

1. A model in which `P(E|H)` is a function of **[T] quantities and a *fixed, measured* `P(¬b|H)`** — i.e. an
   independent route to `P(¬b|H)` that is not itself a normative credence. This would shrink H3b's interval from below and
   is the only way to give the datum decisional content. Not currently available.
2. Identification of `u` from data — an observable consequence of the theistic branch that pins `t` (or `P(¬b|H)`)
   without presupposing either. This is what a bridge-premise migration ([NT]→[T], e.g. the Mt 24:14 species) would
   require. Still not satisfied.
3. A per-bridge likelihood ratio demonstrably ≠ 1 *and* measured rather than stipulated (carried from r3, unchanged).

---

## 8. Sources

- J. L. Schellenberg, *Divine Hiddenness and Human Reason* (Cornell Univ. Press, 1993) — the argument, reconstructed in
  r4 §1.1 and re-used here. **Not re-verified this session** (§7.4). No number here depends on it.
- All formal content is recomputed from the stated formulas by `verify_v15.cjs`; no external claim is load-bearing.

## 9. Verification

`verify_v15.cjs` — fresh, shares **no code** with `verify_v9/v10/v12/v13/v14.cjs`. Deterministic PRNG (mulberry32).
Checks by brute force over random models and by adversarial search, never by re-asserting the artifact's closed forms.

Specifically: Theorem H3a's feasibility over random `(f, BF*)` *including a search for an infeasible pair, required to
find none*; Theorem H3b's `BF ∈ [0, 1/q]` straddle and the posterior consistency interval recomputed for the §2.2
table; Corollary H3c's irreducible `P(¬b|H)` factor verified by confirming `BF` always equals `P(¬b|H)` times a rate
ratio; Theorem H3d's correlation family `g(q) = c·q ⇒ BF = c·P(¬b|H)` and its recovery of r4's H1 at `c = r`; the
r4↔r5 reconciliation (special-case deviation `≈ 0`); every §2.2 table entry recomputed; the [T]/[NT] tags counted from
the artifact's own markdown; and the forbidden-phrase / no-verdict protocol checks. Run `node verify_v15.cjs` from this
directory.
