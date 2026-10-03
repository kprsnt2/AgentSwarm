#!/usr/bin/env python3
"""
test_outsider_cosmogenesis_foundations_and_epicycle_audit_engine.py

Comprehensive unit test suite for outsider_cosmogenesis_foundations_and_epicycle_audit_engine.py.
Verifies all 5 analytical modules across mathematical invariants, numerical thresholds,
and physical consistency.
"""

import unittest
import math
from outsider_cosmogenesis_foundations_and_epicycle_audit_engine import (
    AsymptoticSafetyStarobinskyAudit,
    HolographicDarkEnergyNoGoAudit,
    SorkinCausalSetBBNAudit,
    MultiProbeDistanceLadderSynthesis,
    CosmogenesisTrilemmaAudit,
    run_complete_outsider_cosmogenesis_audit,
    M_PL_GEV
)


class TestAsymptoticSafetyAudit(unittest.TestCase):
    """Tests for Module 1: Asymptotic Safety and Starobinsky Inflation Audit."""

    def setUp(self):
        self.audit = AsymptoticSafetyStarobinskyAudit(A_s=2.10e-9, N_efolds=55.0)

    def test_scalaron_mass_and_alpha(self):
        params = self.audit.compute_scalaron_parameters()
        # Scalaron mass M should be around 3.0e13 to 4.0e13 GeV
        self.assertGreater(params["scalaron_mass_GeV"], 2.0e13)
        self.assertLess(params["scalaron_mass_GeV"], 5.0e13)

        # Alpha should be around 3e8 to 5e8
        self.assertGreater(params["alpha"], 1.0e8)
        self.assertLess(params["alpha"], 1.0e9)

        # Observables ns and r
        self.assertAlmostEqual(params["ns"], 1.0 - 2.0 / 55.0, places=4)
        self.assertAlmostEqual(params["r"], 12.0 / (55.0**2), places=5)

    def test_frg_naturalness_and_ghost(self):
        res = self.audit.audit_frg_naturalness(alpha_natural=0.01)
        # Fine-tuning ratio should exceed 10^10
        self.assertGreater(res.fine_tuning_ratio, 1.0e10)

        # TCC violation factor should exceed 10^26
        self.assertGreater(res.tcc_violation_factor, 1.0e26)

        # Ghost mass should be on Planck scale (around 1.2e18 GeV)
        self.assertGreater(res.ostrogradsky_ghost_mass_GeV, 1.0e18)
        self.assertTrue(res.unitarity_violation)
        self.assertLess(res.ghost_instability_timescale_s, 1.0e-42)


class TestHolographicDarkEnergyNoGo(unittest.TestCase):
    """Tests for Module 2: Holographic Dark Energy Hubble Cutoff No-Go Theorem."""

    def setUp(self):
        self.audit = HolographicDarkEnergyNoGoAudit(c_param=1.0)

    def test_equation_of_state_is_dust(self):
        res = self.audit.evaluate_hubble_cutoff()
        # w must be identically 0.0
        self.assertEqual(res.equation_of_state_w, 0.0)
        self.assertTrue(res.scales_as_dust)
        self.assertFalse(res.can_explain_acceleration)
        self.assertIn("decelerating", res.cosmic_acceleration_sign)


class TestSorkinBBNAudit(unittest.TestCase):
    """Tests for Module 3: Sorkin Causal Set Fluctuations BBN Catastrophe."""

    def setUp(self):
        self.audit = SorkinCausalSetBBNAudit(omega_lambda_fraction=0.68)

    def test_bbn_helium_yield_and_falsification(self):
        res = self.audit.compute_bbn_helium_yield()
        # Standard Y_p should be ~0.246
        self.assertAlmostEqual(res.standard_Yp, 0.246, places=2)

        # Sorkin Y_p should be ~0.34
        self.assertGreater(res.sorkin_Yp, 0.32)
        self.assertLess(res.sorkin_Yp, 0.37)

        # Statistical discrepancy should be > 25 sigma
        self.assertGreater(res.discrepancy_sigma, 25.0)
        self.assertIn("FALSIFIED", res.falsification_verdict)


class TestMultiProbeDistanceLadder(unittest.TestCase):
    """Tests for Module 4: Multi-Probe Distance Ladder Hierarchical Synthesis."""

    def setUp(self):
        self.synth = MultiProbeDistanceLadderSynthesis(planck_H0=67.36, planck_sigma=0.54)

    def test_all_probes_mean_and_tension(self):
        res = self.synth.synthesize()
        self.assertEqual(res.total_probes_analyzed, 7)
        # Weighted mean should be around 71.5 - 72.5 km/s/Mpc
        self.assertGreater(res.all_probes_mean_H0, 71.0)
        self.assertLess(res.all_probes_mean_H0, 73.0)

        # Tension with Planck should be > 5 sigma
        self.assertGreater(res.tension_with_planck_sigma, 5.0)

    def test_tension_without_shoes(self):
        res = self.synth.synthesize()
        # Without SH0ES, H0 should still be > 70.5 km/s/Mpc
        self.assertGreater(res.without_shoes_mean_H0, 70.5)

        # Tension without SH0ES should still exceed 4.0 sigma
        self.assertGreater(res.without_shoes_tension_sigma, 4.0)
        self.assertTrue(res.crowding_hypothesis_refuted)


class TestCosmogenesisTrilemma(unittest.TestCase):
    """Tests for Module 5: Cosmogenesis Trilemma."""

    def setUp(self):
        self.audit = CosmogenesisTrilemmaAudit()

    def test_trilemma_structure(self):
        legs = self.audit.audit_trilemma()
        self.assertEqual(len(legs), 3)
        leg_ids = [l.leg_id for l in legs]
        self.assertEqual(leg_ids, ["TRILEMMA-01", "TRILEMMA-02", "TRILEMMA-03"])

        # Check resolving observables
        self.assertIn("DECIGO", legs[0].decisive_resolving_observable)
        self.assertIn("Euclid", legs[1].decisive_resolving_observable)
        self.assertIn("LiteBIRD", legs[2].decisive_resolving_observable)


class TestEndToEndAuditRunner(unittest.TestCase):
    """Tests the complete end-to-end execution of the audit suite."""

    def test_runner_keys(self):
        results = run_complete_outsider_cosmogenesis_audit()
        self.assertIn("asymptotic_safety_audit", results)
        self.assertIn("holographic_de_nogo_audit", results)
        self.assertIn("sorkin_bbn_audit", results)
        self.assertIn("distance_ladder_synthesis", results)
        self.assertIn("cosmogenesis_trilemma", results)


if __name__ == "__main__":
    unittest.main()
