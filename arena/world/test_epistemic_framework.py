"""
test_epistemic_framework.py

Unit and invariant test suite for epistemic framework analyzer.
Verifies numerical precision of cosmological chronologies and enforcement
of the epistemic firewall separating historical from metaphysical claims.
"""

import unittest
from epistemic_framework_analyzer import (
    PuranicCosmologyCalculator,
    EpistemicMatrix,
    EpistemicClass,
    EmpiricalAdjudicability,
    Pramana
)


class TestPuranicCosmology(unittest.TestCase):

    def setUp(self):
        self.calc = PuranicCosmologyCalculator()
        self.cycles = self.calc.get_cycle_breakdown()
        self.astro = self.calc.compare_with_astrophysics()

    def test_yuga_proportions(self):
        # Verify 4:3:2:1 ratio
        kali = self.cycles["kali_yuga_yr"]
        dvapara = self.cycles["dvapara_yuga_yr"]
        treta = self.cycles["treta_yuga_yr"]
        krita = self.cycles["krita_yuga_yr"]

        self.assertEqual(dvapara, 2 * kali)
        self.assertEqual(treta, 3 * kali)
        self.assertEqual(krita, 4 * kali)
        self.assertEqual(self.cycles["mahayuga_yr"], 4_320_000)

    def test_kalpa_and_brahma_lifetimes(self):
        # 1 Kalpa = 1000 Mahayugas = 4.32 Ga
        self.assertEqual(self.cycles["kalpa_day_yr"], 4_320_000_000)
        # 1 Brahma Day + Night = 2 Kalpas = 8.64 Ga
        self.assertEqual(self.cycles["brahma_nycthemeron_yr"], 8_640_000_000)
        # 1 Brahma Year = 360 * 8.64 Ga = 3.1104e12 yr
        self.assertEqual(self.cycles["brahma_year_yr"], 3_110_400_000_000)
        # 100 Brahma Years = 3.1104e14 yr (311.04 trillion years)
        self.assertEqual(self.cycles["brahma_lifetime_yr"], 311_040_000_000_000)

    def test_astrophysical_comparisons(self):
        # Ensure delta calculation is numerically sound
        self.assertAlmostEqual(self.astro["kalpa_duration_gyr"], 4.32, places=3)
        self.assertAlmostEqual(self.astro["earth_age_gyr"], 4.543, places=3)
        self.assertTrue(0 < self.astro["delta_kalpa_earth_pct"] < 10)


class TestEpistemicFirewall(unittest.TestCase):

    def setUp(self):
        self.matrix = EpistemicMatrix()

    def test_metaphysical_claims_are_undecidable(self):
        """Invariant: Metaphysical claims must NEVER be marked as empirically decidable."""
        meta_claims = self.matrix.get_claims_by_class(EpistemicClass.METAPHYSICAL_ONTOLOGICAL)
        self.assertGreater(len(meta_claims), 0)
        for claim in meta_claims:
            self.assertEqual(
                claim.adjudicability,
                EmpiricalAdjudicability.UNDECIDABLE,
                f"Claim {claim.claim_id} violates epistemic firewall: marked decidable!"
            )
            self.assertIsNotNone(claim.metaphysical_insulation_reason)
            self.assertIsNone(claim.empirical_test, f"Claim {claim.claim_id} has invalid empirical test!")

    def test_historical_claims_have_empirical_tests(self):
        """Invariant: Historical claims must have defined empirical tests and be decidable."""
        hist_claims = self.matrix.get_claims_by_class(EpistemicClass.HISTORICAL_TEXTUAL)
        self.assertGreater(len(hist_claims), 0)
        for claim in hist_claims:
            self.assertEqual(claim.adjudicability, EmpiricalAdjudicability.DECIDABLE)
            self.assertIsNotNone(claim.empirical_test)
            self.assertIsNone(claim.metaphysical_insulation_reason)

    def test_pramana_integrity(self):
        """Historical claims must use empirical pramanas (Pratyaksha/Anumana)."""
        hist_claims = self.matrix.get_claims_by_class(EpistemicClass.HISTORICAL_TEXTUAL)
        for claim in hist_claims:
            self.assertIn(Pramana.PRATYAKSHA, claim.relevant_pramanas)
            self.assertIn(Pramana.ANUMANA, claim.relevant_pramanas)


if __name__ == "__main__":
    unittest.main()
