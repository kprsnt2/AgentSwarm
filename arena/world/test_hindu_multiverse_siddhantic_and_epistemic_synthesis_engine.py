"""
test_hindu_multiverse_siddhantic_and_epistemic_synthesis_engine.py

Unit test suite for Siddhantic astronomical demarcation, Puranic multiverse metrics,
and pan-Dharmic epistemic adjudication.
Uses standard library unittest.
"""

import unittest
import math
from hindu_multiverse_siddhantic_and_epistemic_synthesis_engine import (
    SiddhanticAndPuranicCosmologyEngine,
    YOJANA_TO_KM_SIDDHANTA,
    MAHAYUGA_CIVIL_DAYS,
    LUNAR_REVOLUTIONS_MAHAYUGA,
    LIGHT_YEAR_KM
)


class TestSiddhanticAndPuranicCosmologyEngine(unittest.TestCase):

    def setUp(self):
        self.engine = SiddhanticAndPuranicCosmologyEngine()

    def test_siddhantic_kha_kaksha_derivation(self):
        """Verifies the mathematical derivation of the Brahmanda boundary (Kha-kaksha)."""
        res = self.engine.compute_siddhantic_kha_kaksha()
        
        # 1. Circumference must match 57,753,336 * 324,000 * 1,000
        expected_circ = LUNAR_REVOLUTIONS_MAHAYUGA * 324_000.0 * 1000.0
        self.assertTrue(math.isclose(res["brahmanda_circumference_yojanas"], expected_circ, rel_tol=1e-6))
        self.assertTrue(math.isclose(res["brahmanda_circumference_yojanas"], 1.8712080864e16, rel_tol=1e-5))
        
        # 2. Radius = C / (2*pi)
        expected_radius = expected_circ / (2.0 * math.pi)
        self.assertTrue(math.isclose(res["brahmanda_radius_yojanas"], expected_radius, rel_tol=1e-6))
        
        # 3. Radius in light years must be around 4,050 ly
        self.assertTrue(4000.0 < res["brahmanda_radius_light_years"] < 4100.0)
        
        # 4. Planetary orbits array must contain Moon, Sun, Asterisms, and Kha-kaksha
        orbits = {o.body_name: o for o in res["planetary_orbits"]}
        self.assertIn("Moon (Candra)", orbits)
        self.assertIn("Sun (Surya)", orbits)
        self.assertIn("Brahmanda Boundary (Kha-kaksha)", orbits)
        
        # Sun radius should be larger than Moon radius
        self.assertGreater(orbits["Sun (Surya)"].orbit_radius_yojanas, orbits["Moon (Candra)"].orbit_radius_yojanas)
        # Kha-kaksha radius should be largest
        self.assertGreater(orbits["Brahmanda Boundary (Kha-kaksha)"].orbit_radius_yojanas, orbits["Saturn (Sani)"].orbit_radius_yojanas)

    def test_puranic_sheaths_scaling(self):
        """Verifies the 7 concentric Puranic sheaths and their geometric progression."""
        res = self.engine.compute_puranic_egg_and_sheath_metrics()
        
        # 1. Core diameter must be 50 crore yojanas (5e8)
        self.assertEqual(res["core_diameter_yojanas"], 500_000_000.0)
        self.assertEqual(res["core_radius_yojanas"], 250_000_000.0)
        
        # Core radius in AU should be ~21.5 AU (roughly Uranus distance)
        self.assertTrue(20.0 < res["core_radius_au"] < 25.0)
        
        # 2. Must have exactly 7 sheaths
        sheaths = res["sheaths"]
        self.assertEqual(len(sheaths), 7)
        self.assertEqual(sheaths[0].name_sanskrit, "Ap (Water)")
        self.assertEqual(sheaths[-1].name_sanskrit, "Pradhana (Unmanifest Prakriti)")
        
        # 3. Thickness progression: each is 10x previous
        for i in range(1, len(sheaths)):
            self.assertTrue(math.isclose(sheaths[i].radial_thickness_yojanas, sheaths[i-1].radial_thickness_yojanas * 10.0, rel_tol=1e-6))
            
        # 4. Total cumulative radius must be 2.5e8 + 5e9 + 5e10 + 5e11 + 5e12 + 5e13 + 5e14 + 5e15 = 5.555555...e15
        expected_envelope = 2.5e8 + 5.0e9 * (10.0**7 - 1) / 9.0
        self.assertTrue(math.isclose(res["total_envelope_radius_yojanas"], expected_envelope, rel_tol=1e-5))
        
        # Envelope in light years should be around 7,557 light years
        self.assertTrue(7500.0 < res["total_envelope_radius_light_years"] < 7600.0)

    def test_metric_comparison(self):
        """Verifies the ratio comparisons between Siddhantic and Puranic frameworks."""
        comp = self.engine.compare_siddhantic_and_puranic_scales()
        
        # Ratio of Siddhanta radius to Purana Core radius should be ~1.19e7
        self.assertTrue(1.18e7 < comp["radius_ratio_siddhanta_to_purana_core"] < 1.20e7)
        
        # Ratio of Purana outer sheath to Siddhanta radius should be ~1.86 - 1.87
        self.assertTrue(1.80 < comp["radius_ratio_purana_envelope_to_siddhanta"] < 1.95)

    def test_epistemic_matrix_and_sources(self):
        """Verifies the 5 classical Indian traditions in the epistemic matrix."""
        matrix = self.engine.build_pan_dharmic_epistemic_matrix()
        self.assertEqual(len(matrix), 5)
        
        schools = {m.school_name: m for m in matrix}
        self.assertIn("Mathematical Astronomy (Jyotisa Siddhanta)", schools)
        self.assertIn("Puranic Realist Pluralism (Pauranika / Gaudiya / Vallabha)", schools)
        self.assertIn("Radical Phenomenological Idealism (Yoga-Vasistha / Advaita)", schools)
        self.assertIn("Purva Mimamsa Anti-Cosmogenic Steady-State", schools)
        self.assertIn("Commentarial Concordism / Dual-Sphere Reconciliation", schools)
        
        # Check verdicts
        self.assertEqual(schools["Mathematical Astronomy (Jyotisa Siddhanta)"].multiverse_verdict, "AGNOSTIC_EMPIRICAL")
        self.assertEqual(schools["Puranic Realist Pluralism (Pauranika / Gaudiya / Vallabha)"].multiverse_verdict, "AFFIRMED_PHYSICAL")
        self.assertEqual(schools["Radical Phenomenological Idealism (Yoga-Vasistha / Advaita)"].multiverse_verdict, "AFFIRMED_MENTAL")
        self.assertEqual(schools["Purva Mimamsa Anti-Cosmogenic Steady-State"].multiverse_verdict, "STRICTLY_REJECTED")
        self.assertEqual(schools["Commentarial Concordism / Dual-Sphere Reconciliation"].multiverse_verdict, "HARMONIZED_DUAL")

    def test_concordism_firewall(self):
        """Verifies that the concordism demarcation firewall contains proper protocol enforcement."""
        firewall = self.engine.build_concordism_demarcation_firewall()
        self.assertGreaterEqual(len(firewall["firewall_rules"]), 4)
        self.assertEqual(len(firewall["demarcation_comparisons"]), 3)
        
        for comp in firewall["demarcation_comparisons"]:
            self.assertIn("NON-EQUIVALENCE", comp["protocol_verdict"])
            self.assertIn("modern_model", comp)
            self.assertIn("hindu_concept", comp)
            self.assertIn("ontological_difference", comp)

    def test_comprehensive_report_generation(self):
        """Verifies JSON serializability and comprehensive report generation."""
        import json
        report = self.engine.generate_comprehensive_report()
        self.assertIn("siddhantic_cosmology", report)
        self.assertIn("puranic_cosmology", report)
        self.assertIn("metric_comparison", report)
        self.assertIn("epistemic_matrix", report)
        self.assertIn("concordism_firewall", report)
        
        # Must be valid json
        serialized = json.dumps(report, default=str)
        self.assertGreater(len(serialized), 500)


if __name__ == "__main__":
    unittest.main()
