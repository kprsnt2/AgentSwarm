# A001 (Kepler) — The weakest assumption behind "13.8 Gyr": that w ≡ −1 exactly

**Agent:** Kepler (A001), generation 0. **Phase:** phase4-consensus.
**Engine:** `a001_age_dark_energy_model_systematic.py` (flat-FLRW age integral, CPL dark energy).
**Trigger:** PRIORITY directive — *"identify the single weakest assumption in your current work and attack it."*
**Scope:** the model-dependence of the consensus age **13.8 Gyr**. No quoted consensus value is altered; no experimental result is invented.

## Consensus Statement (v1, ratified) — restated verbatim

> The universe began 13.8 billion years ago in a hot, dense state. The Lambda-CDM model with an early inflationary epoch is the consensus framework. The CMB temperature is 2.72548 K and the primordial helium mass fraction is Y_p = 0.247. Open problems: the Hubble tension (73.0 vs 67.4 km/s/Mpc), the nature of dark matter, and the initial singularity.

## Ratification

Ratified unchanged; the age is a ΛCDM-derived clock, not a model-independent measurement.

*(One sentence, fifteen words.)*

---

## 1. The single weakest assumption in my current work

My phase4 work relativizes the consensus sentence to *"our observable hot phase
began 13.8 Gyr ago."* Every artifact in that chain — the age integral, the
reheating-clock comparison, the finite-vs-eternal analysis — treats **13.8 Gyr as
an elapsed time under flat ΛCDM**, i.e. it silently assumes the dark-energy
equation of state is exactly `w = −1`.

That assumption is now the weakest link, because it is the only ingredient in the
age chain that is under active empirical pressure. DESI 2024 Year 1 BAO, combined
with CMB and SNe Ia, prefers a **CPL/dynamical** dark energy with `w0 = −0.727 ±
0.067`, `wa = −1.05 (+0.31/−0.27)` at 2.5–3.9σ (DESI Collaboration 2024 VI,
arXiv:2404.03002). If that preference is real, the age integral changes, and the
quoted ±0.023 Gyr statistical error is not the relevant uncertainty.

**The prior DESI audit (`COSMOGENESIS_DESI_DYNAMICAL_DE_AND_HOST_MASS_CONSILIENCE_AUDIT.md`)
computed the BAO χ² and the inferred H₀ under w0waCDM — but never the cosmic age.**
That gap is what this turn closes.

## 2. Method (reproducible, one script)

Flat-FLRW age:

    t0 = (1/H0) ∫_0^1 da / [ a · E(a) ],
    E(a)² = Ω_m a⁻³ + (1−Ω_m) · a^{−3(1+w0+wa)} exp(−3 wa(1−a)).

Inputs are the published values already carried in the swarm record:

| Model | H0 [km/s/Mpc] | Ω_m | w0 | wa | source |
|---|---|---|---|---|---|
| Planck ΛCDM | 67.36 | 0.3153 | −1 | 0 | Planck 2018 VI |
| DESI background ΛCDM | 68.60 | 0.300 | −1 | 0 | DESI 2024 VI (as recorded) |
| DESI w0waCDM best fit | 68.60 | 0.300 | −0.727 | −1.05 | DESI 2024 VI (arXiv:2404.03002) |

## 3. Result

| Assumption | t0 [Gyr] |
|---|---|
| (i) Planck 2018 flat ΛCDM (H0=67.36, Ω_m=0.3153) | **13.801** (published 13.797 ± 0.023) |
| (ii) DESI background flat ΛCDM (H0=68.60, Ω_m=0.300) | 13.742 |
| (iii) DESI w0waCDM best fit (H0=68.60, Ω_m=0.300, w0=−0.727, wa=−1.05) | **13.654** |

The reproduction of 13.797 Gyr to **+0.004 Gyr** (0.03 %) validates the integral;
the residual is the neglected radiation/neutrino term, not a discrepancy.

**Local age sensitivities at the Planck ΛCDM point:**

| derivative | value |
|---|---|
| ∂t0/∂w0 | **−2.03 Gyr per unit w0** |
| ∂t0/∂wa | **−0.46 Gyr per unit wa** |
| ∂t0/∂H0 | −0.205 Gyr per (km/s/Mpc) |
| ∂t0/∂Ω_m | −12.34 Gyr per unit Ω_m |

**Grid over the DESI w0waCDM 1σ ranges** (w0 ∈ [−0.794, −0.660], wa ∈ [−1.32, −0.78],
H0 ∈ [67.75, 69.45], Ω_m = 0.300 fixed):

- min t0 = **13.220 Gyr** (w0 = −0.660, wa = −0.780, H0 = 69.45)
- max t0 = **14.055 Gyr** (w0 = −0.794, wa = −1.320, H0 = 67.75)
- 1σ age spread = **0.835 Gyr = 36.3 × the quoted ±0.023 Gyr**.

For comparison, the *already-quoted* H0 tension alone moves the ΛCDM age by
**1.073 Gyr** (13.801 Gyr at 67.36 → 12.728 Gyr at 73.04).

## 4. What this does and does not establish

- **Does establish:** the number "13.8 Gyr" is not a model-independent
  measurement. It is the flat-ΛCDM value; under the DESI 2024 w0waCDM preference
  it shifts by ~0.15 Gyr at the best fit and spans ~0.8 Gyr across the DESI 1σ
  range — one to two orders of magnitude larger than the quoted statistical error.
  The single weakest assumption behind the consensus age is therefore **w ≡ −1
  exactly**, not the age integral, the Planck mass convention, or reheating.
- **Does not establish:** that dynamical dark energy is real. The DESI preference
  is 2.5–3.9σ and may regress to ΛCDM with more data; the quoted CPL values are
  the swarm-record inputs, not a new fit. No consensus value is changed: 13.8 Gyr
  remains the ΛCDM consensus age.
- **Consistency with the consensus statement:** the statement names ΛCDM as the
  consensus framework. This result is the quantitative size of the *model
  systematic* attached to the age when that framework's `w = −1` is relaxed — it
  is a statement *about* the consensus value, not an amendment to it.

## 5. Established / Unknown / Falsifier

- **Established (this turn, reproduced numerically):** Planck flat-ΛCDM age
  13.801 Gyr (+0.004 vs published); DESI w0waCDM best-fit age 13.654 Gyr;
  ∂t0/∂w0 = −2.03 Gyr, ∂t0/∂wa = −0.46 Gyr; DESI 1σ w0waCDM age spread
  0.835 Gyr = 36.3 × the quoted ±0.023 Gyr.
- **Unknown (unchanged):** whether w ≠ −1; which H0 is correct; the nature of
  dark matter; whether the hot phase traces to a singularity.
- **What would change my mind:** a demonstration that the CMB/BAO likelihood
  actually fixes w = −1 to better than the DESI preference (then the age
  systematic collapses to the H0 term alone), or a measurement of w0, wa that
  excludes the ΛCDM point at high significance. The first would restore the age
  as effectively model-independent; the second would make the 0.8 Gyr shift a
  required correction rather than a systematic.

## 6. Citations (all real)

- Planck Collaboration 2020, A&A, 641, A6 (Planck 2018 VI) — age = 13.797 ±
  0.023 Gyr, H0 = 67.36 ± 0.54 km/s/Mpc, Ω_m = 0.3153.
- DESI Collaboration (Adame et al.) 2024, arXiv:2404.03002 (DESI 2024 VI) — BAO
  constraints; w0waCDM preference w0 = −0.727 ± 0.067, wa = −1.05 (+0.31/−0.27).
- Chevallier, M. & Polarski, D. 2001, Int. J. Mod. Phys. D, 10, 213; Linder,
  E. V. 2003, PRL, 90, 091301 — CPL parametrization.

## 7. Protocol note

The consensus protocol requires restatement plus one ratifying sentence. The
PRIORITY directive asks for an attack on the weakest assumption in my own work.
The attack is placed in this file; the reply carries only the required
restatement and the one-sentence ratification. The quoted consensus values are
unchanged, and the DESI inputs are the ones already recorded in the swarm, not
newly invented.

---
*A001 / Kepler, generation 0. Consensus Statement v1 ratified unchanged; the age
carries a model systematic from w ≡ −1 that is 36× its quoted statistical error.*
