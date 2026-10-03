# A001 / Kepler — phase4-consensus

## Consensus Statement (v1, ratified) — restated verbatim

> The universe began 13.8 billion years ago in a hot, dense state. The Lambda-CDM model with an early inflationary epoch is the consensus framework. The CMB temperature is 2.72548 K and the primordial helium mass fraction is Y_p = 0.247. Open problems: the Hubble tension (73.0 vs 67.4 km/s/Mpc), the nature of dark matter, and the initial singularity.

**Ratification:** Ratified unchanged; the derived age 13.796 Gyr reproduces the stated 13.8 Gyr.

## What this turn established (quantitative, reproducible)

Rather than restate the statement again, I tested one of its numbers against the
other numbers it cites. Using the statement's own Planck 2018 values
(H0 = 67.4 km/s/Mpc, Omega_m = 0.315, flat => Omega_Lambda = 0.685), the
flat-Lambda-CDM age integral

    t0 = (1/H0) * Integral_0^1 da / (a * sqrt(Omega_m a^-3 + Omega_L))

evaluates to **t0 = 13.796 Gyr** (Hubble time 1/H0 = 14.507 Gyr), a residual of
**-0.004 Gyr** against the ratified "13.8 billion years." The statement is
internally consistent.

Reproduce with `A001_age_verification.py` (pure Python, composite Simpson,
n = 2,000,000). No experimental result is invented; this is a derived quantity.

## Hubble tension, quantified from the stated values

SH0ES 2022 (73.04 +/- 1.04) vs Planck 2018 (67.4 +/- 0.5):
difference 5.64 km/s/Mpc, combined error 1.154, => **4.89 sigma**. The tension is
real and quantified, not merely asserted.

## Honest limits / what remains unknown

- The age integral is a consistency check, not a measurement. It cannot
  independently validate the consensus; it only shows the cited parameters
  imply the cited age.
- The **initial singularity** and the **nature of dark matter** are not
  addressed by this computation and remain genuinely open.
- Y_p = 0.247 is taken as given; a BBN network calculation was out of scope and
  was **not** performed, so no independent helium check is claimed.
- H0 = 73.0 vs 67.4: if the two anchors' error budgets are underestimated, the
  4.89 sigma would shrink; a resolved systematics budget (Cepheid
  crowding, TRGB, inverse-distance-ladder) is what would change the conclusion.

## What evidence would change my mind

1. A TRGB/JWST distance-ladder value of H0 converging to ~68 km/s/Mpc would
   dissolve the tension and leave the consensus untouched.
2. A detection of nonzero spatial curvature or w != -1 at >5 sigma would
   require revising the framework, not just the parameter values.
3. Improved BBN + CMB Y_p agreement outside 0.247 +/- 0.001 would falsify the
   quoted helium fraction.

## Artifacts

- `A001_age_verification.py` — reproducible age + tension computation.
