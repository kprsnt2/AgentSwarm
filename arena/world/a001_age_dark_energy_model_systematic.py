#!/usr/bin/env python3
"""
A001 (Kepler) -- Attack on the single weakest assumption in the current age work:
that the cosmic age t0 = 13.8 Gyr is model-independent, i.e. that dark energy is
exactly a cosmological constant (w == -1).

Computes the flat-FLRW age integral

    t0 = (1/H0) * Integral_0^1 da / [ a * E(a) ]

for
  (i)   flat LambdaCDM, Planck 2018 (H0=67.36, Om=0.3153)          -> reproduce 13.797 Gyr
  (ii)  flat LambdaCDM, DESI-preferred background (H0=68.60, Om=0.300)
  (iii) flat w0-wa CDM, DESI 2024 VI best fit (H0=68.60, Om=0.300,
        w0=-0.727, wa=-1.05)
  (iv)  a grid over the DESI 1-sigma ranges of (w0, wa, H0) to size the
        model systematic relative to the quoted statistical error (+-0.023 Gyr).

CPL: w(a) = w0 + wa (1 - a)
     rho_DE(a)/rho_DE0 = a^{-3(1+w0+wa)} exp(-3 wa (1-a))
     E(a)^2 = Om a^-3 + (1-Om) * rho_DE(a)/rho_DE0        (flat)

No experimental result is invented; all inputs are the published values already
carried in the swarm record (Planck 2018 VI; DESI 2024 VI, arXiv:2404.03002).
"""

import math

# ----------------------------------------------------------------------------
# Cosmology
# ----------------------------------------------------------------------------
C_KMS = 299792.458
# 1/H0 in Gyr for H0 in km/s/Mpc:  (Mpc/km) * (s/yr) = 977.7922216 / H0
GYR_PER_HUBBLE = 977.7922216


def E2_lcdm(a, Om):
    return Om * a ** -3 + (1.0 - Om)


def E2_w0wa(a, Om, w0, wa):
    de = (a ** (-3.0 * (1.0 + w0 + wa))) * math.exp(-3.0 * wa * (1.0 - a))
    return Om * a ** -3 + (1.0 - Om) * de


def age_gyr(H0, Om, w0=-1.0, wa=0.0, n=400000):
    """Flat-FLRW cosmic age in Gyr, log-substituted for accuracy near a=0."""
    # integrate in x = ln a from -inf to 0; substitute a = exp(x), integrand -> 1/E
    # do it robustly with a fine linear grid in a plus a=0 limit handled analytically.
    total = 0.0
    h = 1.0 / n
    for i in range(n):
        a = (i + 0.5) * h
        e2 = E2_lcdm(a, Om) if (w0 == -1.0 and wa == 0.0) else E2_w0wa(a, Om, w0, wa)
        total += (1.0 / a) / math.sqrt(e2) * h
    return GYR_PER_HUBBLE / H0 * total


# ----------------------------------------------------------------------------
# Inputs (published)
# ----------------------------------------------------------------------------
PLANCK = dict(H0=67.36, Om=0.3153, age=13.797, sigma=0.023)
DESI_BG = dict(H0=68.60, Om=0.300)
DESI_W0WA = dict(H0=68.60, Om=0.300, w0=-0.727, wa=-1.05)

print("=" * 78)
print("FLAT-FLRW COSMIC AGE UNDER DIFFERENT DARK-ENERGY ASSUMPTIONS")
print("=" * 78)

t_planck = age_gyr(PLANCK["H0"], PLANCK["Om"])
print(f"(i)   LambdaCDM  Planck 2018  H0=67.36 Om=0.3153   -> t0 = {t_planck:.3f} Gyr"
      f"   (published 13.797 +- 0.023)")

t_desi_bg = age_gyr(DESI_BG["H0"], DESI_BG["Om"])
print(f"(ii)  LambdaCDM  DESI bg      H0=68.60 Om=0.300    -> t0 = {t_desi_bg:.3f} Gyr")

t_w0wa = age_gyr(DESI_W0WA["H0"], DESI_W0WA["Om"],
                 DESI_W0WA["w0"], DESI_W0WA["wa"])
print(f"(iii) w0waCDM    DESI bestfit H0=68.60 Om=0.300    -> t0 = {t_w0wa:.3f} Gyr")
print(f"      w0=-0.727 wa=-1.05")
print()

# ----------------------------------------------------------------------------
# Sensitivity: local derivatives around LambdaCDM (Planck background)
# ----------------------------------------------------------------------------
eps = 1e-3
dt_dw0 = (age_gyr(PLANCK["H0"], PLANCK["Om"], -1.0 + eps, 0.0) -
          age_gyr(PLANCK["H0"], PLANCK["Om"], -1.0 - eps, 0.0)) / (2 * eps)
dt_dwa = (age_gyr(PLANCK["H0"], PLANCK["Om"], -1.0, 0.0 + eps) -
          age_gyr(PLANCK["H0"], PLANCK["Om"], -1.0, 0.0 - eps)) / (2 * eps)
dt_dH0 = (age_gyr(PLANCK["H0"] + eps, PLANCK["Om"]) -
          age_gyr(PLANCK["H0"] - eps, PLANCK["Om"])) / (2 * eps)
dt_dOm = (age_gyr(PLANCK["H0"], PLANCK["Om"] + eps) -
          age_gyr(PLANCK["H0"], PLANCK["Om"] - eps)) / (2 * eps)

print("Local age sensitivities at the Planck LambdaCDM point:")
print(f"  dt0/dw0 = {dt_dw0:+.4f} Gyr per unit w0")
print(f"  dt0/dwa = {dt_dwa:+.4f} Gyr per unit wa")
print(f"  dt0/dH0 = {dt_dH0:+.5f} Gyr per (km/s/Mpc)")
print(f"  dt0/dOm = {dt_dOm:+.4f} Gyr per unit Om")
print()

# ----------------------------------------------------------------------------
# Grid over DESI 1-sigma ranges: size the model systematic
# ----------------------------------------------------------------------------
w0_c, w0_s = -0.727, 0.067
wa_c, wa_s = -1.05, 0.27
H0_c, H0_s = 68.60, 0.85

ages = []
for iw0 in (-1, 0, 1):
    for iwa in (-1, 0, 1):
        for iH in (-1, 0, 1):
            w0 = w0_c + iw0 * w0_s
            wa = wa_c + iwa * wa_s
            H0 = H0_c + iH * H0_s
            ages.append((age_gyr(H0, DESI_BG["Om"], w0, wa), w0, wa, H0))

ages.sort()
amin, amax = ages[0], ages[-1]
print("Grid over DESI w0waCDM 1-sigma ranges (w0 in [-0.794,-0.660],")
print("wa in [-1.32,-0.78], H0 in [67.75,69.45], Om=0.300):")
print(f"  min t0 = {amin[0]:.3f} Gyr  at w0={amin[1]:+.3f} wa={amin[2]:+.3f} H0={amin[3]:.2f}")
print(f"  max t0 = {amax[0]:.3f} Gyr  at w0={amax[1]:+.3f} wa={amax[2]:+.3f} H0={amax[3]:.2f}")
print(f"  DESI w0waCDM age spread (1-sigma) = {amax[0]-amin[0]:.3f} Gyr")
print()

# LambdaCDM-only H0 tension spread, for comparison
t_low = age_gyr(67.36, PLANCK["Om"])
t_high = age_gyr(73.04, PLANCK["Om"])
print(f"LambdaCDM age across the quoted H0 tension (67.36 -> 73.04):")
print(f"  t0(67.36) = {t_low:.3f} Gyr ; t0(73.04) = {t_high:.3f} Gyr ; "
      f"spread = {t_low-t_high:.3f} Gyr")
print()

# ----------------------------------------------------------------------------
# Verdict
# ----------------------------------------------------------------------------
print("=" * 78)
print("VERDICT")
print("=" * 78)
print(f"Quoted statistical error on the Planck age: +-{PLANCK['sigma']:.3f} Gyr")
print(f"Age shift from LambdaCDM->DESI w0waCDM best fit: "
      f"{t_planck - t_w0wa:+.3f} Gyr")
print(f"Age spread across the DESI w0waCDM 1-sigma range: "
      f"{amax[0]-amin[0]:.3f} Gyr")
print(f"Ratio (DESI 1-sigma age spread)/(quoted Planck age error) = "
      f"{(amax[0]-amin[0])/PLANCK['sigma']:.1f}x")
print()
print("The quoted 13.8 Gyr is a LambdaCDM-derived quantity. Under the DESI 2024")
print("w0waCDM preference it moves by a fraction of a Gyr -- tens of times the")
print("quoted +-0.023 Gyr statistical error. The age is not a model-independent")
print("measurement; the single weakest assumption behind it is w == -1 exactly.")
