#!/usr/bin/env python3
"""A001 / Kepler -- independent re-derivation of the fixed-omega_m age at H0=73.04.

Purpose: audit A001_PRECISION_ASYMMETRY_AND_FALSIFICATION_THRESHOLDS.md Sec.5,
which used a fixed-Omega_m high-H0 branch (t0=12.722 Gyr). The CMB constrains the
*physical* density omega_m = Omega_m h^2, not Omega_m. This script recomputes the
age under both assumptions with two independent quadratures, and reports the
omega_m tension of the fixed-Omega_m branch.

Inputs (published, not invented):
  Planck 2018 VI: H0 = 67.36 +/- 0.54, Omega_m = 0.3153 +/- 0.0073,
                  omega_m = 0.1430 +/- 0.0011, age = 13.797 +/- 0.023 Gyr
  Riess et al. 2022 (SH0ES): H0 = 73.04 +/- 1.04
  Radiation: Omega_r h^2 ~ 4.15e-5 (photons) + neutrino contribution;
             use Omega_r = 9.0e-5 at h=0.674 as in age_integral.py.
No third-party dependencies.
"""
import math

H0_TO_GYR = 977.7922216  # (km/s/Mpc)^-1 -> Gyr

# ---- published anchors -------------------------------------------------
PLANCK_H0 = 67.36
PLANCK_OM = 0.3153
PLANCK_WM = 0.1430
PLANCK_WM_ERR = 0.0011
SHOES_H0 = 73.04
OR = 9.0e-5  # radiation density parameter at Planck h


def omega_m_of(H0, Om):
    return Om * (H0 / 100.0) ** 2


def om_of(H0, wm):
    h = H0 / 100.0
    return wm / h**2


# ---- quadrature A: z-integral, z = tan(u), Simpson in u -----------------
def age_zquad(H0, Om, Or=OR, n=200_000):
    """t0 = (1/H0) * int_0^inf dz / [(1+z) sqrt(Om(1+z)^3+Or(1+z)^4+OL)]."""
    OL = 1.0 - Om - Or

    def integrand(u):
        z = math.tan(u)
        one_z = 1.0 + z
        E = math.sqrt(Om * one_z**3 + Or * one_z**4 + OL)
        return (1.0 / math.cos(u) ** 2) / (one_z * E)

    a, b = 0.0, math.pi / 2.0
    h = (b - a) / n
    s = integrand(a + 1e-12) + integrand(b - 1e-12)
    for i in range(1, n):
        s += (4.0 if i % 2 else 2.0) * integrand(a + i * h)
    I = s * h / 3.0
    return (H0_TO_GYR / H0) * I, I


# ---- quadrature B: log-a integral, Simpson in x = ln a ------------------
def age_logquad(H0, Om, Or=OR, n=1_000_000):
    OL = 1.0 - Om - Or
    x0, x1 = -30.0, 0.0
    h = (x1 - x0) / n

    def f(x):
        a = math.exp(x)
        return 1.0 / math.sqrt(Om / a**3 + Or / a**4 + OL)

    s = f(x0) + f(x1)
    for i in range(1, n):
        s += (4.0 if i % 2 else 2.0) * f(x0 + i * h)
    I = s * h / 3.0
    return (H0_TO_GYR / H0) * I, I


# ---- closed form: matter + Lambda only (no radiation) -------------------
def age_closed_matter_lambda(H0, Om):
    OL = 1.0 - Om
    f = (2.0 / 3.0) * math.asinh(math.sqrt(OL / Om)) / math.sqrt(OL)
    return (H0_TO_GYR / H0) * f, f


def main():
    print("A001 independent fixed-omega_m age recheck")
    print("=" * 78)
    print(f"{'branch':38s} {'H0':>6s} {'Om':>7s} {'wm':>7s} {'t0[Gyr]':>9s}")
    print("-" * 78)

    # 1. Planck anchor, omega_m fixed (input)
    om_p = om_of(PLANCK_H0, PLANCK_WM)
    tA, IA = age_zquad(PLANCK_H0, om_p)
    tB, IB = age_logquad(PLANCK_H0, om_p)
    tC, _ = age_closed_matter_lambda(PLANCK_H0, om_p)
    print(f"{'Planck anchor (wm=0.1430 fixed)':38s} {PLANCK_H0:6.2f} "
          f"{om_p:7.4f} {PLANCK_WM:7.4f} {tA:9.3f}")
    print(f"    cross-checks: z-quad={tA:.4f}  log-a quad={tB:.4f}  "
          f"closed(no rad)={tC:.4f}")
    print(f"    published Planck age = 13.797 +/- 0.023 Gyr")

    # 2. Flawed branch: Omega_m fixed at Planck value, H0 = 73.04
    wm_flawed = omega_m_of(SHOES_H0, PLANCK_OM)
    t_flawed, _ = age_zquad(SHOES_H0, PLANCK_OM)
    tension = (wm_flawed - PLANCK_WM) / PLANCK_WM_ERR
    print(f"{'FLAWED: Om fixed at 0.3153':38s} {SHOES_H0:6.2f} "
          f"{PLANCK_OM:7.4f} {wm_flawed:7.4f} {t_flawed:9.3f}")
    print(f"    implied omega_m = {wm_flawed:.5f}  vs Planck {PLANCK_WM} "
          f"+/- {PLANCK_WM_ERR}")
    print(f"    omega_m violation = {tension:.1f} sigma")

    # 3. Self-consistent branch: omega_m fixed, H0 = 73.04
    om_shoes = om_of(SHOES_H0, PLANCK_WM)
    t_fix, _ = age_zquad(SHOES_H0, om_shoes)
    t_fix_B, _ = age_logquad(SHOES_H0, om_shoes)
    t_fix_C, _ = age_closed_matter_lambda(SHOES_H0, om_shoes)
    print(f"{'SELF-CONSISTENT: wm fixed':38s} {SHOES_H0:6.2f} "
          f"{om_shoes:7.4f} {PLANCK_WM:7.4f} {t_fix:9.3f}")
    print(f"    cross-checks: z-quad={t_fix:.4f}  log-a quad={t_fix_B:.4f}  "
          f"closed(no rad)={t_fix_C:.4f}")

    # 4. Corrected spread vs A001 Sec.5 claim
    spread_old = tA - t_flawed
    spread_new = tA - t_fix
    print("-" * 78)
    print(f"A001 Sec.5 (fixed Om) spread      = {spread_old:.3f} Gyr "
          f"({100*spread_old/tA:.2f}% of anchor)")
    print(f"CORRECTED (fixed wm) spread        = {spread_new:.3f} Gyr "
          f"({100*spread_new/tA:.2f}% of anchor)")
    print(f"Overstatement factor               = {spread_old/spread_new:.3f}x")
    print(f"Corrected spread in sigma_age units = "
          f"{spread_new/0.023:.1f} sigma (was {spread_old/0.023:.1f} sigma)")

    # 5. Sensitivity of the corrected spread to H0 error
    for dH0 in (-1.04, 0.0, 1.04):
        H = SHOES_H0 + dH0
        om = om_of(H, PLANCK_WM)
        t, _ = age_zquad(H, om)
        print(f"    H0 = {H:5.2f} (wm fixed) -> Omega_m={om:.4f}, "
              f"t0 = {t:.3f} Gyr")


if __name__ == "__main__":
    main()
