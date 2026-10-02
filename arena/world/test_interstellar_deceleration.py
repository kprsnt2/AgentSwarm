"""
Unit and Physical Invariant Tests for Interstellar Relativistic Deceleration
Author: Raman (Agent A002, Generation 0)
Domain: Travel at or near light speed (lightspeed)

Verifies:
1. Proton relativistic kinematics at beta = 0.2 (E_k = 19.348 MeV, gamma = 1.02062).
2. Bethe-Bloch nanometer penetration and the ~4.0e-6 drag suppression factor.
3. Actual ISM drag stopping distance > 400,000 light-years.
4. Forward staged sail diffraction spot size > 100,000 km and geometric interception < 1e-14.
5. Photogravitational assist capture velocity ceiling at Alpha Centauri A (1,089 km/s = 0.00363c).
6. Tuned magsail loop parameters for Alpha Centauri capture (R ~ 146 m, M ~ 41 g, v_arrival ~ 1,100 km/s).
7. Magsail transit time penalty (~127 years vs 21.2 years flyby).
8. Superconductor cryogenic stability in deep space (T_eq ~ 19.5 K < T_c = 92 K).
9. Virial hoop tension mechanical integrity (safety factor > 10,000).
10. Astrospheric stellar wind braking integration.
"""

import unittest
import math
from interstellar_deceleration_analyzer import (
    RelativisticDecelerationAnalyzer,
    C,
    DIST_PROXIMA,
    LY,
    AU,
)


class TestInterstellarDeceleration(unittest.TestCase):
    def setUp(self):
        self.analyzer = RelativisticDecelerationAnalyzer(beta=0.2)

    def test_proton_kinematics(self):
        kin = self.analyzer.proton_kinematics()
        self.assertAlmostEqual(kin["beta"], 0.2, places=4)
        self.assertAlmostEqual(kin["gamma"], 1.020621, places=5)
        # Kinetic energy of proton at 0.2c should be ~ 19.348 MeV
        self.assertGreater(kin["ke_mev"], 19.3)
        self.assertLess(kin["ke_mev"], 19.4)
        # Momentum check: p = gamma * m_p * v
        expected_p = kin["gamma"] * 1.67262192369e-27 * (0.2 * C)
        self.assertAlmostEqual(kin["momentum"], expected_p, places=22)

    def test_nanometer_sail_penetration_and_drag_failure(self):
        pen = self.analyzer.nanometer_sail_penetration(sail_mass=1e-3, sail_area=16.0)
        # Areal density must be 6.25e-5 kg/m^2
        self.assertAlmostEqual(pen["areal_density_kg_m2"], 6.25e-5, places=8)
        # Thickness ~ 25 nm for rho = 2500 kg/m^3
        self.assertAlmostEqual(pen["thickness_nm"], 25.0, places=2)
        # Fraction of energy deposited must be < 0.001% (< 1e-4)
        self.assertLess(pen["fraction_energy_deposited"], 1e-4)
        self.assertGreater(pen["fraction_energy_deposited"], 1e-6)
        # Actual drag pressure must be ~ 2.4e-11 Pa vs classical ~ 6.0e-6 Pa
        self.assertAlmostEqual(pen["p_drag_actual_pa"], 2.40688e-11, delta=1e-12)
        self.assertAlmostEqual(pen["p_drag_classical_pa"], 6.00368e-6, delta=1e-7)
        # Drag suppression factor must be ~ 4.0e-6
        self.assertAlmostEqual(pen["drag_suppression_factor"], 4.009e-6, delta=1e-7)
        # Stopping distance must be ~ 493,000 light-years
        self.assertGreater(pen["stopping_distance_ly"], 400000.0)
        self.assertLess(pen["stopping_distance_ly"], 600000.0)

    def test_forward_staged_sail_diffraction_blocker(self):
        opt = self.analyzer.forward_staged_sail_optics(lambda_laser=1.06e-6, d_tx=1000.0, d_sail=4.0)
        # Spot diameter at Alpha Centauri (> 100,000 km)
        self.assertGreater(opt["spot_diameter_km"], 100000.0)
        self.assertLess(opt["spot_diameter_km"], 110000.0)
        # Power interception fraction < 1e-14
        self.assertLess(opt["power_intercept_fraction"], 2e-14)
        # Doppler power loss factor = (1-beta)/(1+beta) = 0.8/1.2 = 2/3 ~ 0.6667
        self.assertAlmostEqual(opt["doppler_power_factor"], 2.0 / 3.0, places=3)
        # Required transmitter aperture for 100 m sail > 1,000,000 km
        self.assertGreater(opt["required_tx_diameter_100m_km"], 1000000.0)

    def test_photogravitational_assist_capture_ceiling(self):
        pg = self.analyzer.photogravitational_assist_limit(sigma=6.25e-5, refl=0.9999, t_max=500.0)
        self.assertTrue(pg["can_brake"])
        # Lightness parameter beta_L ~ 33.8
        self.assertGreater(pg["beta_l"], 30.0)
        self.assertLess(pg["beta_l"], 36.0)
        # Periastron r_min ~ 0.054 AU
        self.assertAlmostEqual(pg["r_min_au"], 0.054, delta=0.005)
        # Maximum capture velocity must be ~ 1,089 km/s (0.00363c)
        self.assertAlmostEqual(pg["v_max_capture_km_s"], 1089.2, delta=5.0)
        self.assertAlmostEqual(pg["v_max_capture_c"], 0.003633, delta=0.0001)

    def test_tuned_magsail_parameters(self):
        tune = self.analyzer.solve_tuned_magsail_capture(target_v_km_s=1100.0, dist_target_ly=4.244)
        # Tuned loop radius ~ 146.46 m
        self.assertAlmostEqual(tune["r_loop_m"], 146.46, delta=2.0)
        # Tuned coil mass ~ 40.95 g
        self.assertAlmostEqual(tune["coil_mass_g"], 40.95, delta=2.0)
        # Arrival velocity matches target 1,100 km/s
        self.assertAlmostEqual(tune["v_at_target_km_s"], 1100.0, delta=1.0)
        # Total stopping distance > 4.5 ly
        self.assertAlmostEqual(tune["total_stopping_dist_ly"], 4.56, delta=0.1)

    def test_magsail_transit_time_and_penalty(self):
        tune = self.analyzer.solve_tuned_magsail_capture()
        # Flyby time at constant 0.2c = 4.244 / 0.2 = 21.22 years
        self.assertAlmostEqual(tune["flyby_time_years"], 21.22, delta=0.1)
        # Magsail transit time ~ 127.3 years
        self.assertAlmostEqual(tune["transit_time_years"], 127.33, delta=2.0)
        # Penalty factor ~ 6.0x
        self.assertAlmostEqual(tune["transit_time_penalty_factor"], 6.0, delta=0.2)

    def test_superconducting_cryogenic_stability(self):
        tune = self.analyzer.solve_tuned_magsail_capture()
        # Equilibrium wire temperature under proton deposition ~ 19.5 K
        self.assertAlmostEqual(tune["equilibrium_temp_k"], 19.50, delta=1.0)
        # Must be well below YBCO critical temperature (92 K)
        self.assertLess(tune["equilibrium_temp_k"], 30.0)
        self.assertLess(tune["equilibrium_temp_k"], tune["superconducting_critical_temp_k"])

    def test_hoop_stress_structural_safety(self):
        tune = self.analyzer.solve_tuned_magsail_capture()
        # Tensile stress ~ 0.032 MPa
        self.assertAlmostEqual(tune["tensile_stress_mpa"], 0.032, delta=0.01)
        # Safety factor > 30,000 against 1,200 MPa Hastelloy yield strength
        self.assertGreater(tune["yield_safety_factor"], 30000.0)

    def test_astrospheric_stellar_wind_braking(self):
        sim = self.analyzer.astrospheric_braking_simulation(
            v_entry=1100e3, r_start_au=80.0, r_end_au=0.054, m_craft=0.041, r_loop=146.46
        )
        # Inward transit sheds ~ 15 km/s
        self.assertAlmostEqual(sim["delta_v_shed_km_s"], 15.08, delta=1.0)
        # Final velocity at periastron is ~ 1,085 km/s
        self.assertAlmostEqual(sim["v_final_km_s"], 1084.9, delta=2.0)
        # Final velocity must be strictly within the 1089.2 km/s photogravitational capture window
        self.assertLessEqual(sim["v_final_km_s"], 1089.5)
        # Encounter time ~ 126 days
        self.assertAlmostEqual(sim["encounter_time_days"], 125.9, delta=3.0)


if __name__ == "__main__":
    unittest.main()
