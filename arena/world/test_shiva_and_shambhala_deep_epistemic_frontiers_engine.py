"""
test_shiva_and_shambhala_deep_epistemic_frontiers_engine.py

Comprehensive Unit Test Suite for shiva_and_shambhala_deep_epistemic_frontiers_engine.py.
Verifies all epigraphic diffusion, satellite geodesy, Kalachakra chronology,
Sambhal archaeology, and protocol safety enforcement.
"""

import unittest
from shiva_and_shambhala_deep_epistemic_frontiers_engine import (
    EpistemicTier,
    OntologicalMode,
    ProtocolViolationType,
    ProtocolViolationException,
    PanEurasianShivaDiffusionAnalyzer,
    ShambhalaGeodeticSatelliteValidator,
    KalachakraEschatologicalEngine,
    SambhalUttarPradeshArchaeologyEngine,
    DeepFrontiersConsilienceEngine,
)


class TestShivaAndShambhalaDeepFrontiersEngine(unittest.TestCase):

    def setUp(self):
        self.engine = DeepFrontiersConsilienceEngine()

    def test_epigraphic_corpus_completeness(self):
        analyzer = self.engine.shiva_diffusion
        corpus = analyzer.get_corpus()
        self.assertGreaterEqual(len(corpus), 10)

        site_names = [rec.site_name for rec in corpus]
        self.assertTrue(any("Gudimallam" in s for s in site_names))
        self.assertTrue(any("Kushan" in s or "Balkh" in s for s in site_names))
        self.assertTrue(any("My Son" in s for s in site_names))
        self.assertTrue(any("Panjakent" in s for s in site_names))
        self.assertTrue(any("Prambanan" in s for s in site_names))
        self.assertTrue(any("Sdok Kok Thom" in s for s in site_names))

        for rec in corpus:
            self.assertEqual(rec.epistemic_tier, EpistemicTier.TIER_1_PRIMARY_MATERIAL_EPIGRAPHIC)

    def test_shiva_geographic_span_and_distance(self):
        span = self.engine.shiva_diffusion.calculate_geographic_span()
        self.assertGreater(span["max_great_circle_span_km"], 5000.0)
        self.assertLessEqual(span["min_latitude"], -7.0)
        self.assertGreaterEqual(span["max_latitude"], 39.0)
        self.assertEqual(span["total_primary_sites"], 10)

    def test_linguistic_dispersion_entropy(self):
        entropy = self.engine.shiva_diffusion.compute_epigraphic_apotheosis_entropy()
        self.assertGreater(entropy, 0.85)
        self.assertLessEqual(entropy, 1.0)

    def test_geodetic_satellite_absence(self):
        validator = self.engine.shambhala_geodesy
        bounds = validator.calculate_textual_vs_physical_bounds()
        self.assertEqual(bounds["probability_of_unobserved_physical_empire"], 0.0)
        self.assertEqual(bounds["global_satellite_mapping_coverage_pct"], 100.0)
        self.assertEqual(bounds["unmapped_territory_sq_km"], 0.0)
        self.assertGreater(bounds["projected_surface_area_sq_km"], 500000.0)

    def test_kalachakra_chronology_and_rabjung(self):
        kalachakra = self.engine.kalachakra_engine
        chronology = kalachakra.get_chronology()
        self.assertEqual(chronology.start_year_ce, 1027)
        self.assertEqual(chronology.kalki_king_index, 25)
        self.assertEqual(chronology.prophesied_culmination_year_ce, 2424)

        cycles = kalachakra.calculate_rabjung_cycles(2424)
        self.assertEqual(cycles["total_years_elapsed"], 1397)
        self.assertEqual(cycles["complete_60_year_rabjung_cycles"], 23)
        self.assertEqual(cycles["current_rabjung_cycle_at_target"], 24)
        self.assertEqual(cycles["year_in_cycle"], 17)

    def test_vimalaprabha_allegorical_mapping(self):
        mapping = self.engine.kalachakra_engine.verify_vimalaprabha_allegory_mapping()
        self.assertIn("Raudra_Cakrin", mapping)
        self.assertIn("Shambhala_Army", mapping)
        self.assertIn("Mlecchas_Barbarian_Invaders", mapping)
        self.assertTrue("Bodhicitta" in mapping["Raudra_Cakrin"] or "Jnana" in mapping["Raudra_Cakrin"])
        self.assertTrue("Prana-Vayus" in mapping["Shambhala_Army"] or "winds" in mapping["Shambhala_Army"])

    def test_sambhal_up_strata(self):
        archaeology = self.engine.sambhal_archaeology
        strata = archaeology.get_strata()
        self.assertEqual(len(strata), 5)
        stratum_names = [s.stratum_name for s in strata]
        self.assertTrue(any("PGW" in s or "Iron Age" in s for s in stratum_names))
        self.assertTrue(any("NBPW" in s for s in stratum_names))
        self.assertTrue(any("Mughal" in s for s in stratum_names))

    def test_puranic_concordance(self):
        concordance = self.engine.sambhal_archaeology.evaluate_puranic_concordance()
        self.assertEqual(concordance["epistemic_verdict"], "PHYSICALLY PRESENT. The Puranic Sambhala is an authentic geographical settlement on Earth.")
        self.assertIn("28.58° N, 78.57° E", concordance["geographical_location"])

    def test_protocol_violation_scripture_as_lab_data(self):
        with self.assertRaises(ProtocolViolationException) as ctx:
            self.engine.enforce_protocol_safety("Perform laboratory test of Shiva using particle accelerator")
        self.assertEqual(ctx.exception.violation_type, ProtocolViolationType.SCRIPTURE_AS_LABORATORY_DATA)

    def test_protocol_violation_absence_of_evidence(self):
        with self.assertRaises(ProtocolViolationException) as ctx:
            self.engine.enforce_protocol_safety("The absence of skeleton proves Shiva is fake and nonexistent")
        self.assertEqual(ctx.exception.violation_type, ProtocolViolationType.ABSENCE_OF_EVIDENCE_AS_PROOF_OF_FALSEHOOD)

    def test_deep_frontier_metrics(self):
        metrics = self.engine.calculate_deep_frontier_metrics()
        self.assertGreater(metrics["composite_deep_epistemic_rigor_index"], 0.95)
        self.assertEqual(metrics["shambhala_macro_empire_physical_prob"], 0.0)
        self.assertEqual(metrics["sambhal_up_archaeological_continuity"], 1.0)
        self.assertGreater(metrics["shiva_great_circle_km"], 5000.0)


if __name__ == "__main__":
    unittest.main()
