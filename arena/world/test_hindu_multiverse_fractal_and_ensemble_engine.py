"""
Unit test suite for hindu_multiverse_fractal_and_ensemble_engine.py

Verifies:
1. Fourfold Multiverse Typology consistency and text links.
2. Asynchronous Multiverse Ensemble rates, age distribution, and conservation laws.
3. Fractal Cosmography scaling, Hausdorff dimension, recursive population, and time dilation.
4. Pan-Dharmic Epistemic Adjudication matrix and divergent philosophical stances.
5. Master Tripartite Demarcation Catalog integrity.
"""

import unittest
import math
from hindu_multiverse_fractal_and_ensemble_engine import (
    BRAHMA_LIFETIME_YEARS,
    BRAHMANDA_RADIUS_METERS,
    PARAMANU_RADIUS_METERS,
    MultiverseTypology,
    AsynchronousMultiverseEnsemble,
    FractalCosmographyEngine,
    PanDharmicAdjudication,
    get_master_demarcation_catalog
)

class TestHinduMultiverseFractalAndEnsembleEngine(unittest.TestCase):

    def test_multiverse_typology(self):
        types = MultiverseTypology.list_all()
        self.assertEqual(len(types), 4)
        expected_keys = [
            "TYPE_I_SPATIAL_PARALLEL",
            "TYPE_II_TEMPORAL_CYCLIC",
            "TYPE_III_FRACTAL_RECURSIVE",
            "TYPE_IV_HIERARCHICAL_DIMENSIONAL"
        ]
        for key in expected_keys:
            self.assertIn(key, types)
            profile = MultiverseTypology.get_typology(key)
            self.assertIn("sanskrit_name", profile)
            self.assertIn("concept", profile)
            self.assertIn("primary_texts", profile)
            self.assertGreater(len(profile["primary_texts"]), 0)

        with self.assertRaises(KeyError):
            MultiverseTypology.get_typology("INVALID_TYPE")

    def test_asynchronous_ensemble_dynamics(self):
        ensemble = AsynchronousMultiverseEnsemble()
        self.assertAlmostEqual(ensemble.tau_lifespan, BRAHMA_LIFETIME_YEARS, places=2)
        self.assertGreater(ensemble.n_total, 0.0)

        # Birth/death turnover rate
        rate_year = ensemble.birth_death_rate_per_year()
        # 6.30e11 / 3.1104e14 = ~0.002025 universes/year
        expected_rate = 6.30e11 / 3.1104e14
        self.assertAlmostEqual(rate_year, expected_rate, delta=1e-5)

        rate_sec = ensemble.birth_death_rate_per_second()
        self.assertGreater(rate_year, rate_sec)
        self.assertAlmostEqual(rate_sec, rate_year / (365.25 * 86400.0), delta=1e-15)

        # Turnover period
        self.assertEqual(ensemble.cosmic_turnover_period(), BRAHMA_LIFETIME_YEARS)

        # Age distribution
        bins = ensemble.universe_age_distribution(num_bins=10)
        self.assertEqual(len(bins), 10)
        total_fraction = sum(b["fraction"] for b in bins)
        total_count = sum(b["universe_count"] for b in bins)
        self.assertAlmostEqual(total_fraction, 1.0, places=5)
        self.assertAlmostEqual(total_count, ensemble.n_total, delta=1.0)

        # Asynchrony index
        self.assertEqual(ensemble.ensemble_asynchrony_index(), 1.0)

    def test_fractal_cosmography_engine(self):
        engine = FractalCosmographyEngine()
        s = engine.scale_contraction_ratio()
        # s = r_paramanu / r_brahmanda = 1e-10 / (3.2e12 m) = ~3.125e-23
        self.assertGreater(s, 0.0)
        self.assertLess(s, 1.0e-20)

        # Hausdorff dimension
        d_h = engine.hausdorff_fractal_dimension()
        # log10(1e60) / log10(1 / 3.125e-23) = 60 / 22.505 = ~2.666
        self.assertGreater(d_h, 2.0)
        self.assertLess(d_h, 3.5)

        # Recursive population
        pop_d0 = engine.recursive_population_at_depth(0)
        pop_d1 = engine.recursive_population_at_depth(1)
        pop_d2 = engine.recursive_population_at_depth(2)
        self.assertEqual(pop_d0, 1.0)
        self.assertEqual(pop_d1, 1.0e60)
        self.assertAlmostEqual(pop_d2, 1.0e120, delta=1.0e110)

        # Cognitive time dilation per tier (8 days external vs 100 divine years internal)
        td = engine.cognitive_time_dilation_per_tier()
        # 36525 days / 8 days = 4565.625
        self.assertAlmostEqual(td, 4565.625, places=2)

        # Epistemic demarcation dict
        analysis = engine.epistemic_demarcation_analysis()
        self.assertIn("ancient_doctrine", analysis)
        self.assertIn("indological_firewall", analysis)
        self.assertIn("protocol_violation_check", analysis)

    def test_pan_dharmic_adjudication(self):
        schools = PanDharmicAdjudication.SCHOOLS
        self.assertEqual(len(schools), 5)
        self.assertIn("PURVA_MIMAMSA", schools)
        self.assertIn("BUDDHIST_ABHIDHARMA", schools)
        self.assertIn("JAIN_COSMOLOGY", schools)
        self.assertIn("PURANIC_VEDANTA", schools)
        self.assertIn("TRIKA_SHAIVISM", schools)

        mimamsa = PanDharmicAdjudication.get_school_profile("PURVA_MIMAMSA")
        self.assertIn("REJECTED", mimamsa["multiverse_status"])

        buddhist = PanDharmicAdjudication.get_school_profile("BUDDHIST_ABHIDHARMA")
        self.assertIn("ACCEPTED", buddhist["multiverse_status"])

        matrix = PanDharmicAdjudication.get_divergence_matrix()
        self.assertEqual(len(matrix), 5)

        with self.assertRaises(KeyError):
            PanDharmicAdjudication.get_school_profile("CHARVAKA")

    def test_master_demarcation_catalog(self):
        catalog = get_master_demarcation_catalog()
        self.assertGreaterEqual(len(catalog), 10)
        categories = {item["category"] for item in catalog}
        self.assertIn("Primary Text", categories)
        self.assertIn("Scholarly Consensus", categories)
        self.assertIn("Devotional Claim", categories)

        for item in catalog:
            self.assertIn("citation", item)
            self.assertIn("chronology", item)
            self.assertIn("epistemic_finding", item)


if __name__ == "__main__":
    unittest.main()
