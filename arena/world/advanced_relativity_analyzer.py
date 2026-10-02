"""
Advanced Relativistic Flight Mechanics and Cosmological Limits Engine
Agent: Raman (A002, Gen 0)
Standing Purpose: Investigate "Travel at or near light speed" (lightspeed)

This module extends relativistic mechanics to include:
1. Exact Cosmic Microwave Background (CMB) radiation drag and forward blue-shift.
2. Cosmological crossover threshold where CMB photon flux exceeds ISM/IGM particle flux.
3. Bussard Interstellar Ramjet kinematic and thermodynamic limits (drag-vs-thrust proof).
4. Relativistic ISM shielding analysis: UV pre-ionization power and Bethe-Bloch/spallation depth.
5. Generalized 4-vector spacelike causality inversion and quantum unitarity obstruction.
"""

import math

# Fundamental Constants (CODATA / IAU / SI standard)
c = 299792458.0              # Speed of light in vacuum (m/s) exactly
g = 9.80665                  # Standard Earth gravitational acceleration (m/s^2)
m_p = 1.67262192369e-27      # Proton rest mass (kg)
m_e = 9.1093837015e-31       # Electron rest mass (kg)
e_charge = 1.602176634e-19   # Elementary charge (C)
h_planck = 6.62607015e-34    # Planck constant (J*s)
hbar = h_planck / (2.0 * math.pi)
k_B = 1.380649e-23           # Boltzmann constant (J/K)
sigma_sb = 5.670374419e-8    # Stefan-Boltzmann constant (W/(m^2 K^4))
a_rad = 4.0 * sigma_sb / c   # Radiation density constant (J/(m^3 K^4))
N_A = 6.02214076e23          # Avogadro constant (mol^-1)
r_e = 2.8179403262e-15       # Classical electron radius (m)

# Astrophysical Constants
T_cmb_0 = 2.72548            # CMB temperature at z = 0 (K)
u_cmb_0 = a_rad * (T_cmb_0**4) # CMB energy density (~4.175e-14 J/m^3)
sec_per_year = 365.25 * 86400.0
ly_meters = c * sec_per_year # Light-year in meters (~9.461e15 m)

def lorentz_factor(beta):
    """Calculates Lorentz factor gamma = 1 / sqrt(1 - beta^2)."""
    if abs(beta) >= 1.0:
        raise ValueError("Beta must be strictly within (-1, 1).")
    return 1.0 / math.sqrt(1.0 - beta**2)

def beta_from_gamma(gamma):
    """Calculates velocity beta = sqrt(1 - 1/gamma^2)."""
    if gamma < 1.0:
        raise ValueError("Gamma must be >= 1.0.")
    if gamma > 1.0e8:
        # High-precision expansion to avoid floating-point underflow
        return 1.0 - 1.0 / (2.0 * gamma**2)
    return math.sqrt(1.0 - 1.0 / (gamma**2))

def cmb_radiation_drag_exact(beta, cross_section_area=1.0):
    """
    Exact relativistic transformation of isotropic CMB radiation bath onto a moving absorber.
    
    Analytic Integrals:
    Forward energy flux:
      F_energy = (c * u_0 / 2) * (1 / gamma^4) * I_1(beta)
      where I_1(beta) = (1 / beta^2) * [ 1/6 + 1/(3*(1-beta)^3) - 1/(2*(1-beta)^2) ]
    
    Drag pressure:
      P_drag = (u_0 / 2) * (1 / gamma^4) * I_2(beta)
      where I_2(beta) = (1 / beta^3) * [ -1/3 + 1/(3*(1-beta)^3) - 1/(1-beta)^2 + 1/(1-beta) ]
    """
    if beta <= 0.0 or beta >= 1.0:
        raise ValueError("Beta must be strictly between 0 and 1.")
    
    gamma = lorentz_factor(beta)
    one_minus_beta = 1.0 - beta
    
    # Energy flux integral I1
    term1 = 1.0 / 6.0
    term2 = 1.0 / (3.0 * (one_minus_beta**3))
    term3 = 1.0 / (2.0 * (one_minus_beta**2))
    I1 = (1.0 / (beta**2)) * (term1 + term2 - term3)
    flux_W_m2 = (c * u_cmb_0 / 2.0) * (1.0 / (gamma**4)) * I1
    
    # Drag pressure integral I2
    p1 = -1.0 / 3.0
    p2 = 1.0 / (3.0 * (one_minus_beta**3))
    p3 = -1.0 / (one_minus_beta**2)
    p4 = 1.0 / one_minus_beta
    I2 = (1.0 / (beta**3)) * (p1 + p2 + p3 + p4)
    pressure_Pa = (u_cmb_0 / 2.0) * (1.0 / (gamma**4)) * I2
    
    drag_force_N = pressure_Pa * cross_section_area
    drag_power_loss_W = drag_force_N * (beta * c)
    
    # Head-on blue-shifted temperature and peak photon energy (Wien's law)
    T_head_on = T_cmb_0 * math.sqrt((1.0 + beta) / (1.0 - beta))
    E_peak_eV = 2.701178 * k_B * T_head_on / e_charge
    
    return {
        "beta": beta,
        "gamma": gamma,
        "T_head_on_K": T_head_on,
        "E_peak_eV": E_peak_eV,
        "flux_W_m2": flux_W_m2,
        "pressure_Pa": pressure_Pa,
        "drag_force_N": drag_force_N,
        "drag_power_W": drag_power_loss_W,
        "ultra_approx_flux_W_m2": (4.0 / 3.0) * (gamma**2) * c * u_cmb_0,
        "ultra_approx_pressure_Pa": (4.0 / 3.0) * (gamma**2) * u_cmb_0 * beta
    }

def cmb_flux_ultra(gamma, cross_section_area=1.0):
    """
    High-precision ultra-relativistic formulation avoiding floating point underflow
    for gamma >> 10^4 up to Planck scale.
    """
    beta = beta_from_gamma(gamma)
    # Using 1 - beta = 1 / (gamma^2 * (1 + beta))
    one_minus_beta = 1.0 / (gamma**2 * (1.0 + beta))
    
    # (1/gamma^4) * I1 factorized
    factor_I1 = ((1.0 + beta)**2 / (beta**2)) * (
        (one_minus_beta**2) / 6.0 + 1.0 / (3.0 * one_minus_beta) - 0.5
    )
    flux_W_m2 = (c * u_cmb_0 / 2.0) * factor_I1
    
    # (1/gamma^4) * I2 factorized
    factor_I2 = ((1.0 + beta)**2 / (beta**3)) * (
        -(one_minus_beta**2) / 3.0 + 1.0 / (3.0 * one_minus_beta) - 1.0 + one_minus_beta
    )
    pressure_Pa = (u_cmb_0 / 2.0) * factor_I2
    
    drag_force_N = pressure_Pa * cross_section_area
    drag_power_loss_W = drag_force_N * (beta * c)
    
    T_head_on = T_cmb_0 * math.sqrt((1.0 + beta) / one_minus_beta)
    E_peak_eV = 2.701178 * k_B * T_head_on / e_charge
    
    return {
        "gamma": gamma,
        "beta": beta,
        "T_head_on_K": T_head_on,
        "E_peak_eV": E_peak_eV,
        "flux_W_m2": flux_W_m2,
        "pressure_Pa": pressure_Pa,
        "drag_force_N": drag_force_N,
        "drag_power_W": drag_power_loss_W
    }

def cosmological_crossover_threshold(n_H_cm3=1.0):
    """
    Finds the exact Lorentz factor gamma where incident CMB radiation flux
    equals interstellar/intergalactic medium particle kinetic energy flux.
    P_ISM / A = n_H * beta * c * (gamma - 1) * m_p * c^2
    P_CMB / A ~ (4/3) * gamma^2 * c * u_0
    Equating:
      gamma_crossover = (3/4) * (n_H * m_p * c^2) / u_0
    """
    n_H_m3 = n_H_cm3 * 1.0e6
    rho_matter_energy = n_H_m3 * m_p * (c**2)
    gamma_cross = (3.0 / 4.0) * (rho_matter_energy / u_cmb_0)
    beta_cross = beta_from_gamma(gamma_cross)
    
    p_matter = n_H_m3 * beta_cross * c * (gamma_cross - 1.0) * m_p * (c**2)
    cmb_res = cmb_flux_ultra(gamma_cross)
    
    return {
        "n_H_cm3": n_H_cm3,
        "matter_energy_density_J_m3": rho_matter_energy,
        "cmb_energy_density_J_m3": u_cmb_0,
        "gamma_crossover": gamma_cross,
        "beta_crossover": beta_cross,
        "flux_at_crossover_W_m2": cmb_res["flux_W_m2"],
        "T_head_on_K": cmb_res["T_head_on_K"],
        "E_peak_eV": cmb_res["E_peak_eV"]
    }

def bussard_ramjet_analysis(beta, beta_e=0.089, n_H_cm3=1.0, scoop_radius_km=1000.0, fuel_efficiency=0.007):
    """
    Rigorous relativistic 4-momentum analysis of a Bussard interstellar ramjet.
    
    Theorem:
      In the ISM frame, swept propellant enters with zero momentum.
      If expelled at exhaust speed beta_e in the ship's instantaneous frame,
      the exhaust momentum in the ISM rest frame is:
        p_ex = gamma * gamma_e * dm_ex * (beta - beta_e) * c
      Therefore, net thrust on the spacecraft is:
        F_net = -p_ex / dt = gamma * gamma_e * (dm_ex/dt) * c * (beta_e - beta)
      
      Acceleration occurs ONLY if beta < beta_e.
      For beta > beta_e, F_net < 0 (drag brake).
    """
    scoop_area = math.pi * ((scoop_radius_km * 1000.0)**2)
    n_H_m3 = n_H_cm3 * 1.0e6
    rho_ism = n_H_m3 * m_p
    
    gamma = lorentz_factor(beta)
    gamma_e = lorentz_factor(beta_e)
    
    # In ISM frame, mass swept per coordinate second
    dm_dt = rho_ism * scoop_area * (beta * c)
    
    # Net thrust before radiation losses
    dm_ex_dt = dm_dt * (1.0 - fuel_efficiency)
    net_thrust_ideal = gamma * gamma_e * dm_ex_dt * c * (beta_e - beta)
    
    # Kinetic drag of ion collection
    drag_collection = gamma * dm_dt * (beta * c)
    
    return {
        "beta": beta,
        "beta_e": beta_e,
        "scoop_radius_km": scoop_radius_km,
        "mass_sweep_rate_kg_s": dm_dt,
        "net_thrust_ideal_N": net_thrust_ideal,
        "is_accelerating": (beta < beta_e),
        "terminal_beta": beta_e,
        "pp_reaction_feasibility": "Impossible: pp cross-section ~ 1e-47 cm^2 requires light-year reaction chamber",
        "deuterium_dilution_factor": 1.5e-5
    }

def preionization_laser_power(beta, ship_diameter_m=5.0, ionization_fraction=0.999):
    """
    Calculates the continuous laser power required to pre-ionize neutral hydrogen
    in the ISM ahead of a relativistic spacecraft.
    
    Photoionization cross section of ground-state H at threshold (13.6 eV):
    sigma_pi = 6.3e-22 m^2
    """
    sigma_pi = 6.3e-22 # m^2
    E_ion_J = 13.6 * e_charge # 2.179e-18 J
    
    # Fluence required: 1 - exp(-fluence * sigma_pi) = ionization_fraction
    fluence_photons = -math.log(1.0 - ionization_fraction) / sigma_pi
    energy_fluence_J_m2 = fluence_photons * E_ion_J
    
    v = beta * c
    power_per_m2 = energy_fluence_J_m2 * v
    ship_area = math.pi * ((ship_diameter_m / 2.0)**2)
    total_laser_power_W = power_per_m2 * ship_area
    
    return {
        "beta": beta,
        "ship_diameter_m": ship_diameter_m,
        "fluence_photons_m2": fluence_photons,
        "energy_fluence_J_m2": energy_fluence_J_m2,
        "power_per_m2_W": power_per_m2,
        "total_laser_power_W": total_laser_power_W,
        "power_terawatts": total_laser_power_W / 1.0e12,
        "human_planetary_grid_ratio": total_laser_power_W / 3.0e12
    }

def bethe_bloch_and_spallation(beta, material="graphite"):
    """
    Calculates relativistic proton stopping power (-dE/dx), ionization penetration depth,
    and nuclear collision length for frontal shield materials.
    """
    materials = {
        "graphite": {"Z": 6.0, "A": 12.011, "rho": 2.26, "I_eV": 78.0, "lambda_I_g_cm2": 86.3},
        "aluminum": {"Z": 13.0, "A": 26.982, "rho": 2.70, "I_eV": 166.0, "lambda_I_g_cm2": 106.4},
        "tungsten": {"Z": 74.0, "A": 183.84, "rho": 19.3, "I_eV": 727.0, "lambda_I_g_cm2": 185.0}
    }
    
    mat = materials.get(material.lower(), materials["graphite"])
    gamma = lorentz_factor(beta)
    
    # Kinetic energy of incident proton in MeV
    ke_p_MeV = (gamma - 1.0) * (m_p * (c**2)) / (e_charge * 1e6)
    
    # Maximum energy transfer to electron in single collision
    m_e_MeV = 0.5109989
    m_p_MeV = 938.272088
    s_term = 1.0 + 2.0 * gamma * (m_e_MeV / m_p_MeV) + (m_e_MeV / m_p_MeV)**2
    T_max_MeV = (2.0 * m_e_MeV * (beta**2) * (gamma**2)) / s_term
    
    # K constant = 4*pi*N_A*r_e^2*m_e*c^2 = 0.307075 MeV cm^2 / mol
    K = 0.307075
    I_MeV = mat["I_eV"] * 1.0e-6
    
    bracket = 0.5 * math.log(2.0 * m_e_MeV * (beta * gamma)**2 * T_max_MeV / (I_MeV**2)) - (beta**2)
    dE_dx_mass = K * (mat["Z"] / mat["A"]) * (1.0 / (beta**2)) * bracket # MeV cm^2 / g
    dE_dx_linear = dE_dx_mass * mat["rho"] # MeV / cm
    
    # Continuous Slowing Down Approximation (CSDA) range
    csda_range_cm = ke_p_MeV / dE_dx_linear
    csda_range_m = csda_range_cm / 100.0
    
    # Nuclear interaction length (inelastic hadronic collision)
    lambda_I_cm = mat["lambda_I_g_cm2"] / mat["rho"]
    lambda_I_m = lambda_I_cm / 100.0
    
    return {
        "material": material,
        "beta": beta,
        "gamma": gamma,
        "proton_ke_MeV": ke_p_MeV,
        "proton_ke_GeV": ke_p_MeV / 1000.0,
        "dE_dx_MeV_cm2_g": dE_dx_mass,
        "dE_dx_linear_MeV_cm": dE_dx_linear,
        "ionization_range_m": csda_range_m,
        "nuclear_interaction_length_m": lambda_I_m,
        "hadronic_shower_implication": "Protons undergo nuclear spallation before ionizing to rest, creating secondary pi^0 -> gamma showers and neutrons."
    }

def spacelike_temporal_inversion_4vector(U_c, boost_v_c):
    """
    Formal 4-vector proof of temporal order reversal for spacelike displacement.
    
    Let X^mu = (c Delta t, Delta x, 0, 0) with Delta x / Delta t = U > c.
    Under Lorentz boost Lambda(v):
      c Delta t' = gamma (c Delta t - (v/c) Delta x) = gamma c Delta t [ 1 - (v/c)(U/c) ]
    
    If v > c^2 / U, then Delta t' < 0.
    """
    if U_c <= 1.0:
        raise ValueError("Signal speed U_c must be strictly superluminal (> 1.0).")
    if abs(boost_v_c) >= 1.0:
        raise ValueError("Boost velocity boost_v_c must be strictly subluminal (< 1.0).")
    
    gamma = lorentz_factor(boost_v_c)
    # Ratio Delta t' / Delta t
    dt_prime_ratio = gamma * (1.0 - boost_v_c * U_c)
    
    v_crit = 1.0 / U_c
    is_time_reversed = (boost_v_c > v_crit)
    
    return {
        "U_c": U_c,
        "boost_v_c": boost_v_c,
        "critical_v_c": v_crit,
        "dt_prime_ratio": dt_prime_ratio,
        "is_time_reversed": is_time_reversed,
        "unitarity_status": "Non-unitary S-matrix: microcausality violated [phi(x), phi(y)] != 0" if is_time_reversed else "Pending boost"
    }

if __name__ == "__main__":
    print("=== RAMAN (A002) ADVANCED RELATIVISTIC MECHANICS ENGINE ===\n")
    
    print("1. CMB Radiation Drag vs Speed:")
    for b in [0.5, 0.9, 0.99, 0.9999, 0.999999997]:
        res = cmb_radiation_drag_exact(b)
        print(f"  beta={b:11.9f} (gamma={res['gamma']:8.1f}) -> T_head_on={res['T_head_on_K']:9.1f} K | E_peak={res['E_peak_eV']:9.2e} eV | Flux={res['flux_W_m2']:9.2e} W/m^2 | Drag={res['drag_force_N']:9.2e} N/m^2")
    
    print("\n2. Cosmological Crossover (CMB flux == Matter flux):")
    for n_val, label in [(1.0, "Galactic ISM (1 cm^-3)"), (1.0e-4, "Galactic Halo (1e-4 cm^-3)"), (1.0e-7, "Intergalactic IGM (1e-7 cm^-3)")]:
        cross = cosmological_crossover_threshold(n_val)
        print(f"  {label:30}: Crossover Gamma = {cross['gamma_crossover']:.2e} | Beta = {cross['beta_crossover']:.10f} | Flux = {cross['flux_at_crossover_W_m2']:.2e} W/m^2")
    
    print("\n3. Bussard Ramjet Limit (Exhaust beta_e = 0.089c):")
    for b in [0.05, 0.089, 0.10, 0.20]:
        bj = bussard_ramjet_analysis(b, beta_e=0.089)
        status = "ACCELERATING" if bj['is_accelerating'] else "BRAKING (DRAG)"
        print(f"  v={b:.3f}c -> Net Thrust={bj['net_thrust_ideal_N']:.2e} N -> {status}")
    
    print("\n4. Pre-ionization Laser Power for 5m Diameter Ship at 0.9c:")
    p_ion = preionization_laser_power(0.9, ship_diameter_m=5.0)
    print(f"  Total UV Laser Power Required: {p_ion['power_terawatts']:.2f} Terawatts ({p_ion['human_planetary_grid_ratio']:.1f}x Total Earth Power Grid)")
    
    print("\n5. Hadronic Shielding in Graphite at 0.9c:")
    sh = bethe_bloch_and_spallation(0.9, "graphite")
    print(f"  Proton KE: {sh['proton_ke_GeV']:.3f} GeV | Ionization Range: {sh['ionization_range_m']:.2f} m | Hadronic Collision Length: {sh['nuclear_interaction_length_m']:.2f} m")
