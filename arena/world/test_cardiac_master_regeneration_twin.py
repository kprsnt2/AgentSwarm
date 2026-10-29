"""
Unit Test Suite: Capstone 30-Day Chrono-Pharmacology Master Digital Twin
========================================================================
Rigorous verification of cross-pathway antagonism failures under Simultaneous
Polypharmacy, 5-Phase Chrono-Gated clearance dynamics, scar burst pressure
invariants, electromechanical wiring, and organ-scale curative endpoints.
"""

import pytest
from arena.world.cardiac_master_regeneration_twin import (
    SystemsPharmacologyCollisionMatrix,
    ChronoPharmacologySchedule,
    CardiacMasterDigitalTwinEngine,
    simulate_30day_regeneration_trajectory,
)


def test_simultaneous_polypharmacy_catastrophic_failures():
    """Verify that Simultaneous Polypharmacy fails all 3 biomechanical checkpoints."""
    sim = simulate_30day_regeneration_trajectory(is_simultaneous=True)
    assert sim["success"] is False
    assert sim["rupture_occurred"] is True, "Premature LOXL2 cleavage must cause scar rupture"
    assert sim["min_burst_pressure_mmhg"] < 100.0, "Burst pressure must collapse below 180 mmHg limit"
    assert sim["arrhythmia_at_day30"] is True, "Cofilin antagonism must induce fatal arrhythmia"
    assert sim["congestion_at_day30"] is True, "Microtubule antagonism must lock diastolic filling"
    assert sim["final_lvef_pct"] < 30.0, "Ejection fraction must degrade under simultaneous failure"


def test_cofilin_clearance_and_actin_traction_recovery():
    """Verify Cofilin-1 PK clearance (>95% cleared by Hour 108) and polar catch traction."""
    # Hour 108: 84h post-dose (t_1/2 = 14.5 h)
    conc_108 = ChronoPharmacologySchedule.get_concentrations(108.0, is_simultaneous=False)
    assert conc_108["c_cofilin"] < 0.05, f"Expected >95% clearance by Hr 108, got {conc_108['c_cofilin']}"

    # Hour 192 (Start of Phase IV): Cofilin is completely cleared
    conc_192 = ChronoPharmacologySchedule.get_concentrations(192.0, is_simultaneous=False)
    assert conc_192["c_cofilin"] == 0.0

    state_192 = CardiacMasterDigitalTwinEngine.evaluate_biophysical_state(192.0, is_simultaneous=False)
    assert state_192["sarcomere_force_nn"] == 14.20, "Sarcomeric passive resistance must be fully restored"
    assert state_192["polar_traction_pn"] >= 11.0, f"Expected F_polar ~11.67 pN, got {state_192['polar_traction_pn']}"
    assert state_192["is_catch_regime"] is True, "Must operate in catch regime (>= 6.5 pN)"


def test_scar_hysteresis_reset_and_burst_pressure_safety():
    """Verify that LOXL2 cleavage is timed at the collagen inflection point and maintains burst pressure > 250 mmHg."""
    # Prior to Hour 120, LOXL2 cleavage must be inactive
    conc_96 = ChronoPharmacologySchedule.get_concentrations(96.0, is_simultaneous=False)
    assert conc_96["c_loxl2"] == 0.0

    # At Hour 120 (inflection point), ECM has matured to 34.5 kPa
    state_120 = CardiacMasterDigitalTwinEngine.evaluate_biophysical_state(120.0, is_simultaneous=False)
    assert state_120["ecm_stiffness_kpa"] >= 34.0
    assert state_120["burst_pressure_mmhg"] > 300.0

    # Post-washout (Hour 240+), ECM stabilizes at 29.6 kPa and burst pressure = 272.8 mmHg
    state_240 = CardiacMasterDigitalTwinEngine.evaluate_biophysical_state(240.0, is_simultaneous=False)
    assert state_240["ecm_stiffness_kpa"] == 29.6
    assert state_240["burst_pressure_mmhg"] == 272.8
    assert state_240["is_rupture_safe"] is True


def test_electromechanical_icd_wiring_and_arrhythmia_collapse():
    """Verify that Phase IV achieves R_polar >= 4.20 and Safety Factor >= 1.75."""
    # Hour 240 (48h into Phase IV): Safety Factor must exceed 1.0
    state_240 = CardiacMasterDigitalTwinEngine.evaluate_biophysical_state(240.0, is_simultaneous=False)
    assert state_240["safety_factor"] >= 1.0, "Safety factor must cross 1.0 within 48h of Phase IV"
    assert state_240["is_arrhythmia_vulnerable"] is False

    # Hour 360 (End of Phase IV): Full polarization
    state_360 = CardiacMasterDigitalTwinEngine.evaluate_biophysical_state(360.0, is_simultaneous=False)
    assert state_360["safety_factor"] >= 1.75
    assert state_360["is_arrhythmia_vulnerable"] is False


def test_chrono_gated_master_digital_twin_curative_invariants():
    """Verify 100% success of 5-Phase Chrono-Gated Schedule across all 720 hours."""
    chrono = simulate_30day_regeneration_trajectory(is_simultaneous=False)
    assert chrono["success"] is True
    assert chrono["clinical_outcome"] == "SUCCESSFUL_REGENERATION_CURED"
    assert chrono["rupture_occurred"] is False
    assert chrono["arrhythmia_at_day30"] is False
    assert chrono["congestion_at_day30"] is False

    # Exact quantitative benchmarks matching Engines 1-5
    assert chrono["min_burst_pressure_mmhg"] >= 250.0, f"Expected min P_burst >= 250 mmHg, got {chrono['min_burst_pressure_mmhg']}"
    assert chrono["final_ecm_stiffness_kpa"] == 29.6
    assert chrono["final_lvef_pct"] >= 52.0, f"Expected LVEF >= 52.0%, got {chrono['final_lvef_pct']}%"
    assert chrono["final_exercise_lvedp_mmhg"] < 14.5, f"Expected exercise LVEDP < 14.5 mmHg, got {chrono['final_exercise_lvedp_mmhg']}"
    assert chrono["final_safety_factor"] >= 1.75, f"Expected final SF >= 1.75, got {chrono['final_safety_factor']}"
