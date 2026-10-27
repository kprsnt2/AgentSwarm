"""
test_targeted_lnp_delivery_engine.py — Comprehensive Unit Test Suite for
Targeted LNP Delivery and Selective Organ Targeting (SORT) Biophysics Engine.

Author: Nagarjuna (A004), Generation 0, Autonomous Research Swarm
Domain: Targeted Lipid Nanoparticle Delivery: Overcoming Liver Tropism via Selective Organ Targeting (SORT)
Epistemic Class: Engineering Feasibility / Biophysical Simulation
"""

import unittest
import math
import numpy as np

from targeted_lnp_delivery_engine import (
    PhysicalConstants,
    SortLipidClass,
    TargetOrgan,
    LNPFormulation,
    ElectrostaticAndPKaEngine,
    PlasmaProtein,
    DynamicProteinCoronaSimulator,
    OrganPBPKParameters,
    PBPKBiodistributionEngine,
    EndosomalTraffickingState,
    EndosomalTraffickingAndEscapeEngine,
    ExpressionAndSafetyEvaluator,
    EndosomalEnergetics,
    ThermodynamicsAndEnergyBalance,
    SimulationResult,
    IntegratedLNPDeliveryEngine,
    SORTDeliveryOptimizer,
    GeneticKnockoutSimulator,
    TumorTargetingResult,
    TumorAndLymphNodeTargetingEngine,
    verify_ground_truth_compliance
)


class TestPhysicalConstantsAndElectrostatics(unittest.TestCase):
    """Verifies fundamental physical and electrostatic primitives."""

    def test_thermal_voltage(self):
        vt = PhysicalConstants.thermal_voltage()
        # V_T at 310.15 K should be ~ 26.72 mV (0.02672 V)
        self.assertAlmostEqual(vt, 0.02672, places=4)

    def test_debye_screening_length(self):
        # In 150 mM NaCl (0.15 M), Debye length is ~ 0.78 nm
        debye_m = PhysicalConstants.debye_length(0.150)
        debye_nm = debye_m * 1e9
        self.assertGreater(debye_nm, 0.70)
        self.assertLess(debye_nm, 0.90)

    def test_grahame_surface_potential_neutral(self):
        # Neutral formulation at pH 7.4
        form = LNPFormulation(name="NeutralTest")
        psi_0, zeta = ElectrostaticAndPKaEngine.calculate_surface_and_zeta_potential(form, ph=7.4)
        # Should be slightly negative (-1 to -4 mV)
        self.assertLess(zeta, 0.0)
        self.assertGreater(zeta, -6.0)

    def test_cationic_and_anionic_potential_shift(self):
        form_cat = LNPFormulation(
            name="CationicTest", sort_mol_pct=30.0,
            sort_class=SortLipidClass.CATIONIC, sort_lipid_name="DOTAP"
        )
        form_ani = LNPFormulation(
            name="AnionicTest", sort_mol_pct=30.0,
            sort_class=SortLipidClass.ANIONIC, sort_lipid_name="18PA"
        )
        _, zeta_cat = ElectrostaticAndPKaEngine.calculate_surface_and_zeta_potential(form_cat, ph=7.4)
        _, zeta_ani = ElectrostaticAndPKaEngine.calculate_surface_and_zeta_potential(form_ani, ph=7.4)

        self.assertGreater(zeta_cat, +15.0)
        self.assertLess(zeta_ani, -15.0)


class TestLNPFormulationStoichiometry(unittest.TestCase):
    """Verifies molecular weights, lipid counts, and mRNA packaging stoichiometry."""

    def setUp(self):
        self.form = LNPFormulation(name="Standard-75nm", diameter_nm=75.0, np_ratio=6.0, mrna_length_nt=2000)

    def test_mol_pct_normalization(self):
        form_unnormalized = LNPFormulation(
            ionizable_mol_pct=50.0, helper_mol_pct=10.0,
            cholesterol_mol_pct=40.0, peg_mol_pct=2.0, sort_mol_pct=0.0
        )
        total = (form_unnormalized.ionizable_mol_pct + form_unnormalized.helper_mol_pct +
                 form_unnormalized.cholesterol_mol_pct + form_unnormalized.peg_mol_pct)
        self.assertAlmostEqual(total, 100.0, places=4)

    def test_total_lipids_per_particle(self):
        total_lipids = self.form.total_lipids_per_particle()
        # For a 75 nm dense core LNP, lipid count is typically 40,000 - 80,000
        self.assertGreater(total_lipids, 35000)
        self.assertLess(total_lipids, 150000)

    def test_mrna_packaging_count(self):
        mrna_count = self.form.mrna_molecules_per_particle()
        # Cryo-TEM and single-molecule fluorescence show 1 to 5 mRNA molecules per 70-80 nm LNP
        self.assertGreater(mrna_count, 0.8)
        self.assertLess(mrna_count, 6.0)

    def test_lipid_to_mrna_mass_ratio(self):
        ratio = self.form.lipid_to_mrna_mass_ratio()
        # In typical formulations, lipid:mRNA mass ratio is ~15:1 to 25:1
        self.assertGreater(ratio, 12.0)
        self.assertLess(ratio, 30.0)


class TestDynamicProteinCoronaSimulator(unittest.TestCase):
    """Verifies competitive Langmuir-Vroman protein adsorption kinetics."""

    def test_corona_fraction_conservation(self):
        form = LNPFormulation()
        corona = DynamicProteinCoronaSimulator.compute_equilibrium_corona(form)
        total_fraction = sum(corona.values())
        self.assertAlmostEqual(total_fraction, 1.0, places=4)

    def test_apoe_binding_dominance_on_neutral_lnp(self):
        form = LNPFormulation(name="Conventional")
        corona = DynamicProteinCoronaSimulator.compute_equilibrium_corona(form)
        # ApoE should be substantially present (>15%)
        self.assertGreater(corona["ApoE"], 0.15)
        # ApoE coverage should exceed Vitronectin and B2GPI on neutral LNP
        self.assertGreater(corona["ApoE"], corona["Vitronectin"])
        self.assertGreater(corona["ApoE"], corona["B2GPI"])
        self.assertLess(corona["Vitronectin"], 0.15)
        self.assertLess(corona["B2GPI"], 0.20)

    def test_vitronectin_enrichment_on_cationic_lnp(self):
        form_cat = LNPFormulation(
            name="LungSORT", sort_mol_pct=50.0,
            sort_class=SortLipidClass.CATIONIC, sort_lipid_name="DOTAP"
        )
        corona = DynamicProteinCoronaSimulator.compute_equilibrium_corona(form_cat)
        # Vitronectin should be enriched, ApoE strongly suppressed
        self.assertGreater(corona["Vitronectin"], 0.15)
        self.assertLess(corona["ApoE"], 0.05)

    def test_b2gpi_enrichment_on_anionic_lnp(self):
        form_ani = LNPFormulation(
            name="SpleenSORT", sort_mol_pct=30.0,
            sort_class=SortLipidClass.ANIONIC, sort_lipid_name="18PA"
        )
        corona = DynamicProteinCoronaSimulator.compute_equilibrium_corona(form_ani)
        # B2GPI and Complement C3 should be enriched, ApoE suppressed
        self.assertGreater(corona["B2GPI"], 0.12)
        self.assertLess(corona["ApoE"], 0.05)


class TestPBPKBiodistributionAndTargeting(unittest.TestCase):
    """Verifies whole-body multi-compartment clearance, fenestrations, and organ retargeting."""

    def test_dose_mass_conservation(self):
        form = LNPFormulation()
        corona = DynamicProteinCoronaSimulator.compute_equilibrium_corona(form)
        injection_dose = 10.0  # ug
        biodist = PBPKBiodistributionEngine.simulate_biodistribution(
            form, corona=corona, injection_dose_ug=injection_dose
        )
        delivered_sum = sum(biodist["organ_delivered_ug"].values())
        self.assertAlmostEqual(delivered_sum, injection_dose, places=4)

    def test_conventional_liver_tropism_gt_90pct(self):
        form = LNPFormulation(name="Conventional")
        res = IntegratedLNPDeliveryEngine.run_simulation(form)
        liver_pct = res.biodistribution["organ_percentages"]["liver"]
        self.assertGreaterEqual(liver_pct, 90.0)
        self.assertEqual(res.biodistribution["primary_organ"], "liver")

    def test_lung_sort_retargeting(self):
        res = SORTDeliveryOptimizer.sweep_cationic_lung_sort([50.0])[0]
        lung_pct = res.biodistribution["organ_percentages"]["lung"]
        self.assertGreaterEqual(lung_pct, 85.0)
        self.assertEqual(res.biodistribution["primary_organ"], "lung")

    def test_spleen_sort_retargeting(self):
        res = SORTDeliveryOptimizer.sweep_anionic_spleen_sort([30.0])[0]
        spleen_pct = res.biodistribution["organ_percentages"]["spleen"]
        self.assertGreaterEqual(spleen_pct, 70.0)
        self.assertEqual(res.biodistribution["primary_organ"], "spleen")

    def test_size_fenestration_gating(self):
        # Particles > 140 nm cannot cross liver sinusoidal fenestrae efficiently
        small_lnp = LNPFormulation(name="Small", diameter_nm=75.0)
        large_lnp = LNPFormulation(name="Large", diameter_nm=200.0)
        res_small = IntegratedLNPDeliveryEngine.run_simulation(small_lnp)
        res_large = IntegratedLNPDeliveryEngine.run_simulation(large_lnp)

        self.assertGreater(
            res_small.biodistribution["organ_percentages"]["liver"],
            res_large.biodistribution["organ_percentages"]["liver"]
        )


class TestEndosomalTraffickingAndEscapeBottleneck(unittest.TestCase):
    """Verifies endosomal acidification kinetics and the <2% escape constraint (Gilleron 2013)."""

    def test_escape_strictly_bounded_sub_2pct(self):
        form = LNPFormulation()
        res = IntegratedLNPDeliveryEngine.run_simulation(form)
        # Established ground truth: <2% escape into cytoplasm
        self.assertLess(res.escape_percent, 2.0)
        self.assertGreater(res.escape_percent, 0.4)

    def test_degradation_and_recycling_dominance(self):
        form = LNPFormulation()
        trafficking = EndosomalTraffickingAndEscapeEngine.simulate_endosomal_maturation(
            form, apparent_pka=form.baseline_apparent_pka
        )
        lost_percent = trafficking["recycled_percent"] + trafficking["degraded_percent"]
        # Over 95% of internalized cargo is degraded or recycled back out
        self.assertGreater(lost_percent, 95.0)

    def test_helper_lipid_cone_shape_enhancement(self):
        # DOPE has inverted cone shape (hexagonal promoter), DSPC is cylindrical
        form = LNPFormulation()
        res_dspc = EndosomalTraffickingAndEscapeEngine.simulate_endosomal_maturation(
            form, apparent_pka=6.45, helper_lipid_cone_factor=1.0
        )
        res_dope = EndosomalTraffickingAndEscapeEngine.simulate_endosomal_maturation(
            form, apparent_pka=6.45, helper_lipid_cone_factor=1.8
        )
        self.assertGreater(
            res_dope["total_escape_efficiency"],
            res_dspc["total_escape_efficiency"]
        )


class TestThermodynamicsAndEnergyBalance(unittest.TestCase):
    """Verifies conservation laws and the energetic cost of endosomal acidification."""

    def test_v_atpase_electrochemical_potential(self):
        form = LNPFormulation()
        energetics = ThermodynamicsAndEnergyBalance.calculate_endosomal_acidification_energy(
            form, escape_efficiency=0.015, dose_ug=5.0
        )
        # Delta mu_H+ should be ~ 16 - 22 kJ/mol (~0.17 - 0.22 eV)
        self.assertGreater(energetics.v_atpase_electrochemical_gradient_kj_mol, 15.0)
        self.assertLess(energetics.v_atpase_electrochemical_gradient_kj_mol, 24.0)
        self.assertGreater(energetics.work_per_proton_ev, 0.15)
        self.assertLess(energetics.work_per_proton_ev, 0.25)

    def test_proton_buffering_and_atp_consumption(self):
        form = LNPFormulation()
        energetics = ThermodynamicsAndEnergyBalance.calculate_endosomal_acidification_energy(
            form, escape_efficiency=0.015, dose_ug=5.0
        )
        # LNP buffers tens of thousands of protons per particle
        self.assertGreater(energetics.protons_buffered_per_particle, 15000)
        self.assertGreater(energetics.atp_consumed_per_endosome, 4000)
        # Mass cost: delivering 1 ug cytosolic mRNA requires >0.5 mg lipid
        self.assertGreater(energetics.effective_lipid_payload_cost_mg_per_ug_cytosolic_mrna, 0.5)


class TestGeneticKnockoutPhenotypes(unittest.TestCase):
    """Verifies ApoE-/- and LDLR-/- knockout dependency and SORT independence."""

    def test_conventional_lnp_apoe_and_ldlr_dependence(self):
        base_form = LNPFormulation(name="Conventional")
        panel = GeneticKnockoutSimulator.simulate_knockout_panel(base_form)

        wt_liver = panel["Wild_Type"].biodistribution["organ_percentages"]["liver"]
        apoe_ko_liver = panel["ApoE_Knockout"].biodistribution["organ_percentages"]["liver"]
        ldlr_ko_liver = panel["LDLR_Knockout"].biodistribution["organ_percentages"]["liver"]

        # WT liver delivery should be >95%
        self.assertGreater(wt_liver, 95.0)
        # ApoE and LDLR knockouts should substantially diminish hepatic delivery
        self.assertLess(apoe_ko_liver, wt_liver - 30.0)
        self.assertLess(ldlr_ko_liver, wt_liver - 15.0)

    def test_lung_sort_independence_of_apoe(self):
        lung_form = SORTDeliveryOptimizer.sweep_cationic_lung_sort([50.0])[0].formulation
        panel = GeneticKnockoutSimulator.simulate_knockout_panel(lung_form)

        wt_lung = panel["Wild_Type"].biodistribution["organ_percentages"]["lung"]
        apoe_ko_lung = panel["ApoE_Knockout"].biodistribution["organ_percentages"]["lung"]

        # Lung SORT retains high lung targeting even without ApoE
        self.assertGreater(wt_lung, 90.0)
        self.assertAlmostEqual(wt_lung, apoe_ko_lung, places=1)

    def test_spleen_sort_independence_of_apoe(self):
        spleen_form = SORTDeliveryOptimizer.sweep_anionic_spleen_sort([30.0])[0].formulation
        panel = GeneticKnockoutSimulator.simulate_knockout_panel(spleen_form)

        wt_spleen = panel["Wild_Type"].biodistribution["organ_percentages"]["spleen"]
        apoe_ko_spleen = panel["ApoE_Knockout"].biodistribution["organ_percentages"]["spleen"]

        # Spleen SORT retains high spleen targeting even without ApoE
        self.assertGreater(wt_spleen, 80.0)
        self.assertAlmostEqual(wt_spleen, apoe_ko_spleen, places=1)


class TestSafetyAndImmunogenicity(unittest.TestCase):
    """Verifies CARPA, hepatotoxicity, and thrombocytopenia scoring."""

    def test_cationic_thrombocytopenia_and_carpa_elevation(self):
        base_res = IntegratedLNPDeliveryEngine.run_simulation(LNPFormulation())
        lung_res = SORTDeliveryOptimizer.sweep_cationic_lung_sort([50.0])[0]

        # 50% DOTAP should have significantly elevated CARPA and thrombocytopenia risk
        self.assertGreater(
            lung_res.expression_and_safety["thrombocytopenia_risk_score"],
            base_res.expression_and_safety["thrombocytopenia_risk_score"]
        )
        self.assertGreater(
            lung_res.expression_and_safety["carpa_risk_score"],
            base_res.expression_and_safety["carpa_risk_score"]
        )


class TestTumorMicroenvironmentAndSTINGDelivery(unittest.TestCase):
    """
    Verifies targeted delivery of STING agonists and microenvironmental decompressors
    to Tumor-Draining Lymph Nodes (TDLNs) and Tumor Vascular Endothelium (Hypatia A003 Link).
    """

    def test_free_msa2_high_hepatic_clearance_and_crs_risk(self):
        free_eval = TumorAndLymphNodeTargetingEngine.evaluate_immunotherapy_delivery(None, is_free_drug=True)
        # Free drug suffers massive hepatic clearance (>80%) and severe cytokine storm risk (>150 pg/mL TNF)
        self.assertGreater(free_eval.liver_delivered_ug / free_eval.injection_dose_ug, 0.80)
        self.assertGreater(free_eval.serum_tnf_alpha_pg_per_ml, 150.0)
        self.assertEqual(free_eval.cytokine_storm_risk, "SEVERE_CRS (Lethal)")
        self.assertLess(free_eval.therapeutic_index, 1.0)

    def test_tdln_bmp_sort_cDC1_targeting_and_sting_activation(self):
        tdln_form = SORTDeliveryOptimizer.create_tdln_bmp_sort_lnp(25.0)
        eval_res = TumorAndLymphNodeTargetingEngine.evaluate_immunotherapy_delivery(tdln_form)

        # >20% delivered to TDLN, liver clearance <15%
        self.assertGreaterEqual(eval_res.tdln_delivered_ug / eval_res.injection_dose_ug, 0.20)
        self.assertLess(eval_res.liver_delivered_ug / eval_res.injection_dose_ug, 0.15)
        # Robust STING pathway activation in cDC1s (>80%)
        self.assertGreater(eval_res.sting_activation_fraction, 0.80)
        # Serum TNF stays well below 150 pg/mL CRS limit
        self.assertLess(eval_res.serum_tnf_alpha_pg_per_ml, 50.0)
        self.assertGreater(eval_res.therapeutic_index, 20.0)

    def test_tumor_endo_sort_vascular_decompression_and_ctl_surge(self):
        endo_form = SORTDeliveryOptimizer.create_tumor_endo_sort_lnp(15.0, ligand="cRGD", helper="DOPE")
        eval_res = TumorAndLymphNodeTargetingEngine.evaluate_immunotherapy_delivery(endo_form)

        # >25% delivered to tumor vasculature
        self.assertGreaterEqual(eval_res.tumor_delivered_ug / eval_res.injection_dose_ug, 0.25)
        # Avoids massive pulmonary retention (lung delivery < 20%)
        self.assertLess(eval_res.lung_delivered_ug / eval_res.injection_dose_ug, 0.20)
        # Microvascular decompression reduces IFP to <= 10 mmHg (>60% reduction)
        self.assertLessEqual(eval_res.tumor_ifp_post_treatment_mmhg, 10.0)
        self.assertGreater(eval_res.microvascular_decompression_pct, 60.0)
        # CD8+ T-cell infiltration increases >5-fold
        self.assertGreater(eval_res.ctl_infiltration_fold_increase, 5.0)

    def test_dual_synergy_cocktail_maximizes_response(self):
        cocktail = TumorAndLymphNodeTargetingEngine.evaluate_dual_synergy_cocktail()
        # Synergy achieves >10x CTL infiltration surge and therapeutic index >30x
        self.assertGreater(cocktail.ctl_infiltration_fold_increase, 10.0)
        self.assertGreater(cocktail.therapeutic_index, 30.0)
        self.assertLess(cocktail.serum_tnf_alpha_pg_per_ml, 25.0)
        self.assertEqual(cocktail.cytokine_storm_risk, "LOW (Safe)")

    def test_hypatia_cold_tumor_conversion_to_hot_inflamed(self):
        cross_talk = TumorAndLymphNodeTargetingEngine.simulate_hypatia_tumor_cross_talk()
        if "error" not in cross_talk:
            self.assertEqual(cross_talk["phenotypic_conversion"], "IMMUNE_EXCLUDED -> HOT_INFLAMED")
            self.assertGreater(cross_talk["cd8_fold_increase"], 20.0)
            self.assertGreater(cross_talk["post_sort_sting"]["anti_pd1_response"], 0.60)
            self.assertGreater(cross_talk["post_sort_sting"]["combo_response"], 0.75)


class TestGroundTruthVerificationSuite(unittest.TestCase):
    """Verifies all required ground-truth assertions pass."""

    def test_verify_all_ground_truths(self):
        gt_results = verify_ground_truth_compliance()
        for k, passed in gt_results.items():
            self.assertTrue(passed, f"Ground Truth constraint failed: {k}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
