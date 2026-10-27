"""
test_cancer_immune_evasion_engine.py — Unit Tests for Cancer Immune Evasion Engine.
Hypatia (A003), generation 0.
Domain: Immunotherapy Resistance in Cold Tumors: STING Signaling, HLA Loss, and Microenvironment Barriers
Epistemic Class: Empirical.
"""

import unittest
import math
import numpy as np

from cancer_immune_evasion_engine import (
    BiophysicalConstants,
    TumorPhenotype,
    log_factorial,
    log_comb,
    fisher_exact_2x2,
    normal_cdf,
    normal_ppf,
    CGASSTINGState,
    CGASSTINGPathwaySimulator,
    APMGenotype,
    APMOutput,
    AntigenPresentationSimulator,
    MicroenvironmentBarriers,
    MicroenvironmentOutput,
    PhysicalAndMetabolicBarrierSimulator,
    PatientTumorProfile,
    ResponsePrediction,
    IntegratedTumorImmuneEngine,
    SyntheticClinicalCohortGenerator,
    evaluate_clinical_cohort,
    verify_ground_truth_compliance,
    SubclonalDynamicsConfig,
    SubclonalEvolutionSimulator,
    DualPurinergicConfig,
    DualPurinergicReceptorSimulator,
    SequencingStrategy,
    DynamicCombinatorialSequencingSimulator,
    BystanderSTINGTransferConfig,
    BystanderSTINGTransferOutput,
    IntercellularBystanderSTINGSimulator,
    SolidStressPerfusionConfig,
    SolidStressPerfusionOutput,
    VascularCompressionPerfusionSimulator
)


class TestStatisticalAndMathematicalPrimitives(unittest.TestCase):
    """Verifies numerical precision of statistical functions."""

    def test_normal_distribution_functions(self):
        self.assertAlmostEqual(normal_cdf(0.0), 0.5, places=5)
        self.assertAlmostEqual(normal_cdf(1.96), 0.975, places=3)
        self.assertAlmostEqual(normal_cdf(-1.96), 0.025, places=3)
        self.assertAlmostEqual(normal_ppf(0.5), 0.0, places=4)
        self.assertAlmostEqual(normal_ppf(0.975), 1.96, delta=0.01)
        self.assertAlmostEqual(normal_ppf(0.95), 1.645, delta=0.01)

    def test_combinatorics(self):
        self.assertAlmostEqual(math.exp(log_factorial(5)), 120.0, places=4)
        self.assertAlmostEqual(math.exp(log_comb(10, 3)), 120.0, places=4)

    def test_fisher_exact_test(self):
        # 2x2 table: [[12, 2], [1, 15]] -> strong association
        odds_ratio, p_value = fisher_exact_2x2(12, 2, 1, 15)
        self.assertGreater(odds_ratio, 10.0)
        self.assertLess(p_value, 0.001)


class TestCGASSTINGPathway(unittest.TestCase):
    """Verifies cGAS sensing, 2'3'-cGAMP catalysis, TREX1/ENPP1 degradation, and STING signaling."""

    def setUp(self):
        self.sim = CGASSTINGPathwaySimulator()

    def test_dsdna_dose_dependent_cgamp_production(self):
        state_low = CGASSTINGState(
            cytosolic_dsdna_nm=5.0, cgas_expression_fraction=1.0,
            sting_expression_fraction=1.0, trex1_activity_fold=1.0, enpp1_activity_fold=1.0
        )
        state_high = CGASSTINGState(
            cytosolic_dsdna_nm=50.0, cgas_expression_fraction=1.0,
            sting_expression_fraction=1.0, trex1_activity_fold=1.0, enpp1_activity_fold=1.0
        )
        res_low = self.sim.simulate(state_low)
        res_high = self.sim.simulate(state_high)

        self.assertGreater(res_high.steady_state_cgamp_nm, res_low.steady_state_cgamp_nm)
        self.assertGreater(res_high.type1_ifn_induction_fold, res_low.type1_ifn_induction_fold)
        self.assertGreater(res_high.cxcl9_10_chemokine_score, res_low.cxcl9_10_chemokine_score)

    def test_trex1_overexpression_blunts_activation(self):
        """TREX1 nucleolytic clearance elevates the threshold for cGAS sensing."""
        state_normal = CGASSTINGState(
            cytosolic_dsdna_nm=30.0, cgas_expression_fraction=1.0,
            sting_expression_fraction=1.0, trex1_activity_fold=1.0, enpp1_activity_fold=1.0
        )
        state_trex1_high = CGASSTINGState(
            cytosolic_dsdna_nm=30.0, cgas_expression_fraction=1.0,
            sting_expression_fraction=1.0, trex1_activity_fold=5.0, enpp1_activity_fold=1.0
        )
        res_normal = self.sim.simulate(state_normal)
        res_trex1 = self.sim.simulate(state_trex1_high)

        self.assertLess(res_trex1.steady_state_cgamp_nm, res_normal.steady_state_cgamp_nm * 0.3)
        self.assertTrue(res_trex1.is_enzymatically_depleted)

    def test_enpp1_overexpression_degrades_cgamp(self):
        """ENPP1 degrades 2'3'-cGAMP, reducing STING activation."""
        state_normal = CGASSTINGState(
            cytosolic_dsdna_nm=35.0, cgas_expression_fraction=1.0,
            sting_expression_fraction=1.0, trex1_activity_fold=1.0, enpp1_activity_fold=1.0
        )
        state_enpp1_high = CGASSTINGState(
            cytosolic_dsdna_nm=35.0, cgas_expression_fraction=1.0,
            sting_expression_fraction=1.0, trex1_activity_fold=1.0, enpp1_activity_fold=5.0
        )
        res_normal = self.sim.simulate(state_normal)
        res_enpp1 = self.sim.simulate(state_enpp1_high)

        self.assertLess(res_enpp1.steady_state_cgamp_nm, res_normal.steady_state_cgamp_nm)
        self.assertLess(res_enpp1.active_sting_fraction, res_normal.active_sting_fraction)

    def test_epigenetic_promoter_silencing(self):
        """Epigenetic silencing of STING or cGAS prevents Type I IFN induction."""
        state_silenced = CGASSTINGState(
            cytosolic_dsdna_nm=45.0, cgas_expression_fraction=0.02, # Hypermethylated
            sting_expression_fraction=0.02, trex1_activity_fold=1.0, enpp1_activity_fold=1.0
        )
        res = self.sim.simulate(state_silenced)

        self.assertTrue(res.is_epigenetically_silenced)
        self.assertLess(res.steady_state_cgamp_nm, 1.0)
        self.assertLess(res.active_sting_fraction, 0.05)
        self.assertAlmostEqual(res.type1_ifn_induction_fold, 1.0, delta=0.5)


class TestAntigenPresentationMachinery(unittest.TestCase):
    """Verifies B2M loss-of-function, HLA LOH, and TAP1/2 downregulation."""

    def setUp(self):
        self.sim = AntigenPresentationSimulator()

    def test_b2m_null_causes_complete_cd8_escape(self):
        """Ground Truth: B2M homozygous loss abolishes surface MHC-I and CD8 recognition."""
        b2m_null = APMGenotype(
            b2m_functional_alleles=0,
            hla_a_alleles=("A*02:01", "A*03:01"),
            hla_b_alleles=("B*07:02", "B*44:02"),
            hla_c_alleles=("C*07:01", "C*05:01"),
            hla_loh_occurred=False,
            lost_maternal_or_paternal="NONE",
            tap1_expression_fraction=1.0,
            tap2_expression_fraction=1.0,
            tapasin_expression_fraction=1.0,
            jak1_jak2_intact=True,
            baseline_clonal_neoantigens=45
        )
        res = self.sim.evaluate(b2m_null)

        self.assertEqual(res.surface_mhc1_copies_per_cell, 0.0)
        self.assertEqual(res.effective_presented_neoantigens, 0.0)
        self.assertEqual(res.cd8_tcr_recognition_probability, 0.0)
        self.assertTrue(res.absolute_cd8_escape)
        self.assertEqual(res.apm_loss_mechanism, "B2M_BIALLELIC_LOSS")
        self.assertGreater(res.nk_cell_missing_self_activation_prob, 0.80)

    def test_hla_loh_causes_partial_neoantigen_loss_sparing_nk_activation(self):
        """HLA LOH deletes one parental haplotype, reducing presented neoantigens while sparing NK lysis."""
        wt = APMGenotype(
            b2m_functional_alleles=2,
            hla_a_alleles=("A*02:01", "A*24:02"),
            hla_b_alleles=("B*08:01", "B*35:01"),
            hla_c_alleles=("C*03:01", "C*07:02"),
            hla_loh_occurred=False,
            lost_maternal_or_paternal="NONE",
            tap1_expression_fraction=1.0,
            tap2_expression_fraction=1.0,
            tapasin_expression_fraction=1.0,
            jak1_jak2_intact=True,
            baseline_clonal_neoantigens=40
        )
        loh = APMGenotype(
            b2m_functional_alleles=2,
            hla_a_alleles=("A*02:01", "A*24:02"),
            hla_b_alleles=("B*08:01", "B*35:01"),
            hla_c_alleles=("C*03:01", "C*07:02"),
            hla_loh_occurred=True,
            lost_maternal_or_paternal="MATERNAL",
            tap1_expression_fraction=1.0,
            tap2_expression_fraction=1.0,
            tapasin_expression_fraction=1.0,
            jak1_jak2_intact=True,
            baseline_clonal_neoantigens=40
        )
        res_wt = self.sim.evaluate(wt)
        res_loh = self.sim.evaluate(loh)

        self.assertAlmostEqual(res_loh.effective_presented_neoantigens, 20.0, delta=1.0)
        self.assertLess(res_loh.effective_presented_neoantigens, res_wt.effective_presented_neoantigens)
        self.assertLess(res_loh.surface_mhc1_copies_per_cell, res_wt.surface_mhc1_copies_per_cell)
        # Sparing NK activation:
        self.assertLess(res_loh.nk_cell_missing_self_activation_prob, 0.25)
        self.assertFalse(res_loh.absolute_cd8_escape)

    def test_tap_downregulation_impairs_presentation(self):
        """Severe TAP1/2 downregulation limits ER peptide loading."""
        tap_def = APMGenotype(
            b2m_functional_alleles=2,
            hla_a_alleles=("A*02:01", "A*02:01"),
            hla_b_alleles=("B*07:02", "B*07:02"),
            hla_c_alleles=("C*07:01", "C*07:01"),
            hla_loh_occurred=False,
            lost_maternal_or_paternal="NONE",
            tap1_expression_fraction=0.08,
            tap2_expression_fraction=0.08,
            tapasin_expression_fraction=0.10,
            jak1_jak2_intact=False,
            baseline_clonal_neoantigens=30
        )
        res = self.sim.evaluate(tap_def)
        self.assertEqual(res.apm_loss_mechanism, "TAP_DEFECTIVE")
        self.assertLess(res.surface_mhc1_copies_per_cell, 4.0e4)


class TestMicroenvironmentBarriers(unittest.TestCase):
    """Verifies ECM biomechanics, T cell exclusion, and CD39/CD73 adenosine suppression."""

    def setUp(self):
        self.sim = PhysicalAndMetabolicBarrierSimulator()

    def test_collagen_desmoplasia_and_youngs_modulus(self):
        normal_env = MicroenvironmentBarriers(
            collagen_density_mg_ml=2.0, tgf_beta_active_pg_ml=100.0,
            caf_myofibroblast_density_cells_mm2=100.0, interstitial_fluid_pressure_mmhg=0.0,
            extracellular_atp_flux_um_hr=0.1, cd39_expression_fold=1.0, cd73_expression_fold=1.0
        )
        desmo_env = MicroenvironmentBarriers(
            collagen_density_mg_ml=20.0, tgf_beta_active_pg_ml=3000.0,
            caf_myofibroblast_density_cells_mm2=500.0, interstitial_fluid_pressure_mmhg=25.0,
            extracellular_atp_flux_um_hr=1.0, cd39_expression_fold=1.0, cd73_expression_fold=1.0
        )
        res_normal = self.sim.evaluate(normal_env)
        res_desmo = self.sim.evaluate(desmo_env)

        self.assertGreater(res_desmo.youngs_modulus_kpa, 20.0)
        self.assertLess(res_desmo.effective_pore_diameter_um, 3.5)
        self.assertLess(res_desmo.t_cell_motility_speed_um_min, 2.0)
        self.assertGreater(res_desmo.stromal_exclusion_index, 0.85)

    def test_adenosine_cascade_and_a2ar_suppression(self):
        """High CD39/CD73 expression generates micromolar adenosine blunting TCR signaling."""
        purinergic_env = MicroenvironmentBarriers(
            collagen_density_mg_ml=3.0, tgf_beta_active_pg_ml=200.0,
            caf_myofibroblast_density_cells_mm2=150.0, interstitial_fluid_pressure_mmhg=5.0,
            extracellular_atp_flux_um_hr=12.0, cd39_expression_fold=4.0, cd73_expression_fold=4.5
        )
        res = self.sim.evaluate(purinergic_env)

        self.assertGreater(res.extracellular_adenosine_conc_um, 1.5)
        self.assertGreater(res.a2ar_receptor_occupancy, 0.95)
        self.assertGreater(res.camp_pka_tcr_inhibition_pct, 80.0)

    def test_mdsc_arginine_depletion(self):
        high_mdsc_env = MicroenvironmentBarriers(
            collagen_density_mg_ml=3.0, tgf_beta_active_pg_ml=200.0,
            caf_myofibroblast_density_cells_mm2=150.0, interstitial_fluid_pressure_mmhg=5.0,
            extracellular_atp_flux_um_hr=1.0, cd39_expression_fold=1.0, cd73_expression_fold=1.0,
            mdsc_density_cells_mm2=450.0, arginase1_activity_fold=2.0
        )
        res = self.sim.evaluate(high_mdsc_env)
        self.assertGreater(res.mdsc_arginine_depletion_pct, 80.0)
        self.assertGreater(res.composite_metabolic_suppression_pct, 80.0)


class TestIntegratedTumorImmuneClassifier(unittest.TestCase):
    """Verifies end-to-end patient classification and combination therapy predictions."""

    def setUp(self):
        self.engine = IntegratedTumorImmuneEngine()

    def test_b2m_null_patient_classified_antigen_defective_with_zero_pd1_response(self):
        profile = PatientTumorProfile(
            patient_id="PAT-MEL-0001",
            cancer_type="MELANOMA",
            cgas_state=CGASSTINGState(30.0, 1.0, 1.0, 1.0, 1.0),
            apm_genotype=APMGenotype(
                0, ("A*02:01", "A*02:01"), ("B*07:02", "B*07:02"), ("C*07:01", "C*07:01"),
                False, "NONE", 1.0, 1.0, 1.0, True, 40
            ),
            barriers=MicroenvironmentBarriers(2.0, 200.0, 100.0, 2.0, 1.0, 1.0, 1.0),
            cd8_t_cell_periphery_density_mm2=500.0
        )
        pred = self.engine.analyze_patient(profile)

        self.assertEqual(pred.phenotype, TumorPhenotype.ANTIGEN_DEFECTIVE)
        self.assertEqual(pred.anti_pd1_monotherapy_response_prob, 0.0)
        self.assertIn("NK Cell Engager", pred.optimal_rational_regimen)

    def test_stromal_excluded_patient_response_and_rational_rescue(self):
        profile = PatientTumorProfile(
            patient_id="PAT-NSC-0002",
            cancer_type="NSCLC",
            cgas_state=CGASSTINGState(35.0, 1.0, 1.0, 1.0, 1.0),
            apm_genotype=APMGenotype(
                2, ("A*02:01", "A*24:02"), ("B*07:02", "B*44:02"), ("C*07:01", "C*04:01"),
                False, "NONE", 1.0, 1.0, 1.0, True, 35
            ),
            barriers=MicroenvironmentBarriers(
                collagen_density_mg_ml=18.0, tgf_beta_active_pg_ml=3000.0,
                caf_myofibroblast_density_cells_mm2=500.0, interstitial_fluid_pressure_mmhg=25.0,
                extracellular_atp_flux_um_hr=8.0, cd39_expression_fold=3.5, cd73_expression_fold=4.0
            ),
            cd8_t_cell_periphery_density_mm2=400.0
        )
        pred = self.engine.analyze_patient(profile)

        self.assertEqual(pred.phenotype, TumorPhenotype.IMMUNE_EXCLUDED)
        self.assertLess(pred.anti_pd1_monotherapy_response_prob, 0.20)
        self.assertGreater(pred.rational_combination_response_prob, 0.50)
        self.assertIn("TGF-beta", pred.optimal_rational_regimen)


class TestCohortAndStatisticalValidation(unittest.TestCase):
    """Verifies synthetic clinical trial generation and landmark statistical associations."""

    def test_pan_cancer_unselected_cohort_orr_benchmark(self):
        """Unselected solid tumor single-agent anti-PD-1 ORR must fall between 15% and 30%."""
        gen = SyntheticClinicalCohortGenerator(seed=2026)
        cohort = gen.generate_cohort(n_patients_per_arm=100) # 500 patients
        stats = evaluate_clinical_cohort(cohort)

        orr = stats["overall_anti_pd1_orr_pct"]
        self.assertGreaterEqual(orr, 15.0)
        self.assertLessEqual(orr, 30.0)

        # Melanoma response rate is higher than PDAC response rate
        mel_orr = stats["indication_breakdown"]["MELANOMA"]["pd1_resp"]
        pdac_orr = stats["indication_breakdown"]["PDAC"]["pd1_resp"]
        self.assertGreater(mel_orr, pdac_orr * 3)

    def test_hot_vs_cold_responder_enrichment_fisher_exact(self):
        """Verifies statistically significant response enrichment in Hot vs Cold/Excluded tumors."""
        gen = SyntheticClinicalCohortGenerator(seed=999)
        cohort = gen.generate_cohort(n_patients_per_arm=60) # 300 patients
        engine = IntegratedTumorImmuneEngine()

        hot_resp, hot_non_resp = 0, 0
        cold_resp, cold_non_resp = 0, 0

        for patient in cohort:
            pred = engine.analyze_patient(patient)
            patient_seed = sum(ord(c) for c in patient.patient_id)
            rng = np.random.default_rng(patient_seed)
            responded = rng.random() < pred.anti_pd1_monotherapy_response_prob

            if pred.phenotype == TumorPhenotype.HOT_INFLAMED:
                if responded:
                    hot_resp += 1
                else:
                    hot_non_resp += 1
            else:
                if responded:
                    cold_resp += 1
                else:
                    cold_non_resp += 1

        odds_ratio, p_value = fisher_exact_2x2(hot_resp, hot_non_resp, cold_resp, cold_non_resp)
        self.assertGreater(odds_ratio, 5.0)
        self.assertLess(p_value, 1.0e-5)

    def test_ground_truth_compliance_function(self):
        """Verifies the standalone verify_ground_truth_compliance function."""
        results = verify_ground_truth_compliance()
        for name, passed in results.items():
            self.assertTrue(passed, f"Ground truth test failed: {name}")


class TestSubclonalDynamicsAndClonalSweep(unittest.TestCase):
    """Verifies subclonal evolutionary dynamics, critical thresholds, and clonal sweeps."""

    def setUp(self):
        self.sim = SubclonalEvolutionSimulator()

    def test_subclonal_escape_and_acquired_resistance(self):
        # 5% initial B2M-null subclone under CD8 kill pressure
        cfg = SubclonalDynamicsConfig(
            initial_total_tumor_cells=1.0e9,
            subclonal_escape_fraction=0.05,
            tumor_growth_rate_per_day=0.03,
            cd8_cytotoxic_kill_rate_per_day=0.08,
            simulation_duration_days=180
        )
        res = self.sim.simulate(cfg)
        self.assertTrue(res.acquired_resistance_observed)
        self.assertLess(res.nadir_tumor_burden_fraction, 0.70)
        self.assertGreater(res.nadir_day, 10.0)
        self.assertGreater(res.final_subclonal_escape_fraction, 0.85)

    def test_analytical_primary_resistance_boundary(self):
        # When kill rate is 0.08 and growth rate is 0.03:
        # f_primary* = 1 - (0.03 / 0.08) = 1 - 0.375 = 0.625
        thresh = self.sim.calculate_analytical_thresholds(growth_rate=0.03, kill_rate=0.08)
        self.assertAlmostEqual(thresh, 0.625, places=3)

        # If subclonal escape fraction exceeds f_primary*, the tumor never regresses below baseline
        cfg_high = SubclonalDynamicsConfig(
            initial_total_tumor_cells=1.0e9,
            subclonal_escape_fraction=0.70,
            tumor_growth_rate_per_day=0.03,
            cd8_cytotoxic_kill_rate_per_day=0.08,
            simulation_duration_days=100
        )
        res_high = self.sim.simulate(cfg_high)
        self.assertGreaterEqual(res_high.nadir_tumor_burden_fraction, 0.95)
        self.assertEqual(res_high.nadir_day, 0.0)


class TestDualPurinergicA2ARAndA2BR(unittest.TestCase):
    """Verifies high-affinity A2AR vs low-affinity A2BR purinergic kinetics and dual inhibition."""

    def setUp(self):
        self.sim = DualPurinergicReceptorSimulator()

    def test_selective_a2ar_spares_a2br_myeloid_escape(self):
        cfg = DualPurinergicConfig(
            extracellular_adenosine_um=4.0,
            selective_a2ar_antagonist_conc_nm=1500.0,
            selective_a2ar_antagonist_ki_nm=3.0,
            selective_a2ar_antagonist_ki_a2br_nm=2500.0
        )
        res = self.sim.evaluate(cfg)
        self.assertTrue(res.is_a2br_escape_active)
        self.assertLess(res.tcell_a2ar_inhibition_pct, 30.0)
        self.assertGreater(res.myeloid_a2br_inhibition_pct, 50.0)
        self.assertGreater(res.composite_purinergic_suppression_pct, 30.0)

    def test_dual_antagonist_suppresses_both_receptors(self):
        cfg = DualPurinergicConfig(
            extracellular_adenosine_um=4.0,
            dual_antagonist_conc_nm=1500.0,
            dual_antagonist_ki_a2ar_nm=1.5,
            dual_antagonist_ki_a2br_nm=17.0
        )
        res = self.sim.evaluate(cfg)
        self.assertFalse(res.is_a2br_escape_active)
        self.assertLess(res.tcell_a2ar_inhibition_pct, 15.0)
        self.assertLess(res.myeloid_a2br_inhibition_pct, 10.0)
        self.assertLess(res.composite_purinergic_suppression_pct, 12.0)

    def test_cd73_enzymatic_inhibition_collapses_adenosine_pool(self):
        cfg = DualPurinergicConfig(
            extracellular_adenosine_um=5.0,
            cd73_enzymatic_inhibition_pct=90.0
        )
        res = self.sim.evaluate(cfg)
        self.assertAlmostEqual(res.effective_adenosine_um, 0.50, places=2)
        self.assertLess(res.a2br_occupancy_pct, 25.0)


class TestDynamicCombinatorialSequencing(unittest.TestCase):
    """Verifies timing, scheduling, and AICD prevention in multi-agent rescue regimens."""

    def setUp(self):
        self.sim = DynamicCombinatorialSequencingSimulator()

    def test_staged_priming_maximizes_cure_and_minimizes_aicd(self):
        res = self.sim.simulate(SequencingStrategy.STAGED_MECHANISTIC_PRIMING)
        self.assertGreater(res.durable_remission_probability, 0.65)
        self.assertLess(res.t_cell_exhaustion_or_aicd_pct, 18.0)
        self.assertGreater(res.core_t_cell_density_relative, 0.80)

    def test_concurrent_therapy_provokes_severe_aicd(self):
        res = self.sim.simulate(SequencingStrategy.CONCURRENT_TRIPLE)
        self.assertLess(res.durable_remission_probability, 0.35)
        self.assertGreater(res.t_cell_exhaustion_or_aicd_pct, 50.0)
        self.assertIn("HIGH", res.systemic_cytokine_toxicity_risk)


class TestIntercellularBystanderSTING(unittest.TestCase):
    """Verifies Connexin-43 gap junction transfer and bystander cDC1 priming."""

    def setUp(self):
        self.sim = IntercellularBystanderSTINGSimulator()

    def test_bystander_rescue_in_tumor_sting_silenced_cell(self):
        cfg = BystanderSTINGTransferConfig(
            tumor_cytosolic_cgamp_nm=25.0,
            tumor_has_functional_cgas=True,
            tumor_has_functional_sting=False,
            cx43_gap_junction_permeability_pct=90.0,
            extracellular_enpp1_fold=1.0,
            cdc1_sting_expression_fraction=1.0
        )
        res = self.sim.evaluate(cfg)
        self.assertFalse(res.tumor_autocrine_sting_active)
        self.assertTrue(res.cdc1_cross_priming_competent)
        self.assertTrue(res.bystander_rescue_operational)
        self.assertGreater(res.cdc1_sting_activation_fraction, 0.40)
        self.assertEqual(res.limiting_chokepoint, "NONE_ROBUST_CROSS_PRIMING")

    def test_cgas_deficient_tumor_yields_zero_bystander_priming(self):
        cfg = BystanderSTINGTransferConfig(
            tumor_cytosolic_cgamp_nm=25.0,
            tumor_has_functional_cgas=False,
            tumor_has_functional_sting=False,
            cx43_gap_junction_permeability_pct=90.0,
            cdc1_sting_expression_fraction=1.0
        )
        res = self.sim.evaluate(cfg)
        self.assertEqual(res.direct_gap_junction_flux_nm_s, 0.0)
        self.assertEqual(res.cdc1_intracellular_cgamp_nm, 0.0)
        self.assertFalse(res.bystander_rescue_operational)
        self.assertEqual(res.limiting_chokepoint, "TUMOR_CGAS_ABSENT")

    def test_cx43_closure_with_high_enpp1_abrogates_bystander_priming(self):
        cfg = BystanderSTINGTransferConfig(
            tumor_cytosolic_cgamp_nm=25.0,
            tumor_has_functional_cgas=True,
            tumor_has_functional_sting=False,
            cx43_gap_junction_permeability_pct=0.0,
            extracellular_enpp1_fold=5.0,
            cdc1_sting_expression_fraction=1.0
        )
        res = self.sim.evaluate(cfg)
        self.assertEqual(res.direct_gap_junction_flux_nm_s, 0.0)
        self.assertFalse(res.bystander_rescue_operational)
        self.assertIn("CX43", res.limiting_chokepoint)

    def test_host_cdc1_sting_deficiency_blocks_rescue(self):
        cfg = BystanderSTINGTransferConfig(
            tumor_cytosolic_cgamp_nm=25.0,
            tumor_has_functional_cgas=True,
            tumor_has_functional_sting=False,
            cx43_gap_junction_permeability_pct=90.0,
            cdc1_sting_expression_fraction=0.0
        )
        res = self.sim.evaluate(cfg)
        self.assertFalse(res.cdc1_cross_priming_competent)
        self.assertFalse(res.bystander_rescue_operational)
        self.assertEqual(res.limiting_chokepoint, "HOST_CDC1_STING_DEFICIENT")


class TestVascularCompressionPerfusion(unittest.TestCase):
    """Verifies solid stress, microvascular collapse, and macromolecular drug delivery."""

    def setUp(self):
        self.sim = VascularCompressionPerfusionSimulator()

    def test_normal_tissue_perfusion_and_delivery(self):
        cfg = SolidStressPerfusionConfig(
            collagen_density_mg_ml=2.0,
            hyaluronan_density_mg_ml=0.20
        )
        res = self.sim.evaluate(cfg)
        self.assertLess(res.macroscopic_solid_stress_mmhg, 6.0)
        self.assertGreater(res.fractional_vascular_patency_pct, 90.0)
        self.assertGreater(res.macromolecular_antibody_penetration_pct, 65.0)
        self.assertEqual(res.microvascular_collapse_state, "DECOMPRESSED_FUNCTIONAL_PERFUSION")

    def test_desmoplasia_drives_severe_vascular_collapse(self):
        cfg = SolidStressPerfusionConfig(
            collagen_density_mg_ml=22.0,
            hyaluronan_density_mg_ml=2.20
        )
        res = self.sim.evaluate(cfg)
        self.assertGreater(res.macroscopic_solid_stress_mmhg, 30.0)
        self.assertLess(res.fractional_vascular_patency_pct, 15.0)
        self.assertLess(res.macromolecular_antibody_penetration_pct, 10.0)
        self.assertEqual(res.microvascular_collapse_state, "SEVERE_MICROVASCULAR_COLLAPSE")

    def test_enzymatic_matrix_decompression_restores_antibody_delivery(self):
        cfg_decomp = SolidStressPerfusionConfig(
            collagen_density_mg_ml=22.0,
            hyaluronan_density_mg_ml=2.20,
            enzymatic_ha_depletion_pct=90.0,
            tgf_beta_inhibition_pct=60.0
        )
        res_decomp = self.sim.evaluate(cfg_decomp)
        self.assertLess(res_decomp.macroscopic_solid_stress_mmhg, 12.0)
        self.assertGreater(res_decomp.fractional_vascular_patency_pct, 70.0)
        self.assertGreater(res_decomp.macromolecular_antibody_penetration_pct, 50.0)
        self.assertEqual(res_decomp.microvascular_collapse_state, "DECOMPRESSED_FUNCTIONAL_PERFUSION")


if __name__ == "__main__":
    unittest.main()
