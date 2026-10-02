"""
test_lightspeed_engine.py - Test suite for Phase 2 Relativistic Flight & FTL Causality Engine
Verifies engine contract, physical laws, thermodynamic radiator limits, ISM flux, and FTL causality.
"""

import sys
import os
import unittest
import math

# Ensure module path is accessible when run directly or via test runner
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lightspeed_engine import (
    C,
    M_P,
    SIGMA_SB,
    ISM_DENSITY_STANDARD,
    lorentz_gamma,
    relativistic_kinetic_energy,
    relativistic_momentum,
    time_dilation,
    rocket_mass_ratio,
    ism_interaction_flux,
    thermal_radiator_mass_ratio,
    tachyonic_antitelephone_boost,
    analyze,
)


class TestLightspeedEngine(unittest.TestCase):
    """Rigorous verification of the relativistic flight and causality engine."""

    def test_analyze_contract_schema(self):
        """Property 1: Verify analyze() contract matches the phase 2 specification."""
        res = analyze()
        self.assertIsInstance(res, dict)
        required_keys = {"domain", "claims", "confidence", "evidence"}
        self.assertTrue(required_keys.issubset(res.keys()))

        self.assertEqual(res["domain"], "lightspeed")
        self.assertIsInstance(res["confidence"], (int, float))
        self.assertTrue(0.0 <= res["confidence"] <= 1.0)

        self.assertIsInstance(res["claims"], list)
        self.assertGreaterEqual(len(res["claims"]), 4)
        for claim in res["claims"]:
            self.assertIsInstance(claim, str)
            self.assertGreater(len(claim), 20)

        self.assertIsInstance(res["evidence"], list)
        self.assertGreaterEqual(len(res["evidence"]), 4)
        for ev in res["evidence"]:
            self.assertIsInstance(ev, dict)
            self.assertIn("kind", ev)
            self.assertIn("value", ev)
            self.assertIn("source", ev)

    def test_special_relativity_lorentz_gamma(self):
        """Property 2: Verify Lorentz factor gamma behavior and divergence as beta -> 1."""
        self.assertAlmostEqual(lorentz_gamma(0.0), 1.0)
        self.assertAlmostEqual(lorentz_gamma(0.6), 1.25, places=5)
        self.assertAlmostEqual(lorentz_gamma(0.8), 5.0 / 3.0, places=5)

        gamma_099 = lorentz_gamma(0.99)
        self.assertAlmostEqual(gamma_099, 7.088812, places=4)

        # Divergence check
        gamma_0999 = lorentz_gamma(0.999)
        self.assertGreater(gamma_0999, 22.0)

        # Boundary assertions
        with self.assertRaises(ValueError):
            lorentz_gamma(1.0)
        with self.assertRaises(ValueError):
            lorentz_gamma(1.05)
        with self.assertRaises(ValueError):
            lorentz_gamma(-0.1)

    def test_relativistic_kinetic_energy_ground_truth(self):
        """Property 3: Verify kinetic energy for 1 kg at 0.99c matches ~5.5e17 J ground truth."""
        ke_1kg_099 = relativistic_kinetic_energy(1.0, 0.99)
        # Ground truth: ~5.474e17 J (~5.5e17 J)
        self.assertGreater(ke_1kg_099, 5.4e17)
        self.assertLess(ke_1kg_099, 5.6e17)
        self.assertAlmostEqual(ke_1kg_099 / 1e17, 5.4725, delta=0.05)

        # Low velocity correspondence with Newtonian KE: 1/2 m v^2
        v_low = 1000.0  # 1 km/s
        beta_low = v_low / C
        ke_rel_low = relativistic_kinetic_energy(1.0, beta_low)
        ke_class_low = 0.5 * 1.0 * (v_low ** 2)
        self.assertAlmostEqual(ke_rel_low, ke_class_low, delta=ke_class_low * 1e-4)

    def test_relativistic_rocket_equation_mass_ratios(self):
        """Property 4: Verify relativistic rocket mass ratios confirm impossibility of 0.9c onboard fusion."""
        # Fusion exhaust velocity u_ex = 0.05 c
        u_fusion = 0.05
        # Reaching beta = 0.1c: ((1.1/0.9))^10 = 7.43878
        r_01c = rocket_mass_ratio(0.1, u_fusion)
        self.assertAlmostEqual(r_01c, 7.439, places=2)

        # Reaching beta = 0.9c (one-way acceleration)
        r_09c = rocket_mass_ratio(0.9, u_fusion)
        self.assertGreater(r_09c, 6.0e12)
        self.assertLess(r_09c, 6.2e12)

        # Round trip / stop (deceleration) squares the mass ratio: R_total = R^2
        r_09c_stop = r_09c ** 2
        self.assertGreater(r_09c_stop, 3.7e25)
        # 3.76e25 kg fuel per kg payload exceeds Earth's mass (~5.97e24 kg)!

    def test_interstellar_medium_lethal_flux(self):
        """Property 5: Verify ISM proton flux and power at relativistic velocity beta = 0.9c."""
        flux_09c = ism_interaction_flux(0.9)
        # Proton kinetic energy at 0.9c (gamma = 2.294) is (gamma - 1) * 938 MeV ~ 1.21 GeV
        self.assertAlmostEqual(flux_09c["proton_kinetic_energy_gev"], 1.214, places=2)

        # Power flux is ~52.5 kW / m^2
        self.assertAlmostEqual(flux_09c["power_flux_kw_per_m2"], 52.54, delta=0.5)

        # Particle flux at 0.9c is 10^6 * 0.9 * 3e8 = 2.7e14 protons / (m^2 s)
        self.assertAlmostEqual(flux_09c["particle_flux_per_m2_s"] / 1e14, 2.698, places=2)

        # At beta = 0.99c, power flux reaches ~271.7 kW / m^2
        flux_099c = ism_interaction_flux(0.99)
        self.assertGreater(flux_099c["power_flux_kw_per_m2"], 250.0)
        self.assertAlmostEqual(flux_099c["power_flux_kw_per_m2"], 271.66, delta=1.0)

    def test_thermal_radiator_acceleration_limits(self):
        """Property 6: Verify thermal radiator mass bounds clamp onboard rocket acceleration."""
        rad = thermal_radiator_mass_ratio(thrust_n=1.0, temp_k=1800.0)
        # Waste power is ~41.64 MW per Newton
        self.assertAlmostEqual(rad["waste_power_mw_per_n"], 41.638, places=2)

        # Radiator mass per Newton is ~194.3 kg/N
        self.assertAlmostEqual(rad["radiator_mass_kg_per_n"], 194.3, delta=0.5)

        # Acceleration bound is clamped to ~ 0.00052 g (5.15e-3 m/s^2)
        self.assertLess(rad["max_acceleration_g"], 0.0006)
        self.assertGreater(rad["max_acceleration_g"], 0.0004)

    def test_ftl_tachyonic_antitelephone_causality_obstruction(self):
        """Property 7: Verify FTL signaling creates closed timelike curves (t'_B < 0) under Lorentz boost."""
        # Signal traveling at 2c in frame S over distance 1e9 m
        # Boost velocity = 0.6c -> v_boost * v_ftl / c^2 = 1.2 > 1.0
        boost_res = tachyonic_antitelephone_boost(v_ftl=2.0 * C, v_boost=0.6 * C, distance_m=1.0e9)

        self.assertTrue(boost_res["causality_violation"])
        self.assertTrue(boost_res["t_prime_negative"])
        self.assertLess(boost_res["t_prime_b_boosted_frame_s"], 0.0)

        # Sub-light velocity cannot violate causality
        with self.assertRaises(ValueError):
            tachyonic_antitelephone_boost(v_ftl=0.9 * C, v_boost=0.6 * C, distance_m=1.0e9)

    def test_time_dilation_and_momentum_consistency(self):
        """Property 8: Verify relativistic time dilation and momentum equations."""
        tau = 3600.0  # 1 hour proper time
        t_dilated = time_dilation(tau, 0.8)  # gamma = 5/3
        self.assertAlmostEqual(t_dilated, 6000.0, places=2)

        # Relativistic momentum p = gamma * m * v
        mass = 10.0
        beta = 0.6
        p = relativistic_momentum(mass, beta)
        gamma = lorentz_gamma(beta)
        expected_p = gamma * mass * (beta * C)
        self.assertAlmostEqual(p, expected_p, places=4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
