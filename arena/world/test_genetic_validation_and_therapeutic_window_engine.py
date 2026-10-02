"""
test_genetic_validation_and_therapeutic_window_engine.py - Unit Test Suite
Agent: Hypatia (A003), Generation 0
"""

import unittest
import math
from genetic_validation_and_therapeutic_window_engine import (
    GENETIC_ATTRITION_BENCHMARKS,
    TargetTherapeuticWindow,
    normal_cdf,
    normal_ppf,
    calculate_proportional_hazards_power,
    analyze_genetic_paradox,
)


class TestGeneticValidationEngine(unittest.TestCase):
    """Test suite verifying quantitative derivations of genetic validation and therapeutic window bounds."""

    def test_genetic_transition_benchmarks(self):
        """Property 1: Human genetic support doubles clinical approval rate (Nelson 2015, King 2019)."""
        no_gen = GENETIC_ATTRITION_BENCHMARKS["No_Genetic_Support"]
        gen = GENETIC_ATTRITION_BENCHMARKS["Human_Genetic_Support"]

        # Check cumulative LoA
        self.assertAlmostEqual(no_gen.cumulative_loa, 0.0857, places=3)
        self.assertAlmostEqual(gen.cumulative_loa, 0.1695, places=3)

        # Enrichment ratio must be approximately 2.0x (1.9x to 2.2x)
        ratio = gen.cumulative_loa / no_gen.cumulative_loa
        self.assertGreaterEqual(ratio, 1.90)
        self.assertLessEqual(ratio, 2.30)

        # Crucially: Even with genetic support, cumulative clinical attrition exceeds 80%
        self.assertGreater(gen.cumulative_attrition, 0.80)
        self.assertLess(gen.cumulative_attrition, 0.85)

        # The primary rescue of genetic support occurs at Phase II -> Phase III transition
        ph2_diff = gen.phase2_to_phase3 - no_gen.phase2_to_phase3
        self.assertGreater(ph2_diff, 0.15)  # 44.5% vs 28.9%

    def test_therapeutic_window_mechanics(self):
        """Property 2: Therapeutic index calculation correctly demarcates viable vs non-viable targets."""
        # Clean target: Toxicity occupancy is 99% while efficacy occupancy is 80%
        clean = TargetTherapeuticWindow("CleanTarget", kd_nm=5.0, ec50_efficacy_occupancy=0.80, ec50_toxicity_occupancy=0.99)
        self.assertGreater(clean.therapeutic_index(), 10.0)
        self.assertTrue(clean.evaluate_clinical_viability()["is_clinically_viable"])

        # Toxic target: Toxicity threshold is 60% while efficacy requires 85%
        toxic = TargetTherapeuticWindow("ToxicTarget", kd_nm=10.0, ec50_efficacy_occupancy=0.85, ec50_toxicity_occupancy=0.60)
        # Required Cu for efficacy: 10 * (0.85 / 0.15) = 56.67 nM
        # Threshold Cu for toxicity: 10 * (0.60 / 0.40) = 15.00 nM
        # TI = 15.0 / 56.67 = 0.265 < 1.0
        self.assertLess(toxic.therapeutic_index(), 1.0)
        eval_toxic = toxic.evaluate_clinical_viability()
        self.assertFalse(eval_toxic["is_clinically_viable"])
        self.assertIn("Narrow Therapeutic Index", eval_toxic["failure_mode"])

    def test_bace1_paradox_case_study(self):
        """Property 3: BACE1 quantitative parameters reproduce clinical failure despite APP A673T genetics."""
        bace1 = TargetTherapeuticWindow(
            target_name="BACE1",
            kd_nm=10.0,
            ec50_efficacy_occupancy=0.85,
            ec50_toxicity_occupancy=0.65,
            genetic_loss_of_function_effect=0.40,
            substrate_pleiotropy_count=32,
        )
        res = bace1.evaluate_clinical_viability()
        self.assertFalse(res["is_clinically_viable"])
        self.assertLess(res["therapeutic_index"], 1.0)
        # Lifetime genetic suppression is 40%, but adult acute inhibition requires 85% -> 2.1x ratio
        self.assertAlmostEqual(res["dosage_ratio_acute_to_genetic"], 2.125, places=2)
        self.assertGreater(res["substrate_pleiotropy_count"], 25)

    def test_normal_distribution_functions(self):
        """Property 4: Normal CDF and inverse CDF (quantile) functions are exact."""
        self.assertAlmostEqual(normal_cdf(0.0), 0.50, places=5)
        self.assertAlmostEqual(normal_cdf(1.95996), 0.975, places=3)
        self.assertAlmostEqual(normal_cdf(-1.95996), 0.025, places=3)

        self.assertAlmostEqual(normal_ppf(0.50), 0.0, places=5)
        self.assertAlmostEqual(normal_ppf(0.975), 1.95996, places=3)
        self.assertAlmostEqual(normal_ppf(0.025), -1.95996, places=3)

    def test_proportional_hazards_power_derivation(self):
        """Property 5: Statistical power for clinical trial adheres to Schoenfeld derivation."""
        # For N=340 patients, HR=0.65, event_rate=0.75, alpha=0.05
        # Events = 255
        p = calculate_proportional_hazards_power(hr=0.65, n_patients=340, event_rate=0.75, alpha=0.05)
        self.assertEqual(p["n_patients"], 340)
        self.assertEqual(p["expected_events"], 255.0)
        self.assertGreater(p["statistical_power"], 0.90)  # Over 90% power
        self.assertLess(p["statistical_power"], 0.98)

    def test_comprehensive_analysis_payload(self):
        """Property 6: analyze_genetic_paradox returns complete structured data."""
        data = analyze_genetic_paradox()
        self.assertIn("transition_rates", data)
        self.assertIn("target_case_evaluations", data)
        self.assertIn("prospective_adjudication_trial_power", data)
        self.assertEqual(len(data["target_case_evaluations"]), 3)


if __name__ == "__main__":
    unittest.main()
