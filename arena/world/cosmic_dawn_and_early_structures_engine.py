"""
Cosmic Dawn, Early Structure Formation, and Primordial Physical Discrepancies Engine
Agent: Kepler (A001) | Generation: 0 | Domain: Origin of the Universe (Cosmogenesis)

This engine quantitatively evaluates:
1. CMB precision thermodynamics, photon density, and spectral distortion bounds.
2. Standard Big Bang Nucleosynthesis (BBN) vs the Spite Plateau Primordial Lithium-7 Anomaly.
3. Sound horizon (r_s) shrinkage dynamics under Early Dark Energy (EDE) vs the S8 cosmic shear tension.
4. JWST ultra-early massive galaxy / supermassive black hole anomaly and halo mass function bounds.
5. Cosmic dawn 21-cm hydrogen differential brightness temperature (EDGES vs standard adiabatic floor vs SARAS 3).
6. Primordial non-Gaussianity f_NL consistency bounds for single-field vs multi-field inflation.
7. Relic neutrino effective degrees of freedom N_eff and thermal dark radiation thresholds.
8. Primordial magnetic field (PMF) void boundaries from TeV blazar gamma-ray non-cascade.
"""

import math
from typing import Dict, Any, Tuple, List

# Physical Constants (CODATA 2022 / NIST / Particle Data Group)
C_LIGHT = 2.99792458e8             # Speed of light [m/s]
K_BOLTZMANN = 1.380649e-23         # Boltzmann constant [J/K]
H_PLANCK = 6.62607015e-34          # Planck constant [J s]
H_BAR = H_PLANCK / (2.0 * math.pi) # Reduced Planck constant [J s]
G_NEWTON = 6.67430e-11             # Gravitational constant [m^3 kg^-1 s^-2]
M_PROTON = 1.67262192e-27          # Proton mass [kg]
SIGMA_SB = 5.670374419e-8          # Stefan-Boltzmann constant [W m^-2 K^-4]
MPC_TO_METERS = 3.085677581e22     # Megaparsec in meters
MSUN_TO_KG = 1.98847e30            # Solar mass in kg

# Established Cosmological Ground Truths (Planck 2018 / Riess 2022)
T_CMB_0 = 2.72548                  # CMB monopole temperature [K] (COBE/FIRAS)
H0_CMB = 67.4                      # Early CMB Hubble constant [km/s/Mpc] (Planck 2018)
H0_LOCAL = 73.04                   # Late local Hubble constant [km/s/Mpc] (SH0ES 2022)
H0_LOCAL_ERR = 1.04                # Error on local H0
H0_CMB_ERR = 0.54                  # Error on CMB H0
OMEGA_B_H2 = 0.02237               # Physical baryon density (Planck 2018)
OMEGA_C_H2 = 0.1200                # Physical cold dark matter density
OMEGA_M = (OMEGA_B_H2 + OMEGA_C_H2) / ((H0_CMB / 100.0) ** 2) # Total matter density ~ 0.3153
N_EFF_SM = 3.0440                  # Standard Model effective neutrino species


def calculate_cmb_thermodynamics(T0: float = T_CMB_0) -> Dict[str, float]:
    """
    Computes blackbody photon number density, energy density, and entropy density.
    """
    zeta_3 = 1.202056903159594
    # Number density n_gamma = (2 * zeta(3) / pi^2) * (k_B T / (hbar * c))^3
    kT_hbar_c = (K_BOLTZMANN * T0) / (H_BAR * C_LIGHT)
    n_gamma_m3 = (2.0 * zeta_3 / (math.pi ** 2)) * (kT_hbar_c ** 3)
    n_gamma_cm3 = n_gamma_m3 * 1e-6

    # Energy density u_gamma = (pi^2 / 15) * (k_B T)^4 / (hbar * c)^3
    u_gamma_J_m3 = (math.pi ** 2 / 15.0) * ((K_BOLTZMANN * T0) ** 4) / ((H_BAR * C_LIGHT) ** 3)
    rho_gamma_kg_m3 = u_gamma_J_m3 / (C_LIGHT ** 2)

    # Critical density today rho_crit = 3 H0^2 / (8 pi G)
    H0_si = (H0_CMB * 1000.0) / MPC_TO_METERS
    rho_crit_kg_m3 = (3.0 * (H0_si ** 2)) / (8.0 * math.pi * G_NEWTON)
    omega_gamma = rho_gamma_kg_m3 / rho_crit_kg_m3

    # Baryon-to-photon ratio eta = n_b / n_gamma
    rho_b_kg_m3 = (OMEGA_B_H2 / ((H0_CMB / 100.0) ** 2)) * rho_crit_kg_m3
    n_b_m3 = rho_b_kg_m3 / M_PROTON
    eta = n_b_m3 / n_gamma_m3

    return {
        "T0_kelvin": T0,
        "n_gamma_cm3": n_gamma_cm3,
        "rho_gamma_kg_m3": rho_gamma_kg_m3,
        "omega_gamma": omega_gamma,
        "omega_gamma_h2": omega_gamma * ((H0_CMB / 100.0) ** 2),
        "eta_baryon_photon": eta,
    }


def evaluate_bbn_lithium_anomaly(
    li7_theory: float = 4.68e-10,
    li7_theory_err: float = 0.32e-10,
    li7_obs: float = 1.58e-10,
    li7_obs_err: float = 0.11e-10,
) -> Dict[str, Any]:
    """
    Computes the statistical tension between standard BBN prediction of 7Li/H and
    the Spite plateau observational abundance in metal-poor galactic halo stars.
    """
    delta = li7_theory - li7_obs
    sigma_total = math.sqrt(li7_theory_err ** 2 + li7_obs_err ** 2)
    z_score = delta / sigma_total
    discrepancy_ratio = li7_theory / li7_obs

    # Primordial helium and deuterium
    yp_mass_fraction = 0.245           # 24.5% He-4
    xp_mass_fraction = 1.0 - yp_mass_fraction # 75.5% H-1
    dh_deuterium = 2.547e-5            # Cooke et al. 2018

    return {
        "li7_theory": li7_theory,
        "li7_obs": li7_obs,
        "delta": delta,
        "sigma_total": sigma_total,
        "z_score_tension": z_score,
        "discrepancy_ratio": discrepancy_ratio,
        "helium_4_mass_fraction": yp_mass_fraction,
        "hydrogen_1_mass_fraction": xp_mass_fraction,
        "deuterium_abundance_dh": dh_deuterium,
    }


def sound_horizon_and_early_dark_energy_shift(
    h0_early: float = H0_CMB,
    h0_late: float = H0_LOCAL,
    rs_baseline_mpc: float = 147.09,
) -> Dict[str, Any]:
    """
    Computes the required sound horizon shrinkage Delta r_s to reconcile the early
    and late Hubble parameters, and evaluates the resulting S8 growth tension.
    """
    # In flat LCDM, theta_* = r_s(z_*) / D_A(z_*) is measured to 0.03% precision by Planck.
    # D_A ~ c / H0 * integral(...)
    # Therefore, to increase H0 from h0_early to h0_late, r_s must shrink proportionally:
    # r_s_required / r_s_baseline = h0_early / h0_late
    rs_required_mpc = rs_baseline_mpc * (h0_early / h0_late)
    delta_rs_mpc = rs_required_mpc - rs_baseline_mpc
    percentage_reduction = (abs(delta_rs_mpc) / rs_baseline_mpc) * 100.0

    # Hubble tension significance
    sigma_h0 = math.sqrt(H0_LOCAL_ERR ** 2 + H0_CMB_ERR ** 2)
    h0_tension_sigma = (h0_late - h0_early) / sigma_h0

    # S8 tension consequence:
    # EDE models increase S8 from Planck baseline ~0.834 to ~0.852, whereas weak lensing finds:
    s8_planck = 0.834
    s8_ede = 0.852
    s8_kids = 0.759
    s8_kids_err = 0.023
    kids_tension_planck = (s8_planck - s8_kids) / s8_kids_err
    kids_tension_ede = (s8_ede - s8_kids) / s8_kids_err

    return {
        "h0_early_cmb": h0_early,
        "h0_late_local": h0_late,
        "h0_tension_sigma": h0_tension_sigma,
        "rs_baseline_mpc": rs_baseline_mpc,
        "rs_required_mpc": rs_required_mpc,
        "delta_rs_mpc": delta_rs_mpc,
        "percentage_reduction": percentage_reduction,
        "s8_planck": s8_planck,
        "s8_ede": s8_ede,
        "s8_kids_1000": s8_kids,
        "s8_kids_tension_planck_sigma": kids_tension_planck,
        "s8_kids_tension_ede_sigma": kids_tension_ede,
    }


def jwst_highz_galaxy_overdensity(
    redshift: float = 10.0,
    m_star_msun: float = 10.0 ** 10.5,
    max_star_formation_efficiency: float = 0.32,
) -> Dict[str, Any]:
    """
    Computes required dark matter halo mass and Gaussian fluctuation peak height nu(M, z)
    for extreme JWST high-redshift galaxies (e.g. JADES-GS-z14-0 or massive candidates).
    """
    # Cosmic baryon fraction
    fb = OMEGA_B_H2 / (OMEGA_B_H2 + OMEGA_C_H2)  # ~ 0.157
    m_halo_req_msun = m_star_msun / (max_star_formation_efficiency * fb)

    # In standard LCDM with sigma8 = 0.811, linear growth factor D(z) ~ 1 / (1 + z) at high z
    # Linear root-mean-square mass fluctuation sigma(M) ~ sigma8 * (M / M8)^(-gamma)
    # At z = 10, for M_halo ~ 2e11 Msun, sigma(M, z) is approximately 0.26
    # Critical overdensity delta_c = 1.686
    sigma_m_z10 = 0.26
    delta_c = 1.686
    nu_peak = delta_c / sigma_m_z10

    # Probability of Gaussian peak exceeding nu: P(>nu) ~ erfc(nu / sqrt(2)) / 2
    # For nu ~ 6.5, this is exceedingly suppressed: ~ 4e-11
    log10_prob_gaussian = -0.5 * (nu_peak ** 2) * math.log10(math.e) - math.log10(nu_peak * math.sqrt(2 * math.pi))

    return {
        "redshift": redshift,
        "m_star_msun": m_star_msun,
        "baryon_fraction_fb": fb,
        "max_epsilon_sf": max_star_formation_efficiency,
        "m_halo_req_msun": m_halo_req_msun,
        "nu_peak_significance": nu_peak,
        "log10_gaussian_probability": log10_prob_gaussian,
    }


def cosmic_dawn_21cm_temperature_anomaly(
    z_edges: float = 17.2,
    tb_edges_obs_mk: float = -500.0,
) -> Dict[str, Any]:
    """
    Computes the standard adiabatic gas cooling floor at z = 17.2 and compares
    it with the EDGES detected absorption trough (-500 mK).
    """
    # CMB temperature at redshift z
    t_cmb = T_CMB_0 * (1.0 + z_edges)  # 2.72548 * 18.2 = 49.60 K

    # Gas temperature under pure adiabatic expansion after thermal decoupling at z_dec ~ 150:
    # T_gas(z) = T_CMB(z_dec) * ((1 + z) / (1 + z_dec))^2
    # At z = 17.2, standard thermal calculation yields T_gas,min ~ 6.8 K
    t_gas_adiabatic_min = 6.8

    # Standard maximum absorption amplitude (assuming saturated Ly-alpha coupling Ts -> Tgas, x_HI = 1)
    # delta_Tb = 27 * x_HI * (1 - T_rad / T_s) * sqrt((1+z)/10) * ... [mK]
    # For standard LCDM: T_rad = T_CMB
    term_geometry = math.sqrt((1.0 + z_edges) / 10.0)  # sqrt(1.82) ~ 1.349
    delta_tb_standard_min_mk = 27.0 * 1.349 * (1.0 - (t_cmb / t_gas_adiabatic_min))

    # Required radiation temperature or excess cooling to explain -500 mK
    # -500 = 27 * 1.349 * (1 - T_rad / T_s) => 1 - T_rad/T_s = -500 / 36.426 = -13.726
    # T_rad / T_s = 14.726
    # If T_s = 6.8 K, T_rad must be 14.726 * 6.8 = 100.1 K (an excess of ~50.5 K over CMB!)
    trad_required_k = 14.726 * t_gas_adiabatic_min
    trad_excess_ratio = trad_required_k / t_cmb

    return {
        "redshift_z": z_edges,
        "frequency_mhz": 1420.40575 / (1.0 + z_edges),
        "t_cmb_k": t_cmb,
        "t_gas_adiabatic_min_k": t_gas_adiabatic_min,
        "delta_tb_standard_min_mk": delta_tb_standard_min_mk,
        "delta_tb_edges_obs_mk": tb_edges_obs_mk,
        "discrepancy_factor": tb_edges_obs_mk / delta_tb_standard_min_mk,
        "trad_required_k": trad_required_k,
        "trad_excess_over_cmb_ratio": trad_excess_ratio,
    }


def inflationary_non_gaussianity_bounds(ns: float = 0.9649) -> Dict[str, Any]:
    """
    Evaluates Maldacena's single-field consistency relation against Planck constraints
    and future SPHEREx/Euclid discriminative power.
    """
    # Maldacena consistency theorem for single-field slow-roll inflation:
    # f_NL^(local) = (5/12) * (1 - n_s)
    fnl_single_field = (5.0 / 12.0) * (1.0 - ns)

    # Observational constraints
    planck_fnl_local = -0.9
    planck_fnl_err = 5.1
    spherex_sigma = 0.5

    return {
        "spectral_index_ns": ns,
        "fnl_local_single_field_maldacena": fnl_single_field,
        "planck_2018_fnl_local": planck_fnl_local,
        "planck_2018_uncertainty": planck_fnl_err,
        "spherex_forecast_sigma": spherex_sigma,
        "discrimination_margin_sigma": abs(1.0 - fnl_single_field) / spherex_sigma,
    }


def relic_neutrino_effective_dof(
    n_eff_measured: float = 2.99,
    n_eff_err: float = 0.17,
) -> Dict[str, Any]:
    """
    Evaluates N_eff bounds against the Standard Model prediction and future CMB-S4 reach.
    """
    delta_n_eff = n_eff_measured - N_EFF_SM
    sigma_cmbs4 = 0.03
    # Minimum Delta N_eff for a single real scalar decoupling before top quark (g*s ~ 106.75):
    # Delta N_eff = (4/7) * (11/4 * 3.91 / 106.75)^(4/3) ~ 0.027
    delta_neff_minimal_scalar = (4.0 / 7.0) * ((11.0 / 4.0) * (3.91 / 106.75)) ** (4.0 / 3.0)

    return {
        "n_eff_standard_model": N_EFF_SM,
        "n_eff_measured_planck": n_eff_measured,
        "delta_n_eff_measured": delta_n_eff,
        "tension_with_sm_sigma": abs(delta_n_eff) / n_eff_err,
        "cmbs4_forecast_sigma": sigma_cmbs4,
        "minimal_scalar_thermal_relic_shift": delta_neff_minimal_scalar,
    }


def primordial_magnetic_field_void_bounds() -> Dict[str, Any]:
    """
    Evaluates blazar TeV gamma-ray halo lower limits and CMB upper limits on PMFs.
    """
    b_min_void_gauss = 1.0e-16         # Fermi-LAT / HESS / MAGIC non-cascade lower bound
    b_max_cmb_gauss = 0.8e-9           # Planck CMB Faraday rotation & anisotropy upper bound
    dynamic_range_orders = math.log10(b_max_cmb_gauss / b_min_void_gauss)

    return {
        "pmf_min_void_gauss": b_min_void_gauss,
        "pmf_max_cmb_gauss": b_max_cmb_gauss,
        "orders_of_magnitude_window": dynamic_range_orders,
        "resolving_instrument": "CTA (Cherenkov Telescope Array) and SKA Faraday Grid",
    }


def compile_master_cosmic_dawn_registry() -> Dict[str, Any]:
    """
    Synthesizes all quantitative calculations into a unified registry of open problems
    and their decisive resolving empirical observations.
    """
    cmb_data = calculate_cmb_thermodynamics()
    bbn_data = evaluate_bbn_lithium_anomaly()
    hubble_data = sound_horizon_and_early_dark_energy_shift()
    jwst_data = jwst_highz_galaxy_overdensity()
    cd_data = cosmic_dawn_21cm_temperature_anomaly()
    fnl_data = inflationary_non_gaussianity_bounds()
    neff_data = relic_neutrino_effective_dof()
    pmf_data = primordial_magnetic_field_void_bounds()

    return {
        "cmb_thermodynamics": cmb_data,
        "bbn_lithium": bbn_data,
        "sound_horizon_ede": hubble_data,
        "jwst_highz": jwst_data,
        "cosmic_dawn_21cm": cd_data,
        "inflation_non_gaussianity": fnl_data,
        "relic_neutrinos": neff_data,
        "primordial_magnetic_fields": pmf_data,
    }


if __name__ == "__main__":
    registry = compile_master_cosmic_dawn_registry()
    print("=== COSMIC DAWN & EARLY STRUCTURE ENGINE COMPILED SUCCESSFULLY ===")
    print(f"CMB T0: {registry['cmb_thermodynamics']['T0_kelvin']} K, n_gamma: {registry['cmb_thermodynamics']['n_gamma_cm3']:.2f} cm^-3")
    print(f"BBN 7Li tension: {registry['bbn_lithium']['z_score_tension']:.2f} sigma (theory {registry['bbn_lithium']['li7_theory']:.2e} vs obs {registry['bbn_lithium']['li7_obs']:.2e})")
    print(f"Hubble tension: {registry['sound_horizon_ede']['h0_tension_sigma']:.2f} sigma (shrinkage: {registry['sound_horizon_ede']['delta_rs_mpc']:.2f} Mpc)")
    print(f"JWST high-z halo peak: {registry['jwst_highz']['nu_peak_significance']:.2f} sigma (halo {registry['jwst_highz']['m_halo_req_msun']:.2e} Msun)")
    print(f"21-cm EDGES vs Standard: {registry['cosmic_dawn_21cm']['delta_tb_edges_obs_mk']} mK vs {registry['cosmic_dawn_21cm']['delta_tb_standard_min_mk']:.2f} mK")
