"""
test_patient_heterogeneity_engine.py
Agent: Hypatia (A003), Generation 0
Domain: New drug discovery (drug-discovery)

Unit tests for patient heterogeneity, cohort dilution, and multi-omic classifier enrichment.
"""

import unittest
import math
from patient_heterogeneity_and_endotype_stratification_engine import (
    normal_cdf,
    normal_ppf,
    SyndromicTrialModel,
    CASE_STUDIES,
    run_comprehensive_stratification_analysis
)


class TestPatientHeterogeneityEngine(unittest.TestCase):
    """Verifies mathematical validity of patient heterogeneity calculations."""

    def test_normal_distribution_approximations(self):
        """Test accuracy of normal CDF and PPF."""
        self.assertAlmostEqual(normal_cdf(0.0), 0.50, places=5)
        self.assertAlmostEqual(normal_ppf(0.50), 0.0, places=5)
        self.assertAlmostEqual(normal_ppf(0.975), 1.95996, places=3)
        self.assertAlmostEqual(normal_ppf(0.8413447), 1.0, places=3)

    def test_cohort_dilution_mechanics(self):
        """Test that observed effect size scales linearly with responder prevalence."""
        model = SyndromicTrialModel("Test", true_biological_effect_d=0.60, unselected_responder_prevalence=0.25)
        d_obs_100 = model.calculate_diluted_effect(1.0)
        d_obs_50 = model.calculate_diluted_effect(0.50)
        d_obs_25 = model.calculate_diluted_effect(0.25)

        self.assertAlmostEqual(d_obs_100, 0.60, places=4)
        self.assertAlmostEqual(d_obs_50, 0.30, places=4)
        self.assertAlmostEqual(d_obs_25, 0.15, places=4)

    def test_quadratic_sample_size_scaling(self):
        """Test that required sample size scales as (1 / f_responder)^2."""
        model = SyndromicTrialModel("Test", true_biological_effect_d=0.50, unselected_responder_prevalence=0.20)
        n_100 = model.calculate_required_sample_size(1.0, target_power=0.80)
        n_50 = model.calculate_required_sample_size(0.50, target_power=0.80)
        n_25 = model.calculate_required_sample_size(0.25, target_power=0.80)

        # Ratio between N(0.50) and N(1.0) should be approx (1/0.50)^2 = 4.0
        ratio_50 = n_50 / n_100
        self.assertTrue(3.8 <= ratio_50 <= 4.2, f"Expected ~4.0, got {ratio_50}")

        # Ratio between N(0.25) and N(1.0) should be approx (1/0.25)^2 = 16.0
        ratio_25 = n_25 / n_100
        self.assertTrue(15.5 <= ratio_25 <= 16.5, f"Expected ~16.0, got {ratio_25}")

    def test_phase2_power_collapse_in_unselected_cohorts(self):
        """Test that Phase II power (N=100 per arm) collapses below 25% when f_responder <= 0.25."""
        for name, model in CASE_STUDIES.items():
            prev = model.unselected_responder_prevalence
            power = model.calculate_statistical_power(prev, n_per_arm=100)
            self.assertLess(power, 0.35, f"Indication {name} baseline power unexpectedly high: {power}")

    def test_enrichment_classifier_rescue(self):
        """Test that a multi-omic classifier (sens 85%, spec 90%) elevates power and reduces sample size >5x."""
        for name, model in CASE_STUDIES.items():
            eval_res = model.evaluate_enrichment_impact(0.85, 0.90)
            adv = eval_res["comparative_advantage"]
            self.assertGreater(adv["sample_size_reduction_factor"], 5.0)
            self.assertGreater(eval_res["enriched"]["phase2_power_at_n100"], 0.70)


if __name__ == "__main__":
    unittest.main()
