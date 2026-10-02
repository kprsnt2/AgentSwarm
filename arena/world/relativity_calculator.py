"""
Relativistic Flight Mechanics and FTL Causality Verification Engine
Agent: Kepler (A001, Gen 0)
Purpose: Complete numerical evaluation of kinematics, rocket mass ratios,
         beamed propulsion, interstellar medium (ISM) damage, and
         formal FTL causality violation (Tachyonic Antitelephone).
"""

import math

# Fundamental Constants (SI units)
c = 299792458.0              # Speed of light in vacuum (m/s)
g = 9.80665                  # Standard Earth gravitational acceleration (m/s^2)
m_p = 1.67262192369e-27      # Proton rest mass (kg)
e_charge = 1.602176634e-19   # Elementary charge (C or J/eV)
sec_per_year = 365.25 * 86400.0
ly_meters = c * sec_per_year # 1 light-year in meters (~9.461e15 m)
sigma_sb = 5.670374419e-8    # Stefan-Boltzmann constant (W/(m^2 K^4))

def lorentz_factor(beta):
    """Compute Lorentz factor gamma = 1 / sqrt(1 - beta^2)."""
    if abs(beta) >= 1.0:
        raise ValueError("Beta must be strictly within (-1, 1).")
    return 1.0 / math.sqrt(1.0 - beta**2)

def kinetic_energy_per_kg(beta):
    """Specific kinetic energy (J/kg) = (gamma - 1) * c^2."""
    gamma = lorentz_factor(beta)
    return (gamma - 1.0) * c**2

def rocket_mass_ratio(beta, beta_e, burns=1):
    """
    Relativistic Tsiolkovsky Rocket Equation:
    R = M_0 / M_f = ((1 + beta)/(1 - beta))^(burns / (2 * beta_e))
    burns = 1: acceleration only
    burns = 2: brachistochrone (acceleration + deceleration)
    burns = 4: full round trip (accelerate, decelerate, return accelerate, return decelerate)
    """
    if beta >= 1.0 or beta <= -1.0:
        return float('inf')
    ratio_base = (1.0 + beta) / (1.0 - beta)
    exponent = burns / (2.0 * beta_e)
    try:
        return ratio_base ** exponent
    except OverflowError:
        return float('inf')

def brachistochrone_trajectory(d_lightyears, accel=g):
    """
    1-g brachistochrone profile: continuous acceleration at rate `accel`
    to midpoint d/2, followed by turnaround and 1-g deceleration to destination.
    """
    d_m = d_lightyears * ly_meters
    cosh_val = 1.0 + (accel * (d_m / 2.0)) / (c**2)
    tau_mid = (c / accel) * math.acosh(cosh_val)
    tau_total = 2.0 * tau_mid # proper time experienced by crew
    
    sinh_val = math.sqrt(cosh_val**2 - 1.0)
    t_mid = (c / accel) * sinh_val
    t_total = 2.0 * t_mid     # coordinate time elapsed on Earth
    
    gamma_peak = cosh_val
    beta_peak = sinh_val / cosh_val
    
    return {
        "distance_ly": d_lightyears,
        "crew_time_years": tau_total / sec_per_year,
        "earth_time_years": t_total / sec_per_year,
        "peak_beta": beta_peak,
        "peak_gamma": gamma_peak
    }

def beamed_laser_sail(payload_mass_kg, target_beta, sail_diameter_m=10.0, wavelength_m=1.064e-6, absorption=1e-5):
    """
    Calculates power, diffraction aperture size, and thermal equilibrium for a laser-pushed sail.
    """
    sail_area = math.pi * (sail_diameter_m / 2.0)**2
    # Assume 1000 g acceleration for wafer or 1 g for human
    # Let's compute for 1-g acceleration:
    accel = g
    thrust = payload_mass_kg * accel
    beam_power = (thrust * c) / 2.0 # Perfect reflector F = 2P/c
    
    # Distance to reach target_beta under 1g
    # sinh(g * tau / c) = gamma * beta
    gamma = lorentz_factor(target_beta)
    accel_dist_m = (c**2 / accel) * (gamma - 1.0)
    
    # Diffraction limit: D_array >= 2.44 * lambda * L / d_sail
    d_array_m = 2.44 * wavelength_m * accel_dist_m / sail_diameter_m
    
    # Thermal equilibrium at peak power:
    # Flux I = P / sail_area
    flux = beam_power / sail_area
    flux_absorbed = flux * absorption
    # Radiated from 2 sides: 2 * sigma * T^4 = flux_absorbed
    temp_k = (flux_absorbed / (2.0 * sigma_sb))**0.25
    
    return {
        "thrust_N": thrust,
        "beam_power_W": beam_power,
        "accel_dist_m": accel_dist_m,
        "accel_dist_AU": accel_dist_m / 1.496e11,
        "array_aperture_km": d_array_m / 1000.0,
        "sail_temp_K": temp_k
    }

def ism_hazards(beta, n_cm3=1.0):
    """
    Computes relativistic proton bombardment, energy flux, and dust impact energy.
    """
    n_m3 = n_cm3 * 1.0e6
    gamma = lorentz_factor(beta)
    v = beta * c
    flux_particles = n_m3 * v # protons / (m^2 * s)
    
    # Proton kinetic energy
    ke_proton_J = (gamma - 1.0) * m_p * c**2
    ke_proton_GeV = ke_proton_J / (e_charge * 1e9)
    power_flux_kW = (flux_particles * ke_proton_J) / 1000.0
    
    # Interstellar dust grain: 1 um (1e-14 kg) and 10 um (1e-11 kg)
    ke_dust_1um_J = (gamma - 1.0) * 1.0e-14 * c**2
    ke_dust_10um_J = (gamma - 1.0) * 1.0e-11 * c**2
    tnt_kg_10um = ke_dust_10um_J / 4.184e6
    
    return {
        "beta": beta,
        "gamma": gamma,
        "proton_ke_GeV": ke_proton_GeV,
        "flux_p_m2_s": flux_particles,
        "power_flux_kW_m2": power_flux_kW,
        "dust_1um_J": ke_dust_1um_J,
        "dust_10um_MJ": ke_dust_10um_J / 1e6,
        "dust_10um_tnt_kg": tnt_kg_10um
    }

def tachyonic_antitelephone_exact(U_c, v_c, t1=100.0):
    """
    Exact algebraic derivation of Tolman's Tachyonic Antitelephone.
    Signal speed U = U_c * c (U_c > 1).
    Outpost velocity v = v_c * c (0 < v_c < 1).
    Alice sends signal at t1.
    Signal intersects Bob at t2. Bob immediately replies at speed U in his frame S'.
    Reply reaches Alice at t3.
    Exact closed-form ratio:
    t3 / t1 = (1 - v_c^2) * U_c^2 / (U_c - v_c)^2
    Threshold for backward time travel (t3 < t1):
    v_threshold = 2 * U_c / (U_c^2 + 1)
    """
    ratio = (1.0 - v_c**2) * (U_c**2) / ((U_c - v_c)**2)
    t3 = ratio * t1
    v_threshold = (2.0 * U_c) / (U_c**2 + 1.0)
    
    return {
        "U_c": U_c,
        "v_c": v_c,
        "t1": t1,
        "t3": t3,
        "delta_t": t3 - t1,
        "ratio": ratio,
        "v_threshold": v_threshold,
        "is_causality_violated": (t3 < t1)
    }

if __name__ == "__main__":
    print("=== SUMMARY OF RELATIVISTIC CALCULATIONS ===\n")
    
    print("1. Trajectories (1-g Brachistochrone):")
    for name, d in [("Proxima Centauri", 4.246), ("Sirius", 8.60), ("Vega", 25.0), ("Galactic Center", 26000.0), ("Andromeda", 2.537e6)]:
        res = brachistochrone_trajectory(d)
        print(f"  {name:20} ({d:,.1f} ly): Crew={res['crew_time_years']:.2f} yr | Earth={res['earth_time_years']:.2f} yr | Peak beta={res['peak_beta']:.7f} (gamma={res['peak_gamma']:.1f})")

    print("\n2. Rocket Mass Ratios (Payload = 1 kg):")
    for eng_name, beta_e in [("Fusion (0.05c)", 0.05), ("Antimatter Beam (0.5c)", 0.5), ("Ideal Photon Rocket (1.0c)", 1.0)]:
        print(f"  --- {eng_name} ---")
        for b in [0.1, 0.5, 0.9, 0.99]:
            r_acc = rocket_mass_ratio(b, beta_e, burns=1)
            r_dec = rocket_mass_ratio(b, beta_e, burns=2)
            print(f"    v={b:.2f}c -> Boost: {r_acc:.2e} kg | Boost+Decel: {r_dec:.2e} kg")

    print("\n3. Interstellar Medium Hazards (n = 1 cm^-3):")
    for b in [0.1, 0.5, 0.9, 0.99, 0.999]:
        h = ism_hazards(b)
        print(f"    v={b:.3f}c: Proton KE={h['proton_ke_GeV']:.3f} GeV | Flux={h['power_flux_kW_m2']:.2f} kW/m^2 | 10um Dust={h['dust_10um_MJ']:.2f} MJ ({h['dust_10um_tnt_kg']:.2f} kg TNT)")

    print("\n4. Tachyonic Antitelephone (t1 = 100.0 s):")
    for U_c, v_c in [(2.0, 0.5), (2.0, 0.8), (2.0, 0.9), (10.0, 0.3), (100.0, 0.05)]:
        t = tachyonic_antitelephone_exact(U_c, v_c, 100.0)
        status = "VIOLATION (t3 < t1)" if t['is_causality_violated'] else "Forward (t3 >= t1)"
        print(f"    U={U_c:5.1f}c, v={v_c:.2f}c (Threshold={t['v_threshold']:.3f}c): t3 = {t['t3']:6.2f} s [Delta t = {t['delta_t']:+6.2f} s] -> {status}")
