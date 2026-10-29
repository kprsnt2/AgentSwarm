"""
Unit Test Suite: Cardiomyocyte Electromechanical Integration Engine
===================================================================
Rigorous verification of N-cadherin catch-bond fascia adherens mechanics,
microtubule targeted Cx43 delivery, perinexal Nav1.5 ephaptic coupling,
bidomain cable theory safety factor, and re-entrant arrhythmia collapse.
"""

import pytest
from arena.world.cardiac_electromechanical_integration_engine import (
    NCadherinCatchBondMechanics,
    MicrotubuleTargetedCx43Trafficking,
    PerinexusEphapticCoupling,
    BidomainCableConductionAndArrhythmia,
    simulate_post_cytokinetic_electromechanical_maturation,
)


def test_ncadherin_catch_bond_polar_mechanics():
    """Verify N-cadherin catch-bond kinetics and alpha-T-catenin unfolding at cell poles."""
    # Polar region under 29.6 kPa matrix + 15 kPa active systolic stress
    polar_force = NCadherinCatchBondMechanics.compute_local_tension(
        matrix_stiffness_kpa=29.6,
        systolic_stress_kpa=15.0,
        cyclic_strain_amplitude=0.10,
        is_polar_region=True,
    )
    assert 10.0 <= polar_force <= 15.0, f"Expected polar force 10-15 pN, got {polar_force}"

    polar_kinetics = NCadherinCatchBondMechanics.evaluate_bond_lifetime(polar_force)
    assert polar_kinetics["is_catch_regime"] is True
    assert polar_kinetics["is_alpha_catenin_unfolded"] is True
    assert polar_kinetics["vinculin_recruitment_factor"] > 0.40
    assert polar_kinetics["bond_lifetime_s"] > 3.0, "Catch regime should sustain long bond lifetime"

    # Lateral membrane under minimal orthogonal stress
    lateral_force = NCadherinCatchBondMechanics.compute_local_tension(
        matrix_stiffness_kpa=29.6,
        systolic_stress_kpa=15.0,
        cyclic_strain_amplitude=0.10,
        is_polar_region=False,
    )
    assert lateral_force < 2.0, f"Expected lateral force < 2 pN, got {lateral_force}"

    lateral_kinetics = NCadherinCatchBondMechanics.evaluate_bond_lifetime(lateral_force)
    assert lateral_kinetics["is_catch_regime"] is False
    assert lateral_kinetics["is_alpha_catenin_unfolded"] is False
    assert lateral_kinetics["vinculin_recruitment_factor"] == 0.0


def test_microtubule_targeted_cx43_trafficking():
    """Verify kinesin-mediated Cx43 trafficking and cortical +TIP capture polarization."""
    flux_baseline = MicrotubuleTargetedCx43Trafficking.compute_cx43_polarization_flux(
        polar_vinculin_factor=0.65,
        lateral_vinculin_factor=0.0,
        eb1_stabilizer_active=False,
    )
    assert flux_baseline["p_capture_polar"] > 0.60
    assert flux_baseline["p_capture_lateral"] == 0.04
    assert flux_baseline["polar_to_lateral_ratio_r"] > 50.0

    # With EB1 stabilization (+TIP capture enhancer)
    flux_stabilized = MicrotubuleTargetedCx43Trafficking.compute_cx43_polarization_flux(
        polar_vinculin_factor=0.65,
        lateral_vinculin_factor=0.0,
        eb1_stabilizer_active=True,
    )
    assert flux_stabilized["p_capture_polar"] >= flux_baseline["p_capture_polar"]
    assert flux_stabilized["polar_delivery_flux"] >= flux_baseline["polar_delivery_flux"]


def test_perinexus_ephaptic_coupling():
    """Verify perinexal cleft resistance, Nav1.5 negative cleft potential, and alphaCT1 effect."""
    res_control = PerinexusEphapticCoupling.compute_ephaptic_voltage_transient(
        cleft_width_nm=15.0,
        nav15_peak_current_pa=-1800.0,
        alpha_ct1_peptide_active=False,
    )
    assert res_control["cleft_resistance_mohm"] > 1.0
    assert res_control["perinexal_v_cleft_mv"] < -15.0
    assert res_control["ephaptic_depolarization_mv"] > 15.0
    assert res_control["plaque_accretion_rate_multiplier"] == 1.00

    # Test alphaCT1 peptide activation (ZO-1 PDZ2 displacement)
    res_treated = PerinexusEphapticCoupling.compute_ephaptic_voltage_transient(
        cleft_width_nm=15.0,
        nav15_peak_current_pa=-1800.0,
        alpha_ct1_peptide_active=True,
    )
    assert res_treated["plaque_accretion_rate_multiplier"] == 3.40


def test_bidomain_cable_conduction_and_arrhythmia():
    """Verify anisotropic conduction velocities and Source-Sink Safety Factor thresholds."""
    # Immature, isotropic phenotype (Day 0)
    immature = BidomainCableConductionAndArrhythmia.evaluate_conduction_and_vulnerability(
        r_polar=1.0,
        ik1_current_density_pa_per_pf=2.5,
    )
    assert immature["source_sink_safety_factor"] < 1.0
    assert immature["is_arrhythmia_vulnerable"] is True
    assert immature["electrophysiological_fate"] == "UNIDIRECTIONAL_BLOCK_REENTRY_VULNERABLE"

    # Fully mature, polarized phenotype (Day 14 treated)
    mature = BidomainCableConductionAndArrhythmia.evaluate_conduction_and_vulnerability(
        r_polar=8.5,
        ik1_current_density_pa_per_pf=11.5,
    )
    assert mature["source_sink_safety_factor"] > 1.30
    assert mature["is_arrhythmia_vulnerable"] is False
    assert mature["electrophysiological_fate"] == "SYNCHRONOUS_1_TO_1_CAPTURE"
    assert mature["anisotropy_ratio"] > 4.0


def test_multiscale_electromechanical_maturation_simulation():
    """Verify 14-day temporal trajectory and collapse of arrhythmia vulnerable window."""
    # Untreated trajectory
    untreated = simulate_post_cytokinetic_electromechanical_maturation(treatment_applied=False)
    assert untreated["synchronous_capture_achieved"] is False
    assert untreated["arrhythmia_risk_classification"] == "HIGH_VULNERABILITY_LETHAL"
    assert untreated["final_safety_factor"] < 1.0
    assert untreated["vulnerable_days_count"] == 15

    # Treated with Tri-Modal Protocol (alphaCT1 + Epothilone D + T3/Dex)
    treated = simulate_post_cytokinetic_electromechanical_maturation(treatment_applied=True)
    assert treated["synchronous_capture_achieved"] is True
    assert treated["arrhythmia_risk_classification"] == "ZERO_REENTRY_SAFE"
    assert treated["final_safety_factor"] > 1.30
    assert treated["final_r_polar"] >= 8.0
    assert treated["vulnerable_days_count"] <= 3, "Vulnerability window must collapse within 72 hours"
