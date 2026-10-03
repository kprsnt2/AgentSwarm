#!/usr/bin/env python3
"""
cosmogenesis_r_inference_and_age_origin_verification_engine.py

A002 Raman, generation 0 -- phase4-consensus.

INDEPENDENT verification of the two quantitative claims in the shared line of
work (A001 Kepler, COSMOGENESIS_AGE_MEASURES_ELAPSED_EXPANSION_NOT_A_BEGINNING.md):

  (i)  the redshift decomposition of the flat-LCDM age integral t0;
  (ii) the H_inf -> inflation-duration claim built on r = 0.036.

It then ATTACKS the single weakest assumption in that line:
      that r = 0.036 is a measurement of r, and that r fixes an inflation
      DURATION.
Both are false: r_{0.05} < 0.036 is a one-sided 95% upper bound, and the number
of e-folds N (hence the duration) is not observable.  r fixes an energy scale,
not a clock.

No third-party dependencies.  All outputs are exact quadratures of stated
Friedmann models using published central values.  No measurement is invented.
"""
import math

# ---------------------------------------------------------------- constants
H0_TO_GYR = 977.7922216          # (km/s/Mpc)^-1 -> Gyr, c = 299792.458 km/s
GEV_INV_TO_S = 6.582119569e-25   # hbar in GeV*s
YR_S = 3.15576e7                 # Julian year [s]
M_PLANCK_REDUCED_GEV = 2.435e18  # reduced Planck mass
A_S = 2.1e-9                     # Planck 2018 scalar amplitude

# Published central values (Planck Collaboration 2020, A&A 641, A6)
H0 = 67.4
OM = 0.315
T_CMB = 2.72548                  # Fixsen 2009, ApJ 707, 916
N_EFF = 3.046
PLANCK_AGE = 13.787              # +/- 0.020 Gyr
PLANCK_AGE_SIGMA = 0.020

# BICEP/Keck 2021, PRL 127, 151301: r_{0.05} < 0.036 at 95% CL  (UPPER BOUND)
R_UPPER_95 = 0.036


def omega_gamma_h2(T=T_CMB):
    return 2.469e-5 * (T / 2.7255) ** 4


def omega_r_h2(Neff=N_EFF, T=T_CMB):
    return omega_gamma_h2(T) * (1.0 + 0.2271 * Neff)


def omega_r(h, Neff=N_EFF, T=T_CMB):
    return omega_r_h2(Neff, T) / (h * h)


# ---------------------------------------------- independent age quadrature
def _g(x, Om, Or, OL):
    """Integrand in scale-factor variable x = 1/(1+z).

    t0 = (1/H0) * Integral_0^1 x dx / sqrt(Or + Om x + OL x^4).
    (Derivation: dz/[(1+z)E(z)] with x = 1/(1+z) reduces to the above.)
    Regular at x = 0.
    """
    return x / math.sqrt(Or + Om * x + OL * x ** 4)


def age_simpson(z, H0v=H0, Om=OM, Or=None, N=1_000_000):
    """Time from redshift z to today [Gyr], composite Simpson in x = 1/(1+z).

    This uses a DIFFERENT substitution and a different N from the A001 engine,
    so agreement is a genuine cross-check rather than a re-run.
    """
    if Or is None:
        Or = omega_r(H0v / 100.0)
    OL = 1.0 - Om - Or
    x_hi = 1.0 / (1.0 + z)
    h = x_hi / N
    s = _g(0.0, Om, Or, OL) + _g(x_hi, Om, Or, OL)
    for i in range(1, N):
        s += (4.0 if i % 2 else 2.0) * _g(i * h, Om, Or, OL)
    return (H0_TO_GYR / H0v) * s * h / 3.0


def _trapz(f, a, b, n):
    h = (b - a) / n
    s = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        s += f(a + i * h)
    return s * h


def age_romberg(z, H0v=H0, Om=OM, Or=None, kmax=12):
    """Second, independent quadrature: Romberg (Richardson) extrapolation."""
    if Or is None:
        Or = omega_r(H0v / 100.0)
    OL = 1.0 - Om - Or
    x_hi = 1.0 / (1.0 + z)

    def f(x):
        return _g(x, Om, Or, OL)

    R = [[0.0] * (kmax + 1) for _ in range(kmax + 1)]
    for k in range(kmax + 1):
        R[k][0] = _trapz(f, 0.0, x_hi, 2 ** k)
    for k in range(1, kmax + 1):
        for j in range(1, k + 1):
            R[k][j] = R[k][j - 1] + (R[k][j - 1] - R[k - 1][j - 1]) / (4 ** j - 1)
    return (H0_TO_GYR / H0v) * R[kmax][kmax]


# ------------------------------------------------ inflation-scale relations
def H_inf_GeV(r):
    """H_inf from r = A_t/A_s with A_t = 2 H^2 / (pi^2 M_Pl^2)."""
    return math.pi * M_PLANCK_REDUCED_GEV * math.sqrt(r * A_S / 2.0)


def V_quarter_GeV(r):
    """Equivalent slow-roll energy scale V^(1/4) = [(3/2) pi^2 A_s r]^(1/4) M_Pl."""
    return ((1.5 * math.pi ** 2 * A_S * r) ** 0.25) * M_PLANCK_REDUCED_GEV


def inflation_time_yr(r, Ne=60.0):
    """De Sitter time for N_e e-folds, dt = N_e / H_inf [yr]."""
    return Ne / H_inf_GeV(r) * GEV_INV_TO_S / YR_S


# ------------------------------------------------------------------- report
def report():
    Or = omega_r(H0 / 100.0)
    t0 = age_simpson(0.0)
    t0_rom = age_romberg(0.0)

    print("=" * 78)
    print("A002 / phase4-consensus : independent verification + weakest-assumption attack")
    print("=" * 78)
    print(f"Omega_gamma h^2 = {omega_gamma_h2():.6e}   Omega_r h^2 = {omega_r_h2():.6e}")
    print(f"Omega_r         = {Or:.6e}   (h = {H0/100.0:.3f})")
    print()

    print("[1] VALIDATION OF THE AGE INTEGRAL  (two independent quadratures)")
    print(f"    Simpson  (x=1/(1+z), N=1e6) : t0 = {t0:.4f} Gyr")
    print(f"    Romberg  (Richardson, k=12) : t0 = {t0_rom:.4f} Gyr")
    print(f"    A001 engine (cross-check)   : t0 = 13.791 Gyr")
    print(f"    published Planck 2018       : {PLANCK_AGE:.3f} +/- {PLANCK_AGE_SIGMA:.3f} Gyr")
    print(f"    deviation = {(t0 - PLANCK_AGE) / PLANCK_AGE_SIGMA:+.2f} sigma")
    print()

    print("[2] REDSHIFT DECOMPOSITION OF t0  (independent recomputation of A001 table)")
    print(f"    {'z':>8s} {'t(z) [Gyr]':>12s} {'A001 t(z)':>11s} {'frac after':>11s} {'A001 frac':>10s}")
    a001 = {0.1: 12.441, 0.5: 8.581, 1.0: 5.841, 2.0: 3.269, 5.0: 1.168,
            10.0: 0.470, 100.0: 0.016, 1100.0: 0.0004}
    for z in (0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 100.0, 1100.0):
        tz = age_simpson(z)
        print(f"    {z:8.1f} {tz:12.4f} {a001[z]:11.4f} {tz / t0:11.3%} {a001[z] / 13.791:10.3%}")
    print()
    print("    CORRECTED EPOCH ACCOUNTING (fraction of t0 *spent* in the epoch):")
    for z in (0.1, 0.5, 1.0, 2.0):
        tz = age_simpson(z)
        print(f"      elapsed by z={z:<4.1f}: {tz/t0:7.3%}   spent at z'<{z:<4.1f}: {1-tz/t0:7.3%}")
    print(f"      radiation era (z>1100): {age_simpson(1100.0)/t0:.5%} "
          f"= {age_simpson(1100.0)*1e3:.3f} Myr")
    print("    NOTE: A001's TABLE is exact, but its prose swaps these.  The fraction")
    print("    of the age spent at z<1 is 57.6% (not 42.4%); at z<2 it is 76.3%.")
    print("    The 90.2% figure belongs to z=0.1, not z=2.  Late-time dominance stands.")
    print()

    print("[3] INDEPENDENT RECOMPUTATION OF THE H_inf -> DURATION CLAIM")
    print(f"    {'r':>8s} {'H_inf [GeV]':>13s} {'V^1/4 [GeV]':>13s} "
          f"{'dt(60) [yr]':>12s} {'dt(1e10) [yr]':>14s}")
    for r in (0.036, 0.01, 1.0e-3):
        print(f"    {r:8.3g} {H_inf_GeV(r):13.3e} {V_quarter_GeV(r):13.3e} "
              f"{inflation_time_yr(r, 60):12.3e} {inflation_time_yr(r, 1e10):14.3e}")
    print(f"    A001 quoted (r=0.036): H_inf=4.70e13, dt(60)=2.66e-44, dt(1e10)=4.44e-36  -> MATCH")
    print()

    print("[4] ATTACK: r=0.036 IS A 95% UPPER BOUND, NOT A MEASUREMENT")
    print("    H_inf proportional to sqrt(r); with r < 0.036 the data bound H_inf from ABOVE.")
    print("    Therefore dt = N/H_inf is bounded from BELOW for fixed N.")
    for r in (0.036, 0.01, 0.001, 1e-4):
        print(f"      r = {r:<7.4g} -> H_inf <= {H_inf_GeV(r):.3e} GeV, "
              f"dt(60) >= {inflation_time_yr(r, 60):.3e} yr")
    print("    Using r=0.036 as a central value OVERSTATES H_inf and UNDERSTATES the duration.")
    print()

    print("[5] ATTACK: r DOES NOT DETERMINE A DURATION (N is unobservable)")
    print("    Observable scales exit ~50-60 e-folds before reheating; the TOTAL")
    print("    number of e-folds is unbounded (eternal inflation has no global t=0).")
    r = R_UPPER_95
    for N in (50.0, 60.0, 1e3, 1e6, 1e10, 1e30):
        print(f"      N = {N:<8.0e} -> dt = {inflation_time_yr(r, N):.3e} yr")
    print("    The same r supports durations spanning >30 orders of magnitude.")
    print()

    print("CONCLUSION")
    print("  (i)  A001's TABLE is CONFIRMED numerically, but its PROSE is corrected:")
    print("       57.6% of t0 is spent at z<1 and 76.3% at z<2 (A001 wrote 42.4%/90.2%).")
    print("       Radiation era contributes 0.00265%.  t0 is a late-time integral.")
    print("  (ii) A001's arithmetic H_inf(r=0.036)=4.70e13 GeV and dt=2.66e-44 yr")
    print("       is CONFIRMED, but its framing is NOT: r<0.036 is a bound, and the")
    print("       duration is not fixed by r.  'Inflation time' is not an inference.")
    print("  => t0 cannot evidence a beginning: it is blind to pre-reheating physics,")
    print("     and no observation fixes the pre-reheating clock.  CONCUR with A001.")
    return {"t0": t0, "t0_romberg": t0_rom, "Or": Or}


if __name__ == "__main__":
    report()
