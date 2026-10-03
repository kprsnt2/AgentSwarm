#!/usr/bin/env python3
"""Reproducible Lambda-CDM age integral.

t0 = (1/H0) * Integral_0^1 da / (a * sqrt(Om a^-3 + Or a^-4 + OL))
Log substitution x = ln a  =>  t0 = (1/H0) * Integral_-inf^0 dx / E(e^x)
Simpson, N = 4e6.  No third-party dependencies.
"""
import math

H0_to_Gyr = 977.7922216  # (km/s/Mpc)^-1 -> Gyr, c=299792.458


def age(H0, Om, Or=9.0e-5):
    """Return (t0 [Gyr], dimensionless age integral I)."""
    OL = 1.0 - Om - Or
    x0, x1, N = -30.0, 0.0, 4_000_000  # N even for Simpson

    def f(x):
        a = math.exp(x)
        E = math.sqrt(Om / a**3 + Or / a**4 + OL)
        return 1.0 / E

    h = (x1 - x0) / N
    s = f(x0) + f(x1)
    for i in range(1, N):
        s += (4.0 if i % 2 else 2.0) * f(x0 + i * h)
    integral = s * h / 3.0
    return (H0_to_Gyr / H0) * integral, integral


if __name__ == "__main__":
    rows = [
        ("Planck 2018 (67.4, Om=0.315)", 67.4, 0.315),
        ("Local H0=73.0, Planck Om=0.315", 73.0, 0.315),
        ("Local H0=73.0, Om=0.30", 73.0, 0.30),
        ("SH0ES 73.04, Om=0.315", 73.04, 0.315),
        ("EdS (H0=73, Om=1)", 73.0, 1.0),
    ]
    print(f"{'case':34s} {'t0 [Gyr]':>9s}   I")
    for name, H0, Om in rows:
        t, I = age(H0, Om)
        print(f"{name:34s} {t:9.3f}   {I:.5f}")
    print(f"\n1/H0 @ 73.0 = {H0_to_Gyr/73.0:.4f} Gyr")
    print(f"1/H0 @ 67.4 = {H0_to_Gyr/67.4:.4f} Gyr")
