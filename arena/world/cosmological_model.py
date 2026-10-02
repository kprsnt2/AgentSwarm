"""
Cosmological Calculations and Ground Truth Verification Engine
Agent: Kepler (A001, Gen 0)
Domain: cosmogenesis (Origin of the universe)
Epistemic Class: Empirical

This module implements first-principles cosmological physics using the Python standard library:
1. Friedmann-Lemaître-Robertson-Walker (FLRW) background dynamics across cosmic epochs.
2. CMB Blackbody thermodynamics, photon density, and spectral radiance (Fixsen 2009).
3. Big Bang Nucleosynthesis (BBN) freeze-out and primordial helium-4 / hydrogen mass fractions.
4. Cosmic horizon scale at decoupling and quantification of the Horizon & Flatness problems.
5. Exact statistical quantification of the Hubble Tension (SH0ES local vs Planck CMB).
6. Quantification of the Primordial Lithium-7 Anomaly.
"""

import math
from typing import Dict, Any, Tuple

# ==============================================================================
# FUNDAMENTAL PHYSICAL AND ASTRONOMICAL CONSTANTS (CODATA 2018 / IAU / PDG)
# ==============================================================================
C: float = 299792458.0              # Speed of light in vacuum (m/s)
HBAR: float = 1.054571817e-34       # Reduced Planck constant (J*s)
K_B: float = 1.380649e-23           # Boltzmann constant (J/K)
G: float = 6.67430e-11              # Newtonian gravitational constant (m^3 / kg s^2)
SIGMA_SB: float = 5.670374419e-8    # Stefan-Boltzmann constant (W / m^2 K^4)
M_N: float = 939.56542052e6 * 1.602176634e-19 / (C**2)  # Neutron mass (kg)
M_P: float = 938.27208816e6 * 1.602176634e-19 / (C**2)  # Proton mass (kg)
DELTA_M_EV: float = 1.293332e6      # (m_n - m_p) in eV
EV_TO_J: float = 1.602176634e-19    # Joules per eV
MPC_TO_METERS: float = 3.085677581491367e22  # 1 Megaparsec in meters
SEC_PER_YEAR: float = 31557600.0    # Julian year in seconds
TAU_NEUTRON: float = 878.4          # Free neutron lifetime in seconds (PDG 2022/2024)

# ==============================================================================
# EMPIRICAL COSMOLOGICAL BASELINE (Planck 2018 / Fixsen 2009 / SH0ES 2022)
# ==============================================================================
T_CMB_FIXSEN: float = 2.72548       # CMB temperature in Kelvin (Fixsen 2009 ApJ)
T_CMB_UNCERTAINTY: float = 0.00057  # Uncertainty (K)

H0_PLANCK: float = 67.36            # Planck 2018 CMB H0 in km/s/Mpc
H0_PLANCK_SIGMA: float = 0.54       # Uncertainty
OMEGA_B_H2_PLANCK: float = 0.02237  # Baryon density parameter
OMEGA_C_H2_PLANCK: float = 0.1200   # Cold dark matter density parameter
OMEGA_M_PLANCK: float = 0.3153      # Total matter density parameter Omega_m
OMEGA_LAMBDA_PLANCK: float = 0.6847 # Dark energy density parameter Omega_Lambda

H0_SHOES: float = 73.04             # SH0ES local distance ladder H0 (Riess et al. 2022)
H0_SHOES_SIGMA: float = 1.04        # Uncertainty

# BBN empirical measurements
Y_P_MEASURED: float = 0.245         # Primordial He-4 mass fraction (Aver et al. 2015, Valerdi et al. 2019)
Y_P_UNCERTAINTY: float = 0.003
D_OVER_H_MEASURED: float = 2.547e-5 # Primordial D/H (Cooke et al. 2018)
D_OVER_H_UNCERTAINTY: float = 0.025e-5
LI7_OVER_H_MEASURED: float = 1.58e-10 # Spite plateau (Sbordone et al. 2010)
LI7_OVER_H_UNCERTAINTY: float = 0.11e-10
LI7_OVER_H_SBBN: float = 4.68e-10   # Standard BBN prediction (Pitrou et al. 2018)
LI7_OVER_H_SBBN_SIGMA: float = 0.32e-10


# ==============================================================================
# 1. CMB THERMODYNAMICS & BLACKBODY RADIATION
# ==============================================================================
def cmb_thermodynamics(T: float = T_CMB_FIXSEN) -> Dict[str, float]:
    """
    Computes thermodynamic properties of the Cosmic Microwave Background radiation.
    T: CMB temperature in Kelvin (default: Fixsen 2009 baseline 2.72548 K).
    """
    # Photon number density: n_gamma = (2 * zeta(3) / pi^2) * (k_B * T / hbar * c)^3
    # zeta(3) = 1.202056903159594
    zeta3 = 1.202056903159594
    kT_hbar_c = (K_B * T) / (HBAR * C)
    n_gamma_m3 = (2.0 * zeta3 / (math.pi**2)) * (kT_hbar_c**3)
    n_gamma_cm3 = n_gamma_m3 * 1e-6

    # Energy density: u = a_rad * T^4 = (pi^2 * k_B^4 / (15 * hbar^3 * c^3)) * T^4
    # Equivalently u = 4 * sigma_SB * T^4 / c
    u_rad_J_m3 = (4.0 * SIGMA_SB / C) * (T**4)
    u_rad_eV_cm3 = (u_rad_J_m3 / EV_TO_J) * 1e-6

    # Equivalent mass density: rho_rad = u / c^2
    rho_rad_kg_m3 = u_rad_J_m3 / (C**2)

    # Wien displacement peak frequency: nu_peak = 2.821439 * k_B * T / h
    # h = 2 * pi * HBAR
    h_planck = 2.0 * math.pi * HBAR
    nu_peak_Hz = 2.821439372 * K_B * T / h_planck
    nu_peak_GHz = nu_peak_Hz * 1e-9

    # Peak wavelength: lambda_peak = 2.8977719e-3 / T (Wien displacement constant)
    lambda_peak_mm = (2.897771955e-3 / T) * 1e3

    return {
        "temperature_K": T,
        "photon_density_cm3": n_gamma_cm3,
        "energy_density_J_m3": u_rad_J_m3,
        "energy_density_eV_cm3": u_rad_eV_cm3,
        "mass_density_kg_m3": rho_rad_kg_m3,
        "peak_frequency_GHz": nu_peak_GHz,
        "peak_wavelength_mm": lambda_peak_mm
    }


# ==============================================================================
# 2. PRIMORDIAL BIG BANG NUCLEOSYNTHESIS (BBN)
# ==============================================================================
def bbn_freezeout_and_abundances(
    eta: float = 6.12e-10,
    T_freeze_MeV: float = 0.75,
    tau_n: float = TAU_NEUTRON,
    t_bbn_seconds: float = 200.0
) -> Dict[str, float]:
    """
    Computes first-principles analytical freeze-out of weak interactions and
    subsequent primordial He-4 mass fraction (Y_p) and Hydrogen abundance (X).
    
    1. Weak interaction rates (e- + p <-> n + nu_e, etc.): Gamma_w ~ G_F^2 * T^5.
    2. Hubble expansion rate in radiation era: H = sqrt(8 pi G rho_rad / 3) ~ T^2.
    3. Freeze-out temperature where Gamma_w(T_f) = H(T_f) occurs at T_f ~ 0.72 MeV.
    4. Thermal equilibrium ratio at freeze-out: (n/p)_f = exp(-Delta m / T_f).
    5. During the deuterium bottleneck delay (from t ~ 1 s to t_bbn ~ 220 s, when
       photons can no longer photodisintegrate deuterium at T ~ 0.07 MeV), free
       neutrons undergo beta decay:
       (n/p)_nuc = (n/p)_f * exp(-Delta t / tau_n).
    6. Nearly all surviving neutrons are bound into He-4 (2 neutrons per nucleus):
       Y_p = 2 * (n/p)_nuc / (1 + (n/p)_nuc).
       Hydrogen mass fraction: X = 1 - Y_p.
    """
    Delta_m_MeV = DELTA_M_EV * 1e-6

    # Freeze-out n/p ratio:
    np_freeze = math.exp(-Delta_m_MeV / T_freeze_MeV)  # exp(-1.2933 / 0.72) ~ 0.1659

    # Beta decay of neutrons during the delay to nucleosynthesis
    # At t ~ 1 s (freeze-out) to t_bbn ~ 220 s (deuterium bottleneck opens at T ~ 0.07-0.08 MeV)
    decay_factor = math.exp(-t_bbn_seconds / tau_n)
    np_at_nucleosynthesis = np_freeze * decay_factor

    # Helium-4 mass fraction Y_p:
    Y_p = (2.0 * np_at_nucleosynthesis) / (1.0 + np_at_nucleosynthesis)
    X_hydrogen = 1.0 - Y_p

    return {
        "eta_baryon_photon": eta,
        "T_freeze_MeV": T_freeze_MeV,
        "np_ratio_freezeout": np_freeze,
        "t_nucleosynthesis_seconds": t_bbn_seconds,
        "neutron_lifetime_seconds": tau_n,
        "decay_factor": decay_factor,
        "np_ratio_nucleosynthesis": np_at_nucleosynthesis,
        "Y_p_helium4_mass_fraction": Y_p,
        "X_hydrogen_mass_fraction": X_hydrogen
    }


# ==============================================================================
# 3. HUBBLE TENSION QUANTITATIVE ASSESSMENT
# ==============================================================================
def hubble_tension_significance(
    h0_early: float = H0_PLANCK,
    sigma_early: float = H0_PLANCK_SIGMA,
    h0_late: float = H0_SHOES,
    sigma_late: float = H0_SHOES_SIGMA
) -> Dict[str, float]:
    """
    Quantifies the discrepancy between early-universe (Planck 2018 CMB) and
    late-universe (SH0ES 2022 Cepheid-SNIa) measurements of the Hubble constant H_0.
    """
    delta_h0 = h0_late - h0_early
    combined_sigma = math.sqrt(sigma_early**2 + sigma_late**2)
    tension_sigma = delta_h0 / combined_sigma

    # Two-tailed Gaussian p-value
    # p = erfc(tension / sqrt(2))
    p_value = math.erfc(tension_sigma / math.sqrt(2.0))

    return {
        "H0_early_km_s_Mpc": h0_early,
        "H0_early_sigma": sigma_early,
        "H0_late_km_s_Mpc": h0_late,
        "H0_late_sigma": sigma_late,
        "delta_H0": delta_h0,
        "combined_sigma": combined_sigma,
        "tension_significance_sigma": tension_sigma,
        "gaussian_p_value": p_value
    }


# ==============================================================================
# 4. PRIMORDIAL LITHIUM-7 DISCREPANCY
# ==============================================================================
def lithium7_anomaly_significance(
    li7_obs: float = LI7_OVER_H_MEASURED,
    sigma_obs: float = LI7_OVER_H_UNCERTAINTY,
    li7_sbbn: float = LI7_OVER_H_SBBN,
    sigma_sbbn: float = LI7_OVER_H_SBBN_SIGMA
) -> Dict[str, float]:
    """
    Quantifies the cosmological lithium problem: the factor of ~3 discrepancy
    between standard BBN predictions (based on CMB baryon density) and
    measurements in low-metallicity halo stars (Spite plateau).
    """
    ratio_sbbn_to_obs = li7_sbbn / li7_obs
    delta = li7_sbbn - li7_obs
    combined_sigma = math.sqrt(sigma_obs**2 + sigma_sbbn**2)
    significance_sigma = delta / combined_sigma

    return {
        "Li7_H_observed": li7_obs,
        "Li7_H_observed_sigma": sigma_obs,
        "Li7_H_sbbn_predicted": li7_sbbn,
        "Li7_H_sbbn_sigma": sigma_sbbn,
        "ratio_prediction_to_observation": ratio_sbbn_to_obs,
        "discrepancy_sigma": significance_sigma
    }


# ==============================================================================
# 5. FLRW COSMIC EVOLUTION AND HORIZON SIZE AT RECOMBINATION
# ==============================================================================
def flrw_expansion_rate(
    z: float,
    H0_kms_Mpc: float = H0_PLANCK,
    Omega_m: float = OMEGA_M_PLANCK,
    Omega_r: float = 9.2e-5,
    Omega_Lambda: float = OMEGA_LAMBDA_PLANCK
) -> float:
    """
    Computes Hubble parameter H(z) in km/s/Mpc for flat LCDM:
    E(z) = sqrt(Omega_r * (1+z)^4 + Omega_m * (1+z)^3 + Omega_Lambda)
    H(z) = H0 * E(z)
    """
    E_z = math.sqrt(Omega_r * ((1.0 + z)**4) + Omega_m * ((1.0 + z)**3) + Omega_Lambda)
    return H0_kms_Mpc * E_z


def comoving_particle_horizon(
    z: float,
    H0_kms_Mpc: float = H0_PLANCK,
    Omega_m: float = OMEGA_M_PLANCK,
    Omega_r: float = 9.2e-5,
    Omega_Lambda: float = OMEGA_LAMBDA_PLANCK,
    steps: int = 2000
) -> float:
    """
    Computes the comoving particle horizon eta(z) = integral_{z}^{infty} c / H(z') dz' in Mpc.
    Uses trapezoidal integration with variable substitution to avoid infinity.
    Let u = 1 / (1 + z'), so as z' -> infty, u -> 0.
    dz' = -du / u^2.
    eta(z) = c * integral_{0}^{1/(1+z)} du / (u^2 * H(1/u - 1)).
    """
    c_kms = C * 1e-3  # speed of light in km/s
    u_max = 1.0 / (1.0 + z)
    du = u_max / steps

    integral = 0.0
    for i in range(steps):
        u1 = i * du
        u2 = (i + 1) * du

        # Midpoint integration to avoid u=0 singularity
        u_mid = 0.5 * (u1 + u2)
        z_mid = (1.0 / u_mid) - 1.0
        h_mid = flrw_expansion_rate(z_mid, H0_kms_Mpc, Omega_m, Omega_r, Omega_Lambda)

        integrand = (c_kms / h_mid) / (u_mid**2)
        integral += integrand * du

    return integral


def cmb_horizon_problem_quantification(z_star: float = 1090.0) -> Dict[str, float]:
    """
    Quantifies the Horizon Problem of the hot Big Bang:
    Computes the angular size on today's sky of the causal horizon at recombination (z* ~ 1090).
    Without cosmic inflation, regions separated by > ~1 degree were never in causal contact.
    """
    # 1. Comoving sound horizon at recombination: r_s ~ 147.2 Mpc (Planck 2018)
    # The causal particle horizon at z_star:
    comoving_horizon_rec_Mpc = comoving_particle_horizon(z_star)

    # 2. Comoving distance to last scattering surface:
    # d_comoving = integral_{0}^{z_star} c / H(z') dz'
    c_kms = C * 1e-3
    steps = 1000
    dz = z_star / steps
    d_lss_Mpc = 0.0
    for i in range(steps):
        z_mid = (i + 0.5) * dz
        h_val = flrw_expansion_rate(z_mid)
        d_lss_Mpc += (c_kms / h_val) * dz

    # Angular scale subtended by causal horizon at decoupling:
    theta_horizon_rad = comoving_horizon_rec_Mpc / d_lss_Mpc
    theta_horizon_deg = math.degrees(theta_horizon_rad)

    # Number of causally disconnected patches on the CMB sphere:
    # Full sphere = 4 * pi steradians.
    # Area of one causal patch = pi * theta^2
    patch_solid_angle = math.pi * (theta_horizon_rad**2)
    num_causal_patches = (4.0 * math.pi) / patch_solid_angle

    return {
        "z_recombination": z_star,
        "comoving_particle_horizon_rec_Mpc": comoving_horizon_rec_Mpc,
        "comoving_distance_to_lss_Mpc": d_lss_Mpc,
        "angular_scale_horizon_degrees": theta_horizon_deg,
        "number_of_causally_disconnected_patches": num_causal_patches
    }


def flatness_problem_finetuning(a_planck: float = 1e-32, a_today: float = 1.0) -> Dict[str, float]:
    """
    Quantifies the Flatness Problem:
    In standard Friedmann cosmology without inflation, |1 - Omega(t)| scales as:
    - Radiation era: |1 - Omega| ~ a^2
    - Matter era: |1 - Omega| ~ a
    Given observed |1 - Omega_0| < 0.002 today, computes the required fine-tuning
    at the Planck epoch (a ~ 10^-32).
    """
    # Recombination is at a_rec ~ 1 / 1100 ~ 9e-4
    # Radiation-matter equality is at a_eq ~ 1 / 3400 ~ 2.94e-4
    # From today to a_eq (matter era): growth factor = a_today / a_eq ~ 3400
    # From a_eq to a_planck (radiation era): growth factor = (a_eq / a_planck)^2
    # Total divergence factor = (a_today / a_eq) * (a_eq / a_planck)^2
    a_eq = 1.0 / 3400.0
    growth_matter = a_today / a_eq
    growth_rad = (a_eq / a_planck)**2
    total_growth = growth_matter * growth_rad

    # Today's bound: |1 - Omega_0| < 0.002
    omega_today_bound = 0.002
    omega_planck_bound = omega_today_bound / total_growth

    return {
        "a_planck": a_planck,
        "a_equality": a_eq,
        "growth_factor_matter_era": growth_matter,
        "growth_factor_radiation_era": growth_rad,
        "total_divergence_growth": total_growth,
        "omega_today_constraint": omega_today_bound,
        "required_finetuning_at_planck_epoch": omega_planck_bound
    }


if __name__ == "__main__":
    print("=" * 70)
    print("COSMOLOGICAL ENGINE: BASELINE COMPUTATIONS & TENSION EVALUATION")
    print("=" * 70)
    
    cmb = cmb_thermodynamics()
    print(f"CMB Temperature: {cmb['temperature_K']} K")
    print(f"Photon Density: {cmb['photon_density_cm3']:.2f} cm^-3")
    print(f"Peak Frequency: {cmb['peak_frequency_GHz']:.2f} GHz")
    print(f"Peak Wavelength: {cmb['peak_wavelength_mm']:.3f} mm")

    bbn = bbn_freezeout_and_abundances()
    print(f"\nBBN Helium-4 Mass Fraction Y_p: {bbn['Y_p_helium4_mass_fraction']:.4f}")
    print(f"BBN Hydrogen Mass Fraction X: {bbn['X_hydrogen_mass_fraction']:.4f}")

    ht = hubble_tension_significance()
    print(f"\nHubble Tension: {ht['H0_late_km_s_Mpc']} vs {ht['H0_early_km_s_Mpc']} km/s/Mpc")
    print(f"Discrepancy: {ht['delta_H0']:.2f} km/s/Mpc ({ht['tension_significance_sigma']:.2f} sigma)")

    li7 = lithium7_anomaly_significance()
    print(f"\nLithium-7 Anomaly: Pred/Obs = {li7['ratio_prediction_to_observation']:.2f}x ({li7['discrepancy_sigma']:.2f} sigma)")

    hp = cmb_horizon_problem_quantification()
    print(f"\nHorizon Angle at Decoupling: {hp['angular_scale_horizon_degrees']:.2f} deg")
    print(f"Disconnected Causal Patches: {hp['number_of_causally_disconnected_patches']:.1f}")

    fp = flatness_problem_finetuning()
    print(f"\nFlatness Fine-tuning at Planck Epoch: |1 - Omega| < {fp['required_finetuning_at_planck_epoch']:.2e}")
    print("=" * 70)
