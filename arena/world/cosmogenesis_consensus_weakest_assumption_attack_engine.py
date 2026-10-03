"""
cosmogenesis_consensus_weakest_assumption_attack_engine.py

Quantitative Epistemic Engine Attacking the Weakest Assumption in the
Cosmogenesis Consensus Statement: Constant Dark Energy (w = -1) and
Unmodified Pre-Recombination Sound Horizon (r_s = 147.1 Mpc).

Authored by Agent Raman (A002), Generation 0.
Swarm Ledger Forensic Turn Deliverable.
"""

import math
from dataclasses import dataclass
from typing import Dict, Any, Tuple


# Fundamental Physical Constants (CODATA 2018 / PDG 2022)
C_LIGHT_KM_S: float = 299792.458            # Speed of light in km/s
C_LIGHT_M_S: float = 299792458.0             # Speed of light in m/s
G_NEWTON: float = 6.67430e-11                # m^3 kg^-1 s^-2
HBAR: float = 1.054571817e-34                # J s
M_PLANCK_GEV: float = 1.22091e19             # Planck mass in GeV


@dataclass(frozen=True)
class ConsensusBaseline:
    """Ratified Consensus Parameters (Planck 2018 PR3 baseline)."""
    H0: float = 67.36                        # km/s/Mpc
    H0_err: float = 0.54                     # km/s/Mpc
    Omega_m: float = 0.3153
    Omega_Lambda: float = 0.6847
    r_s_planck: float = 147.09               # Mpc (sound horizon at drag epoch)
    r_s_err: float = 0.26                    # Mpc
    theta_star: float = 0.0104110            # Angular scale of sound horizon
    theta_star_err: float = 0.0000031
    sigma_8: float = 0.8111
    sigma_8_err: float = 0.0060
    Y_p: float = 0.247


@dataclass(frozen=True)
class LocalObservationLadder:
    """Local Empirical Measurements Attacking the Baseline."""
    H0_shoes: float = 73.04                  # km/s/Mpc (Riess et al. 2022)
    H0_shoes_err: float = 1.04               # km/s/Mpc
    H0_cchp: float = 69.80                   # km/s/Mpc (TRGB Freedman et al.)
    H0_cchp_err: float = 1.70
    S8_weak_lensing: float = 0.766           # KiDS-1000 + DES-Y3 cosmic shear
    S8_wl_err: float = 0.014


class WeakestAssumptionAttackEngine:
    """
    Quantitative attacks against the consensus statement's core assumption:
    FLRW LCDM with cosmological constant w = -1 and standard early sound horizon.
    """

    def __init__(self):
        self.consensus = ConsensusBaseline()
        self.local = LocalObservationLadder()

    def evaluate_hubble_tension(self) -> Dict[str, float]:
        """
        Calculate the exact tension sigma between early CMB sound horizon
        and late-time local Cepheid-SN distance ladder.
        """
        diff = self.local.H0_shoes - self.consensus.H0
        combined_err = math.sqrt(self.local.H0_shoes_err ** 2 + self.consensus.H0_err ** 2)
        tension_sigma = diff / combined_err
        return {
            "H0_early": self.consensus.H0,
            "H0_late": self.local.H0_shoes,
            "delta_H0": diff,
            "combined_error": combined_err,
            "tension_sigma": tension_sigma,
        }

    def evaluate_sound_horizon_deficit(self) -> Dict[str, float]:
        """
        Calculate the required sound horizon r_s to reconcile Planck theta_*
        with the local H0 = 73.04 km/s/Mpc without late-time alterations.
        """
        # theta_* = r_s / D_A(z_*)
        # Since D_A is inversely proportional to H0 (D_A ~ c / H0 * integral),
        # r_s_required = r_s_planck * (H0_planck / H0_shoes)
        ratio = self.consensus.H0 / self.local.H0_shoes
        r_s_required = self.consensus.r_s_planck * ratio
        delta_r_s = r_s_required - self.consensus.r_s_planck
        pct_deficit = (delta_r_s / self.consensus.r_s_planck) * 100.0

        # Required error propagation
        # sigma_ratio / ratio = sqrt((err_early/early)^2 + (err_late/late)^2)
        rel_err = math.sqrt((self.consensus.H0_err / self.consensus.H0) ** 2 +
                            (self.local.H0_shoes_err / self.local.H0_shoes) ** 2)
        r_s_req_err = r_s_required * rel_err
        tension_sigma = abs(self.consensus.r_s_planck - r_s_required) / math.sqrt(
            self.consensus.r_s_err ** 2 + r_s_req_err ** 2
        )

        return {
            "r_s_planck_mpc": self.consensus.r_s_planck,
            "r_s_required_mpc": r_s_required,
            "r_s_deficit_mpc": delta_r_s,
            "percentage_deficit": pct_deficit,
            "tension_sigma": tension_sigma,
        }

    def evaluate_dynamical_dark_energy_breakdown(self, w0: float = -0.827, wa: float = -0.750) -> Dict[str, Any]:
        """
        Evaluate Chevallier-Polarski-Linder (CPL) dynamical dark energy:
        w(a) = w0 + wa * (1 - a)
        Assesses deviation from LCDM (w0 = -1, wa = 0).
        """
        # Distance to LCDM in parameter space
        delta_w0 = w0 - (-1.0)
        delta_wa = wa - 0.0

        # Covariance matrix for DESI 2024 Year 1 + CMB + DES-SN5YR (approximate 1-sigma)
        sigma_w0 = 0.063
        sigma_wa = 0.27
        rho_corr = -0.82  # strong negative degeneracy between w0 and wa

        # Chi-squared difference from LCDM (w0 = -1, wa = 0)
        # Delta chi^2 = [dw0, dwa] * Cov^(-1) * [dw0, dwa]^T
        det_cov = (sigma_w0 ** 2) * (sigma_wa ** 2) * (1.0 - rho_corr ** 2)
        inv_c00 = (sigma_wa ** 2) / det_cov
        inv_c11 = (sigma_w0 ** 2) / det_cov
        inv_c01 = - (rho_corr * sigma_w0 * sigma_wa) / det_cov

        delta_chi2 = (delta_w0 ** 2) * inv_c00 + 2.0 * delta_w0 * delta_wa * inv_c01 + (delta_wa ** 2) * inv_c11
        significance_sigma = math.sqrt(max(0.0, delta_chi2))

        # Check if phantom crossing occurs: w(a) = -1
        # w0 + wa * (1 - a) = -1 => wa * (1 - a) = -1 - w0 => 1 - a = (-1 - w0) / wa
        a_cross = 1.0 - (-1.0 - w0) / wa if wa != 0 else None
        z_cross = (1.0 / a_cross) - 1.0 if (a_cross is not None and 0 < a_cross < 1) else None

        return {
            "w0": w0,
            "wa": wa,
            "delta_chi2_from_lcdm": delta_chi2,
            "tension_sigma": significance_sigma,
            "phantom_crossing_scale_factor": a_cross,
            "phantom_crossing_redshift": z_cross,
            "lcdm_falsified_above_2sigma": significance_sigma > 2.0,
        }

    def evaluate_tcc_and_bgv_incompleteness(self, H_inf_gev: float = 1.0e13, e_folds: float = 60.0) -> Dict[str, Any]:
        """
        Evaluate Trans-Planckian Censorship Conjecture (TCC) and Borde-Guth-Vilenkin (BGV)
        singularity theorem against the simple inflation consensus assumption.
        """
        # TCC requirement: a_f / a_i * (H_f / M_pl) < 1
        # In de Sitter expansion, a_f / a_i = exp(N_e)
        # TCC bound: exp(N_e) * (H_inf / M_pl) < 1 => H_inf < M_pl * exp(-N_e)
        max_H_inf_tcc_gev = M_PLANCK_GEV * math.exp(-e_folds)
        violates_tcc = H_inf_gev > max_H_inf_tcc_gev

        # Tensor-to-scalar ratio r in canonical slow-roll: r = 16 * epsilon
        # H_inf = sqrt(pi^2 * A_s * r / 2) * M_pl => r ~ 2 * (H_inf / M_pl)^2 / (pi^2 * A_s)
        # For TCC-compliant H_inf, r_max < 10^-30
        A_s = 2.1e-9
        r_canonical = 2.0 * ((H_inf_gev / M_PLANCK_GEV) ** 2) / ((math.pi ** 2) * A_s)
        r_tcc_max = 2.0 * ((max_H_inf_tcc_gev / M_PLANCK_GEV) ** 2) / ((math.pi ** 2) * A_s)

        # BGV theorem: integral of H(t) dt > 0 along any past directed null geodesic
        # implies geodesic incompleteness (initial singularity) in classical spacetime.
        bgv_past_incomplete = True

        return {
            "H_inflation_assumed_gev": H_inf_gev,
            "max_H_inflation_tcc_gev": max_H_inf_tcc_gev,
            "violates_tcc": violates_tcc,
            "r_canonical_slow_roll": r_canonical,
            "r_tcc_max_bound": r_tcc_max,
            "bgv_geodesic_incompleteness": bgv_past_incomplete,
        }

    def evaluate_early_universe_reconciliation(self, f_ede: float = 0.10) -> Dict[str, float]:
        """
        Evaluate Early Dark Energy (EDE) resolution of the sound horizon deficit.
        Adding an axion-like field that acts as dark energy prior to recombination
        and decays faster than radiation (w_phi > 1/3) boosts H(z) around z_c ~ 3500,
        shrinking r_s without altering late-time angular diameter distance.
        """
        # delta r_s / r_s ~= - 0.5 * f_ede
        sound_horizon_reduction_pct = 0.5 * f_ede * 100.0
        r_s_reduced = self.consensus.r_s_planck * (1.0 - 0.5 * f_ede)
        inferred_H0 = self.consensus.H0 * (self.consensus.r_s_planck / r_s_reduced)
        residual_tension_sigma = abs(self.local.H0_shoes - inferred_H0) / math.sqrt(
            self.local.H0_shoes_err ** 2 + 1.2 ** 2
        )

        return {
            "f_ede_fraction": f_ede,
            "sound_horizon_reduction_pct": sound_horizon_reduction_pct,
            "r_s_reconciled_mpc": r_s_reduced,
            "inferred_H0_km_s_mpc": inferred_H0,
            "residual_tension_sigma": residual_tension_sigma,
        }
