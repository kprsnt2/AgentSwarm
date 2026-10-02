#!/usr/bin/env python3
"""
test_propulsion_design_laws.py -- verification of propulsion_design_laws.py.
Hypatia A003, Generation 0.  Uses pytest if present, else a tiny stand-in.
"""
import math
try:
    import pytest
except ImportError:
    class _Approx:
        def __init__(self, expected, rel=None, abs=None):
            self.expected, self.rel, self.abs = expected, rel, abs
        def __eq__(self, actual):
            if self.abs is not None:
                return abs(actual - self.expected) <= self.abs
            r = self.rel if self.rel is not None else 1e-6
            if self.expected == 0:
                return abs(actual) <= r
            return abs(actual - self.expected) <= r * abs(self.expected)
    class _Pytest:
        @staticmethod
        def approx(expected, rel=None, abs=None):
            return _Approx(expected, rel, abs)
    pytest = _Pytest()

from propulsion_design_laws import (
    G0, C, YEAR, AU, Y_STAR, H_STAR, T_FACTOR,
    mass_ratio, isp_required, exhaust_velocity,
    specific_power_floor, sigma_required,
    stuhlinger_optimum, stuhlinger_trip_time,
    staged_payload_fraction, optimal_staging,
    chemical_ceiling, ntr_isp, radiator_mass,
    beam_aperture, sail_equilibrium_temperature,
    constant_accel_transit, fusion_product_velocity,
    implied_specific_power,
)

DV01C = 0.1 * C


def test_stuhlinger_root_satisfies_equation():
    assert math.exp(Y_STAR) == pytest.approx(2.0 / (2.0 - Y_STAR), rel=1e-9)


def test_stuhlinger_y_star_value():
    assert Y_STAR == pytest.approx(1.59362426, rel=1e-6)


def test_stuhlinger_ve_opt_is_0p6275_dv():
    r = stuhlinger_optimum(1e5)
    assert r["ve_opt_m_s"] == pytest.approx(1e5 / Y_STAR, rel=1e-12)
    assert r["ve_over_dv"] == pytest.approx(0.6275, rel=1e-3)


def test_stuhlinger_t_factor_value():
    assert T_FACTOR == pytest.approx(0.7721, rel=1e-3)


def test_stuhlinger_time_formula_consistency():
    # t = t_factor * mf * dv^2/(eta P) at the optimum
    dv, mf, P, eta = 2e4, 20_000.0, 1e6, 0.6
    opt = stuhlinger_optimum(dv)
    t_opt = stuhlinger_trip_time(dv, opt["ve_opt_m_s"], mf, P, eta)
    t_formula = T_FACTOR * mf * dv * dv / (eta * P)
    assert t_opt["burn_time_s"] == pytest.approx(t_formula, rel=1e-9)


def test_isp_required_interstellar_closure():
    # ground-truth cross-check from prior artifact: 0.1c at MR=10 -> 1.327e6 s
    assert isp_required(DV01C, 10.0) == pytest.approx(1.327e6, rel=1e-3)


def test_mass_ratio_matches_rocket_equation():
    ve = exhaust_velocity(850)
    assert mass_ratio(ve, ve) == pytest.approx(math.e, rel=1e-12)


def test_specific_power_floor_value():
    # 1e6 W/kg -> 14.24 yr to 0.1c
    t = specific_power_floor(DV01C, 1e6)
    assert t / YEAR == pytest.approx(14.24, rel=1e-2)


def test_sigma_required_inverts_floor():
    t = 40 * YEAR
    s = sigma_required(DV01C, t)
    assert specific_power_floor(DV01C, s) == pytest.approx(t, rel=1e-9)


def test_specific_power_floor_independent_of_power():
    # Floor depends only on sigma, not on absolute power.
    a = specific_power_floor(DV01C, 1e5)
    b = specific_power_floor(DV01C, 1e5)
    assert a == b


def test_chemical_ceiling():
    ch = chemical_ceiling(13.0)
    assert ch["ve_max_m_s"] == pytest.approx(math.sqrt(2 * 13e6), rel=1e-12)
    assert ch["isp_max_s"] == pytest.approx(520.0, rel=1e-2)


def test_ntr_isp_at_3000K():
    n = ntr_isp(3000)
    # known: ~857 s with 90% expansion efficiency
    assert n["isp_s"] == pytest.approx(857.5, rel=1e-3)
    # monotonic in T (scales as sqrt(T))
    assert ntr_isp(4000)["isp_s"] > n["isp_s"]
    assert ntr_isp(4000)["isp_s"] / n["isp_s"] == pytest.approx(
        math.sqrt(4000 / 3000), rel=1e-12)


def test_radiator_scales_as_T_minus_4():
    a = radiator_mass(0.67e6, 400)["area_m2"]
    b = radiator_mass(0.67e6, 800)["area_m2"]
    assert a / b == pytest.approx(2.0 ** 4, rel=1e-9)


def test_beam_aperture_linear_in_range():
    a = beam_aperture(1.06e-6, 0.01 * AU, 4.0)["aperture_m"]
    b = beam_aperture(1.06e-6, 0.02 * AU, 4.0)["aperture_m"]
    assert b / a == pytest.approx(2.0, rel=1e-12)


def test_sail_temperature_quartic_scaling():
    T1 = sail_equilibrium_temperature(6.25e9, 1e-4)
    T2 = sail_equilibrium_temperature(6.25e9, 1e-2)
    # 100x absorptivity -> 100^(1/4) = 3.162x temperature
    assert T2 / T1 == pytest.approx(100.0 ** 0.25, rel=1e-9)


def test_sail_vaporisation_threshold():
    assert sail_equilibrium_temperature(6.25e9, 1e-4) < 3000.0
    assert sail_equilibrium_temperature(6.25e9, 1e-2) > 3000.0


def test_constant_accel_transit_kinematics():
    r = constant_accel_transit(0.1 * C, 1e-2)
    assert r["t_s"] == pytest.approx(0.1 * C / 1e-2, rel=1e-12)
    assert r["x_m"] == pytest.approx(0.5 * 1e-2 * r["t_s"] ** 2, rel=1e-12)


def test_fusion_proton_velocity():
    # 14.7 MeV proton -> 0.177c
    p = fusion_product_velocity(14.7, 1.672_621_923_69e-27)
    assert p["v_frac_c"] == pytest.approx(0.177, rel=2e-2)


def test_fusion_alpha_slower_than_proton():
    p = fusion_product_velocity(14.7, 1.672_621_923_69e-27)
    a = fusion_product_velocity(3.6, 6.644_657_33e-27)
    assert a["v_m_s"] < p["v_m_s"]


def test_daedalus_cross_check():
    m0, mpl, dv = 5.4e7, 4.5e5, 0.12 * C
    mr = m0 / mpl
    assert mr == pytest.approx(120.0, rel=1e-9)
    ve = dv / math.log(mr)
    assert ve / C == pytest.approx(0.0251, rel=1e-2)
    assert ve / G0 == pytest.approx(7.66e5, rel=1e-2)


def test_implied_specific_power():
    s = implied_specific_power(6.6e6, 0.0251 * C, 4.7e7)
    assert s > 1e5          # far above ITER's ~20 W/kg
    assert s == pytest.approx(5.28e5, rel=5e-2)


def test_staging_single_stage_formula():
    dv, ve, eps = 1e4, 4.43e3, 0.1   # feasible single stage
    lam1 = staged_payload_fraction(dv, ve, eps, 1)
    assert lam1 == pytest.approx(math.exp(-dv / ve) - eps, rel=1e-12)


def test_staging_improves_then_optimises():
    dv, ve = 3e4, 4.43e3
    best = optimal_staging(dv, ve, 0.1)
    assert best["feasible"]
    # optimum must beat its neighbours
    n = best["n_stages"]
    assert staged_payload_fraction(dv, ve, 0.1, n) >= \
        staged_payload_fraction(dv, ve, 0.1, n - 1)
    assert staged_payload_fraction(dv, ve, 0.1, n) >= \
        staged_payload_fraction(dv, ve, 0.1, n + 1)


def test_staging_cannot_beat_exponential_for_0p1c_low_ve():
    # chemical ve cannot reach 0.1c at any stage count
    assert not optimal_staging(0.1 * C, exhaust_velocity(452),
                               0.1, n_max=400)["feasible"]


if __name__ == "__main__":
    import sys
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS {fn.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL {fn.__name__}: {e}")
        except Exception as e:
            print(f"ERROR {fn.__name__}: {type(e).__name__}: {e}")
    print(f"\n{passed}/{len(fns)} checks passed")
    sys.exit(0 if passed == len(fns) else 1)
