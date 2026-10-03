"""
test_cosmogenesis_age_model_dependence_engine.py
Verification suite for the age model-dependence engine (Raman A002).
"""
import math
from cosmogenesis_age_model_dependence_engine import (
    LCDM, CPL, age_gyr, run, omega_m_for_h, hubble_time_gyr,
    PLANCK18, SH0ES22,
)


def test_baseline_matches_planck_age():
    t = age_gyr(LCDM(H0=PLANCK18["H0"], Omega_m=PLANCK18["Omega_m"]))
    # Planck 2018: 13.787 +/- 0.020 Gyr
    assert 13.75 < t < 13.83, t


def test_w_minus_one_reproduces_lcdm():
    a = age_gyr(LCDM(H0=67.36, Omega_m=0.3153))
    b = age_gyr(CPL(H0=67.36, Omega_m=0.3153, w0=-1.0, wa=0.0))
    assert abs(a - b) < 1e-6


def test_hubble_time_sanity():
    # 1/H0 for H0 = 100 km/s/Mpc is 9.778 Gyr
    assert abs(hubble_time_gyr(100.0) - 9.7779) < 1e-3


def test_omega_m_h2_conservation():
    # Planck omega_m h^2 = 0.1430
    om = omega_m_for_h(0.7304)
    assert abs(om * 0.7304 ** 2 - 0.1430) < 1e-9


def test_higher_h0_lowers_age():
    t_low = age_gyr(LCDM(H0=67.36, Omega_m=0.3153))
    t_high = age_gyr(LCDM(H0=73.04, Omega_m=0.3153))
    assert t_high < t_low
    assert abs((t_low - t_high) - 1.0728) < 0.01


def test_naive_local_age_below_globular_cluster_floor():
    # The naive combination falls near/below the ~13.5 Gyr oldest-star floor.
    t = age_gyr(LCDM(H0=SH0ES22["H0"], Omega_m=PLANCK18["Omega_m"]))
    assert t < 13.0


def test_desi_cpl_age_is_robust():
    r = run()
    assert abs(r["delta_cpl_vs_base_gyr"]) < 0.05


def test_sensitivities():
    r = run()
    assert r["dt_dH0_gyr_per_unit"] < 0
    assert r["dt_dOmega_m_gyr_per_unit"] < 0


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"{len(fns)}/{len(fns)} tests passing")
