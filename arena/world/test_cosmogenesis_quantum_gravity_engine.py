"""
Unit Test Suite for Cosmogenesis Quantum Gravity and Observational Discrimination Engine
Author: Kepler (A001) | Generation: 0 | Epistemic Class: Empirical Precision Cosmology
"""

import unittest
import math
from cosmogenesis_quantum_gravity_engine import (
    PhysicalConstants,
    CosmicEntropyEngine,
    QuantumCosmogenesisDiscriminator,
    BaryogenesisPhaseTransitionEngine,
    HubbleAcousticScaleEngine,
    PrimordialMagnetogenesisEngine,
    CosmogenesisOpenProblemsRegistry,
    run_cosmogenesis_frontiers_summary
)

class TestCosmogenesisQuantumGravityEngine(unittest.TestCase):

    def setUp(self):
        self.const = PhysicalConstants()
        self.entropy = CosmicEntropyEngine(self.const)
        self.quantum = QuantumCosmogenesisDiscriminator(self.const)
        self.baryon = BaryogenesisPhaseTransitionEngine(self.const)
        self.hubble = HubbleAcousticScaleEngine(self.const)
        self.magneto = PrimordialMagnetogenesisEngine()
        self.registry = CosmogenesisOpenProblemsRegistry()

    def test_planck_units(self):
        """Verify derived Planck scales match standard physical definitions."""
        self.assertAlmostEqual(self.const.m_Pl, 2.176434e-8, delta=1e-10)
        self.assertAlmostEqual(self.const.l_Pl, 1.616255e-35, delta=1e-37)
        self.assertAlmostEqual(self.const.t_Pl, 5.391247e-44, delta=1e-46)
        self.assertTrue(self.const.rho_Pl > 1e113)

    def test_cosmic_entropy_hierarchy(self):
        """Verify the monotonic cosmic entropy hierarchy: S_init < S_SMBH < S_max (de Sitter)."""
        s_gamma = self.entropy.cmb_photon_entropy()
        s_nu = self.entropy.relic_neutrino_entropy()
        s_smbh = self.entropy.supermassive_black_hole_entropy()
        s_max = self.entropy.de_sitter_horizon_entropy()

        # Check photon entropy order ~ 10^88 - 10^90 k_B
        self.assertTrue(1e88 < s_gamma < 1e91)
        # Check neutrino entropy
        self.assertAlmostEqual(s_nu / s_gamma, 21.0 / 11.0, places=4)
        # Check SMBH entropy order ~ 10^104 k_B (Egan & Lineweaver 2010)
        self.assertTrue(1e103 < s_smbh < 1e105)
        # Check de Sitter horizon entropy order ~ 10^122 k_B
        self.assertTrue(1e121 < s_max < 1e124)
        # Check strict inequality hierarchy
        self.assertTrue(s_gamma < s_smbh < s_max)

    def test_penrose_phase_space_ratio(self):
        """Verify Penrose's phase space volume ratio calculation."""
        s_init, s_max, ratio_str = self.entropy.penrose_phase_space_volume_ratio()
        self.assertTrue(s_init < 1e92)
        self.assertTrue(s_max > 1e121)
        self.assertTrue("10^(-" in ratio_str)

    def test_quantum_cosmogenesis_models(self):
        """Verify canonical origin models and their specific observable predictions."""
        models = self.quantum.get_canonical_models()
        self.assertEqual(len(models), 5)
        self.assertIn("single_field_slow_roll", models)
        self.assertIn("picard_lefschetz_tunneling", models)
        self.assertIn("loop_quantum_cosmology_bounce", models)
        self.assertIn("string_gas_cosmology", models)
        self.assertIn("ekpyrotic_cyclic_bounce", models)

        # Single-field consistency relation: n_T = -r/8
        sf = models["single_field_slow_roll"]
        self.assertAlmostEqual(sf.tensor_spectral_index_n_T, -sf.tensor_to_scalar_r / 8.0)

        # LQC and String Gas predict blue tensor tilt (n_T > 0)
        self.assertTrue(models["loop_quantum_cosmology_bounce"].tensor_spectral_index_n_T > 0)
        self.assertTrue(models["string_gas_cosmology"].tensor_spectral_index_n_T > 0)

        # Ekpyrotic predicts tiny r
        self.assertTrue(models["ekpyrotic_cyclic_bounce"].tensor_to_scalar_r < 1e-10)

    def test_trans_planckian_censorship_bound(self):
        """Verify TCC evaluation for slow roll inflation."""
        res_high = self.quantum.evaluate_tcc_bound(r_measured=0.0035)
        self.assertTrue(res_high["violates_tcc"])
        self.assertIn("falsifies the TCC", res_high["implication"])

        res_low = self.quantum.evaluate_tcc_bound(r_measured=1e-35)
        self.assertFalse(res_low["violates_tcc"])

    def test_sm_sakharov_deficit(self):
        """Verify Standard Model failure to explain baryon asymmetry."""
        deficit = self.baryon.sm_sakharov_deficit()
        self.assertFalse(deficit["is_first_order_transition"])
        self.assertTrue(deficit["deficit_orders_of_magnitude"] > 9.5)
        self.assertEqual(deficit["eta_observed"], 6.12e-10)

    def test_thermal_leptogenesis_bounds(self):
        """Verify Davidson-Ibarra bound and resolving experiments."""
        lepto = self.baryon.thermal_leptogenesis_bounds()
        self.assertEqual(lepto["davidson_ibarra_bound_N1_mass_GeV"], 1e9)
        self.assertTrue(lepto["predicts_majorana_neutrinos"])
        self.assertTrue(len(lepto["resolving_experiments"]) >= 3)

    def test_phase_transition_gw_peak(self):
        """Verify GW peak frequency for electroweak scale transition."""
        gw = self.baryon.phase_transition_gravitational_wave_peak(T_star_GeV=100.0)
        # Peak at ~1.9e-5 * 100 / 100 Hz ~ 1.9e-5 Hz
        self.assertAlmostEqual(gw["f_peak_Hz"], 1.91e-5, delta=1e-6)
        self.assertTrue(gw["omega_gw_h2_peak"] > 1e-12)

    def test_hubble_sound_horizon_shift(self):
        """Verify the exact sound horizon shift needed to reconcile H0."""
        shift = self.hubble.required_sound_horizon_shift()
        self.assertAlmostEqual(shift["H_0_CMB"], 67.4)
        self.assertAlmostEqual(shift["H_0_Local"], 73.04)
        # Tension should be ~ 4.85 sigma
        self.assertTrue(4.5 < shift["tension_sigma"] < 5.2)
        # Target r_s should be ~ 135.8 Mpc
        self.assertTrue(134.0 < shift["r_s_target_Mpc"] < 138.0)
        # Delta r_s should be negative ~ -9.8 to -11.4 Mpc
        self.assertTrue(-13.0 < shift["delta_r_s_Mpc"] < -9.0)
        # Percentage reduction ~ 6.5% - 8%
        self.assertTrue(-9.0 < shift["percentage_reduction"] < -6.0)

    def test_early_dark_energy_mechanics(self):
        """Verify EDE fraction and exacerbated S8 tension."""
        ede = self.hubble.early_dark_energy_parameters()
        self.assertEqual(ede["z_critical"], 3500.0)
        self.assertTrue(0.08 < ede["f_ede_critical"] < 0.15)
        self.assertTrue(ede["s_8_ede_predicted"] > ede["s_8_weak_lensing_observed"])
        self.assertTrue(ede["s_8_tension_sigma"] > 2.0)

    def test_primordial_magnetogenesis_bounds(self):
        """Verify blazar void limits and SKA discovery window."""
        mag = self.magneto.evaluate_void_field_implication()
        self.assertEqual(mag["B_void_lower_bound_Gauss"], 1e-16)
        self.assertEqual(mag["B_cmb_upper_bound_Gauss"], 1e-9)
        self.assertEqual(mag["viable_window_orders_of_magnitude"], 7.0)

    def test_open_problems_registry_completeness(self):
        """Verify the 8 canonical open problems and required quantitative criteria."""
        problems = self.registry.problems
        self.assertEqual(len(problems), 8)

        for p in problems:
            self.assertTrue(len(p.title) > 5)
            self.assertTrue(len(p.theoretical_failure) > 20)
            self.assertTrue(len(p.resolving_observatory) > 3)
            self.assertTrue(len(p.specific_observable) > 10)
            self.assertTrue(len(p.quantitative_threshold) > 10)
            self.assertTrue(len(p.falsification_criterion) > 15)

        # Verify markdown table generation
        md_table = self.registry.to_markdown_table()
        self.assertTrue("| ID | Open Problem |" in md_table)
        self.assertTrue("| **#8** |" in md_table)

    def test_full_summary_runner(self):
        """Verify the complete summary execution pipeline."""
        summary = run_cosmogenesis_frontiers_summary()
        self.assertEqual(summary["open_problems_count"], 8)
        self.assertEqual(summary["models_count"], 5)
        self.assertTrue("phase_space_volume_ratio" in summary["entropy"])


if __name__ == "__main__":
    unittest.main()
