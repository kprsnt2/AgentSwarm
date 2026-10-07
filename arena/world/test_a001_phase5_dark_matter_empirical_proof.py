#!/usr/bin/env python3
"""
Unit tests for Agent 1 (A001_DarkMatter) Phase 5 Empirical Proof Engine:
- Galactic dynamics (Keplerian decline vs NFW vs MOND)
- Bullet Cluster lensing offset significance & MOND center-of-mass failure
- Cosmological CMB peak ratios, BBN light element bounds, and structure growth
- Candidate constraints (LZ 2024 WIMP bound, PBH microlensing, and psiDM BEC properties)
- Handover JSON schema and integrity verification
"""

import unittest
import os
import sys
import json
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from a001_phase5_dark_matter_empirical_proof import (
    GalacticDynamicsEngine,
    BulletClusterEngine,
    CosmologicalProofEngine,
    CandidateEvaluationEngine,
    run_master_empirical_proof_pipeline,
    G_SI,
    A0_MOND_SI
)

class TestDarkMatterEmpiricalProof(unittest.TestCase):

    def setUp(self):
        self.gal = GalacticDynamicsEngine()
        self.bullet = BulletClusterEngine()
        self.cosmo = CosmologicalProofEngine()
        self.candidate = CandidateEvaluationEngine()

    def test_galactic_dynamics_keplerian_decline(self):
        """Verify that Keplerian velocity declines as 1/sqrt(r) while total velocity flattens."""
        v_kep_8 = self.gal.v_kepler_km_s(8.5)
        v_kep_50 = self.gal.v_kepler_km_s(50.0)
        self.assertGreater(v_kep_8, v_kep_50, "Keplerian velocity must decline with radius")

        # Check total velocity with NFW halo
        v_tot_8 = self.gal.v_total_dm_km_s(8.5)
        v_tot_50 = self.gal.v_total_dm_km_s(50.0)
        self.assertGreater(v_tot_50, 180.0, "Total velocity at 50 kpc must remain elevated (>180 km/s)")
        self.assertGreater(v_tot_50, v_kep_50 + 100.0, "Dark matter must produce > 100 km/s deficit at 50 kpc")

        # Test MOND behavior in deep MOND regime
        v_mond_50 = self.gal.v_mond_km_s(50.0)
        self.assertGreater(v_mond_50, v_kep_50, "MOND velocity must be greater than Keplerian at low acceleration")

    def test_bullet_cluster_decoupling(self):
        """Verify the 8-sigma+ spatial separation between collisional gas and collisionless lensing mass."""
        results = self.bullet.compute_offset_significance()
        self.assertGreaterEqual(results["subcluster_offset_sigma"], 8.0, "Subcluster offset must exceed 8 sigma")
        self.assertGreater(results["gas_share_of_baryons_percent"], 80.0, "Gas must constitute > 80% of baryonic mass")
        self.assertGreater(results["dark_matter_mass_fraction_percent"], 80.0, "Dark matter must constitute > 80% of cluster mass")
        self.assertGreater(results["mond_rejection_significance_sigma"], 10.0, "MOND baryonic center of mass must fail at > 10 sigma")

    def test_cosmological_cmb_and_bbn(self):
        """Verify CMB acoustic peak ratios and BBN Deuterium bounds."""
        cmb = self.cosmo.cmb_acoustic_peak_ratios()
        bbn = self.cosmo.bbn_nucleosynthesis_bounds()
        growth = self.cosmo.structure_formation_growth_growth()

        # Dark to baryon ratio ~ 5.36
        self.assertAlmostEqual(cmb["omega_c_over_omega_b"], 5.3643, delta=0.01)
        self.assertGreater(cmb["baryon_only_rejection_sigma"], 30.0, "Baryon-only CMB must be rejected at > 30 sigma")

        # BBN Concordance
        self.assertLess(bbn["planck_bbn_concordance_pull_sigma"], 0.5, "Planck and BBN must agree within 0.5 sigma")
        self.assertGreater(bbn["all_matter_as_baryons_depletion_factor"], 10.0, "All-baryon model must severely deplete Deuterium")

        # Structure formation
        self.assertFalse(growth["baryon_only_collapsed"], "Baryons alone cannot collapse into non-linear structure")
        self.assertTrue(growth["cdm_collapsed"], "CDM must successfully undergo non-linear collapse by z=0")

    def test_axion_bec_quantum_properties(self):
        """Verify ultra-light axion BEC scales and quantum pressure."""
        props = self.candidate.compute_axion_quantum_wave_properties(velocity_dispersion_km_s=30.0, soliton_core_mass_msun=1.0e9)
        self.assertGreater(props["de_broglie_wavelength_kpc"], 1.0, "de Broglie wavelength must be > 1 kpc")
        self.assertGreater(props["soliton_core_radius_kpc"], 0.5, "Core radius must be > 0.5 kpc")
        self.assertTrue(props["is_macroscopic_bec"], "Must form macroscopic Bose-Einstein condensate")
        self.assertGreater(props["central_quantum_potential_j_per_kg"], 0.0, "Central quantum potential must be repulsive (positive)")

    def test_handover_json_generation(self):
        """Verify the generation and structure of phase5_dark_matter_handover.json."""
        handover = run_master_empirical_proof_pipeline()
        json_path = os.path.join(os.path.dirname(__file__), "phase5_dark_matter_handover.json")
        self.assertTrue(os.path.exists(json_path), "Handover JSON file must exist")

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data["metadata"]["source_agent"], "A001_DarkMatter")
        self.assertEqual(data["metadata"]["recipient_agent"], "A002_QuantumCosmos")
        self.assertIn("empirical_pillars", data)
        self.assertIn("candidate_viability_matrix", data)
        self.assertIn("handover_bridge_to_agent_2", data)

if __name__ == "__main__":
    unittest.main()
