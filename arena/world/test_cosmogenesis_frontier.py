"""
Unit Tests for Cosmogenesis Frontier Theoretical & Empirical Engine
Agent: Kepler (A001, Gen 0)
"""

import unittest
import math
from cosmogenesis_frontier_engine import (
    electroweak_baryogenesis_feasibility,
    intergalactic_magnetogenesis_bounds,
    transplanckian_censorship_bound,
    cosmogenesis_model_discriminator_matrix,
    penrose_weyl_curvature_and_entropy,
    master_open_problems_full_taxonomy
)


class TestCosmogenesisFrontierEngine(unittest.TestCase):
    
    def test_electroweak_baryogenesis_sm_failure_and_bsm_viability(self):
        """Verify that SM fails SFOPT (sphaleron washout) and BSM dim-6 restores it."""
        res_sm = electroweak_baryogenesis_feasibility(cutoff_lambda_gev=800.0)
        
        # SM should strictly fail SFOPT
        self.assertLess(res_sm["SM_v_over_Tc"], 1.0)
        self.assertFalse(res_sm["SM_SFOPT_satisfied"])
        self.assertTrue(res_sm["SM_is_smooth_crossover"])
        self.assertIn("strictly ruled out", res_sm["SM_verdict"])
        
        # BSM with 800 GeV cutoff should satisfy SFOPT
        self.assertGreaterEqual(res_sm["BSM_v_over_Tc"], 1.0)
        self.assertTrue(res_sm["BSM_SFOPT_satisfied"])
        self.assertGreater(res_sm["BSM_Higgs_trilinear_deviation_delta_kappa"], 0.20)
        
        # LISA gravitational wave background peak in mHz band
        self.assertGreater(res_sm["GW_peak_frequency_mHz"], 1.0)
        self.assertLess(res_sm["GW_peak_frequency_mHz"], 10.0)
        self.assertGreater(res_sm["GW_peak_energy_density_Omega_h2"], 1e-12)

    def test_intergalactic_magnetogenesis_bounds(self):
        """Verify Fermi blazar lower bound and causality restrictions on primordial fields."""
        mag = intergalactic_magnetogenesis_bounds()
        
        self.assertEqual(mag["fermi_blazar_lower_bound_Gauss"], 1.0e-16)
        self.assertEqual(mag["coherence_length_Mpc"], 1.0)
        self.assertGreater(mag["biermann_deficit_factor"], 1000.0)
        
        # EW causal comoving scale should be much smaller than 1 Mpc (causality gap > 100)
        self.assertGreater(mag["causality_gap_to_Mpc"], 100.0)
        self.assertGreater(len(mag["resolving_observations"]), 0)

    def test_transplanckian_censorship_bound(self):
        """Verify TCC limit r <= 10^-28 and clash with Starobinsky inflation."""
        tcc = transplanckian_censorship_bound(n_efolds=60.0)
        
        # TCC maximum allowed r must be <= 1e-25
        self.assertLess(tcc["TCC_maximum_allowed_r"], 1.0e-25)
        # Starobinsky r must be ~ 0.0033
        self.assertAlmostEqual(tcc["Starobinsky_predicted_r"], 0.003333, places=4)
        # Clash should exceed 20 orders of magnitude
        self.assertGreater(tcc["clash_orders_of_magnitude"], 20.0)
        self.assertEqual(tcc["LiteBIRD_sensitivity_sigma_r"], 0.001)

    def test_model_discriminator_matrix(self):
        """Verify the 5-paradigm cosmogenesis discriminator matrix consistency."""
        matrix = cosmogenesis_model_discriminator_matrix()
        self.assertEqual(len(matrix), 5)
        
        model_names = [m["model_name"] for m in matrix]
        self.assertTrue(any("Starobinsky" in name for name in model_names))
        self.assertTrue(any("Ekpyrotic" in name for name in model_names))
        self.assertTrue(any("String Gas" in name for name in model_names))
        self.assertTrue(any("Loop Quantum" in name for name in model_names))
        self.assertTrue(any("Conformal Cyclic" in name for name in model_names))
        
        # Starobinsky consistency relation: nT = -r/8 < 0
        starobinsky = next(m for m in matrix if "Starobinsky" in m["model_name"])
        self.assertAlmostEqual(starobinsky["tensor_spectral_index_nT"], -starobinsky["tensor_to_scalar_r"] / 8.0, places=5)
        self.assertLess(starobinsky["tensor_spectral_index_nT"], 0.0)
        
        # Ekpyrotic must predict unobservable r and non-zero non-Gaussianity
        ekpyrotic = next(m for m in matrix if "Ekpyrotic" in m["model_name"])
        self.assertLess(ekpyrotic["tensor_to_scalar_r"], 1.0e-30)
        self.assertNotEqual(ekpyrotic["non_gaussianity_f_NL_local"], 0.0)
        
        # String Gas must predict BLUE-TILTED tensor spectrum nT > 0
        string_gas = next(m for m in matrix if "String Gas" in m["model_name"])
        self.assertGreater(string_gas["tensor_spectral_index_nT"], 0.0)

    def test_penrose_weyl_entropy(self):
        """Verify Penrose initial entropy vs black hole maximum entropy."""
        pen = penrose_weyl_curvature_and_entropy()
        
        self.assertAlmostEqual(pen["log10_S_init"], 89.9, places=1)
        self.assertGreater(pen["log10_S_max"], 120.0)
        self.assertIn("exp(-10^", pen["phase_space_tuning_factor"])

    def test_master_open_problems_taxonomy(self):
        """Verify the 10 master open problems are fully specified."""
        problems = master_open_problems_full_taxonomy()
        self.assertEqual(len(problems), 10)
        
        required_keys = [
            "id", "name", "epistemic_status", "unexplained",
            "resolving_observation", "target_facility", "quantitative_threshold"
        ]
        for prob in problems:
            for key in required_keys:
                self.assertIn(key, prob, f"Problem {prob.get('id')} missing key {key}")
                self.assertIsInstance(prob[key], str)
                self.assertGreater(len(prob[key]), 0)


if __name__ == "__main__":
    unittest.main()
