# Confirmation-Ceiling Result (Part 11 — companion to god-religions-taxonomy.md)

**Standing prohibition observed:** this artifact asserts no verdict. It does not conclude
that the divine exists or fails to exist, nor that any tradition is true or false. It
*computes the maximum posterior probability that confirming evidence can assign* to the
core metaphysical claim H₀ of a tradition, and states precisely what would move that
maximum. Companion to the verified taxonomy (14-row testability ledger), the separation
result (Part 9), and the two-gate insulation result (Part 10). Standalone so the
already-verified master file keeps its 60/60 invariants intact.

## 0. Why this artifact exists

Parts 9–10 bounded the **disconfirmation** side: a refuted dated prediction delivers
zero observation-driven content to the core (reach κ ≤ 0.25, localization LR = 1.0).
The brief's item 3 and 5 demand the mirror — *what would count as evidence **for** each
class of claim*. That mirror is a distinct mathematical structure (Bayes confirmation
over a rival set, not insulation-by-auxiliary), it is quantitatively exact, and it pins
the same ceiling from the other direction. The qualitative point (under Duhem–Quine,
unfalsifiable and unconfirmable come as a pair) is standard; the contribution here is
wiring it to the ledger's own anchors — R4's 0-of-6 record, N = 9 999 rivals, and the
LR_req that the separation result already surfaced.

## 1. Model

- H₀ = the core metaphysical commitment of one tradition (the [NT]-tagged layer).
- {A₁ … A_N} = residual rival attributions that would produce the same confirming data
  E (fulfilled prophecy, verified miracle). N = 9 999 (the ~10⁴-conception set, one
  tradition singled out).
- LR_j = P(E | H₀) / P(E | A_j) is the likelihood ratio favoring H₀ over rival A_j.

Equal prior odds π_j = π₀ give the exact posterior:

    P(H₀ | E) = 1 / [ 1 + Σ_j (π_j/π₀)·(1/LR_j) ] ,   and with equal priors:  1 / [ 1 + Σ_j 1/LR_j ].

## 2. Theorem — the gating rival (confirmation ceiling)

The posterior is bounded by the **worst-treated residual rival**, not by the best
evidence. Suppose one rival A* is *flexible* on E — stipulated to reproduce whatever
the data turn out to be, so P(E|A*) = P(E|H₀) and LR_* = 1 (this is the unknown-agent
/ inscrutable-motive rival; by Duhem–Quine it need not commit to a prediction). Then:

    P(H₀ | E) ≤ 1 / [ 1 + π_*/π₀ ]  ,  independent of how large the other 9 998 LRs are
                                    and independent of how many anomalies are stacked.

- Even priors (π_* = π₀): ceiling = **1/2 = 0.50.** No volume of confirming data —
  witnessed, medically verified, however extreme — raises H₀ above 50 % against a
  single even-prior flexible rival.
- Rival 3× likelier a priori (π_*/π₀ = 3): ceiling = 0.25. 9× : 0.10.

**Corollary (compounding is possible, but only against a rival that commits).** Against
a *hardened* rival with per-independent-anomaly LR = r > 1, the bound decays as r^(−k)
over k independent anomalies; confirmation is then attainable in principle. The flexible
rival is exactly the case r = 1, where r^(−k) = 1 for every k — hence no compounding.

## 3. The asymmetry — confirm/refute as one Duhem flexibility aimed both ways

| direction | mechanism | net core reach |
|---|---|---|
| **Refute** the core (Part 10) | auxiliary escape — core defined to survive the datum; reach κ(k;a)=(1−a)^k = 0.25 (a=0.5,k=2), 0.0625 (k=4); localization LR = 1.0 | ≈ 0 |
| **Confirm** the core (this) | gating rival — the one flexible residual LR_* = 1 pins the ceiling at 0.5 (even prior) | ≈ 0 (never exceeds ceiling) |

Same Duhem–Quine flexibility: pointed outward it makes the core *insulated*; pointed
inward it makes the residual rival *incommensurable*. Symmetric outcome (≈ 0),
opposite direction.

## 4. Second gate — even a confirmed anomaly does not say *which* tradition

Even if E drove P(H₀|E) toward its ceiling, it would not identify the tradition:
pairwise core separability is 0/28 under the [NT] tags and at most 9/28 under the
strongest testable reading (Part 9), and every separable pair collapses onto the
**single** contested observation type — law-violating interruption — which all ~10⁴
conceptions claim for themselves. So a confirmed anomaly confirms *"law-violation by
some agent X,"* never *"tradition T is the true one."* The two gates chain: confirmation
dies at the gating rival (§2) *and*, surviving that, dies at separation (this §).

## 5. What would move the ceiling — the explicit bar (and falsifier)

Closed form for confirming H₀ over N equal rivals at confidence f (equal priors, equal
per-rival LR), from §1:

    LR_req(N, f) = N · f / (1 − f).

| f | required per-rival LR, N = 9 999 (even priors) |
|---|---|
| 0.90 | **89 991** |
| 0.99 | 989 901 |
| 0.999 | 9 989 001 |

So reaching merely 90 % confidence requires, **per rival**, evidence ~90 000× more likely
under H₀ than under each rival — i.e. the 89 991 figure the separation result reported.

Against a single *hardened* even-prior rival (it commits, r = 2 per anomaly), the
k-independent-anomaly bar to exceed 90 % is k ≥ 4 (P(3) = 0.8889, P(4) = 0.9412); at
r = 1.5, k ≥ 6. **I change my mind — I update the core posterior — if and only if all
three hold:**

1. **Supply:** ≥ 4 independent anomalies materialize (corroborated, mutually witnessed,
   not date-fitted). The ledger's observational peg (R4) records **0 of 6** testable
   predictive items corroborated, so the r^(−k) compounding factor is currently absent.
2. **Hardening:** the residual unknown-agent rival is *forced* to commit — LR_* fixed
   ≠ 1 — rather than left flexible (LR_* = 1). Left flexible, the ceiling is 0.5 and the
   r^(−k) factor is 1 for all k.
3. **Separation:** the anomalies discriminate (separate) the traditions — which per
   Part 9 they do not: 0/28 separable, all reducing to one shared observation type.

If supply and hardening hold but separation does not, I concede confirmation of a
*class* (law-violation occurs) while the *which-tradition* question stays open. If
hardening fails (condition 2), the ceiling stands at 0.5 regardless of anything else.
**None of the three currently holds; the honest status of the core is therefore
"ceiling-bounded, at 0.5 vs one flexible even-prior rival and gated at 89 991 for the
tradition set"** — not settled, in either direction.

## 6. Unknown / blocked

- External-source verification (Lourdes cure counts, Family Radio, Simon–Ehrlich,
  Tetlock, Miller–Martin) remains **blocked on web-search tooling** (HTTP endpoint
  error, this session). No number in §4–5 depends on those sources; they would only
  firm up the [T]-ledger's empirical rows, never the core ceiling computed here.

## Verification

`verify_v12.cjs` recomputes every figure above (60-style fresh recompute): the
posterior identity, the closed form LR_req = N·f/(1−f), the gating-rival ceiling at 0.5
across k ∈ {1,2,5,20} with LR_h = 10⁹ and 9 998 specified rivals, the hardened r = 2
crossover (k_need = 4) and r = 1.5 (k_need = 6), the R4 0-of-6 no-compounding case, the
κ = 0.25 / 0.0625 cross-check, and a banned-construction scan.
