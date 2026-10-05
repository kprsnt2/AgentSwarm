"""
test_krishna_mahabharata_epistemic_limits_and_demarcation_engine.py
===================================================================
Unit tests verifying the EpistemicLimitsAndDemarcationEngine implementation.
Ensures zero protocol violations, exact mathematical bounds, and strict adherence to the scientific brief.
"""

import unittest
import math
from krishna_mahabharata_epistemic_limits_and_demarcation_engine import (
    EpistemicLimitsAndDemarcationEngine
)


class TestEpistemicLimitsAndDemarcationEngine(unittest.TestCase):

    def setUp(self):
        self.engine = EpistemicLimitsAndDemarcationEngine()

    def test_facet_decomposition_and_count(self):
        """Verify exactly 12 facets: 6 Krishna (K1-K6) and 6 Mahabharata (M1-M6)."""
        facets = self.engine.facets
        self.assertEqual(len(facets), 12)
        krishna_keys = [f"K{i}" for i in range(1, 7)]
        mahabharata_keys = [f"M{i}" for i in range(1, 7)]
        for k in krishna_keys:
            self.assertIn(k, facets)
            self.assertEqual(facets[k]["subject"], "Lord Krishna")
        for k in mahabharata_keys:
            self.assertIn(k, facets)
            self.assertEqual(facets[k]["subject"], "Mahabharata")

    def test_metaphysical_demarcation_and_invariants(self):
        """Verify exactly 3 metaphysical facets (K3, K4, K5) with zero verdicts and infinite bounds."""
        metaphysical_keys = ["K3", "K4", "K5"]
        for k in metaphysical_keys:
            facet = self.engine.facets[k]
            self.assertTrue(facet["is_metaphysical"])
            self.assertEqual(facet["status"], "Undecidable (Metaphysical Boundary)")
            self.assertEqual(facet["bayes_factor_threshold"], math.inf)
            self.assertEqual(self.engine.calculate_likelihood_ratio(k), 1.0)
            self.assertEqual(self.engine.calculate_fisher_information(k), 0.0)
            self.assertEqual(self.engine.calculate_cramer_rao_variance_bound(k), math.inf)

    def test_decidable_facets_classification(self):
        """Verify 9 decidable empirical facets."""
        facets = self.engine.facets
        decidable = [k for k, v in facets.items() if not v["is_metaphysical"]]
        self.assertEqual(len(decidable), 9)

        # Check status groups
        corroborated_or_clarified = [
            k for k, v in facets.items()
            if "Corroborated" in v["status"] or "Clarified" in v["status"]
        ]
        self.assertIn("K2", corroborated_or_clarified)
        self.assertIn("M1", corroborated_or_clarified)
        self.assertIn("M3", corroborated_or_clarified)
        self.assertIn("M4", corroborated_or_clarified)
        self.assertIn("M5", corroborated_or_clarified)

        refuted = [k for k, v in facets.items() if "Refuted" in v["status"]]
        self.assertIn("K6", refuted)
        self.assertIn("M2", refuted)
        self.assertIn("M6", refuted)

        underdetermined = [k for k, v in facets.items() if "Underdetermined" in v["status"]]
        self.assertIn("K1", underdetermined)

    def test_demographic_and_carrying_capacity(self):
        """Verify regional carrying capacity and warrior mobilization limits."""
        res = self.engine.calculate_carrying_capacity(
            area_km2=25000.0,
            arable_fraction=0.08,
            yield_kg_ha=600.0
        )
        self.assertAlmostEqual(res["arable_hectares"], 200000.0)
        self.assertAlmostEqual(res["gross_grain_kg"], 120000000.0)
        self.assertAlmostEqual(res["net_grain_kg"], 90000000.0)
        self.assertGreater(res["sustainable_population"], 360000.0)
        self.assertLess(res["sustainable_population"], 380000.0)
        self.assertGreater(res["max_mobilizable_combatants"], 28000.0)
        self.assertLess(res["max_mobilizable_combatants"], 31000.0)

    def test_akshauhini_logistics(self):
        """Verify troop counts and logistical resource requirements for 18 Akshauhinis."""
        logistics = self.engine.calculate_akshauhini_logistics(18.0)
        self.assertEqual(logistics["total_combatants"], 3936600)
        self.assertEqual(logistics["chariots"], 393660)
        self.assertEqual(logistics["elephants"], 393660)
        self.assertEqual(logistics["cavalry"], 1180980)
        self.assertEqual(logistics["infantry"], 1968300)
        self.assertGreater(logistics["daily_grain_metric_tons"], 4000.0)
        self.assertGreater(logistics["daily_water_liters"], 8.0e7)

    def test_taphonomic_decay(self):
        """Verify taphonomic loss of bone in monsoonal alluvium over 3,000 years."""
        decay = self.engine.evaluate_taphonomic_decay(
            initial_mass_g=1000.0,
            half_life_years=350.0,
            elapsed_years=3000.0
        )
        self.assertLess(decay["preservation_fraction"], 0.003)
        self.assertGreater(decay["preservation_fraction"], 0.0001)

    def test_geochemical_nuclear_refutation(self):
        """Verify natural isotopic baseline and absence of nuclear fission products."""
        geo = self.engine.evaluate_geochemical_nuclear_signatures(
            cs137_bq_kg=0.0,
            sr90_bq_kg=0.0,
            pu239_bq_kg=0.0,
            u235_u238_ratio=0.007253
        )
        self.assertFalse(geo["is_anthropogenic_fission_detected"])
        self.assertAlmostEqual(geo["natural_ratio_deviation"], 0.0, places=5)

    def test_siddhantic_retrograde_calculation(self):
        """Verify Aryabhata's 3600-year retrograde calculation to 3102 BCE."""
        retro = self.engine.evaluate_astronomical_retrocalculation(
            trad_kali_yuga_bce=3102,
            aryabhata_ce=499,
            elapsed_years=3600
        )
        self.assertTrue(retro["is_exact_siddhantic_retrograde"])
        self.assertEqual(retro["historical_year_bce"], 3102)

    def test_bayesian_posterior_invariance_for_metaphysical(self):
        """Verify that when Likelihood Ratio is unity, Bayesian posterior equals prior."""
        for prior in [0.01, 0.25, 0.5, 0.75, 0.99]:
            post = self.engine.calculate_bayesian_posterior(prior=prior, likelihood_ratio=1.0)
            self.assertAlmostEqual(post, prior, places=7)

    def test_protocol_compliance_audit(self):
        """Ensure full compliance with the Metaphysical brief and absence of protocol violations."""
        audit = self.engine.verify_protocol_compliance()
        self.assertTrue(audit["metaphysical_facet_count_correct"])
        self.assertTrue(audit["status_strictly_undecidable"])
        self.assertTrue(audit["fisher_information_zero"])
        self.assertTrue(audit["likelihood_ratio_unity"])
        self.assertTrue(audit["bayes_factor_threshold_infinite"])
        self.assertTrue(audit["zero_metaphysical_verdicts"])
        self.assertTrue(audit["protocol_fully_compliant"])


if __name__ == "__main__":
    unittest.main()
