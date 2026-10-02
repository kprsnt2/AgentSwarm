"""
test_cosmogenesis_master_decision_engine.py
===========================================
Unit test verification suite for cosmogenesis_master_decision_engine.py.
"""

import unittest
import math
from cosmogenesis_master_decision_engine import (
    MasterConstants,
    SingularityAndQuantumBounce,
    WeylCurvatureAndEntropy,
    InflationAndSwampland,
    BaryogenesisAndNeutrinoHierarchy,
    DarkSectorAndHubbleSirens,
    LithiumAndTopologyEngine,
    MasterObservationalDecisionRegistry,
    execute_master_consilience_synthesis
)


class TestCosmogenesisMasterDecisionEngine(unittest.TestCase):
    """Test suite for master decision engine."""

    def test_constants(self):
        self.assertAlmostEqual(MasterConstants.c, 299792458.0)
        self.assertAlmostEqual(MasterConstants.hbar, 1.054571817e-34)
        self.assertTrue(MasterConstants.G > 6.67e-11)
        self.assertTrue(MasterConstants.rho_Pl_kg_m3 > 5.0e96)

    def test_borde_guth_vilenkin_theorem(self):
        H_avg = 2.2e-18  # s^-1 ~ 68 km/s/Mpc
        bgv = SingularityAndQuantumBounce.borde_guth_vilenkin_theorem(H_avg)
        self.assertTrue(bgv["is_past_geodesically_incomplete"])
        self.assertTrue(bgv["max_affine_parameter_Gyr"] > 0)
        with self.assertRaises(ValueError):
            SingularityAndQuantumBounce.borde_guth_vilenkin_theorem(-1.0)

    def test_loop_quantum_cosmology_bounce(self):
        lqc = SingularityAndQuantumBounce.loop_quantum_cosmology_bounce(barbero_immirzi=0.2375)
        self.assertTrue(lqc["physical_singularity_avoided"])
        self.assertTrue(0.3 < lqc["critical_density_fraction_of_planck"] < 0.6)
        
        # Test at density equal to or above critical density
        lqc_bounce = SingularityAndQuantumBounce.loop_quantum_cosmology_bounce(
            energy_density_initial_kg_m3=lqc["critical_bounce_density_kg_m3"] * 1.05
        )
        self.assertTrue(lqc_bounce["is_at_bounce_point"])
        self.assertEqual(lqc_bounce["modified_Hubble_rate_s_inv"], 0.0)

    def test_penrose_weyl_fine_tuning(self):
        penrose = WeylCurvatureAndEntropy.compute_penrose_fine_tuning()
        self.assertTrue(penrose["maximum_black_hole_entropy_kB"] > 1.0e123)
        self.assertTrue(penrose["log10_exponent_fine_tuning"] > 7.0e122)

    def test_starobinsky_model_and_lyth(self):
        starobinsky = InflationAndSwampland.starobinsky_r2_model(N_efolds=60.0)
        self.assertAlmostEqual(starobinsky["n_s"], 1.0 - 2.0 / 60.0, places=4)
        self.assertAlmostEqual(starobinsky["r"], 12.0 / 3600.0, places=5)
        self.assertTrue(starobinsky["n_T"] < 0)  # Standard inflation tensor tilt is red
        
        lyth = InflationAndSwampland.lyth_bound(starobinsky["r"], N_efolds=60.0)
        self.assertTrue(lyth > 1.0)  # Super-Planckian field excursion

    def test_trans_planckian_censorship(self):
        tcc = InflationAndSwampland.trans_planckian_censorship_conjecture()
        self.assertTrue(tcc["TCC_r_upper_bound"] <= 1.0e-20)
        self.assertTrue(tcc["TCC_max_N_efolds"] > 0)

    def test_sakharov_ckm_shortfall(self):
        sakharov = BaryogenesisAndNeutrinoHierarchy.sakharov_ckm_shortfall()
        self.assertTrue(sakharov["shortfall_factor"] > 1.0e10)
        self.assertTrue(sakharov["orders_of_magnitude_shortfall"] >= 10.0)

    def test_neutrino_hierarchy(self):
        nu = BaryogenesisAndNeutrinoHierarchy.neutrino_mass_hierarchy_bounds()
        self.assertTrue(0.055 < nu["sum_m_nu_NH_min_eV"] < 0.065)
        self.assertTrue(0.095 < nu["sum_m_nu_IH_min_eV"] < 0.105)
        self.assertTrue(nu["inverted_hierarchy_excluded_by_cosmology"])

    def test_desi_dark_energy_and_growth(self):
        w_today = DarkSectorAndHubbleSirens.desi_2024_w0_wa_model(a=1.0)
        self.assertAlmostEqual(w_today, -0.827, places=3)
        w_early = DarkSectorAndHubbleSirens.desi_2024_w0_wa_model(a=0.5)
        self.assertAlmostEqual(w_early, -0.827 + -0.75 * 0.5, places=3)
        
        gamma_GR = DarkSectorAndHubbleSirens.modified_gravity_growth_rate(Omega_m_z=0.3, growth_index_gamma=0.55)
        gamma_DGP = DarkSectorAndHubbleSirens.modified_gravity_growth_rate(Omega_m_z=0.3, growth_index_gamma=0.68)
        self.assertTrue(gamma_GR > gamma_DGP)

    def test_standard_siren_precision(self):
        sirens_10 = DarkSectorAndHubbleSirens.standard_siren_hubble_precision(N_sirens=10)
        self.assertFalse(sirens_10["is_tension_definitively_resolved"])
        
        sirens_50 = DarkSectorAndHubbleSirens.standard_siren_hubble_precision(N_sirens=50)
        self.assertTrue(sirens_50["is_tension_definitively_resolved"])
        self.assertTrue(sirens_50["discrimination_power_sigma"] >= 5.0)

    def test_lithium_tension(self):
        lithium = LithiumAndTopologyEngine.analyze_lithium_tension()
        self.assertTrue(2.9 < lithium["discrepancy_factor"] < 3.0)
        self.assertTrue(lithium["statistical_tension_sigma"] > 9.0)

    def test_topology_circles(self):
        top = LithiumAndTopologyEngine.evaluate_cosmic_topology_circles_bound(R_LSS_Gpc=14.0)
        self.assertTrue(top["is_compact_scale_larger_than_horizon"])
        self.assertTrue(top["lower_bound_topology_scale_Gpc"] >= 27.0)

    def test_master_observational_registry(self):
        registry = MasterObservationalDecisionRegistry()
        self.assertEqual(len(registry.entries), 10)
        
        # Test specific entry retrieval
        mop1 = registry.get_entry("MOP-01")
        self.assertIsNotNone(mop1)
        self.assertIn("Initial Singularity", mop1.frontier_title)
        
        mop8 = registry.get_entry("MOP-08")
        self.assertIsNotNone(mop8)
        self.assertIn("Hubble Tension", mop8.frontier_title)
        
        summary = registry.export_summary_table()
        self.assertEqual(len(summary), 10)

    def test_execute_master_consilience_synthesis(self):
        res = execute_master_consilience_synthesis()
        self.assertEqual(res["total_master_open_problems"], 10)
        self.assertTrue(res["bgv_theorem"]["is_past_geodesically_incomplete"])
        self.assertTrue(res["lqc_bounce"]["physical_singularity_avoided"])


if __name__ == "__main__":
    unittest.main()
