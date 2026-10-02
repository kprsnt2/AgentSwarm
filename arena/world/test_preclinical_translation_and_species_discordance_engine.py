"""
test_preclinical_translation_and_species_discordance_engine.py - Unit Tests
Agent: Hypatia (A003), Generation 0
"""

import unittest
from preclinical_translation_and_species_discordance_engine import (
    normal_cdf,
    normal_ppf,
    allometric_pk_scaling,
    bayesian_predictive_value,
    calculate_two_sample_power,
    fisher_exact_2x2,
    PreclinicalTranslationModel
)

class TestPreclinicalTranslationEngine(unittest.TestCase):
    def test_normal_distribution_functions(self):
        self.assertAlmostEqual(normal_cdf(0.0), 0.50, places=5)
        self.assertAlmostEqual(normal_ppf(0.50), 0.0, places=5)
        self.assertAlmostEqual(normal_ppf(0.975), 1.95996, places=3)

    def test_allometric_scaling_principles(self):
        pk = allometric_pk_scaling(bw_mouse_kg=0.02, bw_human_kg=70.0)
        # Half-life scales as (70/0.02)^0.25 = 3500^0.25 = 7.69
        self.assertAlmostEqual(pk["half_life_ratio_human_to_mouse"], (70.0 / 0.02)**0.25, places=2)
        self.assertGreater(pk["t_half_human_hr"], pk["t_half_mouse_hr"])
        # Mouse requires dramatically higher Cmax/Cmin ratio at 12h
        self.assertGreater(pk["cmax_cmin_ratio_mouse_12h"], pk["cmax_cmin_ratio_human_12h"])
        self.assertGreater(pk["peak_exposure_penalty_mouse"], 10.0)

    def test_bayesian_predictive_values(self):
        # When prevalence is 10%, a test with Sens=0.50, Spec=0.68 has high FDR
        rodent = bayesian_predictive_value(sensitivity=0.50, specificity=0.68, prevalence=0.10)
        self.assertLess(rodent["ppv"], 0.20)
        self.assertGreater(rodent["false_discovery_rate"], 0.80)

        # Human MPS with Sens=0.87, Spec=0.98 has high PPV
        mps = bayesian_predictive_value(sensitivity=0.87, specificity=0.98, prevalence=0.10)
        self.assertGreater(mps["ppv"], 0.80)
        self.assertLess(mps["false_discovery_rate"], 0.20)

    def test_adjudication_trial_statistical_power(self):
        model = PreclinicalTranslationModel()
        trial = model.evaluate_clinical_adjudication_trial(n_per_arm=90)
        self.assertGreater(trial["statistical_power"], 0.90)
        self.assertGreater(trial["odds_ratio"], 3.0)
        self.assertLess(trial["fisher_p_value"], 0.001)

    def test_fisher_exact_symmetry_and_values(self):
        odds, p = fisher_exact_2x2(52, 38, 26, 64)
        self.assertAlmostEqual(odds, (52 * 64) / (38 * 26), places=2)
        self.assertLess(p, 0.001)

if __name__ == "__main__":
    unittest.main()
