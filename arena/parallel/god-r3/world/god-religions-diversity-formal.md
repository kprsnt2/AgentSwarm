# The Argument from Religious Diversity, Formalized

### Why the best-attested datum in this domain is symmetrically inert — and what the identification problem actually costs

**Status:** new (r6). **Domain:** god-religions-truth. **Epistemic class:** metaphysical; not empirically decidable.

---

## Protocol note (read first)

**This artifact asserts no verdict on whether any God exists, on which tradition is true, or on whether any religion is
false.** It analyses the *logical structure of one argument* — the argument from religious diversity — and asks what
that argument's premises can and cannot do. Every result below is a claim about an **argument**, conditional on stated
models, and is compatible with the exclusivist being right, with the pluralist being right, and with the atheist being
right. Neither of the two verdict phrases the brief forbids appears anywhere in this document; `verify_v16.cjs`
enforces this as a machine check.

Where a number or an external claim is reported, its source is named and its verification status stated. Web search has
failed for **nine consecutive sessions** (`MCP tool stepsearch.web_search failed: Streamable HTTP error`; probed again
this session, still failing — the blocker is on tooling, not on argument), so no external citation below was
re-verified this session. **No result in this artifact depends on an external source** — every figure is computed from
the formulas stated here.

---

## 0. The open problem, stated precisely

The brief's fourth deliverable is "the logical structure of the problem," naming the argument from religious diversity,
divine hiddenness, the problem of evil, and the Euthyphro dilemma. The corpus has formalised hiddenness twice (r4
`god-religions-hiddenness-formal.md`, r5 `god-religions-hiddenness-identifiability.md`), and r3's
`god-religions-truth_bridge_premise_formal.md` gave diversity a **bridge-accounting** treatment (Table 1, row A1:
"`BF = ⟨τ⟩_w` on the neutral bridges; the offense bridge is stipulated, not measured").

Three things were never done, and they are the whole content of this artifact:

1. **Diversity's datum is the only one in the domain whose [T] component is multiply replicated and instrumented.** The
   hiddenness argument's minor premise (non-resistant nonbelief exists) is [T] but r4's Theorem H1 showed its base rate
   `q` **cancels exactly** out of the Bayes factor. Diversity's minor premise — that religious affiliation tracks
   birth-culture — is [T] *and* independently measured across many populations. Nobody asked whether that extra
   empirical strength buys anything. **Theorem D1: it does not.**
2. **Diversity is the only classic argument whose structure is *comparative across many rivals* rather than two-hypothesis.**
   Hiddenness, evil, and religious experience are all `H` vs `¬H`. Diversity is `H₁` vs `H₂` vs … vs `H_M`. The relevant
   object is a **posterior simplex**, not a single Bayes factor, and the two-hypothesis intuition misleads here.
   **Theorem D2** makes this exact.
3. **Euthyphro has no artifact at all.** r3's row A4 correctly records "BF **undefined** in the evidential sense" but
   does not say *why*, beyond "there is no E." **Theorem D4** gives the reason.

---

## 1. Setup

**Rivals.** Let `H₁ … H_M` be the mutually exclusive divine-conception families of the companion taxonomy
(`god-religions-taxonomy.md` §1), at the granularity that corpus uses: classical monotheism counted once (Judaism,
Christianity, Islam — the three traditions differ on revelation and incarnation, not on the number or nature of the
divine), Hindu devotional polytheism, ANE/Greco-Roman polytheism, pantheism, panentheism, Advaita Vedānta, deism, and
Buddhism/Jainism. That is **M = 10**. `verify_v16.cjs` checks each of these ten labels appears in the taxonomy.

**`M` is an analytic individuation, not a discovery.** The same taxonomy's §6.1 counts distinct *religions* at
N ≈ 4 000–10 000+ and notes the count "depends entirely on how 'distinct' is individuated." Denominations, sects and
schools sit between the two counts. Theorem D2's point is that the *structure is invariant to where you cut*; only the
price changes.

**Priors.** Following the corpus's own convention (`README.md`: "the τ_req lattice assumes an even start"), the
baseline case is the uniform prior `P(H_i) = 1/M`. §5 states what a non-even prior does.

**Evidence.** `D` denotes the diversity datum, with three separable components:

| # | component | tag | status |
|---|---|---|---|
| (a) | religious affiliation is strongly correlated with birth-culture | **[T]** | real and independently measured across many populations. *Value not re-verified this session (§8).* |
| (b) | the families make mutually incompatible claims | **[T/O]** | documented claim-by-claim in taxonomy §1 (one God vs. many vs. none vs. "one but non-personal") |
| (c) | the rival traditions carry **equal epistemic warrant** | **[NT]** | **normative.** This is the load-bearing premise and it is not a measurement |

The standard reconstruction (taxonomy §3.1, after Hick, *An Interpretation of Religion*, 1989) runs: (a) + (b) + (c) ⟹
claims to unique truth are undercut. Taxonomy §3.1 already noted the argument is "*empirical* as to the correlation and
the incompatibility [T/O], but its force against exclusivism is philosophical, not deductively coercing." This artifact
supplies the arithmetic behind that sentence.

---

## 2. Theorem D1 — Transmission Invariance: the [T] datum is inert

**Model (stipulated, and stipulated by both sides).** Affiliation propagates by cultural transmission: each generation
retains the natal family with probability `β ∈ [0,1]` and converts according to a row-stochastic matrix `Q`, starting
from `π₀` over the M families. Write the resulting distribution `π = π₀ Qᵗ`.

Let the predicted share of family `k` under rival `H_i` be written with an **availability surplus** `s ≥ 0` — the weight
given to the possibility that some of family `i`'s adherence is determined by **access to truth** rather than by
transmission:

> `p^{(i)}_k = π_k · (1 − π_i − s)/(1 − π_i)` for `k ≠ i`, and `p^{(i)}_i = π_i + s`.

(`s = 0` is pure transmission. `s > 0` is the availability mechanism, used and priced in §4.)

**Theorem D1.** If `s = 0` — i.e. if the observed distribution is fully accounted for by transmission — then
`P(D | H_i) = P(D | H_j)` for **every** pair `i ≠ j`, exactly. Hence `BF_ij = 1` exactly, for all pairs.

**Proof.** With `s = 0`, `p^{(i)} = π` for every `i`, and the likelihood reduces to the pure-transmission multinomial
whose parameters `(π₀, Q, t, β, N)` are stipulated common to all rivals. ∎

`verify_v16.cjs` confirms the equality numerically (max residual reported over random models) **and** confirms the
theorem is not vacuous by recomputing at `s > 0`, where the predicted shares separate.

> **Corollary D1a — the posterior returns exactly to the prior.** With `a = 0` and uniform priors, the posterior on
> every rival is `1/M`. The most replicated [T] premise in this entire domain leaves the credal state **exactly** where
> it found it. In information terms: **zero bits of discrimination.**

### 2.1 Why this is stronger than r4's Theorem H1

Hiddenness's neutrality was **conditional on a parameterisation** — the two-cell model `P(E|H,¬b) = q·r`. r5 granted
the objection that this condition is substantive and showed that relaxing it leaves the Bayes factor *unidentified*
rather than neutral. D1's neutrality is conditional on something weaker and much better attested: **that the
distribution of belief is produced by the transmission mechanism that the sociology of religion independently measures.**
That is not a modelling convenience imported by the analyst; it is what (a) *is*.

### 2.2 The obvious objection, and where it lives

> *"But if a truth-seeking God existed and wanted relationship, we would expect less birth-correlation and more
> independent convergence. So the datum **is** evidence against the exclusivist."*

This objection is correct, it is the strongest form of the argument, and it is **not** a counterexample to D1. It is a
claim that `s > 0` — that the observed distribution is *not* fully accounted for by transmission, because a truth-
seeking God would add an availability surplus. D1 says nothing about whether `s > 0`; it says only that `s = 0`
yields neutrality. The objection therefore **relocates** the entire force of the argument into `s`, and §4 is the price
list for `s`. Note the symmetry: the exclusivist who replies "transmission is how truth is also passed on" (taxonomy
§3.1, response (i)) is *also* asserting a value of `s`. **Both horns of the argument are availability claims, and neither
is measured.**

---

## 3. Theorem D2 — Mode versus confidence: the M-penalty

Under any rival `H₁` that receives relative likelihood `m = P(D|H₁)/P(D|H_j) > 1` against each of the other `M−1`
rivals, with uniform priors:

> **posterior(H₁) = m / (m + M − 1).**

**Theorem D2.**

1. **Mode.** `H₁` is the *most probable* rival as soon as `m > 1`. A Bayes factor barely above unity suffices.
2. **Confidence.** Reaching posterior `p` requires `m = p(M−1)/(1−p)`.
3. **M-penalty.** `∂posterior/∂M < 0` at fixed `m`. The requirement is **linear in M**:

| target posterior `p` | `m` required, M = 2 | M = 3 | M = 5 | M = 10 | M = 100 | M = 10 000 |
|---|---|---|---|---|---|---|
| 0.50 | 1 | 2 | 4 | 9 | 99 | 9 999 |
| 0.90 | 9 | 18 | 36 | **81** | 891 | 89 991 |
| 0.99 | 99 | 198 | 396 | **891** | 9 801 | 989 901 |

Read row 3 across: **demanding 99% confidence on one tradition costs 9 801 times the discriminating evidence at
M = 100, and 989 901 times at M = 10 000.** Every row is linear in M.

> **Corollary D2a — the diversity argument is M-amplifying.** The argument's own rhetorical work is to increase the
> number of traditions one takes seriously (Hick's pluralism is precisely the insistence that all the great traditions
> are live options). Under Theorem D2 that work **lowers** the confidence any single tradition can be certified to. The
> argument that multiplies the candidate space simultaneously multiplies the evidence needed to pick one winner. This
> is not a paradox; it is the same quantity viewed from both ends.

> **Corollary D2b — mode ≠ certification.** The gap between `m = 1.01` (the mode) and `m = 81` (90% at M = 10) is
> where the entire intuitive force of the argument lives. "The evidence favours my tradition" and "the evidence
> establishes my tradition" differ by **two orders of magnitude** in `m` at M = 10, and by **five** at M = 10 000
(89 991/1.01 ≈ 8.9 × 10⁴).

### 3.1 Relationship to taxonomy §6.1 — no novelty claimed where the arithmetic already exists

Taxonomy §6.1 did this arithmetic once, in passing: "a BF of 1000 that favoured one *specific* tradition against each of
~10⁴ rivals would put that tradition at ≈ 9.1%." That is Theorem D2's formula evaluated at `M = 10⁴, m = 1000`
(`1000/(1000+9999) = 0.0909`). §6.1's conclusion — "past BF ≈ 1000 the posterior saturates, because the bound is set by
the size of the candidate space, not by the strength of the evidence" — is the same finding. **What §6.1 did not extract
is the mode/confidence split (D2a–b) or the M-monotonicity**, and it did not connect the lattice to the availability
question, which is §4.

### 3.2 The information-theoretic form

Isolating one candidate from `M` rivals requires `log2(M)` bits of *discriminating* evidence (taxonomy §6.1: 3.0 bits
at M = 8, 13.3 bits at M = 10 000). Theorem D2 is the odds form of the same constraint. The diversity datum, by D1,
supplies **0 bits**.

---

## 4. Theorem D3 — the price of escaping D1

D1's neutrality is bought at `a = 0`. To make the diversity datum probative one must posit `a > 0`: differential
availability across families. Substituting the availability model of §2 into the likelihood gives, for rival `H_{i*}`
against rival `H_j`:

> `BF(i*, j) = Π_k [ p_k^{(i*)} / p_k^{(j)} ]^{N π_k}`, `p^{(i)} = (1−a)π + a·δ_i`

**Theorem D3 (even-start symmetry).** If `π` is uniform over all M families, then `BF(i*, j) = 1` for **every** pair
`i, j` and **every** value of `a ∈ [0,1)`. No availability differential, of any size below the degenerate limit,
breaks the tie. (Scope: `a = 1` is a point-mass limit in which both predictions become δ-functions and the ratio is
0/0; it is excluded, and `verify_v16.cjs` enforces the exclusion.)

*Proof sketch.* With uniform `π` and `a = 0` the likelihood is flat by symmetry. With `a > 0`, `p^{(i)}` is a rotation
of `p^{(j)}` under the permutation group, and the observed multinomial weights `π_k = 1/M` are invariant under that
group, so the product is unchanged. ∎ `verify_v16.cjs` confirms this exactly by brute force over random `a`, random `M`.

**This matters because the even start is the corpus's own baseline** (`README.md`). On the even start, "escape from D1"
is not merely expensive — it is **impossible**.

### 4.1 Off the even start: the price is second-order in the very quantity nobody measures

Reparametrize availability as a **recruitment surplus** `s ≥ 0`: family `i*` holds `s` more of the population than
transmission alone predicts, the surplus being drawn from the other families in proportion to their shares:

> `p^{(i)}_i = π_i + s`, `p^{(i)}_k = π_k · (1 − π_i − s)/(1 − π_i)` for `k ≠ i`; and symmetrically for `p^{(j)}`.

Take the observed distribution `D` to be consistent with a measured surplus `δ` for the modal family 1:
`D_1 = π_1 + δ`, `D_k = π_k(1 − π_1 − δ)/(1 − π_1)`.

> **Corollary D3a — first-order flatness (exact).** `∂BF(1, j)/∂δ = 0` at `δ = 0`, for every `j`, every `π`, every `M`,
> every `N`. The diversity datum has **no first-order leverage** on differential availability.

The proof is a two-line cancellation, and `verify_v16.cjs` checks the identity symbolically-numerically: write
`u = 1 − π_1`, `v = 1 − π_j`. The three contributions to `∂(log BF)/∂δ` at `δ = 0` are
`A = π_1/v − π_j/u` (modal and runner-up terms), `C = (1 − π_1 − π_j)(u − v)/(uv)` (all remaining families), and
`A = (π_1 − π_j)(1 − π_1 − π_j)/(uv) = −C` exactly, so `A + C = 0`.

> **Corollary D3b — the surviving term is quadratic.** `log BF ≈ ½ · C₂ · N · δ²`, where
> `C₂ := ∂²(log BF)/∂δ²|₀ / N` is the **per-sample** curvature. Inverting for a required relative likelihood
> `m_req`:
> **`δ_min = √( 2 ln m_req / (C₂ N) )`.**

> **Audit correction (caught by `verify_v16.cjs` on first run).** An earlier draft of this corollary claimed `C₂`
> **vanishes whenever `π₁ = π₂`** ("families 1 and 2 are then exchangeable, so `BF = 1` identically"). **That is false
> in this model**, and the verifier now pins the correction at five equal-share cases: at `π₁ = π₂ = π` the exact value
> is `C₂ = 2(1/(uπ) + 1/u²)` with `u = 1 − π` — **15.625** at the reference even-pair `π = 0.20`, not 0. The
> exchangeability intuition fails because the **datum** credits the measured surplus to family 1 (`D = g`) while the
> rival's prediction credits it to family `j` (`h`): the observation itself breaks the 1↔`j` swap even when the two
> families' transmission shares are identical. Exact even-start neutrality is **Theorem D3**'s mixing-parameter
> result (`BF ≡ 1` for all `a` under uniform `π`), a different parameterisation; it does not transfer to `δ`, and the
> draft had silently borrowed it across models.

Reference case — `M = 10`, modal share `π_1 = 0.33`, runner-up `π_2 = 0.20`, remaining eight families sharing `0.47`,
`N = 10⁵` (`C₂ = 14.5042`, recovered by Richardson-extrapolated differences and confirmed by exact-function series
fit in `verify_v16.cjs`):

| target posterior | `m_req` (Thm D2) | `δ_min` | at `N = 10⁶` |
|---|---|---|---|
| 0.50 | 9 | 1.7 × 10⁻³ | 5.5 × 10⁻⁴ |
| 0.90 | 81 | **2.5 × 10⁻³** | 7.8 × 10⁻⁴ |
| 0.99 | 891 | 3.1 × 10⁻³ | 9.7 × 10⁻⁴ |

**Reported honestly, against this artifact's own interest.** The surpluses are **small** — about 2.5 per thousand of
all adherents certifies a modal family at 90% in a sample of 100 000 (the pre-fix draft said 7 per thousand, having
divided by a `C₂` ≈ 8.4× too small; the correction makes the detectability side *stronger*, not weaker, and leaves the
[NT]-status of `δ` untouched). This is not special to religious arguments: it is the ordinary large-`N` behaviour of
Bayesian testing, in which any consistent effect becomes detectable given enough samples. Three consequences follow,
and they are the point of the section:

1. **The discrimination is available in principle and unavailable in practice, for one specific reason: `δ` is [NT] and
   is not measured.** No instrument, archive, or survey partitions the world's adherents into "held because transmitted"
   and "held because true." The literature stipulates `δ` in both directions (§2.2).
2. **The scaling is `1/√N`, not `1/N`** — a consequence of D3a's flatness. Doubling the evidence buys only `√2`.
3. **The calculation treats both `D` and `π` as known exactly.** Both are estimated; the estimation-error floor is not
   modelled here and would raise `δ_min` substantially. The `δ_min` column is a **lower bound** on the price, not the
   price. It is also quoted at a *stipulated* `π₁ = 0.33, π₂ = 0.20`, and `δ_min` is sensitive to both.

### 4.2 Reconciliation with r3's Theorem 2

The availability price (`δ_min` in the surplus model, `a_min` in the mixing model) and r3's bridge-accounting
`m_req = 9(M−1)`-style requirement are the *same* requirement arrived at twice: once from the prior side (how much
tilt the reader supplies) and once from the likelihood side (how much differential availability the mechanism
supplies). Two likelihood-side derivations (plus the prior-side one) land on the same *order* — a few per mille of the
population — which is a **consistency check**, not three discoveries. The substantive point is r3's: in every case the
quantity that does the work is stipulated.

---

## 5. Theorem D4 — Euthyphro is D1 in disguise

Plato's question (*Euthyphro* 10a): is the pious loved by the gods *because* it is pious, or pious *because* loved?
Modern horns:

- **Horn P — independence.** Moral facts hold independently of the divine.
- **Horn V — constitution.** Moral facts are constituted by the divine will/nature.

**Theorem D4.**

1. **Horn P is exactly neutral.** If moral facts are independent of `H`, then `P(M | H) = P(M | ¬H)` by the content of
   the horn, and `BF = 1` **exactly** — no bridge, no parameter. Horn P is the *only* classic argument in this domain
   with a clean, exact, parameter-free neutrality.
2. **Horn V inherits D1.** If moral facts are constituted by divine will, then
   `P(M | H) = Σ_w P(M | w) · P(w | H)` where `w` ranges over the competing doctrinal readings of that will. The
   distribution `P(w | H)` over rival readings is *exactly* the object D1 neutralizes: under the transmission model each
   reading is held at `1/M`. Hence `BF_V = 1` **unless a doctrinal lock-in is already assumed** — i.e. unless one has
   *already* adjudicated the identification question. `verify_v16.cjs` confirms the collapse numerically.
3. **The perfect-being third horn** (Aquinas; Adams, *Finite and Infinite Goods*, 1999) indexes the moral datum to the
   divine nature. That nature is **[NT]** by the taxonomy's own ledger (rows 11–14: beyond being, ground of
   consciousness, necessarily existing, *nirguṇa*). So `BF` is **unmeasurable**, not equal to 1. This is strictly worse
   than horn P and not better than horn V: it is a stipulation with a number attached.

> **Conclusion D4.** Euthyphro has **no evidential content of its own**. Horn P is neutral by definition; horn V is
> neutral by D1; the third horn is [NT]. Unlike diversity, it does not even possess an *inert* [T] datum — it has no
> datum at all. **This is why r3's row A4 correctly records "BF undefined in the evidential sense,"** and it is the
> purest instance of the category error the brief's §3.5 item 5 names: moral and metaphysical commitments are framework
> choices under which empirical data are read, not predictions competing for the same data.

**Scope, stated so the conclusion is not over-read.** Theorem D4 says nothing about **moral realism**, about whether
metaethical views are true, or about which horn is correct. Those are contested philosophical positions, out of scope by
protocol, and D4 does not adjudicate them. It says only that the dilemma is not an argument that a dataset can settle.

---

## 6. Non-even priors, and the two escapes

1. **Non-even priors do not change the structure.** A skewed prior changes which posterior `m` delivers; it does not
   change `m_req(p, M)`. With `P(H₁) = π₁`, reaching posterior `p` requires `m = p(1−π₁) / (π₁(1−p))`, still linear in
   the mass on the rivals. The even start is the clean case, as `README.md` already says.
2. **Shrinking M.** A proponent may legitimately reply that only two hypotheses are live (theism/atheism), which drops
   `m_req(0.9)` from 81 to 9. This is a real move — but it is a move *away from* the diversity argument, and it is
   itself a **[NT]** claim about which traditions are live. The diversity argument cannot both enlarge the candidate
   space (its own rhetorical function) and shrink it (to cheapen certification).
3. **Migrating `a` to [T].** The single change that would matter: an independent, measured route to differential
   availability. §7.

---

## 7. What I established, what remains unknown, what would change my mind

**Established (conditional on stated models, all machine-checked in `verify_v16.cjs`):**

- **D1.** The diversity argument's [T] core — birth-culture correlation — is **exactly** neutral across all rivals when
  produced by transmission: `BF_ij = 1`, posterior returns to the prior, zero bits of discrimination.
- **D2.** Certification is **mode ≠ confidence**; `m_req = p(M−1)/(1−p)`; linear in M; the argument is M-amplifying.
- **D3.** Escaping D1 requires differential availability `a`; on the even start **no value of `a` works**; off it, the
  price is **second-order, not linear** (audit correction — see §10): in the surplus model
  `δ_min = √(2 ln m_req/(C₂ N))` ≈ **2.5 × 10⁻³** of all adherents for 90% at `M = 10`, `N = 10⁵` (§4.1 reference), and
  in the mixing model `a_min ≈ √(2 ln m_req/(N(1/πⱼ − 1/πᵢ)))` ≈ 6.8 × 10⁻³ there. Small — and unmeasured.
- **D4.** Euthyphro has no evidential content of its own: horn P exactly neutral, horn V neutral by D1, third horn [NT].

**Remains unknown:**

- **`a` is not measured and not measurable here.** Theorem D3 states what discrimination *costs*; it does not evaluate
  whether it is worth paying. Any actual value of `a` is a theological and normative commitment, out of scope by
  protocol.
- **`π` is estimated, and the estimation-error floor on `δ_min` is not modelled** (§4.1 item 2). The `δ_min` column is a
  lower bound.
- **Premise (c) — equal warrant — is [NT] and is the argument's actual load-bearing premise.** D1 and D2 determine what
  the [T] premises can do; they do not touch (c), in either direction.
- **External sources unverified this session** (§8). No figure depends on them.

**What would change my mind:**

1. **A measured route to `a`** — an observable consequence of differential availability that does not presuppose which
   family is true. This is the diversity analogue of r5's "identification of `u`," and it is the only thing that would
   give the argument's [T] premise decisional content.
2. **A model in which the birth-correlation datum is not a transmission product** — i.e. a mechanism under which
   `P(D | H_i) ≠ P(D | H_j)` without positing `a`. D1 is conditional on transmission; a demonstrated non-transmission
   mechanism with measured parameters would break it. None is on the table.
3. **A per-rival likelihood ratio demonstrably ≠ 1 and measured rather than stipulated** (carried from r3, unchanged).
4. **A reduction of M that is itself argued rather than assumed** — which would be a *different* argument, not a
   strengthening of this one.

None of these currently holds.

---

## 8. Sources

Named for provenance; **none re-verified this session** (web search failed, **ninth** consecutive session — probed once
more this session and still failing). **No figure in this artifact depends on any of them.**

- John Hick, *An Interpretation of Religion* (1989) — the diversity argument, reconstructed in taxonomy §3.1 and r3
  Table 1 row A1.
- Plato, *Euthyphro*, ~10a — the dilemma (ground truth in this brief; stated in taxonomy §3.4).
- Robert M. Adams, *Finite and Infinite Goods* (1999) — the perfect-being response, reported not adjudicated (§5).
- Birth-culture correlation: the empirical literature on religious socialisation ( Pew Research Center, *Religious
  Landscape Study*, 2014, being the most-cited large-sample instance). **The point estimate is not used anywhere in this
  artifact** — Theorem D1 holds for any `β` and any `π`, and the §4.1 `δ_min` table states its own `π₂` and `N` as stipulated
  reference values.
- All formal content is recomputed from the formulas stated above by `verify_v16.cjs`; no external claim is load-bearing.

---

## 9. Verification

`verify_v16.cjs` — fresh, shares **no code** with `verify_v9/v10/v12/v13/v14/v15.cjs`. Deterministic PRNG (mulberry32).
Checks by brute force over random models and by adversarial search, never by re-asserting the artifact's closed forms.

- **D1** — neutrality at `a = 0` verified pairwise across random models (max residual reported); **non-vacuity** verified
  by recomputing at `a > 0` and requiring the likelihoods to separate.
- **D1a** — posterior at `m = 1` equals `1/M` exactly, random M.
- **D2** — closed form `m/(m+M−1)` against brute-force normalisation of a full random likelihood simplex; the §3
  table recomputed entry-by-entry; M-monotonicity verified numerically; cross-check that the formula reproduces
  taxonomy §6.1's 9.1% at `M = 10⁴, m = 1000` and r3's 9:1 / 99:1 requirements at `M = 2`.
- **D3** — even-start symmetry verified over random `a ∈ [0,1)` and random M (all pairs equal); non-vacuity off the
  even start required (some `a` must break the tie). **D3a** — the flatness identity `A + C = 0` checked algebraically
  and by finite differences over 20 000 random `π` (every `π`, `M`, `N`; the true first derivative is exactly 0, so the
  numeric check is a residual bound on O(1)-sized terms). **D3b** — the quadratic law `log BF ≈ ½C₂Nδ²` checked against
  the exact function; `C₂` recovered by Richardson-extrapolated differences and required to equal the artifact's quoted
  14.5042; the §4.1 `δ_min` table recovered by **exact bisection** (overflow-safe, on `log BF = ln m_req`) and required
  to match the quoted cells; `C₂(π₁ = π₂) = 2(1/(uπ) + 1/u²)` pinned at five equal-share cases; the mixing-model
  `a_min` recovered by bisection and required to match the quadratic law within 5%.
- **D4** — horn P's `BF = 1` exactly; horn V's collapse to 1 under a uniform doctrinal distribution, verified by brute
  force, and required **not** to collapse when the distribution is skewed (non-vacuity).
- **Protocol** — the two forbidden phrases absent; no asserted verdict; the ten rival labels checked present in the
  companion taxonomy; the [T]/[NT] tags of §1's table counted from this file's own markdown.

Run `node verify_v16.cjs` from this directory.

---

## 10. Audit trail (r6): what the independent verifier caught

`verify_v16.cjs` **failed 23 checks on its first run against this draft**, and **six were real errors in the
artifact**, not script mis-specifications. All six are fixed above; the failing numbers are recorded here so the
correction is auditable rather than silent. This is the **fourth consecutive round** in which the adversarial
verifier/reviewer caught an error of the same class — a dropped term or a mis-evaluated lattice cell — and each time
the headline survived while the stated reason got more general or the numbers got corrected.

1. **D2 lattice, three cells** (§3 table): the `M = 100` and `M = 10⁴` columns were computed with `M` in place of
   `M−1` in the tail: 9 891 → **9 801** (99% at M = 100), 89 999 → **89 991** and 989 999 → **989 901**
   (90% / 99% at M = 10 000). The prose under the table and D2b's order-of-magnitude count ("four" → **five**) were
   corrected with them.
2. **`C₂ = 1.7272` was wrong by ≈ 8.4×.** The exact per-sample curvature of the §4.1 surplus model at the stated
   reference point (`M = 10`, `π₁ = 0.33`, `π₂ = 0.20`) is **14.5042** — Richardson-extrapolated central differences,
   cross-checked against a series fit of the exact function and against the bisection-recovered `δ_min`.
3. **The `δ_min` table was computed from the wrong `C₂`** and is ≈ 2.9× too large throughout: 5.0 / 7.1 / 8.9 × 10⁻³
   → **1.7 / 2.5 / 3.1 × 10⁻³** at `N = 10⁵`; 1.6 / 2.3 / 2.8 × 10⁻³ → **5.5 / 7.8 / 9.7 × 10⁻⁴** at `N = 10⁶`. The
   correction **strengthens** the in-principle detectability side (a *smaller* surplus suffices at large `N`) and leaves
   the practical barrier — `δ` is [NT] and unmeasured — untouched. Both directions of the error are reported, not only
   the convenient one.
4. **"`C₂` vanishes whenever `π₁ = π₂`" was false.** In the D-weighted surplus model the *datum* credits the measured
   surplus to family 1 while the rival's prediction credits it to family `j`, so the observation itself breaks the
   1↔`j` swap even when the two families' transmission shares are identical; the exact value is
   `C₂ = 2(1/(uπ) + 1/u²)` = **15.625** at the reference even-pair `π = 0.20`. The draft had borrowed Theorem D3's
   exchangeability (which is about the *mixing* parameter `a` under uniform `π`) and applied it to a different model.
   Two parameterisations, two symmetries — the fix keeps them separate.
5. **§7's linear availability price `a_min = ln(m_req)/(N π_j)` was false.** Every parameterisation tried (mixing `a`,
   surplus `δ`) is **first-order flat** — that is Theorem D3a itself — so the price is **quadratic** in the availability
   parameter: `δ_min = √(2 ln m_req/(C₂ N))` and `a_min ≈ √(2 ln m_req/(N(1/πⱼ − 1/πᵢ)))`. At the reference point the
   correct 90% price is ≈ **2.5 × 10⁻³** (surplus) / **6.8 × 10⁻³** (mixing, exact bisection; the quadratic law gives
   6.68 × 10⁻³, within the cubic correction); the linear form had quoted ≈ 2.2 × 10⁻⁴,
   understating the price by ≈ 30×. The §9 check-plan line `BF ≈ exp(N a π_j)` was the same error in check form and is
   replaced by the checks actually performed. The verifier now requires the linear form to be **absent**.
6. **`a = 1` was left inside the stated symmetry range.** At the point-mass endpoint both predictions are δ-functions
   and the ratio is 0/0; the theorem is scoped to `a ∈ [0,1)` and the verifier samples `a` strictly below 1.

The remaining first-run failures were script mis-specifications (an over-tight tolerance on `log₂(10⁴) = 13.29` vs the
artifact's quoted 13.3; a strict-equality float comparison on the `m_req` column; a superscript parser that assumed a
single minus-sign codepoint), each fixed in the verifier without touching a theorem. The pattern is the one r3
recorded: **the headline results were kept only because the verifier did not share the artifact's assumptions.**
