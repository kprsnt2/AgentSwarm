"""
Unit and Verification Suite for Cosmogenesis Deep Analyzer
Agent: Kepler (A001, Gen 0)
Domain: cosmogenesis (Origin of the universe)
Epistemic Class: Empirical
"""

import unittest
import math
from cosmogenesis_deep_analyzer import (
    bgv_theorem_past_incompleteness,
    lqc_bounce_critical_density,
    gravitino_leptogenesis_window,
    desi_cpl_dark_energy_evaluation,
    cnub_relic_neutrino_properties,
    jwst_highz_baryon_conversion_efficiency,
    master_open_problems_matrix,
    RHO_PLANCK_KG_M3
)

class TestCosmogenesisDeepAnalyzer(unittest.TestCase):

    def test_bgv_past_incompleteness(self):
        """Verify BGV theorem past affine length boundedness."""
        # For inflationary Hubble rate H ~ 1.5e37 s^-1
        h_inf = 1.5e37
        bgv = bgv_theorem_past_incompleteness(h_inf)
        self.assertFalse(bgv["is_past_geodesically_complete"])
        self.assertAlmostEqual(bgv["max_past_affine_parameter_s"], 1.0 / h_inf, places=40)
        self.assertGreater(bgv["max_past_affine_parameter_s"], 0)
        
        # Test error handling on non-expanding spacetime
        with self.assertRaises(ValueError):
            bgv_theorem_past_incompleteness(-1.0)

    def test_lqc_bounce_critical_density(self):
        """Verify Loop Quantum Cosmology bounce density calculation."""
        lqc = lqc_bounce_critical_density()
        # Barbero-Immirzi parameter gamma ~ 0.2375
        self.assertAlmostEqual(lqc["barbero_immirzi_parameter"], 0.2375, places=3)
        # Prefactor fraction ~ 0.41 of Planck density
        self.assertAlmostEqual(lqc["prefactor_fraction_planck"], 0.41, delta=0.02)
        # Density ~ 2.1e96 kg/m^3
        self.assertAlmostEqual(lqc["critical_bounce_density_kg_m3"], 0.41 * RHO_PLANCK_KG_M3, delta=0.1e96)

    def test_gravitino_leptogenesis_window(self):
        """Verify Gravitino-Leptogenesis tension calculation."""
        # For standard 1 TeV gravitino, conflict must be present
        grav_1tev = gravitino_leptogenesis_window(1000.0)
        self.assertTrue(grav_1tev["is_in_conflict"])
        self.assertGreater(grav_1tev["tension_factor"], 10.0)
        
        # For heavy gravitino (> 50 TeV), conflict is resolved
        grav_heavy = gravitino_leptogenesis_window(60000.0)
        self.assertFalse(grav_heavy["is_in_conflict"])
        self.assertLessEqual(grav_heavy["tension_factor"], 1.0)

    def test_desi_cpl_dark_energy(self):
        """Verify DESI 2024 CPL dynamical dark energy parameters."""
        desi = desi_cpl_dark_energy_evaluation(w0=-0.827, wa=-0.750, z_eval=1.0)
        # At z = 1, a = 0.5, w(z=1) = -0.827 - 0.75 * 0.5 = -1.202
        self.assertAlmostEqual(desi["w_at_z"], -1.202, places=3)
        # Crosses phantom divide (-0.827 > -1, but -1.202 < -1)
        self.assertTrue(desi["crosses_phantom_divide"])
        # Statistical deviation from LCDM ~ 3.9 sigma
        self.assertGreater(desi["statistical_deviation_from_LCDM_sigma"], 3.5)
        self.assertLess(desi["statistical_deviation_from_LCDM_sigma"], 4.5)

    def test_cnub_properties_and_exclusion(self):
        """Verify Cosmic Neutrino Background properties and Inverted Hierarchy exclusion."""
        cnb = cnub_relic_neutrino_properties()
        # Temperature ~ 1.945 K
        self.assertAlmostEqual(cnb["T_nu_Kelvin"], 1.945, places=2)
        # Number density per flavor ~ 112 cm^-3
        self.assertAlmostEqual(cnb["n_nu_per_flavor_cm3"], 112.0, delta=2.0)
        # Total density ~ 336 cm^-3
        self.assertAlmostEqual(cnb["n_nu_total_cm3"], 336.0, delta=6.0)
        
        # Inverted hierarchy minimum sum ~ 0.100 eV
        self.assertAlmostEqual(cnb["sum_m_nu_min_inverted_hierarchy_eV"], 0.100, delta=0.005)
        # Normal hierarchy minimum sum ~ 0.059 eV
        self.assertAlmostEqual(cnb["sum_m_nu_min_normal_hierarchy_eV"], 0.059, delta=0.005)
        
        # DESI 2024 upper bound 0.072 eV disfavors Inverted Hierarchy
        self.assertTrue(cnb["inverted_hierarchy_disfavored_by_cosmology"])
        
        # PTOLEMY Tritium capture rate on 100 g is order of ~5-15 events per year
        self.assertGreater(cnb["ptolemy_capture_events_per_year"], 2.0)
        self.assertLess(cnb["ptolemy_capture_events_per_year"], 25.0)

    def test_jwst_baryon_conversion_efficiency(self):
        """Verify JWST high-z galaxy conversion efficiency and anomaly threshold."""
        # Case 1: Standard normal galaxy (M* = 1e8, M_halo = 1e11)
        res_normal = jwst_highz_baryon_conversion_efficiency(10.0, 1e8, 1e11)
        self.assertFalse(res_normal["is_super_efficient"])
        self.assertFalse(res_normal["violates_maximal_efficiency"])
        
        # Case 2: Extreme JWST candidate (M* = 1e9, M_halo = 1.5e10)
        # epsilon = 1e9 / (0.15636 * 1.5e10) = 1e9 / 2.345e9 ~ 0.426
        res_extreme = jwst_highz_baryon_conversion_efficiency(14.32, 1e9, 1.5e10)
        self.assertTrue(res_extreme["is_super_efficient"])
        self.assertFalse(res_extreme["violates_maximal_efficiency"])
        self.assertAlmostEqual(res_extreme["conversion_efficiency_epsilon"], 0.426, delta=0.01)

    def test_master_open_problems_matrix_completeness(self):
        """Verify that all 10 open problems are fully populated with required fields."""
        matrix = master_open_problems_matrix()
        self.assertEqual(len(matrix), 10)
        required_keys = [
            "id", "name", "epistemic_status", "unexplained_phenomenon",
            "resolving_observation", "target_instrument", "critical_metric"
        ]
        for prob in matrix:
            for key in required_keys:
                self.assertIn(key, prob)
                self.assertIsInstance(prob[key], str)
                self.assertGreaterEqual(len(prob[key]), 5)

if __name__ == "__main__":
    unittest.main()
