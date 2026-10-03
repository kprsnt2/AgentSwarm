#!/usr/bin/env python3
"""
A001 (Kepler) -- Does "eternal inflation" force dropping the word "began"
entirely, or only the date?

Raman (A002) asked:
  "Confirm N_e/H_inf is negligible for finite inflation; does eternal inflation
   force dropping 'began' entirely rather than just the date?"

This script answers both parts with published-only inputs.

PART A -- FINITE INFLATION.  For a finite total number of e-folds N_e the
pre-reheating duration is dt = N_e / H_inf (H_inf ~ const during slow roll).
Using the slow-roll normalization A_s = H_inf^2 / (8 pi^2 eps M_Pl^2) and
eps = r/16, we tabulate dt and the N_e that would be needed for inflation alone
to last 13.8 Gyr.  If that crossover N_e is absurd, the correction is negligible.

PART B -- ETERNAL INFLATION.  Stochastic self-reproduction sets in where the
per-e-fold quantum scatter of the inflaton, H_inf/(2 pi), exceeds the classical
roll, sqrt(2 eps) M_Pl.  Squaring, that condition is exactly
   A_s(local) = V / (24 pi^2 eps M_Pl^4) > 1,
i.e. the local scalar amplitude exceeds unity.  The observed pivot value is
A_s = 2.1e-9, so the observable window is NOT eternally inflating; eternalness
is a model-dependent statement about unobservable field regions.  For quadratic
chaotic inflation we locate the eternal threshold and compute the finite
pre-reheating duration of the whole self-reproducing field range.

PART C -- BGV.  The Borde-Guth-Vilenkin theorem (PRL 90, 151301, 2003): any
spacetime whose averaged expansion is positive is past-geodesically-incomplete.
So even a future-eternal inflating region has a past boundary; "eternal" is a
statement about the future, not a licence for a past-eternal complete spacetime.

All inputs are published.  Nothing is invented.
"""

import math

# ---- published constants -------------------------------------------------
MPC_KM    = 3.0856775814913673e19      # km per Mpc
GYR_S     = 3.15576e16                  # s per Julian Gyr
GEV_INV_S = 1.519267447e24              # 1 GeV = 1.519e24 s^-1
GEV_INV_S_TO_S = 1.0 / GEV_INV_S        # s per GeV^-1 = 6.582e-25 s
M_PL_GEV  = 2.435e18                    # reduced Planck mass, GeV

H0  = 67.36                             # Planck 2018 VI, km/s/Mpc
OM  = 0.3153
OR  = 9.15e-5
OL  = 1.0 - OM - OR
A_S = 2.1e-9                            # Planck 2018 scalar amplitude at pivot
Z_REC = 1089.92


def E(z):
    return math.sqrt(OR * (1.0 + z) ** 4 + OM * (1.0 + z) ** 3 + OL)


def t0_gyr(n=400000):
    """Flat Lambda-CDM age, independent log-a Simpson quadrature (Gyr)."""
    x_lo = math.log(1e-14)
    h = (0.0 - x_lo) / n
    s = 0.0
    for i in range(n + 1):
        x = x_lo + i * h
        a = math.exp(x)
        e = math.sqrt(OR * a ** -4 + OM * a ** -3 + OL)
        w = 1.0 if i in (0, n) else (4.0 if i % 2 else 2.0)
        s += w / e
    return s * h / 3.0 * (MPC_KM / H0) / GYR_S


def h_inf_gev(r):
    """Slow-roll H_inf (GeV) from r and the measured A_s."""
    eps = r / 16.0
    return M_PL_GEV * math.sqrt(8.0 * math.pi ** 2 * eps * A_S)


def main():
    print("=" * 78)
    print("A001 / Kepler -- finite vs eternal inflation and the word 'began'")
    print("=" * 78)

    t0 = t0_gyr()
    t0_s = t0 * GYR_S
    print(f"\n[0] Lambda-CDM age anchor: t0 = {t0:.4f} Gyr "
          f"(Planck 2018 VI: 13.797 +/- 0.023 Gyr)")

    # ---------- PART A: finite inflation ----------
    print("\n[PART A] Finite inflation: dt = N_e / H_inf")
    print(f"{'r':>8} {'H_inf [GeV]':>14} {'H_inf [s^-1]':>14} "
          f"{'dt(60) [s]':>12} {'N_e for 13.8 Gyr':>18}")
    for r in (0.036, 0.010, 0.001, 1e-4):
        H = h_inf_gev(r)
        H_s = H * GEV_INV_S
        dt60 = 60.0 / H_s
        N_cross = t0_s * H_s
        print(f"{r:>8.4g} {H:>14.3e} {H_s:>14.3e} {dt60:>12.3e} "
              f"{N_cross:>18.3e}")
    print("    dt scales linearly in N_e.  Even N_e = 1e20 at r = 0.036 gives")
    H36 = h_inf_gev(0.036) * GEV_INV_S
    print(f"    dt = {1e20/H36:.3e} s = {1e20/H36/GYR_S:.3e} Gyr "
          f"(still < 1e-9 of 13.8 Gyr).")

    # ---------- PART B: eternal inflation ----------
    print("\n[PART B] Eternal self-reproduction threshold: A_s(local) > 1")
    print("    Quantum scatter per e-fold H/(2pi) > classical roll sqrt(2 eps) M_Pl")
    print("    <=>  A_s(local) = V/(24 pi^2 eps M_Pl^4) > 1.")
    print(f"    Observed pivot: A_s = {A_S:.2e}  ->  observable window is "
          f"{math.log10(1.0/A_S):.1f} dex below threshold.")

    # Quadratic chaotic inflation V = 1/2 m^2 phi^2, A_s = m^2 phi^4/(96 pi^2 M_Pl^6)
    phi_pivot = 15.0 * M_PL_GEV            # standard CMB pivot field value
    m2 = A_S * 96.0 * math.pi ** 2 * M_PL_GEV ** 6 / phi_pivot ** 4
    m = math.sqrt(m2)
    print(f"\n    Quadratic test model V = 1/2 m^2 phi^2:")
    print(f"      m = {m:.3e} GeV (fixed by A_s at phi = 15 M_Pl)")
    phi_et = (96.0 * math.pi ** 2 * M_PL_GEV ** 6 / m2) ** 0.25
    print(f"      eternal threshold phi_et = {phi_et/M_PL_GEV:.1f} M_Pl "
          f"(A_s(local)=1)")
    phi_end = math.sqrt(2.0) * M_PL_GEV    # eps = 1, slow-roll end
    N_total = (phi_et ** 2 - phi_end ** 2) / (4.0 * M_PL_GEV ** 2)
    # analytic duration for quadratic: t = sqrt(6) (phi_et - phi_end)/(2 m M_Pl)
    t_analytic_gev = math.sqrt(6.0) * (phi_et - phi_end) / (2.0 * m * M_PL_GEV)
    t_analytic_s = t_analytic_gev * GEV_INV_S_TO_S
    # independent numeric duration: sum dN/H over the field range
    Nn = 2000000
    dphi = (phi_et - phi_end) / Nn
    t_num_s = 0.0
    for i in range(Nn):
        phi = phi_end + (i + 0.5) * dphi
        H = m * phi / math.sqrt(6.0) / M_PL_GEV   # GeV
        dN = phi * dphi / (2.0 * M_PL_GEV ** 2)
        t_num_s += dN / (H * GEV_INV_S)
    print(f"      N_total (phi_et -> sqrt2 M_Pl) = {N_total:.3e} e-folds")
    print(f"      pre-reheating duration (analytic) = {t_analytic_s:.3e} s "
          f"= {t_analytic_s/GYR_S:.3e} Gyr")
    print(f"      pre-reheating duration (numeric)  = {t_num_s:.3e} s")
    print("    Even the whole self-reproducing field range is a finite,")
    print("    duration-negligible pre-reheating epoch.")

    # ---------- PART C: BGV ----------
    print("\n[PART C] Borde-Guth-Vilenkin (PRL 90, 151301, 2003):")
    print("    Any spacetime with positive averaged expansion H_avg > 0 along")
    print("    past-directed geodesics is past-incomplete.  A future-eternal")
    print("    inflating region therefore still has a PAST BOUNDARY; 'eternal'")
    print("    is not a claim of a past-eternal complete spacetime.")

    # ---------- verdict ----------
    print("\n[VERDICT]")
    print("    1. FINITE inflation: N_e/H_inf is negligible.  To shift the age by")
    print("       13.8 Gyr you would need N_e ~ 1e55 e-folds at H_inf ~ 1e13 GeV.")
    print("    2. ETERNAL inflation: reheating is not a single spacelike event,")
    print("       so 'began' cannot be a global single-moment claim.  But BGV keeps")
    print("       a past boundary.  The correct minimal fix is to relativize:")
    print("       'our hot phase began 13.8 Gyr ago', NOT to delete 'began'.")
    print("=" * 78)


if __name__ == "__main__":
    main()
