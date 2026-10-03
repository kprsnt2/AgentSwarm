#!/usr/bin/env python3
"""
A001 / Kepler -- phase4-consensus
Concrete quantitative check of the ratified consensus statement.

Claim under test: "The universe began 13.8 billion years ago..."
Method: integrate the flat Lambda-CDM age integral using the SAME parameter
values named in the consensus statement (Planck 2018: H0=67.4, Omega_m=0.315,
flat => Omega_L=0.685). No new experimental result is invented; this is a
derived quantity from established values.

t0 = (1/H0) * Integral_0^1 da / (a * sqrt(Omega_m a^-3 + Omega_r a^-4 + Omega_L))
"""
import math

MPC_KM = 3.0856775814913673e19  # km per Mpc
YR_S = 3.15576e7                # seconds per Julian year
GYR_S = 1.0e9 * YR_S

def hubble_time_gyr(H0_kmsMpc):
    H0_si = H0_kmsMpc / MPC_KM            # 1/s
    return (1.0 / H0_si) / GYR_S          # Gyr

def age_gyr(H0, Om, OL, Or=0.0, n=2_000_000):
    # composite Simpson on a in (0,1]; integrand is smooth after substituting
    # x = ln a to tame the a->0 behaviour, but a in [1e-8,1] trapezoid is fine here.
    a0, a1 = 1e-8, 1.0
    h = (a1 - a0) / n
    def f(a):
        return 1.0 / (a * math.sqrt(Om * a**-3 + Or * a**-4 + OL))
    s = f(a0) + f(a1)
    for i in range(1, n):
        a = a0 + i * h
        s += (4.0 if i % 2 else 2.0) * f(a)
    integral = s * h / 3.0
    return integral / (H0 / MPC_KM) / GYR_S

def main():
    print("=== Age of the universe from the consensus parameters ===")
    H0 = 67.4          # Planck 2018 TT,TE,EE+lowE+lensing (consensus value)
    Om = 0.315         # Planck 2018
    OL = 1.0 - Om      # flat
    Ht = hubble_time_gyr(H0)
    t0 = age_gyr(H0, Om, OL)
    print(f"H0                 = {H0} km/s/Mpc")
    print(f"Omega_m            = {Om}   (Omega_Lambda = {OL:.3f}, flat)")
    print(f"Hubble time 1/H0   = {Ht:.3f} Gyr")
    print(f"Age integral       = {t0:.3f} Gyr")
    print(f"Consensus claim    = 13.8 Gyr  -> residual {t0-13.8:+.3f} Gyr\n")

    print("=== Sensitivity: how much does H0 alone move the age? ===")
    for H0x in (67.4, 73.0):
        print(f"  H0={H0x:5.1f} -> t0={age_gyr(H0x, Om, 1-Om):.3f} Gyr")

    print("\n=== Hubble tension magnitude (consensus-stated values) ===")
    # SH0ES 2022: 73.04 +/- 1.04 ; Planck 2018: 67.4 +/- 0.5
    d = 73.04 - 67.4
    sig = math.sqrt(1.04**2 + 0.5**2)
    print(f"  difference = {d:.2f} km/s/Mpc")
    print(f"  combined 1-sigma = {sig:.3f}")
    print(f"  tension = {d/sig:.2f} sigma")

    print("\n=== Primordial helium (stated, not recomputed here) ===")
    print("  Y_p = 0.247 (Planck/BBN consensus). Requires BBN network; out of scope.")

if __name__ == "__main__":
    main()
