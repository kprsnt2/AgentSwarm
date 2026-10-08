#!/usr/bin/env python3
"""
test_a002_phase6_unified_dark_perturbations.py
=============================================
Unit Test Suite for Agent 2 (A002_QuantumCosmos) Phase 6 Deliverables:
- Linear scalar field perturbations and effective sound speed c_s^2(z).
- Late-time growth suppression ODE and S_8 cosmic shear tension resolution.
- High-z CMB acoustic scale theta_* invariance (< 0.03% discrepancy).
- Z_2 domain wall Planck-suppressed volume bias annihilation.
- Cross-agent handover file integrity and schema validation.
"""

import os
import json
import math
import unittest

from a002_phase6_unified_dark_perturbations_s8 import (
    ScalarFieldPerturbationsEngine,
    LinearGrowthAndS8Engine,
    CMBAcousticScaleEngine,
    DomainWallDynamicsEngine,
    Z_CRIT_FIDUCIAL,
    PLANCK_THETA_STAR_100,
    PLANCK_SIGMA_8,
    PLANCK_S_8,
    OMEGA_M0,
    OMEGA_DE0,
    W0_DESI,
    WA_DESI
)


class TestA002UnifiedDarkPerturbations(unittest.TestCase):
    """
    Test suite for linear perturbations, S_8 tension resolution, CMB acoustic scale,
    and Z_2 domain wall annihilation.
    """

    @classmethod
    def setUpClass(cls):
        cls.pert_engine = ScalarFieldPerturbationsEngine()
        cls.growth_engine = LinearGrowthAndS8Engine()
        cls.cmb_engine = CMBAcousticScaleEngine()
        cls.wall_engine = DomainWallDynamicsEngine()
        cls.handover_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "phase6_perturbations_s8_handover.json"
        )

    # -------------------------------------------------------------------------
    # 1. SCALAR PERTURBATIONS & SOUND SPEED TESTS
    # -------------------------------------------------------------------------
    def test_sound_speed_and_geff(self):
        """
        Verifies:
        - Exact Cold Dark Matter behavior (c_s^2 = 0, G_eff = G) for z >= z_crit.
        - Positive stiffness (c_s^2 > 0) and weakened gravity (G_eff < G) for z < z_crit.
        """
        # Symmetric phase (z >= z_crit)
        for z in [5.0, 3.0, 1.5, Z_CRIT_FIDUCIAL]:
            cs2 = self.pert_engine.effective_sound_speed_squared(z)
            geff = self.pert_engine.effective_gravitational_coupling(z)
            self.assertEqual(cs2, 0.0, f"Sound speed must be 0 for z={z} >= z_crit")
            self.assertEqual(geff, 1.0, f"G_eff / G must be 1.0 for z={z} >= z_crit")

        # Broken phase (z < z_crit)
        for z in [0.7, 0.5, 0.2, 0.0]:
            cs2 = self.pert_engine.effective_sound_speed_squared(z)
            geff = self.pert_engine.effective_gravitational_coupling(z)
            self.assertGreater(cs2, 0.0, f"Sound speed must be > 0 for z={z} < z_crit")
            self.assertLessEqual(cs2, 0.35, f"Sound speed bounded by 0.35 for z={z}")
            self.assertLess(geff, 1.0, f"G_eff / G must be < 1.0 for z={z} < z_crit")
            self.assertGreater(geff, 0.98, f"G_eff / G must remain close to 1 for z={z}")

    # -------------------------------------------------------------------------
    # 2. S_8 GROWTH SUPPRESSION & TENSION RESOLUTION TESTS
    # -------------------------------------------------------------------------
    def test_s8_growth_suppression_and_tension_resolution(self):
        """
        Verifies:
        - Late-time growth suppression ratio D_model / D_LambdaCDM ~ 0.94.
        - S_8 = 0.775 +/- 0.015, matching DES Y3 within < 0.3 sigma.
        - Significant relief of the Planck S_8 tension (> 3 sigma tension resolved).
        """
        res = self.growth_engine.solve_linear_growth()

        growth_ratio = res["growth_suppression_ratio"]
        s8_model = res["unified_model_s_8"]
        pull_des = res["pull_des_y3_sigma"]
        pull_kids = res["pull_kids_1000_sigma"]
        pull_planck = res["pull_planck_sigma"]

        # Growth suppression ratio should be ~ 0.93 - 0.95
        self.assertAlmostEqual(growth_ratio, 0.9396, delta=0.015)

        # S_8 target: 0.775 +/- 0.015
        self.assertTrue(
            0.760 <= s8_model <= 0.790,
            f"S_8 {s8_model:.4f} outside target window [0.760, 0.790]"
        )

        # DES Y3 pull must be well under 0.3 sigma
        self.assertLess(
            pull_des,
            0.30,
            f"Pull with DES Y3 {pull_des:.3f} exceeds 0.3 sigma threshold!"
        )

        # KiDS-1000 pull under 1.0 sigma
        self.assertLess(
            pull_kids,
            1.00,
            f"Pull with KiDS-1000 {pull_kids:.3f} exceeds 1.0 sigma threshold!"
        )

        # Tension with Planck fiducial LambdaCDM must exceed 3.0 sigma
        self.assertGreater(
            pull_planck,
            3.00,
            f"Tension relief {pull_planck:.3f} is less than 3.0 sigma!"
        )

    # -------------------------------------------------------------------------
    # 3. HIGH-Z CMB ACOUSTIC SCALE INVARIANCE TESTS
    # -------------------------------------------------------------------------
    def test_cmb_acoustic_scale_invariance(self):
        """
        Verifies:
        - 100 * theta_* matches Planck 2018 (1.04110) within Delta theta_* / theta_* < 0.03%.
        - Sound horizon r_s(z_*) ~ 144.43 Mpc.
        """
        res = self.cmb_engine.compute_acoustic_angular_scale()

        theta_star_100 = res["theta_star_100"]
        frac_diff = res["fractional_difference"]
        sound_horizon = res["sound_horizon_r_s_mpc"]

        # Fractional discrepancy < 0.03% (i.e. < 0.0003)
        self.assertLess(
            frac_diff,
            0.0003,
            f"CMB acoustic scale fractional error {frac_diff:.6f} exceeds 0.03% target!"
        )

        # Exact Planck alignment to 4 decimal places
        self.assertAlmostEqual(theta_star_100, PLANCK_THETA_STAR_100, places=4)

        # Standard physical sound horizon at recombination
        self.assertAlmostEqual(sound_horizon, 144.43, delta=1.0)
        self.assertTrue(res["within_planck_tolerance"])

    # -------------------------------------------------------------------------
    # 4. Z_2 DOMAIN WALL ANNIHILATION TESTS
    # -------------------------------------------------------------------------
    def test_z2_domain_wall_annihilation(self):
        """
        Verifies:
        - Bias pressure dominates horizon surface tension pressure: p_bias / p_tension >> 1.
        - Annihilation timescale t_ann << t_Hubble.
        - Walls safely collapse without overclosing the universe.
        """
        res = self.wall_engine.compute_wall_properties()

        ratio = res["bias_to_tension_ratio"]
        t_ann = res["annihilation_time_years"]
        t_hubble = res["hubble_time_at_z_crit_years"]
        safe = res["domain_walls_safely_annihilated"]

        self.assertGreater(
            ratio,
            1.0e10,
            f"Bias pressure to tension ratio {ratio:.2e} must be >> 1!"
        )
        self.assertLess(
            t_ann,
            t_hubble * 1.0e-20,
            f"Annihilation time {t_ann:.2e} yr must be << Hubble time {t_hubble:.2e} yr!"
        )
        self.assertTrue(safe, "Domain walls were not safely annihilated!")

    # -------------------------------------------------------------------------
    # 5. HANDOVER JSON INTEGRITY & CROSS-AGENT SCHEMA TESTS
    # -------------------------------------------------------------------------
    def test_handover_json_integrity(self):
        """
        Verifies:
        - phase6_perturbations_s8_handover.json exists and is valid JSON.
        - Ingested metadata from Agent 1 (A001_DarkMatter) is documented.
        - Contains all required sections and parameters.
        """
        self.assertTrue(
            os.path.exists(self.handover_path),
            f"Handover JSON missing at {self.handover_path}"
        )

        with open(self.handover_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIn("metadata", data)
        self.assertEqual(data["metadata"]["source_agent"], "A002_QuantumCosmos")
        self.assertEqual(data["metadata"]["phase"], "Phase 6")
        self.assertTrue(data["metadata"]["handover_from_agent_1_ingested"])

        # Check sub-sections
        self.assertIn("linear_perturbations", data)
        self.assertIn("s8_tension_resolution", data)
        self.assertIn("cmb_acoustic_concordance", data)
        self.assertIn("domain_wall_annihilation", data)

        s8_sec = data["s8_tension_resolution"]
        self.assertAlmostEqual(s8_sec["unified_model_s_8"], 0.7754, delta=0.015)
        self.assertLess(s8_sec["pull_des_y3_sigma"], 0.3)

        cmb_sec = data["cmb_acoustic_concordance"]
        self.assertLess(cmb_sec["fractional_difference"], 0.0003)

        wall_sec = data["domain_wall_annihilation"]
        self.assertTrue(wall_sec["domain_walls_safely_annihilated"])


if __name__ == "__main__":
    unittest.main()
