"""
Unit Test Suite: HFpEF Rate-Dependent Diastolic Viscoelastic Engine
===================================================================
Rigorous verification of Marko-Siggia WLC titin mechanics, detyrosinated
microtubule viscous drag, residual cross-bridge detachment, chamber lusitropy
(tau_Weiss, EDPVR), and Tri-Pathway Protocol efficacy with systolic preservation.
"""

import pytest
from arena.world.cardiac_hfpef_viscoelastic_relaxation_engine import (
    TitinPolymerMechanicsWLC,
    MicrotubuleDesminViscoelasticDrag,
    ResidualCrossbridgeLatch,
    ChamberMechanicsAndLusitropy,
    simulate_hfpef_exercise_relaxation_dynamics,
)


def test_titin_wlc_polymer_mechanics_and_pkg_effect():
    """Verify Marko-Siggia WLC titin elasticity and PKG phosphorylation rescue."""
    # Healthy baseline at SL = 2.20 um
    healthy = TitinPolymerMechanicsWLC.compute_titin_passive_stress(
        sarcomere_length_um=2.20,
        is_hfpef=False,
    )
    assert 1.5 <= healthy["passive_titin_stress_kpa"] <= 3.5, f"Expected 1.5-3.5 kPa, got {healthy['passive_titin_stress_kpa']}"
    assert healthy["persistence_length_nm"] == 1.35
    assert healthy["contour_length_nm"] == 220.0

    # HFpEF hypophosphorylated & oxidized state
    hfpef = TitinPolymerMechanicsWLC.compute_titin_passive_stress(
        sarcomere_length_um=2.20,
        is_hfpef=True,
        pkg_phosphorylation_ratio=0.22,
        oxidative_crosslink_density=0.75,
    )
    assert hfpef["passive_titin_stress_kpa"] >= 7.5, f"Expected >= 7.5 kPa in HFpEF, got {hfpef['passive_titin_stress_kpa']}"
    assert hfpef["persistence_length_nm"] < 0.80
    assert hfpef["contour_length_nm"] < 130.0

    # PKG rescue
    rescued = TitinPolymerMechanicsWLC.compute_titin_passive_stress(
        sarcomere_length_um=2.20,
        is_hfpef=True,
        pkg_phosphorylation_ratio=0.95,
        oxidative_crosslink_density=0.10,
    )
    assert rescued["passive_titin_stress_kpa"] < 2.5, "PKG phosphorylation must restore compliant titin tension"


def test_microtubule_desmin_viscous_drag():
    """Verify strain-rate dependent viscous drag and VASH1/2 inhibition effect."""
    # Rest velocity (2.5 um/s) vs Exercise velocity (6.6 um/s) in untreated HFpEF
    rest_drag = MicrotubuleDesminViscoelasticDrag.compute_viscous_resistance(
        sarcomere_velocity_um_s=2.5,
        detyrosination_fraction=0.68,
        sarcomere_length_um=1.95,
    )
    exercise_drag = MicrotubuleDesminViscoelasticDrag.compute_viscous_resistance(
        sarcomere_velocity_um_s=6.6,
        detyrosination_fraction=0.68,
        sarcomere_length_um=1.95,
    )
    assert exercise_drag["viscous_drag_stress_kpa"] > 2.0 * rest_drag["viscous_drag_stress_kpa"]
    assert exercise_drag["effective_viscosity_kpa_s"] > 0.65

    # VASH1/2 inhibition (detyrosination reduced to 0.14)
    treated_drag = MicrotubuleDesminViscoelasticDrag.compute_viscous_resistance(
        sarcomere_velocity_um_s=6.6,
        detyrosination_fraction=0.14,
        sarcomere_length_um=1.95,
    )
    assert treated_drag["effective_viscosity_kpa_s"] < 0.25
    assert treated_drag["viscous_drag_stress_kpa"] < 0.80


def test_residual_crossbridge_detachment_kinetics():
    """Verify delayed cross-bridge detachment and SERCA2a acceleration."""
    # Control HFpEF (tau_xb = 65 ms) at t = 55 ms
    control_xb = ResidualCrossbridgeLatch.compute_residual_crossbridge_stress(
        time_post_systole_ms=55.0,
        is_hfpef=True,
        serca_activation_factor=1.0,
    )
    assert control_xb["tau_crossbridge_ms"] == 65.0
    assert control_xb["residual_crossbridge_stress_kpa"] > 1.80

    # SERCA2a/DWORF activated (factor 2.6)
    accelerated_xb = ResidualCrossbridgeLatch.compute_residual_crossbridge_stress(
        time_post_systole_ms=55.0,
        is_hfpef=True,
        serca_activation_factor=2.6,
    )
    assert accelerated_xb["tau_crossbridge_ms"] < 45.0
    assert accelerated_xb["residual_crossbridge_stress_kpa"] < 1.45


def test_chamber_mechanics_and_lusitropic_bifurcation():
    """Verify chamber filling, critical heart rate bifurcation, and congestion threshold."""
    bifurcation = ChamberMechanicsAndLusitropy.compute_critical_lusitropic_bifurcation(
        detyrosination_fraction=0.68,
        serca_activation_factor=1.0,
    )
    assert 130.0 <= bifurcation["critical_heart_rate_bpm"] <= 145.0, f"Expected HR_crit ~130-145, got {bifurcation['critical_heart_rate_bpm']}"
    assert 5.5 <= bifurcation["critical_sarcomere_velocity_um_s"] <= 7.5
    assert bifurcation["critical_strain_rate_per_s"] > 2.8


def test_tri_pathway_exercise_rescue_and_systolic_preservation():
    """Verify Tri-Pathway Protocol collapse of exercise LVEDP and systolic contractility preservation."""
    # Untreated exercise at 140 bpm
    untreated = simulate_hfpef_exercise_relaxation_dynamics(is_treated=False, heart_rate_bpm=140.0)
    assert untreated["lvedp_mmhg"] >= 25.0, f"Untreated LVEDP must exceed 25 mmHg, got {untreated['lvedp_mmhg']}"
    assert untreated["clinical_state"] == "PULMONARY_CONGESTION_LOCK"
    assert untreated["is_congestion_prevented"] is False
    assert untreated["tau_weiss_ms"] > 70.0

    # Treated exercise at 140 bpm
    treated = simulate_hfpef_exercise_relaxation_dynamics(is_treated=True, heart_rate_bpm=140.0)
    assert treated["lvedp_mmhg"] < 15.0, f"Treated LVEDP must be < 15 mmHg, got {treated['lvedp_mmhg']}"
    assert treated["clinical_state"] == "COMPENSATED_LUSITROPIC_CAPTURE"
    assert treated["is_congestion_prevented"] is True
    assert treated["tau_weiss_ms"] < 45.0
    assert treated["peak_systolic_preservation_pct"] >= 95.0, "Must preserve >95% peak systolic force"
