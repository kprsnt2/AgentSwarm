"""
test_krishna_mahabharata_epigraphic_logistics_engine.py
========================================================
Comprehensive unit test suite for:
1. Epigraphic and numismatic corpus of Krishna-Vasudeva & Vrishni heroes.
2. Battlefield logistics, spatial footprint, and biomass/water requirements of the 18 Akshauhinis.
3. Iron Age demographic calibration and symbolic inflation factor.
4. Archaeoastronomy critical analysis and 3102 BCE planetary scatter quantification.
5. Gita textual stratigraphy and philosophical development.
6. 10-Dimensional Bayesian joint evaluation.
"""

import unittest
import math
from krishna_mahabharata_epigraphic_logistics_engine import (
    EpigraphicNumismaticCorpusEngine,
    BattlefieldLogisticsAttritionEngine,
    ArchaeoastronomyCriticalEngine,
    GitaStratigraphyEngine,
    GrandIntegratedEpistemicEvaluation
)

class TestKrishnaMahabharataEpigraphicLogisticsEngine(unittest.TestCase):

    def test_epigraphic_corpus_completeness(self):
        """Verify the catalog of primary pre-Christian and early CE epigraphy."""
        corpus = EpigraphicNumismaticCorpusEngine.get_corpus()
        self.assertGreaterEqual(len(corpus), 7)
        ids = [item["id"] for item in corpus]
        self.assertIn("AI_KHANOUM_COINS", ids)
        self.assertIn("BESNAGAR_HELIODORUS_PILLAR", ids)
        self.assertIn("GHOSUNDI_HATHIBADA", ids)
        self.assertIn("NANEGHAT_CAVE", ids)
        self.assertIn("MORA_WELL_INSCRIPTION", ids)

    def test_epigraphic_diffusion_analysis(self):
        """Test geographic and chronological diffusion metrics."""
        diff = EpigraphicNumismaticCorpusEngine.analyze_epigraphic_diffusion()
        self.assertEqual(diff["total_primary_records"], 7)
        self.assertGreater(diff["chronological_span_years"], 300)
        self.assertIn("Bactria", diff["geographic_coverage"])
        self.assertIn("Pancha-Vira Cult", diff["theological_stages_breakdown"])

    def test_heliodorus_scriptural_cross_link(self):
        """Verify the exact cross-reference between Besnagar pillar and Mahabharata 5.43.22."""
        corpus = EpigraphicNumismaticCorpusEngine.get_corpus()
        helio = next(item for item in corpus if item["id"] == "BESNAGAR_HELIODORUS_PILLAR")
        self.assertIn("Mahabharata 5.43.22", helio["scriptural_cross_link"])
        self.assertIn("Sanatsujatiya", helio["scriptural_cross_link"])
        self.assertIn("Dama", helio["scriptural_cross_link"])

    def test_akshauhini_decomposition(self):
        """Test mathematical decomposition of 1 and 18 Akshauhinis."""
        decomp_1 = BattlefieldLogisticsAttritionEngine.decompose_akshauhinis(1.0)
        self.assertEqual(decomp_1["rathas"], 21870)
        self.assertEqual(decomp_1["gajas"], 21870)
        self.assertEqual(decomp_1["cavalry_horses"], 65610)
        self.assertEqual(decomp_1["infantry_soldiers"], 109350)
        self.assertEqual(decomp_1["combatants_nominal"], 218700)

        decomp_18 = BattlefieldLogisticsAttritionEngine.decompose_akshauhinis(18.0)
        self.assertEqual(decomp_18["rathas"], 393660)
        self.assertEqual(decomp_18["gajas"], 393660)
        self.assertEqual(decomp_18["cavalry_horses"], 1180980)
        self.assertEqual(decomp_18["infantry_soldiers"], 1968300)
        self.assertEqual(decomp_18["combatants_nominal"], 3936600)
        self.assertEqual(decomp_18["total_human_personnel"], 4723920)

    def test_logistical_requirements_impossibility(self):
        """Verify that water, fodder, and spatial requirements exceed Iron Age carrying capacity."""
        reqs = BattlefieldLogisticsAttritionEngine.calculate_logistical_requirements(18.0, 18)
        self.assertFalse(reqs["is_physically_possible_in_iron_age"])

        # Daily water demand should exceed 100 million liters
        self.assertGreater(reqs["daily_water_demand_liters"], 1.5e8)

        # Total 18-day biomass should exceed 1 million metric tons
        self.assertGreater(reqs["total_18day_biomass_mt"], 1.0e6)

        # Tactical deployment area should exceed 1,000 km^2
        self.assertGreater(reqs["tactical_deployment_area_km2"], 1000.0)

    def test_iron_age_demographic_reality(self):
        """Test demographic realism and epic inflation factor."""
        demo = BattlefieldLogisticsAttritionEngine.evaluate_iron_age_demographic_reality()
        # Epic force represents > 100% of adult males in the subcontinent
        self.assertGreater(demo["epic_force_percentage_of_all_indian_males"], 100.0)
        # Realistic coalition warrior force ~6,500
        self.assertLess(demo["realistic_historical_force_size"], 15000)
        # Inflation factor > 500x
        self.assertGreater(demo["epic_inflation_factor"], 500.0)

    def test_planetary_scatter_3102bce(self):
        """Test quantification of planetary dispersion on 18 Feb 3102 BCE."""
        scatter = ArchaeoastronomyCriticalEngine.evaluate_planetary_scatter_3102bce()
        self.assertFalse(scatter["was_true_conjunction"])
        self.assertGreater(scatter["total_angular_span_deg"], 40.0)
        self.assertGreater(scatter["standard_deviation_deg"], 15.0)

    def test_astronomical_hypotheses_comparison(self):
        """Test comparison of 5561 BCE, 3102 BCE, 3067 BCE, and 950 BCE."""
        hyps = ArchaeoastronomyCriticalEngine.compare_astronomical_hypotheses()
        self.assertFalse(hyps["OAK_VARTAK_5561_BCE"]["is_tenable_historically"])
        self.assertFalse(hyps["ARYABHATA_3102_BCE"]["is_tenable_historically"])
        self.assertFalse(hyps["ACHAR_3067_BCE"]["is_tenable_historically"])
        self.assertTrue(hyps["SCHOLARLY_CONSENSUS_950_BCE"]["is_tenable_historically"])

    def test_gita_stratigraphy(self):
        """Test Gita stratigraphy and verse proportions."""
        strata = GitaStratigraphyEngine.get_strata()
        self.assertEqual(len(strata), 3)
        comp = GitaStratigraphyEngine.analyze_gita_composition()
        self.assertEqual(comp["total_estimated_verses"], 700)
        self.assertIn("Stratum I", comp["strata_proportions"])

    def test_10d_bayesian_evaluation(self):
        """Test 10-dimensional Bayesian joint likelihood and posterior convergence."""
        eval_res = GrandIntegratedEpistemicEvaluation.evaluate_all_epochs()
        self.assertEqual(eval_res["optimal_epoch"], "950_BCE")
        cand = eval_res["candidate_evaluations"]
        self.assertGreater(cand["950_BCE"]["posterior_probability"], 0.99)
        # Delta log-likelihood for 5561 BCE and 3102 BCE should be astronomical
        self.assertGreater(cand["5561_BCE"]["delta_log_likelihood_vs_950bce"], 5000.0)
        self.assertGreater(cand["3102_BCE"]["delta_log_likelihood_vs_950bce"], 1000.0)

if __name__ == "__main__":
    unittest.main()
