"""
test_krishna_mahabharata_linguistic_ballistics_and_diffusion_engine.py

Unit test suite for krishna_mahabharata_linguistic_ballistics_and_diffusion_engine.py.
Verifies linguistic morphosyntax stratigraphy, Pan-Eurasian epigraphic diffusion,
PGW iron ballistics, cross-tradition stemmatics, and 4-hypothesis Bayesian adjudication.

Authors: Kepler (A001), Swarm Research Agent (Gen 0)
Workspace: D:/AgentSwarm/arena/world
"""

import unittest
from krishna_mahabharata_linguistic_ballistics_and_diffusion_engine import (
    StrictEpistemicCategory,
    LinguisticStratigraphyAndPhilologyEngine,
    PanEurasianEpigraphicDiffusionEngine,
    IronAgeBallisticsAndArchaeoMetallurgyEngine,
    CrossTraditionStemmaticLikelihoodEngine,
    MultiHypothesisEpistemicAdjudicationEngine,
    run_full_epistemic_analysis
)


class TestLinguisticStratigraphyAndPhilologyEngine(unittest.TestCase):
    def test_parva_profiles_structure(self):
        profiles = LinguisticStratigraphyAndPhilologyEngine.PARVA_LINGUISTIC_PROFILES
        self.assertEqual(len(profiles), 18)
        self.assertIn("Bhisma_Parva", profiles)
        self.assertIn("Santi_Parva", profiles)

    def test_archaic_features_count(self):
        features = LinguisticStratigraphyAndPhilologyEngine.ARCHAIC_VEDIC_FEATURES
        self.assertGreaterEqual(len(features), 5)
        for f in features:
            self.assertIn("feature", f)
            self.assertIn("stratum", f)

    def test_textual_stratigraphy_evaluation(self):
        res = LinguisticStratigraphyAndPhilologyEngine.evaluate_textual_stratigraphy()
        self.assertGreater(res["total_verses_analyzed"], 80000)
        self.assertGreater(res["war_core_vedicisms_per_k"], 25.0)
        self.assertLess(res["didactic_vedicisms_per_k"], 10.0)
        self.assertGreater(res["vedicism_enrichment_ratio"], 4.0)
        self.assertLess(res["war_core_paninian_regularity"], res["didactic_paninian_regularity"])
        self.assertIn("philological_inference", res)


class TestPanEurasianEpigraphicDiffusionEngine(unittest.TestCase):
    def test_epigraphic_corpus_structure(self):
        corpus = PanEurasianEpigraphicDiffusionEngine.EPIGRAPHIC_CORPUS
        self.assertEqual(len(corpus), 7)
        for record in corpus:
            self.assertEqual(record["epistemic_status"], StrictEpistemicCategory.PRIMARY_DATA)
            self.assertIn("distance_from_mathura_km", record)
            self.assertIn("artifact_type", record)

    def test_spatial_diffusion_metrics(self):
        metrics = PanEurasianEpigraphicDiffusionEngine.calculate_spatial_diffusion_metrics()
        self.assertEqual(metrics["origin_epicenter"], "Mathura (Surasena heartland)")
        self.assertEqual(metrics["maximum_attested_radius_km"], 1420.0)
        self.assertGreater(metrics["diffusion_velocity_km_per_century"], 200.0)
        self.assertEqual(len(metrics["uttarapatha_attestations"]), 2)
        self.assertEqual(len(metrics["dakshinapatha_attestations"]), 4)


class TestIronAgeBallisticsAndArchaeoMetallurgyEngine(unittest.TestCase):
    def test_metallurgical_parameters(self):
        pgw = IronAgeBallisticsAndArchaeoMetallurgyEngine.PGW_METALLURGY
        self.assertEqual(pgw["epistemic_status"], StrictEpistemicCategory.PRIMARY_DATA)
        self.assertLess(pgw["carbon_content_percent"][1], 0.35)

    def test_celestial_astra_demarcation(self):
        astras = IronAgeBallisticsAndArchaeoMetallurgyEngine.CELESTIAL_ASTRA_DEMARCATION
        self.assertIn("Brahmastra", astras)
        self.assertIn("Narayanastra", astras)
        self.assertIn("Pramohanastra", astras)
        self.assertEqual(astras["Brahmastra"]["epistemic_status"], StrictEpistemicCategory.DEVOTIONAL_CLAIM)
        self.assertEqual(astras["Pramohanastra"]["epistemic_status"], StrictEpistemicCategory.SCHOLARLY_CONSENSUS)

    def test_arrow_kinematics(self):
        kinematics = IronAgeBallisticsAndArchaeoMetallurgyEngine.calculate_arrow_kinematics()
        self.assertGreater(kinematics["arrow_kinetic_energy_joules"], 50.0)
        self.assertGreater(kinematics["launch_velocity_mps"], 50.0)
        self.assertTrue(kinematics["penetrates_rawhide_quilted_cuirass"])
        self.assertTrue(kinematics["penetrates_iron_scale_mail_at_point_blank"])
        self.assertGreater(kinematics["estimated_penetration_tissue_cm"], 20.0)


class TestCrossTraditionStemmaticLikelihoodEngine(unittest.TestCase):
    def test_biographical_kernels(self):
        kernels = CrossTraditionStemmaticLikelihoodEngine.BIOGRAPHICAL_KERNELS
        self.assertEqual(len(kernels), 6)
        for k in kernels:
            self.assertTrue(k["independent_concordance"])
            self.assertFalse(k["theological_advantage"])

    def test_stemmatic_likelihood_calculation(self):
        res = CrossTraditionStemmaticLikelihoodEngine.calculate_stemmatic_likelihood()
        self.assertEqual(res["total_biographical_kernels_analyzed"], 6)
        self.assertEqual(res["concordant_across_all_three_traditions"], 6)
        self.assertLess(res["joint_probability_independent_fabrication"], 1e-7)
        self.assertGreater(res["bayes_factor_in_favor_of_history"], 1e7)


class TestMultiHypothesisEpistemicAdjudicationEngine(unittest.TestCase):
    def test_hypotheses_and_evidence_vectors(self):
        hypotheses = MultiHypothesisEpistemicAdjudicationEngine.HYPOTHESES
        self.assertEqual(len(hypotheses), 4)
        vectors = MultiHypothesisEpistemicAdjudicationEngine.EVIDENCE_VECTORS
        self.assertEqual(len(vectors), 10)

    def test_falsification_criteria(self):
        criteria = MultiHypothesisEpistemicAdjudicationEngine.FALSIFICATION_CRITERIA_FOR_H4
        self.assertEqual(len(criteria), 4)
        for c in criteria:
            self.assertIn("criterion", c)
            self.assertIn("impact", c)

    def test_bayesian_posterior_adjudication(self):
        res = MultiHypothesisEpistemicAdjudicationEngine.calculate_bayesian_posteriors()
        self.assertEqual(res["favored_hypothesis"], "H4_Stratified_Historical_Nucleus")
        self.assertGreater(res["posterior_probability_h4"], 0.999)
        self.assertLess(res["posterior_probability_h1_mythicism"], 1e-5)
        self.assertLess(res["posterior_probability_h2_literalism"], 1e-10)


class TestFullEpistemicAnalysis(unittest.TestCase):
    def test_run_full_epistemic_analysis(self):
        full = run_full_epistemic_analysis()
        self.assertIn("stratigraphy", full)
        self.assertIn("diffusion", full)
        self.assertIn("ballistics", full)
        self.assertIn("stemmatics", full)
        self.assertIn("bayesian", full)


if __name__ == "__main__":
    unittest.main()
