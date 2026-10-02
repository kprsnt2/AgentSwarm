"""
Verification script for Relativistic Interstellar Travel Feasibility and FTL Causality Obstruction.
Author: Kepler (A001, Generation 0)
"""

import math
import sys

def verify_all():
    print("=" * 70)
    print("VERIFYING RELATIVISTIC INTERSTELLAR TRAVEL FEASIBILITY & FTL CAUSALITY")
    print("=" * 70)
    
    # 1. Exact Physical Constants
    c = 299792458.0  # m/s exactly
    m_p = 1.67262192369e-27  # kg
    e_charge = 1.602176634e-19  # C
    m_p_ev = (m_p * c**2) / e_charge  # ~ 938.272 MeV
    sigma_sb = 5.670374419e-8  # W/(m^2 K^4)
    g0 = 9.80665  # m/s^2
    
    print("[1] Constants and Ground Truth:")
    assert c == 299792458.0
    print(f"  c = {c} m/s (exact)")
    
    # Kinetic energy at 0.99c
    beta_99 = 0.99
    gamma_99 = 1.0 / math.sqrt(1.0 - beta_99**2)
    e_k_99 = (gamma_99 - 1.0) * 1.0 * c**2
    print(f"  gamma(0.99c) = {gamma_99:.6f}")
    print(f"  KE(1 kg at 0.99c) = {e_k_99:.4e} J (~5.5e17 J)")
    assert 5.4e17 < e_k_99 < 5.5e17
    
    # Kinetic energy at 0.10c
    beta_10 = 0.10
    gamma_10 = 1.0 / math.sqrt(1.0 - beta_10**2)
    e_k_10 = (gamma_10 - 1.0) * 1.0 * c**2
    print(f"  gamma(0.10c) = {gamma_10:.8f}")
    print(f"  KE(1 kg at 0.10c) = {e_k_10:.4e} J (~4.53e14 J)")
    assert 4.5e14 < e_k_10 < 4.6e14
    
    # 2. Interstellar Medium Radiation Flux at 0.90c
    print("\n[2] ISM Radiation Flux at 0.90c (n_H = 1 atom/cm^3):")
    n_H = 1.0e6  # atoms / m^3
    beta_90 = 0.90
    gamma_90 = 1.0 / math.sqrt(1.0 - beta_90**2)
    v_90 = beta_90 * c
    flux_particle = n_H * v_90
    e_proton_j = (gamma_90 - 1.0) * m_p * c**2
    e_proton_gev = e_proton_j / (1e9 * e_charge)
    power_flux = flux_particle * e_proton_j
    print(f"  gamma(0.90c) = {gamma_90:.4f}")
    print(f"  Proton KE = {e_proton_gev:.3f} GeV (~1.214 GeV)")
    print(f"  Particle flux = {flux_particle:.3e} protons/(m^2 s)")
    print(f"  Continuous power flux = {power_flux / 1000.0:.2f} kW/m^2 (~52.5 kW/m^2)")
    assert 1.20 < e_proton_gev < 1.23
    assert 52.0 < (power_flux / 1000.0) < 53.0
    
    # Dust grain impact at 0.90c (10 micron grain, mass ~ 1e-11 kg)
    m_grain = 1.0e-11  # kg
    e_grain_j = (gamma_90 - 1.0) * m_grain * c**2
    tnt_equiv_kg = e_grain_j / 4.184e6
    print(f"  10 um dust grain KE at 0.90c = {e_grain_j / 1e6:.2f} MJ ({tnt_equiv_kg:.2f} kg TNT)")
    assert 1.15 < (e_grain_j / 1e6) < 1.18
    
    # 3. Relativistic Rocket Equation
    print("\n[3] Relativistic Rocket Equation Mass Ratios:")
    def mass_ratio(beta, beta_e, burns=1):
        ratio_single = ((1.0 + beta) / (1.0 - beta)) ** (1.0 / (2.0 * beta_e))
        return ratio_single ** burns
    
    # Fusion boost to 0.1c (beta_e = 0.05)
    r_fus_01_boost = mass_ratio(0.10, 0.05, burns=1)
    r_fus_01_rendezvous = mass_ratio(0.10, 0.05, burns=2)
    r_fus_01_roundtrip = mass_ratio(0.10, 0.05, burns=4)
    print(f"  Fusion (ve=0.05c) to 0.1c: boost={r_fus_01_boost:.2f}, rendezvous={r_fus_01_rendezvous:.2f}, roundtrip={r_fus_01_roundtrip:.1f}")
    assert 7.4 < r_fus_01_boost < 7.5
    assert 55.0 < r_fus_01_rendezvous < 56.0
    assert 3000.0 < r_fus_01_roundtrip < 3100.0
    
    # Fusion boost to 0.9c
    r_fus_09_boost = mass_ratio(0.90, 0.05, burns=1)
    r_fus_09_rendezvous = mass_ratio(0.90, 0.05, burns=2)
    print(f"  Fusion (ve=0.05c) to 0.9c: boost={r_fus_09_boost:.2e}, rendezvous={r_fus_09_rendezvous:.2e} kg/kg")
    assert 6.0e12 < r_fus_09_boost < 6.3e12
    assert 3.7e25 < r_fus_09_rendezvous < 3.8e25
    
    # Antimatter beam (beta_e = 0.5) to 0.9c
    r_anti_09_rendezvous = mass_ratio(0.90, 0.50, burns=2)
    print(f"  Antimatter beam (ve=0.5c) to 0.9c: rendezvous={r_anti_09_rendezvous:.1f}")
    assert 360.0 < r_anti_09_rendezvous < 362.0
    
    # Ideal photon rocket (beta_e = 1.0)
    r_photon_09_rendezvous = mass_ratio(0.90, 1.00, burns=2)
    r_photon_99_rendezvous = mass_ratio(0.99, 1.00, burns=2)
    print(f"  Photon rocket (ve=c): 0.9c rendezvous={r_photon_09_rendezvous:.1f}, 0.99c rendezvous={r_photon_99_rendezvous:.1f}")
    assert 18.9 < r_photon_09_rendezvous < 19.1
    assert 198.0 < r_photon_99_rendezvous < 200.0
    
    # 4. FTL Causality & Tachyonic Antitelephone
    print("\n[4] FTL Causality Violation & Antitelephone Threshold:")
    def v_threshold(U_over_c):
        return (2.0 * U_over_c) / (U_over_c**2 + 1.0)
    
    # Test U = 2.0c
    v_thresh_2 = v_threshold(2.0)
    print(f"  For U = 2.0c: v_threshold = {v_thresh_2:.4f} c")
    assert abs(v_thresh_2 - 0.80) < 1e-6
    
    # Test return time for U = 2.0c, v = 0.90c, t1 = 100s
    v_c = 0.90
    U_c = 2.0
    t1 = 100.0
    gamma_v = 1.0 / math.sqrt(1.0 - v_c**2)
    t3 = (1.0 - v_c**2) * (U_c**2 / (U_c - v_c)**2) * t1
    print(f"  At v = 0.90c, U = 2.0c, t1 = 100 s: t3 = {t3:.2f} s (< 100 s, received {t1 - t3:.2f} s before transmission!)")
    assert t3 < t1
    assert abs(t3 - 62.8099) < 0.01
    
    # Test instantaneous U -> infinity
    v_thresh_large = v_threshold(1e6)
    print(f"  For U = 1e6 c: v_threshold = {v_thresh_large:.6e} c (~0)")
    assert v_thresh_large < 1e-5
    
    # 5. Waste Heat Radiator Acceleration Clamp
    print("\n[5] Waste Heat Radiator Acceleration Clamp:")
    # Antimatter rocket: ve = 0.36c = 1.079e8 m/s, f_waste = 0.05 -> P_waste / F = 41.64 MW/N
    p_waste_per_newton_am = 41.64e6  # W/N
    t_rad = 1800.0  # K
    eps = 0.85
    sigma_areal = 10.0  # kg/m^2
    q_rad = 2.0 * eps * sigma_sb * t_rad**4
    alpha_rad = sigma_areal / q_rad  # kg/W
    m_rad_per_n = alpha_rad * p_waste_per_newton_am
    print(f"  Radiator heat flux at 1800K = {q_rad / 1e6:.3f} MW/m^2")
    print(f"  Radiator specific mass = {alpha_rad:.3e} kg/W")
    print(f"  Radiator mass per unit thrust = {m_rad_per_n:.1f} kg/N")
    a_max = 1.0 / m_rad_per_n
    print(f"  Max acceleration = {a_max:.4e} m/s^2 ({a_max / g0:.6f} g0)")
    # With Raman's optimized composite radiator (194.3 kg/N):
    a_max_raman = 1.0 / 194.3
    t_to_02c = (0.20 * c) / a_max_raman
    print(f"  With 194.3 kg/N radiator: a_max = {a_max_raman / g0:.6f} g0, time to reach 0.2c = {t_to_02c / (365.25 * 86400):.1f} years")
    assert 360.0 < (t_to_02c / (365.25 * 86400)) < 380.0
    
    print("\nALL VERIFICATIONS PASSED CONSTRUCTIVELY AND EXACTLY.")
    print("=" * 70)

if __name__ == "__main__":
    verify_all()
