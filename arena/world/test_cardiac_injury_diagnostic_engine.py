"""
Test Suite for Cardiac Injury Diagnostic Simulation Engine
==========================================================
Deterministic verification of qPCR efficiency, dPCR Poisson quantification,
cfDNA methylation deconvolution, snRNA-seq cardiac cell atlas, and multi-omic scoring.

Author: Swarm Research Agent
License: MIT
"""

import pytest
import math
from cardiac_injury_diagnostic_engine import (
    calculate_pcr_efficiency,
    delta_delta_ct,
    assess_hemolysis_risk,
    digital_pcr_poisson,
    taqman_multiplex_panel_spec,
    CardiomyocyteMethylationDeconvolver,
    CardiacCellTypeAtlas,
    calculate_cardiac_injury_score,
    compute_roc_metrics,
    simulate_hipsc_hypoxia_reoxygenation_kinetics,
)


# ==============================================================================
# 1. qPCR & dPCR TESTS
# ==============================================================================

def test_pcr_efficiency_calculation():
    # Ideal slope -3.3219 gives ~100% efficiency (E = 1.0)
    eff_ideal = calculate_pcr_efficiency(-3.3219)
    assert pytest.approx(eff_ideal, abs=0.01) == 1.0

    # Slope -3.10 gives ~1.10 (110%)
    eff_high = calculate_pcr_efficiency(-3.10)
    assert 1.08 <= eff_high <= 1.12

    # Slope -3.58 gives ~0.90 (90%)
    eff_low = calculate_pcr_efficiency(-3.58)
    assert 0.88 <= eff_low <= 0.92

    # Positive slope must raise ValueError
    with pytest.raises(ValueError):
        calculate_pcr_efficiency(0.5)


def test_delta_delta_ct_livak_and_pfaffl():
    # When delta Ct is identical, fold change must be 1.0
    res_equal = delta_delta_ct(
        target_sample_ct=24.0,
        ref_sample_ct=20.0,
        target_control_ct=24.0,
        ref_control_ct=20.0,
    )
    assert res_equal["ddct"] == 0.0
    assert res_equal["fold_change_livak"] == 1.0
    assert res_equal["fold_change_pfaffl"] == 1.0

    # 2 cycles earlier target in sample -> 4-fold upregulation
    res_up = delta_delta_ct(
        target_sample_ct=22.0,
        ref_sample_ct=20.0,
        target_control_ct=24.0,
        ref_control_ct=20.0,
    )
    assert res_up["ddct"] == -2.0
    assert pytest.approx(res_up["fold_change_livak"], abs=0.001) == 4.0
    assert pytest.approx(res_up["log2_fold_change"], abs=0.001) == 2.0

    # Pfaffl model with customized efficiency
    res_pfaffl = delta_delta_ct(
        target_sample_ct=22.0,
        ref_sample_ct=20.0,
        target_control_ct=24.0,
        ref_control_ct=20.0,
        target_efficiency=0.95,
        ref_efficiency=0.98,
    )
    assert res_pfaffl["fold_change_pfaffl"] > 3.5


def test_hemolysis_risk_assessment():
    # Clean plasma (Delta Ct < 5.0)
    res_clean = assess_hemolysis_risk(mir23a_ct=22.0, mir451a_ct=18.5)
    assert res_clean["status"] == "PASSED_NON_HEMOLYZED"
    assert res_clean["is_usable"] is True
    assert res_clean["delta_ct"] == 3.5

    # Borderline plasma (Delta Ct = 6.2)
    res_borderline = assess_hemolysis_risk(mir23a_ct=25.0, mir451a_ct=18.8)
    assert res_borderline["status"] == "BORDERLINE_MILD_HEMOLYSIS"
    assert res_borderline["is_usable"] is True

    # Severe hemolysis (Delta Ct > 7.0) -> Must be rejected
    res_severe = assess_hemolysis_risk(mir23a_ct=28.0, mir451a_ct=19.0)
    assert res_severe["status"] == "REJECTED_SEVERE_HEMOLYSIS"
    assert res_severe["is_usable"] is False
    assert res_severe["severity"] == "CONTAMINATED"


def test_digital_pcr_poisson():
    # 0 positive partitions -> 0 concentration
    res_zero = digital_pcr_poisson(positive_partitions=0, total_partitions=20000)
    assert res_zero["concentration_copies_per_ul"] == 0.0

    # 10,000 / 20,000 positive partitions (50% positive)
    # lambda = -ln(1 - 0.5) = ln(2) ~ 0.69315
    res_half = digital_pcr_poisson(positive_partitions=10000, total_partitions=20000, droplet_volume_nl=0.85)
    expected_lambda = math.log(2.0)
    assert pytest.approx(res_half["lambda_per_partition"], abs=0.001) == expected_lambda
    # concentration = (0.69315 / 0.85) * 1000 ~ 815.47 copies/uL
    assert 810.0 <= res_half["concentration_copies_per_ul"] <= 820.0
    assert res_half["ci_lower_copies_per_ul"] < res_half["concentration_copies_per_ul"] < res_half["ci_upper_copies_per_ul"]

    # Exception checks
    with pytest.raises(ValueError):
        digital_pcr_poisson(positive_partitions=25000, total_partitions=20000)
    with pytest.raises(ValueError):
        digital_pcr_poisson(positive_partitions=-5, total_partitions=20000)


def test_taqman_multiplex_panel_spec():
    spec = taqman_multiplex_panel_spec()
    assert "miR-208a-3p" in spec
    assert "miR-499a-5p" in spec
    assert "miR-1-3p" in spec
    assert "cel-miR-39-3p" in spec
    assert "miR-451a" in spec

    # Verify dye spectral orthogonality
    dyes = [v["dye"].split()[0] for v in spec.values()]
    assert len(dyes) == len(set(dyes)), "Fluorophore reporter dyes must be spectrally distinct"

    # All amplicon lengths must be < 85 bp for optimal degradation-resistant circulating detection
    for k, v in spec.items():
        assert v["amplicon_length_bp"] < 85
        assert 58.0 <= v["primer_tm_celsius"] <= 62.0
        assert 67.0 <= v["probe_tm_celsius"] <= 71.0


# ==============================================================================
# 2. cfDNA METHYLATION DECONVOLUTION TESTS
# ==============================================================================

def test_cfdna_methylation_deconvolution():
    deconvolver = CardiomyocyteMethylationDeconvolver()

    # Case 1: Healthy Baseline Plasma (mostly WBC background, hypermethylated at cardiac loci)
    healthy_plasma = {
        "MYH6_CpG_island_1": 0.95,
        "TNNT2_promoter_CpG": 0.97,
        "MYL2_intron1_CpG": 0.94,
        "NKX2_5_enhancer_CpG": 0.96,
        "ACTC1_exon1_CpG": 0.93,
    }
    res_healthy = deconvolver.deconvolve_plasma_cfdna(healthy_plasma, total_cfdna_ng_per_ml=10.0)
    assert res_healthy["cardiomyocyte_pct"] < 1.0
    assert res_healthy["cardiac_genome_equivalents_per_ml"] < 25.0
    assert res_healthy["clinical_status"] == "PHYSIOLOGICAL_BASELINE"

    # Case 2: Acute Myocardial Infarction Plasma (marked unmethylated cardiac spillover)
    infarct_plasma = {
        "MYH6_CpG_island_1": 0.78,
        "TNNT2_promoter_CpG": 0.79,
        "MYL2_intron1_CpG": 0.77,
        "NKX2_5_enhancer_CpG": 0.79,
        "ACTC1_exon1_CpG": 0.76,
    }
    res_mi = deconvolver.deconvolve_plasma_cfdna(infarct_plasma, total_cfdna_ng_per_ml=25.0)
    assert res_mi["cardiomyocyte_pct"] > 10.0
    assert res_mi["cardiac_genome_equivalents_per_ml"] > 800.0
    assert res_mi["clinical_status"] == "EXTENSIVE_ACUTE_MYOCARDIAL_INFARCTION"

    # Missing locus raises ValueError
    with pytest.raises(ValueError):
        deconvolver.deconvolve_plasma_cfdna({"MYH6_CpG_island_1": 0.8})


# ==============================================================================
# 3. SINGLE-CELL / SINGLE-NUCLEUS RNA-seq CLASSIFIER TESTS
# ==============================================================================

def test_cardiac_cell_type_atlas_classification():
    # Profile 1: Cardiomyocyte
    cm_profile = {
        "TNNT2": 9.5,
        "MYH6": 7.8,
        "MYH7": 5.2,
        "ACTC1": 8.9,
        "TNNI3": 8.5,
        "DCN": 0.2,
        "PECAM1": 0.1,
    }
    res_cm = CardiacCellTypeAtlas.classify_cell_profile(cm_profile)
    assert res_cm["predicted_cell_type"] == "Cardiomyocyte"
    assert res_cm["confidence_score"] > 0.40

    # Profile 2: Activated Myofibroblast
    myofib_profile = {
        "POSTN": 9.2,
        "COL1A1": 8.8,
        "COL3A1": 8.1,
        "FAP": 6.5,
        "ACTA2": 7.4,
        "TNNT2": 0.0,
        "CD68": 0.1,
    }
    res_myo = CardiacCellTypeAtlas.classify_cell_profile(myofib_profile)
    assert res_myo["predicted_cell_type"] == "Myofibroblast_Activated"

    # Profile 3: Inflammatory M1 Macrophage
    m1_profile = {
        "CCR2": 7.8,
        "IL1B": 8.4,
        "TNF": 6.9,
        "S100A8": 9.1,
        "TNNT2": 0.0,
    }
    res_m1 = CardiacCellTypeAtlas.classify_cell_profile(m1_profile)
    assert res_m1["predicted_cell_type"] == "Macrophage_Inflammatory_M1"


def test_ischemic_remodeling_scoring():
    # Healthy resting cardiomyocyte
    healthy_cm = {
        "CPT1B": 6.5,
        "PPARA": 5.2,
        "SLC2A1": 0.4,
        "LDHA": 0.8,
        "HIF1A": 0.3,
        "MYH6": 7.8,
        "MYH7": 1.2,
        "NPPA": 0.2,
        "NPPB": 0.1,
        "DCN": 5.0,
        "POSTN": 0.1,
        "COL1A1": 0.4,
        "MRC1": 4.5,
        "LYVE1": 3.8,
        "CCR2": 0.2,
        "IL1B": 0.1,
    }
    score_healthy = CardiacCellTypeAtlas.score_ischemic_remodeling(healthy_cm)
    assert score_healthy["metabolic_hypoxia_shift_score"] < 0.5
    assert score_healthy["fetal_gene_reprogramming_ratio"] < 0.5
    assert score_healthy["myofibroblast_activation_index"] < 0.2
    assert score_healthy["composite_transcriptomic_injury_score"] < 1.0

    # Severe acute post-MI border zone profile
    infarct_border = {
        "CPT1B": 0.5,
        "PPARA": 0.3,
        "SLC2A1": 6.8,
        "LDHA": 8.2,
        "HIF1A": 7.4,
        "MYH6": 1.1,
        "MYH7": 8.5,
        "NPPA": 7.9,
        "NPPB": 8.1,
        "DCN": 1.0,
        "POSTN": 8.9,
        "COL1A1": 9.4,
        "MRC1": 1.0,
        "LYVE1": 0.8,
        "CCR2": 8.5,
        "IL1B": 7.9,
    }
    score_infarct = CardiacCellTypeAtlas.score_ischemic_remodeling(infarct_border)
    assert score_infarct["metabolic_hypoxia_shift_score"] > 5.0
    assert score_infarct["fetal_gene_reprogramming_ratio"] > 5.0
    assert score_infarct["myofibroblast_activation_index"] > 5.0
    assert score_infarct["composite_transcriptomic_injury_score"] > 5.0


# ==============================================================================
# 4. MULTI-OMIC SCORE & ROC PERFORMANCE TESTS
# ==============================================================================

def test_cardiac_injury_score_calculation():
    # Healthy baseline patient
    res_normal = calculate_cardiac_injury_score(
        mir208a_fold_change=1.1,
        mir499_fold_change=1.0,
        cardiac_cfdna_ge_per_ml=12.0,
        troponin_hs_ctni_pg_per_ml=4.2,
    )
    assert res_normal["cardiac_injury_score"] < 15.0
    assert res_normal["diagnosis"] == "NORMAL_UNINJURED"
    assert res_normal["risk_level"] == "LOW"

    # Acute Transmural Myocardial Infarction patient
    res_ami = calculate_cardiac_injury_score(
        mir208a_fold_change=45.0,
        mir499_fold_change=38.0,
        cardiac_cfdna_ge_per_ml=620.0,
        troponin_hs_ctni_pg_per_ml=1450.0,
    )
    assert res_ami["cardiac_injury_score"] > 70.0
    assert res_ami["diagnosis"] == "ACUTE_TRANSMURAL_MYOCARDIAL_INFARCTION"
    assert res_ami["risk_level"] == "CRITICAL"


def test_roc_metrics_computation():
    labels = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
    # Predict high scores for first 5, low for last 5
    scores = [85.0, 72.0, 68.0, 55.0, 42.0, 12.0, 8.0, 14.0, 22.0, 19.0]

    roc = compute_roc_metrics(labels, scores, threshold=35.0)
    assert roc["sensitivity"] == 1.0
    assert roc["specificity"] == 1.0
    assert roc["accuracy"] == 1.0
    assert roc["youden_index"] == 1.0
    assert roc["true_positives"] == 5
    assert roc["true_negatives"] == 5

    # Length mismatch raises ValueError
    with pytest.raises(ValueError):
        compute_roc_metrics([1, 0], [50.0])


# ==============================================================================
# 5. IN-VITRO KINETICS TIME-COURSE TESTS
# ==============================================================================

def test_hipsc_hypoxia_reoxygenation_kinetics():
    kinetics = simulate_hipsc_hypoxia_reoxygenation_kinetics()
    assert len(kinetics["time_points_hours"]) == 9
    assert kinetics["early_window_mir208_advantage_hours"] > 1.0

    # At t=1.0 hour hypoxia, miR-208a has started leaking while troponin is still near baseline
    t1_idx = kinetics["time_points_hours"].index(1.0)
    mir_t1 = kinetics["mir208a_fold_release"][t1_idx]
    ctni_t1 = kinetics["ctni_fold_release"][t1_idx]
    assert mir_t1 > 4.0
    assert ctni_t1 < 1.5, "Troponin macromolecule should not leak significantly at 1 hour hypoxia"
