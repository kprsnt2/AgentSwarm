"""
Unit Tests for Adult Mammalian Cardiac Regeneration & Cytokinesis Engine
========================================================================
Deterministic verification of cleavage furrow biophysics, Hippo-YAP signaling,
post-infarct functional regeneration, and electrophysiological safety.

Author: Swarm Research Agent
License: MIT
"""

import pytest
from cardiac_regeneration_cytokinesis_engine import (
    CardiomyocyteBiomechanics,
    HippoYAPSignalingModel,
    simulate_post_infarct_regeneration,
    assess_arrhythmogenic_and_oncogenic_safety,
)


def test_cleavage_force_sarcomere_stiffness_threshold():
    # Case 1: Mature adult cardiomyocyte with rigid myofibrillar apparatus (stiffness = 14.2 nN)
    stalled_res = CardiomyocyteBiomechanics.calculate_cleavage_force(
        furrow_radius_um=0.5,
        sarcomere_stiffness_nn=14.2,
    )
    assert stalled_res["net_force_nn"] < 0
    assert stalled_res["is_permissive"] is False

    # Case 2: De-tensioned cardiomyocyte (sarcomeric stiffness = 2.8 nN)
    permissive_res = CardiomyocyteBiomechanics.calculate_cleavage_force(
        furrow_radius_um=0.5,
        sarcomere_stiffness_nn=2.8,
    )
    assert permissive_res["net_force_nn"] > 5.0
    assert permissive_res["is_permissive"] is True


def test_cytokinesis_success_probability():
    # Baseline adult: high stiffness (14.2 nN), no LATS inhibition
    baseline = CardiomyocyteBiomechanics.calculate_cytokinesis_success_probability(
        sarcomeric_stiffness_nn=14.2,
        aurora_b_activity_ratio=1.0,
        lats1_2_inhibition_pct=0.0,
    )
    assert baseline["cytokinesis_success_pct"] < 20.0
    assert baseline["binucleation_rate_pct"] > 80.0
    assert "ABORTIVE_BINUCLEATION" in baseline["predominant_fate"]

    # Reprogrammed: de-tensioned (2.8 nN), 85% LATS inhibition, enhanced Aurora B (1.2)
    reprogrammed = CardiomyocyteBiomechanics.calculate_cytokinesis_success_probability(
        sarcomeric_stiffness_nn=2.8,
        aurora_b_activity_ratio=1.2,
        lats1_2_inhibition_pct=85.0,
    )
    assert reprogrammed["cytokinesis_success_pct"] > 75.0
    assert reprogrammed["predominant_fate"] == "COMPLETE_CYTOKINESIS_ABSCISSION"


def test_hippo_yap_signaling_kinetics():
    # Adult baseline (0% LATS inhibition)
    model_baseline = HippoYAPSignalingModel(lats_inhibition_factor=0.0)
    res_base = model_baseline.compute_steady_state()
    assert res_base["nuclear_yap_fraction"] < 0.15
    assert res_base["tead_transcriptional_activation"] < 0.20
    assert res_base["mitotic_gene_induction_fold"] < 2.5

    # Target inhibition (85% LATS inhibition) -> 3.5x nuclear YAP surge
    model_active = HippoYAPSignalingModel(lats_inhibition_factor=0.85)
    res_active = model_active.compute_steady_state()
    assert res_active["nuclear_yap_fraction"] > 0.25
    assert res_active["tead_transcriptional_activation"] > 0.50
    assert res_active["mitotic_gene_induction_fold"] > 5.0


def test_post_infarct_regeneration_simulation():
    # 1. Untreated Control
    sim_untreated = simulate_post_infarct_regeneration(
        initial_lvef_pct=32.0,
        infarct_scar_area_pct=28.0,
        treatment_applied=False,
        simulation_days=28,
    )
    assert sim_untreated["delta_lvef_pct"] <= 0.0
    assert sim_untreated["total_new_myocytes_generated_millions"] < 5.0

    # 2. Treated with T4CI Regimen
    sim_treated = simulate_post_infarct_regeneration(
        initial_lvef_pct=32.0,
        infarct_scar_area_pct=28.0,
        treatment_applied=True,
        simulation_days=28,
    )
    # LVEF should improve significantly (+10 to +20%)
    assert 10.0 <= sim_treated["delta_lvef_pct"] <= 20.0
    assert sim_treated["final_lvef_pct"] > 44.0
    # Generates hundreds of millions of new myocytes
    assert sim_treated["total_new_myocytes_generated_millions"] > 200.0
    # Scar area is reduced by myocyte regeneration
    assert sim_treated["final_scar_pct"] < 20.0


def test_safety_clearance_and_electrophysiology():
    safety = assess_arrhythmogenic_and_oncogenic_safety()
    assert safety["mrna_clearance_at_72h_pct"] > 95.0
    assert safety["oncogenic_transformation_risk"] == "NEGLIGIBLE_SELF_LIMITING_MRNA"
    assert safety["synchronous_calcium_transients_restored"] is True

    # Check electrophysiology normalization by day 21
    day21 = safety["electrophysiology_normalization"]["Day_21_Mature"]
    assert day21["resting_potential_mv"] <= -84.0
    assert 300.0 <= day21["apd90_ms"] <= 320.0
    assert day21["conduction_velocity_m_per_s"] >= 0.60
