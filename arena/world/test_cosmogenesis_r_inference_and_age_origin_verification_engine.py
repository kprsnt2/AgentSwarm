#!/usr/bin/env python3
"""Tests for cosmogenesis_r_inference_and_age_origin_verification_engine.py"""
import math
from cosmogenesis_r_inference_and_age_origin_verification_engine import (
    age_simpson, age_romberg, H_inf_GeV, V_quarter_GeV, inflation_time_yr,
    omega_r, H0, OM, R_UPPER_95,
)

PASS = 0
FAIL = 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  PASS  {name}  {detail}")
    else:
        FAIL += 1
        print(f"  FAIL  {name}  {detail}")


# 1. age integral reproduces Planck within 1 sigma
t0 = age_simpson(0.0)
check("t0 within 1 sigma of Planck 13.787+/-0.020", abs(t0 - 13.787) < 0.020,
      f"t0={t0:.4f}")

# 2. two independent quadratures agree to <0.01 Gyr
t0r = age_romberg(0.0)
check("Simpson vs Romberg agree <0.01 Gyr", abs(t0 - t0r) < 0.01,
      f"{t0:.5f} vs {t0r:.5f}")

# 3. fraction of t0 elapsed BY z=1 is ~42.4% (accumulated at z>1)
f1 = age_simpson(1.0) / t0
check("fraction elapsed by z=1 in [0.40,0.45]", 0.40 < f1 < 0.45, f"{f1:.3%}")

# 4. fraction of t0 SPENT at z<1 is ~57.6%
spent1 = 1.0 - age_simpson(1.0) / t0
check("fraction of t0 spent at z<1 in [0.55,0.60]", 0.55 < spent1 < 0.60, f"{spent1:.3%}")

# 5. fraction spent at z<2 is ~76.3%
spent2 = 1.0 - age_simpson(2.0) / t0
check("fraction of t0 spent at z<2 in [0.74,0.79]", 0.74 < spent2 < 0.79, f"{spent2:.3%}")

# 5b. radiation era contribution is negligible (age AT z=1100, not after it)
f1100 = age_simpson(1100.0) / t0
check("radiation-era fraction < 0.01%", f1100 < 1e-4, f"{f1100:.2e}")

# 6. H_inf(r=0.036) matches A001 to 1%
h = H_inf_GeV(0.036)
check("H_inf(0.036) = 4.70e13 GeV (1%)", abs(h - 4.70e13) / 4.70e13 < 0.01,
      f"{h:.3e}")

# 7. V^(1/4) cross-check: r=0.01 -> ~1.0e16 GeV
v = V_quarter_GeV(0.01)
check("V^1/4(0.01) = 1.0e16 GeV (5%)", abs(v - 1.0e16) / 1.0e16 < 0.05,
      f"{v:.3e}")

# 8. dt(60, r=0.036) matches A001 to 2%
dt = inflation_time_yr(0.036, 60)
check("dt(60,0.036) = 2.66e-44 yr (2%)", abs(dt - 2.66e-44) / 2.66e-44 < 0.02,
      f"{dt:.3e}")

# 9. dt(1e10, r=0.036) matches A001 to 2%
dt10 = inflation_time_yr(0.036, 1e10)
check("dt(1e10,0.036) = 4.44e-36 yr (2%)", abs(dt10 - 4.44e-36) / 4.44e-36 < 0.02,
      f"{dt10:.3e}")

# 10. lower r -> smaller H_inf -> longer duration (bound direction)
check("dt(60,r=0.001) > dt(60,r=0.036)",
      inflation_time_yr(0.001, 60) > inflation_time_yr(0.036, 60),
      f"{inflation_time_yr(0.001,60):.3e} > {inflation_time_yr(0.036,60):.3e}")

# 11. duration is unbounded in N: same r spans many orders of magnitude
span = math.log10(inflation_time_yr(0.036, 1e30) / inflation_time_yr(0.036, 50))
check("duration spans >25 decades across N", span > 25, f"{span:.1f} decades")

# 12. pre-reheating duration is utterly negligible vs t0 for any sane N
check("dt(1e10,0.036) / t0 < 1e-40",
      dt10 / (t0 * 1e9) < 1e-40, f"{dt10/(t0*1e9):.2e}")

print(f"\n{PASS} passed, {FAIL} failed")
raise SystemExit(1 if FAIL else 0)
