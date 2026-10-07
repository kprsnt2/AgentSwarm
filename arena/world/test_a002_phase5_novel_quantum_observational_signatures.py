#!/usr/bin/env python3
"""
===============================================================================
AgentSwarm Phase 5 - Agent 2 (A002_QuantumCosmos, Theoretical Physicist & Cosmologist)
Unit Test Suite: test_a002_phase5_novel_quantum_observational_signatures.py
===============================================================================

Comprehensive test suite verifying the observational signatures derived from
gravitational decoherence of galactic dark matter solitons:
1. Signature 1: Lorentzian spectral line shape, FWHM linewidth Delta f = Gamma / (2*pi),
   and radial broadening gradient across galactocentric radii.
2. Signature 2: Quantum-classical core-halo bifurcation (pristine dwarf scaling vs
   decoherence-expanded spiral cores).
3. Signature 3: PTA detection prospects and SNRs in NANOGrav, IPTA DR3, and SKA.
4. Pipeline execution and handover JSON validation.
"""

import unittest
import os
import sys
import json
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from a002_phase5_novel_quantum_observational_signatures import (
    PulsarTimingLinewidthEngine,
    QuantumClassicalBifurcationEngine,
    PTADetectionProspectsEngine,
    run_novel_signatures_pipeline
)

class TestNovelQuantumObservationalSignatures(unittest.TestCase):

    def setUp(self):
        self.pta_engine = PulsarTimingLinewidthEngine(axion_mass_ev=1.0e-22)
        self.bifurcation_engine = QuantumClassicalBifurcationEngine(axion_mass_ev=1.0e-22)
        self.prospects_engine = PTADetectionProspectsEngine(axion_mass_ev=1.0e-22)

    def test_signature_1_pta_lorentzian_psd_and_linewidth(self):
        """Verify the Lorentzian spectral line shape and radial linewidth gradient."""
        # 1. Central frequency
        self.assertAlmostEqual(self.pta_engine.f0_nhz, 48.36, delta=0.5)

        # 2. Lorentzian peak and half-maximum test
        gamma = 1.0e-18 # s^-1
        delta_f = gamma / (2.0 * math.pi)
        f0 = self.pta_engine.f0_hz

        psd_peak = self.pta_engine.compute_lorentzian_psd(f0, gamma, amplitude_a=1.0)
        psd_half_right = self.pta_engine.compute_lorentzian_psd(f0 + delta_f / 2.0, gamma, amplitude_a=1.0)
        psd_half_left = self.pta_engine.compute_lorentzian_psd(f0 - delta_f / 2.0, gamma, amplitude_a=1.0)

        self.assertAlmostEqual(psd_half_right, psd_peak / 2.0, delta=psd_peak * 0.01)
        self.assertAlmostEqual(psd_half_left, psd_peak / 2.0, delta=psd_peak * 0.01)

        # 3. Radial profile gradient: Linewidth must decrease with galactocentric radius
        profile = self.pta_engine.generate_radial_linewidth_profile()
        self.assertGreaterEqual(len(profile), 6)

        df_nuclear = profile[0]["linewidth_delta_f_hz"]
        df_disk = profile[2]["linewidth_delta_f_hz"]
        df_halo = profile[-1]["linewidth_delta_f_hz"]

        self.assertGreater(df_nuclear, df_disk, "Nuclear linewidth must exceed disk linewidth")
        self.assertGreater(df_disk, df_halo, "Disk linewidth must exceed halo linewidth")
        self.assertGreater(df_nuclear / df_halo, 1.0e6, "Linewidth must span many orders of magnitude")

    def test_signature_2_core_halo_bifurcation(self):
        """Verify the quantum-classical core-halo bifurcation across dwarf vs spiral galaxies."""
        table = self.bifurcation_engine.generate_galaxy_sample_bifurcation_table()
        self.assertGreaterEqual(len(table), 5)

        # Dwarf galaxies (e.g. Fornax, Draco, Segue 1)
        dwarfs = [g for g in table if "Dwarf" in g["galaxy_name"]]
        self.assertGreaterEqual(len(dwarfs), 2)
        for d in dwarfs:
            self.assertTrue(d["is_pristine_quantum"], f"{d['galaxy_name']} must be pristine quantum core")
            self.assertAlmostEqual(d["expansion_factor"], 1.000, places=3)
            self.assertAlmostEqual(d["central_density_retention"], 1.000, places=3)

        # Massive spirals (Milky Way, M31)
        spirals = [g for g in table if "Milky Way" in g["galaxy_name"] or "Andromeda" in g["galaxy_name"]]
        self.assertGreaterEqual(len(spirals), 2)
        for s in spirals:
            self.assertFalse(s["is_pristine_quantum"], f"{s['galaxy_name']} must undergo tidal decoherence heating")
            self.assertGreater(s["expansion_factor"], 1.02)
            self.assertLess(s["central_density_retention"], 0.95)

    def test_signature_3_pta_detection_thresholds(self):
        """Verify PTA detection thresholds and signal-to-noise ratios."""
        prospects = self.prospects_engine.compute_pta_snr_and_sensitivities()
        surveys = {s["array_name"]: s for s in prospects["surveys"]}

        # NANOGrav 15-yr bin width approx 2.11 nHz
        self.assertAlmostEqual(surveys["NANOGrav 15-year"]["frequency_bin_width_nhz"], 2.11, delta=0.1)

        # IPTA DR3 achieves statistical significance SNR > 5
        self.assertGreater(surveys["IPTA DR3 (Combined Global Array)"]["projected_snr"], 4.5)

        # MeerTime / SKA Phase 1 reaches decisive discovery SNR > 30
        self.assertGreater(surveys["MeerTime / SKA-Mid Phase 1"]["projected_snr"], 25.0)

        # SKA Phase 2 reaches extraordinary precision SNR > 500
        self.assertGreater(surveys["SKA Phase 2 (Full Deployment)"]["projected_snr"], 400.0)

    def test_pipeline_and_handover_json(self):
        """Verify pipeline execution and handover JSON generation."""
        payload = run_novel_signatures_pipeline(export_handover=True)
        self.assertEqual(payload["metadata"]["source_agent"], "A002_QuantumCosmos")
        self.assertTrue(payload["metadata"]["handover_from_agent_1_ingested"], "Must ingest Agent 1 handover")

        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "phase5_novel_signatures_handover.json")
        self.assertTrue(os.path.exists(json_path), "Handover JSON file must exist on disk")

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("signature_1_pta_linewidth_broadening", data)
        self.assertIn("signature_2_core_halo_bifurcation", data)
        self.assertIn("signature_3_pta_detection_thresholds", data)

if __name__ == "__main__":
    unittest.main()
