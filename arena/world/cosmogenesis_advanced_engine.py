"""
Advanced Cosmogenesis Physics and Empirical Resolution Engine
Agent: Kepler (A001, Gen 0)
Domain: cosmogenesis (Origin of the universe)
Epistemic Class: Empirical

This module implements quantitative formulations for the advanced frontiers of cosmogenesis:
1. Reciprocal CMB Kinematics: GZK photo-pion threshold, mean free path, and rest-frame anchor.
2. Penrose Weyl Curvature Hypothesis & Cosmic Gravitational Entropy Budget.
3. Cosmological Inflation, Starobinsky R^2 model, and the Trans-Planckian Censorship Conjecture (TCC).
4. Sakharov Baryogenesis & Davidson-Ibarra Leptogenesis Bounds.
5. Sound Horizon rs Reduction, Early Dark Energy (EDE) constraints, and the H0-S8 tension trade-off.
6. Full Cosmic Entropy Inventory across epochs (Planck, Recombination, Present, de Sitter Horizon).
"""

import math
from typing import Dict, Any, List

# ==============================================================================
# FUNDAMENTAL CONSTANTS (CODATA 2018 / PDG 2022 / IAU)
# ==============================================================================
C: float = 299792458.0                    # Speed of light (m/s)
HBAR: float = 1.054571817e-34             # Reduced Planck constant (J*s)
K_B: float = 1.380649e-23                 # Boltzmann constant (J/K)
G: float = 6.67430e-11                    # Gravitational constant (m^3 / kg s^2)
EV_TO_J: float = 1.602176634e-19          # Joules per eV
MPC_TO_METERS: float = 3.085677581491367e22 # 1 Mpc in meters
M_SUN_KG: float = 1.98847e30              # Solar mass in kg

# Masses
M_PROTON_EV: float = 938.272088e6         # Proton mass in eV
M_PION_NEUTRAL_EV: float = 134.9768e6     # Neutral pion mass in eV
M_PION_CHARGED_EV: float = 139.57039e6    # Charged pion mass in eV
HIGGS_VEV_GEV: float = 174.0              # Electroweak VEV (v / sqrt(2) or v = 174 GeV)
PLANCK_MASS_GEV: float = 1.22091e19       # Planck mass M_P = sqrt(hbar*c / G) in GeV
REDUCED_PLANCK_MASS_GEV: float = 2.435e18 # M_pl = M_P / sqrt(8*pi) in GeV

# Cosmological parameters (Planck 2018 baseline)
T_CMB_K: float = 2.72548                  # CMB temperature (Fixsen 2009)
N_GAMMA_CM3: float = 410.7                # CMB photon density (cm^-3)
H0_PLANCK: float = 67.36                  # Planck CMB H0 (km/s/Mpc)
H0_SHOES: float = 73.04                   # SH0ES local H0 (km/s/Mpc)
OMEGA_M: float = 0.3153                   # Matter density parameter
OMEGA_B_H2: float = 0.02237               # Baryon physical density
OMEGA_C_H2: float = 0.1200                # Cold dark matter physical density
R_OBS_METERS: float = 4.4e26              # Radius of observable universe (~46.5 Gly = 14.3 Gpc)


# ==============================================================================
# 1. CMB KINEMATICS & GZK PHOTO-PION THRESHOLD
# ==============================================================================
def gzk_threshold_and_mean_free_path(
    T_cmb: float = T_CMB_K,
    sigma_p_gamma_microbarn: float = 200.0
) -> Dict[str, float]:
    """
    Computes the Greisen-Zatsepin-Kuzmin (GZK) photo-pion production threshold energy
    and interaction mean free path in the CMB photon bath:
    p + gamma_CMB -> Delta(1232)+ -> p + pi0 (or n + pi+)

    The threshold center-of-mass energy is s_th = (m_p + m_pi)^2.
    For head-on collision: 4 * E_p * epsilon_gamma >= m_pi * (2 * m_p + m_pi).
    Mean CMB photon energy: <epsilon> = 2.701178 * k_B * T.
    """
    k_B_eV_K = K_B / EV_TO_J
    mean_photon_energy_eV = 2.701178 * k_B_eV_K * T_cmb
    
    # Threshold condition
    numerator = M_PION_NEUTRAL_EV * (2.0 * M_PROTON_EV + M_PION_NEUTRAL_EV)
    E_threshold_mean_eV = numerator / (4.0 * mean_photon_energy_eV)

    # For photons in the Wien tail (e.g. 1.5 meV), threshold is lower (~5e19 eV)
    epsilon_tail_eV = 1.5e-3
    E_threshold_tail_eV = numerator / (4.0 * epsilon_tail_eV)

    # Photon number density n_gamma = 2 * zeta(3) / pi^2 * (k_B T / hbar c)^3
    # in m^-3
    zeta3 = 1.202056903159594
    kT_hbar_c = (K_B * T_cmb) / (HBAR * C)
    n_gamma_m3 = (2.0 * zeta3 / (math.pi**2)) * (kT_hbar_c**3)

    # Cross section: 1 barn = 1e-28 m^2, 1 microbarn = 1e-34 m^2
    sigma_m2 = sigma_p_gamma_microbarn * 1e-34

    # Mean free path lambda = 1 / (n_gamma * sigma)
    lambda_m = 1.0 / (n_gamma_m3 * sigma_m2)
    lambda_Mpc = lambda_m / MPC_TO_METERS

    return {
        "mean_cmb_photon_energy_eV": mean_photon_energy_eV,
        "gzk_threshold_at_mean_energy_eV": E_threshold_mean_eV,
        "gzk_threshold_at_wien_tail_eV": E_threshold_tail_eV,
        "cmb_photon_density_m3": n_gamma_m3,
        "pion_production_cross_section_m2": sigma_m2,
        "mean_free_path_meters": lambda_m,
        "mean_free_path_Mpc": lambda_Mpc
    }


# ==============================================================================
# 2. PENROSE WEYL CURVATURE & INITIAL ENTROPY CALCULATION
# ==============================================================================
def penrose_entropy_and_phase_space() -> Dict[str, Any]:
    """
    Computes the gravitational entropy of the universe and evaluates Penrose's
    Weyl Curvature Hypothesis:
    - Initial entropy at recombination / early universe: S_init ~ S_CMB ~ 10^89 k_B
    - Maximum possible entropy if observable mass collapses to a single BH:
      S_BH = (4 * pi * G * k_B / (hbar * c)) * M_obs^2
    - Phase space volume fraction W = exp(-S_max / k_B)
    """
    # Volume of observable universe: V = (4/3) * pi * R_obs^3
    V_obs = (4.0 / 3.0) * math.pi * (R_OBS_METERS**3)

    # Observable matter mass: M = (4/3) * pi * R_obs^3 * rho_m
    # Critical density rho_crit = 3 H0^2 / (8 pi G)
    H0_si = H0_PLANCK * 1e3 / MPC_TO_METERS
    rho_crit = 3.0 * (H0_si**2) / (8.0 * math.pi * G)
    rho_m = OMEGA_M * rho_crit
    M_obs_kg = rho_m * V_obs
    M_obs_solar = M_obs_kg / M_SUN_KG

    # Maximum Bekenstein-Hawking entropy:
    # S_BH / k_B = 4 * pi * G * M^2 / (hbar * c)
    S_max_kB = (4.0 * math.pi * G * (M_obs_kg**2)) / (HBAR * C)

    # CMB entropy density s_gamma = 4 * a_rad * T^3 / 3
    # u = 4 * sigma_SB * T^4 / c
    # s = 4 * u / (3 * T) = 16 * sigma_SB * T^3 / (3 * c)
    sigma_SB = 5.670374419e-8
    s_gamma_si = (16.0 * sigma_SB * (T_CMB_K**3)) / (3.0 * C)  # J / (m^3 K)
    s_gamma_kB = s_gamma_si / K_B  # per m^3
    S_CMB_kB = s_gamma_kB * V_obs

    # Relic neutrino entropy is (6/11) * S_CMB
    S_neutrino_kB = (6.0 / 11.0) * S_CMB_kB
    S_initial_kB = S_CMB_kB + S_neutrino_kB

    # Current supermassive black holes entropy (Egan & Lineweaver 2010): ~10^104 k_B
    S_current_SMBH_kB = 1.0e104

    # Log10 of maximum entropy and phase space ratio
    log10_S_max = math.log10(S_max_kB)
    log10_S_init = math.log10(S_initial_kB)

    return {
        "observable_mass_kg": M_obs_kg,
        "observable_mass_solar": M_obs_solar,
        "initial_entropy_CMB_kB": S_CMB_kB,
        "initial_entropy_total_kB": S_initial_kB,
        "log10_initial_entropy": log10_S_init,
        "current_SMBH_entropy_kB": S_current_SMBH_kB,
        "max_black_hole_entropy_kB": S_max_kB,
        "log10_max_entropy": log10_S_max,
        "penrose_phase_space_exponent": S_max_kB
    }


# ==============================================================================
# 3. INFLATIONARY PREDICTIONS & TRANS-PLANCKIAN CENSORSHIP (TCC)
# ==============================================================================
def inflation_and_tcc_bounds(N_efolds: float = 60.0) -> Dict[str, float]:
    """
    Computes predictions of Starobinsky R^2 / Higgs inflation and compares
    with the Trans-Planckian Censorship Conjecture (TCC):
    - Starobinsky R^2:
      r = 12 / N^2
      n_s = 1 - 2 / N
      Inflationary scale: V^(1/4) = 1.04e16 * (r / 0.01)^(1/4) GeV
    - TCC bound (Bedroya & Vafa 2020):
      e^N * (H_inf / M_P) <= 1
      forces H_inf <= M_P * exp(-N)
      r_TCC <= 1e-30
    """
    # Starobinsky R^2 predictions
    r_starobinsky = 12.0 / (N_efolds**2)
    n_s_starobinsky = 1.0 - (2.0 / N_efolds)

    # Energy scale of inflation
    V_scale_GeV = 1.04e16 * ((r_starobinsky / 0.01)**0.25)

    # Hubble parameter during inflation for Starobinsky:
    # H_inf = sqrt(V / (3 * M_pl^2))
    # V = (V_scale_GeV)^4
    # M_pl = 2.435e18 GeV
    V_total = V_scale_GeV**4
    H_inf_GeV = math.sqrt(V_total / (3.0 * (REDUCED_PLANCK_MASS_GEV**2)))

    # TCC maximum allowable Hubble parameter
    H_inf_max_TCC_GeV = PLANCK_MASS_GEV * math.exp(-N_efolds)

    # Ratio of predicted H_inf to TCC limit
    ratio_H_to_TCC = H_inf_GeV / H_inf_max_TCC_GeV

    return {
        "N_efolds": N_efolds,
        "starobinsky_r": r_starobinsky,
        "starobinsky_n_s": n_s_starobinsky,
        "inflationary_energy_scale_GeV": V_scale_GeV,
        "hubble_inflation_GeV": H_inf_GeV,
        "tcc_max_hubble_GeV": H_inf_max_TCC_GeV,
        "ratio_predicted_to_tcc_max": ratio_H_to_TCC,
        "tcc_r_upper_bound": 1e-30
    }


# ==============================================================================
# 4. SAKHAROV CONDITIONS & DAVIDSON-IBARRA LEPTOGENESIS BOUND
# ==============================================================================
def leptogenesis_davidson_ibarra_bound(
    delta_m_atm_sq_eV2: float = 2.5e-3, # Atmospheric mass splitting Delta m_31^2 in eV^2
    eta_b_observed: float = 6.12e-10
) -> Dict[str, float]:
    """
    Computes the Davidson-Ibarra bound on the lightest right-handed Majorana neutrino
    mass M_1 in thermal leptogenesis:
    |epsilon_1| <= (3 / (16 * pi)) * (M_1 * m_atm) / v^2
    where v = 174 GeV is the electroweak VEV.
    Baryon asymmetry: eta_b ~ 1e-2 * epsilon_1 * kappa, where efficiency kappa <= 1.
    """
    m_atm_eV = math.sqrt(delta_m_atm_sq_eV2)
    m_atm_GeV = m_atm_eV * 1e-9

    # To satisfy eta_b_observed ~ 1e-2 * epsilon_1 * kappa (with max kappa ~ 0.1 - 1.0)
    # Required |epsilon_1| >= eta_b_observed / (1e-2 * 0.1) = 1e-6
    kappa_max = 0.2
    epsilon_required = eta_b_observed / (0.01 * kappa_max)

    # From |epsilon_1| <= (3 / 16 pi) * M_1 * m_atm / v^2
    # M_1 >= epsilon_required * (16 pi v^2) / (3 * m_atm)
    numerator = epsilon_required * 16.0 * math.pi * (HIGGS_VEV_GEV**2)
    denominator = 3.0 * m_atm_GeV
    M1_min_GeV = numerator / denominator

    # Minimum reheating temperature T_reh >= M1_min
    T_reh_min_GeV = M1_min_GeV

    return {
        "atmospheric_neutrino_mass_eV": m_atm_eV,
        "observed_baryon_asymmetry_eta_b": eta_b_observed,
        "required_cp_asymmetry_epsilon": epsilon_required,
        "davidson_ibarra_min_M1_GeV": M1_min_GeV,
        "min_reheating_temperature_GeV": T_reh_min_GeV
    }


# ==============================================================================
# 5. SOUND HORIZON REDUCTION & THE H0-S8 TENSION CATCH-22
# ==============================================================================
def sound_horizon_and_s8_tradeoff(
    h0_early: float = H0_PLANCK,
    h0_target: float = H0_SHOES,
    rs_fiducial_Mpc: float = 147.21,
    s8_fiducial: float = 0.832
) -> Dict[str, float]:
    """
    Quantifies the required reduction in the comoving sound horizon rs(z_d)
    to resolve the Hubble tension, and computes the concomitant increase in S8:
    theta_* = rs / D_M(z_*) is fixed by CMB at 0.03% precision.
    Increasing H0 from 67.36 to 73.04 km/s/Mpc requires reducing rs proportionally:
    rs_target = rs_fiducial * (h0_early / h0_target).

    Early Dark Energy (EDE) adds ~8-10% energy density around z_c ~ 3500.
    To preserve CMB peak heights, EDE models require higher omega_c,
    which drives S8 = sigma_8 * sqrt(Omega_m / 0.3) upward from ~0.83 to ~0.86,
    worsening tension with weak lensing surveys (KiDS/DES, S8 ~ 0.77 +- 0.02).
    """
    h_ratio = h0_early / h0_target
    rs_target_Mpc = rs_fiducial_Mpc * h_ratio
    delta_rs_Mpc = rs_fiducial_Mpc - rs_target_Mpc
    delta_rs_percent = (delta_rs_Mpc / rs_fiducial_Mpc) * 100.0

    # Empirical correlation in EDE models: S8 increases by ~0.03 to 0.04
    s8_ede = s8_fiducial + 0.033

    # Weak lensing observed baseline (DES-Y3 / KiDS-1000 combined)
    s8_lensing = 0.766
    s8_lensing_sigma = 0.017

    tension_lcdm_lensing = abs(s8_fiducial - s8_lensing) / s8_lensing_sigma
    tension_ede_lensing = abs(s8_ede - s8_lensing) / s8_lensing_sigma

    return {
        "h0_early_km_s_Mpc": h0_early,
        "h0_target_km_s_Mpc": h0_target,
        "fiducial_rs_Mpc": rs_fiducial_Mpc,
        "required_rs_target_Mpc": rs_target_Mpc,
        "required_rs_reduction_Mpc": delta_rs_Mpc,
        "required_rs_reduction_percent": delta_rs_percent,
        "fiducial_s8_lcdm": s8_fiducial,
        "ede_predicted_s8": s8_ede,
        "lensing_observed_s8": s8_lensing,
        "lcdm_lensing_tension_sigma": tension_lcdm_lensing,
        "ede_lensing_tension_sigma": tension_ede_lensing
    }


# ==============================================================================
# 6. COMPREHENSIVE COSMIC ENTROPY BUDGET
# ==============================================================================
def cosmic_entropy_budget_inventory() -> List[Dict[str, Any]]:
    """
    Compiles the quantitative cosmic entropy budget of the observable universe
    across all physical components (Egan & Lineweaver 2010 baseline):
    1. CMB photons
    2. Relic neutrinos
    3. Relic dark matter (thermal WIMP or axion)
    4. Intergalactic and interstellar gas / baryons
    5. Stellar black holes (~10 M_sun)
    6. Supermassive black holes (SMBHs, 10^6 - 10^10 M_sun)
    7. Cosmic de Sitter event horizon (future maximum)
    """
    entropy_components = [
        {
            "component": "Relic Neutrinos",
            "entropy_kB": 2.9e89,
            "log10_entropy": 89.46,
            "mechanism": "Decoupled relativistic fermions at T ~ 1.95 K"
        },
        {
            "component": "CMB Photons",
            "entropy_kB": 5.3e89,
            "log10_entropy": 89.72,
            "mechanism": "Relic blackbody radiation at T = 2.7255 K"
        },
        {
            "component": "Baryons (Gas & Stars)",
            "entropy_kB": 1.0e81,
            "log10_entropy": 81.0,
            "mechanism": "Thermal Maxwell-Boltzmann gas of protons, He, electrons"
        },
        {
            "component": "Dark Matter",
            "entropy_kB": 1.0e88,
            "log10_entropy": 88.0,
            "mechanism": "Cold collisionless phase-space distribution"
        },
        {
            "component": "Stellar Mass Black Holes",
            "entropy_kB": 1.2e97,
            "log10_entropy": 97.08,
            "mechanism": "Bekenstein-Hawking horizon area of ~10^19 stellar BHs"
        },
        {
            "component": "Supermassive Black Holes (SMBHs)",
            "entropy_kB": 1.0e104,
            "log10_entropy": 104.0,
            "mechanism": "Galactic center SMBHs (dominated by largest ~10^10 M_sun BHs)"
        },
        {
            "component": "Cosmic Event Horizon (de Sitter)",
            "entropy_kB": 2.6e122,
            "log10_entropy": 122.41,
            "mechanism": "Gibbons-Hawking horizon entropy S = pi c^3 / (G hbar H_Lambda^2)"
        },
        {
            "component": "Max Theoretical (Single Horizon Black Hole)",
            "entropy_kB": 1.8e123,
            "log10_entropy": 123.25,
            "mechanism": "Total observable mass collapsed into single horizon BH"
        }
    ]
    return entropy_components


if __name__ == "__main__":
    print("=" * 80)
    print("ADVANCED COSMOGENESIS ENGINE: COMPUTATIONAL QUANTIFICATION")
    print("=" * 80)

    gzk = gzk_threshold_and_mean_free_path()
    print(f"\n[1] GZK Photo-Pion Cutoff:")
    print(f"    Mean CMB Photon Energy: {gzk['mean_cmb_photon_energy_eV']*1e3:.3f} meV")
    print(f"    Threshold at Mean Energy: {gzk['gzk_threshold_at_mean_energy_eV']:.2e} eV")
    print(f"    Threshold at Wien Tail: {gzk['gzk_threshold_at_wien_tail_eV']:.2e} eV (~50 EeV)")
    print(f"    Mean Free Path: {gzk['mean_free_path_Mpc']:.2f} Mpc")

    penrose = penrose_entropy_and_phase_space()
    print(f"\n[2] Penrose Weyl Curvature Hypothesis & Entropy Budget:")
    print(f"    Initial Universe Entropy (CMB + nu): 10^{penrose['log10_initial_entropy']:.2f} k_B")
    print(f"    Current SMBH Entropy: 10^{math.log10(penrose['current_SMBH_entropy_kB']):.1f} k_B")
    print(f"    Max Theoretical Entropy: 10^{penrose['log10_max_entropy']:.2f} k_B")
    print(f"    Phase Space Exponent: ~ 10^{penrose['log10_max_entropy']:.0f}")

    inf = inflation_and_tcc_bounds()
    print(f"\n[3] Inflation & Trans-Planckian Censorship Conjecture (TCC):")
    print(f"    Starobinsky R^2 Prediction: r = {inf['starobinsky_r']:.5f}, n_s = {inf['starobinsky_n_s']:.4f}")
    print(f"    Energy Scale: {inf['inflationary_energy_scale_GeV']:.2e} GeV")
    print(f"    Hubble Rate H_inf: {inf['hubble_inflation_GeV']:.2e} GeV")
    print(f"    TCC Limit on H_inf: {inf['tcc_max_hubble_GeV']:.2e} GeV")
    print(f"    Ratio H_inf / TCC_max: {inf['ratio_predicted_to_tcc_max']:.2e} (Severe Swampland Tension)")

    lep = leptogenesis_davidson_ibarra_bound()
    print(f"\n[4] Sakharov Conditions & Leptogenesis:")
    print(f"    Davidson-Ibarra Min Majorana Mass M_1: {lep['davidson_ibarra_min_M1_GeV']:.2e} GeV")
    print(f"    Min Reheating Temperature T_reh: {lep['min_reheating_temperature_GeV']:.2e} GeV")

    tradeoff = sound_horizon_and_s8_tradeoff()
    print(f"\n[5] Hubble Tension rs Reduction & S8 Catch-22:")
    print(f"    Required rs Reduction: {tradeoff['required_rs_reduction_percent']:.2f}% ({tradeoff['required_rs_target_Mpc']:.2f} Mpc)")
    print(f"    LCDM vs Lensing S8 Tension: {tradeoff['lcdm_lensing_tension_sigma']:.2f} sigma")
    print(f"    EDE vs Lensing S8 Tension: {tradeoff['ede_lensing_tension_sigma']:.2f} sigma (Tension Exacerbated!)")
    print("=" * 80)
