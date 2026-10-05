"""
test_krishna_mahabharata_dynamic_epistemic_and_shannon_transmission_engine.py

Unit tests for Dynamic Epistemic Logic, Shannon oral transmission entropy,
the Trivikrama Trilemma, and Swarm Protocol Safety Firewall.

Author: Kepler (A001, Swarm Generation 0)
Workspace: D:\\AgentSwarm\\arena\\world
"""

import unittest
from krishna_mahabharata_dynamic_epistemic_and_shannon_transmission_engine import (
    ShannonOralTransmissionModel,
    DynamicEpistemicLogicModel,
    TrivikramaTrilemmaModel,
    SwarmProtocolSafetyFirewall,
    run_comprehensive_dynamic_synthesis
)


class TestShannonOralTransmissionModel(unittest.TestCase):
    def setUp(self):
        self.model = ShannonOralTransmissionModel()

    def test_bits_per_verse(self):
        # 32 syllables * 4.5 bits/syllable = 144 bits
        self.assertEqual(self.model.bits_per_verse, 144.0)

    def test_stratigraphy_metrics(self):
        metrics = self.model.calculate_textual_stratigraphy_metrics()
        self.assertIn("Jaya", metrics)
        self.assertIn("Bharata", metrics)
        self.assertIn("Mahabharata_Vulgate", metrics)

        # Jaya is 8,800 verses -> 1,267,200 bits
        self.assertEqual(metrics["Jaya"]["verses"], 8800)
        self.assertEqual(metrics["Jaya"]["information_bits"], 8800 * 144.0)

        # Accretion ratios
        self.assertAlmostEqual(metrics["expansion_ratio_jaya_to_bharata"], 24000 / 8800, places=4)
        self.assertAlmostEqual(metrics["expansion_ratio_jaya_to_vulgate"], 100000 / 8800, places=4)

    def test_retention_probability_decay(self):
        # Tally decay with 1.5% mutation rate over 40 generations
        p_tally = self.model.retention_probability(generations=40, mutation_rate_per_gen=0.015)
        self.assertTrue(0.0 < p_tally < 0.6)  # should decay significantly: (0.985)^40 ~ 0.545

        # Name decay with 0.2% mutation rate over 40 generations
        p_name = self.model.retention_probability(generations=40, mutation_rate_per_gen=0.002)
        self.assertTrue(p_name > 0.90)  # should remain highly conserved: (0.998)^40 ~ 0.923

    def test_cultural_attractor_fidelity(self):
        # Cultural archetype fidelity should approach 1.0 asymptotically
        f_40 = self.model.cultural_attractor_fidelity(generations=40, selection_bias=0.2)
        f_80 = self.model.cultural_attractor_fidelity(generations=80, selection_bias=0.2)
        self.assertTrue(f_40 > 0.99)
        self.assertTrue(f_80 >= f_40)


class TestDynamicEpistemicLogicModel(unittest.TestCase):
    def setUp(self):
        self.del_model = DynamicEpistemicLogicModel()

    def test_initial_worlds(self):
        self.assertEqual(len(self.del_model.worlds), 5)
        self.assertEqual(len(self.del_model.active_worlds), 5)

    def test_public_announcements(self):
        # Announce P1 = True (Historical core established)
        surviving = self.del_model.public_announcement("P1", True)
        self.assertEqual(surviving, ["w1", "w2", "w3"])

        # Announce P2 = False (Hyperbole rejected)
        surviving = self.del_model.public_announcement("P2", False)
        self.assertEqual(surviving, ["w1", "w2"])

    def test_metaphysical_invariance_proof(self):
        result = self.del_model.test_metaphysical_invariance()
        # Surviving worlds must be w1 and w2
        self.assertEqual(result["surviving_worlds"], ["w1", "w2"])
        # In w1, P3 is True; in w2, P3 is False.
        # Neither Historian nor Theologian knows P3 is True or False with certainty
        self.assertFalse(result["is_metaphysically_decided"])
        self.assertTrue(result["epistemic_resistance_proved"])


class TestTrivikramaTrilemmaModel(unittest.TestCase):
    def setUp(self):
        self.trilemma = TrivikramaTrilemmaModel()

    def test_likelihood_ratios_equal_unity(self):
        # For physical settlement and epigraphy, likelihood ratio is identically 1.0
        # because mortal and avatar hypotheses predict identical empirical traces
        res_settlement = self.trilemma.evaluate_likelihood_ratio("archaeological_settlement")
        self.assertAlmostEqual(res_settlement["likelihood_ratio"], 1.0, places=5)
        self.assertAlmostEqual(res_settlement["log10_bayes_factor"], 0.0, places=5)
        self.assertAlmostEqual(res_settlement["evidential_discriminability"], 0.0, places=5)

        res_epigraphy = self.trilemma.evaluate_likelihood_ratio("epigraphic_veneration")
        self.assertAlmostEqual(res_epigraphy["likelihood_ratio"], 1.0, places=5)
        self.assertAlmostEqual(res_epigraphy["evidential_discriminability"], 0.0, places=5)


class TestSwarmProtocolSafetyFirewall(unittest.TestCase):
    def test_forbidden_verdicts_caught(self):
        bad_statement_1 = "It is proven that Krishna was God."
        is_safe, msg = SwarmProtocolSafetyFirewall.audit_assertion(bad_statement_1)
        self.assertFalse(is_safe)
        self.assertIn("PROTOCOL VIOLATION", msg)

        bad_statement_2 = "We have disproven that Krishna was God."
        is_safe2, msg2 = SwarmProtocolSafetyFirewall.audit_assertion(bad_statement_2)
        self.assertFalse(is_safe2)
        self.assertIn("PROTOCOL VIOLATION", msg2)

    def test_permitted_demarcation_passes(self):
        good_statement = "The metaphysical claim of Krishna's divinity is not empirically decidable, so no verdict is asserted."
        is_safe, msg = SwarmProtocolSafetyFirewall.audit_assertion(good_statement)
        self.assertTrue(is_safe)
        self.assertEqual(msg, "COMPLIANT_ASSERTION")


class TestComprehensiveSynthesis(unittest.TestCase):
    def test_full_synthesis_pipeline(self):
        summary = run_comprehensive_dynamic_synthesis()
        self.assertEqual(summary["status"], "SUCCESS")
        self.assertTrue(summary["firewall_compliance"])
        self.assertTrue(summary["dynamic_epistemic_logic"]["epistemic_resistance_proved"])
        self.assertIn("expansion_ratio_jaya_to_vulgate", summary["stratigraphy"])


if __name__ == "__main__":
    unittest.main()
