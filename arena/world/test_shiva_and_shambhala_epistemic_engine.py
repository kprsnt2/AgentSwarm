"""
test_shiva_and_shambhala_epistemic_engine.py

Comprehensive test suite verifying the Epistemic Engine for Lord Shiva Historicity
and Shambhala Presence.
"""

import unittest
from shiva_and_shambhala_epistemic_engine import (
    EpistemicCategory,
    OntologicalMode,
    ProtocolViolationType,
    ProtocolViolationException,
    ShivaStratigraphyLayer,
    PhilologicalEvolutionRecord,
    MaterialEpigraphicRecord,
    ShambhalaDomainRecord,
    KalachakraEschatologyRecord,
    ShivaHistoricityAnalyzer,
    ShambhalaPresenceAnalyzer,
    ConsilienceEngine
)


class TestShivaHistoricityAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = ShivaHistoricityAnalyzer()

    def test_stratigraphy_chronological_ordering(self):
        """Invariant: Stratigraphic layers must be ordered chronologically."""
        stratigraphy = self.analyzer.get_stratigraphy()
        self.assertGreaterEqual(len(stratigraphy), 5)

        for i in range(len(stratigraphy) - 1):
            curr_start = stratigraphy[i].chronological_bce_ce_range[0]
            next_start = stratigraphy[i + 1].chronological_bce_ce_range[0]
            self.assertLessEqual(curr_start, next_start, f"Stratigraphy out of order at layer {i}: {stratigraphy[i].epoch_name}")

    def test_rigvedic_rudra_linguistic_distinction(self):
        """Invariant: Early Vedic stratum must identify 'śiva' as an adjective, not yet a standalone personal name."""
        stratigraphy = self.analyzer.get_stratigraphy()
        early_vedic = next(layer for layer in stratigraphy if "Early Vedic" in layer.epoch_name)
        self.assertIn("adjective", early_vedic.linguistic_form_of_name.lower())
        self.assertIn("rudra", early_vedic.linguistic_form_of_name.lower())

    def test_material_epigraphic_evidence_presence(self):
        """Invariant: Material horizon must cite Gudimallam Lingam and Kushan OESHO coinage."""
        stratigraphy = self.analyzer.get_stratigraphy()
        material_layer = next(layer for layer in stratigraphy if "Early Epigraphic" in layer.epoch_name)
        text_dump = " ".join(material_layer.epigraphic_or_material_evidence)
        self.assertIn("Gudimallam", text_dump)
        self.assertIn("OESHO", text_dump)

    def test_philological_corpus_evolution(self):
        """Invariant: Philological corpus must trace RV adjective to Yajurvedic invocation to Upanishadic Brahman."""
        corpus = self.analyzer.get_philological_corpus()
        self.assertEqual(len(corpus), 4)
        rv = corpus[0]
        yv = corpus[1]
        up = corpus[2]
        tantra = corpus[3]
        self.assertIn("Pure adjective", rv.grammatical_status_of_siva)
        self.assertIn("Śrī Rudram", yv.textual_witness)
        self.assertIn("Śvetāśvatara", up.textual_witness)
        self.assertIn("Paramashiva", tantra.grammatical_status_of_siva)

    def test_material_catalog_anchors(self):
        """Invariant: Material catalog must include Gudimallam, Kushan coins, Mathura pillar, Elephanta."""
        catalog = self.analyzer.get_material_catalog()
        self.assertEqual(len(catalog), 4)
        names = [item.artifact_or_site for item in catalog]
        self.assertTrue(any("Gudimallam" in n for n in names))
        self.assertTrue(any("Kushan" in n for n in names))
        self.assertTrue(any("Mathura" in n for n in names))
        self.assertTrue(any("Elephanta" in n for n in names))

    def test_bio_historical_personhood_adjudication(self):
        """Invariant: Bio-historical personhood for Shiva must evaluate to low posterior probability (archetypal deity)."""
        bio_eval = self.analyzer.evaluate_bio_historical_personhood()
        self.assertLess(bio_eval["posterior_probability"], 0.05)
        self.assertEqual(bio_eval["ontological_verdict"], OntologicalMode.ARCHETYPAL_COSMIC_DEITY)

    def test_pramana_epistemic_demarcation(self):
        """Invariant: Pramana analysis must cover Pratyaksha, Anumana, and Shabda."""
        pramana_eval = self.analyzer.evaluate_reality_under_pramanas()
        self.assertIn("pratyaksha_empirical_perception", pramana_eval)
        self.assertIn("anumana_logical_inference", pramana_eval)
        self.assertIn("shabda_textual_testimony", pramana_eval)
        self.assertIn("metaphysical_reality_in_shaivism", pramana_eval)


class TestShambhalaPresenceAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = ShambhalaPresenceAnalyzer()

    def test_domain_demarcation_completeness(self):
        """Invariant: Must delineate Puranic Sambhal, Kalachakra Tantra, and Modern Occultism."""
        domains = self.analyzer.get_domains()
        self.assertEqual(len(domains), 3)

        types = [d.domain_type for d in domains]
        self.assertTrue(any("Puranic Sambhala" in t for t in types))
        self.assertTrue(any("Kalachakra" in t for t in types))
        self.assertTrue(any("Western Theosophical" in t for t in types))

    def test_puranic_sambhal_geographic_anchoring(self):
        """Invariant: Puranic Sambhala-grama must anchor to the physical town of Sambhal, UP."""
        domains = self.analyzer.get_domains()
        puranic = next(d for d in domains if "Puranic" in d.domain_type)
        self.assertIsNotNone(puranic.coordinates)
        self.assertAlmostEqual(puranic.coordinates[0], 28.58, delta=0.5)
        self.assertAlmostEqual(puranic.coordinates[1], 78.57, delta=0.5)
        self.assertEqual(puranic.ontological_classification, OntologicalMode.PHYSICAL_GEOPOLITICAL_TERRITORY)

    def test_kalachakra_pure_land_classification(self):
        """Invariant: Kalachakra Shambhala must be classified as an esoteric subtle realm / pure land."""
        domains = self.analyzer.get_domains()
        kalachakra = next(d for d in domains if "Kalachakra" in d.domain_type)
        self.assertEqual(kalachakra.ontological_classification, OntologicalMode.ESOTERIC_PURE_LAND_SUBTLE_REALM)
        self.assertEqual(kalachakra.epistemic_tier, EpistemicCategory.TIER_3_DEVOTIONAL_THEOLOGICAL_CLAIM)

    def test_kalachakra_eschatology_record(self):
        """Invariant: Kalachakra eschatology must record 32 rulers, Raudra Chakrin, and internal allegory."""
        eschatology = self.analyzer.get_kalachakra_eschatology()
        self.assertEqual(eschatology.total_rulers, 32)
        self.assertEqual(eschatology.climactic_prophesied_king, "Raudra Chakrin (Kalki 25)")
        self.assertEqual(eschatology.eschatological_epoch_approx_ce, 2424)
        self.assertIn("allegory", eschatology.tantric_allegorical_interpretation.lower())

    def test_theosophical_occult_classification(self):
        """Invariant: Theosophical/Occult Shambhala must be classified as pseudohistorical fabrication."""
        domains = self.analyzer.get_domains()
        occult = next(d for d in domains if "Western Theosophical" in d.domain_type)
        self.assertEqual(occult.ontological_classification, OntologicalMode.PSEUDOHISTORICAL_FABRICATION)
        self.assertEqual(occult.epistemic_tier, EpistemicCategory.TIER_4_ESOTERIC_OCCULT_MODERN_INVENTION)

    def test_presence_synthesis_multi_modal(self):
        """Invariant: Presence synthesis must report False for macro-physical kingdom and True for Sambhal, UP and Subtle realm."""
        presence = self.analyzer.evaluate_presence()
        self.assertFalse(presence["geographical_physical_macro_kingdom"]["is_present"])
        self.assertTrue(presence["historical_indic_location_sambhal_up"]["is_present"])
        self.assertTrue(presence["vajrayana_pure_land_subtle_reality"]["is_present"])


class TestConsilienceAndProtocolGuards(unittest.TestCase):

    def setUp(self):
        self.engine = ConsilienceEngine()

    def test_protocol_violation_scripture_as_laboratory_data(self):
        """Invariant: Attempting to treat scripture as laboratory data MUST raise ProtocolViolationException."""
        with self.assertRaises(ProtocolViolationException) as ctx:
            self.engine.enforce_protocol_guards(
                claim_statement="Measure tensile strength of Pinaka using laboratory test",
                method="empirical_materials_testing"
            )
        self.assertEqual(ctx.exception.violation_type, ProtocolViolationType.SCRIPTURE_AS_LABORATORY_DATA)

    def test_protocol_violation_absence_of_evidence(self):
        """Invariant: Attempting to treat absence of evidence as proof of falsehood MUST raise ProtocolViolationException."""
        with self.assertRaises(ProtocolViolationException) as ctx:
            self.engine.enforce_protocol_guards(
                claim_statement="Absence of bones proves nonexistence of deity Shiva",
                method="positivist_reductionism"
            )
        self.assertEqual(ctx.exception.violation_type, ProtocolViolationType.ABSENCE_OF_EVIDENCE_AS_PROOF_OF_FALSEHOOD)

    def test_epistemic_demarcation_metrics(self):
        """Invariant: Epistemic metrics must reflect rigorous multi-tier consilience."""
        metrics = self.engine.calculate_epistemic_demarcation_metrics()
        self.assertEqual(metrics["shiva_stratigraphic_completeness"], 1.0)
        self.assertEqual(metrics["shiva_material_epigraphic_anchoring"], 1.0)
        self.assertLess(metrics["shiva_bio_historical_human_posterior"], 0.05)
        self.assertEqual(metrics["shambhala_physical_macro_kingdom_verifiability"], 0.0)
        self.assertEqual(metrics["shambhala_sambhal_up_topographical_reality"], 1.0)
        self.assertGreater(metrics["composite_epistemic_rigor_index"], 0.9)


if __name__ == "__main__":
    unittest.main()
