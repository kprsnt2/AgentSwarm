"""
test_hindu_multiverse_cosmogenetic_nucleation_engine.py
========================================================
Unit and regression test suite for the Hindu Multiverse Cosmogenetic Nucleation
and Concordism Demarcation computational engine.
"""

import unittest
import math
from hindu_multiverse_cosmogenetic_nucleation_engine import (
    SankhyaPuranicEvolutionEngine,
    BrahmandaMetricEngine,
    MahaVisnuNucleationEngine,
    DemiurgeMultiverseScalingEngine,
    CausalOceanPackingEngine,
    UniversalTransitBarrierEngine,
    ConcordismDemarcationEngine,
    HinduMultiverseMasterSuite,
    KM_PER_AU,
    KM_PER_LY
)


class TestSankhyaPuranicEvolution(unittest.TestCase):
    def test_cosmogenetic_phases_order_and_count(self):
        phases = SankhyaPuranicEvolutionEngine.get_cosmogenetic_phases()
        self.assertEqual(len(phases), 6)
        for idx, phase in enumerate(phases, start=1):
            self.assertEqual(phase.order, idx)
            self.assertTrue(len(phase.sanskrit_name) > 0)
            self.assertTrue("Purana" in phase.primary_citation)

    def test_total_tattvas(self):
        tattvas = SankhyaPuranicEvolutionEngine.get_total_tattvas()
        self.assertEqual(tattvas, 24)


class TestBrahmandaMetricEngine(unittest.TestCase):
    def setUp(self):
        self.engine = BrahmandaMetricEngine()

    def test_inner_core_metrics(self):
        core = self.engine.compute_inner_core_metrics()
        # 50 crore yojanas * 12.874752 km/yojana / 1.4959787e8 km/AU ~ 43.031 AU
        self.assertAlmostEqual(core["core_diameter_au"], 43.03135, places=3)
        self.assertAlmostEqual(core["core_radius_au"], 21.51568, places=3)
        self.assertGreater(core["core_volume_km3"], 0)

    def test_sheath_envelope_scaling(self):
        sheaths = self.engine.compute_sheath_envelope()
        self.assertEqual(len(sheaths), 7)

        # Check 10x geometric progression
        # First sheath thickness = 10 * 500,000,000 = 5,000,000,000 yojanas
        self.assertEqual(sheaths[0].thickness_yojanas, 5_000_000_000.0)
        for i in range(1, 7):
            ratio = sheaths[i].thickness_yojanas / sheaths[i-1].thickness_yojanas
            self.assertAlmostEqual(ratio, 10.0, places=5)

        # Check cumulative outer radius in light years
        # 7th layer cumulative radius is ~7,560 light years (diameter ~15,120 ly)
        outer_r_ly = sheaths[-1].cumulative_radius_ly
        self.assertGreater(outer_r_ly, 7000.0)
        self.assertLess(outer_r_ly, 8000.0)


class TestMahaVisnuNucleationEngine(unittest.TestCase):
    def test_nucleation_dynamics(self):
        metrics = MahaVisnuNucleationEngine.compute_nucleation_dynamics()

        # 1 Mahakalpa = 3.1104e14 solar years
        self.assertEqual(metrics.mahakalpa_years, 3.1104e14)
        # Exhalation = 50 Brahma years = 1.5552e14 years
        self.assertEqual(metrics.exhalation_duration_years, 1.5552e14)

        # Caraka pore count: 35 million
        self.assertEqual(metrics.pore_count_caraka, 35_000_000)

        # 18,000 Kalpas per exhalation
        self.assertEqual(metrics.kalpas_per_exhalation, 18_000.0)

        # Total universes emitted = 35e6 * 18,000 = 6.3e11
        self.assertAlmostEqual(metrics.total_universes_emitted, 6.3e11, delta=1e8)

        # Dilation factor: ~1.5552e14 * 31557600 / 4 ~ 1.227e21
        self.assertGreater(metrics.temporal_dilation_factor_vishnu_to_earth, 1e21)

        # Divine frame nucleation rate: 6.3e11 universes / 4 seconds = 1.575e11 Hz
        self.assertAlmostEqual(metrics.nucleation_rate_divine_frame_hz, 1.575e11, places=1)


class TestDemiurgeMultiverseScaling(unittest.TestCase):
    def setUp(self):
        self.engine = DemiurgeMultiverseScalingEngine()

    def test_canonical_brahma_counts(self):
        vol_scales = self.engine.compute_scaling_series(model="volumetric")
        lin_scales = self.engine.compute_scaling_series(model="linear")
        self.assertEqual(len(vol_scales), 10)
        self.assertEqual(len(lin_scales), 10)

        # Baseline 4-headed Brahma
        self.assertEqual(vol_scales[0].head_count, 4)
        self.assertAlmostEqual(vol_scales[0].relative_volume_to_our_universe, 1.0, places=4)
        self.assertAlmostEqual(lin_scales[0].relative_volume_to_our_universe, 1.0, places=4)

        # 1,000,000-headed Brahma (Koti-mukha)
        koti_vol = vol_scales[-1]
        self.assertEqual(koti_vol.head_count, 1_000_000)
        # Volumetric ratio: 1,000,000 / 4 = 250,000
        self.assertAlmostEqual(koti_vol.relative_volume_to_our_universe, 250_000.0, places=2)
        # Radius multiplier = 250,000^(1/3) ~ 62.996
        self.assertAlmostEqual(koti_vol.core_radius_au / vol_scales[0].core_radius_au, 62.996, places=2)

        # Linear scaling for Koti-mukha
        koti_lin = lin_scales[-1]
        self.assertAlmostEqual(koti_lin.core_radius_au / lin_scales[0].core_radius_au, 250_000.0, places=2)


class TestCausalOceanPacking(unittest.TestCase):
    def test_fcc_and_rcp_packing(self):
        r_universe = 7560.4
        fcc = CausalOceanPackingEngine.compute_cluster_metrics(
            universe_radius_ly=r_universe,
            universe_count=1000,
            packing_type="kepler_fcc"
        )
        rcp = CausalOceanPackingEngine.compute_cluster_metrics(
            universe_radius_ly=r_universe,
            universe_count=1000,
            packing_type="random_close_packing"
        )

        # Kepler FCC packing fraction ~ 0.74048
        self.assertAlmostEqual(fcc.packing_fraction_eta, math.pi / (3.0 * math.sqrt(2.0)), places=5)
        # RCP is 0.64
        self.assertEqual(rcp.packing_fraction_eta, 0.64)

        # Lower density requires larger bounding volume
        self.assertGreater(rcp.cluster_aggregate_volume_ly3, fcc.cluster_aggregate_volume_ly3)
        self.assertGreater(rcp.cluster_bounding_radius_ly, fcc.cluster_bounding_radius_ly)

        # Minimum center-to-center separation is 2 * R
        self.assertAlmostEqual(fcc.mean_center_to_center_separation_ly, 2.0 * r_universe, places=3)


class TestTransitBarrierEngine(unittest.TestCase):
    def test_barrier_penetration_rules(self):
        tensor = UniversalTransitBarrierEngine.get_transit_feasibility_tensor()
        self.assertEqual(len(tensor), 4)

        # Physical body (Adhibhautika) cannot cross sheaths physically
        adhibhautika = tensor[0]
        self.assertFalse(adhibhautika.cross_7_sheaths_physical)
        self.assertFalse(adhibhautika.cross_by_consciousness)
        self.assertTrue(adhibhautika.cross_by_divine_will)

        # Subtle body (Ativahika) can cross by consciousness
        ativahika = tensor[2]
        self.assertTrue(ativahika.cross_by_consciousness)

        # Divine will (Isvariya) can do all
        isvariya = tensor[3]
        self.assertTrue(isvariya.cross_7_sheaths_physical)
        self.assertTrue(isvariya.cross_by_consciousness)
        self.assertTrue(isvariya.cross_by_divine_will)


class TestConcordismDemarcationEngine(unittest.TestCase):
    def test_cdi_scores(self):
        cdi = ConcordismDemarcationEngine.compute_concordism_demarcation_index()
        self.assertEqual(cdi["dimension_count"], 6)

        # Category disparity must be very high (>0.9)
        self.assertGreater(cdi["average_epistemic_category_disparity"], 0.90)

        # Formal mathematical rigor in text must be essentially zero
        self.assertLess(cdi["average_formal_mathematical_rigor"], 0.05)

        # Scientific concordance score must be tiny (<0.01)
        self.assertLess(cdi["scientific_concordance_score"], 0.01)

        # Indological firewall rigor must be high (>0.90)
        self.assertGreater(cdi["indological_firewall_rigor"], 0.90)


class TestHinduMultiverseMasterSuite(unittest.TestCase):
    def test_master_report_completeness(self):
        report = HinduMultiverseMasterSuite.generate_full_metrics_report()
        self.assertIn("core_metrics", report)
        self.assertIn("outer_sheath_radius_ly", report)
        self.assertIn("nucleation_metrics", report)
        self.assertIn("volumetric_scaling", report)
        self.assertIn("linear_scaling", report)
        self.assertIn("fcc_packing", report)
        self.assertIn("cdi_analysis", report)
        self.assertEqual(report["transit_tensor_count"], 4)


if __name__ == "__main__":
    unittest.main()
