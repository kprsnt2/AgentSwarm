"""
test_propulsion_thermodynamic_and_terminal_capture_engine.py
============================================================
Comprehensive test suite for:
1. Froude kinetic propulsive efficiency bounds and optimal mass ratio peak.
2. Thermodynamic Stefan-Boltzmann waste heat and radiator mass wall.
3. Antimatter neutral pion gamma ray heating and shielding penalty.
4. Macro-pellet stream vs laser light sail thrust-to-power and divergence.
5. Exoplanet terminal capture delta-v, chemical impossibility, and aerocapture heating.
6. Ranked propulsion feasibility matrix integrity.

Author: Kepler (Agent A001, Generation 0)
Domain: Practical Space Propulsion
"""

import unittest
import math
from propulsion_thermodynamic_and_terminal_capture_engine import (
    C, G0, AU, LY, YEAR, M_PROXIMA, A_PROXIMA_B,
    froude_instantaneous_efficiency,
    froude_mission_averaged_efficiency,
    optimal_froude_mass_ratio,
    thermodynamic_radiator_limit,
    antimatter_gamma_shielding_analysis,
    macro_pellet_vs_laser_beam_comparison,
    exoplanet_terminal_capture_analysis,
    complete_propulsion_feasibility_matrix
)


class TestPropulsionThermodynamicsAndTerminalCapture(unittest.TestCase):

    def test_froude_instantaneous_efficiency(self):
        # When v == v_e, eta_p must be exactly 1.0 (100%)
        eta_1 = froude_instantaneous_efficiency(10000.0, 10000.0)
        self.assertAlmostEqual(eta_1, 1.0, places=6)

        # When v = 0.5 * v_e: eta_p = 2*(0.5) / (1 + 0.25) = 1.0 / 1.25 = 0.80
        eta_half = froude_instantaneous_efficiency(5000.0, 10000.0)
        self.assertAlmostEqual(eta_half, 0.80, places=6)

        # When v = 2.0 * v_e: eta_p = 2*(2.0) / (1 + 4.0) = 4.0 / 5.0 = 0.80
        eta_double = froude_instantaneous_efficiency(20000.0, 10000.0)
        self.assertAlmostEqual(eta_double, 0.80, places=6)

        # Negative or zero exhaust velocity should raise ValueError
        with self.assertRaises(ValueError):
            froude_instantaneous_efficiency(100.0, 0.0)

    def test_optimal_froude_mass_ratio(self):
        res = optimal_froude_mass_ratio()
        r_opt = res["optimal_mass_ratio"]
        u_opt = res["optimal_velocity_ratio"]
        eta_max = res["max_kinetic_efficiency"]

        # R_opt satisfies ln(R) = 2*(1 - 1/R)
        self.assertAlmostEqual(math.log(r_opt), 2.0 * (1.0 - 1.0 / r_opt), places=5)
        self.assertAlmostEqual(r_opt, 4.9215536, delta=0.001)
        self.assertAlmostEqual(u_opt, 1.59362, delta=0.001)
        self.assertAlmostEqual(eta_max, 0.64761, delta=0.001)

    def test_froude_mission_averaged_scaling(self):
        # Chemical rocket attempting 0.1c (v_f = 30,000 km/s, v_e = 4.43 km/s)
        # R = exp(30000 / 4.43) = exp(6772) -> eta_mission -> 0.0
        # Check that high mass ratios plummet in efficiency
        eta_r10 = froude_mission_averaged_efficiency(10.0)
        self.assertAlmostEqual(eta_r10, (math.log(10.0)**2) / 9.0, places=5)
        self.assertLess(eta_r10, 0.60)

        # R = 1.0 gives 0.0
        self.assertEqual(froude_mission_averaged_efficiency(1.0), 0.0)

    def test_thermodynamic_radiator_limit(self):
        # Test 1000 N thrust at v_e = 20,000 km/s (2.0e7 m/s)
        # P_jet = 0.5 * 1000 * 2.0e7 = 10 GW
        thrust = 1000.0
        v_e = 2.0e7
        rad = thermodynamic_radiator_limit(thrust, v_e, eta_engine=0.80, t_rad=1000.0, emissivity=0.85, areal_density=5.0)

        self.assertAlmostEqual(rad["jet_power_w"], 1.0e10, places=1)
        # Waste heat = 10 GW * 0.20 / 0.80 = 2.5 GW
        self.assertAlmostEqual(rad["waste_heat_w"], 2.5e9, places=1)

        # q_rad = 2 * 0.85 * 5.670374e-8 * 10^12 = 96,396.36 W/m^2
        expected_flux = 2.0 * 0.85 * 5.670374419e-8 * (1000.0**4)
        self.assertAlmostEqual(rad["radiator_flux_w_m2"], expected_flux, places=2)

        # Radiator area = 2.5e9 / 96396.36 = 25,934.58 m^2
        self.assertAlmostEqual(rad["radiator_area_m2"], 25934.58, delta=1.0)

        # Radiator mass = 5.0 * 25934.58 = 129,672.9 kg (129.7 tonnes)
        self.assertAlmostEqual(rad["radiator_mass_kg"], 129672.9, delta=5.0)

        # Thrust to mass = 1000 / 129672.9 = 0.00771 N/kg
        # Thrust to weight (g) = 0.00771 / 9.80665 = 0.000786 g
        self.assertLess(rad["thrust_to_weight_g"], 0.001)

    def test_antimatter_gamma_shielding(self):
        # 1000 N thrust at 0.331 c (9.923e7 m/s)
        thrust = 1000.0
        v_e = 0.331 * C
        res = antimatter_gamma_shielding_analysis(thrust, v_exhaust=v_e, gamma_fraction=0.33, solid_angle_fraction=0.02)

        # Jet power = 0.5 * 1000 * 9.923e7 = 4.9615e10 W (~49.6 GW)
        self.assertAlmostEqual(res["annihilation_power_w"], 4.9615e10 / 0.67, delta=1.0e8)
        # Intercepted gamma power
        self.assertGreater(res["intercepted_gamma_power_w"], 1.0e7)  # > 10 MW
        # Shield mass must be substantial (> 10 tonnes)
        self.assertGreater(res["shield_mass_tonnes"], 10.0)

    def test_macro_pellet_vs_laser_beam(self):
        comp = macro_pellet_vs_laser_beam_comparison(
            pellet_velocity=3.0e6,
            pellet_mass=1.0e-9,
            pellet_temp=1.0,
            laser_wavelength=1.06e-6,
            laser_aperture=1000.0,
            range_m=AU
        )

        # Thrust per power ratio: 2 * c / u = 2 * 299792458 / 3e6 = 199.8616
        self.assertAlmostEqual(comp["thrust_gain_factor"], 199.86, places=2)
        self.assertAlmostEqual(comp["thrust_gain_factor"], 200.0, delta=0.5)

        # Laser divergence vs pellet divergence:
        # Laser: 1.22 * 1.06e-6 / 1000 = 1.2932e-9 rad
        self.assertAlmostEqual(comp["laser_divergence_rad"], 1.2932e-9, delta=1e-11)

        # Pellet divergence is extremely small (thermal speed ~ 2e-7 m/s, theta ~ 6.8e-14 rad)
        self.assertLess(comp["pellet_divergence_rad"], 1.0e-12)

        # Spot concentration gain should be > 10,000x
        self.assertGreater(comp["spot_concentration_gain"], 10000.0)

    def test_exoplanet_terminal_capture_mechanics(self):
        cap = exoplanet_terminal_capture_analysis()

        # Proxima b orbital velocity around host star (~47.2 km/s)
        self.assertAlmostEqual(cap["host_orbital_velocity_m_s"] / 1000.0, 47.24, delta=0.5)

        # Hyperbolic excess v_inf after magsail cutoff (~352.8 km/s)
        self.assertAlmostEqual(cap["hyperbolic_excess_v_inf_m_s"] / 1000.0, 352.76, delta=0.5)

        # Terminal capture delta-v requirement (> 300 km/s)
        self.assertGreater(cap["terminal_capture_delta_v_m_s"], 300000.0)

        # Chemical mass ratio exponent log10(R) should be > 30 (impossible)
        self.assertGreater(cap["log10_mass_ratio_chemical"], 30.0)

        # Ion mass ratio should be reasonable (~20 to 30)
        self.assertGreater(cap["mass_ratio_ion"], 20.0)
        self.assertLess(cap["mass_ratio_ion"], 30.0)

        # Aerocapture heat ratio vs Apollo should be > 30,000x
        self.assertGreater(cap["aerocapture_heat_ratio_vs_apollo"], 30000.0)

    def test_feasibility_matrix_completeness(self):
        matrix = complete_propulsion_feasibility_matrix()
        self.assertEqual(len(matrix), 10)

        # Check required fields
        for entry in matrix:
            self.assertIn("rank", entry)
            self.assertIn("family", entry)
            self.assertIn("isp_s", entry)
            self.assertIn("v_e_kms", entry)
            self.assertIn("thrust_range", entry)
            self.assertIn("tw_ratio", entry)
            self.assertIn("thrust_per_mw", entry)
            self.assertIn("domain", entry)
            self.assertIn("interstellar", entry)
            self.assertIn("single_biggest_blocker", entry)

        # Chemical must not be interstellar capable
        self.assertFalse(matrix[0]["interstellar"])
        # Fusion, Antimatter, Laser must be marked interstellar capable
        fusion = [m for m in matrix if "Fusion" in m["family"]][0]
        antimatter = [m for m in matrix if "Antimatter" in m["family"]][0]
        laser = [m for m in matrix if "Laser-Pushed" in m["family"]][0]
        self.assertTrue(fusion["interstellar"])
        self.assertTrue(antimatter["interstellar"])
        self.assertTrue(laser["interstellar"])


if __name__ == "__main__":
    unittest.main()
