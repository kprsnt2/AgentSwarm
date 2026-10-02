"""
test_hindu_multiverse_micro_macro_and_reception_engine.py

Unit test suite for hindu_multiverse_micro_macro_and_reception_engine.py.

Verifies:
1. Complete 14-Loka anatomical correspondence ordering and coverage (0.0 to 1.0 body height).
2. Piṇḍāṇḍa to Brahmāṇḍa linear and volumetric scaling calculations.
3. Carl Sagan Darasuram Kalpa vs. Earth radiometric age concordance metric.
4. Cidākāśa consciousness-projected recursive multiverse capacity.
5. Three Spaces (Bhūtākāśa, Cittākāśa, Cidākāśa) philosophical demarcation.
6. Reception history catalog completeness and categorization.
7. Concordist claims evaluation and Indological firewall rejection rate.
"""

import math
import unittest

from hindu_multiverse_micro_macro_and_reception_engine import (
    EpistemicCategory,
    MicroMacrocosmEngine,
    SpaceType,
    run_comprehensive_analysis,
)


class TestMicroMacrocosmEngine(unittest.TestCase):
    def setUp(self):
        self.engine = MicroMacrocosmEngine()

    def test_anatomical_lokas_completeness_and_ordering(self):
        lokas = self.engine.anatomical_lokas
        self.assertEqual(len(lokas), 14, "Must contain exactly 14 lokas")

        # Verify ordering from level 1 to 14
        for i, loka in enumerate(lokas):
            self.assertEqual(loka.loka_level, i + 1, f"Loka level should match index + 1: {loka.loka_name}")

        # Verify bottom starts at 0.0 and top ends at 1.0
        self.assertAlmostEqual(lokas[0].height_fraction_min, 0.00, places=2)
        self.assertAlmostEqual(lokas[-1].height_fraction_max, 1.00, places=2)

        # Verify Pātāla is at the soles and Satyaloka is at the crown
        self.assertEqual(lokas[0].loka_name, "Pātāla")
        self.assertIn("Soles", lokas[0].anatomical_region)
        self.assertEqual(lokas[-1].loka_name, "Satyaloka (Brahmaloka)")
        self.assertIn("Crown", lokas[-1].anatomical_region)

        # Verify Bhūloka (Earth) is at the navel / mid-body
        bhuloka = [l for l in lokas if "Bhūloka" in l.loka_name][0]
        self.assertEqual(bhuloka.loka_level, 8)
        self.assertAlmostEqual(bhuloka.height_fraction_min, 0.50, places=2)

    def test_anatomical_scaling_calculation(self):
        scaling = self.engine.compute_anatomical_scaling(human_height_m=1.75)
        # Egg diameter = 5e8 yojana * 12.8 km = 6.4e9 km = 6.4e12 m
        # Ratio = 6.4e12 / 1.75 = 3.65714e12
        self.assertAlmostEqual(scaling["puranic_egg_diameter_km"], 6.4e9, delta=1e7)
        self.assertAlmostEqual(scaling["linear_magnification_factor"], 3.65714e12, delta=1e9)
        self.assertGreater(scaling["log10_linear_magnification"], 12.5)
        self.assertLess(scaling["log10_linear_magnification"], 12.6)
        self.assertGreater(scaling["log10_volumetric_magnification"], 38.0)

    def test_sagan_concordance_metrics(self):
        sagan = self.engine.compute_sagan_concordance_metrics()
        self.assertAlmostEqual(sagan["kalpa_duration_years"], 4.32e9)
        self.assertAlmostEqual(sagan["earth_radiometric_age_years"], 4.543e9)
        # Relative error should be around 4.9%
        self.assertLess(sagan["relative_error_percent"], 5.0)
        self.assertGreater(sagan["relative_error_percent"], 4.5)
        self.assertAlmostEqual(sagan["ratio_kalpa_to_earth_age"], 0.9509, delta=0.005)

    def test_cidakasa_capacity_calculation(self):
        res = self.engine.compute_cidākāśa_multiverse_capacity(
            base_sentient_beings_per_universe=1e14, recursion_depth=3
        )
        self.assertEqual(res["recursion_depth"], 3)
        self.assertEqual(res["spatial_displacement_volume_m3"], 0.0)
        # Depth 3 with base 1e14 means (10^14)^3 = 10^42
        self.assertAlmostEqual(res["log10_total_universes_at_depth"], 42.0, delta=0.1)

    def test_three_spaces_properties(self):
        spaces = self.engine.verify_three_spaces_properties()
        self.assertIn(SpaceType.BHUTAKASA, spaces)
        self.assertIn(SpaceType.CITTAKASA, spaces)
        self.assertIn(SpaceType.CIDAKASA, spaces)

        # Check key differentiating qualities
        self.assertIn("material element", spaces[SpaceType.BHUTAKASA]["ontological_status"])
        self.assertIn("subtle body", spaces[SpaceType.CITTAKASA]["ontological_status"])
        self.assertIn("pure consciousness", spaces[SpaceType.CIDAKASA]["ontological_status"])

    def test_reception_history_catalog(self):
        milestones = self.engine.reception_milestones
        self.assertGreaterEqual(len(milestones), 7)
        years = [m.year for m in milestones]
        self.assertEqual(years, sorted(years), "Milestones should be chronologically ordered")

        # Verify prominent historical figures
        figures = [m.figure_or_movement for m in milestones]
        self.assertTrue(any("Jones" in f for f in figures))
        self.assertTrue(any("Vivekananda" in f for f in figures))
        self.assertTrue(any("Oppenheimer" in f for f in figures))
        self.assertTrue(any("Sagan" in f for f in figures))
        self.assertTrue(any("Capra" in f for f in figures))

    def test_concordist_evaluations_and_demarcation(self):
        evals = self.engine.concordist_evaluations
        self.assertEqual(len(evals), 5)

        # Only the historical convergence (Sagan) should pass demarcation
        passes = [e for e in evals if e.demarcation_pass]
        failures = [e for e in evals if not e.demarcation_pass]

        self.assertEqual(len(passes), 1)
        self.assertEqual(passes[0].claim_id, "CLAIM-05-SAGAN-KALPA-NUMERICAL-ACCORD")
        self.assertEqual(len(failures), 4)

        # Verify rejection of quantum and string concordism
        wormhole_claim = [e for e in failures if "WORMHOLES" in e.claim_id][0]
        self.assertIn("Superficial Metaphorical Equivocation", wormhole_claim.fallacy_type)

        mwi_claim = [e for e in failures if "EVERETT-MWI" in e.claim_id][0]
        self.assertIn("Category Mistake", mwi_claim.fallacy_type)

    def test_comprehensive_runner(self):
        res = run_comprehensive_analysis()
        self.assertIn("scaling", res)
        self.assertIn("sagan", res)
        self.assertIn("cidakasa", res)
        self.assertIn("spaces", res)
        self.assertIn("audit", res)
        self.assertEqual(res["audit"]["total_anatomical_lokas"], 14)


if __name__ == "__main__":
    unittest.main()
