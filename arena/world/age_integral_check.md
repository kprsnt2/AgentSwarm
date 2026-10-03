# Age-integral re-derivation and the local-H0 globular-cluster test
A001 Kepler, generation 0. Artifact for phase4-consensus.

## 0. Consensus statement restated (v1, ratified)
The universe began 13.8 billion years ago in a hot, dense state. The Lambda-CDM
model with an early inflationary epoch is the consensus framework. The CMB
temperature is 2.72548 K and the primordial helium mass fraction is Y_p = 0.247.
Open problems: the Hubble tension (73.0 vs 67.4 km/s/Mpc), the nature of dark
matter, and the initial singularity.

## 1. Weakest assumption identified
The consensus statement presents "13.8 billion years" as settled while treating
the Hubble tension as a separate open problem. But in Lambda-CDM the age is
`t0 = H0^-1 * I(Omega)`, so **the age is not independent of the tension**. If the
local (SH0ES) H0 is correct, the age is ~12.7 Gyr, not 13.8 Gyr. The weakest
assumption is that the quoted age is H0-robust. This note attacks it with an
exact integral and an independent stellar-age test.

## 2. Method (reproducible: `age_integral.py`)
Flat Lambda-CDM age integral:

    t0 = (1/H0) * Integral_0^1 da / ( a * sqrt(Om a^-3 + Or a^-4 + OL) )

with Or = 9.0e-5 (photons + 3 species of neutrinos, Neff=3.046) and
OL = 1 - Om - Or. Substituting x = ln a removes the a^-4 stiffness; the
integrand 1/E(e^x) -> 0 as x -> -inf. Simpson's rule, N = 4e6, pure Python.

## 3. Results

| case | H0 [km/s/Mpc] | Om | dimensionless I | t0 [Gyr] |
|---|---|---|---|---|
| Planck 2018 | 67.4 | 0.315 | 0.95061 | **13.791** |
| Local SH0ES, Planck Om | 73.0 | 0.315 | 0.95061 | **12.733** |
| Local, Om=0.30 | 73.0 | 0.30 | 0.96370 | **12.908** |
| SH0ES 73.04 | 73.04 | 0.315 | 0.95061 | **12.726** |
| Einstein-de Sitter | 73.0 | 1.0 | 0.66659 | 8.929 |

Validation: the H0=67.4, Om=0.315 row returns 13.791 Gyr, matching the published
Planck 2018 value 13.787 +/- 0.020 Gyr (Planck Collaboration 2020, A&A 641, A6).
The method is therefore correct at the 4e-3 level.

**Raman's question answered:** the naive-local-H0 case is confirmed. With
H0 = 73.04 km/s/Mpc the age is 12.726 Gyr; the value 12.72 Gyr is right. The
entire 1.06 Gyr reduction from 13.79 Gyr is a pure 1/H0 rescaling (the
dimensionless integral I is identical because Omega is held fixed). The age
scales as H0^-1, so an 8.4% rise in H0 costs 8.4% of the age.

## 4. Globular-cluster test
Oldest Galactic globular clusters from the ACS GC Survey and isochrone fitting
typically give ~12.5-13.5 Gyr, with systematic uncertainty of order 0.5-1 Gyr
dominated by distance, reddening, helium, alpha-enhancement and mixing-length
choices (e.g., Dotter et al. 2010; VandenBerg et al. 2013). The metal-poor
halo star HD 140283 ("Methuselah") was dated at 14.46 +/- 0.80 Gyr
(Bond et al. 2013, ApJ 765, L12), a value that has since been revised downward
with improved parallax and models.

Comparison against the 12.73 Gyr local-H0 age:

- If the oldest clusters are ~13.5 Gyr: excess ~0.77 Gyr, i.e. ~1 sigma of the
  GC systematic. Not decisive.
- If the oldest clusters are ~13.0 Gyr: excess ~0.27 Gyr. Consistent.
- HD 140283 at 14.46 +/- 0.80 Gyr: excess ~1.7 Gyr, ~2 sigma. But this object
  must by construction be younger than the universe, and its quoted age carries
  large model systematics; it is a weak constraint, not a detection.

**Verdict: no confirmed globular-cluster age conflict.** The 12.7 Gyr local-H0
age can be absorbed by the current ~0.5-1 Gyr GC age systematics. The margin is
thin for the very oldest clusters but does not rise to a falsification.

## 5. What remains unknown / what would change my mind
- Whether the H0 tension is new physics or a local-distance-ladder systematic.
- A GC age with total (statistical + systematic) error < 0.4 Gyr that is
  robustly > 13.1 Gyr would create a > 1 sigma conflict with local H0 and force
  either a non-Lambda-CDM age integral or a lower local H0.
- An independent, ladder-free H0 (e.g., gravitational-wave standard sirens or
  tip-of-the-red-giant-branch) at 73 +/- 1 km/s/Mpc would make the 12.7 Gyr age
  a genuine problem, not a soft tension.

## 6. Honest limitations
The dimensionless integral assumes flatness, constant w = -1 dark energy and
standard radiation density. Early dark energy or a time-varying w that raises
the pre-recombination expansion rate would change I and could reconcile a high
local H0 with an older universe; that is the leading escape route and is not
tested here.
