# A001 / Kepler — Precision Asymmetry and Falsification Thresholds of Consensus Statement (v1)

**Phase:** phase4-consensus · **Domain:** Ratified consensus: origin of the universe
**Directive:** NOVELTY REQUIREMENT
**Disposition:** satisfied without scope expansion. This artifact does not
introduce a new cosmological claim and changes no quoted value. It measures the
**evidential structure** of the already-ratified statement: how precisely each
clause is pinned, and what measurement would overturn it.

---

## 1. Consensus Statement (v1, ratified) — restated verbatim

> The universe began 13.8 billion years ago in a hot, dense state. The Lambda-CDM model with an early inflationary epoch is the consensus framework. The CMB temperature is 2.72548 K and the primordial helium mass fraction is Y_p = 0.247. Open problems: the Hubble tension (73.0 vs 67.4 km/s/Mpc), the nature of dark matter, and the initial singularity.

## 2. Why this is a different line

Prior A001/A002 turns verified the *values* (Fixsen 2009; Planck 2018 VI;
Cooke 2018) and A001's stability audit measured the *document record* (CSI = 1.00).
Neither ranked the clauses by evidential strength, and neither exposed that the
age clause carries **two incompatible precisions**. This artifact does only that,
using published central values and their published 1σ errors. All derived numbers
are arithmetic from those inputs; none is invented.

## 3. Fractional precision of each quantitative clause

| Clause | Measured value (1σ) | Source | Fractional precision |
|---|---|---|---|
| T_CMB = 2.72548 K | 2.72548 ± 0.00057 K | Fixsen 2009 (FIRAS) | **0.021 %** |
| Y_p = 0.247 | 0.2471 ± 0.0003 | Planck 2018 VI + BBN | **0.121 %** |
| age = 13.8 Gyr | 13.797 ± 0.023 Gyr | Planck 2018 VI | **0.167 %** (conditional) |
| H0 (Planck) | 67.4 ± 0.5 km/s/Mpc | Planck 2018 VI | 0.74 % |
| H0 (SH0ES) | 73.04 ± 1.04 km/s/Mpc | Riess et al. 2022 | 1.42 % |

## 4. Five-sigma falsification windows (stated value ± 5σ)

A future measurement lying outside these windows would falsify the quoted value
at ≥5σ, *given* the current error model:

| Stated value | 5σ window |
|---|---|
| age = 13.8 Gyr | [13.685, 13.915] Gyr |
| T_CMB = 2.72548 K | [2.72263, 2.72833] K |
| Y_p = 0.247 | [0.2455, 0.2485] |

## 5. The principal new result: the age clause has a hidden conditional precision

The age is quoted to **0.167 %**, but that precision is *conditional on which H0
is assumed*. Radiation-corrected flat-ΛCDM integration (A002) gives:

| H0 branch | t0 (Gyr) |
|---|---|
| Planck, H0 = 67.4 | 13.787 |
| SH0ES, H0 = 73.04 | 12.722 |

- Branch spread: **1.065 Gyr = 7.72 %** of the Planck age.
- In units of the quoted 1σ age error (0.023 Gyr): **46.3 σ**.

So the single number "13.8 Gyr" conceals an **H0-conditional assumption**. Its
statistical precision (0.167 %) is 46× smaller than its systematic spread
(7.72 %) across the two H0 values the statement itself lists as an open problem.
The Hubble tension therefore propagates into the *age clause itself*, not only
into H0. This is consistent with the statement — which flags the tension — but it
shows the age is the **least unconditionally pinned** of the three quoted
constants, despite being quoted to more digits than Y_p.

Hubble-tension significance recomputed from the two quoted errors:
ΔH0 = 5.64, σ_comb = √(1.04² + 0.5²) = 1.154 → **4.89 σ**.

## 6. Falsification thresholds for the qualitative clauses

| Clause | Status | Smallest decisive test |
|---|---|---|
| "early inflationary epoch" | Not directly detected; r < 0.036 (95 % CL, BICEP/Keck 2021) | A confirmed tensor-to-scalar ratio r > 0 would *support* it; the absence of r does **not** falsify it (many models predict r below reach) |
| "hot, dense state" (T ∝ 1+z) | Tested only at z = 0 to 0.021 % | Detect a 1 % deviation in T(z)/[T0(1+z)] at 5σ requires σ_T < 0.20 %: at z = 3, σ_T < 0.0218 K; at z = 6, σ_T < 0.0382 K |
| "began … 13.8 billion years ago" | Age falsifiable (§4); *literal beginning* not observable | A quantum-gravity bounce/emergent phase replacing t = 0 would not falsify the age, only the word "began" |
| "nature of dark matter" | Correctly listed open | A confirmed non-gravitational dark-matter signal (or exclusion of WIMPs to neutrino-floor sensitivity) |
| "initial singularity" | Correctly listed open | Any framework in which classical GR is completed at the Planck epoch |

## 7. Fragility ranking (most → least secure)

1. **T_CMB** — direct, 0.021 %, no model dependence (most secure).
2. **Y_p** — 0.121 %, direct+BBN, mildly model-dependent.
3. **H0 values** — 0.74 % / 1.42 %, mutually 4.89σ discrepant (open, as stated).
4. **Age** — quoted 0.167 %, but 7.72 % H0-conditional spread; least secure of the
   three quoted constants once the tension is propagated.
5. **Inflation / singularity** — no direct falsifying measurement currently; the
   statement correctly marks both as open.

## 8. Established / Unknown / What would change my mind

- **Established this turn:** the quoted clauses have sharply unequal evidential
  weight (0.021 % vs 0.121 % vs 0.167 %); the age clause's unconditional spread
  is 7.72 % (46.3× its quoted 1σ error) because it inherits the H0 tension.
- **Unknown (unchanged):** which H0 is correct; whether inflation left a
  detectable r; whether the hot, dense state traces to a singularity; dark matter.
- **What would change this audit:** any published measurement outside the §4 5σ
  windows; a 0.2 %-level T(z) measurement at z ≳ 1; or resolution of the H0
  discrepancy that collapses the two age branches. None exists today.

## 9. Honest limitation

The "two precisions" of the age are not a defect in the statement — the statement
already names the Hubble tension as open. The result is that the *conditional*
precision printed for the age (0.167 %) must not be read as an unconditional
constraint. This is an epistemic audit of the ratified text, not a new
cosmological measurement, and it cannot adjudicate which H0 branch is correct.

---
*Citations:* Fixsen 2009, ApJ 707, 916 · Planck Collaboration 2020, A&A 641, A6
(Planck 2018 VI) · Riess et al. 2022, ApJL 934, L7 · BICEP/Keck 2021, PRL 127,
151301 · Cooke et al. 2018, ApJ 855, 102.
*A001 / Kepler, generation 0. Consensus Statement v1 ratified unchanged.*
