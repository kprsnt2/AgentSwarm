"""
Cosmogenesis Neutrino Mass and Free-Streaming Analysis Engine
============================================================
Quantitative empirical framework analyzing the cosmological neutrino mass bound,
free-streaming suppression of large-scale structure, and the tension between
laboratory neutrino oscillation lower limits and cosmological upper bounds
(Planck 2018 + DESI 2024).

Standards of Evidence:
- NuFIT 5.2 (2022/2024) three-neutrino oscillation parameters.
- Planck 2018 cosmological parameters (A&A 641, A6, 2020).
- DESI 2024 BAO and cosmological constraints (arXiv:2404.03002).
- KATRIN direct kinematic limit (Nature Physics 18, 160-166, 2022).
- KamLAND-Zen 0nu-beta-beta constraint on m_bb (PRL 130, 051801, 2023).
"""

import math
from typing import Dict, Any, Tuple, List

# Physical constants and fiducial parameters
C_KM_S: float = 299792.458                 # Speed of light in km/s
T_CMB_K: float = 2.72548                   # CMB temperature in Kelvin (Fixsen 2009)
N_EFF_STANDARD: float = 3.044              # Relativistic degrees of freedom (Bennett et al. 2021)
K_B_EV_K: float = 8.617333262e-5           # Boltzmann constant in eV/K

# NuFIT 5.2 (2022) neutrino oscillation parameters
DELTA_M21_SQ_EV2: float = 7.42e-5          # Solar mass splitting (eV^2)
DELTA_M21_SQ_ERR_EV2: float = 0.21e-5

DELTA_M31_SQ_NO_EV2: float = 2.515e-3      # Atmospheric mass splitting for Normal Ordering (eV^2)
DELTA_M31_SQ_NO_ERR_EV2: float = 0.028e-3

DELTA_M32_SQ_IO_EV2: float = 2.498e-3      # Atmospheric mass splitting for Inverted Ordering (|Delta m^2_32|, eV^2)
DELTA_M32_SQ_IO_ERR_EV2: float = 0.028e-3

# Cosmological observational bounds on sum m_nu (95% CL)
SUM_M_NU_BOUND_PLANCK18: float = 0.120      # Planck 2018 TT,TE,EE+lowE+lensing+BAO (eV)
SUM_M_NU_BOUND_DESI2024: float = 0.072      # DESI 2024 + Planck PR4 + CMB lensing (eV)
SUM_M_NU_BOUND_DESI_ACT: float = 0.064      # DESI 2024 + ACT DR6 lensing + Pantheon+ (eV)

# Laboratory direct limits (90% CL)
KATRIN_LIMIT_EV: float = 0.45              # Direct kinematic tritium decay bound (eV)
KAMLAND_ZEN_MBB_MAX_EV: float = 0.156      # 0nu-beta-beta limit upper band (eV)
KAMLAND_ZEN_MBB_MIN_EV: float = 0.036      # 0nu-beta-beta limit lower band (eV)

# Fiducial background cosmology (Planck 2018 base Lambda-CDM)
OMEGA_B_H2: float = 0.02237
OMEGA_C_H2: float = 0.1200
H0_PLANCK: float = 67.36
H_PARAM: float = H0_PLANCK / 100.0
OMEGA_M: float = (OMEGA_B_H2 + OMEGA_C_H2) / (H_PARAM ** 2)


class NeutrinoMassOscillationModel:
    """Models neutrino mass spectra and absolute physical thresholds from oscillation data."""

    @staticmethod
    def compute_masses_normal_ordering(m1: float = 0.0) -> Tuple[float, float, float, float]:
        """
        Calculates (m1, m2, m3, sum_m) for Normal Ordering given lightest neutrino mass m1.
        m2 = sqrt(m1^2 + Delta m_21^2)
        m3 = sqrt(m1^2 + Delta m_31^2)
        """
        if m1 < 0:
            raise ValueError("Mass m1 cannot be negative")
        m2 = math.sqrt(m1 ** 2 + DELTA_M21_SQ_EV2)
        m3 = math.sqrt(m1 ** 2 + DELTA_M31_SQ_NO_EV2)
        sum_m = m1 + m2 + m3
        return m1, m2, m3, sum_m

    @staticmethod
    def compute_masses_inverted_ordering(m3: float = 0.0) -> Tuple[float, float, float, float]:
        """
        Calculates (m1, m2, m3, sum_m) for Inverted Ordering given lightest neutrino mass m3.
        m2 = sqrt(m3^2 + |Delta m_32^2|)
        m1 = sqrt(m2^2 - Delta m_21^2)
        """
        if m3 < 0:
            raise ValueError("Mass m3 cannot be negative")
        m2 = math.sqrt(m3 ** 2 + DELTA_M32_SQ_IO_EV2)
        m1 = math.sqrt(m2 ** 2 - DELTA_M21_SQ_EV2)
        sum_m = m1 + m2 + m3
        return m1, m2, m3, sum_m

    @classmethod
    def get_physical_floors(cls) -> Dict[str, Any]:
        """Returns the rigorous minimum sum of neutrino masses allowed by oscillation data."""
        _, _, _, sum_no_min = cls.compute_masses_normal_ordering(m1=0.0)
        _, _, _, sum_io_min = cls.compute_masses_inverted_ordering(m3=0.0)
        return {
            "normal_ordering_min_sum_ev": round(sum_no_min, 5),
            "inverted_ordering_min_sum_ev": round(sum_io_min, 5),
            "ratio_io_to_no_floor": round(sum_io_min / sum_no_min, 4)
        }


class RelicNeutrinoCosmologyEngine:
    """Computes cosmic neutrino background properties, free-streaming scales, and LSS suppression."""

    @staticmethod
    def compute_neutrino_temperature_today() -> float:
        """
        T_nu,0 = (4/11)^(1/3) * T_gamma,0 in Kelvin.
        """
        return ((4.0 / 11.0) ** (1.0 / 3.0)) * T_CMB_K

    @classmethod
    def compute_omega_nu_h2(cls, sum_m_nu_ev: float) -> float:
        """
        Relic energy density: Omega_nu * h^2 = sum(m_nu) / (93.14 eV).
        Derived from rho_nu,0 = (3/4) * (4/11)^(4/3) * rho_gamma,0 * sum(m_nu) / (3.15 * T_nu,0).
        """
        return sum_m_nu_ev / 93.14

    @classmethod
    def compute_non_relativistic_redshift(cls, m_nu_ev: float) -> float:
        """
        Redshift z_nr when a neutrino of mass m_nu becomes non-relativistic (3*T_nu ~ m_nu):
        1 + z_nr = m_nu / (3.15 * k_B * T_nu,0)
        """
        t_nu_ev = cls.compute_neutrino_temperature_today() * K_B_EV_K
        one_plus_z = m_nu_ev / (3.15 * t_nu_ev)
        return max(0.0, one_plus_z - 1.0)

    @classmethod
    def compute_free_streaming_wavenumber_nr(cls, m_nu_ev: float, omega_m: float = OMEGA_M) -> float:
        """
        Comoving wavenumber k_nr at non-relativistic transition (h / Mpc):
        k_nr approx 0.018 * sqrt(Omega_m) * (m_nu / 1 eV)^(1/2) h Mpc^-1
        """
        return 0.018 * math.sqrt(omega_m) * math.sqrt(max(0.001, m_nu_ev))

    @classmethod
    def compute_matter_power_suppression(cls, sum_m_nu_ev: float, omega_m_h2: float = (OMEGA_B_H2 + OMEGA_C_H2)) -> float:
        """
        Asymptotic linear matter power spectrum suppression on scales k >> k_fs:
        Delta P(k) / P(k) approx -8 * (Omega_nu / Omega_m) = -8 * (sum_m_nu / (93.14 * Omega_m * h^2))
        """
        f_nu = cls.compute_omega_nu_h2(sum_m_nu_ev) / omega_m_h2
        return -8.0 * f_nu


class CosmologicalNeutrinoTensionAuditor:
    """Audits the tension between cosmological upper limits and oscillation lower floors."""

    @classmethod
    def evaluate_ordering_viability(cls) -> Dict[str, Any]:
        floors = NeutrinoMassOscillationModel.get_physical_floors()
        sum_no = floors["normal_ordering_min_sum_ev"]
        sum_io = floors["inverted_ordering_min_sum_ev"]

        # DESI 2024 + Planck bound: sum m_nu < 0.072 eV (95% CL)
        # Assuming a half-Gaussian posterior peaking at 0, 95% CL = 1.96 * sigma_eff
        sigma_eff = SUM_M_NU_BOUND_DESI2024 / 1.96

        io_tension_sigma = (sum_io - SUM_M_NU_BOUND_DESI2024) / sigma_eff
        # Probability of IO exceeding upper limit under cosmological likelihood
        io_disfavored_cl = (sum_io - 0.0) / sigma_eff

        # DESI + ACT bound: sum m_nu < 0.064 eV
        no_margin_desi_act = SUM_M_NU_BOUND_DESI_ACT - sum_no
        no_margin_desi = SUM_M_NU_BOUND_DESI2024 - sum_no

        return {
            "sum_m_nu_no_floor_ev": sum_no,
            "sum_m_nu_io_floor_ev": sum_io,
            "desi_2024_upper_limit_ev": SUM_M_NU_BOUND_DESI2024,
            "desi_act_upper_limit_ev": SUM_M_NU_BOUND_DESI_ACT,
            "is_inverted_ordering_disfavored_at_95CL": sum_io > SUM_M_NU_BOUND_DESI2024,
            "inverted_ordering_tension_sigma": round(io_disfavored_cl, 2),
            "normal_ordering_headroom_desi2024_ev": round(no_margin_desi, 4),
            "normal_ordering_headroom_desi_act_ev": round(no_margin_desi_act, 4),
            "normal_ordering_near_threshold_squeeze": no_margin_desi_act < 0.010
        }

    @classmethod
    def evaluate_arbitration_hypotheses(cls) -> List[Dict[str, Any]]:
        """
        Returns competitive hypotheses explaining why cosmological sum m_nu appears lower
        than expected or tightly squeezed against the physical floor.
        """
        return [
            {
                "hypothesis_id": "H1_DYNAMICAL_DE_COMPENSATION",
                "mechanism": "Dynamical dark energy (w0 > -1, wa < 0 as suggested by DESI 2024) increases early growth, canceling out the neutrino free-streaming suppression Delta P(k)/P(k) and widening the allowable sum m_nu range back to ~0.15 eV.",
                "discriminating_observable": "Joint DESI Year 3 BAO + Euclid cosmic shear tomography testing w(z) evolution against constant w = -1.",
                "falsification_condition": "If Euclid + DESI confirm w0 = -1.00 +- 0.02 and wa = 0.0 +- 0.05, H1 is decisively falsified."
            },
            {
                "hypothesis_id": "H2_DECAYING_NEUTRINOS_OR_NSI",
                "mechanism": "Neutrinos possess non-standard interactions (NSI) or undergo late decay into sterile/dark radiation states before z ~ 5 (nu_heavy -> nu_light + phi), preventing standard free-streaming suppression at late times.",
                "discriminating_observable": "CMB spectral distortions (PIXIE class) and absence of the non-relativistic neutrino free-streaming signature in high-z Lyman-alpha forest.",
                "falsification_condition": "Detection of standard free-streaming phase shift in CMB lensing and Lyman-alpha P(k) consistent with stable SM fermions."
            },
            {
                "hypothesis_id": "H3_LENSING_SYSTEMATICS_OR_A_L_ANOMALY",
                "mechanism": "An unmodeled systematic in Planck / ACT CMB lensing normalization (or the persistent A_L > 1 phenomenological tension) artificially drives cosmological sum m_nu downwards.",
                "discriminating_observable": "Cross-correlation of CMB-S4 lensing with Vera C. Rubin (LSST) galaxy shear without relying on Planck internal lensing.",
                "falsification_condition": "CMB-S4 + LSST cross-correlation yielding A_L = 1.000 +- 0.005 with identical sum m_nu limits rules out instrumental/modeling systematics."
            }
        ]


def run_full_neutrino_cosmogenesis_audit() -> Dict[str, Any]:
    """Executes the full diagnostic suite and returns comprehensive quantitative results."""
    floors = NeutrinoMassOscillationModel.get_physical_floors()
    m1_no, m2_no, m3_no, sum_no = NeutrinoMassOscillationModel.compute_masses_normal_ordering(0.0)
    m1_io, m2_io, m3_io, sum_io = NeutrinoMassOscillationModel.compute_masses_inverted_ordering(0.0)

    t_nu_k = RelicNeutrinoCosmologyEngine.compute_neutrino_temperature_today()
    omega_nu_no = RelicNeutrinoCosmologyEngine.compute_omega_nu_h2(sum_no)
    z_nr_m3_no = RelicNeutrinoCosmologyEngine.compute_non_relativistic_redshift(m3_no)
    k_nr_m3_no = RelicNeutrinoCosmologyEngine.compute_free_streaming_wavenumber_nr(m3_no)
    p_supp_no = RelicNeutrinoCosmologyEngine.compute_matter_power_suppression(sum_no)

    tension = CosmologicalNeutrinoTensionAuditor.evaluate_ordering_viability()
    hypotheses = CosmologicalNeutrinoTensionAuditor.evaluate_arbitration_hypotheses()

    return {
        "neutrino_temperature_today_K": round(t_nu_k, 5),
        "normal_ordering_spectrum": {
            "m1_ev": round(m1_no, 6),
            "m2_ev": round(m2_no, 6),
            "m3_ev": round(m3_no, 6),
            "sum_m_ev": round(sum_no, 5),
            "omega_nu_h2": round(omega_nu_no, 6),
            "z_nr_heaviest": round(z_nr_m3_no, 2),
            "k_nr_heaviest_h_mpc": round(k_nr_m3_no, 5),
            "power_suppression_pct": round(p_supp_no * 100.0, 2)
        },
        "inverted_ordering_spectrum": {
            "m1_ev": round(m1_io, 6),
            "m2_ev": round(m2_io, 6),
            "m3_ev": round(m3_io, 6),
            "sum_m_ev": round(sum_io, 5)
        },
        "tension_audit": tension,
        "arbitration_hypotheses": hypotheses
    }


if __name__ == "__main__":
    audit = run_full_neutrino_cosmogenesis_audit()
    print("=== NEUTRINO MASS AND COSMOGENESIS AUDIT ===")
    print(f"T_nu,0: {audit['neutrino_temperature_today_K']} K")
    print(f"Normal Ordering Minimum Sum: {audit['normal_ordering_spectrum']['sum_m_ev']} eV")
    print(f"Inverted Ordering Minimum Sum: {audit['inverted_ordering_spectrum']['sum_m_ev']} eV")
    print(f"DESI 2024 Bound: {audit['tension_audit']['desi_2024_upper_limit_ev']} eV")
    print(f"Is Inverted Ordering Disfavored at 95% CL: {audit['tension_audit']['is_inverted_ordering_disfavored_at_95CL']}")
    print(f"Inverted Ordering Exclusion Significance: {audit['tension_audit']['inverted_ordering_tension_sigma']} sigma")
    print(f"Normal Ordering Headroom (DESI+ACT): {audit['tension_audit']['normal_ordering_headroom_desi_act_ev']} eV")
    print(f"Power Spectrum Suppression (NO min): {audit['normal_ordering_spectrum']['power_suppression_pct']}%")
