#!/usr/bin/env python3
"""
A001 (Kepler) -- Attack on the single weakest assumption behind the consensus
sentence "The universe began 13.8 billion years ago":

    ASSUMPTION: the FLRW age integral t0 = int_0^inf dz / ((1+z) H(z))
                measures the ORIGIN of the universe.

In the ratified Lambda-CDM + inflation framework the hot Big Bang is preceded
by inflation, so the integral's lower limit a -> 0 (extrapolated) is NOT the
end of inflation.  Reheating is what starts the hot, radiation-dominated phase
whose age the CMB actually calibrates.  This script quantifies three things:

  (1) the standard age integral (reproduces the published Planck 2018 value),
  (2) how little of t0 comes from z above recombination / the radiation era,
      i.e. how insensitive t0 is to reheating temperature T_rh,
  (3) the physical duration of the required inflationary epoch (~60 e-folds)
      using only published A_s, r bounds and the reduced Planck mass.

Every input is a published quantity.  Nothing is invented.
"""

import math

# ---- published constants -------------------------------------------------
c_km_s   = 299792.458
MPC_KM   = 3.0856775814913673e19          # km per Mpc
GYR_S    = 3.15576e16                      # s per Gyr (Julian yr)
GEV_INV_S = 1.519267447e24                 # 1 GeV = 1.519e24 s^-1
M_PL_GEV = 2.435e18                        # reduced Planck mass, GeV

T0_CMB = 2.72548                           # Fixsen 2009, K
H0     = 67.36                             # Planck 2018 VI, km/s/Mpc
OM     = 0.3153
OR     = 9.15e-5                           # photons + 3 neutrinos
OL     = 1.0 - OM - OR
A_S    = 2.1e-9                            # Planck 2018 scalar amplitude
Z_REC  = 1089.92                           # Planck 2018 recombination


def E(z):
    """Dimensionless expansion rate H(z)/H0 (flat, radiation included)."""
    return math.sqrt(OR * (1.0 + z) ** 4 + OM * (1.0 + z) ** 3 + OL)


def t_from_z(z_lo, z_hi, n=200000):
    """(1/H0) * int_{z_lo}^{z_hi} dz / ((1+z) E(z))  in Gyr.

    z = tan(u) substitution maps [0, inf) -> [0, pi/2); partial ranges are
    handled by mapping [z_lo, z_hi] onto [u_lo, u_hi] with the same rule.
    """
    u_lo = math.atan(z_lo)
    u_hi = math.atan(z_hi)
    if n % 2:
        n += 1
    h = (u_hi - u_lo) / n
    s = 0.0
    for i in range(n + 1):
        u = u_lo + i * h
        z = math.tan(u)
        f = (1.0 + z * z) / ((1.0 + z) * E(z))      # dz = (1+z^2) du
        w = 1.0 if i in (0, n) else (4.0 if i % 2 else 2.0)
        s += w * f
    integral = s * h / 3.0
    hubble_time_s = MPC_KM / H0                 # 1/H0 in seconds
    return integral * hubble_time_s / GYR_S


def t_from_loga(n=400000, a_min=1e-14):
    """Independent quadrature: t0 = (1/H0) int_{ln a_min}^{0} dx / E(e^x)."""
    x_lo = math.log(a_min)
    if n % 2:
        n += 1
    h = (0.0 - x_lo) / n
    s = 0.0
    for i in range(n + 1):
        x = x_lo + i * h
        a = math.exp(x)
        e = math.sqrt(OR * a ** -4 + OM * a ** -3 + OL)
        w = 1.0 if i in (0, n) else (4.0 if i % 2 else 2.0)
        s += w / e
    integral = s * h / 3.0
    return integral * (MPC_KM / H0) / GYR_S


def main():
    print("=" * 74)
    print("A001 / Kepler -- 'origin' vs 'reheating clock' attack")
    print("=" * 74)

    t0 = t_from_z(0.0, 1e12)
    t0b = t_from_loga()
    print(f"\n[1] Full FLRW age integral (z=0..1e12):  t0 = {t0:.4f} Gyr")
    print(f"    Independent log-a quadrature:        t0 = {t0b:.4f} Gyr")
    print(f"    Published Planck 2018 VI age        = 13.797 +/- 0.023 Gyr")

    print("\n[2] Where the age comes from (fraction of t0):")
    for zc, label in [(Z_REC, "recombination z_*"), (3400.0, "matter-rad. eq."),
                      (1e6, "z=1e6"), (1e9, "z=1e9")]:
        t_early = t_from_z(zc, 1e12)            # time from zc back to z=inf
        print(f"    z > {label:>20}: {t_early*1e3:8.4f} Myr  "
              f"= {100.0*t_early/t0:6.3f} % of t0")

    print("\n[3] Age measured from reheating (T_rh), t(z_rh -> 0):")
    for T_rh in (1e9, 1e12, 1e15):
        z_rh = T_rh / T0_CMB - 1.0
        t_since_rh = t0 - t_from_z(z_rh, 1e12)
        print(f"    T_rh = {T_rh:.0e} GeV  (z_rh={z_rh:.3e}): "
              f"t = {t_since_rh:.6f} Gyr  "
              f"(differs from t0 by {1e6*(t0-t_since_rh):.3f} yr)")

    print("\n[4] Inflation clock from published A_s and r (slow roll):")
    print("    V^(1/4) = (24 pi^2 eps A_s)^(1/4) M_Pl,  H_inf = M_Pl sqrt(8 pi^2 eps A_s)")
    for r in (0.036, 0.01, 0.001):
        eps = r / 16.0
        v14 = (24.0 * math.pi ** 2 * eps * A_S) ** 0.25 * M_PL_GEV
        H_inf = M_PL_GEV * math.sqrt(8.0 * math.pi ** 2 * eps * A_S)   # GeV
        H_s = H_inf * GEV_INV_S
        dt60_s = 60.0 / H_s
        dt60_gyr = dt60_s / GYR_S
        print(f"    r = {r:<6}: V^(1/4) = {v14:.3e} GeV, H_inf = {H_inf:.3e} GeV,"
              f"  60 e-folds = {dt60_gyr:.3e} Gyr ({dt60_s:.2e} s)")

    print("\n[5] Verdict on the assumption:")
    print("    - t0 is the extrapolated hot-Big-Bang clock, insensitive to T_rh")
    print("      (changes by < 1e-5 Gyr over T_rh = 1e9..1e15 GeV).")
    print("    - The required ~60 e-folds of inflation last ~1e-52 Gyr, i.e. the")
    print("      pre-reheating epoch is physically real but duration-negligible.")
    print("    - Therefore '13.8 Gyr' dates the ONSET OF THE HOT PHASE (reheating),")
    print("      not the origin. Whether an origin exists is the listed open problem.")
    print("=" * 74)


if __name__ == "__main__":
    main()
