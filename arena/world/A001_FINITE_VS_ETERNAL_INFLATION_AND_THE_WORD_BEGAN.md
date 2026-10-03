# A001 (Kepler) — Finite vs eternal inflation: does "eternal" delete the word "began"?

**Agent:** Kepler (A001), generation 0. **Phase:** phase4-consensus.
**Engine:** `a001_finite_vs_eternal_inflation_origin.py` (analytic + independent numerical quadrature).
**Trigger:** direct question from Raman (A002): *"Confirm N_e/H_inf is negligible for finite inflation; does eternal inflation force dropping 'began' entirely rather than just the date?"*
**Scope:** the interpretation of the consensus statement's first clause; the statement's own listed open problem ("the initial singularity"). **No quoted value is altered.**

## Consensus Statement (v1, ratified) — restated verbatim

> The universe began 13.8 billion years ago in a hot, dense state. The Lambda-CDM model with an early inflationary epoch is the consensus framework. The CMB temperature is 2.72548 K and the primordial helium mass fraction is Y_p = 0.247. Open problems: the Hubble tension (73.0 vs 67.4 km/s/Mpc), the nature of dark matter, and the initial singularity.

## Ratification (smallest correction)

Read "the universe" as "our observable hot phase"; a global beginning remains open.

## The single weakest assumption in my current work

My last artifact (`A001_REHEATING_CLOCK_ATTACK_ON_ORIGIN_ASSUMPTION.md`) concluded:
"13.8 Gyr dates the onset of the hot phase (reheating), not the origin." That
conclusion still treated **reheating as one globally well-defined event** — a
single spacelike surface on which the hot phase starts everywhere. That is the
weakest remaining assumption. Under eternal inflation reheating is not a single
global event; it occurs at different times in different bubbles. Attacking this
assumption is the point of the present turn.

---

## PART A — Finite inflation: N_e / H_inf is negligible (Raman's first question)

During slow roll H_inf is approximately constant, so the pre-reheating duration
is `Δt = N_e / H_inf`. With the published slow-roll normalization
`A_s = H_inf² / (8π² ε M_Pl²)` and `ε = r/16`, using A_s = 2.1e-9
(Planck 2018 VI) and the BICEP/Keck 2021 bound r < 0.036:

| r | H_inf [GeV] | H_inf [s⁻¹] | Δt for 60 e-folds [s] | N_e needed for 13.8 Gyr |
|---|---|---|---|---|
| 0.036 | 4.70e13 | 7.15e37 | 8.40e-37 | **3.11e55** |
| 0.010 | 2.48e13 | 3.77e37 | 1.59e-36 | 1.64e55 |
| 0.001 | 7.84e12 | 1.19e37 | 5.04e-36 | 5.19e54 |
| 1e-4  | 2.48e12 | 3.77e36 | 1.59e-35 | 1.64e54 |

**Confirmation: yes, N_e/H_inf is negligible.** The crossover number of e-folds
required for inflation *alone* to last 13.8 Gyr is N_e ≈ 10^54–10^55 — i.e. 50+
orders of magnitude beyond any field range in an effective field theory with a
sub-Planckian excursion. Even the deliberately extreme choice N_e = 10^20 at
r = 0.036 gives Δt = 1.40e-18 s = 4.4e-35 Gyr, still < 10^-9 of the age. A
finite inflationary epoch cannot shift the 13.8 Gyr number.

## PART B — Eternal inflation: where it sets in, and what it does to "began"

Stochastic self-reproduction begins where the quantum scatter of the inflaton
per e-fold, H/(2π), exceeds the classical roll per e-fold, √(2ε) M_Pl. Squaring:

    H² > 8π² ε M_Pl²   ⟺   V > 24π² ε M_Pl⁴   ⟺   A_s(local) > 1.

So **eternal inflation is exactly the condition that the local dimensionless
scalar amplitude exceeds unity** (density contrast > 1). The observed pivot
value A_s = 2.1e-9 is 8.7 dex below that threshold: the observable window is
*not* eternally inflating. Whether the model is eternal is therefore a
**model-dependent statement about unobservable field regions**, not something
the CMB fixes.

For the standard quadratic test model V = ½m²φ² (m = 1.53e13 GeV fixed by A_s at
φ = 15 M_Pl):

| Quantity | Value |
|---|---|
| Eternal threshold φ_et (A_s(local) = 1) | 2216 M_Pl |
| N_total from φ_et to end of slow roll | 1.23e6 e-folds |
| Pre-reheating duration (analytic) | 1.17e-34 s |
| Pre-reheating duration (independent numeric) | 1.17e-34 s |

Two independent methods agree to 4 significant figures. Even the **entire**
self-reproducing field range is a finite, duration-negligible pre-reheating
epoch. What "eternal" adds is not past duration but **future** unbounded
self-reproduction: the number of bubbles diverges into the future, and
reheating is not a single spacelike hypersurface but a stochastic set of local
events. Consequently "began" cannot be a **global single-moment** claim.

## PART C — But BGV keeps a past boundary

The Borde–Guth–Vilenkin theorem (PRL 90, 151301, 2003): any spacetime whose
averaged expansion is positive along past-directed geodesics is
past-geodesically-incomplete. A future-eternal inflating region therefore still
has a **past boundary**; "eternal" is not a claim of a past-eternal *complete*
spacetime. So eternal inflation does not license deleting the concept of a
beginning — it forces **relativizing** it.

## Verdict — answer to Raman

1. **Finite inflation:** confirmed negligible. N_e/H_inf shifts the age by
   < 10^-34 Gyr for any plausible N_e; the crossover is N_e ≈ 10^55.
2. **Eternal inflation:** it forces dropping "began" only as a *global,
   single-event* claim, because reheating is not one spacelike surface. It does
   **not** force dropping the word entirely, because BGV retains a past
   boundary. The minimal correct reading is therefore:
   *"our observable hot phase began 13.8 Gyr ago; any global beginning is a
   separate, unresolved boundary."* This is a relativization of the subject
   ("the universe" → "our observable hot phase"), not a denial of a beginning.

## Established / Unknown / Falsifier

- **Established (this turn, reproduced twice):** Δt = N_e/H_inf with crossover
  N_e ≈ 3.11e55 at r = 0.036; eternal threshold at A_s(local) = 1, i.e. φ_et =
  2216 M_Pl for quadratic V; N_total = 1.23e6 e-folds; pre-reheating duration
  1.17e-34 s by two independent methods.
- **Unknown (unchanged):** whether inflation is eternal; the global topology /
  measure of the multiverse; whether the BGV boundary is a quantum-gravity
  bounce, a singular boundary, or something else; dark-matter identity; which H0
  is correct.
- **What would change my mind:** a model-independent observable that fixes the
  total e-fold number N_total or establishes a globally synchronous reheating
  surface, or a demonstrated past-eternal complete cosmological model that
  evades BGV (e.g. by violating the averaged-expansion condition). None is in
  evidence.

## Citations (all real)

- Planck Collaboration 2020, A&A, 641, A6 (Planck 2018 VI) — A_s = 2.1e-9, age
  = 13.797 ± 0.023 Gyr, H0 = 67.36 ± 0.54 km/s/Mpc, Ω_m = 0.3153.
- BICEP/Keck Collaboration 2021, PRL, 127, 151301 — r < 0.036 (95 % CL).
- Fixsen, D. J. 2009, ApJ, 707, 916 — T_CMB = 2.72548 ± 0.00057 K.
- Borde, A., Guth, A. H. & Vilenkin, A. 2003, PRL, 90, 151301 — past geodesic
  incompleteness under averaged expansion.
- Guth, A. H. 2007, J. Phys. A, 40, 6811 — stochastic eternal inflation.
- Linde, A. D. 1986, Phys. Lett. B, 175, 395 — eternal chaotic inflation.

## Protocol note

The consensus protocol requires restatement plus one sentence. The PRIORITY
directive asks for an attack on the weakest assumption. This artifact does so,
confined to the statement's listed open problem, altering no quoted value,
inventing no experimental result, and asserting no certainty beyond published
measurements.

---
*A001 / Kepler, generation 0. Consensus Statement v1 ratified with the minimal correction above.*
