"""
test_krishna_mahabharata_epistemic_undecidability_and_closure_engine.py

Comprehensive Unit Test Suite for:
krishna_mahabharata_epistemic_undecidability_and_closure_engine.py

Validates epistemic categorization, taphonomic models, Shannon information decay,
protocol invariants compliance, and boundary demarcation.

Author: Kepler (A001), Generation 0 Swarm Research Agent
Workspace: D:/AgentSwarm/arena/world
"""

import unittest
from krishna_mahabharata_epistemic_undecidability_and_closure_engine import (
    EpistemicCategory,
    DemarcationBoundary,
    SubClaimDefinition,
    TaphonomicPreservationModel,
    EpistemicUndecidabilityDeconstructionEngine,
    ShannonEpistemicEntropyEngine,
    DemarcationAndProtocolVerifier,
    run_full_epistemic_closure_evaluation,
)


class TestSubClaimStructure(unittest.TestCase):
    def setUp(self):
        self.claims = EpistemicUndecidabilityDeconstructionEngine.SUB_CLAIMS

    def test_subclaims_completeness(self):
        self.assertEqual(len(self.claims), 5)
        self.assertIn("C1_METAPHYSICAL_AVATARA", self.claims)
        self.assertIn("C2_HISTORICAL_KRISHNA", self.claims)
        self.assertIn("C3_KURUKSHETRA_WAR", self.claims)
        self.assertIn("C4_EPIC_SCALE_DEMOGRAPHY", self.claims)
        self.assertIn("C5_THERMONUCLEAR_ASTRAS", self.claims)

    def test_c1_metaphysical_is_strictly_undecidable(self):
        c1 = self.claims["C1_METAPHYSICAL_AVATARA"]
        self.assertEqual(c1.boundary, DemarcationBoundary.METAPHYSICAL)
        self.assertEqual(c1.category, EpistemicCategory.METAPHYSICAL_TRANSCENDENT)
        self.assertEqual(c1.falsifiability_score, 0.0)
        self.assertEqual(c1.empirical_decidability_score, 0.0)
        self.assertGreaterEqual(c1.duhem_quine_auxiliary_count, 5)

    def test_c2_historical_krishna_is_underdetermined(self):
        c2 = self.claims["C2_HISTORICAL_KRISHNA"]
        self.assertEqual(c2.boundary, DemarcationBoundary.EMPIRICAL_HISTORICAL)
        self.assertEqual(c2.category, EpistemicCategory.HISTORICAL_PLAUSIBLE_CORE)
        self.assertGreater(c2.falsifiability_score, 0.0)
        self.assertLess(c2.falsifiability_score, 0.5)
        self.assertGreater(len(c2.evidence_for_required), 2)
        self.assertGreater(len(c2.evidence_against_required), 1)

    def test_c4_and_c5_are_empirically_falsified_as_literal_history(self):
        c4 = self.claims["C4_EPIC_SCALE_DEMOGRAPHY"]
        c5 = self.claims["C5_THERMONUCLEAR_ASTRAS"]
        self.assertEqual(c4.category, EpistemicCategory.POETIC_HYPERBOLIC_FALSIFIED)
        self.assertEqual(c5.category, EpistemicCategory.POETIC_HYPERBOLIC_FALSIFIED)
        self.assertGreater(c4.falsifiability_score, 0.9)
        self.assertGreater(c5.falsifiability_score, 0.9)
        self.assertGreater(c4.empirical_decidability_score, 0.9)
        self.assertGreater(c5.empirical_decidability_score, 0.9)


class TestTaphonomicPreservationModel(unittest.TestCase):
    def setUp(self):
        self.model = TaphonomicPreservationModel()

    def test_organic_survival_near_zero(self):
        prob = self.model.compute_organic_survival_probability()
        # Over 3,000 years with 150-yr half life = 20 half-lives = 2^-20 ~ 9.5e-7
        self.assertLess(prob, 1e-5)
        self.assertGreater(prob, 0.0)

    def test_uncremated_skeletal_recovery(self):
        recovery = self.model.compute_uncremated_skeletal_recovery_fraction()
        # 5% uncremated * 2% soil preservation = 0.001 (0.1%)
        self.assertAlmostEqual(recovery, 0.001, places=4)

    def test_iron_artifact_corrosion(self):
        # 3 mm original thickness -> half-thickness is 1.5 mm = 1500 microns
        # 1.2 microns/yr * 3000 yr = 3600 microns > 1500 microns -> completely mineralized (1.0)
        corrosion = self.model.compute_iron_artifact_degradation_fraction(3.0)
        self.assertEqual(corrosion, 1.0)

        # Thick 10 mm iron anvil -> half-thickness is 5.0 mm = 5000 microns
        # 3600 / 5000 = 0.72
        corrosion_thick = self.model.compute_iron_artifact_degradation_fraction(10.0)
        self.assertAlmostEqual(corrosion_thick, 0.72, places=2)


class TestShannonEpistemicEntropyEngine(unittest.TestCase):
    def test_information_decay_calculation(self):
        decay = ShannonEpistemicEntropyEngine.calculate_information_decay(
            initial_information_bits=1000.0,
            oral_generations=25,
            fidelity_per_generation=0.985,
            taphonomic_loss_factor=0.92
        )
        self.assertEqual(decay["initial_information_bits"], 1000.0)
        self.assertGreater(decay["cumulative_oral_fidelity"], 0.6)
        self.assertLess(decay["cumulative_oral_fidelity"], 0.8)
        self.assertLess(decay["retained_information_bits"], 100.0)
        self.assertGreater(decay["retained_information_bits"], 40.0)
        self.assertGreater(decay["noise_bits"], 900.0)
        self.assertLess(decay["signal_to_noise_ratio_db"], -10.0)
        self.assertGreater(decay["epistemic_underdetermination_index"], 0.90)


class TestDemarcationAndProtocolVerifier(unittest.TestCase):
    def test_compliant_report_passes(self):
        valid_text = (
            "This epistemic inquiry establishes strict demarcation between the metaphysical realm, "
            "which is empirically undecidable, and material historical questions. "
            "We examine falsifiability, taphonomic degradation, and clarify what would count as evidence "
            "for or against each proposition without asserting a dogmatic verdict."
        )
        result = DemarcationAndProtocolVerifier.verify_protocol_invariants(valid_text)
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["protocol_status"], "COMPLIANT")
        self.assertEqual(len(result["violations_found"]), 0)
        self.assertEqual(len(result["missing_essential_terms"]), 0)

    def test_verdict_assertion_violation_caught(self):
        violating_text = (
            "We have proven that Krishna existed in 3102 BCE! "
            "In my personal conviction, the epic is literal truth."
        )
        result = DemarcationAndProtocolVerifier.verify_protocol_invariants(violating_text)
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["protocol_status"], "VIOLATION")
        self.assertIn("we have proven that krishna existed", result["violations_found"])
        self.assertIn("in my personal conviction", result["violations_found"])

    def test_missing_essential_terms_caught(self):
        bare_text = "The story happened long ago in ancient India."
        result = DemarcationAndProtocolVerifier.verify_protocol_invariants(bare_text)
        self.assertFalse(result["is_valid"])
        self.assertGreater(len(result["missing_essential_terms"]), 0)


class TestFullEpistemicClosureEvaluation(unittest.TestCase):
    def test_full_evaluation_runs_cleanly(self):
        res = run_full_epistemic_closure_evaluation()
        self.assertIn("epistemic_structure", res)
        self.assertIn("taphonomic_metrics", res)
        self.assertIn("shannon_decay", res)
        self.assertIn("summary", res)
        self.assertEqual(len(res["epistemic_structure"]), 5)


if __name__ == "__main__":
    unittest.main()
