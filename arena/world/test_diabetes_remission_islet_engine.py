"""
test_diabetes_remission_islet_engine.py

Comprehensive Pytest Suite for:
1. Type 2 Diabetes Remission Biophysics (Twin Cycle Model, PFT, DiRECT benchmarks)
2. Stem Cell Islet Microencapsulation & Transport (Krogh cylinder/sphere reaction-diffusion)
3. Planar Macroencapsulation Chambers (VX-264 device footprint, packing density, anoxic midplane)
4. Nutrient/Hormone Diffusion Lag & Foreign Body Response Evasion
5. Autoimmune Interception Kinetics (Teplizumab TrialNet TN-10 validation)
6. Cross-Modality Curative Frontier Synthesis

Author: Kepler (A001) - Autonomous Research Agent
Epistemic Class: Empirical
"""

import pytest
import numpy as np
from diabetes_remission_islet_engine import (
    TwinCycleParameters,
    TwinCycleModel,
    PersonalFatThreshold,
    IsletTransportParameters,
    IsletMicroencapsulationModel,
    MacroencapsulationDeviceModel,
    NutrientDiffusionLagModel,
    ForeignBodyResponseModel,
    TeplizumabInterceptionParameters,
    TeplizumabInterceptionModel,
    CurativeDiabetesFrontier,
)


# ==============================================================================
# SECTION 1: TYPE 2 DIABETES & TWIN CYCLE MODEL TESTS
# ==============================================================================

class TestTwinCycleModel:
    """Tests the biophysics of the Twin Cycle Hypothesis calibrated to DiRECT."""

    def test_rapid_hepatic_clearance_and_glucose_normalization(self):
        """
        DiRECT/Counterbalance ground truth: Intrahepatic TAG falls rapidly within
        7-10 days on negative energy balance, which directly normalizes hepatic
        glucose production and fasting plasma glucose.
        """
        engine = TwinCycleModel()
        traj = engine.simulate_dietary_remission(duration_days=140, daily_deficit_kcal=1200.0)

        # Baseline check
        assert traj.ihtg_pct[0] == pytest.approx(16.0, abs=0.1)
        assert traj.fpg_mmol[0] == pytest.approx(9.2, abs=0.1)

        # Day 7 check: rapid liver fat clearance below normal threshold (5.56%)
        assert traj.ihtg_pct[7] <= 5.56
        # FPG drops rapidly towards non-diabetic range (< 6.0 mmol/L)
        assert traj.fpg_mmol[7] < 6.0
        assert traj.fpg_mmol[7] < traj.fpg_mmol[0] - 3.0

    def test_delayed_pancreatic_steatosis_clearance(self):
        """
        Pancreatic fat clears at a much slower rate (half-life ~25 days) compared to
        liver fat (half-life ~3.15 days). Intrapancreatic fat takes 8-16 weeks to normalize.
        """
        engine = TwinCycleModel()
        traj = engine.simulate_dietary_remission(duration_days=140, daily_deficit_kcal=1200.0)

        # At Day 7, IPTG is still high (> 7.5%) while IHTG has already normalized
        assert traj.iptg_pct[7] > 7.5
        assert traj.iptg_pct[7] > engine.params.iptg_lipotox_thresh

        # At Day 140 (20 weeks), pancreatic fat has cleared below lipotoxic threshold
        assert traj.iptg_pct[-1] < engine.params.iptg_lipotox_thresh
        assert traj.iptg_pct[-1] < traj.iptg_pct[0] - 2.5

    def test_first_phase_insulin_recovery_timing(self):
        """
        First-phase insulin secretion (AIRg) does NOT recover immediately on day 7;
        it requires pancreatic fat to drop below the lipotoxic threshold (~5.8%).
        Recovery occurs progressively between weeks 8 and 20.
        """
        engine = TwinCycleModel()
        traj = engine.simulate_dietary_remission(duration_days=140, daily_deficit_kcal=1200.0)

        # At day 7 and day 28, AIRg is still near baseline (< 0.05 nmol/L)
        assert traj.airg_nmol[7] < 0.06
        assert traj.airg_nmol[28] < 0.06

        # By day 140, AIRg is robustly restored (> 0.30 nmol/L)
        assert traj.airg_nmol[-1] > 0.30
        assert traj.airg_nmol[-1] > traj.airg_nmol[0] * 5.0

    def test_remission_criteria_success(self):
        """
        DiRECT remission criteria: HbA1c < 6.5%, FPG < 7.0 mmol/L, AIRg > 0.20 nmol/L.
        """
        engine = TwinCycleModel()
        traj = engine.simulate_dietary_remission(duration_days=140, daily_deficit_kcal=1200.0)

        assert traj.remission_achieved is True
        assert traj.fpg_mmol[-1] < 7.0
        assert traj.hba1c_est_pct[-1] < 6.5
        assert traj.airg_nmol[-1] > 0.20
        # Weight loss should be in the 15-22 kg range for 20 weeks of 1200 kcal/day deficit
        weight_loss = traj.weight_kg[0] - traj.weight_kg[-1]
        assert 15.0 <= weight_loss <= 23.0

    def test_diabetes_duration_attenuation(self):
        """
        Taylor et al. (DiRECT/Counterbalance): Patients with longer disease duration (>10 years)
        suffer irreversible beta-cell apoptosis, capping the recoverable AIRg.
        """
        p_short = TwinCycleParameters(disease_duration_years=1.0)
        p_long = TwinCycleParameters(disease_duration_years=12.0)

        engine_short = TwinCycleModel(p_short)
        engine_long = TwinCycleModel(p_long)

        traj_short = engine_short.simulate_dietary_remission(duration_days=140)
        traj_long = engine_long.simulate_dietary_remission(duration_days=140)

        assert traj_short.airg_nmol[-1] > traj_long.airg_nmol[-1] * 2.0

    def test_weight_regain_relapse_reverse_route(self):
        """
        Al-Mrabeh et al. (Lancet Diabetes Endocrinol 2020):
        Weight regain drives ectopic fat accumulation back into liver and pancreas,
        re-inducing beta-cell dedifferentiation and clinical T2D relapse.
        """
        engine = TwinCycleModel()
        traj = engine.simulate_dietary_remission(duration_days=140)
        assert traj.remission_achieved is True

        relapse = engine.simulate_weight_regain_relapse(traj, regain_duration_days=365, daily_surplus_kcal=350.0)

        assert relapse["relapsed"] is True
        assert relapse["weight_kg"][-1] > traj.weight_kg[-1] + 10.0
        assert relapse["ihtg_pct"][-1] > engine.params.ihtg_norm_thresh
        assert relapse["iptg_pct"][-1] > engine.params.iptg_lipotox_thresh
        assert relapse["fpg_mmol"][-1] >= 7.0
        assert relapse["airg_nmol"][-1] < 0.10


# ==============================================================================
# SECTION 2: PERSONAL FAT THRESHOLD TESTS
# ==============================================================================

class TestPersonalFatThreshold:
    """Tests the Personal Fat Threshold (PFT) model (Taylor & Holman 2015, ReTUNE 2021)."""

    def test_ectopic_overflow_in_normal_bmi(self):
        """
        ReTUNE study benchmark: A patient with normal BMI (24.0 kg/m^2) can develop T2D
        if their personal SAT capacity is low (e.g. 21.0 kg/m^2).
        """
        res = PersonalFatThreshold.calculate_ectopic_overflow(
            bmi=24.0,
            personal_sat_capacity_bmi=21.0,
            body_fat_pct=26.0
        )
        assert res["in_ectopic_overflow"] is True
        assert res["estimated_ihtg_pct"] > 10.0  # Pathological hepatic steatosis
        assert res["estimated_iptg_pct"] > 7.0   # Pathological pancreatic steatosis

    def test_sub_threshold_safe_adiposity(self):
        """
        When BMI is below personal SAT threshold, ectopic spillover is minimal.
        """
        res = PersonalFatThreshold.calculate_ectopic_overflow(
            bmi=21.0,
            personal_sat_capacity_bmi=23.0,
            body_fat_pct=18.0
        )
        assert res["in_ectopic_overflow"] is False
        assert res["estimated_ihtg_pct"] < 5.56  # Normal liver fat

    def test_direct_stratified_remission_probabilities(self):
        """
        DiRECT trial published remission rates:
        < 5 kg: ~7-9%
        5 - 10 kg: ~34%
        10 - 15 kg: ~57%
        >= 15 kg: ~86%
        """
        p_3kg = PersonalFatThreshold.direct_remission_probability(weight_loss_kg=3.0, diabetes_duration_years=3.0)
        p_7_5kg = PersonalFatThreshold.direct_remission_probability(weight_loss_kg=7.5, diabetes_duration_years=3.0)
        p_12_5kg = PersonalFatThreshold.direct_remission_probability(weight_loss_kg=12.5, diabetes_duration_years=3.0)
        p_17_5kg = PersonalFatThreshold.direct_remission_probability(weight_loss_kg=17.5, diabetes_duration_years=3.0)

        # Monotonicity with weight loss
        assert p_3kg < p_7_5kg < p_12_5kg < p_17_5kg

        # Quantitative accuracy against DiRECT published rates
        assert 0.05 <= p_3kg <= 0.15
        assert 0.20 <= p_7_5kg <= 0.40
        assert 0.45 <= p_12_5kg <= 0.65
        assert 0.75 <= p_17_5kg <= 0.95


# ==============================================================================
# SECTION 3: ISLET MICROENCAPSULATION TRANSPORT TESTS
# ==============================================================================

class TestIsletMicroencapsulationModel:
    """Tests reaction-diffusion oxygen transport in single microencapsulated islets."""

    def test_microcapsule_baseline_transport(self):
        """
        A 150 um diameter islet in a 250 um radius alginate capsule in subcutaneous bed
        (pO2 = 35 mmHg) maintains > 90% viable fraction without fibrosis.
        """
        model = IsletMicroencapsulationModel()
        res = model.solve_oxygen_profile_analytical(
            capsule_radius_um=250.0,
            fibrotic_thickness_um=0.0,
            host_tissue_po2_mmhg=35.0
        )
        assert res["viable_fraction"] > 0.90
        assert res["islet_surface_po2_mmhg"] > 12.0
        assert res["delta_p_alginate_mmhg"] > 0.0
        assert res["delta_p_fibrosis_mmhg"] == 0.0

    def test_fibrotic_strangulation_gradient(self):
        """
        Pericapsular fibrotic scar imposes severe diffusion resistance, driving
        expansion of the anoxic core and collapsing viable fraction.
        """
        model = IsletMicroencapsulationModel()
        clean = model.solve_oxygen_profile_analytical(capsule_radius_um=250.0, fibrotic_thickness_um=0.0, host_tissue_po2_mmhg=35.0)
        moderate_scar = model.solve_oxygen_profile_analytical(capsule_radius_um=250.0, fibrotic_thickness_um=30.0, host_tissue_po2_mmhg=35.0)
        heavy_scar = model.solve_oxygen_profile_analytical(capsule_radius_um=250.0, fibrotic_thickness_um=70.0, host_tissue_po2_mmhg=35.0)

        # Surface pO2 decreases monotonically with scar thickness
        assert clean["islet_surface_po2_mmhg"] > moderate_scar["islet_surface_po2_mmhg"] > heavy_scar["islet_surface_po2_mmhg"]
        # Anoxic core radius expands monotonically
        assert clean["anoxic_core_radius_um"] < moderate_scar["anoxic_core_radius_um"] < heavy_scar["anoxic_core_radius_um"]
        # Viable fraction decreases monotonically
        assert clean["viable_fraction"] >= moderate_scar["viable_fraction"] > heavy_scar["viable_fraction"]
        # GSIS competent fraction drops severely
        assert clean["gsis_competent_fraction"] > heavy_scar["gsis_competent_fraction"]

    def test_hyperoxic_environment_eliminates_anoxia(self):
        """
        When external pO2 is sufficiently high (e.g. 70 mmHg), the islet core
        remains fully oxygenated above 0 mmHg and viable fraction is 100%.
        """
        model = IsletMicroencapsulationModel()
        res = model.solve_oxygen_profile_analytical(
            capsule_radius_um=250.0,
            fibrotic_thickness_um=0.0,
            host_tissue_po2_mmhg=70.0
        )
        assert res["viable_fraction"] == pytest.approx(1.0, abs=1e-5)
        assert res["anoxic_core_radius_um"] == pytest.approx(0.0, abs=1e-5)
        assert res["core_po2_mmhg"] > 15.0
        assert res["gsis_competent_fraction"] > 0.90


# ==============================================================================
# SECTION 4: PLANAR MACROENCAPSULATION DEVICE TESTS
# ==============================================================================

class TestMacroencapsulationDeviceModel:
    """Tests 1D reaction-diffusion transport in planar macroencapsulation devices (e.g. VX-264)."""

    def test_planar_oxygenation_density_scaling(self):
        """
        As islet packing density phi increases, oxygen consumption per unit chamber volume
        increases proportionally, driving midplane pO2 downward.
        """
        model = MacroencapsulationDeviceModel()
        low_density = model.compute_planar_oxygenation(
            chamber_half_thickness_um=125.0,
            membrane_thickness_um=25.0,
            fibrotic_capsule_um=30.0,
            islet_volume_fraction=0.02,
            host_tissue_po2_mmhg=35.0
        )
        med_density = model.compute_planar_oxygenation(
            chamber_half_thickness_um=125.0,
            membrane_thickness_um=25.0,
            fibrotic_capsule_um=30.0,
            islet_volume_fraction=0.05,
            host_tissue_po2_mmhg=35.0
        )
        high_density = model.compute_planar_oxygenation(
            chamber_half_thickness_um=125.0,
            membrane_thickness_um=25.0,
            fibrotic_capsule_um=30.0,
            islet_volume_fraction=0.12,
            host_tissue_po2_mmhg=35.0
        )

        assert low_density["midplane_po2_mmhg"] > med_density["midplane_po2_mmhg"] > high_density["midplane_po2_mmhg"]
        assert low_density["is_midplane_anoxic"] is False
        assert high_density["is_midplane_anoxic"] is True
        assert high_density["viable_fraction"] < 1.0

    def test_human_therapeutic_footprint_scaling(self):
        """
        A human dose of 500,000 IEQ requires large device area at low packing densities.
        At phi=0.05 and 2L=250 um, footprint is ~707 cm^2.
        """
        model = MacroencapsulationDeviceModel()
        res = model.compute_planar_oxygenation(
            chamber_half_thickness_um=125.0,
            membrane_thickness_um=25.0,
            fibrotic_capsule_um=30.0,
            islet_volume_fraction=0.05
        )
        assert res["human_dose_area_cm2"] == pytest.approx(706.9, rel=0.02)

    def test_max_allowable_packing_density_solver(self):
        """
        Solver finds maximum packing density to maintain midplane pO2 >= 15 mmHg.
        """
        model = MacroencapsulationDeviceModel()
        max_phi = model.solve_max_packing_density(
            chamber_half_thickness_um=125.0,
            membrane_thickness_um=25.0,
            fibrotic_capsule_um=30.0,
            target_min_po2_mmhg=15.0,
            host_tissue_po2_mmhg=35.0
        )
        assert 0.04 < max_phi < 0.06

        # Check that midplane pO2 at max_phi is indeed ~15 mmHg
        check = model.compute_planar_oxygenation(
            chamber_half_thickness_um=125.0,
            membrane_thickness_um=25.0,
            fibrotic_capsule_um=30.0,
            islet_volume_fraction=max_phi,
            host_tissue_po2_mmhg=35.0
        )
        assert check["midplane_po2_mmhg"] == pytest.approx(15.0, abs=0.1)


# ==============================================================================
# SECTION 5: NUTRIENT LAG & FOREIGN BODY RESPONSE TESTS
# ==============================================================================

class TestNutrientLagAndFBR:
    """Tests nutrient/insulin transport delays and foreign body evasion dynamics."""

    def test_diffusion_lag_kinetics(self):
        """
        Diffusion time tau = L^2 / (2D). For 250 um distance:
        Glucose lag ~2 min, Insulin lag ~6.5 min.
        """
        res = NutrientDiffusionLagModel.calculate_lag_times(capsule_diffusion_dist_um=250.0)
        assert 1.5 < res["glucose_lag_min"] < 3.0
        assert 5.0 < res["insulin_lag_min"] < 8.0
        assert 6.5 < res["total_biphasic_delay_min"] < 11.0

    def test_foreign_body_size_evasion(self):
        """
        Vegas et al. (Nat Biotechnol 2016): Spheres with R >= 750 um (1.5 mm diameter)
        reduce fibrotic overgrowth by > 90% compared to standard small microcapsules.
        """
        t, thick_small = ForeignBodyResponseModel.fibrotic_thickness_trajectory(capsule_radius_um=250.0, is_triazole_modified=False)
        t, thick_large = ForeignBodyResponseModel.fibrotic_thickness_trajectory(capsule_radius_um=750.0, is_triazole_modified=False)

        assert thick_large[-1] < thick_small[-1] * 0.15

    def test_triazole_chemical_modification_effect(self):
        """
        Triazole (TMTD/Z1-Y15) modification attenuates fibrosis by ~95%.
        """
        t, thick_unmod = ForeignBodyResponseModel.fibrotic_thickness_trajectory(capsule_radius_um=250.0, is_triazole_modified=False)
        t, thick_mod = ForeignBodyResponseModel.fibrotic_thickness_trajectory(capsule_radius_um=250.0, is_triazole_modified=True)

        assert thick_mod[-1] < thick_unmod[-1] * 0.10


# ==============================================================================
# SECTION 6: AUTOIMMUNE INTERCEPTION (TEPLIZUMAB) TESTS
# ==============================================================================

class TestTeplizumabInterceptionModel:
    """Tests anti-CD3 interception dynamics calibrated to TrialNet TN-10."""

    def test_untreated_stage2_progression_time(self):
        """
        In TrialNet TN-10, untreated Stage 2 patients reached Stage 3 clinical diabetes
        at a median of ~24.4 months.
        """
        engine = TeplizumabInterceptionModel()
        sim = engine.simulate_interception(teplizumab_treated=False)
        assert 22.0 <= sim["stage3_onset_months"] <= 27.0

    def test_teplizumab_delay_magnitude(self):
        """
        Teplizumab delays Stage 3 diagnosis by a median of 2.0 to 3.5 years (24 to 40+ months).
        """
        engine = TeplizumabInterceptionModel()
        delays = engine.calculate_trialnet_median_delay()

        assert delays["delay_months"] > 24.0
        assert delays["delay_years"] >= 2.0
        assert delays["teplizumab_onset_months"] > delays["placebo_onset_months"] + 24.0

    def test_c_peptide_preservation(self):
        """
        Teplizumab preserves residual C-peptide secretion during the 3-year active window.
        """
        engine = TeplizumabInterceptionModel()
        untreated = engine.simulate_interception(simulation_years=3.0, teplizumab_treated=False)
        treated = engine.simulate_interception(simulation_years=3.0, teplizumab_treated=True)

        assert treated["final_c_peptide_auc"] > untreated["final_c_peptide_auc"] * 2.0


# ==============================================================================
# SECTION 7: COMPARATIVE FRONTIER SYNTHESIS TESTS
# ==============================================================================

class TestCurativeDiabetesFrontier:
    """Tests the comprehensive 4-modality comparative synthesis."""

    def test_frontier_completeness_and_structure(self):
        modalities = CurativeDiabetesFrontier.compare_modalities()
        assert len(modalities) == 4

        names = [m["modality"] for m in modalities]
        assert any("DiRECT" in n for n in names)
        assert any("Teplizumab" in n for n in names)
        assert any("VX-880" in n for n in names)
        assert any("VX-264" in n for n in names)

        for m in modalities:
            assert "target_population" in m
            assert "biological_mechanism" in m
            assert "durability_years" in m
            assert "insulin_independence_rate_pct" in m
            assert "primary_biophysical_bottleneck" in m
            assert "immunosuppression_required" in m
