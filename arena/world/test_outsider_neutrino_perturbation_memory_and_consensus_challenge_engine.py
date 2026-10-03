"""
Verification Suite for Outsider Neutrino Perturbation Memory and Consensus Challenge Engine
============================================================================================
Author: Outsider3 (A003, Generation 0)
"""

import math
import unittest
from outsider_neutrino_perturbation_memory_and_consensus_challenge_engine import (
    PerturbationMemoryAuditEngine,
    LymanAlphaFisherCollapseAuditEngine,
    GeometricBAOvsGrowthDecompositionEngine,
    AlternativeConsensusBreakerEngine,
    SUM_M_NU_NO_MIN,
    SUM_M_NU_IO_MIN,
    BOUND_DESI_PLANCK_95
)


class TestPerturbationMemoryAuditEngine(unittest.TestCase):
    def test_analytic_erasure_efficiency(self):
        res = PerturbationMemoryAuditEngine.analytic_erasure_efficiency(
            z_decay=3.2, z_obs=0.0, z_eq=3400.0, sum_pre=0.05821, sum_post=0.00868
        )
        self.assertAlmostEqual(res["pre_growth_fraction"], 0.8235, places=3)
        self.assertAlmostEqual(res["post_growth_fraction"], 0.1765, places=3)
        self.assertAlmostEqual(res["analytic_erasure_efficiency"], 0.1502, places=3)
        self.assertAlmostEqual(res["apparent_mass_eV"], 0.04947, places=3)

    def test_numerical_apparent_mass_normal_ordering(self):
        res = PerturbationMemoryAuditEngine.evaluate_numerical_apparent_mass(
            sum_pre=SUM_M_NU_NO_MIN, sum_post=0.00868, z_decay=3.2, n_steps=1000
        )
        # Numerical erasure in CDM+b is only ~4-5%, NOT 85.3%!
        self.assertLess(res["numerical_erasure_efficiency_pct"], 10.0)
        self.assertGreater(res["numerical_erasure_efficiency_pct"], 3.0)
        # Apparent mass is around 0.0557 eV, far from 0.0086 eV!
        self.assertGreater(res["apparent_mass_eV"], 0.050)
        self.assertLess(res["apparent_mass_eV"], 0.058)

    def test_numerical_apparent_mass_inverted_ordering(self):
        res = PerturbationMemoryAuditEngine.evaluate_numerical_apparent_mass(
            sum_pre=SUM_M_NU_IO_MIN, sum_post=0.0, z_decay=3.2, n_steps=1000
        )
        # Inverted ordering apparent mass under 100% decay remains above DESI 0.072 eV bound!
        self.assertGreater(res["apparent_mass_eV"], BOUND_DESI_PLANCK_95)
        self.assertGreater(res["apparent_mass_eV"], 0.090)


class TestLymanAlphaFisherCollapseAuditEngine(unittest.TestCase):
    def test_tomographic_discrepancy(self):
        records = LymanAlphaFisherCollapseAuditEngine.compute_tomographic_discrepancy(
            redshifts=[3.0, 2.5, 2.0, 1.0, 0.0], z_decay=3.2
        )
        z3_record = [r for r in records if r["redshift"] == 3.0][0]
        # At z=3.0, true difference vs stable neutrinos is tiny (<0.05%)
        self.assertLess(z3_record["true_difference_vs_stable_pct"], 0.05)
        # Raman/Kepler naive model claimed Delta P/P = -0.52%, discrepancy > 2.0%
        self.assertGreater(z3_record["discrepancy_naive_vs_true_pct"], 2.0)

    def test_fisher_collapse(self):
        res = LymanAlphaFisherCollapseAuditEngine.evaluate_fisher_collapse(z_decay=3.2, z_obs=3.0)
        # Naive Lyman sigma was 7.50
        self.assertAlmostEqual(res["naive_sigma_lyman"], 7.50, places=2)
        # True Lyman sigma collapses to ~0.054
        self.assertLess(res["true_sigma_lyman"], 0.10)
        self.assertGreater(res["true_sigma_lyman"], 0.04)
        # Loss factor is > 100x
        self.assertGreater(res["lyman_significance_loss_factor"], 100.0)
        # True total joint significance is around 9.61 sigma (pure Euclid w0), NOT 12.19 sigma!
        self.assertAlmostEqual(res["true_sigma_total"], math.sqrt((0.173/0.018)**2 + res["true_chi2_lyman"]), places=2)


class TestGeometricBAOvsGrowthDecompositionEngine(unittest.TestCase):
    def test_geometric_ladder(self):
        ladder = GeometricBAOvsGrowthDecompositionEngine.compute_geometric_ladder(
            z_list=[0.30, 0.51, 0.71, 0.93, 1.32, 1.49, 2.33], sum_m_nu=0.0
        )
        self.assertAlmostEqual(ladder[0.30]["D_M_over_rd"], 8.405, places=1)
        self.assertAlmostEqual(ladder[2.33]["D_M_over_rd"], 39.163, places=1)

    def test_h0_neutrino_degeneracy(self):
        records = GeometricBAOvsGrowthDecompositionEngine.evaluate_h0_neutrino_degeneracy(
            sum_m_nu_values=[0.0, 0.06, 0.10, 0.165]
        )
        # Increasing neutrino mass reduces required H0 to preserve theta_*
        h0_0 = records[0]["required_H0_km_s_Mpc"]
        h0_16 = records[3]["required_H0_km_s_Mpc"]
        self.assertGreater(h0_0, h0_16)
        self.assertLess(records[3]["delta_H0_km_s_Mpc"], -0.3)


class TestAlternativeConsensusBreakerEngine(unittest.TestCase):
    def test_neutrino_self_interaction(self):
        res = AlternativeConsensusBreakerEngine.evaluate_neutrino_self_interaction(G_eff_over_GF=1.0e8)
        self.assertTrue(res["fluid_regime_active"])
        self.assertGreater(res["free_streaming_inhibition_pct"], 95.0)

    def test_low_reheating_dilution(self):
        res = AlternativeConsensusBreakerEngine.evaluate_low_reheating_dilution(
            T_rh_MeV=2.5, sum_true_eV=SUM_M_NU_IO_MIN
        )
        # Dilution allows IO to evade the 0.072 eV bound
        self.assertTrue(res["evades_desi_0_072_bound"])
        self.assertLess(res["apparent_gravitational_mass_eV"], 0.072)

    def test_supernova_sample_bias(self):
        biases = AlternativeConsensusBreakerEngine.evaluate_supernova_sample_bias()
        self.assertEqual(biases["DESI_BAO_alone"]["significance_sigma"], 0.60)
        self.assertEqual(biases["DESI_BAO_plus_CMB"]["significance_sigma"], 1.50)
        self.assertEqual(biases["DESI_plus_CMB_plus_DESSN5Y"]["significance_sigma"], 3.90)


if __name__ == "__main__":
    unittest.main()
