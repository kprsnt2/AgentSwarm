"""
Test Suite for Cardiac Myofibroblast Mechanical Memory & Fibrotic Hysteresis Engine
===================================================================================
Author: Swarm Research Agent (Cardiovascular Mechanobiology Frontier)
"""

import pytest
from cardiac_fibrosis_hysteresis_engine import (
    FocalAdhesionMechanosensing,
    LINCComplexNuclearMechanics,
    NucleocytoplasmicTransportAndEpigenetics,
    BistableFibroticHysteresisModel,
    evaluate_scar_integrity_and_reversion,
)


def test_focal_adhesion_mechanosensing():
    # 1. Stiff border zone ECM (E = 35 kPa)
    stiff_res = FocalAdhesionMechanosensing.compute_traction_force(35.0)
    assert stiff_res["matrix_stiffness_kpa"] == 35.0
    assert stiff_res["clutch_force_pn"] > 25.0
    assert stiff_res["is_talin_unfolded"] is True
    assert stiff_res["vbs_exposed_ratio"] > 0.50

    # 2. Soft normal myocardium (E = 6.0 kPa)
    soft_res = FocalAdhesionMechanosensing.compute_traction_force(6.0)
    assert soft_res["matrix_stiffness_kpa"] == 6.0
    assert soft_res["clutch_force_pn"] < 10.0
    assert soft_res["is_talin_unfolded"] is False
    assert soft_res["vbs_exposed_ratio"] == 0.0


def test_linc_complex_nuclear_mechanics():
    # Intact LINC (eta = 1.0) under high tension
    intact = LINCComplexNuclearMechanics.compute_nuclear_state(
        clutch_force_pn=34.0, alpha_sma_level=0.90, linc_coupling_efficiency=1.0
    )
    assert intact["nuclear_tension_nn_per_um"] > 10.0
    assert intact["pore_dilation_nm"] > 1.80
    assert intact["pore_effective_radius_nm"] > 6.40

    # Uncoupled LINC (eta = 0.20)
    uncoupled = LINCComplexNuclearMechanics.compute_nuclear_state(
        clutch_force_pn=34.0, alpha_sma_level=0.90, linc_coupling_efficiency=0.20
    )
    assert uncoupled["nuclear_tension_nn_per_um"] < 3.50
    assert uncoupled["pore_dilation_nm"] < 0.50
    assert uncoupled["pore_effective_radius_nm"] < 5.10


def test_nucleocytoplasmic_transport_and_epigenetics():
    # Dilated pore state (r = 6.80 nm)
    dilated = NucleocytoplasmicTransportAndEpigenetics.compute_steady_state_import(6.80, chromatin_accessibility_init=0.85)
    assert dilated["nuclear_mrtfa_fraction"] > 0.60
    assert dilated["nuclear_yap_fraction"] > 0.65
    assert dilated["chromatin_accessibility"] > 0.60
    assert dilated["h3k27ac_promoter_permissiveness"] > 60.0

    # Constricted pore state (r = 4.70 nm)
    constricted = NucleocytoplasmicTransportAndEpigenetics.compute_steady_state_import(4.70, chromatin_accessibility_init=0.10)
    assert constricted["nuclear_mrtfa_fraction"] < 0.30
    assert constricted["nuclear_yap_fraction"] < 0.50
    assert constricted["chromatin_accessibility"] < 0.20


def test_bistable_hysteresis_loop():
    # In wild-type conditions (eta=1.0, LOXL2=0), test presence of hysteresis
    scan = BistableFibroticHysteresisModel.scan_hysteresis_loop(
        stiffness_range_kpa=(2.0, 45.0), num_points=30, linc_efficiency=1.0, loxl2_inhibition_pct=0.0
    )
    assert scan["is_bistable"] is True
    assert scan["e_activation_threshold_kpa"] >= 28.0
    assert scan["e_deactivation_threshold_kpa"] <= 24.0
    assert scan["hysteresis_gap_kpa"] >= 6.0

    # Fibroblasts at 35 kPa remain locked in myofibroblast state once activated
    locked_state = BistableFibroticHysteresisModel.solve_steady_state(
        35.0, initial_state=0.92, linc_efficiency=1.0, loxl2_inhibition_pct=0.0
    )
    assert locked_state > 0.80


def test_therapeutic_hysteresis_collapse_and_scar_safety():
    # Test dual-targeted therapy: transient LINC uncoupling (eta=0.22) + LOXL2 crosslink cleavage (38.5%)
    res = evaluate_scar_integrity_and_reversion(
        pre_treatment_stiffness_kpa=35.0,
        linc_uncoupling_efficiency=0.22,
        loxl2_inhibition_pct=38.5,
        treatment_duration_days=4,
    )
    # Verification of myofibroblast reversion
    assert res["reversion_successful"] is True
    assert res["treated_myofibroblast_state"] < 0.15
    assert res["post_washout_myofibroblast_state"] < 0.15
    assert res["phenotypic_fate"] == "QUIESCENT_REVERTED_FIBROBLAST"

    # Verification of tensile integrity and rupture safety
    assert res["residual_scar_stiffness_kpa"] >= 18.0
    assert res["residual_scar_stiffness_kpa"] <= 35.0
    assert res["estimated_burst_pressure_mmhg"] >= 180.0
    assert res["rupture_safety_certified"] is True
