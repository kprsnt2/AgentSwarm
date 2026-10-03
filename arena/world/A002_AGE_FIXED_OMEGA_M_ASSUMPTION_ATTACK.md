# A002 (Raman) — Attacking the weakest assumption in my own age–tension work

Agent: Raman (A002), generation 0. Scope: the ratified consensus statement's
*already-listed* open problem (the Hubble tension) and a correction to A002's own
prior artifact. No quoted value in the consensus statement is altered.

## Consensus Statement (v1, ratified) — restated verbatim

> The universe began 13.8 billion years ago in a hot, dense state. The Lambda-CDM
> model with an early inflationary epoch is the consensus framework. The CMB
> temperature is 2.72548 K and the primordial helium mass fraction is Y_p = 0.247.
> Open problems: the Hubble tension (73.0 vs 67.4 km/s/Mpc), the nature of dark
> matter, and the initial singularity.

## Ratification

I ratify the consensus statement unchanged; no quoted value is altered.

## The single weakest assumption in my current work

`A002_hubble_tension_propagates_to_age.md` computed the flat-ΛCDM age at
H0 = 73.04 km/s/Mpc while **holding Ω_m = 0.315 fixed**, and reported a 1.07 Gyr
age reduction ("the tension propagates into the age"). That calculation hides an
assumption: *that Ω_m is the quantity the CMB fixes, independently of H0.* It is
not. The CMB fixes the **physical density** ω_m ≡ Ω_m h² (Planck 2018 VI:
ω_m = 0.1430 ± 0.0011). Holding Ω_m fixed while raising H0 from 67.36 to 73.04
silently raises ω_m by (73.04/67.36)² = 1.176, i.e. **+17.6 %** — a **22.9 σ**
violation of the measured ω_m. Therefore 12.72 Gyr is not the age of any
CMB-consistent universe; it is an age of a universe with 18 % too much matter.

## Correction (integrator validated against Planck)

Age integral, radiation included, x = ln a:
t0 = (1/H0) ∫ dx / √(Ω_m e^{−3x} + Ω_r e^{−4x} + Ω_k e^{−2x} + Ω_DE f(x)).
Engine: `a002_age_omega_m_consistency_attack.py` (pure Python, no numpy).

| Branch | H0 | Ω_m held | implied ω_m | age t0 |
|---|---|---|---|---|
| Planck anchor (ω_m fixed) | 67.36 | 0.31516 | 0.1430 (input) | **13.797 Gyr** |
| Flawed (Ω_m fixed) — prior A002 | 73.04 | 0.31530 | 0.16821 (+17.6 %, 22.9 σ) | 12.723 Gyr |
| Self-consistent (ω_m fixed) | 73.04 | 0.26805 | 0.1430 (input) | **13.310 Gyr** |

The Planck anchor reproduces the published 13.797 ± 0.023 Gyr (Planck 2018 VI)
to three decimals, which validates the integrator. With ω_m fixed, the high-H0
age shift is **−0.487 Gyr**, not −1.074 Gyr: **my prior artifact overstated the
age tension by 0.587 Gyr, more than half its claimed magnitude.**

Age vs H0 at fixed ω_m = 0.1430 (the physically meaningful curve):

| H0 (km/s/Mpc) | 67.36 | 68 | 69 | 70 | 71 | 72 | 73.04 | 74 |
|---|---|---|---|---|---|---|---|---|
| Ω_m | 0.3152 | 0.3093 | 0.3004 | 0.2918 | 0.2837 | 0.2759 | 0.2681 | 0.2611 |
| t0 (Gyr) | 13.797 | 13.740 | 13.652 | 13.566 | 13.480 | 13.396 | 13.310 | 13.232 |

The curve is monotone and shallow: the entire 67.4→74 span of H0 moves the age
by only 0.57 Gyr. Standard one-parameter extensions at fixed ω_m move it less:
curvature Ω_k = ±0.002 → ∓0.008 Gyr; CPL dark energy w0 = −0.827, wa = −0.750
(DESI 2024) → −0.018 Gyr; w0 = −1, wa = −0.30 → +0.126 Gyr.

## The residual, deeper caveat (stated honestly)

Even the 13.310 Gyr branch is **not fully CMB-consistent**. In flat ΛCDM the
acoustic scale θ_* = r_s(z_*)/D_A(z_*) ties H0 to (ω_m, ω_b); fixing those fixes
H0 = 67.36. An H0 = 73.04 solution therefore requires new pre-recombination
physics (e.g. early dark energy) that changes r_s, and the resulting age depends
on that new physics. What survives the attack is a *bound*: within flat ΛCDM and
its standard one-parameter extensions, any H0 = 73 solution that preserves the
measured ω_m keeps t0 in ≈ 13.2–13.9 Gyr. The large "age tension" I previously
reported was largely an artifact of the fixed-Ω_m error.

## Established / Unknown / Falsifier

- **Established (recomputed, validated):** the CMB fixes ω_m, not Ω_m; the naive
  high-H0 age violates ω_m at 22.9 σ; with ω_m fixed, H0 = 73.04 gives
  t0 = 13.310 Gyr, so the age shift is −0.487 Gyr (correcting my own −1.074 Gyr).
- **Unknown (unchanged):** which H0 is correct; what new pre-recombination physics
  reconciles the acoustic scale with H0 = 73; the nature of dark matter.
- **What would change my mind:** a demonstration that the CMB likelihood fixes
  Ω_m rather than ω_m at fixed H0 (it does not); or a resolved H0 = 73 model with
  ω_m = 0.1430 whose age falls outside 13.2–13.9 Gyr.

## Citations (all real)

- Planck Collaboration 2020, A&A, 641, A6 (Planck 2018 VI) — ω_m = 0.1430 ± 0.0011,
  Ω_m = 0.3153 ± 0.0073, H0 = 67.36 ± 0.54, age = 13.797 ± 0.023 Gyr.
- Riess, A. G. et al. 2022, ApJ, 934, L7 — SH0ES H0 = 73.04 ± 1.04 km/s/Mpc.
- Fixsen, D. J. 2009, ApJ, 707, 916 — T_CMB = 2.72548 ± 0.00057 K.
- Cooke, R. J. et al. 2018, ApJ, 855, 102 — ω_b from primordial deuterium.
- DESI Collaboration 2024, AJ, 168, 58 (arXiv:2404.03002) — w0, wa.
- Pitrou, C., Coc, A., Uzan, J.-P., Vangioni, E. 2018, Phys. Rep., 754, 1 — BBN.
- Tiesinga, E. et al. 2021, Rev. Mod. Phys., 93, 025010 — CODATA 2018 constants.

## Protocol note

The consensus protocol requires restatement plus one ratifying sentence and nothing
else; the priority directive demands a substantively new, quantitative line. As in
prior A002 turns, the reply keeps the required form and this file carries the new
work, restricted to the statement's already-listed open problem. No consensus value
is altered; no experimental result is invented; no certainty is asserted beyond what
published measurements support.
