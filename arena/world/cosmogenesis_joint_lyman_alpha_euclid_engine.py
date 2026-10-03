"""
Cosmogenesis Joint Lyman-Alpha and Euclid Neutrino Mass Deficit Arbitration Engine

Quantitative synthesis combining high-redshift Lyman-alpha forest 1D power spectra P_F(k, z)
and Euclid cosmic shear tomography C_ell^{kappa, kappa}(z_i, z_j) to decisively break the
degeneracy between:
  1. Hypothesis A (H_A): DESI Dynamical Dark Energy (w0 > -1, wa < 0)
  2. Hypothesis B (H_B): Decaying Relic Neutrinos (nu_3 -> dark radiation)
"""

import math
from typing import Dict, List, Tuple, Any

# =====================================================================
# Physical & Cosmological Constants (Planck 2018 / DESI 2024 Baseline)
# =====================================================================
H0_BASELINE = 67.4                    # km/s/Mpc
H_PARAM = H0_BASELINE / 100.0         # h = 0.674
OMEGA_M_0 = 0.315                     # Omega_m today
OMEGA_B_0 = 0.049                     # Omega_b today
OMEGA_C_0 = OMEGA_M_0 - OMEGA_B_0     # Omega_cdm today
OMEGA_LAMBDA_0 = 1.0 - OMEGA_M_0      # Flat universe Omega_DE today = 0.685
N_EFF_STANDARD = 3.044

# Neutrino Mass Splittings from Terrestrial Oscillation Experiments (PDG 2024 / NuFIT 5.2)
DELTA_M21_SQ = 7.53e-5                # eV^2 (solar)
DELTA_M31_SQ_NO = 2.453e-3            # eV^2 (atmospheric, Normal Ordering)
DELTA_M32_SQ_IO = -2.450e-3           # eV^2 (atmospheric, Inverted Ordering)

# Minimal Mass Sums
SUM_M_NU_NO_MIN_EV = math.sqrt(DELTA_M21_SQ) + math.sqrt(DELTA_M31_SQ_NO)  # ~0.05821 eV
SUM_M_NU_IO_MIN_EV = math.sqrt(abs(DELTA_M32_SQ_IO)) + math.sqrt(abs(DELTA_M32_SQ_IO) - DELTA_M21_SQ)  # ~0.09823 eV

# Cosmological Upper Bounds (95% CL)
BOUND_LAMBDA_CDM_DESI_PLANCK = 0.072   # eV (flat Lambda-CDM)
BOUND_LAMBDA_CDM_DESI_ACT = 0.064      # eV (tightest cosmological bound)
BOUND_W0WA_CDM_DESI_PLANCK = 0.165     # eV (DESI + Planck with dynamical DE)

# DESI 2024 + CMB + SNe Best-fit CPL Parameters
W0_DESI = -0.827
WA_DESI = -0.750
SIGMA_W0_DESI = 0.063
SIGMA_WA_DESI = 0.350

# Survey Capabilities
EUCLID_SKY_FRACTION = 0.36            # 15,000 sq deg
EUCLID_GALAXY_DENSITY = 30.0          # arcmin^-2
EUCLID_SIGMA_W0 = 0.018               # Marginalized 1-sigma uncertainty on w0
EUCLID_SIGMA_WA = 0.075               # Marginalized 1-sigma uncertainty on wa
LYMAN_ALPHA_SIGMA_SUPPRESSION = 0.0040 # 0.40% precision on Delta P/P at z=3.0


class CosmologicalBackgroundEngine:
    """Computes background expansion and dark energy fractions across redshift."""

    @staticmethod
    def dark_energy_density_ratio(z: float, w0: float = W0_DESI, wa: float = WA_DESI) -> float:
        """
        Computes rho_DE(z) / rho_DE(0) for CPL parametrization:
        rho_DE(a) = rho_DE(0) * a^(-3(1 + w0 + wa)) * exp(-3 * wa * (1 - a))
        """
        a = 1.0 / (1.0 + z)
        exponent = -3.0 * (1.0 + w0 + wa)
        exp_factor = math.exp(-3.0 * wa * (1.0 - a))
        return (a ** exponent) * exp_factor

    @classmethod
    def hubble_parameter(cls, z: float, w0: float = W0_DESI, wa: float = WA_DESI) -> float:
        """Computes H(z) in km/s/Mpc for flat w0-wa-CDM."""
        rho_m = OMEGA_M_0 * ((1.0 + z) ** 3)
        rho_de = OMEGA_LAMBDA_0 * cls.dark_energy_density_ratio(z, w0, wa)
        return H0_BASELINE * math.sqrt(rho_m + rho_de)

    @classmethod
    def dark_energy_fraction(cls, z: float, w0: float = W0_DESI, wa: float = WA_DESI) -> float:
        """Returns Omega_DE(z) = rho_DE(z) / rho_crit(z)."""
        rho_m = OMEGA_M_0 * ((1.0 + z) ** 3)
        rho_de = OMEGA_LAMBDA_0 * cls.dark_energy_density_ratio(z, w0, wa)
        return rho_de / (rho_m + rho_de)


class MatterPowerSuppressionEngine:
    """Computes linear and non-linear matter power spectrum suppression Delta P/P."""

    @staticmethod
    def neutrino_fraction(sum_m_nu_ev: float) -> float:
        """
        Calculates neutrino fraction f_nu = Omega_nu / Omega_m.
        Omega_nu = sum(m_nu) / (93.14 * h^2).
        """
        omega_nu = sum_m_nu_ev / (93.14 * (H_PARAM ** 2))
        return omega_nu / OMEGA_M_0

    @classmethod
    def linear_power_suppression(cls, sum_m_nu_ev: float) -> float:
        """
        Computes Hu-Eisenstein / Lesgourgues-Pastor linear power suppression:
        Delta P(k) / P(k) = -8 * f_nu (for k >> k_nr).
        """
        f_nu = cls.neutrino_fraction(sum_m_nu_ev)
        return -8.0 * f_nu

    @classmethod
    def decaying_neutrino_suppression(cls, z: float, z_decay: float = 3.2,
                                     ordering: str = "NO") -> Dict[str, float]:
        """
        Evaluates power spectrum suppression under decaying relic neutrinos:
        nu_3 -> nu_1 + phi_DR.
        Before decay (z > z_decay): nu_3 is non-relativistic matter (m3 ~ 0.050 eV).
        After decay (z < z_decay): daughter phi is massless radiation, rest mass is lost from clustering.
        """
        if ordering == "NO":
            m1 = 0.0
            m2 = math.sqrt(DELTA_M21_SQ)
            m3 = math.sqrt(DELTA_M31_SQ_NO)
            sum_pre = m1 + m2 + m3
            sum_post = m1 + m2  # only m2 remains non-relativistic matter
        else:
            m3 = 0.0
            m2 = math.sqrt(abs(DELTA_M32_SQ_IO))
            m1 = math.sqrt(abs(DELTA_M32_SQ_IO) - DELTA_M21_SQ)
            sum_pre = m1 + m2 + m3
            sum_post = 0.0  # both degenerate heavy states decay in full IO decay

        f_nu_pre = cls.neutrino_fraction(sum_pre)
        f_nu_post = cls.neutrino_fraction(sum_post)

        suppression_pre = -8.0 * f_nu_pre
        suppression_post = -8.0 * f_nu_post

        # Suppression at observed redshift z
        if z >= z_decay:
            active_suppression = suppression_pre
            apparent_mass = sum_pre
        else:
            active_suppression = suppression_post
            apparent_mass = sum_post

        erasure_pct = (1.0 - (suppression_post / suppression_pre)) * 100.0 if suppression_pre != 0 else 0.0

        return {
            "redshift": z,
            "z_decay": z_decay,
            "ordering": ordering,
            "sum_m_nu_pre_decay_ev": sum_pre,
            "sum_m_nu_post_decay_ev": sum_post,
            "apparent_mass_ev": apparent_mass,
            "active_suppression_pct": active_suppression * 100.0,
            "suppression_pre_decay_pct": suppression_pre * 100.0,
            "suppression_post_decay_pct": suppression_post * 100.0,
            "erasure_efficiency_pct": erasure_pct
        }


class JointFalsificationArbitrator:
    """
    Jointly evaluates High-z Lyman-alpha P_F(k, z) and Euclid Cosmic Shear Tomography
    to formulate decisive arbitration metrics.
    """

    @classmethod
    def compute_tomographic_trace(cls, redshifts: List[float], z_decay: float = 3.2) -> List[Dict[str, Any]]:
        """
        Traces dark energy fraction, dynamical DE suppression, and decaying neutrino suppression
        across a redshift ladder spanning Euclid (z ~ 0.2 - 2.0) and Lyman-alpha (z ~ 2.2 - 4.0).
        """
        trace = []
        for z in redshifts:
            omega_de = CosmologicalBackgroundEngine.dark_energy_fraction(z, W0_DESI, WA_DESI)
            
            # Hypothesis A: Dynamical DE (physical mass = 0.060 eV, standard stable)
            supp_h_a = MatterPowerSuppressionEngine.linear_power_suppression(SUM_M_NU_NO_MIN_EV) * 100.0
            
            # Hypothesis B: Decaying Neutrinos (z_decay = 3.2, stable Lambda-CDM background w=-1)
            decay_res = MatterPowerSuppressionEngine.decaying_neutrino_suppression(z, z_decay=z_decay, ordering="NO")
            supp_h_b = decay_res["active_suppression_pct"]
            
            # Discriminant delta: |supp_h_a - supp_h_b|
            discriminant = abs(supp_h_a - supp_h_b)
            
            # Primary observational probe for this redshift bin
            if z <= 0.8:
                probe = "Euclid Cosmic Shear Bin 1-4 (z < 0.8)"
            elif z <= 2.0:
                probe = "Euclid Cosmic Shear Bin 5-10 + Roman SNe (0.8 <= z <= 2.0)"
            elif z <= 3.2:
                probe = "DESI / WEAVE Lyman-alpha Forest 1D Power (Post-decay Window)"
            else:
                probe = "High-z Lyman-alpha Forest / Quasar Absorption (Pre-decay Window)"

            trace.append({
                "redshift_z": z,
                "omega_de_pct": round(omega_de * 100.0, 2),
                "h_a_dynamical_de_suppression_pct": round(supp_h_a, 3),
                "h_b_decaying_nu_suppression_pct": round(supp_h_b, 3),
                "discriminant_delta_pct": round(discriminant, 3),
                "primary_probe": probe
            })
        return trace

    @classmethod
    def compute_joint_fisher_separation(cls) -> Dict[str, Any]:
        """
        Computes 2D Fisher Information separation between Hypothesis A and Hypothesis B
        in the joint parameter space [w0, Delta P/P(z=3.0)].
        """
        # Coordinate for H_A (Dynamical DE): w0 = -0.827, Delta P/P(z=3) = -3.55%
        w0_ha = W0_DESI
        supp_z3_ha = MatterPowerSuppressionEngine.linear_power_suppression(SUM_M_NU_NO_MIN_EV) * 100.0
        
        # Coordinate for H_B (Decaying Neutrinos): w0 = -1.000, Delta P/P(z=3) = -0.52% (assuming z_dec > 3.0)
        w0_hb = -1.000
        decay_post = MatterPowerSuppressionEngine.decaying_neutrino_suppression(3.0, z_decay=3.5, ordering="NO")
        supp_z3_hb = decay_post["active_suppression_pct"]

        # Marginalized 1-sigma uncertainties
        sigma_w0_euclid = EUCLID_SIGMA_W0
        sigma_supp_lyman = LYMAN_ALPHA_SIGMA_SUPPRESSION * 100.0  # 0.40%

        # Orthogonal Chi-Square Distance
        delta_w0 = w0_ha - w0_hb
        chi2_w0 = (delta_w0 / sigma_w0_euclid) ** 2
        
        delta_supp = supp_z3_ha - supp_z3_hb
        chi2_supp = (delta_supp / sigma_supp_lyman) ** 2
        
        total_chi2 = chi2_w0 + chi2_supp
        separation_sigma = math.sqrt(total_chi2)

        return {
            "h_a_coordinates": {"w0": w0_ha, "suppression_z3_pct": round(supp_z3_ha, 3)},
            "h_b_coordinates": {"w0": w0_hb, "suppression_z3_pct": round(supp_z3_hb, 3)},
            "measurement_uncertainties": {
                "euclid_sigma_w0": sigma_w0_euclid,
                "lyman_alpha_sigma_suppression_pct": round(sigma_supp_lyman, 3)
            },
            "chi2_components": {
                "chi2_euclid_w0": round(chi2_w0, 2),
                "chi2_lyman_suppression": round(chi2_supp, 2),
                "total_delta_chi2": round(total_chi2, 2)
            },
            "statistical_separation_sigma": round(separation_sigma, 2),
            "is_falsification_guaranteed_gt_5_sigma": separation_sigma > 5.0
        }

    @classmethod
    def evaluate_arbitration_decision(cls, measured_w0: float,
                                     measured_supp_z3_pct: float) -> Dict[str, Any]:
        """
        Applies decisive decision rules to classify an incoming joint measurement.
        """
        # Distance to H_A
        d_ha = math.sqrt(((measured_w0 - W0_DESI) / EUCLID_SIGMA_W0) ** 2 +
                         ((measured_supp_z3_pct - MatterPowerSuppressionEngine.linear_power_suppression(SUM_M_NU_NO_MIN_EV) * 100.0) /
                          (LYMAN_ALPHA_SIGMA_SUPPRESSION * 100.0)) ** 2)
        
        # Distance to H_B
        post_supp = MatterPowerSuppressionEngine.decaying_neutrino_suppression(3.0, z_decay=3.5, ordering="NO")["active_suppression_pct"]
        d_hb = math.sqrt(((measured_w0 - (-1.000)) / EUCLID_SIGMA_W0) ** 2 +
                         ((measured_supp_z3_pct - post_supp) / (LYMAN_ALPHA_SIGMA_SUPPRESSION * 100.0)) ** 2)

        if d_ha < 3.0 and d_hb > 5.0:
            verdict = "CONFIRMED: Dynamical Dark Energy (Hypothesis A). Decaying Neutrinos Falsified."
        elif d_hb < 3.0 and d_ha > 5.0:
            verdict = "CONFIRMED: Decaying Relic Neutrinos (Hypothesis B). Dynamical Dark Energy Falsified."
        elif d_ha > 5.0 and d_hb > 5.0:
            verdict = "ANOMALY: Both Hypotheses Falsified (New Physics Required, e.g. modified gravity or non-cold DM)."
        else:
            verdict = "INTERMEDIATE: Insufficient statistical tension to declare exclusive victory."

        return {
            "measured_w0": measured_w0,
            "measured_supp_z3_pct": measured_supp_z3_pct,
            "distance_to_h_a_sigma": round(d_ha, 2),
            "distance_to_h_b_sigma": round(d_hb, 2),
            "verdict": verdict
        }


def run_full_joint_falsification_suite() -> Dict[str, Any]:
    """Executes the complete joint Lyman-alpha + Euclid falsification analysis."""
    redshifts = [0.0, 0.5, 1.0, 1.8, 2.5, 3.0, 3.5, 4.2]
    tomography = JointFalsificationArbitrator.compute_tomographic_trace(redshifts, z_decay=3.2)
    fisher = JointFalsificationArbitrator.compute_joint_fisher_separation()
    
    # Test cases:
    test_ha = JointFalsificationArbitrator.evaluate_arbitration_decision(measured_w0=-0.830, measured_supp_z3_pct=-3.50)
    test_hb = JointFalsificationArbitrator.evaluate_arbitration_decision(measured_w0=-1.002, measured_supp_z3_pct=-0.55)

    return {
        "tomographic_trace": tomography,
        "fisher_separation": fisher,
        "test_case_h_a": test_ha,
        "test_case_h_b": test_hb
    }


if __name__ == "__main__":
    suite = run_full_joint_falsification_suite()
    print("=== JOINT FALSIFICATION AUDIT COMPLETED ===")
    print(f"Statistical Separation: {suite['fisher_separation']['statistical_separation_sigma']} sigma")
    print(f"Total Delta Chi2: {suite['fisher_separation']['chi2_components']['total_delta_chi2']}")
