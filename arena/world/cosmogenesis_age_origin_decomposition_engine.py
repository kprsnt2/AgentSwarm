#!/usr/bin/env python3
"""
cosmogenesis_age_origin_decomposition_engine.py

A001 Kepler, generation 0 -- phase4-consensus.

Attacks the single weakest assumption of the A001 age-integral work:
that the quoted "13.8 Gyr" measures a *beginning* of the universe.

Three exact numerical results from published inputs only:

  1. Validation: reproduce the Planck 2018 flat-LCDM age (13.787 +/- 0.020 Gyr).
  2. Redshift decomposition of t0: how much of the elapsed 13.8 Gyr is laid down
     in each epoch. This shows t0 is an *elapsed expansion time*, dominated by
     late times, not a clock running from an origin.
  3. Time added by a pre-reheating inflationary epoch, Delta t = N_e / H_inf,
     with H_inf fixed by the tensor-to-scalar ratio r. Compare with the age.
  4. Sensitivity of t0 to the radiation content (N_eff), the remaining free
     input of the age integral.

No third-party dependencies.  All numbers are integrals of stated Friedmann
models; no measurement is invented.
"""
import math

H0_TO_GYR = 977.7922216            # (km/s/Mpc)^-1 -> Gyr (c = 299792.458 km/s)
GEV_INV_TO_S = 6.582119569e-25     # hbar in GeV*s
YR_S = 3.15576e7                   # Julian year in seconds
M_PLANCK_REDUCED_GEV = 2.435e18    # reduced Planck mass
A_S = 2.1e-9                       # Planck 2018 scalar amplitude

# Published central values (Planck Collaboration 2020, A&A 641, A6)
PLANCK_H0 = 67.4
PLANCK_OM = 0.315
PLANCK_AGE = 13.787                # +/- 0.020 Gyr
PLANCK_AGE_SIGMA = 0.020
FIXSEN_TCMB = 2.72548              # Fixsen 2009, ApJ 707, 916


def omega_gamma_h2(T=FIXSEN_TCMB):
    """Photons: Omega_gamma h^2 = 2.469e-5 (T/2.7255 K)^4."""
    return 2.469e-5 * (T / 2.7255) ** 4


def omega_r_h2(Neff=3.046, T=FIXSEN_TCMB):
    """Photons + massless neutrinos: factor (1 + 0.2271 N_eff)."""
    return omega_gamma_h2(T) * (1.0 + 0.2271 * Neff)


def omega_r(h, Neff=3.046, T=FIXSEN_TCMB):
    return omega_r_h2(Neff, T) / (h * h)


def _E(z, Om, Or, OL):
    return math.sqrt(Om * (1.0 + z) ** 3 + Or * (1.0 + z) ** 4 + OL)


def age_from_z(z, H0, Om, Or, N=400_000):
    """Time from redshift z to today [Gyr].

    t(z) = (1/H0) * Integral_z^inf dz' / [(1+z') E(z')].
    Substitution x = z'/(1+z') maps [z, inf) -> [z/(1+z), 1); the integrand
    1/[(1-x) E] -> 0 as x -> 1, so Simpson is stable.
    """
    OL = 1.0 - Om - Or
    x_lo = z / (1.0 + z)
    x_hi = 1.0

    def f(x):
        if x >= 1.0:
            return 0.0
        zp1 = 1.0 / (1.0 - x)
        return 1.0 / ((1.0 - x) * _E(zp1 - 1.0, Om, Or, OL))

    h = (x_hi - x_lo) / N
    s = f(x_lo) + f(x_hi)
    for i in range(1, N):
        s += (4.0 if i % 2 else 2.0) * f(x_lo + i * h)
    return (H0_TO_GYR / H0) * s * h / 3.0


def H_inf_GeV(r):
    """Inflationary Hubble rate from r = A_t/A_s, A_t = 2 H^2/(pi^2 M_Pl^2)."""
    return math.pi * M_PLANCK_REDUCED_GEV * math.sqrt(r * A_S / 2.0)


def inflation_time_yr(r, Ne=60.0):
    """Time added by N_e e-folds of de Sitter expansion [yr]."""
    return Ne / H_inf_GeV(r) * GEV_INV_TO_S / YR_S


def report():
    h = PLANCK_H0 / 100.0
    Or = omega_r(h, 3.046)
    t0 = age_from_z(0.0, PLANCK_H0, PLANCK_OM, Or)
    print("=" * 72)
    print("A001 / phase4-consensus : age-origin decomposition")
    print("=" * 72)
    print(f"Omega_gamma h^2 = {omega_gamma_h2():.4e}")
    print(f"Omega_r h^2     = {omega_r_h2(3.046):.4e}   (N_eff = 3.046)")
    print(f"Omega_r         = {Or:.4e}   (h = {h:.3f})")
    print()
    print("[1] VALIDATION")
    print(f"    t0(Planck H0=67.4, Om=0.315) = {t0:.3f} Gyr")
    print(f"    published Planck 2018        = {PLANCK_AGE:.3f} +/- {PLANCK_AGE_SIGMA:.3f} Gyr")
    print(f"    deviation = {(t0-PLANCK_AGE)/PLANCK_AGE_SIGMA:+.2f} sigma")
    print()
    print("[2] WHERE THE 13.8 Gyr COMES FROM  (fraction of t0 laid down at z < z_col)")
    print(f"    {'z_col':>8s} {'t(z_col) [Gyr]':>15s} {'fraction after':>15s} {'fraction before':>16s}")
    for z in (0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 100.0, 1100.0, 1.0e4, 1.0e6):
        tz = age_from_z(z, PLANCK_H0, PLANCK_OM, Or)
        print(f"    {z:8.1f} {tz:15.3f} {tz/t0:15.3%} {1.0-tz/t0:16.3%}")
    print()
    print("[3] PRE-REHEATING INFLATION ADDS (almost) NOTHING TO t0")
    for r in (0.036, 0.01, 1.0e-3):
        Hi = H_inf_GeV(r)
        dt60 = inflation_time_yr(r, 60.0)
        dt1e10 = inflation_time_yr(r, 1.0e10)
        print(f"    r={r:<7.3g} H_inf={Hi:.3e} GeV  60 e-folds = {dt60:.3e} yr  1e10 e-folds = {dt1e10:.3e} yr")
    print(f"    (t0 = {t0:.3e} Gyr = {t0*1e9:.3e} yr; a pre-Big-Bang phase is invisible in t0)")
    print()
    print("[4] RADIATION-CONTENT SENSITIVITY OF t0 (Om, h fixed)")
    print(f"    {'N_eff':>8s} {'Omega_r':>12s} {'t0 [Gyr]':>10s} {'dt0 [Gyr]':>11s}")
    base = None
    for Neff in (2.0, 3.046, 3.5, 4.0):
        orr = omega_r(h, Neff)
        tt = age_from_z(0.0, PLANCK_H0, PLANCK_OM, orr)
        if abs(Neff - 3.046) < 1e-9:
            base = tt
    for Neff in (2.0, 3.046, 3.5, 4.0):
        orr = omega_r(h, Neff)
        tt = age_from_z(0.0, PLANCK_H0, PLANCK_OM, orr)
        print(f"    {Neff:8.3f} {orr:12.4e} {tt:10.3f} {tt-base:+11.3f}")
    print()
    print("CONCLUSION: t0 is dominated by z < 2 and is insensitive (<0.1 Gyr) to")
    print("radiation content.  It measures elapsed expansion since reheating, not")
    print("an origin; the singularity/origin is not an output of this integral.")
    return t0


if __name__ == "__main__":
    report()
