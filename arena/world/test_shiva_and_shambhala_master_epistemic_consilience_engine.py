"""
test_shiva_and_shambhala_master_epistemic_consilience_engine.py

Comprehensive Unit Test Suite for shiva_and_shambhala_master_epistemic_consilience_engine.py.
Verifies all mathematical models, Bayesian posteriors, epigraphic metrics,
Shambhala taxonomy, and protocol safety guardrails.
"""

import unittest
from shiva_and_shambhala_master_epistemic_consilience_engine import (
    EpistemicCategory,
    OnticMode,
    ShambhalaDomain,
    ProtocolViolationError,
    ProtocolSafetyGuard,
    ShivaStratigraphyAndEuhemerismEngine,
    ShambhalaEmpiricalTaxonomyEngine,
    MasterEpistemicConsilienceEngine,
)


class TestMasterEpistemicConsilienceEngine(unittest.TestCase):

    def setUp(self):
        self.engine = MasterEpistemicConsilienceEngine()

    def test_protocol_safety_guard_violations(self):
        # 1. Trapping scripture as laboratory physics
        with self.assertRaises(ProtocolViolationError):
            ProtocolSafetyGuard.validate_claim("The Tantra is laboratory physics that proves energy conservation.")

        with self.assertRaises(ProtocolViolationError):
            ProtocolSafetyGuard.validate_claim("Using scripture as laboratory data.")

        # 2. Trapping absence of evidence as proof of falsehood
        with self.assertRaises(ProtocolViolationError):
            ProtocolSafetyGuard.validate_claim("Unobserved pure land proves consciousness does not exist.")

        with self.assertRaises(ProtocolViolationError):
            ProtocolSafetyGuard.validate_claim("Lack of bones proves Shiva is a lie.")

    def test_protocol_safety_guard_valid_claims(self):
        # Legitimate scholarly and historical-textual claims should not raise exceptions
        try:
            ProtocolSafetyGuard.validate_claim("The Rigveda mentions Rudra as an archer deity.")
            ProtocolSafetyGuard.validate_claim("The archaeological mound at Sambhal exhibits PGW pottery.")
            ProtocolSafetyGuard.validate_claim("Abhinavagupta formulates the Pratyabhijna philosophy of consciousness.")
        except ProtocolViolationError:
            self.fail("ProtocolSafetyGuard raised an exception on a legitimate scholarly statement.")

    def test_bayesian_euhemerism_differentiation(self):
        shiva_eng = self.engine.shiva_engine

        p_shiva = shiva_eng.compute_bayesian_euhemerism_posterior("Lord Shiva")
        p_krishna = shiva_eng.compute_bayesian_euhemerism_posterior("Krishna (Vasudeva)")
        p_caesar = shiva_eng.compute_bayesian_euhemerism_posterior("Julius Caesar")
        p_buddha = shiva_eng.compute_bayesian_euhemerism_posterior("Gautama Buddha")

        # Shiva has no mortal genealogy, no mortal parents, no mortal death site -> P(mortal) < 0.001
        self.assertLess(p_shiva, 0.001)

        # Figures with documented mortal genealogies and lifespans have high posteriors
        self.assertGreater(p_krishna, 0.90)
        self.assertGreater(p_buddha, 0.95)
        self.assertGreater(p_caesar, 0.99)

    def test_epigraphic_network_metrics(self):
        shiva_eng = self.engine.shiva_engine
        arc = shiva_eng.calculate_epigraphic_arc_distance()

        self.assertGreaterEqual(arc["total_sites_indexed"], 8)
        self.assertGreater(arc["max_distance_km"], 6000.0)

        # Verify coordinates of all sites are valid
        for site in shiva_eng.epigraphic_network:
            self.assertGreaterEqual(site.latitude, -90.0)
            self.assertLessEqual(site.latitude, 90.0)
            self.assertGreaterEqual(site.longitude, -180.0)
            self.assertLessEqual(site.longitude, 180.0)
            self.assertTrue(len(site.language) > 0)
            self.assertTrue(len(site.deity_epithet) > 0)

    def test_shambhala_threefold_taxonomy(self):
        shambhala_eng = self.engine.shambhala_engine
        facets = shambhala_eng.facets
        self.assertEqual(len(facets), 3)

        # Facet 1: Puranic Sambhal (UP)
        puranic = next(f for f in facets if f.domain == ShambhalaDomain.PURANIC_SAMBHAL_UP)
        self.assertTrue(puranic.physical_surface_presence)
        self.assertIsNotNone(puranic.geographic_coordinates)
        lat, lon = puranic.geographic_coordinates
        self.assertAlmostEqual(lat, 28.5833, places=2)
        self.assertAlmostEqual(lon, 78.5667, places=2)

        # Facet 2: Kalachakra Shambhala
        kalachakra = next(f for f in facets if f.domain == ShambhalaDomain.KALACHAKRA_TANTRA)
        self.assertFalse(kalachakra.physical_surface_presence)
        self.assertIn("heart", kalachakra.yogic_symbolic_meaning.lower())
        self.assertIn("avadhūtī", kalachakra.yogic_symbolic_meaning)

        # Facet 3: Occult / Theosophical
        occult = next(f for f in facets if f.domain == ShambhalaDomain.OCCULT_THEOSOPHICAL)
        self.assertFalse(occult.physical_surface_presence)
        self.assertIn("confabulation", occult.scholarly_consensus_verdict.lower())

    def test_satellite_geodesy(self):
        shambhala_eng = self.engine.shambhala_engine
        geodesy = shambhala_eng.calculate_satellite_geodetic_coverage()

        self.assertEqual(geodesy["geodetic_blind_spots_km2"], 0.0)
        self.assertEqual(geodesy["eurasian_landmass_coverage_pct"], 100.0)
        self.assertEqual(geodesy["p_hidden_physical_kingdom_earth_crust"], 0.0)

    def test_evidence_corpus_categorization_and_standards(self):
        # Must strictly separate Primary Text, Scholarly Consensus, and Devotional Claim
        all_evidence = self.engine.shiva_engine.evidence_corpus + self.engine.shambhala_engine.evidence_corpus
        categories_found = {item.category for item in all_evidence}

        self.assertIn(EpistemicCategory.PRIMARY_TEXT, categories_found)
        self.assertIn(EpistemicCategory.SCHOLARLY_CONSENSUS, categories_found)
        self.assertIn(EpistemicCategory.DEVOTIONAL_CLAIM, categories_found)

        for item in all_evidence:
            self.assertGreater(len(item.citation), 0)
            self.assertGreater(len(item.description), 0)
            self.assertGreaterEqual(item.empirical_verifiability, 0.0)
            self.assertLessEqual(item.empirical_verifiability, 1.0)
            self.assertGreaterEqual(item.devotional_salience, 0.0)
            self.assertLessEqual(item.devotional_salience, 1.0)
            self.assertGreaterEqual(item.scholarly_confidence, 0.0)
            self.assertLessEqual(item.scholarly_confidence, 1.0)

    def test_master_consilience_report_synthesis(self):
        report = self.engine.generate_master_consilience_report()

        self.assertIn("shiva_bayesian_euhemerism_posterior", report)
        self.assertIn("krishna_bayesian_euhemerism_posterior", report)
        self.assertIn("epigraphic_arc_max_km", report)
        self.assertIn("shambhala_physical_presence_p", report)
        self.assertIn("puranic_sambhal_present", report)

        self.assertTrue(report["puranic_sambhal_present"])
        self.assertEqual(report["shambhala_physical_presence_p"], 0.0)
        self.assertLess(report["shiva_bayesian_euhemerism_posterior"], 0.001)


if __name__ == "__main__":
    unittest.main()
