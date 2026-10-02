"""
test_aryabhata_epistemic_engine.py

Comprehensive test suite verifying the Aryabhata Epistemic Demarcation Engine,
Firewall Enforcement, Aryabhatiya Astronomical Calculations, Classical Pramana-shastra,
and Bayesian Likelihood Invariance.
"""

import unittest
import math
from aryabhata_epistemic_engine import (
    ProtocolViolationError,
    EpistemicCategory,
    Pramana,
    AdjudicationStatus,
    IndianPhilosophicalSchool,
    FormalDharmicClaim,
    AryabhataAstronomicalEngine,
    VedicInformationTheoryEngine,
    ClassicalEpistemologyFramework,
    BayesianMetaphysicalInvarianceEngine,
    ComprehensiveDharmicTaxonomyEngine
)


class TestEpistemicFirewallEnforcement(unittest.TestCase):

    def setUp(self):
        self.registry = ComprehensiveDharmicTaxonomyEngine()

    def test_firewall_raises_protocol_violation_on_class_b_verdict(self):
        """Invariant: Asserting any verdict on a Class B claim must raise ProtocolViolationError."""
        class_b_claims = self.registry.get_claims_by_category(EpistemicCategory.CLASS_B_METAPHYSICAL_ONTOLOGICAL)
        self.assertGreater(len(class_b_claims), 0)

        for claim in class_b_claims:
            for forbidden_verdict in ["TRUE", "FALSE", "PROVEN", "DISPROVEN", "VERIFIED", "REFUTED"]:
                with self.assertRaises(ProtocolViolationError):
                    claim.attempt_verdict_assertion(forbidden_verdict)

    def test_class_b_claims_have_zero_discriminative_bayes_power(self):
        """Invariant: Metaphysical claims must possess 0.0 Bayes factor discriminative power."""
        class_b_claims = self.registry.get_claims_by_category(EpistemicCategory.CLASS_B_METAPHYSICAL_ONTOLOGICAL)
        for claim in class_b_claims:
            self.assertEqual(claim.bayes_factor_discriminative_power, 0.0)
            self.assertIsNone(claim.empirical_investigation_method)
            self.assertIsNotNone(claim.epistemic_insulation_mechanism)
            self.assertEqual(claim.adjudication_status, AdjudicationStatus.EMPIRICALLY_UNDECIDABLE)

    def test_class_a1_claims_are_decidable(self):
        """Invariant: Historical claims must have empirical investigation methods and non-zero discriminative power."""
        class_a1_claims = self.registry.get_claims_by_category(EpistemicCategory.CLASS_A1_HISTORICAL_TEXTUAL)
        self.assertGreater(len(class_a1_claims), 0)
        for claim in class_a1_claims:
            self.assertEqual(claim.adjudication_status, AdjudicationStatus.EMPIRICALLY_DECIDABLE)
            self.assertIsNotNone(claim.empirical_investigation_method)
            self.assertIsNone(claim.epistemic_insulation_mechanism)
            self.assertGreater(claim.bayes_factor_discriminative_power, 0.0)

    def test_registry_firewall_audit_clean(self):
        """Registry audit must report 0 violations and intact firewall."""
        audit = self.registry.verify_firewall_integrity()
        self.assertTrue(audit["firewall_intact"])
        self.assertEqual(audit["violations_count"], 0)
        self.assertEqual(audit["total_claims"], 12)
        self.assertEqual(audit["class_a1_count"], 4)
        self.assertEqual(audit["class_a2_count"], 2)
        self.assertEqual(audit["class_b_count"], 6)


class TestAryabhataAstronomicalEngine(unittest.TestCase):

    def test_civil_days_and_year_length(self):
        periods = AryabhataAstronomicalEngine.calculate_aryabhata_periods()
        # Civil days = 1,582,237,500 - 4,320,000 = 1,577,917,500
        self.assertEqual(periods["civil_days_per_mahayuga"], 1_577_917_500)
        # Year length = 1,577,917,500 / 4,320,000 = 365.25868... days
        self.assertAlmostEqual(periods["year_length_civil_days"], 365.25868, places=4)
        # Year error relative to modern 365.256363 days is under 0.001%
        self.assertLess(periods["relative_errors_pct"]["year_length"], 0.001)

    def test_planetary_periods_accuracy(self):
        periods = AryabhataAstronomicalEngine.calculate_aryabhata_periods()
        # Mars: ~686.9997 days vs modern 686.9797 days (< 0.01% error)
        self.assertAlmostEqual(periods["mars_period_days"], 687.0, places=1)
        self.assertLess(periods["relative_errors_pct"]["mars"], 0.01)

        # Jupiter: ~4332.27 days vs modern 4332.59 days (< 0.01% error)
        self.assertAlmostEqual(periods["jupiter_period_days"], 4332.27, places=1)
        self.assertLess(periods["relative_errors_pct"]["jupiter"], 0.01)

        # Saturn: ~10766.06 days vs modern 10759.22 days (< 0.1% error)
        self.assertAlmostEqual(periods["saturn_period_days"], 10766.1, places=1)
        self.assertLess(periods["relative_errors_pct"]["saturn"], 0.1)

        # Moon: ~27.321668 days vs modern 27.321661 days (< 0.0001% error)
        self.assertAlmostEqual(periods["moon_month_days"], 27.321668, places=5)
        self.assertLess(periods["relative_errors_pct"]["moon"], 0.0001)

    def test_yuga_and_kalpa_comparison(self):
        cmp = AryabhataAstronomicalEngine.compare_yuga_and_kalpa_models()
        # Aryabhata Kalpa: 1,008 * 4.32 Ma = 4.35456 Ga
        self.assertEqual(cmp["aryabhata_model"]["kalpa_mahayugas"], 1008)
        self.assertAlmostEqual(cmp["aryabhata_model"]["kalpa_gyr"], 4.35456, places=5)
        self.assertAlmostEqual(cmp["aryabhata_model"]["earth_age_delta_pct"], 4.148, places=2)

        # Surya Siddhanta Kalpa: 1,000 * 4.32 Ma = 4.320 Ga
        self.assertEqual(cmp["puranic_surya_siddhanta_model"]["kalpa_mahayugas"], 1000)
        self.assertAlmostEqual(cmp["puranic_surya_siddhanta_model"]["kalpa_gyr"], 4.320, places=3)
        self.assertAlmostEqual(cmp["puranic_surya_siddhanta_model"]["earth_age_delta_pct"], 4.909, places=2)

        # Aryabhata has 4 equal yugas of 1,080,000 yr
        self.assertEqual(cmp["aryabhata_model"]["yuga_length_years"], 1_080_000)

    def test_eclipse_shadow_geometry(self):
        eclipse = AryabhataAstronomicalEngine.calculate_eclipse_shadow_geometry()
        # Shadow cone length > 1.3 million km (reaches far past Moon at 384,400 km)
        self.assertGreater(eclipse["shadow_cone_length_km"], 1_300_000.0)
        # Umbra diameter at Moon > 9,000 km
        self.assertGreater(eclipse["umbra_diameter_at_moon_km"], 9_000.0)
        # Moon diameter is 3,474 km, so coverage ratio > 2.5
        self.assertGreater(eclipse["coverage_ratio"], 2.5)
        self.assertTrue(eclipse["is_total_eclipse_possible"])


class TestVedicInformationTheoryEngine(unittest.TestCase):

    def test_ghana_convolution_scaling(self):
        res = VedicInformationTheoryEngine.analyze_ghana_convolution(10)
        self.assertEqual(res["pada_tokens"], 10)
        self.assertEqual(res["krama_tokens"], 18)
        self.assertEqual(res["jata_tokens"], 54)
        self.assertEqual(res["ghana_tokens"], 110)
        self.assertEqual(res["redundancy_ghana"], 11.0)
        self.assertEqual(res["internal_context_checks"], 13)
        self.assertGreater(res["error_suppression_fidelity"], 0.999999999999)
        self.assertAlmostEqual(res["shannon_redundancy"], 0.9091, places=3)

    def test_ghana_convolution_validation(self):
        with self.assertRaises(ValueError):
            VedicInformationTheoryEngine.analyze_ghana_convolution(2)


class TestClassicalEpistemologyFramework(unittest.TestCase):

    def test_school_pramanas_mapping(self):
        pramanas = ClassicalEpistemologyFramework.get_school_pramanas()
        # Carvaka accepts ONLY Pratyaksha
        self.assertEqual(pramanas[IndianPhilosophicalSchool.CARVAKA_LOKAYATA.value], [Pramana.PRATYAKSHA])
        # Buddhist accepts Pratyaksha and Anumana
        self.assertEqual(pramanas[IndianPhilosophicalSchool.BUDDHIST_PRAMANAVADA.value], [Pramana.PRATYAKSHA, Pramana.ANUMANA])
        # Nyaya accepts 4
        self.assertEqual(len(pramanas[IndianPhilosophicalSchool.NYAYA_VAISHESHIKA.value]), 4)
        # Mimamsa and Advaita accept 6
        self.assertEqual(len(pramanas[IndianPhilosophicalSchool.PURVA_MIMAMSA.value]), 6)
        self.assertEqual(len(pramanas[IndianPhilosophicalSchool.ADVAITA_VEDANTA.value]), 6)

    def test_advaita_three_tier_ontology(self):
        ontology = ClassicalEpistemologyFramework.analyze_advaita_three_tier_ontology()
        self.assertIn("Pratibhasika", ontology["strata"])
        self.assertIn("Vyavaharika", ontology["strata"])
        self.assertIn("Paramarthika", ontology["strata"])
        self.assertIn("scientific_applicability", ontology["strata"]["Vyavaharika"])
        self.assertIn("scientific_applicability", ontology["strata"]["Paramarthika"])

    def test_purva_mimamsa_paradox(self):
        mimamsa = ClassicalEpistemologyFramework.analyze_purva_mimamsa_paradox()
        self.assertIn("Atheistic", mimamsa["creator_god_status"])
        self.assertIn("Apaurusheyatva", mimamsa["scripture_status"])


class TestBayesianInvarianceEngine(unittest.TestCase):

    def test_likelihood_invariance_produces_zero_bits(self):
        res = BayesianMetaphysicalInvarianceEngine.compute_likelihood_invariance(0.5, 0.5)
        self.assertAlmostEqual(res["likelihood_ratio_lambda"], 1.0, places=5)
        self.assertAlmostEqual(res["log_bayes_factor"], 0.0, places=5)
        self.assertAlmostEqual(res["information_gain_bits"], 0.0, places=5)
        self.assertTrue(res["is_likelihood_invariant"])

    def test_likelihood_invariance_breaks_on_discriminative_data(self):
        res = BayesianMetaphysicalInvarianceEngine.compute_likelihood_invariance(0.1, 0.9)
        self.assertFalse(res["is_likelihood_invariant"])
        self.assertAlmostEqual(res["likelihood_ratio_lambda"], 9.0, places=4)
        self.assertGreater(res["information_gain_bits"], 0.0)

    def test_karmic_causal_overfitting(self):
        fit = BayesianMetaphysicalInvarianceEngine.analyze_karmic_causal_overfitting(100)
        self.assertGreater(fit["naturalist_model"]["residual_degrees_of_freedom"], 0)
        self.assertLessEqual(fit["karmic_model"]["residual_degrees_of_freedom"], 0)
        self.assertEqual(fit["karmic_model"]["falsifiability_status"], "Non-falsifiable (infinite latent parameter capacity absorbs all residuals post-hoc)")

    def test_axiomatic_disagreement_structure(self):
        disagreement = BayesianMetaphysicalInvarianceEngine.formalize_axiomatic_disagreement()
        matrix = disagreement["divergence_matrix"]
        self.assertEqual(len(matrix), 3)
        domains = [item["domain"] for item in matrix]
        self.assertIn("Ontological Primitive", domains)
        self.assertIn("Moral Causality Conservation", domains)
        self.assertIn("Epistemic Grounding (Pramana Validity)", domains)


if __name__ == "__main__":
    unittest.main()
