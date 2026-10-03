#!/usr/bin/env python3
"""Unit tests for cosmogenesis_age_origin_decomposition_engine.py (A001)."""
import math
import cosmogenesis_age_origin_decomposition_engine as eng

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


def main():
    h = eng.PLANCK_H0 / 100.0
    Or = eng.omega_r(h, 3.046)

    # 1. Validation against Planck 2018 age, within 1 sigma.
    t0 = eng.age_from_z(0.0, eng.PLANCK_H0, eng.PLANCK_OM, Or)
    check("validation vs Planck 2018 age",
          abs(t0 - eng.PLANCK_AGE) < eng.PLANCK_AGE_SIGMA,
          f"t0={t0:.4f} Gyr, published {eng.PLANCK_AGE}+/-{eng.PLANCK_AGE_SIGMA}")

    # 2. t(z) is monotonically decreasing in z.
    zs = [0.0, 0.5, 1.0, 5.0, 100.0, 1100.0]
    ts = [eng.age_from_z(z, eng.PLANCK_H0, eng.PLANCK_OM, Or) for z in zs]
    check("t(z) monotonically decreasing",
          all(ts[i] > ts[i + 1] for i in range(len(ts) - 1)),
          f"{[round(x,3) for x in ts]}")

    # 3. Late universe dominates: > 40% of t0 accumulates after z=1.
    frac_late = eng.age_from_z(1.0, eng.PLANCK_H0, eng.PLANCK_OM, Or) / t0
    check("late-time dominance (>40% after z=1)", frac_late > 0.40,
          f"fraction after z=1 = {frac_late:.3f}")

    # 4. Radiation era (z>1100) contributes < 1% of t0.
    frac_rad = eng.age_from_z(1100.0, eng.PLANCK_H0, eng.PLANCK_OM, Or) / t0
    check("radiation era contributes <1%", frac_rad < 0.01,
          f"fraction after z=1100 = {frac_rad:.5f}")

    # 5. Inflation time is negligible vs t0 even for 1e10 e-folds.
    dt = eng.inflation_time_yr(0.036, 1.0e10)
    check("pre-reheating time << t0", dt < 1.0e-6,
          f"dt(1e10 e-folds, r=0.036) = {dt:.3e} yr")

    # 6. H_inf decreases with r.
    check("H_inf monotone in r",
          eng.H_inf_GeV(0.036) > eng.H_inf_GeV(0.01) > eng.H_inf_GeV(1e-3))

    # 7. Extra radiation makes the universe younger.
    t_neff4 = eng.age_from_z(0.0, eng.PLANCK_H0, eng.PLANCK_OM, eng.omega_r(h, 4.0))
    check("extra radiation lowers t0", t_neff4 < t0,
          f"t0(N_eff=4)={t_neff4:.4f} < t0(N_eff=3.046)={t0:.4f}")

    # 8. Radiation-content sensitivity is small (<0.1 Gyr over N_eff 2..4).
    t_neff2 = eng.age_from_z(0.0, eng.PLANCK_H0, eng.PLANCK_OM, eng.omega_r(h, 2.0))
    check("t0 robust to N_eff (<0.1 Gyr)", (t_neff2 - t_neff4) < 0.1,
          f"spread = {t_neff2 - t_neff4:.4f} Gyr")

    print(f"\n{PASS}/{PASS+FAIL} tests passed")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
