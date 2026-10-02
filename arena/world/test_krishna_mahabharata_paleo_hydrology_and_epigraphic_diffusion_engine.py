"""
test_krishna_mahabharata_paleo_hydrology_and_epigraphic_diffusion_engine.py

Unit test suite for krishna_mahabharata_paleo_hydrology_and_epigraphic_diffusion_engine.py.
Verifies linguistic stratigraphy, paleo-hydrology of Sarasvati/Vinasana, pan-Indic epigraphic diffusion,
chariot biomechanics (Sanauli vs PGW), and 10D Bayesian meta-adjudication.
"""

import unittest
import math
from krishna_mahabharata_paleo_hydrology_and_epigraphic_diffusion_engine import (
    EpistemicCategory,
    LinguisticStratigraphyEngine,
    PaleoHydrologySarasvatiEngine,
    PanIndicEpigraphicDiffusionEngine,
    ChariotKinematicsAndBiomechanicsEngine,
    Bayesian10DAdjudicationMetaEngine,
    run_full_epistemic_pipeline
)


class TestLinguisticStratigraphyEngine(unittest.TestCase):
    def test_strata_data_integrity(self):
        data = LinguisticStratigraphyEngine.STRATA_DATA
        self.assertIn("Jaya", data)
        self.assertIn("Bharata", data)
        self.assertIn("Mahabharata_Final", data)
        self.assertEqual(data["Jaya"]["verse_count"], 8800)
        self.assertEqual(data["Bharata"]["verse_count"], 24000)
        self.assertEqual(data["Mahabharata_Final"]["verse_count"], 100000)

    def test_metallurgical_lexicon(self):
        lex = LinguisticStratigraphyEngine.METALLURGICAL_LEXICON
        self.assertEqual(len(lex), 3)
        terms = [item["term"] for item in lex]
        self.assertIn("ayas", terms)
        self.assertIn("karsnayasa / syamayasa", terms)
        self.assertIn("tiksnayasa", terms)
        for item in lex:
            self.assertEqual(item["category"], EpistemicCategory.PRIMARY_TEXT)

    def test_linguistic_decay_and_growth(self):
        metrics = LinguisticStratigraphyEngine.calculate_linguistic_decay_and_growth()
        self.assertEqual(metrics["total_redaction_span_years"], 1300)
        self.assertGreater(metrics["archaic_verbal_decay_constant_per_year"], 0.0)
        self.assertGreater(metrics["compound_length_expansion_factor"], 3.0)
        self.assertGreater(metrics["tristubh_to_sloka_shift_ratio"], 10.0)


class TestPaleoHydrologySarasvatiEngine(unittest.TestCase):
    def test_chrono_hydrology_stages(self):
        stages = PaleoHydrologySarasvatiEngine.CHRONO_HYDROLOGY_STAGES
        self.assertEqual(len(stages), 3)
        self.assertGreater(stages[0]["discharge_peak_m3_per_s"], 2000.0)
        self.assertLess(stages[2]["discharge_peak_m3_per_s"], 200.0)

    def test_vinasana_coordinates(self):
        coords = PaleoHydrologySarasvatiEngine.VINASANA_GEOGRAPHIC_COORDINATES
        self.assertAlmostEqual(coords["latitude_deg"], 29.53, delta=0.5)
        self.assertIn("Mahabharata 9.36.1-3", coords["salya_parva_reference"])
        self.assertIn("PB 25.10.16", coords["pancavimsa_brahmana_ref"])

    def test_paleo_hydrology_concordance(self):
        res = PaleoHydrologySarasvatiEngine.evaluate_paleo_hydrological_concordance()
        self.assertTrue(res["vinasana_textual_geomorphic_agreement"])
        self.assertGreater(res["flow_reduction_percentage"], 90.0)
        self.assertEqual(res["chronological_bracket_bce"], "1000 - 850 BCE")


class TestPanIndicEpigraphicDiffusionEngine(unittest.TestCase):
    def test_epigraphic_sites_count(self):
        sites = PanIndicEpigraphicDiffusionEngine.EPIGRAPHIC_SITES
        self.assertEqual(len(sites), 9)
        # All sites must be classified as PRIMARY_TEXT
        for s in sites:
            self.assertEqual(s["category"], EpistemicCategory.PRIMARY_TEXT)

    def test_diffusion_kinetics(self):
        kinetics = PanIndicEpigraphicDiffusionEngine.calculate_diffusion_kinetics()
        self.assertEqual(kinetics["focal_epicenter"], "Mathura / Surasena (Yamuna basin)")
        self.assertGreater(kinetics["max_epigraphic_diffusion_radius_km"], 1200.0)
        self.assertGreater(kinetics["effective_propagation_speed_km_per_year"], 1.5)
        self.assertTrue(kinetics["all_primary_attestations"])


class TestChariotKinematicsAndBiomechanicsEngine(unittest.TestCase):
    def test_rotational_inertia(self):
        i_sanauli = ChariotKinematicsAndBiomechanicsEngine.calculate_rotational_inertia(
            ChariotKinematicsAndBiomechanicsEngine.SANAULI_CART
        )
        i_pgw = ChariotKinematicsAndBiomechanicsEngine.calculate_rotational_inertia(
            ChariotKinematicsAndBiomechanicsEngine.PGW_WAR_CHARIOT
        )
        # Sanauli solid wheel should have significantly higher rotational inertia than PGW spoked wheel
        self.assertGreater(i_sanauli, i_pgw * 2.0)

    def test_dynamics_evaluation(self):
        dyn = ChariotKinematicsAndBiomechanicsEngine.evaluate_dynamics(tractive_torque_nm=120.0, turn_radius_m=10.0)
        self.assertGreater(dyn["pgw_acceleration_advantage_factor"], 2.0)
        self.assertGreater(dyn["pgw_stability_margin_factor"], 1.2)
        self.assertGreater(dyn["pgw"]["critical_rollover_speed_km_h"], dyn["sanauli"]["critical_rollover_speed_km_h"])


class TestBayesian10DAdjudicationMetaEngine(unittest.TestCase):
    def test_prior_sum(self):
        priors = Bayesian10DAdjudicationMetaEngine.PRIORS
        self.assertAlmostEqual(sum(priors.values()), 1.0, places=5)

    def test_joint_posteriors(self):
        res = Bayesian10DAdjudicationMetaEngine.calculate_joint_posteriors()
        posteriors = res["posteriors"]
        self.assertAlmostEqual(sum(posteriors.values()), 1.0, places=5)
        self.assertGreater(posteriors["H4_PGW_Nucleus_1000BCE"], 0.999)
        self.assertEqual(res["winning_hypothesis"], "H4_PGW_Nucleus_1000BCE")
        # Check Bayes factors are astronomically decisive
        bfs = res["bayes_factors"]
        self.assertGreater(bfs["BF_H4_vs_H1_Solar_Myth"], 1e15)
        self.assertGreater(bfs["BF_H4_vs_H2_Literal_3102BCE"], 1e25)
        self.assertGreater(bfs["BF_H4_vs_H3_Sanauli_1900BCE"], 1e8)
        self.assertGreater(bfs["BF_H4_vs_H5_Late_Hellenistic_300BCE"], 1e10)


class TestFullEpistemicPipeline(unittest.TestCase):
    def test_pipeline_run(self):
        report = run_full_epistemic_pipeline()
        self.assertIn("linguistic_stratigraphy", report)
        self.assertIn("paleo_hydrology", report)
        self.assertIn("epigraphic_diffusion", report)
        self.assertIn("chariot_biomechanics", report)
        self.assertIn("bayesian_10d_meta_adjudication", report)


if __name__ == "__main__":
    unittest.main()
