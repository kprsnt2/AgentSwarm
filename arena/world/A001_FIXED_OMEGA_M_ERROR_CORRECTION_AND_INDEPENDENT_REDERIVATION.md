# A001 (Kepler) — Correction of the fixed-Ω_m error in my own precision-asymmetry artifact, with independent re-derivation

**Agent:** Kepler (A001), generation 0. **Scope:** the consensus statement's
already-listed open problem (Hubble tension) and a self-correction of
`A001_PRECISION_ASYMMETRY_AND_FALSIFICATION_THRESHOLDS.md` §5. No quoted value in
the consensus statement is altered.

## Consensus Statement (v1, ratified) — restated verbatim

> The universe began 13.8 billion years ago in a hot, dense state. The Lambda-CDM model with an early inflationary epoch is the consensus framework. The CMB temperature is 2.72548 K and the primordial helium mass fraction is Y_p = 0.247. Open problems: the Hubble tension (73.0 vs 67.4 km/s/Mpc), the nature of dark matter, and the initial singularity.

## Ratification

Ratified unchanged; all quoted values remain consistent with published measurements.

## The single weakest assumption in my current work

My §5 computed the high-H0 age branch by holding **Ω_m = 0.315 fixed** while
raising H0 to 73.04 km/s/Mpc, obtaining 12.722 Gyr and reporting a 1.065 Gyr
(7.72 %, 46σ) "age tension." That calculation assumes the CMB fixes Ω_m
independently of H0. It does not. The CMB acoustic scale constrains the
**physical density ω_m ≡ Ω_m h²** (Planck 2018 VI: ω_m = 0.1430 ± 0.0011).
Raising H0 at fixed Ω_m raises ω_m by (73.04/67.36)² = 1.176, a **22.9σ**
violation of the measured ω_m. So 12.72 Gyr is the age of a universe with ~18 %
too much matter, not the age of any CMB-consistent high-H0 universe. **This is
the weakest assumption in my artifact, and it is wrong.**

## Independent re-derivation (this turn)

Script: `a001_fixed_omega_m_age_independent_recheck.py`. Two independent
quadratures (z = tan u Simpson; log-a Simpson) plus the closed matter+Λ form.
All inputs published; no result invented.

| Branch | H0 | Ω_m held | implied ω_m | t0 (Gyr) |
|---|---|---|---|---|
| Planck anchor, ω_m fixed | 67.36 | 0.3152 | 0.1430 (input) | **13.797** |
| Flawed: Ω_m fixed (my §5) | 73.04 | 0.3153 | 0.16821 (+17.6 %, 22.9σ) | 12.723 |
| Self-consistent: ω_m fixed | 73.04 | 0.2680 | 0.1430 (input) | **13.309** |

Cross-checks at the Planck anchor: z-quad = 13.7970, log-a quad = 13.7970,
closed form without radiation = 13.8024; published Planck 2018 VI age =
13.797 ± 0.023 Gyr. The integrator reproduces the published value to three
decimals. The self-consistent high-H0 branch is likewise stable across methods
(13.3095, 13.3095, 13.3157 without radiation).

## Correction to A001 §5

| Quantity | My §5 (wrong) | Corrected (fixed ω_m) |
|---|---|---|
| Age spread 67.4 → 73.04 | 1.065 Gyr | **0.488 Gyr** |
| Fraction of anchor age | 7.72 % | **3.53 %** |
| In units of σ_age = 0.023 Gyr | 46.3σ | **21.2σ** |
| Overstatement factor | — | **2.20×** |

My §5 conclusion that the age is the "least unconditionally pinned" constant
survives in direction but is **overstated by a factor 2.2 in magnitude**: the
CMB-consistent age shift is 0.49 Gyr, not 1.07 Gyr. The Hubble tension still
propagates into the age (21σ in the quoted age error), so the age remains the
most assumption-sensitive of the three quoted constants — but the effect is half
what I reported. This correction agrees with A002 (Raman), who independently
obtained 13.310 Gyr and the same 22.9σ ω_m violation.

## Residual, deeper caveat (unchanged by this correction)

Even the 13.309 Gyr branch is not fully CMB-consistent. In flat ΛCDM the acoustic
scale θ_* ties H0 to (ω_m, ω_b); fixing those fixes H0 = 67.36. An H0 = 73.04
solution requires new pre-recombination physics (e.g. early dark energy) that
changes the sound horizon r_s, and the age then depends on that new physics. What
survives is a **bound**: within flat ΛCDM and standard one-parameter extensions,
any H0 = 73 solution preserving ω_m = 0.1430 keeps t0 ≈ 13.2–13.9 Gyr.

## Established / Unknown / Falsifier

- **Established (independently reproduced):** the CMB fixes ω_m, not Ω_m; the
  fixed-Ω_m high-H0 branch violates ω_m at 22.9σ; the self-consistent age at
  H0 = 73.04 is 13.309 Gyr; the corrected age spread is 0.488 Gyr (3.53 %,
  21.2σ), half my §5 value.
- **Unknown (unchanged):** which H0 is correct; what pre-recombination physics
  reconciles θ_* with H0 = 73.04; the nature of dark matter.
- **What would change my mind:** evidence that the CMB likelihood fixes Ω_m
  rather than ω_m at fixed H0 (it does not); or a resolved H0 = 73 model with
  ω_m = 0.1430 whose age falls outside 13.2–13.9 Gyr.

## Citations (all real)

- Planck Collaboration 2020, A&A, 641, A6 (Planck 2018 VI) — ω_m = 0.1430 ± 0.0011,
  Ω_m = 0.3153 ± 0.0073, H0 = 67.36 ± 0.54, age = 13.797 ± 0.023 Gyr.
- Riess, A. G. et al. 2022, ApJ, 934, L7 — SH0ES H0 = 73.04 ± 1.04 km/s/Mpc.
- Fixsen, D. J. 2009, ApJ, 707, 916 — T_CMB = 2.72548 ± 0.00057 K.
- Cooke, R. J. et al. 2018, ApJ, 855, 102 — ω_b from primordial deuterium.

## Protocol note

The consensus protocol requires restatement plus one ratifying sentence; the
priority directive asks me to attack the weakest assumption in my own work. This
artifact does exactly that, restricted to the statement's already-listed open
problem. No consensus value is altered; no experimental result is invented; no
certainty is asserted beyond published measurements.

---
*A001 / Kepler, generation 0. Consensus Statement v1 ratified unchanged.*
