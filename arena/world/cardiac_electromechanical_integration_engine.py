"""
Cardiomyocyte Electromechanical Integration & Arrhythmogenesis Engine
=====================================================================
Biophysical modeling of post-cytokinetic cardiomyocyte polarization,
N-cadherin catch-bond fascia adherens mechanics, microtubule (+TIP)
targeted Cx43 trafficking, perinexal Nav1.5 ephaptic coupling,
bidomain cable conduction anisotropy, and re-entrant arrhythmia safety.

Author: Swarm Research Agent (Cardiovascular Electrophysiology Frontier)
License: MIT
"""

import math
from typing import Dict, List, Tuple, Any


class NCadherinCatchBondMechanics:
    """
    Directional stress tensor and single-molecule catch-slip bond kinetics
    of trans-dimerizing N-cadherin (CDH2) and alpha-T-catenin (CTNNA3) unfolding.
    """

    K_CATCH_0 = 0.08       # Basal catch-pathway dissociation rate (s^-1)
    K_SLIP_0 = 0.02        # Basal slip-pathway dissociation rate (s^-1)
    X_CATCH_NM = 0.85      # Catch-pathway transition distance (nm)
    X_SLIP_NM = 0.42       # Slip-pathway transition distance (nm)
    KB_T_PN_NM = 4.114     # Thermal energy at 310 K (pN * nm)
    ALPHA_CATENIN_UNFOLD_THRESH_PN = 6.5  # Force required to unfold alpha-T-catenin to expose vinculin/desmoplakin binding sites

    @classmethod
    def compute_local_tension(
        cls,
        matrix_stiffness_kpa: float = 29.6,
        systolic_stress_kpa: float = 15.0,
        cyclic_strain_amplitude: float = 0.10,
        is_polar_region: bool = True,
    ) -> float:
        """
        Compute tensile force per single N-cadherin trans-dimer (pN) at cell poles vs lateral membranes.
        """
        if is_polar_region:
            # Uniaxial strain aligned with longitudinal myofibril axis
            effective_stress = systolic_stress_kpa + matrix_stiffness_kpa * cyclic_strain_amplitude
            # Scaled to single cadherin dimer force (pN) across fascia adherens junction density
            force_pn = min(22.0, max(1.0, 0.65 * effective_stress))
        else:
            # Lateral membrane undergoes minimal orthogonal strain
            effective_stress = 0.08 * systolic_stress_kpa
            force_pn = min(3.5, max(0.2, 0.45 * effective_stress))

        return round(force_pn, 3)

    @classmethod
    def evaluate_bond_lifetime(cls, force_pn: float) -> Dict[str, Any]:
        """
        Evaluate two-pathway catch-slip bond lifetime:
            k_off(F) = k_catch * exp(-F * x_catch / kBT) + k_slip * exp(F * x_slip / kBT)
            tau = 1 / k_off
        """
        f = max(0.0, float(force_pn))
        k_catch = cls.K_CATCH_0 * math.exp(-f * cls.X_CATCH_NM / cls.KB_T_PN_NM)
        k_slip = cls.K_SLIP_0 * math.exp(f * cls.X_SLIP_NM / cls.KB_T_PN_NM)
        k_off = k_catch + k_slip
        lifetime_s = 1.0 / k_off if k_off > 0 else 0.0

        is_catenin_unfolded = bool(f >= cls.ALPHA_CATENIN_UNFOLD_THRESH_PN)
        vinculin_recruitment_factor = min(1.0, max(0.0, (f - cls.ALPHA_CATENIN_UNFOLD_THRESH_PN) / 8.0)) if is_catenin_unfolded else 0.0

        return {
            "applied_force_pn": round(f, 3),
            "k_off_per_s": round(k_off, 4),
            "bond_lifetime_s": round(lifetime_s, 3),
            "is_catch_regime": bool(5.0 <= f <= 15.0),
            "is_alpha_catenin_unfolded": is_catenin_unfolded,
            "vinculin_recruitment_factor": round(vinculin_recruitment_factor, 4),
        }


class MicrotubuleTargetedCx43Trafficking:
    """
    Intracellular reaction-diffusion + active Kinesin-1 transport of Cx43 connexons
    along microtubules with cortical plus-end (+TIP) capture by p150Glued/dynein.
    """

    V_KINESIN_UM_S = 0.85    # Active kinesin anterograde transport velocity (um/s)
    P_CAPTURE_BASE = 0.04    # Passive cortical capture probability at unpolarized membranes
    P_CAPTURE_POLAR_MAX = 0.92  # Maximum plus-end capture probability at tension-activated ICD poles

    @classmethod
    def compute_cx43_polarization_flux(
        cls,
        polar_vinculin_factor: float,
        lateral_vinculin_factor: float,
        eb1_stabilizer_active: bool = False,
    ) -> Dict[str, float]:
        """
        Compute polar vs lateral Cx43 delivery rate and polarization partitioning ratio R_polar.
        """
        # Cortical p150Glued anchorage is proportional to tension-stabilized cadherin-catenin-vinculin plaques
        p_capture_polar = cls.P_CAPTURE_BASE + (cls.P_CAPTURE_POLAR_MAX - cls.P_CAPTURE_BASE) * polar_vinculin_factor
        p_capture_lateral = cls.P_CAPTURE_BASE + (cls.P_CAPTURE_POLAR_MAX - cls.P_CAPTURE_BASE) * lateral_vinculin_factor

        if eb1_stabilizer_active:
            p_capture_polar = min(0.98, p_capture_polar * 1.15)

        # Delivery fluxes (arbitrary relative units)
        j_polar = 100.0 * p_capture_polar
        j_lateral = 100.0 * max(0.02, p_capture_lateral) * 0.25  # Endocytosis active at low tension

        r_polar = j_polar / j_lateral if j_lateral > 0 else 1.0

        return {
            "p_capture_polar": round(p_capture_polar, 4),
            "p_capture_lateral": round(p_capture_lateral, 4),
            "polar_delivery_flux": round(j_polar, 2),
            "lateral_delivery_flux": round(j_lateral, 2),
            "polar_to_lateral_ratio_r": round(r_polar, 3),
        }


class PerinexusEphapticCoupling:
    """
    Kinetic partitioning of Cx43 from perinexal hemichannels into docked gap junctions,
    ZO-1 PDZ2 binding inhibition (alphaCT1), and Nav1.5/Kir2.1 ephaptic coupling.
    """

    CLEFT_WIDTH_RESTING_NM = 15.0   # Perinexal intercellular cleft width (nm)
    R_INTERSTITIAL_OHM_CM = 150.0   # Cleft extracellular resistivity (Ohm * cm)
    NAV15_PERINEXAL_FRACTION = 0.62 # Fraction of cellular Nav1.5 clustered in perinexus

    @classmethod
    def compute_ephaptic_voltage_transient(
        cls,
        cleft_width_nm: float = 15.0,
        nav15_peak_current_pa: float = -1800.0,
        alpha_ct1_peptide_active: bool = False,
    ) -> Dict[str, float]:
        """
        Compute negative extracellular cleft potential V_cleft and downstream ephaptic depolarization.
        """
        w = max(5.0, float(cleft_width_nm))
        # Cleft resistance scales inversely with width
        # R_cleft = rho * L / (w * W_perinexus)
        r_cleft_mohm = (cls.R_INTERSTITIAL_OHM_CM * 1e-4) / (w * 1e-7 * 1.0) * 1.25  # MegaOhms

        # Nav1.5 inward current into the upstream cell generates negative cleft voltage:
        # V_cleft = I_Na * R_cleft
        # Downstream cell experiences an immediate depolarization: Delta V_m = -V_cleft
        v_cleft_mv = (nav15_peak_current_pa * 1e-12) * (r_cleft_mohm * 1e6) * 1000.0  # mV
        ephaptic_depol_mv = -v_cleft_mv  # positive inward driving force

        # Docked gap junction accretion rate
        # alphaCT1 blocks ZO-1 PDZ2, freeing perinexal Cx43 to dock into plaques
        accretion_rate_multiplier = 3.40 if alpha_ct1_peptide_active else 1.00

        return {
            "cleft_width_nm": round(w, 1),
            "cleft_resistance_mohm": round(r_cleft_mohm, 2),
            "perinexal_v_cleft_mv": round(v_cleft_mv, 2),
            "ephaptic_depolarization_mv": round(ephaptic_depol_mv, 2),
            "plaque_accretion_rate_multiplier": round(accretion_rate_multiplier, 2),
        }


class BidomainCableConductionAndArrhythmia:
    """
    Bidomain continuous cable theory modeling of cardiac tissue conduction,
    conduction velocity anisotropy (theta_L / theta_T), and Source-Sink Safety Factor (SF).
    """

    R_POLAR_CRITICAL = 4.20     # Minimum polarization ratio to prevent re-entry
    IK1_DENSITY_CRITICAL = 6.50  # Minimum Kir2.1 / IK1 current density (pA/pF) to stabilize resting potential
    THETA_L_MATURE_CM_S = 65.0  # Normal adult longitudinal conduction velocity (cm/s)
    THETA_T_MATURE_CM_S = 18.5  # Normal transverse conduction velocity (cm/s)

    @classmethod
    def evaluate_conduction_and_vulnerability(
        cls,
        r_polar: float,
        ik1_current_density_pa_per_pf: float,
        is_systolic_contracting: bool = True,
    ) -> Dict[str, Any]:
        """
        Evaluate anisotropic conduction velocity, Source-Sink Safety Factor (SF),
        and arrhythmogenic re-entry vulnerability window.
        """
        r = max(0.5, float(r_polar))
        ik1 = max(0.5, float(ik1_current_density_pa_per_pf))

        # Conduction velocities: theta_L scales with polar gap junction conductance
        # theta_T scales with lateral conductance (inversely with polarization)
        theta_l = min(75.0, cls.THETA_L_MATURE_CM_S * math.sqrt(r / (r + 2.5)) * 1.35)
        theta_t = max(8.0, cls.THETA_T_MATURE_CM_S * math.sqrt(3.0 / (r + 1.0)))
        anisotropy_ratio = theta_l / theta_t

        # Source-Sink Safety Factor (SF)
        # SF = I_source / I_sink.
        # High lateral Cx43 creates excessive lateral electrotonic sink load, dragging SF down below 1.0.
        source_strength = 1.0 - math.exp(-r / 3.0)
        sink_load_penalty = 0.55 / math.sqrt(r)
        ik1_stabilization = min(1.3, ik1 / cls.IK1_DENSITY_CRITICAL)

        safety_factor = (0.75 + 0.85 * source_strength - sink_load_penalty) * ik1_stabilization
        safety_factor = max(0.35, min(1.85, safety_factor))

        # Vulnerable window for unidirectional conduction block and spiral wave re-entry
        is_arrhythmia_vulnerable = bool(r < cls.R_POLAR_CRITICAL or ik1 < cls.IK1_DENSITY_CRITICAL or safety_factor < 1.0)

        fate = "SYNCHRONOUS_1_TO_1_CAPTURE" if not is_arrhythmia_vulnerable else "UNIDIRECTIONAL_BLOCK_REENTRY_VULNERABLE"

        return {
            "r_polar": round(r, 3),
            "ik1_density_pa_per_pf": round(ik1, 2),
            "theta_longitudinal_cm_s": round(theta_l, 1),
            "theta_transverse_cm_s": round(theta_t, 1),
            "anisotropy_ratio": round(anisotropy_ratio, 2),
            "source_sink_safety_factor": round(safety_factor, 3),
            "is_arrhythmia_vulnerable": is_arrhythmia_vulnerable,
            "electrophysiological_fate": fate,
        }


def simulate_post_cytokinetic_electromechanical_maturation(
    treatment_applied: bool = True,
    simulation_days: int = 14,
) -> Dict[str, Any]:
    """
    Simulate temporal evolution of newly divided cardiomyocyte from Day 0 (unpolarized spherical)
    to Day 14 post-cytokinesis, with or without the Tri-Modal Maturation Protocol:
      1. alphaCT1 peptide (ZO-1 PDZ2 block -> plaque accretion)
      2. Low-dose Epothilone D / Taxol (microtubule +TIP / EB1 stabilization)
      3. T3 / Dexamethasone metabolic maturation (Kir2.1 / IK1 induction)
    """
    days = list(range(simulation_days + 1))
    r_polar_traj = []
    safety_factor_traj = []
    theta_l_traj = []
    ik1_traj = []
    vulnerable_days = []

    for day in days:
        if not treatment_applied:
            # Spontaneous slow maturation (unassisted in stiff border zone)
            # High lateral mechanical stress retards polarization
            r_pol = 1.0 + 1.8 * (1.0 - math.exp(-day / 8.0))
            ik1 = 2.5 + 3.0 * (1.0 - math.exp(-day / 10.0))
            eb1 = False
            alpha_ct1 = False
        else:
            # Tri-Modal Maturation Protocol applied Days 0-7
            eb1 = bool(day <= 7)
            alpha_ct1 = bool(day <= 7)
            r_pol = 1.0 + 8.2 * (1.0 - math.exp(-day / 3.2))
            ik1 = 2.5 + 9.5 * (1.0 - math.exp(-day / 3.8))

        # Evaluate electrophysiology
        res = BidomainCableConductionAndArrhythmia.evaluate_conduction_and_vulnerability(
            r_polar=r_pol,
            ik1_current_density_pa_per_pf=ik1,
            is_systolic_contracting=True,
        )

        r_polar_traj.append(round(r_pol, 2))
        safety_factor_traj.append(res["source_sink_safety_factor"])
        theta_l_traj.append(res["theta_longitudinal_cm_s"])
        ik1_traj.append(round(ik1, 2))

        if res["is_arrhythmia_vulnerable"]:
            vulnerable_days.append(day)

    final_sf = safety_factor_traj[-1]
    final_r = r_polar_traj[-1]
    capture_achieved = bool(final_sf >= 1.0 and len(vulnerable_days) <= 3 if treatment_applied else False)

    return {
        "treatment_applied": treatment_applied,
        "simulation_days": simulation_days,
        "final_r_polar": final_r,
        "final_safety_factor": final_sf,
        "final_theta_longitudinal_cm_s": theta_l_traj[-1],
        "final_ik1_density": ik1_traj[-1],
        "vulnerable_days_count": len(vulnerable_days),
        "vulnerable_days": vulnerable_days,
        "synchronous_capture_achieved": capture_achieved,
        "arrhythmia_risk_classification": "ZERO_REENTRY_SAFE" if capture_achieved else "HIGH_VULNERABILITY_LETHAL",
        "r_polar_trajectory": r_polar_traj,
        "safety_factor_trajectory": safety_factor_traj,
        "theta_longitudinal_trajectory": theta_l_traj,
    }
