#!/usr/bin/env python3
"""
Unit tests for Agent 1 (A001_DarkMatter) Novel Theoretical Discovery:
Gravitational Decoherence & Phase Diffusion of Macroscopic psiDM Solitons
"""

import unittest
import os
import sys
import json
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from a001_phase5_novel_gravitational_decoherence_engine import (
    BaryonicTidalPowerEngine,
    GravitationalDecoherenceEngine,
    SolitonPhaseDiffusionEngine,
    run_novel_gravitational_decoherence_pipeline
)

class TestNovelGravitationalDecoherence(unittest.TestCase):

    def setUp(self):
        self.mw_env = BaryonicTidalPowerEngine(
            name="Milky_Way_Inner_Disk",
            rho_bar_msun_pc3=0.15,
            m_clump_msun=2.0e5,
            v_rel_km_s=150.0,
            lambda_corr_pc=100.0,
            b_min_pc=40.0,
            b_max_pc=1000.0
        )
        self.nuc_env = BaryonicTidalPowerEngine(
            name="Nuclear_Cluster",
            rho_bar_msun_pc3=50.0,
            m_clump_msun=1.0e6,
            v_rel_km_s=200.0,
            lambda_corr_pc=20.0,
            b_min_pc=10.0,
            b_max_pc=200.0
        )
        self.dwarf_env = BaryonicTidalPowerEngine(
            name="Dwarf_Spheroidal",
            rho_bar_msun_pc3=0.005,
            m_clump_msun=1.0e4,
            v_rel_km_s=30.0,
            lambda_corr_pc=50.0,
            b_min_pc=20.0,
            b_max_pc=500.0
        )
        self.decoh_engine = GravitationalDecoherenceEngine(axion_mass_ev=1.0e-22)
        self.diffusion_engine = SolitonPhaseDiffusionEngine(axion_mass_ev=1.0e-22)

    def test_baryonic_tidal_power_hierarchy(self):
        """Verify noise power density scaling across environments."""
        s_g_mw = self.mw_env.compute_acceleration_power_density()
        s_g_nuc = self.nuc_env.compute_acceleration_power_density()
        s_g_dwarf = self.dwarf_env.compute_acceleration_power_density()

        self.assertGreater(s_g_nuc, s_g_mw, "Nuclear cluster must have higher acceleration noise than MW disk")
        self.assertGreater(s_g_mw, s_g_dwarf, "MW disk must have higher acceleration noise than dwarf spheroidal")
        self.assertGreater(s_g_dwarf, 0.0, "Acceleration noise must be strictly positive")

    def test_spatial_decoherence_profile(self):
        """Verify spatial dependence and asymptotic saturation of Gamma_grav(Delta r)."""
        s_phi = self.mw_env.compute_potential_power_density()
        lambda_kpc = 0.10

        gamma_small = self.decoh_engine.decoherence_rate_at_separation(0.01, s_phi, lambda_kpc)
        gamma_mid = self.decoh_engine.decoherence_rate_at_separation(0.10, s_phi, lambda_kpc)
        gamma_large = self.decoh_engine.decoherence_rate_at_separation(10.0, s_phi, lambda_kpc)
        gamma_asymp = self.decoh_engine.asymptotic_decoherence_rate(s_phi)

        self.assertLess(gamma_small, gamma_mid, "Decoherence rate must increase with spatial separation")
        self.assertLess(gamma_mid, gamma_large, "Decoherence rate must increase toward asymptotic limit")
        self.assertAlmostEqual(gamma_large / gamma_asymp, 1.0, places=2, msg="Large r must approach asymptotic rate")

    def test_axion_mass_scaling(self):
        """Verify quadratic scaling of decoherence rate with axion mass Gamma ~ m_a^2."""
        s_phi = self.mw_env.compute_potential_power_density()
        eng_1 = GravitationalDecoherenceEngine(axion_mass_ev=1.0e-22)
        eng_2 = GravitationalDecoherenceEngine(axion_mass_ev=2.0e-22)

        g1 = eng_1.asymptotic_decoherence_rate(s_phi)
        g2 = eng_2.asymptotic_decoherence_rate(s_phi)

        ratio = g2 / g1
        self.assertAlmostEqual(ratio, 4.0, delta=0.01, msg="Gamma_grav must scale as m_a^2")

    def test_soliton_core_expansion_and_retention(self):
        """Verify virial heating expands core and reduces central density."""
        s_g = self.mw_env.compute_acceleration_power_density()
        res = self.diffusion_engine.compute_core_expansion(core_mass_msun=1.0e9, s_g_0=s_g, time_gyr=8.0)

        self.assertGreater(res["perturbed_core_radius_kpc"], res["unperturbed_core_radius_kpc"])
        self.assertGreater(res["core_expansion_factor"], 1.0)
        self.assertLess(res["central_density_retention_fraction"], 1.0)
        self.assertGreater(res["central_density_retention_fraction"], 0.0)

    def test_novel_handover_generation(self):
        """Verify export of phase5_novel_discovery_handover.json."""
        handover = run_novel_gravitational_decoherence_pipeline()
        json_path = os.path.join(os.path.dirname(__file__), "phase5_novel_discovery_handover.json")
        self.assertTrue(os.path.exists(json_path), "Handover JSON must exist")

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data["metadata"]["source_agent"], "A001_DarkMatter")
        self.assertEqual(data["metadata"]["recipient_agent"], "A002_QuantumCosmos")
        self.assertIn("formal_master_equation", data)
        self.assertIn("simulation_metrics", data)
        self.assertIn("astrophysical_consequences", data)
        self.assertIn("bridges_to_agent_2", data)

if __name__ == "__main__":
    unittest.main()
