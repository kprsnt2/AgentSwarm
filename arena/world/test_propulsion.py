#!/usr/bin/env python3
"""
test_propulsion.py -- verification of propulsion_analyzer.py against
closed-form physics.  Hypatia A003, Generation 0.
"""
import math
try:
    import pytest
except ImportError:  # minimal stand-in so the file imports with bare Python
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

        def __repr__(self):
            return f"approx({self.expected}, rel={self.rel}, abs={self.abs})"

    class _Pytest:
        @staticmethod
        def approx(expected, rel=None, abs=None):
            return _Approx(expected, rel, abs)

        @staticmethod
        def main(*a, **k):
            return 0

    pytest = _Pytest()

from propulsion_analyzer import (
    G0, C, S0, exhaust_velocity, mass_ratio, log10_mass_ratio,
    jet_power, thrust_from_power, kinetic_energy_relativistic,
    photon_rocket_mass_ratio, required_isp, sail_accel,
    antimatter_budget, starshot_check,
    DRIVES, SAIL,
)


def test_exhaust_velocity_definition():
    # Isp 450 s -> ve = 4413.0 m/s
    assert exhaust_velocity(450) == pytest.approx(450 * 9.80665, rel=1e-12)


def test_rocket_equation_known_value():
    # dv = ve ln MR ; choose MR = e -> dv = ve
    ve = exhaust_velocity(450)
    mr = mass_ratio(ve, 450)
    assert mr == pytest.approx(math.e, rel=1e-12)


def test_rocket_equation_inverse():
    dv = 9.4e3
    isp = 452
    mr = mass_ratio(dv, isp)
    recovered = exhaust_velocity(isp) * math.log(mr)
    assert recovered == pytest.approx(dv, rel=1e-9)


def test_log10_mass_ratio_matches():
    dv, isp = 3.0e6, 900.0
    assert log10_mass_ratio(dv, isp) == pytest.approx(
        math.log10(mass_ratio(dv, isp)), rel=1e-9)


def test_chemical_isp_ceiling():
    # Chemical bond energy Q ~ 13 MJ/kg bounds ve <= sqrt(2Q) ~ 5.1 km/s
    ve_max = math.sqrt(2 * 13e6)
    assert ve_max / G0 == pytest.approx(520, abs=8)
    # established ground truth: practical ceiling 450 s is below this
    assert DRIVES["chemical_h2lox"].isp_s <= 465


def test_jet_power_identity():
    T, isp = 1.0, 4000.0
    assert jet_power(T, isp) == pytest.approx(0.5 * T * exhaust_velocity(isp))


def test_thrust_power_roundtrip():
    P, isp, eta = 1e6, 5000.0, 0.6
    T = thrust_from_power(P, isp, eta)
    assert jet_power(T, isp) == pytest.approx(eta * P, rel=1e-12)


def test_relativistic_energy_limit():
    # (gamma-1) mc^2 -> 0.5 m v^2 as v << c
    v = 1e3  # (v/c)^2 ~ 1e-11, so relativistic correction is < 1e-9
    assert kinetic_energy_relativistic(v, 2.0) == pytest.approx(
        0.5 * 2.0 * v * v, rel=1e-9)


def test_relativistic_energy_at_0p1c():
    ke = kinetic_energy_relativistic(0.1 * C, 1.0)
    gamma = 1 / math.sqrt(1 - 0.01)
    assert ke == pytest.approx((gamma - 1) * C * C, rel=1e-12)
    # ~4.5e14 J/kg
    assert ke == pytest.approx(4.52e14, rel=0.02)


def test_photon_rocket_small_dv():
    # exp(dv/c) ~ 1 + dv/c for small dv
    dv = 1e5
    assert photon_rocket_mass_ratio(dv) == pytest.approx(
        1 + dv / C, rel=1e-6)


def test_solar_sail_pressure():
    # 2 S0 / c = 9.08 uN/m^2
    fpa = 2 * S0 / C
    assert fpa == pytest.approx(9.08e-6, rel=1e-3)
    # acceleration for 10 g/m^2 ~ 0.908 mm/s^2
    assert sail_accel(0.010) == pytest.approx(9.08e-4, rel=1e-3)


def test_required_isp_closure():
    # MR=10, 0.1c -> ~1.33e6 s
    assert required_isp(0.1 * C, 10.0) == pytest.approx(1.3277e6, rel=1e-3)


def test_antimatter_energy_accounting():
    # 1000 kg to 0.1c at eta=1 needs total annihilated mass = KE/(2c^2)
    ab = antimatter_budget(0.1 * C, 1000.0, 1.0)
    ke = kinetic_energy_relativistic(0.1 * C, 1000.0)
    assert ab["total_annihilated_kg"] == pytest.approx(ke / (2 * C * C), rel=1e-12)
    assert ab["antimatter_kg"] == pytest.approx(ab["total_annihilated_kg"] / 2, rel=1e-12)


def test_starshot_force_and_accel():
    s = starshot_check()
    P = SAIL["starshot_laser_power"]
    assert s["force_N"] == pytest.approx(2 * P / C, rel=1e-12)
    # 667 N on 1 g = 6.8e5 m/s^2 ~ 6.9e4 g
    assert s["accel_g"] == pytest.approx(6.8e4, rel=0.02)


def test_conservation_energy_chemical():
    # A rocket cannot deliver more kinetic energy to payload+propellant than
    # the chemical energy released. Check order of magnitude for a 450 s stage.
    # ve^2/2 = 9.7 MJ/kg is the max specific jet energy for Isp 450.
    specific_jet_energy = 0.5 * exhaust_velocity(450) ** 2
    assert specific_jet_energy == pytest.approx(9.74e6, rel=0.01)


def _run_without_pytest():
    """Minimal fallback harness so the suite runs with bare Python."""
    import inspect
    import traceback
    tests = [(n, f) for n, f in sorted(globals().items())
             if n.startswith("test_") and callable(f)]
    passed = failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"PASS  {name}")
            passed += 1
        except Exception:
            print(f"FAIL  {name}")
            traceback.print_exc()
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    import sys
    try:
        import pytest  # noqa: F401
    except ImportError:
        print("pytest not installed -- using fallback harness\n")
        sys.exit(_run_without_pytest())
    sys.exit(pytest.main([__file__, "-v"]))
