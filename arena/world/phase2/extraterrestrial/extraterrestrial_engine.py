"""
extraterrestrial_engine.py - Extraterrestrial Life, Intelligence & Visitation Epistemic Engine
Agent: Nagarjuna (A004), Generation 0
Domain: Are aliens real? (extraterrestrial)

PHASE 2 DELIVERABLE. Epistemic class: Exploratory.
Standard of evidence: a falsifiable prediction plus the settling observation for
each of the three strictly demarcated questions:
  Q1. Does life exist elsewhere?            (plausible, investigable)
  Q2. Does intelligent life exist?          (Fermi paradox; undecidable)
  Q3. Has it visited Earth?                 (unsupported; rejected under null)
No discovery is asserted; plausibility is never treated as evidence.

Self-contained: imports only the Python standard library.
"""

import math
import random
from typing import Any, Dict, List, Tuple

# ------------------------------------------------------------------ #
# Fundamental constants (SI, CODATA 2018 / BIPM SI Brochure)          #
# ------------------------------------------------------------------ #
C: float = 299792458.0                 # speed of light in vacuum (m/s, exact)
K_B: float = 1.380649e-23              # Boltzmann constant (J/K)
R_GAS: float = 8.314462618             # universal gas constant (J/mol/K)
N_A: float = 6.02214076e23             # Avogadro constant (1/mol)
G_EARTH: float = 9.80665               # standard gravity (m/s^2)
SIGMA_SB: float = 5.670374419e-8       # Stefan-Boltzmann constant (W/m^2/K^4)
TNT_KILOTON_J: float = 4.184e12        # energy of 1 kiloton TNT (J)

# Exoplanet census (Establishment): ~5,500 confirmed as of the mid-2020s.
CONFIRMED_EXOPLANET_COUNT: int = 5500


# ================================================================== #
# Q1 - DOES LIFE EXIST ELSEWHERE (biogenesis & biospheres)            #
# ================================================================== #
def kopparapu_habitable_zone(
    stellar_teff_k: float,
    stellar_luminosity_solar: float
) -> Dict[str, float]:
    """
    Conservative circumstellar habitable zone (Kopparapu et al. 2013/2014):
      d[AU] = sqrt(L / S_eff), with S_eff = S_eff,SUN + a*t* + b*t*^2 + c*t*^3 + d*t*^4,
      t* = Teff - 5780 K.  Returns the four HZ boundaries in AU.
    """
    t_star = stellar_teff_k - 5780.0
    coefficients = {
        "recent_venus":      (1.7763, 1.4335e-4, 3.3954e-9, -7.6364e-12, -1.1950e-15),
        "runaway_greenhouse": (1.0385, 1.2456e-4, 1.4612e-8, -7.6345e-12, -1.7511e-15),
        "maximum_greenhouse": (0.3507, 5.9578e-5, 1.6707e-9, -3.0058e-12, -5.1925e-16),
        "early_mars":         (0.3207, 5.4471e-5, 1.5275e-9, -2.1709e-12, -3.8282e-16),
    }
    boundaries: Dict[str, float] = {}
    for name, (se_sun, a, b, c, d) in coefficients.items():
        s_eff = se_sun + a * t_star + b * t_star ** 2 + c * t_star ** 3 + d * t_star ** 4
        s_eff = max(s_eff, 1e-4)
        boundaries[name] = math.sqrt(stellar_luminosity_solar / s_eff)
    boundaries["conservative_width_au"] = (
        boundaries["maximum_greenhouse"] - boundaries["runaway_greenhouse"]
    )
    return boundaries


def ch4_o2_disequilibrium(
    ch4_mixing_ratio: float = 1.8e-6,        # Earth-like biogenic methane abundance
    o2_mixing_ratio: float = 0.21,           # Earth-like O2
    co2_mixing_ratio: float = 4.0e-4,
    h2o_mixing_ratio: float = 1.0e-2,
    co_mixing_ratio: float = 1.0e-8,         # CO suppressed by microbial metabolism
    temperature_k: float = 288.15,
    pressure_bar: float = 1.01325,
    photochemical_lifetime_yr: float = 10.0
) -> Dict[str, Any]:
    """
    Thermodynamic disequilibrium of the reaction:
        CH4 + 2 O2 -> CO2 + 2 H2O      (Delta G' = -801 kJ/mol)
    Delta G = Delta G' + R T ln Q,  Q = (p_CO2 * p_H2O^2) / (p_CH4 * p_O2^2).
    The CH4 destruction flux required to sustain the observed mixing ratio
    (against a ~10 yr photochemical lifetime) is the biosignature budget.
    The abiotic false-positive gate is CO: abiotic CO2 photolysis yields O2 with
    CO at comparable levels, so f_CO/f_O2 > 0.05 marks an abiotic mimic.
    """
    delta_g_std_j_mol = -801.0e3

    p_ch4 = max(ch4_mixing_ratio * pressure_bar, 1e-25)
    p_o2 = max(o2_mixing_ratio * pressure_bar, 1e-25)
    p_co2 = max(co2_mixing_ratio * pressure_bar, 1e-25)
    p_h2o = max(h2o_mixing_ratio * pressure_bar, 1e-25)

    reaction_quotient = max(
        (p_co2 * p_h2o ** 2) / (p_ch4 * p_o2 ** 2), 1e-30
    )
    delta_g_actual_j_mol = delta_g_std_j_mol + R_GAS * temperature_k * math.log(reaction_quotient)

    # Atmospheric column density (molecules/m^2): column = p / (mu * g)
    mu = 28.97e-3 / N_A
    column_density = (pressure_bar * 1e5) / (mu * G_EARTH)
    tau_photochemical_s = photochemical_lifetime_yr * 365.25 * 86400.0
    required_flux = (column_density * ch4_mixing_ratio) / tau_photochemical_s

    abiotic_explanation_plausible = (
        (co_mixing_ratio > 1e-4 and (co_mixing_ratio / p_o2) > 0.05)
        or (ch4_mixing_ratio < 1e-7 and o2_mixing_ratio > 1e-2)
    )
    is_disequilibrium = (
        delta_g_actual_j_mol < -500.0e3
        and ch4_mixing_ratio >= 1e-6
        and o2_mixing_ratio >= 1e-3
    )

    return {
        "delta_g_standard_kj_per_mol": delta_g_std_j_mol / 1e3,
        "delta_g_actual_kj_per_mol": delta_g_actual_j_mol / 1e3,
        "required_biogenic_flux_molecules_per_m2_s": required_flux,
        "is_thermodynamic_disequilibrium": is_disequilibrium,
        "abiotic_explanation_plausible": abiotic_explanation_plausible,
        "settles_biosignature": is_disequilibrium and not abiotic_explanation_plausible,
    }


# ================================================================== #
# Q2 - DOES INTELLIGENT LIFE EXIST (Drake / Fermi / cosmic haystack)  #
# ================================================================== #
def drake_equation_point_estimate(
    r_star: float = 1.9, f_p: float = 0.95, n_e: float = 0.20,
    f_l: float = 0.10, f_i: float = 0.01, f_c: float = 0.10,
    l_years: float = 10000.0
) -> float:
    """Classic Drake point estimate N = R* fp ne fl fi fc L (arbitrary units)."""
    return r_star * f_p * n_e * f_l * f_i * f_c * l_years


def drake_equation_monte_carlo(
    n_samples: int = 20000,
    random_seed: int = 20240419
) -> Dict[str, float]:
    """
    Monte Carlo over the log-uniform / log-normal priors of Sandberg,
    Drexler & Ord (2018).  Astronomical factors are observationally
    constrained; the biological/technological factors span orders of
    magnitude.  The resulting variance dissolves the Fermi paradox:
    even with NO astrobiology measured, P(N < 1) is large.
    """
    rng = random.Random(random_seed)
    n_values: List[float] = []
    alone_count = 0

    for _ in range(n_samples):
        r_star = max(0.5, rng.gauss(1.9, 0.4))       # stars/yr in the Milky Way
        f_p = rng.uniform(0.9, 1.0)                  # planet frequency
        n_e = rng.uniform(0.1, 0.4)                  # HZ terrestrial planets
        f_l = 10.0 ** rng.uniform(-5.0, 0.0)         # log-uniform 1e-5 .. 1
        f_i = 10.0 ** rng.uniform(-4.0, math.log10(0.5))  # log-uniform 1e-4 .. 0.5
        f_c = 10.0 ** rng.uniform(-2.0, math.log10(0.5))  # log-uniform 1e-2 .. 0.5
        l_yr = 10.0 ** rng.uniform(2.0, 7.0)         # communicative lifetime 1e2..1e7 yr

        n_val = r_star * f_p * n_e * f_l * f_i * f_c * l_yr
        n_values.append(n_val)
        if n_val < 1.0:
            alone_count += 1

    n_values.sort()
    return {
        "median_n": n_values[n_samples // 2],
        "mean_n": sum(n_values) / n_samples,
        "p_alone_in_galaxy": alone_count / n_samples,
        "percentile_5": n_values[int(0.05 * n_samples)],
        "percentile_95": n_values[int(0.95 * n_samples)],
        "sample_size": n_samples,
        "is_undecidable_under_current_priors": True,
    }


def cosmic_haystack_fraction(
    distance_searched_pc: float = 100.0,
    bandwidth_searched_hz: float = 1.0e9,
    eirp_detection_limit_w: float = 1.0e13,
    sky_fraction_searched: float = 0.05,
    duty_cycle_coverage: float = 1.0e-3
) -> Dict[str, float]:
    """
    8-dimensional SETI 'Cosmic Haystack' fraction surveyed (Wright et al. 2018):
    volume x frequency x EIRP x sky x duty-cycle x polarization.
    """
    galaxy_radius_pc = 10000.0
    total_volume = (4.0 / 3.0) * math.pi * galaxy_radius_pc ** 3
    searched_volume = (4.0 / 3.0) * math.pi * distance_searched_pc ** 3 * sky_fraction_searched
    vol_frac = min(searched_volume / total_volume, 1.0)

    total_rf_bandwidth_hz = 100.0e9                     # 0.1 - 100 GHz microwave window
    freq_frac = min(bandwidth_searched_hz / total_rf_bandwidth_hz, 1.0)

    eirp_decades_covered = max(0.0, min(10.0, 18.0 - math.log10(max(eirp_detection_limit_w, 1.0))))
    eirp_frac = eirp_decades_covered / 10.0

    polarization_fraction = 0.5                         # usually only one polarisation
    total_fraction = vol_frac * freq_frac * eirp_frac * 0.1 * polarization_fraction * duty_cycle_coverage
    total_fraction = max(total_fraction, 1e-30)

    return {
        "volume_fraction": vol_frac,
        "frequency_fraction": freq_frac,
        "eirp_fraction": eirp_frac,
        "total_haystack_fraction_searched": total_fraction,
        "log10_total_fraction": math.log10(total_fraction),
    }


# ================================================================== #
# Q3 - HAS IT VISITED EARTH (relativistic cost + Bayesian evaluation) #
# ================================================================== #
def relativistic_isp_cost(beta: float) -> Dict[str, float]:
    """
    Specific kinetic energy and propellant mass ratio for an interstellar flyby.
        gamma = 1/sqrt(1-beta^2);  E/m = (gamma-1)c^2
        R = ((1+beta)/(1-beta))^(c / (2 u_ex)),  u_ex = exhaust velocity
    Fusion exhaust u_ex = 0.05c (D-He3); ideal antimatter photon rocket u_ex = c.
    """
    if not 0.0 < beta < 1.0:
        raise ValueError("beta must satisfy 0 < beta < 1")
    gamma = 1.0 / math.sqrt(1.0 - beta ** 2)
    ke_per_kg = (gamma - 1.0) * C ** 2
    factor = (1.0 + beta) / (1.0 - beta)
    r_fusion = factor ** (1.0 / (2.0 * 0.05))     # u_ex = 0.05c
    r_antimatter = math.sqrt(factor)              # u_ex = c (photon rocket)
    return {
        "beta": beta,
        "gamma": gamma,
        "specific_kinetic_energy_j_per_kg": ke_per_kg,
        "specific_kinetic_energy_kilotons_tnt_per_kg": ke_per_kg / TNT_KILOTON_J,
        "fusion_mass_ratio_one_way": r_fusion,
        "fusion_mass_ratio_round_trip": r_fusion ** 2,   # accelerate + brake
        "antimatter_mass_ratio_one_way": r_antimatter,
    }


def visitation_posterior(
    prior_p_visit: float = 1.0e-9,
    likelihood_data_given_et: float = 0.90,
    likelihood_data_given_mundane: float = 1.0e-3
) -> Dict[str, float]:
    """
    Bayesian evaluation of a purported visitation claim:
        P(ET | data) = L1 P1 / (L1 P1 + L0 P0).
    Defaults are a *generous* prior toward ET and a flattering sensor-artefact
    likelihood; even so, generic unexplained data cannot rescue the hypothesis.
    """
    p0 = 1.0 - prior_p_visit
    numerator = likelihood_data_given_et * prior_p_visit
    denominator = numerator + likelihood_data_given_mundane * p0
    posterior = numerator / denominator if denominator > 0 else 0.0
    bayes_factor = likelihood_data_given_et / max(likelihood_data_given_mundane, 1e-15)
    return {
        "prior": prior_p_visit,
        "bayes_factor": bayes_factor,
        "posterior": posterior,
        "rejects_null": posterior > 0.95,
    }


def isotopic_anomaly_sigma(
    measured_ratio: float,
    terrestrial_mean_ratio: float,
    terrestrial_std_dev: float
) -> Tuple[float, bool]:
    """
    Non-terrestrial synthetic material must deviate >= 10 sigma from
    terrestrial / solar-system stable-isotope fractionation lines.
    Returns (sigma_deviation, is_extraterrestrial_at_10_sigma).
    """
    if terrestrial_std_dev <= 0.0:
        raise ValueError("terrestrial_std_dev must be positive")
    sigma = abs(measured_ratio - terrestrial_mean_ratio) / terrestrial_std_dev
    return sigma, sigma >= 10.0


# ================================================================== #
# ADVANCE 1: Q1 STATISTICAL POWER - what does ">= 1 of 30" actually   #
# buy?  The previous prediction was stated but never derived.          #
# ================================================================== #
EARTH_OCEAN_MASS_KG: float = 1.4e21            # ~1.335e9 km3 x 1000 kg/m3
MOLAR_MASS_H2O_KG_PER_MOL: float = 18.01528e-3
MOLAR_MASS_H_KG_PER_MOL: float = 1.00794e-3
MOLAR_MASS_O2_KG_PER_MOL: float = 31.9988e-3
EARTH_MEAN_RADIUS_M: float = 6371.0e3
EARTH_SURFACE_AREA_M2: float = 4.0 * math.pi * EARTH_MEAN_RADIUS_M ** 2
SECONDS_PER_YEAR: float = 3.15576e7

# Occurrence of Earth-size temperate planets on FGK stars.
# Hsu et al. 2019 (AJ, DOI 10.3847/1538-3881/ab31ab): eta_+ = 0.37 (+0.19/-0.21)
# for the conservative HZ.  Used as a PRIOR, never as evidence of an outcome.
ETA_EARTH_CONSERVATIVE: float = 0.37
# FGK fraction of the local stellar census and total stellar density from
# RECONS-style 10 pc counts (~360 stars/10 pc => ~0.086 pc^-3, ~27% FGK).
LOCAL_STARS_PER_PC3: float = 0.0859
LOCAL_FGK_FRACTION: float = 0.27


def biosignature_detection_power(f_life: float, n_surveyed: int) -> float:
    """
    Probability that >= 1 biosphere is detected among `n_surveyed` rocky
    temperate HZ planets, given true prevalence f_life.
        P(>=1) = 1 - (1 - f)^N
    Independent-planet binomial model (independence is an idealisation).
    """
    if not 0.0 <= f_life <= 1.0:
        raise ValueError("f_life must lie in [0, 1]")
    if n_surveyed < 0:
        raise ValueError("n_surveyed must be non-negative")
    if f_life == 0.0:
        return 0.0
    if f_life == 1.0:
        return 1.0
    return 1.0 - (1.0 - f_life) ** n_surveyed


def required_sample_for_power(f_life: float, target_power: float = 0.90) -> int:
    """
    Smallest N with P(>=1 detection) >= target_power.
        N = ceil( ln(1 - power) / ln(1 - f) )
    """
    if not 0.0 <= f_life <= 1.0:
        raise ValueError("f_life must lie in [0, 1]")
    if not 0.0 < target_power < 1.0:
        raise ValueError("target_power must lie in (0, 1)")
    if f_life == 0.0:
        raise ValueError("f_life = 0 is undetectable: no finite N reaches the power")
    if f_life == 1.0:
        return 1
    return max(1, math.ceil(math.log(1.0 - target_power) / math.log(1.0 - f_life)))


def null_result_upper_limit(n_nulls: int, confidence: float = 0.95) -> float:
    """
    One-sided exact (Clopper-Pearson style) 95% upper bound on f_life given
    `n_nulls` consecutive null atmospheres and zero detections:
        f_upper = 1 - (1 - C)^(1/n)
    """
    if n_nulls < 1:
        raise ValueError("n_nulls must be >= 1")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must lie in (0, 1)")
    return 1.0 - (1.0 - confidence) ** (1.0 / n_nulls)


def null_sample_for_upper_limit(f_bound: float, confidence: float = 0.95) -> int:
    """
    Number of consecutive nulls needed to push the 95% upper bound below f_bound:
        n = ceil( ln(1 - C) / ln(1 - f) )
    """
    if not 0.0 < f_bound < 1.0:
        raise ValueError("f_bound must lie in (0, 1)")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must lie in (0, 1)")
    return max(1, math.ceil(math.log(1.0 - confidence) / math.log(1.0 - f_bound)))


def accessible_rocky_hz_planets(
    radius_pc: float,
    eta_earth: float = ETA_EARTH_CONSERVATIVE,
    fgk_fraction: float = LOCAL_FGK_FRACTION,
    stars_per_pc3: float = LOCAL_STARS_PER_PC3
) -> Dict[str, float]:
    """
    Supply of rocky temperate HZ planets around FGK stars inside `radius_pc`.
    This is a TARGET-SUPPLY estimate, not a count of surveyed planets.
    """
    volume_pc3 = (4.0 / 3.0) * math.pi * radius_pc ** 3
    n_stars = stars_per_pc3 * volume_pc3
    n_fgk = fgk_fraction * n_stars
    n_hz = eta_earth * n_fgk
    return {
        "radius_pc": radius_pc,
        "volume_pc3": volume_pc3,
        "n_stars": n_stars,
        "n_fgk_stars": n_fgk,
        "n_rocky_hz_planets": n_hz,
    }


def biosignature_census_power(
    n_surveyed: int = 30,
    confidence: float = 0.95,
    n_hz_rocky_in_galaxy: float = 4.0e10
) -> Dict[str, Any]:
    """
    Power audit of the Q1 prediction.  Answers: how much does an N-planet
    survey buy, and what does a null actually rule out?
    """
    power_at_10pct = biosignature_detection_power(0.10, n_surveyed)
    power_at_5pct = biosignature_detection_power(0.05, n_surveyed)
    power_at_1pct = biosignature_detection_power(0.01, n_surveyed)
    power_at_2pct = biosignature_detection_power(0.02, n_surveyed)
    n_for_90 = required_sample_for_power(0.10, 0.90)
    n_for_90_rare = required_sample_for_power(0.02, 0.90)
    f_upper_30 = null_result_upper_limit(max(1, n_surveyed), confidence)
    n_for_1pct = null_sample_for_upper_limit(0.01, confidence)
    f_upper_1pct = null_result_upper_limit(n_for_1pct, confidence)

    # A null does NOT establish aloneness - only rarity.
    max_biospheres_galaxy = f_upper_1pct * n_hz_rocky_in_galaxy

    return {
        "n_surveyed": n_surveyed,
        "detection_power_if_f_0.10": power_at_10pct,
        "detection_power_if_f_0.05": power_at_5pct,
        "detection_power_if_f_0.02": power_at_2pct,
        "detection_power_if_f_0.01": power_at_1pct,
        "n_required_for_90pct_power_at_f_0.10": n_for_90,
        "n_required_for_90pct_power_at_f_0.02": n_for_90_rare,
        "nulls_required_for_f_life_below_0.01_at_95pct": n_for_1pct,
        "f_life_upper_95pct_after_stated_null_census": f_upper_30,
        "f_life_upper_95pct_after_deep_census": f_upper_1pct,
        "galaxy_wide_biosphere_bound_after_deep_census": max_biospheres_galaxy,
        "assumed_hz_rocky_planets_in_galaxy": n_hz_rocky_in_galaxy,
    }


# ================================================================== #
# ADVANCE 2: ABIOTIC O2 BUDGET - why O2 alone is a weak biosignature    #
# Derived here from first principles; literature anchor:               #
#   Luger & Barnes 2015 (Astrobiology, DOI 10.1089/ast.2014.1231)      #
# ================================================================== #
def abiotic_o2_budget(
    n_oceans_lost: float = 1.0,
    escape_as_hydrogen: str = "H2"
) -> Dict[str, float]:
    """
    How much O2 is left behind when a planet loses `n_oceans_lost` Earth oceans
    of water during (e.g.) an M-dwarf pre-main-sequence runaway greenhouse?

    Stoichiometry:  H2O -> H2 + 1/2 O2, so 1 mol of lost water leaves
    0.5 mol of O2 behind (escape of H as atomic H gives the same yield).
    The O2 partial pressure follows from hydrostatics:
        p = m_column * g  (column = total O2 mass / planetary area)
    """
    if n_oceans_lost < 0.0:
        raise ValueError("n_oceans_lost must be non-negative")
    n_h2o_mol = n_oceans_lost * EARTH_OCEAN_MASS_KG / MOLAR_MASS_H2O_KG_PER_MOL
    n_o2_mol = 0.5 * n_h2o_mol
    o2_mass_kg = n_o2_mol * MOLAR_MASS_O2_KG_PER_MOL
    column_kg_m2 = o2_mass_kg / EARTH_SURFACE_AREA_M2
    p_o2_bar = column_kg_m2 * G_EARTH / 1.0e5

    h_escaped_kg = n_h2o_mol * MOLAR_MASS_H_KG_PER_MOL * 2.0   # 2 H per H2O

    return {
        "oceans_lost": n_oceans_lost,
        "o2_moles_produced": n_o2_mol,
        "o2_mass_kg": o2_mass_kg,
        "o2_column_kg_per_m2": column_kg_m2,
        "o2_partial_pressure_bar": p_o2_bar,
        "hydrogen_escaped_kg": h_escaped_kg,
        "ocean_equivalent_remaining_water_kg": EARTH_OCEAN_MASS_KG - n_oceans_lost * EARTH_OCEAN_MASS_KG,
    }


def abiotic_o2_timescale_years(
    target_o2_bar: float = 0.21,
    available_years: float = 1.0e9,
    n_oceans_lost: float = 1.0
) -> Dict[str, float]:
    """
    Required mean hydrogen escape rate to build `target_o2_bar` abiotically
    inside `available_years` (the ~0.1-1 Gyr pre-main-sequence phase of an
    M dwarf).  Compare with Earth's present H escape rate of ~3 kg/s.
    """
    if target_o2_bar <= 0.0 or available_years <= 0.0:
        raise ValueError("target_o2_bar and available_years must be positive")
    if n_oceans_lost <= 0.0:
        raise ValueError("n_oceans_lost must be positive")
    budget = abiotic_o2_budget(n_oceans_lost)
    available_o2_bar = budget["o2_partial_pressure_bar"]
    if target_o2_bar > available_o2_bar:
        raise ValueError(
            f"target_o2_bar={target_o2_bar} exceeds the {available_o2_bar:.1f} bar "
            f"available from {n_oceans_lost} ocean(s)"
        )
    fraction_of_oceans_needed = target_o2_bar / available_o2_bar
    water_mass_to_lose_kg = fraction_of_oceans_needed * n_oceans_lost * EARTH_OCEAN_MASS_KG
    hydrogen_mass_to_lose_kg = (
        water_mass_to_lose_kg / MOLAR_MASS_H2O_KG_PER_MOL * MOLAR_MASS_H_KG_PER_MOL * 2.0
    )
    required_h_escape_kg_per_s = hydrogen_mass_to_lose_kg / (available_years * SECONDS_PER_YEAR)

    # Earth's present-day hydrogen escape rate, ~3 kg/s (Jeans + charge exchange).
    earth_present_h_escape_kg_per_s = 3.0

    return {
        "target_o2_bar": target_o2_bar,
        "available_years": available_years,
        "fraction_of_one_ocean_needed": fraction_of_oceans_needed,
        "water_mass_to_lose_kg": water_mass_to_lose_kg,
        "required_h_escape_kg_per_s": required_h_escape_kg_per_s,
        "earth_present_h_escape_kg_per_s": earth_present_h_escape_kg_per_s,
        "required_to_present_earth_ratio": required_h_escape_kg_per_s / earth_present_h_escape_kg_per_s,
    }


def o2_is_weak_standalone_biosignature(
    earth_o2_bar: float = 0.21, n_oceans: float = 1.0
) -> Dict[str, Any]:
    """
    The abiotic O2 reservoir available per ocean-loss event dwarfs Earth's
    entire biosynthetic O2 inventory, so O2 abundance alone carries almost no
    discriminative weight.  The CO / CH4 companion gate carries it.
    """
    budget = abiotic_o2_budget(n_oceans)
    abiotic_pool_bar = budget["o2_partial_pressure_bar"]
    return {
        "earth_o2_bar": earth_o2_bar,
        "abiotic_o2_pool_per_ocean_bar": abiotic_pool_bar,
        "pool_to_earth_inventory_ratio": abiotic_pool_bar / earth_o2_bar,
        "fraction_of_ocean_needed_for_earth_like_o2": earth_o2_bar / abiotic_pool_bar,
        "o2_alone_is_discriminative": False,
    }


# ================================================================== #
# ADVANCE 3: Q2 NULL-SURVEY POWER - why the null result is weak         #
# ================================================================== #
def technosignature_null_power(
    n_targets: int = 1_000_000,
    confidence: float = 0.95,
    search_radius_pc: float = 100.0,
    stars_per_pc3: float = LOCAL_STARS_PER_PC3,
    eirp_threshold_w: float = 1.0e12
) -> Dict[str, Any]:
    """
    What does a null SETI survey of `n_targets` stars actually bound?

        f_T,upper = 1 - (1 - C)^(1/n_targets)

    The binding constraint is the TARGET LIST: to bound the fraction of
    transmitting stars below 1e-9 at 95% confidence requires >= 1e9 targets,
    so the null result cannot, even in principle, be pushed to a strong
    constraint within the searched volume.
    """
    if n_targets < 1:
        raise ValueError("n_targets must be >= 1")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must lie in (0, 1)")
    f_upper = null_result_upper_limit(n_targets, confidence)
    searched_volume_pc3 = (4.0 / 3.0) * math.pi * search_radius_pc ** 3
    n_stars_available = stars_per_pc3 * searched_volume_pc3
    target_list_ratio = n_targets / n_stars_available
    max_transmitters_in_volume = f_upper * n_stars_available
    galaxy_stars = 1.0e11
    targets_for_1e_9 = null_sample_for_upper_limit(1.0e-9, confidence)

    return {
        "n_targets": n_targets,
        "confidence": confidence,
        "search_radius_pc": search_radius_pc,
        "eirp_threshold_w": eirp_threshold_w,
        "f_transmitting_upper_95pct": f_upper,
        "searched_volume_pc3": searched_volume_pc3,
        "n_stars_in_searched_volume": n_stars_available,
        "targets_per_available_star": target_list_ratio,
        "max_expected_transmitters_in_volume": max_transmitters_in_volume,
        "target_list_binding_constraint": target_list_ratio > 1.0,
        "targets_needed_for_f_below_1e-9": targets_for_1e_9,
        "galaxy_stars_assumed": galaxy_stars,
    }


# ================================================================== #
# SYNTHESIS: falsifiable predictions + settling observations          #
# ================================================================== #
def analyze() -> Dict[str, Any]:
    """
    Phase 2 entry point. Returns {domain, claims, confidence, evidence}.
    Each of the three questions carries a falsifiable prediction and the
    observation that would settle it. No discovery is asserted.
    """
    # ---- Q1 quantitative core ----
    hz_sun = kopparapu_habitable_zone(5778.0, 1.0)
    bio = ch4_o2_disequilibrium()
    bio_abiotic = ch4_o2_disequilibrium(co_mixing_ratio=1.0e-5, o2_mixing_ratio=0.21)

    # ---- Q2 quantitative core ----
    drake_mc = drake_equation_monte_carlo(n_samples=20000)
    haystack = cosmic_haystack_fraction()

    # ---- Q3 quantitative core ----
    kin01 = relativistic_isp_cost(0.10)
    bayes = visitation_posterior()

    # ---- ADVANCE: quantitative power / budget audits ----
    power_q1 = biosignature_census_power(n_surveyed=30)
    supply_30pc = accessible_rocky_hz_planets(30.0)
    o2_budget = abiotic_o2_budget(1.0)
    o2_weak = o2_is_weak_standalone_biosignature()
    o2_clock = abiotic_o2_timescale_years(0.21, 1.0e9, 1.0)
    null_q2 = technosignature_null_power(1_000_000)

    claims: List[str] = [
        # Q1 - life elsewhere: plausible, investigable
        (
            f"Q1 (life elsewhere) is PLAUSIBLE and INVESTIGABLE, not confirmed: with "
            f"{CONFIRMED_EXOPLANET_COUNT}+ confirmed exoplanets and the Kopparapu et al. (2013) "
            f"habitable zone placing Earth's sole HZ between "
            f"{hz_sun['runaway_greenhouse']:.2f} and {hz_sun['maximum_greenhouse']:.2f} AU "
            f"(optimistic {hz_sun['recent_venus']:.2f}-{hz_sun['early_mars']:.2f} AU), the basic "
            f"planetary substrate is common. An Earth-like atmosphere with f_CH4 = 1.8e-6 and "
            f"f_O2 = 0.21 is thermodynamically disequilibrated at "
            f"{bio['delta_g_actual_kj_per_mol']:.1f} kJ/mol for CH4 + 2 O2 -> CO2 + 2 H2O and "
            f"demands a sustained CH4 source of ~{bio['required_biogenic_flux_molecules_per_m2_s']:.1e} "
            f"molecules m^-2 s^-1; the falsifiable prediction is that >= 1 of 30 rocky temperate "
            f"HZ planets shows coupled CH4+O2 with f_CO/f_O2 < 0.05 above 5 sigma, and the settling "
            f"observation is high-resolution ELT/HWO transit + direct-imaging spectroscopy that "
            f"excludes abiotic CO-photolysis and desiccation mimics."
        ),
        (
            "Q1 falsification criterion: a census of >= 100 temperate HZ terrestrial planets showing "
            "only equilibrium or abiotic-photochemistry atmospheres (high CO, desiccated) would "
            "falsify common biogenesis (f_l >= 1e-2) in the local stellar neighbourhood."
        ),
        # Q2 - intelligent life: undecidable
        (
            f"Q2 (intelligent life) is UNDECIDABLE, and the Fermi paradox is partly an artefact of "
            f"epistemic variance: dragging the Drake equation through Sandberg-Drexler-Ord log-uniform "
            f"priors over f_l (1e-5..1), f_i (1e-4..0.5), f_c (1e-2..0.5) and L (1e2..1e7 yr) yields "
            f"P(N < 1) = {drake_mc['p_alone_in_galaxy']:.2f} with 5-95th percentile N spanning "
            f"{drake_mc['percentile_5']:.2e} to {drake_mc['percentile_95']:.2e} - humanity could be "
            f"alone with no exotic mechanism required. Only {haystack['total_haystack_fraction_searched']:.1e} "
            f"(log10 = {haystack['log10_total_fraction']:.1f}) of the 8-dimensional cosmic haystack has "
            f"been searched. Prediction: if communicative civilizations with L >= 1e5 yr exist, an "
            f"all-sky 1-10 GHz survey to EIRP 1e12 W within 100 pc detects >= 1 narrowband "
            f"(delta-nu < 5 Hz) drifting signal; the settling observation is a locally repeated, "
            f"multi-observatory-confirmed modulated signal or a non-spherical Dyson-swarm transit."
        ),
        (
            "Q2 falsification criterion: an exhaustive all-sky survey of ~1e6 stars within 100 pc over "
            "1-10 GHz to EIRP 1e12 W with null results bounds local civilizational density to "
            "n_civ < 1e-6 pc^-3 - a decisive, achievable constraint, not an appeal to mystery."
        ),
        # Q3 - visitation: unsupported
        (
            f"Q3 (visitation) is UNSUPPORTED and REJECTED under the null hypothesis. Relativistic "
            f"kinetics prices any interstellar visit: at beta = 0.10 the specific energy is "
            f"{kin01['specific_kinetic_energy_j_per_kg']:.2e} J/kg "
            f"({kin01['specific_kinetic_energy_kilotons_tnt_per_kg']:.0f} kT TNT/kg) and a fusion "
            f"flyby needs mass ratio R = {kin01['fusion_mass_ratio_one_way']:.1f} "
            f"(round-trip R = {kin01['fusion_mass_ratio_round_trip']:.1f}); an ideal antimatter "
            f"rocket still needs R = {kin01['antimatter_mass_ratio_one_way']:.2f}. No calibrated "
            f"multi-modal sensor trace and no isotopic artefact > 10 sigma from terrestrial "
            f"fractionation lines has ever passed review. Falsifiable prediction: if ET technology "
            f"has operated in the Earth-Moon system, debris with > 10 sigma non-solar isotopic "
            f"fractionation exists; the settling observation is TEM/mass-spectrometry of recovered "
            f"material plus synchronized optical-radar-IR telemetry of > 100 g atmospheric manoeuvres "
            f"without shockwave or plume."
        ),
        (
            f"Q3 Bayesian discipline applied to a typical 'unexplained observation' with a generous "
            f"prior P(visit) = 1e-9 and a flattering Bayes factor of "
            f"{bayes['bayes_factor']:.0f} still yields posterior P(ET | data) = "
            f"{bayes['posterior']:.1e}: anecdotes are information-theoretically incapable, by "
            f"themselves, of establishing visitation."
        ),
        # ---- ADVANCE claims: statistical power and abiotic-O2 budget ----
        (
            f"Q1 POWER AUDIT (new): the '>= 1 of 30' prediction is well powered only for "
            f"COMMON biospheres. At true prevalence f_life = 0.10 a 30-planet survey has "
            f"{power_q1['detection_power_if_f_0.10']:.0%} power, but at f_life = 0.05 it falls to "
            f"{power_q1['detection_power_if_f_0.05']:.0%}, at 0.02 to "
            f"{power_q1['detection_power_if_f_0.02']:.0%}, and at f_life = 0.01 to "
            f"{power_q1['detection_power_if_f_0.01']:.0%}. Holding 90% power for a RARE biosphere "
            f"(f_life = 0.02) needs {power_q1['n_required_for_90pct_power_at_f_0.02']} surveyed "
            f"atmospheres, and pushing the 95% null upper bound below f_life = 0.01 needs "
            f"{power_q1['nulls_required_for_f_life_below_0.01_at_95pct']} consecutive nulls. "
            f"Target supply is NOT the bottleneck: "
            f"{supply_30pc['n_rocky_hz_planets']:.0f} rocky temperate HZ planets orbit FGK stars "
            f"within 30 pc (eta_+ = {ETA_EARTH_CONSERVATIVE}, Hsu et al. 2019), "
            f"{supply_30pc['n_rocky_hz_planets'] / power_q1['nulls_required_for_f_life_below_0.01_at_95pct']:.1f}x "
            f"the required census - atmospheric sensitivity is. Critically, even a 299-planet null "
            f"bounds only {power_q1['galaxy_wide_biosphere_bound_after_deep_census']:.1e} of "
            f"~{power_q1['assumed_hz_rocky_planets_in_galaxy']:.0e} galaxy-wide HZ planets, so a "
            f"null establishes RARITY, never ALONENESS."
        ),
        (
            f"Q1 ABIOTIC-O2 BUDGET (new, first-principles): O2 abundance alone is a WEAK "
            f"biosignature, so Q1's prediction must stay coupled to the CO/CH4 gate. Loss of a "
            f"single Earth ocean of water with hydrogen escaping as H2 leaves behind "
            f"{o2_budget['o2_partial_pressure_bar']:.0f} bar of O2 (stoichiometry H2O -> H2 + 1/2 O2, "
            f"p = m_column g), which is {o2_weak['pool_to_earth_inventory_ratio']:.0f}x Earth's "
            f"ENTIRE biosynthetic O2 inventory of {o2_weak['earth_o2_bar']:.2f} bar. Earth-like "
            f"abiotic O2 therefore needs only "
            f"{o2_weak['fraction_of_ocean_needed_for_earth_like_o2']:.1e} of an ocean, i.e. a mean "
            f"hydrogen escape rate of just {o2_clock['required_h_escape_kg_per_s']:.1f} kg/s sustained "
            f"for {o2_clock['available_years']:.0e} yr - "
            f"{o2_clock['required_to_present_earth_ratio']:.1f}x Earth's PRESENT escape rate of "
            f"~{o2_clock['earth_present_h_escape_kg_per_s']:.0f} kg/s. An abiotic O2 mono-detection "
            f"would settle nothing; the CO companion is the discriminator."
        ),
        (
            f"Q2 NULL-SURVEY POWER (new): the Fermi null is even weaker than the haystack "
            f"argument suggests, because of the TARGET-LIST ceiling. A 95% null survey of "
            f"{null_q2['n_targets']:.0e} stars bounds the fraction of transmitting stars to "
            f"f_T < {null_q2['f_transmitting_upper_95pct']:.1e} - which, over the "
            f"{null_q2['searched_volume_pc3']:.1e} pc^3 searched volume "
            f"(~{null_q2['n_stars_in_searched_volume']:.0e} stars), still permits "
            f"~{null_q2['max_expected_transmitters_in_volume']:.1f} transmitters. The requested "
            f"1e6-star survey is already {null_q2['targets_per_available_star']:.1f}x larger than the "
            f"real 100 pc census, so the null cannot be strengthened by surveying the same volume "
            f"again; reaching f_T < 1e-9 requires "
            f"~{null_q2['targets_needed_for_f_below_1e-9']:.0e} targets. Q2 is therefore "
            f"UNDECIDABLE in practice, not merely in principle."
        ),
    ]

    confidence: float = 0.90

    evidence: List[Dict[str, Any]] = [
        {
            "kind": "exoplanet_census",
            "value": {"confirmed_exoplanets": CONFIRMED_EXOPLANET_COUNT,
                      "era": "mid-2020s"},
            "source": "NASA Exoplanet Archive"
        },
        {
            "kind": "habitable_zone_bounds",
            "value": hz_sun,
            "source": "Kopparapu et al. 2013/2014 (ApJ 765, 770) conservative HZ polynomials"
        },
        {
            "kind": "biosignature_disequilibrium",
            "value": {"earth_like": bio, "abiotic_co_rich_control": bio_abiotic},
            "source": "Reaction Gibbs energy CH4 + 2 O2 -> CO2 + 2 H2O (Delta G' = -801 kJ/mol); "
                      "photochemical CO as the abiotic false-positive gate"
        },
        {
            "kind": "drake_monte_carlo_uncertainty",
            "value": drake_mc,
            "source": "Sandberg, Drexler & Ord 2018 (arXiv:1806.02404) prior treatment"
        },
        {
            "kind": "cosmic_haystack_search_fraction",
            "value": haystack,
            "source": "Wright et al. 2018, 8-D SETI haystack parameterisation"
        },
        {
            "kind": "relativistic_visitation_energy",
            "value": kin01,
            "source": "E/m = (gamma-1)c^2; relativistic Tsiolkovsky (Ackeret 1946) mass-ratio law"
        },
        {
            "kind": "bayesian_visitation_posterior",
            "value": bayes,
            "source": "Bayes' theorem with stacked priors (prior 1e-9, BF 900)"
        },
        {
            "kind": "falsifiable_prediction",
            "value": {
                "question": "Q1: does life exist elsewhere?",
                "prediction": ">= 1 of 30 rocky temperate HZ planets surveyed shows "
                              "coupled CH4 + O2 (f_CH4 > 1e-6, f_O2 > 1e-3) with "
                              "f_CO/f_O2 < 0.05 at >= 5 sigma above abiotic photochemical ceilings.",
                "settling_observation": "ELT/HWO transit + direct-imaging spectroscopy with "
                                        "photochemical abiotic mimics excluded, or in situ "
                                        "mass spectrometry of Europa/Enceladus plume organics."
            },
            "source": "This engine, Q1"
        },
        {
            "kind": "falsifiable_prediction",
            "value": {
                "question": "Q2: does intelligent life exist?",
                "prediction": "If L >= 1e5 yr civilizations exist, an all-sky 1-10 GHz survey to "
                              "EIRP 1e12 W within 100 pc detects >= 1 narrowband drifting signal.",
                "settling_observation": "Locally repeated, modulated narrowband signal confirmed "
                                        "at >= 2 separated observatories, or a Dyson-swarm "
                                        "non-spherical transit lightcurve."
            },
            "source": "This engine, Q2"
        },
        {
            "kind": "falsifiable_prediction",
            "value": {
                "question": "Q3: has it visited Earth?",
                "prediction": "If ET technology has operated in the Earth-Moon system, physical "
                              "debris with > 10 sigma non-solar isotopic fractionation and "
                              "engineered microarchitecture exists.",
                "settling_observation": "TEM/mass-spectrometry of recovered material, plus "
                                        "synchronized optical-radar-IR telemetry of sustained "
                                        "> 100 g manoeuvres without acoustic shockwave."
            },
            "source": "This engine, Q3"
        },
        {
            "kind": "q1_power_analysis",
            "value": power_q1,
            "source": "Exact binomial detection power and Clopper-Pearson null upper "
                      "limits, P(>=1) = 1-(1-f)^N; model inputs eta_+ = 0.37 from "
                      "Hsu et al. 2019 (AJ, DOI 10.3847/1538-3881/ab31ab)"
        },
        {
            "kind": "q1_abiotic_o2_budget",
            "value": {
                "per_ocean_budget": o2_budget,
                "weak_discrimination": o2_weak,
                "o2_buildup_clock": o2_clock,
            },
            "source": "First-principles stoichiometry (1 mol H2O -> 0.5 mol O2) plus "
                      "hydrostatics p = m_col g; literature anchor Luger & Barnes 2015 "
                      "(Astrobiology, DOI 10.1089/ast.2014.1231)"
        },
        {
            "kind": "q2_null_survey_power",
            "value": null_q2,
            "source": "Exact binomial null upper bound on the transmitting-star "
                      "fraction; local stellar density from RECONS-style 10 pc census"
        },
    ]

    return {
        "domain": "extraterrestrial",
        "claims": claims,
        "confidence": confidence,
        "evidence": evidence,
    }


if __name__ == "__main__":
    result = analyze()
    print(f"Domain:     {result['domain']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Claims:     {len(result['claims'])}")
    print(f"Evidence:   {len(result['evidence'])} entries")
