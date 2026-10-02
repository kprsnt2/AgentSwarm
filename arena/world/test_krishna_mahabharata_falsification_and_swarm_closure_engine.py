"""
test_krishna_mahabharata_falsification_and_swarm_closure_engine.py
==================================================================
Unit tests for the Definitive Falsification Suite, Demographic Carrying
Capacity Model, and Prior Sensitivity Engine.

Ensures strict compliance with:
  - Tripartite demarcation across all domains
  - Protocol violations prevention
  - Carrying capacity demographic invariants
  - Bayesian sensitivity consistency
"""

import unittest
import math
from krishna_mahabharata_falsification_and_swarm_closure_engine import (
    EpistemicPlane,
    CounterfactualFalsificationSuite,
    DemographicCarryingCapacityModel,
    GitaStratigraphyAndTheologyModel,
    PriorSensitivityAndRobustnessEngine,
    DefinitiveEpistemicVerdictReporter
)


class TestFalsificationAndClosureEngine(unittest.TestCase):

    def setUp(self):
        self.falsification_suite = CounterfactualFalsificationSuite()
        self.capacity_model = DemographicCarryingCapacityModel()

    def test_falsification_events_definition(self):
        """Verifies that all falsification events specify valid hypotheses and likelihoods."""
        self.assertGreaterEqual(len(self.falsification_suite.falsification_tests), 6)
        for test in self.falsification_suite.falsification_tests:
            self.assertIn("id", test)
            self.assertIn("description", test)
            self.assertIn("falsifies", test)
            self.assertIn("strengthens", test)
            self.assertIn("likelihood_given_H1", test)

    def test_simulation_of_pgw_epigraphy(self):
        """Simulates finding in situ 10th-c. BCE PGW inscription naming Parikshit."""
        priors = {h: 0.2 for h in CounterfactualFalsificationSuite.HYPOTHESES}
        posteriors = self.falsification_suite.simulate_falsification_event("F1_CONTEMPORARY_PGW_EPIGRAPHY", priors)
        self.assertGreater(posteriors["H1_HISTORICAL_NUCLEUS"], 0.65)
        self.assertLess(posteriors["H2_RADICAL_MYTHICISM"], 1e-4)

    def test_simulation_of_zero_occupation_pgw(self):
        """Simulates finding PGW sites were sterile uninhabited wilderness."""
        priors = {h: 0.2 for h in CounterfactualFalsificationSuite.HYPOTHESES}
        posteriors = self.falsification_suite.simulate_falsification_event("F3_ZERO_OCCUPATION_PGW_HORIZON", priors)
        self.assertGreater(posteriors["H2_RADICAL_MYTHICISM"], 0.85)
        self.assertLess(posteriors["H1_HISTORICAL_NUCLEUS"], 1e-4)

    def test_demographic_carrying_capacity(self):
        """Verifies demographic limits of the Kuru-Panchala realm."""
        cap = self.capacity_model.compute_regional_carrying_capacity()
        self.assertGreater(cap["max_sustainable_population"], 50000.0)
        self.assertLess(cap["max_sustainable_population"], 2000000.0)
        self.assertGreater(cap["max_mobilizable_warriors"], 5000.0)
        self.assertLess(cap["max_mobilizable_warriors"], 100000.0)

    def test_akshauhini_hyperbole_factor(self):
        """Verifies Akshauhini hyperbole scaling calculation."""
        comp = self.capacity_model.compare_akshauhini_vs_capacity()
        self.assertEqual(comp["epic_combatant_claim"], 3936600.0)
        self.assertGreater(comp["linear_expansion_ratio"], 10.0)
        self.assertGreater(comp["logarithmic_hyperbole_index"], 1.0)
        self.assertIn("demographic_verdict", comp)

    def test_gita_stratigraphy(self):
        """Verifies the three-tier stratigraphy of the Bhagavad Gita."""
        summary = GitaStratigraphyAndTheologyModel.get_stratigraphic_summary()
        self.assertEqual(summary["total_strata"], 3)
        self.assertIn("CORE_SAMJAYA_DIALOGUE", summary["layers"])
        self.assertIn("UPANISHADIC_SYNTHESIS", summary["layers"])
        self.assertIn("BHAKTI_THEOPHANY", summary["layers"])

    def test_prior_sensitivity_sweep(self):
        """Verifies that even with a skeptical prior of 1 in 100,000, posterior favors H1."""
        sweep = PriorSensitivityAndRobustnessEngine.run_sensitivity_sweep()
        self.assertEqual(len(sweep), 9)
        # Even at prior 1e-5 (0.00001):
        extreme_skeptic = sweep[0]
        self.assertEqual(extreme_skeptic["prior_probability"], 1e-5)
        self.assertGreater(extreme_skeptic["posterior_probability"], 0.999999)

    def test_definitive_verdict_compilation(self):
        """Verifies complete assembly of definitive scientific verdict."""
        verdict = DefinitiveEpistemicVerdictReporter.compile_verdict()
        self.assertIn("demarcation", verdict)
        self.assertIn("WAS_LORD_KRISHNA_REAL", verdict["demarcation"])
        self.assertIn("DID_THE_MAHABHARATA_WAR_HAPPEN", verdict["demarcation"])
        self.assertIn("what_is_established", verdict)
        self.assertIn("what_remains_unknown", verdict)
        self.assertIn("what_evidence_would_change_our_mind", verdict)

        # Check tripartite elements
        krishna_dem = verdict["demarcation"]["WAS_LORD_KRISHNA_REAL"]
        self.assertGreaterEqual(len(krishna_dem["primary_evidence"]), 5)
        self.assertIn("Chandogya Upanishad", krishna_dem["primary_evidence"][0])
        self.assertTrue(len(krishna_dem["scholarly_consensus"]) > 50)
        self.assertTrue(len(krishna_dem["devotional_claim"]) > 50)


if __name__ == "__main__":
    unittest.main()
