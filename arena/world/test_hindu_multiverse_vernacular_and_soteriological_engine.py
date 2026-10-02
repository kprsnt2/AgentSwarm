"""
test_hindu_multiverse_vernacular_and_soteriological_engine.py

Unit test verification suite for Hindu Multiverse Vernacular Narratives,
Aṣṭāvaraṇa Sheath Geometries, and Trans-Universal Soteriological Cartography.
Uses Python's standard library unittest.
"""

import math
import unittest
from hindu_multiverse_vernacular_and_soteriological_engine import (
    KakabhusundiTimeDilation,
    AstavaranaGeometryEngine,
    AstavaranaSheath,
    BrihadBhagavatamrtaCartography,
    TransUniversalStation,
    OntologicalDomain,
    GunaProfile,
    CounterpartOntologyEngine,
    VernacularConcordismAuditor,
    AuditStatus
)


class TestKakabhusundiTimeDilation(unittest.TestCase):
    def setUp(self):
        self.kd = KakabhusundiTimeDilation()

    def test_time_dilation_metrics(self):
        self.assertEqual(self.kd.subjective_kalpas, 100.0)
        self.assertEqual(self.kd.total_subjective_years(), 4.32e11)
        
        # Verify subjective seconds calculation
        expected_sec = 4.32e11 * 31557600.0
        self.assertAlmostEqual(self.kd.total_subjective_seconds() / 1e19, expected_sec / 1e19, places=4)
        
        # Verify external seconds (0.5 ksana * 1.6 s = 0.8 s)
        self.assertEqual(self.kd.total_external_seconds(), 0.8)
        
        # Verify extreme dilation ratio ~ 1.704e19
        gamma = self.kd.time_dilation_factor()
        self.assertGreater(gamma, 1.7e19)
        self.assertLess(gamma, 1.71e19)
        
    def test_lorentz_beta_near_unity(self):
        beta = self.kd.equivalent_lorentz_beta()
        # beta should be effectively indistinguishable from 1.0 in float precision
        self.assertGreater(beta, 0.999999999999999)
        self.assertGreater(self.kd.planck_time_ratio(), 1e42)


class TestAstavaranaGeometryEngine(unittest.TestCase):
    def setUp(self):
        self.engine = AstavaranaGeometryEngine()

    def test_sheath_count_and_order(self):
        sheaths = self.engine.compute_sheaths()
        self.assertEqual(len(sheaths), 8)
        self.assertEqual(sheaths[0].element_sanskrit, "Bhūmi (Prthvī)")
        self.assertEqual(sheaths[7].element_sanskrit, "Pradhāna (Prakṛti)")
        
    def test_model_a_exponential_progression(self):
        sheaths = self.engine.compute_sheaths()
        # In Model A, thickness grows by 10x each sheath
        for i in range(1, 8):
            ratio = sheaths[i].thickness_model_a_yojanas / sheaths[i-1].thickness_model_a_yojanas
            self.assertAlmostEqual(ratio, 10.0, places=4)
            
    def test_model_a_astronomical_envelope(self):
        r_yoj, r_km, r_ly = self.engine.total_outer_radius_model_a()
        # Total outer radius should be ~ 37,580 light years
        self.assertGreater(r_ly, 35000.0)
        self.assertLess(r_ly, 40000.0)
        self.assertGreater(r_km, 3.5e17)
        
        # Volumetric ratio should be massive (> 1e20)
        self.assertGreater(self.engine.volumetric_expansion_ratio_model_a(), 1e24)

    def test_model_b_dimensions(self):
        r_yoj, r_km, r_ly = self.engine.total_outer_radius_model_b()
        # Model B is based on 8 * 10 * Core Diameter = 4.0e10 yojanas + 2.5e8 = 4.025e10 yojanas
        self.assertAlmostEqual(r_yoj / 1e10, 4.025, places=3)
        self.assertGreater(r_ly, 0.05)
        self.assertLess(r_ly, 0.06)


class TestBrihadBhagavatamrtaCartography(unittest.TestCase):
    def setUp(self):
        self.bb = BrihadBhagavatamrtaCartography()

    def test_station_count_and_progression(self):
        stations = self.bb.get_stations()
        self.assertEqual(len(stations), 10)
        self.assertTrue(stations[0].name_sanskrit.startswith("Bhūloka"))
        self.assertEqual(stations[-1].name_sanskrit, "Goloka Vṛndāvana")
        
    def test_domain_partitioning(self):
        partition = self.bb.get_domain_partition()
        # 4 in material core (Bhuloka, Svarga, Mahas/Janas/Tapas, Satyaloka)
        self.assertEqual(partition[OntologicalDomain.MATERIAL_CORE.value], 4)
        # 1 in material sheath (Astavarana)
        self.assertEqual(partition[OntologicalDomain.MATERIAL_SHEATH.value], 1)
        # 2 in trans-material boundary (Viraja, Sivaloka)
        self.assertEqual(partition[OntologicalDomain.TRANS_MATERIAL_BOUNDARY.value], 2)
        # 1 in non-dual effulgence (Brahmajyoti)
        self.assertEqual(partition[OntologicalDomain.NON_DUAL_EFFULGENCE.value], 1)
        # 2 in spiritual multiverse (Vaikuntha, Goloka)
        self.assertEqual(partition[OntologicalDomain.SPIRITUAL_MULTIVERSE.value], 2)

    def test_guna_transformation(self):
        stations = self.bb.get_stations()
        # Earth is Rajas dominant, Vaikuntha is Suddha-Sattva
        self.assertEqual(stations[0].guna_state, GunaProfile.RAJAS_DOMINANT)
        self.assertEqual(stations[8].guna_state, GunaProfile.SUDDHA_SATTVA)
        self.assertEqual(stations[9].guna_state, GunaProfile.SUDDHA_SATTVA)
        # Viraja is Nirguna
        self.assertEqual(stations[5].guna_state, GunaProfile.NIRGUNA)


class TestCounterpartOntologyEngine(unittest.TestCase):
    def setUp(self):
        self.engine = CounterpartOntologyEngine()

    def test_comparison_dimensions(self):
        comparisons = self.engine.get_comparisons()
        self.assertEqual(len(comparisons), 4)
        features = [c.feature for c in comparisons]
        self.assertIn("Nature of Plural Worlds", features)
        self.assertIn("Observer Duplication / Identity", features)
        self.assertIn("Trans-Universal Traversal", features)
        self.assertIn("Temporal Asymmetry / Dilation", features)


class TestVernacularConcordismAuditor(unittest.TestCase):
    def setUp(self):
        self.auditor = VernacularConcordismAuditor()

    def test_audit_counts(self):
        records = self.auditor.audit_all()
        self.assertEqual(len(records), 5)
        summary = self.auditor.get_summary_statistics()
        self.assertEqual(summary["CATEGORY_ERROR"], 3)
        self.assertEqual(summary["REJECTED"], 1)
        self.assertEqual(summary["ACCEPTED"], 1)

    def test_specific_claim_verdicts(self):
        records = {r.claim_id: r for r in self.auditor.audit_all()}
        self.assertEqual(records["AUDIT-VERN-01-KAKABHUSUNDI-RELATIVITY"].epistemic_status, AuditStatus.CATEGORY_ERROR)
        self.assertEqual(records["AUDIT-VERN-02-ASTAVARANA-BLACK-HOLES"].epistemic_status, AuditStatus.REJECTED)
        self.assertEqual(records["AUDIT-VERN-04-RAMCARITMANAS-VERNACULAR-DIFFUSION"].epistemic_status, AuditStatus.ACCEPTED)


if __name__ == "__main__":
    unittest.main()
