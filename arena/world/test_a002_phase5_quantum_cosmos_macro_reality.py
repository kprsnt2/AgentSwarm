#!/usr/bin/env python3
"""
===============================================================================
AgentSwarm Phase 5 - Agent 2 (A002_QuantumCosmos, Theoretical Physicist & Cosmologist)
Unit Test Suite: test_a002_phase5_quantum_cosmos_macro_reality.py
===============================================================================

Comprehensive test suite verifying all theoretical derivations, empirical calculations,
and predictions established in a002_phase5_quantum_cosmos_macro_reality.py:
1. Pillar 1: Inflationary quantum vacuum fluctuations, Mukhanov-Sasaki power spectrum,
   and 8.35-sigma rejection of scale invariance (Planck 2018).
2. Pillar 2: Quantum-dark sector BEC soliton core, Bohm quantum potential,
   and quantum Jeans mass resolving Cold Dark Matter core-cusp & missing satellites.
3. Pillar 3: Environmental decoherence timescales across microscopic, macromolecular,
   SQUID, and macroscopic dust grain regimes, contrasted with Diosi-Penrose collapse.
4. Pillar 4: Three falsifiable predictions (NANOGrav PTA frequency, JWST matter cutoff,
   and MAQRO space-based interferometry).
5. Handover JSON integrity and Agent 1 dark matter ingestion.
"""

import unittest
import os
import sys
import json
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from a002_phase5_quantum_cosmos_macro_reality import (
    CosmicInflationQuantumGenesisEngine,
    QuantumDarkSectorBECSolitonEngine,
    MacroscopicDecoherenceAndPenroseEngine,
    FalsifiablePredictionsEngine,
    run_master_quantum_cosmos_pipeline,
    PLANCK_N_S,
    PLANCK_N_S_SIGMA,
    PLANCK_A_S,
    C_SI,
    G_SI,
    HBAR_SI,
    H_PLANCK_SI,
    AMU_TO_KG
)

class TestQuantumCosmosMacroReality(unittest.TestCase):

    def setUp(self):
        self.inflation = CosmicInflationQuantumGenesisEngine()
        self.bec = QuantumDarkSectorBECSolitonEngine()
        self.decoherence = MacroscopicDecoherenceAndPenroseEngine()
        self.predictions = FalsifiablePredictionsEngine()

    def test_pillar_1_cosmic_inflation_scale_invariance_rejection(self):
        """Verify Planck 2018 8.35-sigma rejection of scale invariance and quantum genesis."""
        rej = self.inflation.scale_invariance_rejection_significance()
        self.assertAlmostEqual(rej["n_s_measured"], 0.9649, places=4)
        self.assertAlmostEqual(rej["n_s_uncertainty"], 0.0042, places=4)
        self.assertGreater(rej["rejection_significance_sigma"], 8.0, "Scale invariance (n_s = 1.0) must be rejected at > 8 sigma")
        self.assertLess(rej["p_value"], 1.0e-15, "p-value must be vanishingly small (< 1e-15)")

        # Verify power spectrum at pivot scale
        p_pivot = self.inflation.primordial_curvature_power(0.05)
        self.assertAlmostEqual(p_pivot, PLANCK_A_S, delta=1.0e-11)

        # Slow-roll parameters
        sr = self.inflation.compute_slow_roll_parameters(tensor_to_scalar_r=0.03)
        self.assertGreater(sr["slow_roll_epsilon"], 0.0)
        self.assertLess(sr["slow_roll_eta"], 0.0, "Scalar tilt requires negative eta")
        self.assertGreater(sr["inflation_energy_scale_gev"], 1.0e15, "GUT-scale inflation energy")

        # Quantum spatial amplification
        qamp = self.inflation.quantum_amplification_factor()
        self.assertGreater(qamp["total_spatial_amplification"], 1.0e50, "Subatomic to cosmic expansion must exceed 1e50")

    def test_pillar_2_quantum_dark_sector_bec_soliton_and_jeans(self):
        """Verify BEC Gross-Pitaevskii / Schrodinger-Poisson soliton and quantum Jeans mass."""
        bohm = self.bec.bohm_quantum_potential_at_origin()
        self.assertGreater(bohm["central_quantum_potential_j_per_kg"], 1.0e8, "Quantum potential must be > 1e8 J/kg")
        self.assertEqual(bohm["repulsive_sign"], 1.0, "Quantum potential must exert outward repulsive force")
        self.assertGreater(bohm["quantum_wave_sound_speed_km_s"], 5.0, "Sound speed must be > 5 km/s")

        # Soliton density profile is non-singular
        rho_0 = self.bec.soliton_density_profile(0.0)
        rho_core = self.bec.soliton_density_profile(1.6)
        self.assertGreater(rho_0, 0.0)
        self.assertLess(rho_core, rho_0, "Density must decrease outwards")
        self.assertGreater(rho_core, rho_0 * 0.1, "Core profile must maintain substantial density at r_c")

        # Quantum Jeans scale
        jeans = self.bec.quantum_jeans_scale_and_mass()
        self.assertGreater(jeans["quantum_jeans_wavenumber_mpc"], 1.0, "Jeans wavenumber must be > 1 Mpc^-1")
        self.assertGreater(jeans["quantum_jeans_mass_msun"], 1.0e7, "Jeans mass must exceed 1e7 M_sun")
        self.assertLess(jeans["quantum_jeans_mass_msun"], 1.0e9, "Jeans mass must be < 1e9 M_sun to preserve dwarfs")

        # Cusp vs Soliton comparison: NFW diverges while soliton remains flat
        comp = self.bec.cusp_vs_soliton_comparison([0.001, 1.0, 10.0])
        self.assertEqual(len(comp), 3)
        self.assertLess(comp[0]["density_ratio_soliton_to_nfw"], 0.05, "At 1 pc, NFW cusp density vastly exceeds flat soliton")

    def test_pillar_3_macroscopic_decoherence_and_penrose_collapse(self):
        """Verify environmental decoherence across 4 regimes and contrast with Diosi-Penrose collapse."""
        table = self.decoherence.generate_full_reality_spectrum_table()
        self.assertEqual(len(table), 7)

        # 1. Microscopic Electron in UHV
        elec = next(r for r in table if "Electron" in r["regime_name"])
        self.assertGreater(elec["combined_environmental_decoherence_time_s"], 1.0e10, "Electron in UHV must retain coherence for > 1e10 s")

        # 2. Macromolecule (25,000 Da, Fein et al. 2019)
        macro = next(r for r in table if "25,000 Da" in r["regime_name"])
        self.assertLess(macro["combined_environmental_decoherence_time_s"], 1.0, "Macromolecule decoheres within sub-second")
        self.assertGreater(macro["diosi_penrose_collapse_time_s"], 1.0e10, "Diosi-Penrose collapse for macromolecule is negligibly slow")

        # 3. Superconducting SQUID (> 10^9 Cooper pairs)
        squid = next(r for r in table if "SQUID" in r["regime_name"])
        self.assertGreater(squid["combined_environmental_decoherence_time_s"], 1.0e-5, "SQUID coherence time must be in microsecond regime")
        self.assertGreater(squid["diosi_penrose_collapse_time_s"], 1.0e10, "Diosi-Penrose time is astronomical for Cooper pair active mass")

        # 4. Everyday Dust Grain in Air (10 um)
        dust_air = next(r for r in table if "Dust Grain" in r["regime_name"] and "Air" in r["regime_name"])
        self.assertLess(dust_air["combined_environmental_decoherence_time_s"], 1.0e-18, "Everyday dust grain in air must decohere in < 1e-18 s")
        self.assertEqual(dust_air["dominant_suppression_mechanism"], "Environmental Decoherence")

        # 5. Diosi-Penrose vs Decoherence on MAQRO nanoparticle
        maqro = next(r for r in table if "MAQRO" in r["regime_name"])
        self.assertLess(maqro["diosi_penrose_collapse_time_s"], 100.0, "Diosi-Penrose collapse for 1e10 Da must be < 100 s")

    def test_pillar_4_falsifiable_predictions(self):
        """Verify the 3 falsifiable experimental predictions."""
        # Prediction 1: PTA oscillation frequency
        p1 = self.predictions.prediction_1_pulsar_timing_oscillation()
        self.assertAlmostEqual(p1["pta_frequency_nhz"], 48.36, delta=0.5)
        self.assertTrue(p1["in_pta_sensitivity_window"], "Must lie within NANOGrav/EPTA 1-100 nHz band")
        self.assertAlmostEqual(p1["oscillation_period_years"], 0.655, delta=0.05)

        # Prediction 2: Matter power spectrum cutoff
        p2 = self.predictions.prediction_2_matter_power_spectrum_cutoff()
        self.assertGreater(p2["quantum_cutoff_wavenumber_mpc"], 15.0, "Cutoff wavenumber must be > 15 Mpc^-1")
        self.assertGreater(p2["half_mode_suppression_mass_msun"], 1.0e9, "Half mode mass must be in dwarf halo regime")

        # Prediction 3: MAQRO space-based test
        p3 = self.predictions.prediction_3_space_based_maqro_interferometry()
        self.assertGreater(p3["test_nanoparticle_mass_daltons"], 1.0e10)
        self.assertGreater(p3["diosi_penrose_collapse_time_s"], 10.0, "Collapse time must be accessible in long free-fall")
        self.assertLess(p3["diosi_penrose_collapse_time_s"], 500.0)

    def test_pipeline_and_handover_json(self):
        """Verify end-to-end execution and handover JSON generation."""
        payload = run_master_quantum_cosmos_pipeline(export_handover=True)
        self.assertEqual(payload["metadata"]["source_agent"], "A002_QuantumCosmos")
        self.assertIn("pillar_1_cosmic_scale_quantum_genesis", payload)
        self.assertIn("pillar_2_quantum_dark_sector_bec", payload)
        self.assertIn("pillar_3_macroscopic_quantum_and_decoherence", payload)
        self.assertIn("pillar_4_falsifiable_predictions", payload)

        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "phase5_quantum_cosmos_handover.json")
        self.assertTrue(os.path.exists(json_path), "Handover JSON file must exist on disk")

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["metadata"]["source_agent"], "A002_QuantumCosmos")
        self.assertTrue(data["metadata"]["handover_from_agent_1_ingested"], "Must successfully ingest Agent 1 handover")

if __name__ == "__main__":
    unittest.main()
