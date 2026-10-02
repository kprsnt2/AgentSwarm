"""
test_cosmogenesis_engine.py - Test Suite for Cosmogenesis Empirical Engine
Agent: Raman (A002, Generation 0)
Domain: Origin of the universe (cosmogenesis)

Verifies:
1. analyze() contract schema (domain, claims, confidence, evidence types).
2. CMB blackbody spectrum physics and COBE/FIRAS ground truths.
3. Big Bang Nucleosynthesis (BBN) light element predictions and the Lithium-7 anomaly.
4. Hubble tension statistical significance and standard siren resolution bounds.
5. Starobinsky R^2 cosmic inflation observables and observational testability.
6. Cosmological constant 120-order-of-magnitude QFT discrepancy.
7. Standard Model failure of Sakharov baryogenesis conditions.
8. Master open problems taxonomy, target facilities, and quantitative thresholds.
"""

import sys
import os
import unittest
import math

# Ensure module path is accessible when run directly or via test runner
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cosmogenesis_engine import (
    C,
    H_PLANCK,
    K_B,
    SIGMA_SB,
    T_CMB_FIDUCIAL,
    H0_EARLY_PLANCK,
    H0_LATE_SHOES,
    Y_P_OBSERVED,
    D_OVER_H_OBSERVED,
    LI7_OVER_H_OBSERVED,
    cmb_spectral_properties,
    bbn_nucleosynthesis_abundances,
    hubble_tension_analysis,
    inflation_dynamics,
    cosmological_constant_discrepancy,
    baryogenesis_sakharov_audit,
    penrose_weyl_entropy_contrast,
    get_open_problems_and_resolutions,
    analyze,
)


class TestCosmogenesisEngine(unittest.TestCase):
    """Rigorous empirical verification of the cosmogenesis engine."""

    def test_analyze_contract_schema(self):
        """Property 1: Verify analyze() returns the exact required schema with valid types."""
        result = analyze()
        self.assertIsInstance(result, dict)

        # Four required contract keys
        self.assertIn("domain", result)
        self.assertIn("claims", result)
        self.assertIn("confidence", result)
        self.assertIn("evidence", result)

        # Domain verification
        self.assertIsInstance(result["domain"], str)
        self.assertTrue(len(result["domain"]) > 0)
        self.assertIn("cosmogenesis", result["domain"].lower())

        # Claims verification
        self.assertIsInstance(result["claims"], list)
        self.assertGreaterEqual(len(result["claims"]), 5)
        for claim in result["claims"]:
            self.assertIsInstance(claim, str)
            self.assertTrue(len(claim) > 20)

        # Confidence verification
        self.assertIsInstance(result["confidence"], float)
        self.assertGreaterEqual(result["confidence"], 0.0)
        self.assertLessEqual(result["confidence"], 1.0)

        # Evidence verification
        self.assertIsInstance(result["evidence"], list)
        self.assertGreaterEqual(len(result["evidence"]), 5)
        for ev in result["evidence"]:
            self.assertIsInstance(ev, dict)
            self.assertIn("kind", ev)
            self.assertIn("value", ev)
            self.assertIn("source", ev)
            self.assertIsInstance(ev["kind"], str)
            self.assertIsInstance(ev["value"], str)
            self.assertIsInstance(ev["source"], str)

    def test_cmb_blackbody_ground_truth(self):
        """Property 2: Verify CMB Planck radiation law, peak frequency, and energy density."""
        cmb = cmb_spectral_properties(temperature=T_CMB_FIDUCIAL, frequency_hz=160.23e9)
        
        # Temperature matches COBE/FIRAS ground truth
        self.assertAlmostEqual(cmb["temperature_k"], 2.72548, places=4)
        
        # Wien peak frequency in GHz: 2.821439 * k_B * T / h ~ 160.23 GHz
        expected_peak_ghz = 2.821439372 * K_B * T_CMB_FIDUCIAL / (H_PLANCK * 1.0e9)
        self.assertAlmostEqual(cmb["wien_peak_frequency_ghz"], expected_peak_ghz, places=2)
        self.assertTrue(159.0 < cmb["wien_peak_frequency_ghz"] < 161.0)
        
        # Energy density u = 4 * sigma * T^4 / c ~ 4.17e-14 J/m^3
        expected_u = (4.0 * SIGMA_SB * (T_CMB_FIDUCIAL ** 4)) / C
        self.assertAlmostEqual(cmb["energy_density_j_m3"], expected_u, places=18)
        self.assertTrue(4.1e-14 < cmb["energy_density_j_m3"] < 4.3e-14)
        
        # Photon number density ~ 410.7 cm^-3
        self.assertTrue(405.0 < cmb["photon_number_density_cm3"] < 415.0)

        # FIRAS limits
        self.assertEqual(cmb["cobe_firas_mu_distortion_limit"], 9.0e-5)
        self.assertEqual(cmb["cobe_firas_y_distortion_limit"], 1.5e-5)

        # Boundary condition check: negative temperature must raise ValueError
        with self.assertRaises(ValueError):
            cmb_spectral_properties(temperature=-1.0)

    def test_bbn_abundance_concordance_and_lithium_tension(self):
        """Property 3: Verify BBN predictions for H, He-4, D, and the 9.2-sigma Lithium-7 anomaly."""
        bbn = bbn_nucleosynthesis_abundances(eta_10=6.12)

        # Primordial Helium-4 mass fraction Y_p ~ 0.245 +/- 0.003
        self.assertTrue(0.240 < bbn["he4_mass_fraction_yp"] < 0.250)
        self.assertAlmostEqual(bbn["he4_mass_fraction_yp"], Y_P_OBSERVED, delta=0.005)

        # Primordial Deuterium D/H ~ 2.54e-5
        self.assertTrue(2.4e-5 < bbn["deuterium_to_hydrogen_ratio"] < 2.7e-5)
        self.assertAlmostEqual(bbn["deuterium_to_hydrogen_ratio"], D_OVER_H_OBSERVED, delta=0.15e-5)

        # Primordial Lithium-7: Predicted ~ 4.68e-10 vs Observed Spite ~ 1.58e-10
        self.assertTrue(4.3e-10 < bbn["li7_to_hydrogen_ratio_predicted"] < 5.0e-10)
        self.assertAlmostEqual(bbn["li7_observed_spite_plateau"], 1.58e-10, places=12)

        # Severe deficit factor ~ 2.96x
        self.assertTrue(2.7 < bbn["li7_deficit_factor"] < 3.2)

        # Statistical tension exceeds 8.0-sigma
        self.assertGreater(bbn["li7_tension_sigma"], 8.0)

        # Boundary condition check
        with self.assertRaises(ValueError):
            bbn_nucleosynthesis_abundances(eta_10=-2.0)

    def test_hubble_tension_statistics_and_sirens_threshold(self):
        """Property 4: Verify Hubble tension significance (4.85-sigma) and standard siren requirements."""
        tension = hubble_tension_analysis(
            h0_early=H0_EARLY_PLANCK,
            sigma_early=0.54,
            h0_late=H0_LATE_SHOES,
            sigma_late=1.04
        )

        # Delta H_0 = 73.04 - 67.36 = 5.68 km/s/Mpc
        self.assertAlmostEqual(tension["delta_h0_km_s_mpc"], 5.68, places=2)

        # Combined 1-sigma uncertainty: sqrt(0.54^2 + 1.04^2) ~ 1.172 km/s/Mpc
        expected_sigma = math.sqrt(0.54**2 + 1.04**2)
        self.assertAlmostEqual(tension["sigma_combined"], expected_sigma, places=3)

        # Tension significance Z = 5.68 / 1.172 ~ 4.85 sigma
        self.assertTrue(4.7 < tension["tension_significance_sigma"] < 5.1)

        # Null hypothesis p-value < 1.0e-5
        self.assertLess(tension["p_value_gaussian"], 1.0e-5)

        # Gravitational wave standard sirens required for 1% resolution: N >= 50
        self.assertGreaterEqual(tension["gw_standard_sirens_required_for_1pct"], 50)

        # Boundary condition check
        with self.assertRaises(ValueError):
            hubble_tension_analysis(sigma_early=-0.5)

    def test_inflation_starobinsky_observables(self):
        """Property 5: Verify Starobinsky R^2 inflation observables match CMB constraints and LiteBIRD targets."""
        inf = inflation_dynamics(n_efolds=60.0, model="starobinsky")

        # Scalar spectral index n_s = 1 - 2/60 = 0.9667
        self.assertAlmostEqual(inf["scalar_spectral_index_ns"], 29.0 / 30.0, places=4)
        self.assertTrue(0.960 < inf["scalar_spectral_index_ns"] < 0.975)

        # Tensor-to-scalar ratio r = 12 / 60^2 = 0.00333
        expected_r = 12.0 / 3600.0
        self.assertAlmostEqual(inf["tensor_to_scalar_ratio_r"], expected_r, places=5)

        # Tensor spectral tilt n_T = -r/8
        self.assertAlmostEqual(inf["tensor_spectral_index_nt"], -expected_r / 8.0, places=6)

        # Allowed by current BICEP/Keck 2021 bound (r < 0.032)
        self.assertFalse(inf["is_ruled_out_by_bicep"])

        # Fully testable by LiteBIRD target sensitivity (sigma(r) = 0.001)
        self.assertTrue(inf["is_testable_by_litebird"])

        # Boundary condition check
        with self.assertRaises(ValueError):
            inflation_dynamics(n_efolds=5.0)

    def test_cosmological_constant_discrepancy(self):
        """Property 6: Verify the 120-order-of-magnitude vacuum energy fine-tuning."""
        cc = cosmological_constant_discrepancy()

        # Observed dark energy density is positive and ~ 10^-10 J/m^3
        self.assertGreater(cc["rho_lambda_observed_j_m3"], 0.0)
        self.assertTrue(1.0e-10 < cc["rho_lambda_observed_j_m3"] < 1.0e-9)

        # Discrepancy between QFT Planck cutoff vacuum energy and observation >= 120 orders of magnitude
        self.assertGreaterEqual(cc["log10_discrepancy_orders_of_magnitude"], 120.0)

        # Dark energy equation of state consistent with w = -1
        self.assertAlmostEqual(cc["dark_energy_equation_of_state_w"], -1.03, places=2)

    def test_sakharov_baryogenesis_failure_audit(self):
        """Property 7: Verify Standard Model failure of Sakharov conditions 2 and 3."""
        audit = baryogenesis_sakharov_audit()

        # Condition 1 is satisfied in SM (sphalerons)
        self.assertTrue(audit["sakharov_condition_1"]["satisfied_in_sm"])

        # Condition 2 (CP violation) fails: deficit factor > 10^8
        self.assertFalse(audit["sakharov_condition_2"]["satisfied_in_sm"])
        self.assertGreater(audit["sakharov_condition_2"]["deficit_factor_vs_observed"], 1.0e8)

        # Condition 3 (Out of equilibrium) fails: m_H = 125.10 GeV > 75.0 GeV critical threshold
        self.assertFalse(audit["sakharov_condition_3"]["satisfied_in_sm"])
        self.assertGreater(
            audit["sakharov_condition_3"]["observed_higgs_mass_gev"],
            audit["sakharov_condition_3"]["critical_threshold_for_sfopt_gev"]
        )

    def test_master_open_problems_and_resolutions_taxonomy(self):
        """Property 8: Verify deliverable taxonomy of open problems, facilities, and quantitative thresholds."""
        problems = get_open_problems_and_resolutions()
        self.assertIsInstance(problems, list)
        self.assertGreaterEqual(len(problems), 8)

        required_keys = [
            "id",
            "name",
            "epistemic_status",
            "unexplained",
            "resolving_observation",
            "target_facility",
            "quantitative_threshold"
        ]

        for prob in problems:
            for key in required_keys:
                self.assertIn(key, prob)
                self.assertIsInstance(prob[key], str)
                self.assertTrue(len(prob[key]) > 0)

        # Spot check specific critical facilities and thresholds
        problem_names = [p["name"] for p in problems]
        self.assertIn("Initial Spacetime Singularity", problem_names)
        self.assertIn("Baryon Asymmetry of the Universe (BAU)", problem_names)
        self.assertIn("The Hubble Tension (Early vs Late Universe Expansion Rate)", problem_names)
        self.assertIn("Primordial Lithium-7 Depletion Anomaly (Spite Plateau)", problem_names)


if __name__ == "__main__":
    unittest.main(verbosity=2)
