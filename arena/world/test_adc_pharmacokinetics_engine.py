"""
Comprehensive Test Suite for Antibody-Drug Conjugate (ADC) Pharmacokinetics Engine
==================================================================================
Validates biophysical mechanisms, mathematical limits, and empirical constants for:
1. Data structures, parameter assertions, and thermodynamic conversions
2. DAR optimization, HIC retention, and hydrophobicity-driven systemic clearance
3. Linker enzymatic stability (Cathepsin B/L vs. non-cleavable SMCC proteolysis)
4. Spatio-temporal bystander transport, membrane permeability, and tumor heterogeneity
5. Clinical benchmarks (T-DXd vs. T-DM1; DESTINY-Breast04 vs. EMILIA trial phenotypes)
6. Master analyze() programmatic interface and empirical evidence consilience
"""

import math
import unittest
import numpy as np

from adc_pharmacokinetics_engine import (
    LinkerType,
    PayloadClass,
    PayloadProperties,
    LinkerProperties,
    TumorMicroenvironmentParameters,
    SystemicPKParameters,
    DAROptimizationEngine,
    LinkerStabilityEngine,
    BystanderTransportEngine,
    BindingSiteBarrierEngine,
    PulmonaryToxicityILDEngine,
    MultiCycleResistanceEngine,
    ClinicalADCDatabase,
    analyze,
)


class TestEnumsAndDataStructures(unittest.TestCase):
    """Verifies data structure validation, physical conversions, and constraints."""

    def test_payload_properties_validation(self):
        # Valid payload
        p = PayloadProperties(
            name="TestPayload",
            payload_class=PayloadClass.TOPOISOMERASE_I_INHIBITOR,
            molecular_weight=450.0,
            log_p=1.5,
            log_d_74=1.4,
            p_app_cm_s=3.0e-6,
            potency_ic50_nm=2.0,
        )
        self.assertEqual(p.name, "TestPayload")
        self.assertAlmostEqual(p.p_app_cm_h, 3.0e-6 * 3600.0, places=5)
        self.assertTrue(p.is_membrane_permeable)

        # Invalid molecular weight
        with self.assertRaises(ValueError):
            PayloadProperties(
                name="BadMW",
                payload_class=PayloadClass.MICROTUBULE_INHIBITOR_AURISTATIN,
                molecular_weight=-100.0,
                log_p=1.0,
                log_d_74=1.0,
                p_app_cm_s=1e-6,
                potency_ic50_nm=1.0,
            )

        # Invalid negative permeability
        with self.assertRaises(ValueError):
            PayloadProperties(
                name="BadPapp",
                payload_class=PayloadClass.MICROTUBULE_INHIBITOR_AURISTATIN,
                molecular_weight=500.0,
                log_p=1.0,
                log_d_74=1.0,
                p_app_cm_s=-1e-6,
                potency_ic50_nm=1.0,
            )

        # Invalid zero or negative potency
        with self.assertRaises(ValueError):
            PayloadProperties(
                name="BadPotency",
                payload_class=PayloadClass.MICROTUBULE_INHIBITOR_AURISTATIN,
                molecular_weight=500.0,
                log_p=1.0,
                log_d_74=1.0,
                p_app_cm_s=1e-6,
                potency_ic50_nm=0.0,
            )

    def test_linker_properties_validation(self):
        linker = LinkerProperties(
            linker_type=LinkerType.CLEAVABLE_TETRAPEPTIDE_GGFG,
            name="GGFG",
            kcat_cathepsin_b_s=2.8,
            km_cathepsin_b_um=30.0,
            kcat_cathepsin_l_s=3.4,
            km_cathepsin_l_um=18.0,
            pabc_elimination_rate_min=0.0,
            plasma_deconjugation_rate_day=0.002,
            retro_michael_rate_day=0.0005,
            hydrophilicity_index=4.2,
            releases_free_payload=True,
        )
        self.assertGreater(linker.catalytic_efficiency_cathepsin_b, 0.0)
        expected_cat_eff_b = 2.8 / (30.0 * 1e-6)
        self.assertAlmostEqual(linker.catalytic_efficiency_cathepsin_b, expected_cat_eff_b, places=1)

        # Hydrophilicity index < 0.5 must raise
        with self.assertRaises(ValueError):
            LinkerProperties(
                linker_type=LinkerType.CLEAVABLE_DIPEPTIDE_VAL_CIT,
                name="BadLinker",
                kcat_cathepsin_b_s=1.0,
                km_cathepsin_b_um=10.0,
                kcat_cathepsin_l_s=1.0,
                km_cathepsin_l_um=10.0,
                pabc_elimination_rate_min=1.0,
                plasma_deconjugation_rate_day=0.01,
                retro_michael_rate_day=0.005,
                hydrophilicity_index=0.2,
                releases_free_payload=True,
            )

    def test_tumor_parameters_geometry_and_kd(self):
        tumor = TumorMicroenvironmentParameters(
            antigen_positive_fraction=0.4,
            receptor_density_ag_pos=1.0e6,
            cell_radius_um=8.0,
            kon_m_inv_s_inv=1.0e5,
            koff_s_inv=5.0e-5,
        )
        # Kd = koff / kon = 5e-5 / 1e5 = 5e-10 M = 0.5 nM
        self.assertAlmostEqual(tumor.kd_molar, 5.0e-10, places=12)

        # Single cell volume: (4/3) * pi * r^3
        r_cm = 8.0 * 1e-4
        expected_vol_l = (4.0 / 3.0) * math.pi * (r_cm ** 3) * 1e-3
        self.assertAlmostEqual(tumor.cell_volume_liters, expected_vol_l, places=16)

        # Surface area: 4 * pi * r^2
        expected_sa_cm2 = 4.0 * math.pi * (r_cm ** 2)
        self.assertAlmostEqual(tumor.cell_surface_area_cm2, expected_sa_cm2, places=12)

        # S/V ratio = 3 / r = 3 / 0.0008 = 3750 cm^-1
        self.assertAlmostEqual(tumor.surface_to_volume_ratio_cm_inv, 3750.0, places=5)

        # Fraction out of bounds
        with self.assertRaises(ValueError):
            TumorMicroenvironmentParameters(antigen_positive_fraction=1.5, receptor_density_ag_pos=1e5)


class TestDAROptimizationAndClearance(unittest.TestCase):
    """Verifies DAR biophysical scaling, Hamblett 2004 replication, and optimal DAR calculation."""

    def setUp(self):
        self.dxd_pay, self.dxd_link, self.dxd_pk = ClinicalADCDatabase.get_trastuzumab_deruxtecan()
        self.mmae_pay, self.mmae_link, self.mmae_pk = ClinicalADCDatabase.get_brentuximab_vedotin()
        self.tumor_env = TumorMicroenvironmentParameters(antigen_positive_fraction=0.3, receptor_density_ag_pos=1.0e5)

    def test_monomer_fraction_and_aggregation_cliff(self):
        """Monomer fraction must be high (>96%) for DAR <= 8, and drop steeply above 8."""
        monomer_2 = DAROptimizationEngine.calculate_soluble_monomer_fraction(2.0, self.dxd_pay, self.dxd_link)
        monomer_4 = DAROptimizationEngine.calculate_soluble_monomer_fraction(4.0, self.dxd_pay, self.dxd_link)
        monomer_8 = DAROptimizationEngine.calculate_soluble_monomer_fraction(8.0, self.dxd_pay, self.dxd_link)
        monomer_9 = DAROptimizationEngine.calculate_soluble_monomer_fraction(9.0, self.dxd_pay, self.dxd_link)
        monomer_10 = DAROptimizationEngine.calculate_soluble_monomer_fraction(10.0, self.dxd_pay, self.dxd_link)

        self.assertGreater(monomer_2, 0.98)
        self.assertGreater(monomer_4, 0.98)
        self.assertGreater(monomer_8, 0.96)
        # Drop sharply above 8
        self.assertLess(monomer_9, monomer_8)
        self.assertLess(monomer_10, 0.50)

    def test_hic_retention_factor_monotonicity(self):
        """HIC retention factor k'_HIC must increase monotonically with DAR."""
        hic_2 = DAROptimizationEngine.calculate_hic_retention_factor(2.0, self.dxd_pay, self.dxd_link)
        hic_4 = DAROptimizationEngine.calculate_hic_retention_factor(4.0, self.dxd_pay, self.dxd_link)
        hic_8 = DAROptimizationEngine.calculate_hic_retention_factor(8.0, self.dxd_pay, self.dxd_link)

        self.assertLess(hic_2, hic_4)
        self.assertLess(hic_4, hic_8)

    def test_hamblett_2004_cysteine_clearance_replication(self):
        """
        Hamblett et al. 2004 ground truth:
        cAC10-vcMMAE: E8 clears ~3-fold faster than E4 and ~5-fold faster than E2.
        """
        cl_2 = DAROptimizationEngine.calculate_systemic_clearance(2.0, self.mmae_pay, self.mmae_link, self.mmae_pk)
        cl_4 = DAROptimizationEngine.calculate_systemic_clearance(4.0, self.mmae_pay, self.mmae_link, self.mmae_pk)
        cl_8 = DAROptimizationEngine.calculate_systemic_clearance(8.0, self.mmae_pay, self.mmae_link, self.mmae_pk)

        ratio_8_to_4 = cl_8 / cl_4
        ratio_8_to_2 = cl_8 / cl_2

        # Ratio DAR 8 to DAR 4 should be approximately 3-fold (2.5 - 3.8)
        self.assertGreaterEqual(ratio_8_to_4, 2.5)
        self.assertLessEqual(ratio_8_to_4, 4.0)

        # Ratio DAR 8 to DAR 2 should be approximately 5-fold (4.0 - 6.5)
        self.assertGreaterEqual(ratio_8_to_2, 4.0)
        self.assertLessEqual(ratio_8_to_2, 6.5)

    def test_t_dxd_clearance_preservation_via_hydrophilic_linker(self):
        """T-DXd at DAR 7.7 preserves normal mAb-like clearance (< 0.50 L/day)."""
        cl_dxd_77 = DAROptimizationEngine.calculate_systemic_clearance(7.7, self.dxd_pay, self.dxd_link, self.dxd_pk)
        self.assertLess(cl_dxd_77, 0.50)
        self.assertGreater(cl_dxd_77, self.dxd_pk.baseline_mab_clearance_l_day)

    def test_fcrn_clearance_cliff_above_dar_8(self):
        """Clearance must surge precipitously once DAR exceeds 8 interchain cysteines."""
        cl_8 = DAROptimizationEngine.calculate_systemic_clearance(8.0, self.dxd_pay, self.dxd_link, self.dxd_pk)
        cl_10 = DAROptimizationEngine.calculate_systemic_clearance(10.0, self.dxd_pay, self.dxd_link, self.dxd_pk)
        self.assertGreater(cl_10, cl_8 * 3.0)

    def test_optimal_dar_optimization(self):
        """
        Optimal DAR search:
        - T-DXd optimal DAR should be between 7.0 and 8.0 (matches clinical DAR 7.7 - 8.0).
        - Brentuximab delivered tumor payload exposure peaks at DAR ~4.0.
        """
        opt_dxd = DAROptimizationEngine.find_optimal_dar(self.dxd_pay, self.dxd_link, self.dxd_pk, self.tumor_env)
        self.assertGreaterEqual(opt_dxd["optimal_dar"], 7.0)
        self.assertLessEqual(opt_dxd["optimal_dar"], 8.0)

        # Brentuximab discrete comparisons
        opt_mmae = DAROptimizationEngine.find_optimal_dar(self.mmae_pay, self.mmae_link, self.mmae_pk, self.tumor_env)
        disc_mmae = opt_mmae["discrete_comparisons"]
        exp_dar2 = disc_mmae["DAR_2.0"]["delivered_payload_exposure"]
        exp_dar4 = disc_mmae["DAR_4.0"]["delivered_payload_exposure"]
        exp_dar8 = disc_mmae["DAR_8.0"]["delivered_payload_exposure"]
        
        # Exposure peaks at DAR 4 for MMAE
        self.assertGreater(exp_dar4, exp_dar2)
        self.assertGreater(exp_dar4, exp_dar8)


class TestLinkerStabilityAndEnzymaticCleavage(unittest.TestCase):
    """Verifies Cathepsin B/L kinetics, PABC self-immolation, and non-cleavable resistance."""

    def setUp(self):
        self.dxd_pay, self.dxd_link, self.dxd_pk = ClinicalADCDatabase.get_trastuzumab_deruxtecan()
        self.dm1_pay, self.dm1_link, self.dm1_pk = ClinicalADCDatabase.get_trastuzumab_emtansine()
        self.mmae_pay, self.mmae_link, self.mmae_pk = ClinicalADCDatabase.get_brentuximab_vedotin()

    def test_cathepsin_cleavage_velocity(self):
        """Cleavable tetrapeptide GGFG and dipeptide Val-Cit are cleaved rapidly in lysosomes."""
        cleav_ggfg = LinkerStabilityEngine.calculate_lysosomal_cleavage_rate(5.0, self.dxd_link)
        self.assertGreater(cleav_ggfg["total_enzymatic_cleavage_rate_um_h"], 10.0)
        self.assertLess(cleav_ggfg["effective_release_half_life_min"], 30.0)

    def test_non_cleavable_smcc_enzymatic_resistance(self):
        """Non-cleavable SMCC shows zero cathepsin cleavage velocity and requires mAb proteolysis."""
        cleav_smcc = LinkerStabilityEngine.calculate_lysosomal_cleavage_rate(5.0, self.dm1_link)
        self.assertEqual(cleav_smcc["cathepsin_b_rate_um_h"], 0.0)
        self.assertEqual(cleav_smcc["cathepsin_l_rate_um_h"], 0.0)
        self.assertEqual(cleav_smcc["total_enzymatic_cleavage_rate_um_h"], 0.0)
        self.assertGreater(cleav_smcc["proteolytic_degradation_rate_um_h"], 0.0)
        # Proteolytic half-life is around 3.85 hours (~230 min)
        self.assertGreater(cleav_smcc["effective_release_half_life_min"], 180.0)

    def test_pabc_elimination_rate(self):
        """PABC self-immolation occurs within minutes (t1/2 < 1 min for Brentuximab)."""
        cleav_mmae = LinkerStabilityEngine.calculate_lysosomal_cleavage_rate(5.0, self.mmae_link)
        self.assertGreater(cleav_mmae["pabc_elimination_half_life_min"], 0.0)
        self.assertLess(cleav_mmae["pabc_elimination_half_life_min"], 1.0)

    def test_premature_plasma_deconjugation_simulation(self):
        """21-day plasma simulation returns non-negative free payload AUC and valid toxicity scores."""
        sim = LinkerStabilityEngine.simulate_premature_systemic_deconjugation(
            duration_days=21.0,
            dar=7.7,
            dose_mg_kg=5.4,
            linker=self.dxd_link,
            payload=self.dxd_pay,
            pk_params=self.dxd_pk,
        )
        self.assertGreater(sim["auc_free_nm_h"], 0.0)
        self.assertGreater(sim["cmax_free_nm"], 0.0)
        # Fraction deconjugated in plasma over 21 days for GGFG is < 5%
        self.assertLess(sim["fraction_deconjugated_21d"], 0.05)
        # Organ toxicity scores must be bounded in [0, 1]
        self.assertGreaterEqual(sim["ild_risk_score"], 0.0)
        self.assertLessEqual(sim["ild_risk_score"], 1.0)
        self.assertGreaterEqual(sim["hematologic_risk_score"], 0.0)
        self.assertLessEqual(sim["hematologic_risk_score"], 1.0)


class TestBystanderTransportAndHeterogeneity(unittest.TestCase):
    """Verifies membrane permeability disparity, penetration length, and tumor heterogeneity response."""

    def setUp(self):
        self.dxd_pay, self.dxd_link, self.dxd_pk = ClinicalADCDatabase.get_trastuzumab_deruxtecan()
        self.dm1_pay, self.dm1_link, self.dm1_pk = ClinicalADCDatabase.get_trastuzumab_emtansine()

    def test_membrane_permeability_contrast(self):
        """DXd (PAMPA Papp ~3e-6 cm/s) vs Lys-MCC-DM1 (Papp <= 1e-9 cm/s) >3000-fold contrast."""
        papp_dxd = self.dxd_pay.p_app_cm_s
        papp_dm1 = self.dm1_pay.p_app_cm_s
        ratio = papp_dxd / papp_dm1
        self.assertGreaterEqual(ratio, 3000.0)
        self.assertTrue(self.dxd_pay.is_membrane_permeable)
        self.assertFalse(self.dm1_pay.is_membrane_permeable)

    def test_bystander_penetration_length(self):
        """DXd penetration length > 100 um; Lys-MCC-DM1 penetration length < 1 um."""
        tumor_env = TumorMicroenvironmentParameters(antigen_positive_fraction=0.3, receptor_density_ag_pos=1.0e5)
        len_dxd = BystanderTransportEngine.calculate_bystander_penetration_length(self.dxd_pay, tumor_env)
        len_dm1 = BystanderTransportEngine.calculate_bystander_penetration_length(self.dm1_pay, tumor_env)

        self.assertGreater(len_dxd, 100.0)
        self.assertLess(len_dm1, 1.0)

    def test_critical_antigen_positive_fraction_boundary(self):
        """
        Critical antigen fraction f_Ag+* required for tumor regression:
        - T-DXd: ~10-20% (HER2-low responsive)
        - T-DM1: >= 90% (HER2-low failure)
        """
        tumor_env = TumorMicroenvironmentParameters(antigen_positive_fraction=0.5, receptor_density_ag_pos=1.0e5)
        f_crit_dxd = BystanderTransportEngine.derive_critical_antigen_positive_fraction(
            7.7, self.dxd_pay, self.dxd_link, tumor_env
        )
        f_crit_dm1 = BystanderTransportEngine.derive_critical_antigen_positive_fraction(
            3.5, self.dm1_pay, self.dm1_link, tumor_env
        )

        self.assertGreaterEqual(f_crit_dxd, 0.05)
        self.assertLessEqual(f_crit_dxd, 0.25)
        self.assertGreaterEqual(f_crit_dm1, 0.90)

    def test_her2_low_heterogeneous_tumor_ode_simulation(self):
        """
        Simulates 21-day ODE in HER2-low tumor (f_Ag+ = 0.25):
        - T-DXd achieves profound tumor growth inhibition (>80%) and high bystander killing (BKR > 0.85).
        - T-DM1 fails to inhibit tumor (TGI < 0% due to expansion of Ag- clones) and BKR == 0.
        """
        her2_low_tumor = TumorMicroenvironmentParameters(
            antigen_positive_fraction=0.25,
            receptor_density_ag_pos=1.0e5,
        )

        sim_dxd = BystanderTransportEngine.simulate_tumor_response_21d(
            dar=7.7,
            payload=self.dxd_pay,
            linker=self.dxd_link,
            pk_params=self.dxd_pk,
            tumor_params=her2_low_tumor,
            duration_days=21.0,
        )

        sim_dm1 = BystanderTransportEngine.simulate_tumor_response_21d(
            dar=3.5,
            payload=self.dm1_pay,
            linker=self.dm1_link,
            pk_params=self.dm1_pk,
            tumor_params=her2_low_tumor,
            duration_days=21.0,
        )

        # T-DXd efficacy in HER2-low
        self.assertGreater(sim_dxd["tumor_growth_inhibition_pct"], 80.0)
        self.assertGreater(sim_dxd["bystander_killing_ratio"], 0.85)

        # T-DM1 failure in HER2-low
        self.assertLess(sim_dm1["tumor_growth_inhibition_pct"], 0.0)  # Tumor progression
        self.assertEqual(sim_dm1["bystander_killing_ratio"], 0.0)     # Zero bystander killing

    def test_her2_amplified_pure_tumor_ode_simulation(self):
        """In pure HER2 3+ tumor (f_Ag+ = 1.0), both T-DXd and T-DM1 achieve potent tumor killing (>90%)."""
        her2_3plus_tumor = TumorMicroenvironmentParameters(
            antigen_positive_fraction=1.0,
            receptor_density_ag_pos=1.5e6,
        )

        sim_dxd = BystanderTransportEngine.simulate_tumor_response_21d(
            dar=7.7,
            payload=self.dxd_pay,
            linker=self.dxd_link,
            pk_params=self.dxd_pk,
            tumor_params=her2_3plus_tumor,
            duration_days=21.0,
        )

        sim_dm1 = BystanderTransportEngine.simulate_tumor_response_21d(
            dar=3.5,
            payload=self.dm1_pay,
            linker=self.dm1_link,
            pk_params=self.dm1_pk,
            tumor_params=her2_3plus_tumor,
            duration_days=21.0,
        )

        self.assertGreater(sim_dxd["tumor_growth_inhibition_pct"], 90.0)
        self.assertGreater(sim_dm1["tumor_growth_inhibition_pct"], 90.0)

    def test_ode_state_positivity(self):
        """All concentrations and cell fractions must remain non-negative throughout simulation."""
        tumor = TumorMicroenvironmentParameters(antigen_positive_fraction=0.3, receptor_density_ag_pos=1e5)
        sim = BystanderTransportEngine.simulate_tumor_response_21d(
            dar=7.7,
            payload=self.dxd_pay,
            linker=self.dxd_link,
            pk_params=self.dxd_pk,
            tumor_params=tumor,
            duration_days=21.0,
        )
        self.assertTrue(np.all(sim["c_adc_plasma"] >= -1e-8))
        self.assertTrue(np.all(sim["c_free_plasma"] >= -1e-8))
        self.assertTrue(np.all(sim["n_ag_pos"] >= -1e-8))
        self.assertTrue(np.all(sim["n_ag_neg"] >= -1e-8))


class TestClinicalDatabaseAndBenchmark(unittest.TestCase):
    """Verifies curated clinical database and DESTINY-Breast04 vs EMILIA trial recreation."""

    def test_curated_profiles(self):
        dxd_p, dxd_l, dxd_pk = ClinicalADCDatabase.get_trastuzumab_deruxtecan()
        dm1_p, dm1_l, dm1_pk = ClinicalADCDatabase.get_trastuzumab_emtansine()
        mmae_p, mmae_l, mmae_pk = ClinicalADCDatabase.get_brentuximab_vedotin()

        self.assertEqual(dxd_p.name, "DXd")
        self.assertEqual(dm1_p.name, "Lys-MCC-DM1")
        self.assertEqual(mmae_p.name, "MMAE")

    def test_destiny_breast04_heterogeneity_comparison(self):
        comp = ClinicalADCDatabase.compare_t_dxd_vs_t_dm1_heterogeneity([0.10, 0.25, 0.50, 0.85, 1.0])
        rows = comp["comparison_table"]
        self.assertEqual(len(rows), 5)

        # For f_Ag+ = 0.10 (HER2-low)
        row_01 = rows[0]
        self.assertGreater(row_01["t_dxd_tgi_pct"], 50.0)
        self.assertLess(row_01["t_dm1_tgi_pct"], 0.0)

        # For f_Ag+ = 1.0 (HER2 3+)
        row_10 = rows[-1]
        self.assertGreater(row_10["t_dxd_tgi_pct"], 90.0)
        self.assertGreater(row_10["t_dm1_tgi_pct"], 90.0)


class TestBindingSiteBarrierEngine(unittest.TestCase):
    """Verifies spatial reaction-diffusion tumor cord microdosimetry and binding site barrier bypass."""

    def setUp(self):
        self.dxd_p, self.dxd_l, _ = ClinicalADCDatabase.get_trastuzumab_deruxtecan()
        self.dm1_p, self.dm1_l, _ = ClinicalADCDatabase.get_trastuzumab_emtansine()
        self.tumor = TumorMicroenvironmentParameters(antigen_positive_fraction=0.3, receptor_density_ag_pos=1.5e5)

    def test_tumor_cord_spatial_resolution(self):
        cord = BindingSiteBarrierEngine.simulate_tumor_cord_spatial_profile(
            7.7, self.dxd_p, self.dxd_l, self.tumor, num_shells=14
        )
        self.assertEqual(len(cord["radii_um"]), 14)
        self.assertAlmostEqual(cord["radii_um"][0], 15.0, places=1)
        self.assertAlmostEqual(cord["radii_um"][-1], 145.0, places=1)

    def test_binding_site_barrier_intact_adc_restriction(self):
        # In a target-dense cord, intact antibody is restricted perivascularly by the binding site barrier
        cord = BindingSiteBarrierEngine.simulate_tumor_cord_spatial_profile(
            7.7, self.dxd_p, self.dxd_l, self.tumor,
            perivascular_antigen_positive_fraction=0.8,
            distal_antigen_positive_fraction=0.8,
        )
        # Distal / perivascular ratio < 0.05 (measured ~0.0015)
        self.assertLess(cord["intact_adc_penetration_ratio"], 0.05)
        self.assertGreater(cord["intact_adc_perivascular_nm"], cord["intact_adc_distal_nm"])

    def test_dxd_bypasses_barrier_vs_dm1_failure(self):
        cord_dxd = BindingSiteBarrierEngine.simulate_tumor_cord_spatial_profile(
            7.7, self.dxd_p, self.dxd_l, self.tumor
        )
        cord_dm1 = BindingSiteBarrierEngine.simulate_tumor_cord_spatial_profile(
            3.5, self.dm1_p, self.dm1_l, self.tumor
        )
        # T-DXd delivers lethal payload across 100% of cord
        self.assertEqual(cord_dxd["cord_kill_fraction"], 1.0)
        self.assertTrue(cord_dxd["bypasses_binding_site_barrier"])
        self.assertGreater(cord_dxd["payload_distal_nm"], self.dxd_p.potency_ic50_nm)

        # T-DM1 distal payload is 0.000 in Ag- cord region
        self.assertAlmostEqual(cord_dm1["payload_distal_nm"], 0.0, places=4)
        self.assertLess(cord_dm1["cord_kill_fraction"], 0.35)
        self.assertFalse(cord_dm1["bypasses_binding_site_barrier"])


class TestPulmonaryToxicityILDEngine(unittest.TestCase):
    """Verifies dose-dependent Interstitial Lung Disease modeling and steroid intervention."""

    def setUp(self):
        self.dxd_p, self.dxd_l, self.dxd_pk = ClinicalADCDatabase.get_trastuzumab_deruxtecan()
        self.dm1_p, self.dm1_l, self.dm1_pk = ClinicalADCDatabase.get_trastuzumab_emtansine()

    def test_dxd_dose_non_linear_ild_risk(self):
        ild_54 = PulmonaryToxicityILDEngine.evaluate_pulmonary_toxicity(5.4, self.dxd_p, self.dxd_l, self.dxd_pk)
        ild_64 = PulmonaryToxicityILDEngine.evaluate_pulmonary_toxicity(6.4, self.dxd_p, self.dxd_l, self.dxd_pk)
        ild_80 = PulmonaryToxicityILDEngine.evaluate_pulmonary_toxicity(8.0, self.dxd_p, self.dxd_l, self.dxd_pk)

        # Calibrated against DESTINY-Breast04 (12.1%) and DESTINY-Gastric01 (15.3%)
        self.assertAlmostEqual(ild_54["overall_ild_incidence_pct"], 11.8, places=0)
        self.assertGreater(ild_64["overall_ild_incidence_pct"], ild_54["overall_ild_incidence_pct"])
        self.assertGreater(ild_80["overall_ild_incidence_pct"], 25.0)

    def test_steroid_intervention_mitigation(self):
        unmitigated = PulmonaryToxicityILDEngine.evaluate_pulmonary_toxicity(5.4, self.dxd_p, self.dxd_l, self.dxd_pk, steroid_intervention=False)
        steroids = PulmonaryToxicityILDEngine.evaluate_pulmonary_toxicity(5.4, self.dxd_p, self.dxd_l, self.dxd_pk, steroid_intervention=True)

        severe_unmitigated = unmitigated["grade_3_4_severe_pct"] + unmitigated["grade_5_fatal_pct"]
        severe_steroids = steroids["grade_3_4_severe_pct"] + steroids["grade_5_fatal_pct"]

        # Steroids reduce severe/fatal ILD by >70%
        self.assertLess(severe_steroids, severe_unmitigated * 0.30)

    def test_t_dm1_minimal_ild_risk(self):
        ild_dm1 = PulmonaryToxicityILDEngine.evaluate_pulmonary_toxicity(3.6, self.dm1_p, self.dm1_l, self.dm1_pk)
        self.assertLess(ild_dm1["overall_ild_incidence_pct"], 0.5)


class TestMultiCycleResistanceEngine(unittest.TestCase):
    """Verifies longitudinal 6-cycle Q3W therapy, shed antigen sink, and clonal evolution."""

    def setUp(self):
        self.dxd_p, self.dxd_l, self.dxd_pk = ClinicalADCDatabase.get_trastuzumab_deruxtecan()
        self.dm1_p, self.dm1_l, self.dm1_pk = ClinicalADCDatabase.get_trastuzumab_emtansine()
        self.tumor = TumorMicroenvironmentParameters(antigen_positive_fraction=0.3, receptor_density_ag_pos=1.5e5)

    def test_multicycle_regimen_execution(self):
        res_dxd = MultiCycleResistanceEngine.simulate_multicycle_regimen(
            7.7, self.dxd_p, self.dxd_l, self.dxd_pk, self.tumor, num_cycles=6
        )
        self.assertEqual(len(res_dxd["cycle_history"]), 6)
        self.assertTrue(res_dxd["progression_free_at_day_126"])
        self.assertLess(res_dxd["final_volume_day_126"], 0.20)

    def test_t_dm1_multicycle_progression_in_heterogeneous_tumors(self):
        res_dm1 = MultiCycleResistanceEngine.simulate_multicycle_regimen(
            3.5, self.dm1_p, self.dm1_l, self.dm1_pk, self.tumor, num_cycles=6
        )
        # T-DM1 fails by cycle 2-3 and shows progressive disease at Day 126
        self.assertFalse(res_dm1["progression_free_at_day_126"])
        self.assertGreater(res_dm1["final_volume_day_126"], 1.50)


class TestMasterAnalyzeInterface(unittest.TestCase):
    """Verifies the master analyze() API endpoint, claims, and quantitative evidence dictionary."""

    def test_analyze_structure_and_evidence(self):
        res = analyze()
        self.assertIn("domain", res)
        self.assertIn("claims", res)
        self.assertIn("confidence", res)
        self.assertIn("evidence", res)

        self.assertGreaterEqual(res["confidence"], 0.95)
        self.assertGreaterEqual(len(res["claims"]), 8)

        ev = res["evidence"]
        self.assertIn("hamblett_2004_dar_clearance_ratio", ev)
        self.assertIn("t_dxd_clinical_clearance_l_day", ev)
        self.assertIn("dxd_apparent_permeability_cm_s", ev)
        self.assertIn("lys_mcc_dm1_permeability_cm_s", ev)
        self.assertIn("t_dxd_critical_antigen_fraction", ev)
        self.assertIn("t_dm1_critical_antigen_fraction", ev)
        self.assertIn("t_dxd_cord_kill_fraction", ev)
        self.assertIn("t_dm1_cord_kill_fraction", ev)
        self.assertIn("t_dxd_ild_rate_54", ev)
        self.assertIn("t_dxd_ild_rate_64", ev)
        self.assertIn("t_dm1_ild_rate", ev)
        self.assertIn("t_dxd_day_126_pfs", ev)
        self.assertIn("t_dm1_day_126_pfs", ev)

        self.assertAlmostEqual(ev["t_dxd_clinical_clearance_l_day"], 0.42, places=2)
        self.assertAlmostEqual(ev["dxd_apparent_permeability_cm_s"], 3.0e-6, places=8)
        self.assertLess(ev["t_dxd_critical_antigen_fraction"], 0.20)
        self.assertGreater(ev["t_dm1_critical_antigen_fraction"], 0.90)
        self.assertEqual(ev["t_dxd_cord_kill_fraction"], 1.0)
        self.assertLess(ev["t_dm1_cord_kill_fraction"], 0.35)
        self.assertTrue(ev["t_dxd_day_126_pfs"])
        self.assertFalse(ev["t_dm1_day_126_pfs"])


if __name__ == "__main__":
    unittest.main()
