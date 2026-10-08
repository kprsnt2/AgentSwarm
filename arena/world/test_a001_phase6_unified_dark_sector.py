#!/usr/bin/env python3
"""
Unit tests for Agent 1 (A001_DarkMatter) Phase 6 Unified Dark Sector Discovery Engine:
- Curvature-induced quantum phase transition
- Spontaneous gravitational symmetry breaking
- Cosmic coincidence problem resolution
- DESI 2024 dynamical dark energy (w0, wa) parameter alignment
- Handover JSON schema and integrity verification
"""

import unittest
import os
import sys
import json
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from a001_phase6_unified_dark_sector_phase_transition import (
    UnifiedDarkSectorAnalytic,
    UnifiedDarkSectorCosmology,
    run_unified_dark_sector_pipeline,
    Z_CRIT_FIDUCIAL,
    OMEGA_DE0,
    OMEGA_DM0
)

class TestUnifiedDarkSectorPhaseTransition(unittest.TestCase):

    def setUp(self):
        self.analytic = UnifiedDarkSectorAnalytic(z_crit=Z_CRIT_FIDUCIAL)
        self.cosmo = UnifiedDarkSectorCosmology(z_crit=Z_CRIT_FIDUCIAL)

    def test_cosmic_curvature_dilution(self):
        """Verify that cosmic Ricci curvature dilutes monotonically as the universe expands."""
        r_z5 = self.analytic.dimensionless_ricci_scalar(5.0)
        r_z1 = self.analytic.dimensionless_ricci_scalar(1.0)
        r_z0 = self.analytic.dimensionless_ricci_scalar(0.0)

        self.assertGreater(r_z5, r_z1, "Curvature at z=5 must exceed curvature at z=1")
        self.assertGreater(r_z1, r_z0, "Curvature at z=1 must exceed curvature at z=0")

        # Verify critical curvature threshold
        r_crit = self.analytic.critical_curvature()
        self.assertGreater(r_crit, r_z0, "Critical curvature must be higher than present day curvature")

    def test_vacuum_energy_emergence_and_coincidence(self):
        """Verify that vacuum energy is zero before z_crit and emerges naturally at z < z_crit."""
        # Before transition (z > z_crit)
        rho_de_early = self.analytic.vacuum_energy_density_ratio(2.0)
        self.assertEqual(rho_de_early, 0.0, "Dark energy density must be exactly zero before phase transition")

        # Today (z = 0)
        rho_de_today = self.analytic.vacuum_energy_density_ratio(0.0)
        self.assertAlmostEqual(rho_de_today, OMEGA_DE0, places=3, msg="Dark energy density today must match Omega_de0")

        # Coincidence ratio resolution
        coincidence_today = self.analytic.coincidence_ratio(0.0)
        self.assertGreater(coincidence_today, 1.0, "rho_DE / rho_DM must be O(1) today")
        self.assertLess(coincidence_today, 5.0, "rho_DE / rho_DM must not exceed O(1) today")

    def test_equation_of_state_transition(self):
        """Verify that dark sector behaves as CDM (w=0) at z >= z_crit and DE at z < z_crit."""
        st_z2 = self.cosmo.state_at_redshift(2.0)
        st_z0 = self.cosmo.state_at_redshift(0.0)

        # Early universe: Pure Cold Dark Matter
        self.assertEqual(st_z2["w_dark"], 0.0, "Dark sector must be pressureless (w=0) at z=2")
        self.assertFalse(st_z2["symmetry_broken"], "Symmetry must be unbroken at z=2")

        # Present universe: Dynamic Dark Energy
        self.assertTrue(st_z0["symmetry_broken"], "Symmetry must be broken at z=0")
        self.assertLess(st_z0["w_dark"], -0.5, "Total dark sector must accelerate expansion at z=0")
        self.assertAlmostEqual(st_z0["w_de"], -0.827, places=2, msg="Dark energy w0 must match DESI best-fit")

    def test_desi_cpl_parameter_fit(self):
        """Verify that fitted CPL parameters align with DESI 2024 Year 1 BAO results."""
        history = self.cosmo.compute_cosmic_history(z_start=3.0, z_end=0.0, num_steps=50)
        desi = self.cosmo.extract_desi_parameters(history)

        self.assertAlmostEqual(desi["w0"], -0.827, places=2, msg="w0 must match DESI -0.827")
        self.assertAlmostEqual(desi["wa"], -0.750, places=2, msg="wa must match DESI -0.750")

    def test_handover_json_generation(self):
        """Verify export of phase6_unified_dark_handover.json."""
        handover = run_unified_dark_sector_pipeline()
        json_path = os.path.join(os.path.dirname(__file__), "phase6_unified_dark_handover.json")
        self.assertTrue(os.path.exists(json_path), "Handover JSON must exist")

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data["metadata"]["source_agent"], "A001_DarkMatter")
        self.assertEqual(data["metadata"]["recipient_agent"], "A002_QuantumCosmos")
        self.assertIn("theoretical_foundation", data)
        self.assertIn("solution_to_cosmic_coincidence", data)
        self.assertIn("desi_dynamical_dark_energy_alignment", data)
        self.assertIn("handover_bridges_for_agent_2", data)

if __name__ == "__main__":
    unittest.main()
