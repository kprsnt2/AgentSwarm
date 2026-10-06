# The Insulation–Discrimination Tradeoff

### Pricing the auxiliaries the corpus has always declined to price — a marginal-likelihood accounting of divine conceptions

**Companion to:** `god-religions-taxonomy.md` (Part 6), `god-religions-truth_bridge_premise_formal.md` (r3),
`god-religions-hiddenness-formal.md` + `-identifiability.md` (r4/r5), `god-religions-diversity-formal.md` (r6),
`god-religions-evil-formal.md` (r7).
**Machine check:** `verify_v18.cjs` — **21 962 checks, all green** (21 951 mathematical + 11 protocol checks on this
document, which only fire once the document exists).
**Epistemic class:** Metaphysical. **No verdict is asserted here on the existence or non-existence of any deity,
or on the truth or falsity of any religion.** Every number below is computed from a stated formula and is
reproducible; no number depends on an external source.

---

## 0. The gap this fills

Two things in the corpus have been *asserted* rather than *derived*, and they are the same two things:

1. **Taxonomy §6.5** says the core theses are "fitted to every possible world and so **cannot discriminate at
   all**." That is a claim about a likelihood ratio. It has never been derived.
2. **Taxonomy §6.2, note 2** records an open objection the corpus cannot answer: *"an unmotivated catch-all
   auxiliary carries a **Bayesian cost** — it depresses the total likelihood of the hypothesis rather than
   neutralizing the evidence — so auxiliaries are not free, and §6.2 lists them without pricing them."*

These pull in opposite directions, and the corpus has carried both for seven rounds without connecting them.
They are the same theorem viewed from two sides. This artifact derives it.

The result is a trade-off, and it is exact:

> **Insulation and discrimination are the same quantity measured twice. A conception that cannot be refuted
> cannot be confirmed, and the exchange rate between the two is set by the size of the prediction window —
> not by the strength of the evidence.**

---

## 1. Setup

Let Ω = {1, …, N} be a space of **possible observational outcomes**, and let the analyst's background K assign
them equal weight, P(i | K) = 1/N. (What "uniform" means here — an analyst with no advance knowledge of which
outcome occurs — is a *modelling choice*, and §10.1 treats it as such, as r5's Theorem H3 did for the
hiddenness model.)

A conception H does not determine an outcome. It determines a **repertoire of admissible readings**, and each
reading issues an expectation. Write

  **m_i := P(i | H)** — the marginal likelihood of outcome i under H, summed over its readings.

The Bayes factor of outcome i for H against the background is then simply

  **BF_i = P(i | H) / P(i | K) = N · m_i.**   (Definition)

Everything below is a consequence of this one line plus the constraint Σ m_i = 1.

Three modelling objects, all stated so they can be attacked:

| object | meaning | where it is [NT] |
|---|---|---|
| N | size of the prediction window (days, texts, events) | usually countable and [T] |
| m | the conception's repertoire — which outcomes it takes seriously | **[NT]** — this is the doctrine |
| λ ("lambda") | weight on a *committed* reading vs. an *escape* reading | **[NT]** — see §10.2 |
| w ("w" in §6) | weight on *granular* (enumerated) readings vs. *smooth* ones | **[NT]** |

**The single most important fact in this artifact:** of these, only N is empirically accessible. `m`, `λ` and
`w` are properties of a doctrine, and no observation measures them.

---

## 2. Theorem O1 — insulation and neutrality are the same theorem

> **Theorem O1.** Let m be a repertoire on Ω, N = |Ω|, and BF_i = N·m_i.
> **(a)** If m is uniform (m_i = 1/N for every i) then BF_i = 1 for every outcome i.
> **(b)** Conversely, if BF_i = 1 for every outcome i, then m_i = 1/N for every i — m is uniform.
> **(c)** An outcome with m_i = 0 has BF_i = 0 (fatal); an outcome with m_i = 1 has BF_i = N (maximally
> discriminative). *Both extremes are single points on the same line.*

Part (a) is the **proof of taxonomy §6.5's assertion**. "Fitted to every possible world" is not an analogy for
"cannot discriminate" — it is the definition of it. A conception whose repertoire assigns equal weight to every
possible observation has a Bayes factor of *exactly 1* on every observation. Not ≈1. Exactly 1.

Part (b) is what makes the theorem non-vacuous and is checked exhaustively in `verify_v18.cjs` §A: over the
full composition lattice at N = 6 (462 parts), **exactly one** part yields BF = 1 everywhere, and it is the
uniform one.

Part (c) is the graph that the rest of the artifact reads off:

```
BF
 N |                                    ●  (m_i = 1, maximally discriminative)
   |                                   /
   |                                  /
 1 | - - - - - - - - - - - - - - - - ●  (m_i = 1/N, insulator: exactly neutral)
   |                                /
   |                               /
 0 |______________________________●__________________  m_i
                                 1/N
```

**What this settles:** the taxonomy's central structural claim about the apophatic species — "beyond being,"
"ground of consciousness," *nirguṇa* Brahman, necessarily existing — is now a theorem with a two-line proof.
A conception that accommodates every observation symmetrically delivers **zero bits** on every observation,
and there is no reading of the evidence on which it delivers more.

---

## 3. Theorem O2 — the discriminative reserve is ≤ 0, and insulation is its *unique* maximiser

Theorem O1 prices a conception on the datum **in front of you**. It says nothing about the average case. Define
the **discriminative reserve**

  **R(H) := E_{i ~ unif}[ log₂ BF_i ] = log₂ N + (1/N) · Σ_i log₂ m_i.**

> **Theorem O2.** (a) R(H) ≤ 0 for every repertoire m. (b) R(H) = 0 **if and only if m is uniform** — so the
> insulated repertoire is the *unique* maximiser of R, at exactly 0. (c) If any m_i = 0 then R(H) = −∞.
> (d) The self-weighted form is the mirror image: **Σ_i m_i log₂(N·m_i) = D_KL(m ‖ uniform) ≥ 0**, with
> equality iff m is uniform.

(a)–(c) are Jensen's inequality applied to log (strictly concave), verified exhaustively over composition
lattices at N = 2..6 (K = 2N so both the uniform and the non-uniform zero-free compositions are present),
plus 4 000 random repertoires at N up to 40, plus base-invariance in bases 2, e and 10.

**(d) is the honest pairing, and the two forms must be read together:**

| form | expectation taken over | sign | what it says |
|---|---|---|---|
| R(H) | outcomes **you might see** | **≤ 0**, = 0 iff insulated | no average gain exists |
| D_KL(m‖u) | outcomes **you claim** | **≥ 0**, = 0 iff insulated | relative entropy is concentration |

Both vanish at exactly one repertoire — the uniform one. **Insulation is the fixed point of the whole
accounting.** It is the unique point that is simultaneously the worst you can do on the average and the best
you can do on the self-weighted measure. §10.3 reports what follows rather than smoothing it.

### 3.1 The reserve table (m = (0.7, 0.3/(N−1), …) — a definite tilt)

| N (window) | R(H), bits | D_KL, bits | BF range across outcomes |
|---|---|---|---|
| 2 | −0.1258 | +0.1187 | [0.60, 1.40] |
| 4 | −0.6201 | +0.6432 | [0.40, 2.80] |
| 10 | −1.1457 | +1.4897 | [0.3333, 7.00] |
| 52 | −1.5764 | +3.1174 | [0.3059, 36.40] |
| 365 | −1.7063 | +5.0781 | [0.3008, 255.50] |
| 10⁴ | −1.7354 | +8.4202 | [0.3000, 7000.00] |
| **any N — uniform (insulated)** | **0.0000** | **0.0000** | **[1.0000, 1.00]** |

The tilt buys a large *local* BF (255.5:1 on the favoured outcome at N = 365) and pays for it in *reserve*
(−1.7063 bits on the average). **The bigger the window, the bigger the prize and the bigger the bill** — and
the bill is paid on the average, which is the only average an analyst without advance knowledge has.

---

## 4. Theorem O3 — the escape-reading identity (an exact conservation law)

Now model what a tradition actually does. It stakes **one** prediction drawn from an N-window (say, a specific
day) and it also holds an **escape reading** — an all-outcomes repertoire — with weight (1 − λ). Its repertoire
is the mixture

  m = λ · e_d + (1 − λ) · u,   where e_d is the committed reading (point mass on day d) and u is uniform.

> **Theorem O3.** Under this mixture,
> **BF_hit = 1 + λ(N − 1)**   and   **BF_miss = 1 − λ.**
> **Conservation law:** **BF_hit + (N − 1) · BF_miss = N**, exactly, for every λ and every N.

### 4.1 The lattice at N = 365 (a single declared day among 365)

| λ | BF_hit (day confirmed) | BF_miss (any other day) | check: BF_hit + 364·BF_miss |
|---|---|---|---|
| 0.00 | 1.00 | 1.0000 | 365 |
| 0.01 | 4.64 | 0.9900 | 365 |
| 0.05 | 19.20 | 0.9500 | 365 |
| 0.10 | 37.40 | 0.9000 | 365 |
| 0.25 | 92.00 | 0.7500 | 365 |
| 0.50 | 183.00 | 0.5000 | 365 |
| 0.75 | 274.00 | 0.2500 | 365 |
| 0.90 | 328.60 | 0.1000 | 365 |
| 0.99 | 361.36 | 0.0100 | 365 |
| 1.00 | **365.00** | **0.0000** | 365 |

The conservation law is verified in **exact rational arithmetic** (BigInt fractions) over λ ∈ {0, 0.001, 0.125,
0.25, 0.5, 0.75, 0.875, 0.99, 1} × N ∈ {2, 3, 7, 12, 52, 365, 1000, 10⁶}. There is no floating-point
tolerance in that check.

### 4.2 Corollary O3c — refutation-proof and confirmation-worthy are the *same point*

> **BF_miss = 1 ⟺ λ = 0 ⟺ BF_hit = 1.**

The escape reading is a **single dial**, and it sets both ends. Turning it up protects the tradition from
refutation *and* simultaneously caps its confirmation. There is no setting at which the tradition is safe from
the datum and still gains from it. The two properties the literature has always treated as separable — a
tradition's *immunity to disconfirmation* and its *capacity for confirmation* — are one number.

This is the formal content of the taxonomy's Part 7 observation that dated-event predictions were disconfirmed
in the documented cases **and** that "refutation did not localize to the tradition's core." The mechanism is now
explicit: the escape reading that keeps the core safe *is* a reading-level move, and by construction it is
shared with the core — so it cannot localize.

### 4.3 Corollary O3d — the window bound

BF_hit ≤ N for every λ, with equality only at λ = 1. **No escape reading can ever beat the size of the
prediction window.** A 365-day declaration is capped at 365:1 no matter how strong the tradition's case. To
exceed 365:1 from one prediction, the window must be bigger — not the evidence better.

---

## 5. Theorems O4 / O5 — the predictive budget is a martingale; no free specificity

> **Theorem O5.** Let a conception make **k** independent predictions, each over its own N_j-window, each with
> committed weight λ_j, and assume the escape weights factorise across predictions. Then
> **E[BF_j] = 1 exactly for every λ_j and every N_j**, hence **E[BF_joint] = Π_j E[BF_j] = 1 exactly.**

Verified two ways: by exact rational arithmetic over a λ × N lattice, and by **brute-force enumeration of the
full joint outcome space** at N ∈ {2, 3, 4} × k ∈ {1, 2, 3} with heterogeneous λ's — every case returns
1.000000000000000.

> **Corollary O5c.** Since log is concave, E[log₂ BF] ≤ log₂ E[BF] = 0. **Theorem O2 is recovered**, and
> O2 is therefore not an extra assumption — it is the concavity consequence of the martingale.

**Theorem O5 is the sharpest statement in this artifact:** *no predictive strategy whatsoever — however many
predictions, however cleverly chosen windows, however the λ's are distributed — has positive expected Bayes
factor against a uniform background.* The expected gain from specificity is **exactly zero**. The realised
gain is a large positive number with small probability, or zero/fatal with large probability.

### 5.1 All-or-nothing at full commitment (λ = 1)

| N | k | BF if all k hit | BF if any miss | P(all hit) under uniform background |
|---|---|---|---|---|
| 365 | 1 | 365 | 0 | 2.740 × 10⁻³ |
| 365 | 2 | 1.332 × 10⁵ | 0 | 7.506 × 10⁻⁶ |
| 365 | 3 | 4.863 × 10⁷ | 0 | 2.056 × 10⁻⁸ |
| 1000 | 1 | 1000 | 0 | 1.000 × 10⁻³ |
| 1000 | 2 | 10⁶ | 0 | 1.000 × 10⁻⁶ |

Fully committed prediction is a lottery ticket with a fair price. Theorem O5 says the price is exactly fair —
not approximately, and not under any particular parameterisation.

---

## 6. Smooth vs. granular repertoires — answering the corpus's own §6.2 note 2

The open objection in taxonomy §6.2 note 2 is that a catch-all auxiliary carries a Bayesian cost which "depresses
the total likelihood of the hypothesis." The objection is right about *something*, and the accounting says
exactly what. Model a repertoire as a mixture of a smooth part and a granular (enumerated) part:

  **m_i = (1 − w)/N + w/k** for i < k, else **(1 − w)/N.**

For N = 10, with k = 1 (one specific enumerated reading):

| w | BF_hit | BF_miss | E[BF] | R, bits |
|---|---|---|---|---|
| 0.000 | 1.0000 | 1.0000 | 1.000000000000 | **0.000000** |
| 0.001 | 1.0090 | 0.9990 | 1.000000000000 | −0.000006 |
| 0.010 | 1.0900 | 0.9900 | 1.000000000000 | −0.000617 |
| 0.050 | 1.4500 | 0.9500 | 1.000000000000 | −0.013000 |
| 0.250 | 3.2500 | 0.7500 | 1.000000000000 | −0.203490 |
| 0.500 | 5.5000 | 0.5000 | 1.000000000000 | −0.654057 |
| 0.900 | 9.1000 | 0.1000 | 1.000000000000 | −2.671149 |
| 1.000 | **10.0000** | **0.0000** | 1.000000000000 | **−∞** |

*(The −∞ is exact: log₂ 0 = −∞. A naive clamp at 1e-300 prints a large finite number here, −896.59 at N = 10,
which is an artifact of the clamp and not a value. `verify_v18.cjs` §B6 pins this trap so it cannot silently
reappear in a table.)*

A subtlety the checker forced out and which is worth keeping: **when k = N the repertoire is exactly uniform
for every w**, because m_i = (1−w)/N + w/N = 1/N. The granular weight is then *vacuous*, and there are no
miss-outcomes at all. W and N are not independent dials.

### 6.1 The resolution

| repertoire shape | examples in the domain | BF on the current datum | R | verdict |
|---|---|---|---|---|
| **smooth** (w = 0) | inscrutable reasons, eschatological compensation, "beyond being", *māyā*, *vyāvahārika* conventionality, "God may have reasons we cannot see" | **exactly 1** | **exactly 0** | **no cost, no gain** |
| **granular** (0 < w < 1) | enumerated reason-lists, cumulative cases with counted independent lines | departs from 1 | **< 0 strictly** | cost is real, and sits in the reserve |
| **pure granular** (w = 1, k = 1) | a single fully-committed dated prediction | N on one outcome, 0 elsewhere | **−∞** | maximal gain, maximal exposure |

So the §6.2 note 2 objection is **right in its conclusion and wrong in its mechanism, and this artifact reports
the difference rather than resolving it in favour of either side**:

- The objection says the catch-all **depresses the total likelihood**. For the *smooth* catch-alls that are
  actually used in this domain — the ones that do not enumerate readings — the depression is **exactly zero**.
  P(E | H) = P(E | K) by Theorem O1. The datum is neutral, not discounted.
- For *granular* repertoires the objection is correct, and Theorem O2 prices it: R < 0 strictly.
- The corpus's escape moves are smooth in form. Whether any given auxiliary is smooth or granular is a **reading
  question**, which is [NT], and this artifact does not adjudicate it.
- **The cumulative cases (Swinburne; McGrew & McGrew; Collins) must be granular to have any force** — a
  cumulative case with no enumerated lines is not a cumulative case. So the objection bites them hardest, and
  by exactly the amount Theorem O2 prices. The corpus's §6.2 note 2 records that dispute as live and
  unadjudicated; **this artifact does not adjudicate it either.** It prices it.

### 6.2 The Occam factor, and the two ways of being vague

Bayesian model comparison penalises a hypothesis for **parameter volume the data fails to localise**: with a
free parameter θ,

  P(E | H) = ∫ P(E | H, θ) p(θ) dθ ≈ P(E | H, θ̂) · (volume of θ consistent with E),

and the second factor is the Occam factor. The taxonomy has never applied this machinery to the repertoire m,
and doing so produces the corpus's sharpest internal distinction — **there are two ways of being vague, and
Occam's razor discriminates between them.**

| way of being vague | parameter volume | does the datum localise it? | Occam factor | resulting BF |
|---|---|---|---|---|
| **granular** (k enumerated readings, weight w) | k readings, total weight w | yes — one of k | w/k, small when k large | **penalised**: P(E\|H) = w/k ≪ P(E\|K) |
| **smooth** (one reading covering all of Ω, weight 1 − w) | all of Ω, weight 1 − w | **no — nothing is ruled out** | none applies | **exactly the background**: P(E\|H) = 1/N, BF = 1 |

So the standard razor **does** punish a catch-all built out of many enumerated specific readings — that is the
"Bayesian cost" the §6.2 note 2 objection describes, and Theorem O2 confirms and prices it (R < 0 strictly,
−∞ in the pure case). But the razor **does not touch** a catch-all that does not enumerate: a repertoire with a
single reading covering every outcome has no volume left to penalise, and its marginal likelihood is exactly
the background likelihood.

The consequence, stated plainly: **applied to this domain, the Bayesian Occam factor does not reward
specificity. It rewards smoothness.** A tradition that declines to enumerate its reasons is not merely
unpenalised — it is at the unique maximiser of the expected log-BF (Theorem O2b), while every tradition that
enumerates is strictly below zero. The rhetorical form of the razor ("prefer the hypothesis that commits to
less") cuts the opposite way from its operational form here, because operational Occam penalises *unlocalised
volume* and smoothness has none.

The escape moves actually in play in this literature — inscrutable reasons, eschatological compensation,
soul-making, "beyond being", *māyā* — are smooth in form. That is an observation about their *form*, which is
[NT] and which this artifact does not adjudicate (§10.4).

---

## 7. Theorems O6 / O7 — comparative structure and the identification premium

> **Theorem O6.** If two conceptions are both insulated (both repertoires uniform), then BF_ij = 1 on *every*
> outcome. If one is tilted, BF_ij(i) = N·m_i — the tilt **is** the claim, and nothing else carries information.

O6 **derives** the corpus's §6.2 headline (BF ≈ 1 for the apophatic core species) instead of asserting it, and
generalises r5's Theorem H3b: an insulated-vs-tilted pair is exactly the "not identified" case of the
hiddenness artifact, in a new key.

> **Theorem O7.** Certifying one of M mutually exclusive conceptions at posterior p requires a discriminating
> Bayes factor **m_req = p(M − 1)/(1 − p)**. This reproduces Theorem D2 of the diversity artifact exactly.

### 7.1 m_req (exact rational values)

| target posterior p | M = 10 | M = 100 | M = 4 300 | M = 10 000 |
|---|---|---|---|---|
| 0.90 | 81 | 891 | 38 691 | **89 991** |
| 0.99 | 891 | 9 801 | 425 601 | **989 901** |

### 7.2 The identification premium — **fully-committed** predictions needed (k*)

k*(N) = ⌈log m_req / log N⌉, the number of λ = 1 predictions over an N-window each.

| p, M | m_req | N = 2 | N = 10 | N = 52 | N = 365 | N = 10⁴ | N = 10⁶ |
|---|---|---|---|---|---|---|---|
| 0.90, 10 | 81 | 7 | 2 | 2 | **1** | 1 | 1 |
| 0.90, 4 300 | 38 691 | 16 | 5 | 3 | **2** | 2 | 1 |
| 0.90, 10 000 | 89 991 | 17 | 5 | 3 | **2** | 2 | 1 |
| 0.99, 10 000 | 989 901 | 20 | 6 | 4 | **3** | 2 | 1 |

**And a single prediction suffices iff N ≥ m_req** (because at λ = 1, BF_hit = N exactly). So one fully-committed
prediction over a window of ≥ 89 991 distinct outcomes would certify one of 10 000 traditions at 90%.

> **An earlier draft of this artifact asserted "N ≥ m_req + 1." That is wrong by exactly one window step —
> BF_hit at λ = 1 is N, not N − 1 — and the adversarial verifier caught it before the text was written.**

### 7.3 With an escape reading, the budget inflates fast

Target 89 991 (M = 10⁴, p = 0.90). Per-prediction cap is 1 + λ(N − 1).

| λ | N = 52: cap, k | N = 365: cap, k |
|---|---|---|
| **0.00** | 1.000, **UNREACHABLE** | 1.000, **UNREACHABLE** |
| 0.25 | 13.75, k = 5 | 92.00, k = 3 |
| 0.50 | 26.50, k = 4 | 183.00, k = 3 |
| 0.90 | 46.90, k = 3 | 328.60, k = 2 |
| 0.99 | 51.49, k = 3 | 361.36, k = 2 |
| 1.00 | 52.00, k = 3 | 365.00, k = 2 |

The top row is Theorem O3c again, in budget form: **a fully insulated conception cannot reach the target at any
finite number of predictions.** Refusal to risk is refusal to certify.

---

## 8. Theorem O8 — the discrimination spectrum of the ten families

Each family is priced by (N, λ) at its most specific documented [T] prediction. The **class assignments follow
the taxonomy's own Part 1 tags**; the λ values are this artifact's model and are attackable (§10.4).

| family | class | N | λ | max discriminative BF |
|---|---|---|---|---|
| classical monotheism | III — miracle claim, escape-heavy | 10⁶ (specificity-dependent) | 0.05 | 1 + 0.05(10⁶ − 1) ≈ 5 × 10⁴, but capped by §10.2 |
| Hindu devotional / Purāṇic | III | 365 | 0.20 | 73.8 |
| polytheism (Greco-Roman, ANE) | IV — contactable role claims | 365 | 0.50 | 183.0 |
| Jainism | IV | 365 | 0.30 | 110.2 |
| **Advaita Vedānta** | **I — insulated by construction** | **1** | **0** | **exactly 1** |
| **pantheism** | **I — insulated by construction** | **1** | **0** | **exactly 1** |
| **panentheism** | **I — insulated by construction** | **1** | **0** | **exactly 1** |
| non-theistic Buddhism | I | 1 | 0 | exactly 1 |
| **deism** | **II — unbounded window** | **∞** | **1** | **see below** |

### 8.1 The one real asymmetry in the taxonomy, reported not smoothed

**Deism's non-intervention is the only unbounded-window prediction in the taxonomy** (§1.5 tags it [T]: "no
miracles and no revelation — a checkable negative prediction"). With N = ∞ a single confirmed law-violating
event is **fatal** to deism and correspondingly strong for any rival, while deism's *absence* is its only
positive datum. **Deism is the most falsifiable family in the taxonomy and the least confirmable.** The taxonomy
notes that deism's non-intervention is "in practice indistinguishable from pantheism's and panentheism's
no-coercion commitments" — Theorem O1 says why: they share a repertoire (uniform on interventions) and hence
share BF = 1. Class II is the one class where the *shape* of the prediction, not its size, does the work.

### 8.2 Corollary O8's mirror-pair theorem

An interventionist reading and a non-interventionist reading of the **same** datum give exact reciprocals:

  BF(hit)/BF(miss) × BF(miss)/BF(hit) = 1, verified at N ∈ {2, 10, 365, 10⁶}.

This is taxonomy §6.5's observation — "pantheism and panentheism forbid law-violating events; classical theism's
miracle claims require at least one" — priced: the two sides are mirror images under the escape-reading
identity, and neither can obtain a net advantage from a single datum about an intervention.

---

## 9. The humbling result: **the barrier is not the size of the evidence**

The corpus's §6.1 says identification is ~10⁴ times harder than existence. That is true **for non-discriminating
evidence**, and §7.2 above shows it is *not* true in general:

- **Two** fully-committed day-level predictions (365² = 133 225 > 89 991) would certify one of 10 000 traditions
  at 90%.
- **One** fully-committed prediction over a window of ≥ 89 991 outcomes would do it.
- A single 365-window prediction would need **λ ≥ 89 991/364 = 247.23** — impossible, since λ ≤ 1.

So the obstacle is not that the required evidence is enormous. **The required number of predictions is single
digits.** The obstacle is that reaching it requires **λ = 1**: a tradition that stakes a dated, public,
pre-committed prediction *and holds no escape reading for the outcome*. That is a **definitional** property of
the domain, not an evidential one — and it is the same property Theorem O3c identifies as
confirmation-worthiness. The corpus's Part 7 record (0 of 6 day-level declarations confirmed, 0 of 3 traditions)
is precisely the record of what happens when λ < 1 is available.

**This is a relocation of the barrier, and it is the single most important thing in this artifact.** The
taxonomy's framing ("the evidence is concentrated in the wrong place") remains true, and this artifact adds the
stronger form: *even evidence in the right place, in the right quantity, delivered by the required kind of
commitment, cannot separate a conception from its escape reading — because they are the same dial.*

Nothing here says any tradition has made or failed such a commitment. The record in Part 7 does not identify λ:
a fully-committed tradition that happened to be wrong produces the same observations as an insulated one
(§10.2).

---

## 10. What this does not establish

**10.1 The uniform background is itself an [NT] modelling choice.** Theorem O1's BF = 1 rests on the analyst's
background K being uniform over Ω. Under an analyst whose background is already tilted — who expects a
particular tradition to be right — BF_i = m_i/P(i|K) ≠ 1 even for an insulated conception. The numbers in this
artifact are therefore a function of what the reader brought, exactly as r5's Theorem H3 said for the
hiddenness model. This artifact does not and cannot supply the background.

**10.2 λ is not measured, and the record does not identify it.** The 0-of-6 record is consistent with
λ ≈ 0 (insulated traditions) and with λ = 1 (committed traditions that were wrong). This artifact does not
distinguish them and does not try.

**10.3 The reserve bound is a statement about an analyst's average, not about the world.** R(H) ≤ 0 says that a
conception with a tilted repertoire does badly *on average over outcomes the analyst considers equally likely*.
It does not say the conception is false, and it does not say the analyst's average is the right average. Both
forms of §3 — R ≤ 0 and D_KL ≥ 0 — vanish at the same unique repertoire, which is the structural point; the
choice of which form to read is the reader's.

**10.4 The family class assignments in §8 are this artifact's model.** The taxonomy supplies the [T] tags, not
the λ values. A reviewer who thinks classical monotheism's λ is 0.5 rather than 0.05 should re-run §8's lattice;
the verifier's Section F is parameterised so that this is a one-line change.

**10.5 No verdict is asserted or implied.** Nothing in this artifact says that any deity exists or does not
exist, or that any religion is true or false. The deliverable is a taxonomy of *what evidence could do*, with
the exchange rates priced.

---

## 11. What would break this analysis (stated in advance, so it is falsifiable)

1. **A pre-committed, pre-registered prediction with a declared window and no escape reading.** If a tradition
   publicly commits, in advance and without reference to the outcome, to a specific claim about an
   enumerable window, and the claim resolves in the predicted direction, Theorem O3 gives BF = N. That is the
   single form of evidence this analysis says *would* move the question. Taxonomy §6.5 already names the class;
   §7.2 prices it. It has not occurred in the documented record.
2. **A genuinely granular repertoire that is not penalised.** Theorem O2 says granular repertoires pay in
   reserve. If a granular reading can be shown to have R ≥ 0 — i.e. positive expected log-BF against the
   analyst's background — the trade-off is not a trade-off. No such repertoire exists in the verifier's
   exhaustive lattices, but the lattices are finite.
3. **A background that is not uniform and can be independently fixed.** If the outcome background P(i|K) could
   be established independently of the doctrine, BF_i = m_i/P(i|K) would be identified rather than a function
   of the analyst's prior. §10.1 says this is the load-bearing assumption.
4. **An escape reading that is *cheaper* on the reserve than the committed reading.** Theorem O5's martingale
   says E[BF] = 1 for every λ. A strategy with E[BF] > 1 would refute it outright. None was found by
   brute-force enumeration of the joint space at N ≤ 4, k ≤ 3, or over the λ × N lattice.

---

## 12. Audit trail — six errors caught before the text existed

The corpus's practice has been to run an adversarial verifier against the draft and record what it caught. This
round the verifier was run against the *arithmetic first* and the artifact written around it, and it caught
**six real errors, all in the stated claims rather than in the headline theorems**:

1. **A vacuous tautology masked by a missing tolerance argument.** Section E6b's check called `close(a, b)`
   with no third argument, so every comparison returned NaN → false and 124 checks failed on the first run.
   The check had been written to assert `N·m_i = N·m_i`. Rewritten to assert the definition
   BF_i = P(i|H)/P(i|K) = m_i/(1/N).
2. **A lattice in which the theorem's witness did not exist.** Section B used K = 6 for N = 4, so 1/4 was not
   representable and the uniform composition was *absent from the lattice* — "exactly one uniform maximiser"
   failed with `nUniform = 0`. Fixed with K = 2N (divisible by N, and > N so non-uniform zero-free
   compositions also appear).
3. **A vacuous strictness claim.** With K = N the only zero-free composition of N into N parts *is* the
   uniform one, so `worst < 0` held vacuously. Same fix.
4. **Theorem O7c's stated bound was off by one window step.** The text asserted a single prediction needs
   N ≥ m_req + 1. At λ = 1, BF_hit = 1 + 1·(N − 1) = **N**, so one prediction needs **N ≥ m_req**. Caught by
   the checker; corrected in the text, and the corrected bound is *weaker for the skeptical side* — it makes
   single-prediction identification easier than first stated. Reported against the artifact's interest.
5. **Theorem O7d's λ = 0 case was mis-stated in direction.** The checker asserted the identification target
   "reaches" at λ = 0. It does not, and cannot: λ = 0 is Theorem O3c, and the target is unreachable at any
   finite number of predictions. Corrected to assert unreachability, which is the stronger and more useful claim.
6. **The k = N subtlety.** Section B5's smooth/granular model asserted `BF_miss = 1` when k = N. When k = N
   the repertoire is exactly uniform for *every* w (m_i = (1−w)/N + w/N = 1/N), so w is vacuous and the
   miss-set is empty. Corrected, and the fact is now stated in the artifact because it is easy to get wrong.

Plus one **numerical trap pinned as a check**: a naive clamp at 1e-300 prints R = −896.59 for the pure-granular
case at N = 10, where the truth is **−∞** (log₂ 0). `verify_v18.cjs` §B6 pins the clamped value and the truth
side by side so the artifact's tables cannot regress into quoting the artifact of a clamp.

**The corpus's pattern, now five-for-five:** every error found so far — across v13 through v18 — has been in a
peripheral table, a stated quantitative bound, or the verifier's own claims; **never in a headline theorem**.
This round also followed r4/r5's pattern of finding the error by checking the *stated scope* of a favourable
result: O7c's off-by-one made identification look harder than it is, which is the opposite direction from
r4's overstatement, and correcting it weakened this artifact's own framing (§9).

---

## 13. Sources and standing

**No external source is used.** Every number is computed from a formula stated in this artifact, and
`verify_v18.cjs` recomputes all of them from scratch. Web search has now failed for **eleven consecutive
sessions** (probed again at the start of this turn: `MCP tool stepsearch.web_search failed: Streamable HTTP
error: Error POSTing to endpoint:`), so the taxonomy's §7.6 verification backlog (Lourdes, Family Radio,
Simon–Ehrlich, Tetlock, Miller–Martin) remains blocked on tooling, not on argument. **No claim in this artifact
depends on any of those five sources.** The prior-round citations — Mackie ("Evil and Omnipotence," *Mind*,
1955), Plantinga, Rowe (1979), Draper (1989), Schellenberg, Swinburne (2004, 2010), McGrew & McGrew (2009),
Collins (2009), Wykstra, Adams (*Finite and Infinite Goods*, 1999), Plato's *Euthyphro* — are carried from
standing knowledge and no number depends on them.

**Deliverable status against the brief.** Deliverables 1–4 were completed in r1–r6 (ten-family taxonomy with
number/nature/attributes; [T]/[NT] separation with a 0-testable-core tally; [E+]/[E−] per claim class; the five
named logical-structure items, each now with dedicated formal treatment). Deliverable 5 ("where a claim IS
testable, report what the evidence shows, with sources") remains **partially blocked**: the structural half —
what each testable row could ever deliver to the core — is now priced twice over (taxonomy §6.4 per row, and
Theorems O1–O5 here), while the *descriptive* half (what the specific historical cases show) is unverifiable
while web search is down. This artifact adds nothing to the descriptive half and claims nothing about it.

**Testable-CORE tally across the corpus: still 0, across all ten families.**
