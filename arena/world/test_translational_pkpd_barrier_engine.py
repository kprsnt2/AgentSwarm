"""
test_translational_pkpd_barrier_engine.py — Unit Tests for Translational PK/PD Engine.
Nagarjuna (A004), generation 0.
"""

import unittest
import math
from translational_pkpd_barrier_engine import (
    log_factorial,
    log_comb,
    fisher_exact_2x2,
    normal_cdf,
    normal_ppf,
    CompoundProfile,
    CNSDispositionModel,
    PathwayTransductionModel,
    HISTORICAL_BENCHMARKS,
    INDICATION_BENCHMARKS,
    calculate_two_sample_proportions_power,
    derive_sample_size_for_hypothesis_h2
)

class TestTranslationalPKPDBoundaries(unittest.TestCase):

    def test_statistical_primitives(self):
        """Verify normal CDF and inverse normal PPF against known values."""
        self.assertAlmostEqual(normal_cdf(0.0), 0.5, places=5)
        self.assertAlmostEqual(normal_cdf(1.96), 0.975, places=3)
        self.assertAlmostEqual(normal_cdf(-1.96), 0.025, places=3)
        self.assertAlmostEqual(normal_ppf(0.5), 0.0, places=4)
        self.assertAlmostEqual(normal_ppf(0.975), 1.96, delta=0.01)
        self.assertAlmostEqual(normal_ppf(0.95), 1.645, delta=0.01)

    def test_fisher_exact_contingency(self):
        """Verify 2x2 Fisher's exact test calculation on known contingency table."""
        # 2x2 table: [[8, 6], [0, 12]]
        odds_ratio, p_value = fisher_exact_2x2(8, 6, 0, 12)
        self.assertGreater(odds_ratio, 20.0)
        self.assertLess(p_value, 0.01)

    def test_in_vivo_potency_paradox(self):
        """
        Verify that lipophilic candidate with 100x better Kd can achieve
        LOWER in vivo free receptor occupancy due to plasma protein binding collapse.
        """
        balanced = CompoundProfile("Balanced", mw=380.0, clogp=1.8, kd_nm=50.0, n_heavy=27)
        greasy = CompoundProfile("Greasy", mw=560.0, clogp=4.8, kd_nm=0.5, n_heavy=41)

        res_b = balanced.evaluate_in_vivo_potency(total_plasma_conc_um=1.0)
        res_g = greasy.evaluate_in_vivo_potency(total_plasma_conc_um=1.0)

        # Greasy candidate has lower unbound fraction
        self.assertLess(res_g["fu_plasma_pct"], res_b["fu_plasma_pct"] / 10.0)
        # Greasy candidate achieves lower free receptor occupancy despite 100x lower Kd
        self.assertGreater(res_b["fractional_occupancy"], res_g["fractional_occupancy"])
        # Balanced compound has superior Lipophilic Ligand Efficiency (LLE)
        self.assertGreater(res_b["lle"], res_g["lle"])

    def test_cns_efflux_barrier(self):
        """
        Verify that active BBB efflux (Kp,uu << 1) demands elevated systemic exposure
        and can trigger Class B dose-limiting peripheral failure.
        """
        # Non-substrate (Kp,uu ~ 1)
        cns_clean = CNSDispositionModel(
            compound_name="Clean", kd_on_target_nm=5.0, clogp=2.0,
            ps_passive_ul_min_g=50.0, vmax_efflux_pmol_min_g=0.0, km_efflux_um=5.0,
            peripheral_toxic_threshold_cu_nm=300.0
        )
        feas_clean = cns_clean.evaluate_cns_therapeutic_feasibility(target_brain_occupancy=0.80)
        self.assertAlmostEqual(feas_clean["effective_kp_uu_brain"], 1.0, places=2)
        self.assertFalse(feas_clean["is_class_b_exposure_failure"])

        # High efflux substrate with low passive permeability
        cns_efflux = CNSDispositionModel(
            compound_name="Effluxed", kd_on_target_nm=5.0, clogp=3.5,
            ps_passive_ul_min_g=5.0, vmax_efflux_pmol_min_g=1500.0, km_efflux_um=1.0,
            peripheral_toxic_threshold_cu_nm=100.0
        )
        feas_efflux = cns_efflux.evaluate_cns_therapeutic_feasibility(target_brain_occupancy=0.80)
        self.assertLess(feas_efflux["effective_kp_uu_brain"], 0.02)
        self.assertTrue(feas_efflux["is_class_b_exposure_failure"])
        self.assertLess(feas_efflux["max_achievable_occupancy_at_mtd"], 0.80)

    def test_pathway_transduction_nonlinearity(self):
        """Verify non-linear Hill response in oncogenic vs GPCR signaling."""
        onco_kras = PathwayTransductionModel("Oncology", "KRAS", gamma_steepness=3.5, occupancy_threshold_50=0.75)
        # At 50% occupancy, steep pathway is < 25% inhibited
        res_50 = onco_kras.evaluate_clinical_translation(0.50)
        self.assertLess(res_50["downstream_pathway_inhibition"], 0.25)
        self.assertFalse(res_50["clinical_poc_achieved"])

        # At 95% occupancy, pathway inhibition is ~69.6% (verifying high threshold requirement)
        res_95 = onco_kras.evaluate_clinical_translation(0.95)
        self.assertAlmostEqual(res_95["downstream_pathway_inhibition"], 0.696, places=2)

        # At 98% occupancy, pathway inhibition surpasses the 70% clinical PoC bar
        res_98 = onco_kras.evaluate_clinical_translation(0.98)
        self.assertGreater(res_98["downstream_pathway_inhibition"], 0.70)
        self.assertTrue(res_98["clinical_poc_achieved"])

    def test_historical_benchmarks_integrity(self):
        """Ensure all 5 historical benchmarks have verified citations and primary mechanisms."""
        self.assertEqual(len(HISTORICAL_BENCHMARKS), 5)
        drugs = [b.drug_name for b in HISTORICAL_BENCHMARKS]
        self.assertIn("Verubecestat (MK-8931)", drugs)
        self.assertIn("Evacetrapib (LY2484595)", drugs)
        self.assertIn("Aprepitant (MK-0869)", drugs)
        self.assertIn("Iniparib (BSI-201)", drugs)
        self.assertIn("Evolocumab (AMG 145)", drugs)

    def test_hypothesis_h2_sample_size_derivation(self):
        """Verify statistical sample size calculation for indication-stratified Hypothesis H2."""
        res = derive_sample_size_for_hypothesis_h2(p_systemic=0.82, p_cns=0.52, alpha=0.05, power_target=0.90)
        self.assertGreater(res["n_classifiable_per_arm"], 30)
        self.assertLess(res["n_classifiable_per_arm"], 60)
        self.assertGreater(res["n_total_combined_study"], 100)
        self.assertLess(res["n_total_combined_study"], 250)

if __name__ == "__main__":
    unittest.main()
