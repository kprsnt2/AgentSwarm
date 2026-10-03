"""
Unit tests for Cosmogenesis Neutrino Mass and Free-Streaming Engine
"""

import unittest
import math
from cosmogenesis_neutrino_mass_and_free_streaming_engine import (
    NeutrinoMassOscillationModel,
    RelicNeutrinoCosmologyEngine,
    CosmologicalNeutrinoTensionAuditor,
    run_full_neutrino_cosmogenesis_audit,
    T_CMB_K,
    SUM_M_NU_BOUND_DESI2024,
    SUM_M_NU_BOUND_DESI_ACT
)


class TestNeutrinoMassEngine(unittest.TestCase):

    def test_neutrino_temperature_ratio(self):
        """Verify T_nu,0 = (4/11)^(1/3) * T_CMB is approximately 1.945 K."""
        t_nu = RelicNeutrinoCosmologyEngine.compute_neutrino_temperature_today()
        expected = ((4.0 / 11.0) ** (1.0 / 3.0)) * T_CMB_K
        self.assertAlmostEqual(t_nu, expected, places=5)
        self.assertTrue(1.94 < t_nu < 1.95)

    def test_normal_ordering_physical_floor(self):
        """Verify the physical lower bound for Normal Ordering is approx 0.059 eV."""
        floors = NeutrinoMassOscillationModel.get_physical_floors()
        sum_no = floors["normal_ordering_min_sum_ev"]
        self.assertTrue(0.058 < sum_no < 0.060)

    def test_inverted_ordering_physical_floor(self):
        """Verify the physical lower bound for Inverted Ordering is approx 0.100 eV."""
        floors = NeutrinoMassOscillationModel.get_physical_floors()
        sum_io = floors["inverted_ordering_min_sum_ev"]
        self.assertTrue(0.098 < sum_io < 0.102)
        self.assertGreater(sum_io, floors["normal_ordering_min_sum_ev"])

    def test_omega_nu_scaling(self):
        """Verify Omega_nu * h^2 = sum(m_nu) / 93.14 eV."""
        omega_h2 = RelicNeutrinoCosmologyEngine.compute_omega_nu_h2(0.09314)
        self.assertAlmostEqual(omega_h2, 0.001, places=5)

    def test_non_relativistic_redshift(self):
        """Verify z_nr is non-negative and scales linearly with neutrino mass."""
        z_nr_1ev = RelicNeutrinoCosmologyEngine.compute_non_relativistic_redshift(1.0)
        z_nr_half = RelicNeutrinoCosmologyEngine.compute_non_relativistic_redshift(0.5)
        self.assertGreater(z_nr_1ev, 1500)
        self.assertAlmostEqual((z_nr_1ev + 1.0) / (z_nr_half + 1.0), 2.0, places=3)

    def test_matter_power_suppression(self):
        """Verify Delta P / P is negative and proportional to sum m_nu."""
        supp = RelicNeutrinoCosmologyEngine.compute_matter_power_suppression(0.06)
        self.assertLess(supp, 0.0)
        self.assertTrue(-0.06 < supp < -0.02)  # Typically ~ -3% to -4%

    def test_tension_audit_desi2024(self):
        """Verify Inverted Ordering is ruled out at 95% CL by DESI 2024 (0.072 eV bound)."""
        tension = CosmologicalNeutrinoTensionAuditor.evaluate_ordering_viability()
        self.assertTrue(tension["is_inverted_ordering_disfavored_at_95CL"])
        self.assertGreater(tension["inverted_ordering_tension_sigma"], 2.0)
        self.assertGreater(tension["normal_ordering_headroom_desi2024_ev"], 0.0)

    def test_full_audit_execution(self):
        """Verify full audit runs cleanly and produces structured valid results."""
        audit = run_full_neutrino_cosmogenesis_audit()
        self.assertIn("neutrino_temperature_today_K", audit)
        self.assertIn("normal_ordering_spectrum", audit)
        self.assertIn("inverted_ordering_spectrum", audit)
        self.assertIn("tension_audit", audit)
        self.assertIn("arbitration_hypotheses", audit)
        self.assertEqual(len(audit["arbitration_hypotheses"]), 3)


if __name__ == "__main__":
    unittest.main()
