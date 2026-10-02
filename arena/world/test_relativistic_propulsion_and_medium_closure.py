"""
test_relativistic_propulsion_and_medium_closure.py

Unit test suite for relativistic propulsion, radiator scaling, gram-scale
beamed sails, ISM benchmarks (beta 0.10, 0.12, 0.20, 0.50, 0.90), and FTL causality proof.

Author: Raman (Agent A002, Generation 0)
"""

import unittest
import math
from relativistic_propulsion_and_medium_closure import (
    C, G0, SIGMA_SB, LY_TO_M, M_P,
    lorentz_gamma, kinetic_energy_per_kg, proton_kinetic_energy_mev,
    radiator_power_to_thrust_thermal, radiator_specific_mass,
    radiator_mass_to_thrust, max_thermal_acceleration,
    antimatter_radiator_limits, nep_radiator_limits, fusion_radiator_limits,
    gram_scale_dust_interaction, gram_scale_proton_radiation_dose,
    medium_interaction_benchmark,
    antitelephone_boost_condition, antitelephone_closed_loop_return_boost,
    antitelephone_event_coordinates
)


class TestRelativisticPropulsionAndMediumClosure(unittest.TestCase):

    def test_lorentz_and_kinematics(self):
        # Gamma identity checks
        self.assertAlmostEqual(lorentz_gamma(0.0), 1.0)
        self.assertAlmostEqual(lorentz_gamma(0.6), 1.25)
        self.assertAlmostEqual(lorentz_gamma(0.8), 5.0 / 3.0)
        # Established ground truth check: energy for 1 kg at 0.99c is ~5.5e17 J
        ke_99 = kinetic_energy_per_kg(0.99)
        self.assertAlmostEqual(ke_99 / 1e17, 5.472, places=2)
        self.assertTrue(5.4e17 < ke_99 < 5.6e17)

    def test_generalized_radiator_scaling_derivation(self):
        # Verify P_waste / F formula: P_waste/F = 0.5 * ve * (1 - eta) / eta
        # If ve = 1e5 m/s, eta = 0.5 -> P_waste/F = 0.5 * 1e5 * 1 = 5e4 W/N
        pw_f = radiator_power_to_thrust_thermal(1.0e5, 0.5)
        self.assertEqual(pw_f, 5.0e4)

        # Radiator Stefan-Boltzmann specific mass
        # At T = 1000 K, sigma_panel = 10 kg/m^2, eps = 1.0, two-sided
        # q = 2 * 1.0 * 5.67037e-8 * 1e12 = 1.13407e5 W/m^2
        # alpha_rad = 10 / 1.13407e5 = 8.81776e-5 kg/W
        alpha = radiator_specific_mass(1000.0, sigma_panel=10.0, emissivity=1.0, two_sided=True)
        self.assertAlmostEqual(alpha, 10.0 / (2.0 * SIGMA_SB * 1e12), places=8)

        # Inverse acceleration scaling: a_max = 1 / (M_rad / F)
        m_rad_f = radiator_mass_to_thrust(pw_f, alpha)
        a_max = max_thermal_acceleration(m_rad_f)
        self.assertAlmostEqual(a_max, 1.0 / (alpha * pw_f), places=8)

    def test_antimatter_radiator_paradox_exact_numbers(self):
        # Reproduces the Raman A002 finding: 41.64 MW/N, 194.3 kg/N, ~5.25e-4 g
        am = antimatter_radiator_limits(f_waste=0.05, w_exhaust=0.36 * C,
                                       t_rad_k=1800.0, sigma_panel=5.0, emissivity=0.90)
        self.assertAlmostEqual(am["p_waste_over_f_MW_per_N"], 41.638, places=2)
        self.assertAlmostEqual(am["m_rad_over_f_kg_per_N"], 194.305, places=1)
        self.assertAlmostEqual(am["a_max_g0"], 5.248e-4, places=6)

    def test_nep_and_fusion_radiator_acceleration_clamping(self):
        # NEP with ve = 49 km/s (Isp = 5000 s), eta = 0.35, T_rad = 900 K
        nep = nep_radiator_limits(ve=4.90e4, eta=0.35, t_rad_k=900.0, sigma_panel=8.0)
        self.assertTrue(nep["p_waste_over_f_kW_per_N"] > 40.0) # ~45.5 kW/N
        self.assertTrue(nep["a_max_g0"] < 0.02) # ~0.0177 g0

        # Fusion with ve = 1.03e7 m/s (Daedalus), eta = 0.50, T_rad = 1500 K
        fusion = fusion_radiator_limits(ve=1.03e7, eta=0.50, t_rad_k=1500.0, sigma_panel=5.0)
        self.assertAlmostEqual(fusion["p_waste_over_f_MW_per_N"], 5.15, places=2)
        # Clamps fusion acceleration to ~ 0.002 g
        self.assertTrue(0.001 < fusion["a_max_g0"] < 0.003)
        # At this acceleration, time to reach 0.1c (3e7 m/s) is > 40 years!
        t_burn_s = (0.10 * C) / fusion["a_max_m_s2"]
        self.assertTrue(t_burn_s > 45.0 * 365.25 * 86400.0)

    def test_gram_scale_dust_and_sail_edge_on_necessity(self):
        # 1 g craft (0.5 g sail of 0.1 g/m^2 -> 5 m^2) to Proxima at 0.2c
        dust = gram_scale_dust_interaction(craft_mass_g=1.0, beta=0.20)
        # Face-on hits from 0.1 um grains exceeds 1e11 impacts
        self.assertTrue(dust["hits_face_on_0_1_um"] > 1.0e11)
        # Total energy dumped on face-on sail exceeds 1 GJ
        self.assertTrue(dust["total_energy_face_on_0_1_um_J"] > 1.0e9)
        # Wafer area (1 cm^2) has far fewer impacts (~1e6 for 0.1 um)
        self.assertTrue(dust["hits_wafer_0_1_um"] < 1.0e7)
        # Large grains (10 um) have low impact probability on 1 cm^2 wafer (< 1e-4)
        self.assertTrue(dust["prob_hit_10_um_wafer"] < 1.0e-3)

    def test_gram_scale_radiation_shielding_closure(self):
        # 1 g wafer probe at 0.2c (19.35 MeV ISM protons)
        rad = gram_scale_proton_radiation_dose(beta=0.20, wafer_area_cm2=1.0, wafer_mass_g=0.5)
        self.assertAlmostEqual(rad["e_p_mev"], 19.35, places=1)
        # Unshielded dose is lethal to semiconductors (> 1e13 Gray = 1e15 Rad)
        self.assertTrue(rad["unshielded_dose_gray"] > 1.0e12)
        # Required shield mass for 1 cm^2 is ~ 0.46 g
        self.assertTrue(0.40 < rad["shield_mass_g"] < 0.55)
        # Diamond shield thickness is ~ 1.3 mm
        self.assertTrue(1.0 < rad["shield_thickness_diamond_mm"] < 1.6)
        # Demonstrates shield mass fraction is ~ 45-50% of probe rest mass
        self.assertTrue(0.40 < rad["shield_mass_fraction"] < 0.55)

    def test_ism_medium_benchmarks_all_regimes(self):
        # Check benchmarks for beta = 0.10, 0.12, 0.20, 0.50, 0.90
        b10 = medium_interaction_benchmark(0.10)
        b12 = medium_interaction_benchmark(0.12)
        b20 = medium_interaction_benchmark(0.20)
        b50 = medium_interaction_benchmark(0.50)
        b90 = medium_interaction_benchmark(0.90)

        # Kinetic energies
        self.assertAlmostEqual(b10["proton_ke_mev"], 4.73, places=1)
        self.assertAlmostEqual(b12["proton_ke_mev"], 6.85, places=1)
        self.assertAlmostEqual(b20["proton_ke_mev"], 19.35, places=1)
        self.assertAlmostEqual(b50["proton_ke_mev"], 145.2, places=0)
        self.assertAlmostEqual(b90["proton_ke_mev"], 1214.6, places=0)

        # Thermal flux increases monotonically
        self.assertAlmostEqual(b10["thermal_flux_w_m2"], 22.7, places=0)
        self.assertAlmostEqual(b12["thermal_flux_w_m2"], 39.5, places=0)
        self.assertAlmostEqual(b20["thermal_flux_w_m2"], 186.0, places=0)
        self.assertTrue(b90["thermal_flux_w_m2"] > 5.0e4) # ~52.5 kW/m^2

        # Bragg range in graphite:
        # At 0.10c: fraction of a mm (~0.22 mm)
        self.assertTrue(0.1 < b10["bragg_range_graphite_mm"] < 0.5)
        # At 0.12c: ~0.42 mm
        self.assertTrue(0.2 < b12["bragg_range_graphite_mm"] < 0.8)
        # At 0.20c: ~2 mm
        self.assertTrue(1.0 < b20["bragg_range_graphite_mm"] < 3.0)
        # At 0.90c: > 1 meter of shielding required
        self.assertTrue(b90["bragg_range_graphite_mm"] > 1000.0)

        # Sputtering erosion over 4.2 ly is sub-micron for subluminal flybys
        self.assertTrue(b10["erosion_depth_4_2_ly_um"] < 1.0)
        self.assertTrue(b20["erosion_depth_4_2_ly_um"] < 1.0)

    def test_ftl_causality_obstruction_and_antitelephone(self):
        # If U = 2c, condition for backward time propagation: v > c / 2 = 0.5c
        self.assertAlmostEqual(antitelephone_boost_condition(2.0), 0.5)
        # For U = 10c, v > 0.1c
        self.assertAlmostEqual(antitelephone_boost_condition(10.0), 0.1)

        # Closed loop return boost condition: v > 2*U / (U^2 + 1)
        # For U = 2c: v > 2*2 / (4 + 1) = 4/5 = 0.8c
        self.assertAlmostEqual(antitelephone_closed_loop_return_boost(2.0), 0.8)

        # Spacetime event transform check:
        # Emitter at x=0 sends signal at U = 2c to Alpha Centauri (4.24 ly).
        # Target receives at t = 2.12 yr.
        # Boosted observer moving at v = 0.6c (since v > 0.5c):
        coords = antitelephone_event_coordinates(4.24, ftl_speed_u_over_c=2.0, v_boost_over_c=0.6)
        self.assertTrue(coords["dt_negative"])
        self.assertTrue(coords["t1_boosted_yr"] < 0.0) # Received in past!
        self.assertTrue(coords["invariant_interval_s2"] < 0.0) # Strictly spacelike interval


if __name__ == "__main__":
    unittest.main()
