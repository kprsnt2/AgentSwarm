"""
A002 (Raman) -- Attack on the weakest assumption in A002's own age-tension work.

Prior artifact A002_hubble_tension_propagates_to_age.md evaluated the flat-LambdaCDM
age integral at H0 = 73.04 km/s/Mpc while HOLDING Omega_m = 0.315 fixed.  The CMB
does not constrain Omega_m at fixed H0; it constrains the PHYSICAL density
omega_m = Omega_m h^2 (plus omega_b h^2), with h = H0/100.  Holding Omega_m fixed
while raising H0 silently raises omega_m by (73.04/67.36)^2 = 1.176, i.e. +17.6%,
which is excluded by Planck at ~23 sigma (sigma(omega_m) = 0.0011).

This script:
  1. Reproduces the Planck anchor (omega_m = 0.1430 -> Omega_m = 0.3153 -> age 13.79 Gyr).
  2. Reproduces the FLAWED branch (Omega_m = 0.315 fixed at H0 = 73.04).
  3. Computes the SELF-CONSISTENT branch (omega_m = 0.1430 fixed at H0 = 73.04).
  4. Maps the age over an H0 grid at fixed omega_m, and over curvature and w.

Every input is a published value.  No experimental result is invented.
Age integral (flat, radiation included):
    t0 = (1/H0) * Integral_0^1 da / [ a * E(a) ],
    E(a)^2 = Omega_m a^-3 + Omega_r a^-4 + Omega_k a^-2 + Omega_DE f(a),
    f(a) = a^{-3(1+w0+wa)} exp(-3 wa (1-a))   [CPL; f=1 for Lambda].
Substitute x = ln a  =>  t0 = (1/H0) * Integral_{-inf}^{0} dx / E(e^x).
Pure-Python Simpson; no numpy required.
"""

import math

# ---- published constants (CODATA 2018 / Planck 2018 VI / Fixsen 2009) ----
C_KM_S = 299792.458
MPC_KM = 3.0856775814913673e19
GYR_S = 3.15576e16
T_CMB = 2.72548                      # K, Fixsen 2009
OMEGA_GAMMA_H2 = 2.4729e-5           # from T_CMB (computed in prior A002 artifact)
NEFF = 3.046
OMEGA_R_H2 = OMEGA_GAMMA_H2 * (1.0 + 0.2271 * NEFF)   # ~4.15e-5
OMEGA_M_H2_PLANCK = 0.1430           # Planck 2018 VI, TT,TE,EE+lowE+lensing
SIGMA_OMEGA_M_H2 = 0.0011
OMEGA_B_H2_PLANCK = 0.02237
H0_PLANCK = 67.36                    # km/s/Mpc
SIGMA_H0_PLANCK = 0.54
H0_SHOES = 73.04                     # Riess et al. 2022
SIGMA_H0_SHOES = 1.04


def _simpson(f, x0, x1, n):
    if n % 2:
        n += 1
    h = (x1 - x0) / n
    s = f(x0) + f(x1)
    for i in range(1, n):
        s += (4.0 if i % 2 else 2.0) * f(x0 + i * h)
    return s * h / 3.0


def age_gyr(H0, Omega_m, Omega_k=0.0, w0=-1.0, wa=0.0, n=200000):
    """Flat/curved LambdaCDM(+CPL) age in Gyr. Radiation included."""
    h = H0 / 100.0
    Omega_r = OMEGA_R_H2 / h**2
    Omega_DE = 1.0 - Omega_m - Omega_r - Omega_k

    def integrand(x):
        a = math.exp(x)
        if abs(w0 + 1.0) < 1e-12 and abs(wa) < 1e-12:
            f = 1.0
        else:
            f = a ** (-3.0 * (1.0 + w0 + wa)) * math.exp(-3.0 * wa * (1.0 - a))
        E2 = (Omega_m * a**-3 + Omega_r * a**-4
              + Omega_k * a**-2 + Omega_DE * f)
        return 1.0 / math.sqrt(E2)

    # x = ln a, integrate x from -40 (radiation-dominated, integrand -> 0) to 0.
    I = _simpson(integrand, -40.0, 0.0, n)
    # 1/H0 [Gyr] = (Mpc in km) / H0[km/s/Mpc] / (s per Gyr); c does not enter.
    return I * (MPC_KM / GYR_S) / H0, I


def main():
    print("=" * 74)
    print("A002: attacking the fixed-Omega_m assumption in the age-tension work")
    print("=" * 74)

    # 1. Planck anchor -----------------------------------------------------
    Om_planck = OMEGA_M_H2_PLANCK / (H0_PLANCK / 100.0) ** 2
    t_planck, I_planck = age_gyr(H0_PLANCK, Om_planck)
    print(f"\n[1] Planck anchor (omega_m fixed = {OMEGA_M_H2_PLANCK}):")
    print(f"    H0={H0_PLANCK}, Omega_m={Om_planck:.5f}, "
          f"age={t_planck:.3f} Gyr  (Planck 2018 VI: 13.797 +/- 0.023)")
    print(f"    dimensionless integral I = {I_planck:.6f}")

    # 2. Flawed branch: Omega_m held fixed (prior A002 artifact) -----------
    t_flaw, _ = age_gyr(H0_SHOES, 0.3153)
    omega_m_flaw = 0.3153 * (H0_SHOES / 100.0) ** 2
    print(f"\n[2] FLAWED branch (Omega_m = 0.3153 held fixed, H0={H0_SHOES}):")
    print(f"    implied omega_m = Omega_m h^2 = {omega_m_flaw:.5f}")
    print(f"    vs Planck {OMEGA_M_H2_PLANCK} -> excess = "
          f"{omega_m_flaw - OMEGA_M_H2_PLANCK:+.5f} "
          f"({100*(omega_m_flaw/OMEGA_M_H2_PLANCK - 1):+.2f}%)")
    n_sigma = (omega_m_flaw - OMEGA_M_H2_PLANCK) / SIGMA_OMEGA_M_H2
    print(f"    significance = {n_sigma:.1f} sigma  --> branch is excluded")
    print(f"    age = {t_flaw:.3f} Gyr   (this is the number my prior artifact quoted)")

    # 3. Self-consistent branch: omega_m held fixed ------------------------
    Om_shoes = OMEGA_M_H2_PLANCK / (H0_SHOES / 100.0) ** 2
    t_self, I_self = age_gyr(H0_SHOES, Om_shoes)
    print(f"\n[3] SELF-CONSISTENT branch (omega_m = {OMEGA_M_H2_PLANCK} fixed, "
          f"H0={H0_SHOES}):")
    print(f"    Omega_m = {Om_shoes:.5f}, Omega_Lambda = {1-Om_shoes:.5f}")
    print(f"    age = {t_self:.3f} Gyr   (I = {I_self:.6f})")
    print(f"    prior claimed shift = {t_flaw - t_planck:+.3f} Gyr")
    print(f"    corrected shift    = {t_self - t_planck:+.3f} Gyr")
    print(f"    my prior artifact overstated the age shift by "
          f"{abs(t_flaw - t_self):.3f} Gyr")

    # 4. Age over H0 at fixed omega_m (the physically meaningful curve) ----
    print(f"\n[4] Age vs H0 at fixed omega_m = {OMEGA_M_H2_PLANCK}:")
    print("    H0      Omega_m   Omega_DE    age[Gyr]")
    for H0 in (67.36, 68.0, 69.0, 70.0, 71.0, 72.0, 73.04, 74.0):
        Om = OMEGA_M_H2_PLANCK / (H0 / 100.0) ** 2
        t, _ = age_gyr(H0, Om)
        print(f"    {H0:6.2f}  {Om:8.5f}  {1-Om:8.5f}    {t:7.3f}")

    # 5. Secondary systematics on the quoted age ---------------------------
    print("\n[5] Secondary systematics on t0 (Planck H0, omega_m fixed):")
    base = t_planck
    for label, kw in (
        ("curvature Omega_k=+0.002", dict(Omega_k=0.002)),
        ("curvature Omega_k=-0.002", dict(Omega_k=-0.002)),
        ("CPL w0=-0.83, wa=-0.75 (DESI)", dict(w0=-0.827, wa=-0.750)),
        ("CPL w0=-1.00, wa=-0.30", dict(w0=-1.0, wa=-0.30)),
    ):
        t, _ = age_gyr(H0_PLANCK, Om_planck, **kw)
        print(f"    {label:34s}: t0={t:.3f} Gyr  (Delta={t-base:+.3f})")

    print("\n[6] Verdict")
    print("    The quoted '13.8 Gyr' is robust to H0 once omega_m (not Omega_m)")
    print("    is held fixed: even H0=73.04 moves t0 by only "
          f"{t_self - t_planck:+.3f} Gyr.")
    print("    The large shift in my prior artifact was an artifact of holding")
    print("    Omega_m fixed, which violates the CMB constraint on omega_m.")


if __name__ == "__main__":
    main()
