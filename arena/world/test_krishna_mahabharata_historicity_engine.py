"""
test_krishna_mahabharata_historicity_engine.py

Comprehensive test suite verifying the Epistemic Analysis Engine for the Historicity of
Lord Krishna and the Mahabharata War.
"""

import unittest
from krishna_mahabharata_historicity_engine import (
    EpistemicClass,
    ProtocolViolationType,
    ProtocolViolationException,
    TextualStratificationModel,
    DynasticGenerationalModel,
    ArchaeoastronomySensitivityModel,
    ArchaeologicalCorpusRegistry,
    EpigraphicCorpusRegistry,
    EpistemicAdjudicationFramework
)


class TestTextualStratificationModel(unittest.TestCase):
    def setUp(self):
        self.model = TextualStratificationModel()

    def test_strata_presence_and_verse_counts(self):
        self.assertIn("Jaya", self.model.strata)
        self.assertIn("Bharata", self.model.strata)
        self.assertIn("Critical_Edition", self.model.strata)
        self.assertIn("Vulgate", self.model.strata)

        self.assertEqual(self.model.strata["Jaya"].approximate_verse_count, 8818)
        self.assertEqual(self.model.strata["Bharata"].approximate_verse_count, 24000)
        self.assertEqual(self.model.strata["Critical_Edition"].approximate_verse_count, 82153)
        self.assertEqual(self.model.strata["Vulgate"].approximate_verse_count, 100000)

    def test_inflation_metrics_calculation(self):
        metrics = self.model.compute_inflation_metrics()
        self.assertAlmostEqual(metrics["jaya_to_bharata_growth"], 24000 / 8818, places=3)
        self.assertAlmostEqual(metrics["jaya_to_vulgate_growth"], 100000 / 8818, places=3)
        self.assertGreater(metrics["net_expansion_factor"], 11.0)
        # BORI Critical Edition pruned ~17,847 late Vulgate verses
        self.assertGreater(metrics["bori_rejection_percentage"], 17.0)
        self.assertLess(metrics["bori_rejection_percentage"], 19.0)


class TestDynasticGenerationalModel(unittest.TestCase):
    def setUp(self):
        self.model = DynasticGenerationalModel()

    def test_traditional_3102_bce_epoch_feasibility(self):
        """Invariant: 3102 BCE war date implies biologically impossible dynastic reign lengths."""
        result = self.model.evaluate_dynastic_feasibility(3102)
        # (3102 - 362) / 30 = 2740 / 30 = 91.33 years per king
        self.assertAlmostEqual(result["implied_mean_reign_years"], 91.333, places=2)
        self.assertFalse(result["feasible"])
        self.assertEqual(result["verdict"], "BIOLOGICALLY_IMPOSSIBLE_DYNASTIC_AVERAGE")

    def test_scholarly_950_bce_epoch_feasibility(self):
        """Invariant: ~950 BCE war date matches empirical dynastic reign averages (14-22 years)."""
        result = self.model.evaluate_dynastic_feasibility(950)
        # (950 - 362) / 30 = 588 / 30 = 19.6 years per king
        self.assertAlmostEqual(result["implied_mean_reign_years"], 19.6, places=1)
        self.assertTrue(result["feasible"])
        self.assertEqual(result["verdict"], "HIGHLY_PLAUSIBLE_HISTORICAL_CONCORDANCE")

    def test_invalid_date_raises_error(self):
        with self.assertRaises(ValueError):
            self.model.compute_implied_reign_length(300)


class TestArchaeoastronomySensitivityModel(unittest.TestCase):
    def setUp(self):
        self.model = ArchaeoastronomySensitivityModel()

    def test_proposals_dispersion_and_inverse_problem(self):
        stats = self.model.compute_dispersion_statistics()
        # The proposed dates span from 950 BCE to 5561 BCE
        self.assertEqual(stats["min_date_bce"], 950.0)
        self.assertEqual(stats["max_date_bce"], 5561.0)
        self.assertEqual(stats["span_years"], 4611.0)
        # Standard deviation exceeds 1000 years, demonstrating extreme ill-posedness
        self.assertGreater(stats["std_deviation_years"], 1300.0)


class TestArchaeologicalCorpusRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = ArchaeologicalCorpusRegistry()

    def test_key_sites_registered(self):
        expected_sites = ["Hastinapura", "Kaushambi", "Kurukshetra", "Dwarka", "Indraprastha", "Sinauli"]
        for site in expected_sites:
            self.assertIn(site, self.registry.sites)

    def test_hastinapura_flood_and_kaushambi_continuity(self):
        hastinapura = self.registry.sites["Hastinapura"]
        kaushambi = self.registry.sites["Kaushambi"]

        self.assertIn("alluvial flood layer", " ".join(hastinapura.key_findings).lower())
        self.assertEqual(hastinapura.scholarly_epistemic_status, "STRONG_PRIMARY_STRATIGRAPHIC_CORROBORATION")
        self.assertEqual(kaushambi.scholarly_epistemic_status, "STRONG_PRIMARY_STRATIGRAPHIC_CORROBORATION")

    def test_dwarka_marine_findings(self):
        dwarka = self.registry.sites["Dwarka"]
        self.assertIn("submerged dressed stone", " ".join(dwarka.key_findings).lower())
        self.assertEqual(dwarka.scholarly_epistemic_status, "CONFIRMED_SUBMERGED_PORT_SETTLEMENT")

    def test_sinauli_chariots(self):
        sinauli = self.registry.sites["Sinauli"]
        self.assertIn("chariots with solid disk wheels", " ".join(sinauli.key_findings).lower())
        self.assertEqual(sinauli.calibrated_c14_bce_range, (2000, 1800))


class TestEpigraphicCorpusRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = EpigraphicCorpusRegistry()

    def test_inscriptions_count_and_presence(self):
        self.assertGreaterEqual(len(self.registry.inscriptions), 5)
        names = [i.artifact_name for i in self.registry.inscriptions]
        self.assertTrue(any("Agathocles" in n for n in names))
        self.assertTrue(any("Heliodorus" in n for n in names))
        self.assertTrue(any("Mora Well" in n for n in names))
        self.assertTrue(any("Ghosundi" in n for n in names))
        self.assertTrue(any("Nanaghat" in n for n in names))

    def test_heliodorus_inscription_details(self):
        heliodorus = next(i for i in self.registry.inscriptions if "Heliodorus" in i.artifact_name)
        self.assertEqual(heliodorus.nominal_year_bce, 113)
        self.assertIn("Devadeva Vasudeva", heliodorus.theological_or_historical_content)
        self.assertIn("Trini Amutapadani", heliodorus.theological_or_historical_content)
        self.assertIn("Bhagavata", heliodorus.theological_or_historical_content)

    def test_agathocles_coins_details(self):
        agathocles = next(i for i in self.registry.inscriptions if "Agathocles" in i.artifact_name)
        self.assertEqual(agathocles.nominal_year_bce, 185)
        self.assertIn("Chakra", agathocles.theological_or_historical_content)
        self.assertIn("Sankarshana", agathocles.theological_or_historical_content)


class TestProtocolViolationFirewall(unittest.TestCase):
    def setUp(self):
        self.framework = EpistemicAdjudicationFramework()

    def test_violation_scripture_as_laboratory_data(self):
        """Violation 1: Treating epic Astras as literal nuclear/radiation laboratory data."""
        invalid_statement = "The Brahmashira weapon emitted 50 megatons of radiation and caused atomic blast fallout."
        with self.assertRaises(ProtocolViolationException) as ctx:
            self.framework.evaluate_claim(
                invalid_statement,
                EpistemicClass.DEVOTIONAL_THEOLOGICAL_CLAIM,
                is_asserting_empirical_proof=True
            )
        self.assertEqual(ctx.exception.violation_type, ProtocolViolationType.SCRIPTURE_AS_LABORATORY_DATA)

    def test_violation_absence_of_evidence_as_proof_of_falsehood(self):
        """Violation 2: Asserting absence of contemporary 3100 BCE inscription proves Krishna never existed."""
        invalid_statement = "The absence of archaeological proof from 3000 BCE proves Krishna never existed and is pure fiction."
        with self.assertRaises(ProtocolViolationException) as ctx:
            self.framework.evaluate_claim(
                invalid_statement,
                EpistemicClass.SCHOLARLY_HISTORICAL_CONSENSUS,
                is_asserting_empirical_proof=False
            )
        self.assertEqual(ctx.exception.violation_type, ProtocolViolationType.ABSENCE_OF_EVIDENCE_AS_PROOF_OF_FALSEHOOD)

    def test_valid_epistemic_claims_pass(self):
        valid_epigraphic = (
            "The Heliodorus pillar inscription (c. 113 BCE) documents that Greek ambassador Heliodorus "
            "venerated Vasudeva as Devadeva and dedicated a Garudadhvaja."
        )
        res = self.framework.evaluate_claim(
            valid_epigraphic,
            EpistemicClass.PRIMARY_MATERIAL_EPIGRAPHIC,
            is_asserting_empirical_proof=False
        )
        self.assertEqual(res["status"], "APPROVED_FOR_ANALYSIS")

        valid_devotional = (
            "In Vaishnava theology, Krishna is revered as Svayam Bhagavan, the Supreme Personality of Godhead."
        )
        res_dev = self.framework.evaluate_claim(
            valid_devotional,
            EpistemicClass.DEVOTIONAL_THEOLOGICAL_CLAIM,
            is_asserting_empirical_proof=False
        )
        self.assertEqual(res_dev["status"], "APPROVED_FOR_ANALYSIS")

    def test_comprehensive_synthesis_generation(self):
        synthesis = self.framework.generate_comprehensive_synthesis()
        self.assertIn("textual_metrics", synthesis)
        self.assertIn("dynastic_feasibility", synthesis)
        self.assertIn("astronomy_dispersion", synthesis)
        self.assertIn("tripartite_demarcation", synthesis)
        self.assertEqual(len(synthesis["tripartite_demarcation"]["primary_material_documented"]), 8)


if __name__ == "__main__":
    unittest.main()
