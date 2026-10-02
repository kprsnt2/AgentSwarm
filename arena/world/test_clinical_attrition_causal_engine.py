"""
test_clinical_attrition_causal_engine.py — Unit tests for clinical_attrition_causal_engine.py.
Verifies all mathematical, combinatorial, and empirical constants against published literature.
"""

import unittest
import math
from clinical_attrition_causal_engine import (
    log_factorial,
    log_comb,
    fisher_exact_2x2,
    normal_cdf,
    normal_ppf,
    BENCHMARK_MODELS,
    FAILURE_CAUSES,
    PfizerThreePillarsData,
    AstraZeneca5RImpact,
    GeneticStoppageParameters,
    compute_causal_target_vs_chemistry_burden,
    sample_size_for_hypothesis_h,
    bayesian_pipeline_progression
)

class TestClinicalAttritionCausalEngine(unittest.TestCase):

    def test_combinatorial_and_normal_math(self):
        """Verifies factorial, combinations, and normal inverse approximations."""
        self.assertAlmostEqual(log_factorial(0), 0.0, places=7)
        self.assertAlmostEqual(log_factorial(5), math.log(120), places=7)
        self.assertAlmostEqual(math.exp(log_comb(10, 3)), 120.0, places=5)
        self.assertAlmostEqual(math.exp(log_comb(26, 8)), 1562275.0, places=3)

        # Standard normal quantiles
        self.assertAlmostEqual(normal_cdf(0.0), 0.5, places=6)
        self.assertAlmostEqual(normal_cdf(1.95996), 0.975, places=3)
        self.assertAlmostEqual(normal_ppf(0.5), 0.0, places=6)
        self.assertAlmostEqual(normal_ppf(0.95), 1.64485, places=2)
        self.assertAlmostEqual(normal_ppf(0.90), 1.28155, places=2)

    def test_fisher_exact_pfizer_three_pillars(self):
        """Verifies Fisher's exact test on the Pfizer 44-program 3 Pillars dataset."""
        pfizer = PfizerThreePillarsData()
        res = pfizer.analyze_pillars()

        # Check raw counts
        self.assertEqual(pfizer.total_programs, 44)
        self.assertEqual(pfizer.three_pillars_advanced, 8)
        self.assertEqual(pfizer.three_pillars_failed, 6)
        self.assertEqual(pfizer.zero_partial_advanced, 0)
        self.assertEqual(pfizer.zero_partial_failed, 12)

        # Success rates
        self.assertAlmostEqual(res["p_success_three_pillars"], 8 / 14, places=4)
        self.assertEqual(res["p_success_zero_partial"], 0.0)

        # Fisher exact p-value must be < 0.005 (highly significant)
        self.assertLess(res["fisher_p_value"], 0.005)
        self.assertGreater(res["fisher_p_value"], 0.001)

        # Indeterminate mechanism fraction must match 43.18%
        self.assertAlmostEqual(res["indeterminate_fraction"], 19 / 44, places=4)

    def test_benchmark_models_wong_2019(self):
        """Verifies benchmark model parameters from Wong et al. 2019."""
        agg = BENCHMARK_MODELS["All_Indications_Aggregate"]
        self.assertAlmostEqual(agg.product_loa, 0.664 * 0.583 * 0.590, places=5)
        self.assertEqual(agg.headline_loa, 0.138)

        onc_nb = BENCHMARK_MODELS["Oncology_No_Biomarker"]
        self.assertAlmostEqual(onc_nb.product_loa, 0.280 * 0.174 * 0.336, places=5)
        self.assertEqual(onc_nb.headline_loa, 0.016)

        onc_b = BENCHMARK_MODELS["Oncology_With_Biomarker"]
        self.assertAlmostEqual(onc_b.product_loa, 0.435 * 0.388 * 0.636, places=5)
        self.assertEqual(onc_b.headline_loa, 0.107)

        # Biomarker lift in oncology is ~6.6x
        lift_onc = onc_b.headline_loa / onc_nb.headline_loa
        self.assertGreater(lift_onc, 6.0)
        self.assertLess(lift_onc, 7.0)

    def test_astrazeneca_5r_productivity(self):
        """Verifies AstraZeneca 5R framework impact reported in Morgan et al. 2018."""
        az = AstraZeneca5RImpact()
        res = az.productivity_multipliers()
        self.assertEqual(az.pre_5r_nomination_to_phase3, 0.04)
        self.assertEqual(az.post_5r_nomination_to_phase3, 0.19)
        self.assertAlmostEqual(res["portfolio_survival_multiplier"], 4.75, places=2)
        self.assertAlmostEqual(res["absolute_portfolio_gain_pp"], 15.0, places=1)

    def test_genetic_stoppage_parameters(self):
        """Verifies parameters from Razuvayevskaya et al. (Nature Genetics 2024)."""
        gen = GeneticStoppageParameters()
        self.assertEqual(gen.total_stopped_trials, 28561)
        self.assertEqual(gen.or_genetics_efficacy_all, 0.61)
        self.assertEqual(gen.or_genetics_efficacy_oncology, 0.53)
        self.assertEqual(gen.or_genetics_efficacy_non_onc, 0.75)
        self.assertEqual(gen.or_mouse_knockout_phenocopy, 0.70)
        self.assertEqual(gen.or_safety_pLOEUF_constrained, 1.50)
        self.assertEqual(gen.or_safety_pLI_intolerant, 1.40)
        self.assertEqual(gen.or_safety_tissue_enriched, 0.80)

        # Efficacy risk reduction should be 39%
        self.assertAlmostEqual(gen.efficacy_risk_reduction(), 39.0, places=1)

    def test_causal_target_vs_chemistry_decomposition(self):
        """Verifies causal decomposition of target biology vs compound chemistry."""
        res = compute_causal_target_vs_chemistry_burden()
        # Target biology (Efficacy + On-target toxicity) = 45% + 15% = 60%
        self.assertAlmostEqual(res["fraction_failures_target_biology"], 0.60, places=2)
        # Compound chemistry (ADMET + Off-target toxicity) = 12.5% + 15% = 27.5%
        self.assertAlmostEqual(res["fraction_failures_compound_chemistry"], 0.275, places=2)
        # Ratio should be ~2.18
        self.assertGreater(res["target_to_chemistry_ratio"], 2.0)
        self.assertLess(res["target_to_chemistry_ratio"], 2.5)

    def test_power_analysis_sample_size(self):
        """Verifies sample size calculation for testing Hypothesis H."""
        res80 = sample_size_for_hypothesis_h(power=0.80)
        res90 = sample_size_for_hypothesis_h(power=0.90)

        self.assertGreater(res90["n_classifiable_required"], res80["n_classifiable_required"])
        # Classifiable sample size for 90% power should be ~92
        self.assertGreaterEqual(res90["n_classifiable_required"], 85)
        self.assertLessEqual(res90["n_classifiable_required"], 100)

        # Total cohort accounting for 43% indeterminate should be ~160-170
        self.assertGreaterEqual(res90["total_cohort_size_required"], 150)
        self.assertLessEqual(res90["total_cohort_size_required"], 180)

    def test_bayesian_pipeline_progression(self):
        """Verifies multi-layer Bayesian pipeline lift."""
        res = bayesian_pipeline_progression(
            has_genetic_support=True,
            has_three_pillars=True,
            has_biomarker_selection=True
        )
        self.assertGreater(res["net_pipeline_lift_ratio"], 1.8)
        self.assertGreater(res["simulated_product_loa"], 0.40)

if __name__ == "__main__":
    unittest.main()
