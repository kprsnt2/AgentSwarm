"""
Extraterrestrial Life and Technosignature Epistemic Analysis Engine
Agent: Agent5 (A006, Gen 0)
Domain: Are aliens real? (extraterrestrial)
Epistemic Class: Exploratory

This module provides first-principles physical, chemical, thermodynamic,
astronomical, and statistical models strictly demarcating three independent questions:
  1. Does life exist elsewhere (Biogenesis & Biospheres)
  2. Does intelligent life exist (Technosignatures & The Fermi Paradox)
  3. Has it visited Earth (Physical Artefacts & Relativistic Interstellar Kinematics)

Standard of Evidence:
  - Falsifiable predictions with exact settling observations.
  - No assertion of discovery.
  - No substitution of plausibility for evidence.
"""

import math
import random
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any, Optional

# ==============================================================================
# PHYSICAL, CHEMICAL, AND ASTRONOMICAL CONSTANTS (CODATA 2018 / IAU / NIST)
# ==============================================================================
C: float = 299792458.0                     # Speed of light in vacuum (m/s)
G: float = 6.67430e-11                     # Gravitational constant (m^3 / kg s^2)
HBAR: float = 1.054571817e-34              # Reduced Planck constant (J s)
H_PLANCK: float = 6.62607015e-34           # Planck constant (J s)
K_B: float = 1.380649e-23                  # Boltzmann constant (J / K)
N_A: float = 6.02214076e23                 # Avogadro constant (mol^-1)
R_GAS: float = 8.314462618                 # Universal gas constant (J / mol K)
SIGMA_SB: float = 5.670374419e-8           # Stefan-Boltzmann constant (W / m^2 K^4)
WIEN_B: float = 2.897771955e-3             # Wien displacement constant (m K)

# Astronomical Constants
AU: float = 1.495978707e11                 # Astronomical Unit (m)
PARSEC: float = 3.085677581e16             # Parsec (m)
LIGHT_YEAR: float = 9.460730472e15         # Light year (m)
M_SUN: float = 1.98847e30                  # Solar mass (kg)
L_SUN: float = 3.828e26                    # Solar luminosity (W)
R_SUN: float = 6.957e8                     # Solar radius (m)
T_EFF_SUN: float = 5778.0                  # Solar effective temperature (K)
M_EARTH: float = 5.9722e24                 # Earth mass (kg)
R_EARTH: float = 6.371e6                   # Earth mean radius (m)
P_EARTH_SURF: float = 101325.0             # Earth surface pressure (Pa = 1 atm)
G_EARTH: float = 9.80665                   # Earth standard surface gravity (m/s^2)

# Interstellar Medium Constants
RHO_ISM: float = 1.67e-21                  # Typical ISM density (kg/m^3 ~ 1 H atom / cm^3)


# ==============================================================================
# DATA CLASSES FOR STRUCTURED MODEL RESULTS
# ==============================================================================
@dataclass(frozen=True)
class HabitableZoneBoundaries:
    """Circumstellar Habitable Zone boundaries in Astronomical Units (AU)."""
    stellar_teff: float
    stellar_luminosity_solar: float
    recent_venus_au: float
    runaway_greenhouse_au: float
    maximum_greenhouse_au: float
    early_mars_au: float

    @property
    def conservative_width_au(self) -> float:
        return self.maximum_greenhouse_au - self.runaway_greenhouse_au

    @property
    def optimistic_width_au(self) -> float:
        return self.early_mars_au - self.recent_venus_au


@dataclass(frozen=True)
class ChemicalDisequilibriumResult:
    """Atmospheric chemical thermodynamic disequilibrium metrics."""
    temperature_k: float
    pressure_bar: float
    delta_g_standard_kj_per_mol: float
    delta_g_actual_kj_per_mol: float
    methane_mixing_ratio: float
    oxygen_mixing_ratio: float
    photochemical_flux_molecules_per_m2_s: float
    is_thermodynamically_disequilibrium: bool
    abiotic_explanation_plausible: bool
    confidence_description: str


@dataclass(frozen=True)
class DrakeEquationMonteCarlo:
    """Probabilistic distribution of communicative civilizations in Milky Way."""
    median_n: float
    mean_n: float
    p_alone_in_galaxy: float                # P(N < 1)
    p_multiple_civilizations: float         # P(N >= 2)
    percentile_5: float
    percentile_95: float
    sample_size: int


@dataclass(frozen=True)
class CosmicHaystackFraction:
    """Wright et al. 8-dimensional technosignature search space metric."""
    volume_searched_fraction: float
    frequency_coverage_fraction: float
    eirp_sensitivity_fraction: float
    polarization_fraction: float
    repetition_fraction: float
    total_haystack_fraction_searched: float
    log10_haystack_fraction: float


@dataclass(frozen=True)
class RelativisticKinematicsResult:
    """Relativistic interstellar journey physics and energy requirements."""
    beta: float                              # v / c
    gamma: float                             # Lorentz factor
    kinetic_energy_per_kg: float             # J / kg
    tnt_kilotons_per_kg: float               # kT TNT / kg (1 kT = 4.184e12 J)
    tnt_megatons_per_kg: float               # MT TNT / kg (1 MT = 4.184e15 J)
    travel_time_proxima_years: float         # Proxima Centauri (4.2465 ly) observer frame
    proper_time_proxima_years: float         # Ship frame proper time
    ism_stagnation_pressure_pa: float        # Stagnation pressure against ISM (Pa)
    ism_power_flux_w_per_m2: float           # Kinetic energy flux from ISM (W / m^2)
    micro_dust_impact_energy_j: float        # Impact energy of a 1-micron dust grain (J)
    fusion_mass_ratio_one_way: float         # Relativistic rocket mass ratio (ve = 0.05c)
    antimatter_mass_ratio_one_way: float     # Ideal antimatter rocket mass ratio (ve = c)


@dataclass(frozen=True)
class BayesianVisitationEvaluation:
    """Bayesian hypothesis testing of purported extraterrestrial visitation."""
    prior_probability: float                 # Prior P(ET visit)
    likelihood_evidence_given_et: float      # P(Data | ET visit)
    likelihood_evidence_given_null: float    # P(Data | Sensor artifact / mundane)
    bayes_factor: float
    posterior_probability: float
    epistemic_conclusion: str


# ==============================================================================
# QUESTION 1: DOES LIFE EXIST ELSEWHERE (BIOGENESIS & BIOSPHERES)
# ==============================================================================
class BiogenesisBiosphereModel:
    """
    Physical and chemical framework for assessing extraterrestrial biogenesis,
    circumstellar habitable zones, atmospheric biosignatures, and abiotic mimics.
    """

    @staticmethod
    def calculate_habitable_zone(
        stellar_teff_k: float,
        stellar_luminosity_solar: float
    ) -> HabitableZoneBoundaries:
        """
        Calculates Circumstellar Habitable Zone boundaries using Kopparapu et al. (2013, 2014)
        polynomial coefficients for 2600 K <= Teff <= 7200 K.
        """
        t_star = stellar_teff_k - 5780.0

        # Kopparapu et al. (2014) coefficients for terrestrial planets (1 Earth mass)
        # S_eff = S_eff_sun + a*T* + b*T*^2 + c*T*^3 + d*T*^4
        coefficients = {
            "recent_venus": (1.7763, 1.4335e-4, 3.3954e-9, -7.6364e-12, -1.1950e-15),
            "runaway_greenhouse": (1.0385, 1.2456e-4, 1.4612e-8, -7.6345e-12, -1.7511e-15),
            "maximum_greenhouse": (0.3507, 5.9578e-5, 1.6707e-9, -3.0058e-12, -5.1925e-16),
            "early_mars": (0.3207, 5.4471e-5, 1.5275e-9, -2.1709e-12, -3.8282e-16),
        }

        s_eff_values = {}
        for boundary, (se_sun, a, b, c, d) in coefficients.items():
            se = se_sun + a * t_star + b * (t_star ** 2) + c * (t_star ** 3) + d * (t_star ** 4)
            s_eff_values[boundary] = max(se, 1e-4)

        # Distance d = sqrt(L_star / S_eff) in AU
        distances = {
            b: math.sqrt(stellar_luminosity_solar / s_eff_values[b])
            for b in coefficients
        }

        return HabitableZoneBoundaries(
            stellar_teff=stellar_teff_k,
            stellar_luminosity_solar=stellar_luminosity_solar,
            recent_venus_au=distances["recent_venus"],
            runaway_greenhouse_au=distances["runaway_greenhouse"],
            maximum_greenhouse_au=distances["maximum_greenhouse"],
            early_mars_au=distances["early_mars"],
        )

    @staticmethod
    def atmospheric_scale_height(
        equilibrium_temp_k: float,
        mean_molecular_weight_amu: float,
        surface_gravity_m_s2: float
    ) -> float:
        """Calculates atmospheric scale height H = k_B * T / (mu * m_u * g) in meters."""
        m_u = 1.66053906660e-27  # Atomic mass constant in kg
        mu_kg = mean_molecular_weight_amu * m_u
        return (K_B * equilibrium_temp_k) / (mu_kg * surface_gravity_m_s2)
    @staticmethod
    def solid_planet_transit_depth(
        planet_radius_m: float,
        stellar_radius_m: float
    ) -> float:
        """Calculates geometric transit depth of the opaque planetary disk: delta_geom = (R_p / R_*)^2."""
        return (planet_radius_m / stellar_radius_m) ** 2

    @staticmethod
    def transmission_spectroscopy_transit_depth(
        planet_radius_m: float,
        stellar_radius_m: float,
        scale_height_m: float,
        n_scale_heights: float = 5.0
    ) -> float:
        """
        Calculates effective atmospheric transit depth signal delta = (2 * R_p * n*H) / R_*^2.
        Represents the spectroscopic signature of atmospheric absorption lines.
        """
        annulus_area = 2.0 * math.pi * planet_radius_m * (n_scale_heights * scale_height_m)
        stellar_area = math.pi * (stellar_radius_m ** 2)
        return annulus_area / stellar_area

    @staticmethod
    def chemical_disequilibrium_ch4_o2(
        ch4_mixing_ratio: float,
        o2_mixing_ratio: float,
        co2_mixing_ratio: float = 4.0e-4,
        h2o_mixing_ratio: float = 1.0e-2,
        co_mixing_ratio: float = 1.0e-7,
        temperature_k: float = 288.15,
        pressure_bar: float = 1.01325
    ) -> ChemicalDisequilibriumResult:
        """
        Quantifies chemical disequilibrium for the reaction:
            CH4 + 2 O2 -> CO2 + 2 H2O
        Standard Gibbs Free Energy: Delta G° = -801.0 kJ/mol (strongly exergonic).
        Delta G = Delta G° + R * T * ln( (a_CO2 * a_H2O^2) / (a_CH4 * a_O2^2) ).
        Evaluates required biogenic flux against photochemical oxidation and tests
        abiotic false-positive indicators (e.g. CO accumulation).
        """
        # Standard free energy change at 298.15 K
        delta_g_std_j_mol = -801.0e3

        # Approximate reaction quotient Q = (p_CO2 * p_H2O^2) / (p_CH4 * p_O2^2)
        p_ch4 = max(ch4_mixing_ratio * pressure_bar, 1e-25)
        p_o2 = max(o2_mixing_ratio * pressure_bar, 1e-25)
        p_co2 = max(co2_mixing_ratio * pressure_bar, 1e-25)
        p_h2o = max(h2o_mixing_ratio * pressure_bar, 1e-25)

        reaction_quotient = (p_co2 * (p_h2o ** 2)) / (p_ch4 * (p_o2 ** 2))
        reaction_quotient = max(reaction_quotient, 1e-30)

        delta_g_actual_j_mol = delta_g_std_j_mol + R_GAS * temperature_k * math.log(reaction_quotient)
        delta_g_actual_kj_mol = delta_g_actual_j_mol / 1000.0

        # Photochemical destruction lifetime of methane in oxidizing atmosphere ~ 10-12 years
        # Atmospheric column density ~ 2.15e29 molecules / m^2 on Earth
        column_density = (pressure_bar * 1e5) / (G_EARTH * 28.97e-3 / N_A)
        tau_photochemical_seconds = 10.0 * 365.25 * 86400.0
        required_flux = (column_density * ch4_mixing_ratio) / tau_photochemical_seconds

        # Abiotic false positive evaluation:
        # 1. Abiotic photolysis of CO2 yields O2 and CO in 1:2 ratio.
        #    If life is present, microbial metabolisms (acetogenesis, methanogenesis) draw CO down (CO < 1e-2).
        # 2. High O2 with high CO (co_mixing_ratio / o2_mixing_ratio > 0.1) points to abiotic runaway photolysis.
        abiotic_plausible = False
        if co_mixing_ratio > 1e-3 and (co_mixing_ratio / p_o2) > 0.05:
            abiotic_plausible = True
        if ch4_mixing_ratio < 1e-7 and o2_mixing_ratio > 0.01:
            # Oxygen without methane can be generated via abiotic water loss / desiccated atmosphere
            abiotic_plausible = True

        disequilibrium = (delta_g_actual_kj_mol < -500.0) and (ch4_mixing_ratio >= 1e-6) and (o2_mixing_ratio >= 1e-3)

        if disequilibrium and not abiotic_plausible:
            desc = "Strong candidate atmospheric biosignature: simultaneous high-disequilibrium CH4+O2 with CO suppressed."
        elif disequilibrium and abiotic_plausible:
            desc = "Ambiguous disequilibrium: abiotic false positive cannot be excluded (elevated CO or water-loss signature)."
        elif not disequilibrium and o2_mixing_ratio > 0.05:
            desc = "Oxygen present without reduced gases: high probability of abiotic runaway photolysis / desiccation."
        else:
            desc = "Equilibrium or trace gases: no evidence of biogenic atmospheric modification."

        return ChemicalDisequilibriumResult(
            temperature_k=temperature_k,
            pressure_bar=pressure_bar,
            delta_g_standard_kj_per_mol=delta_g_std_j_mol / 1000.0,
            delta_g_actual_kj_per_mol=delta_g_actual_kj_mol,
            methane_mixing_ratio=ch4_mixing_ratio,
            oxygen_mixing_ratio=o2_mixing_ratio,
            photochemical_flux_molecules_per_m2_s=required_flux,
            is_thermodynamically_disequilibrium=disequilibrium,
            abiotic_explanation_plausible=abiotic_plausible,
            confidence_description=desc
        )


# ==============================================================================
# QUESTION 2: DOES INTELLIGENT LIFE EXIST (THE FERMI PARADOX & TECHNOSIGNATURES)
# ==============================================================================
class TechnosignatureFermiModel:
    """
    Quantitative framework for the Drake equation, Bayesian distribution of civilization
    frequency, the 8-dimensional Cosmic Haystack search volume, and Dyson megastructure limits.
    """

    @staticmethod
    def drake_equation_point_estimate(
        r_star: float = 1.9,         # Galactic star formation rate (stars/yr)
        f_p: float = 0.95,           # Fraction of stars with planets
        n_e: float = 0.20,           # Habitable zone terrestrial planets per planetary system
        f_l: float = 0.10,           # Fraction of habitable planets that develop life
        f_i: float = 0.01,           # Fraction of biospheres developing intelligence
        f_c: float = 0.10,           # Fraction of intelligent species creating communicative technosignatures
        l_years: float = 10000.0     # Mean duration of communicative phase (years)
    ) -> float:
        """Calculates standard Drake equation point estimate: N = R* * fp * ne * fl * fi * fc * L."""
        return r_star * f_p * n_e * f_l * f_i * f_c * l_years

    @staticmethod
    def drake_equation_monte_carlo(
        n_samples: int = 50000,
        random_seed: int = 42
    ) -> DrakeEquationMonteCarlo:
        """
        Evaluates the Drake Equation over wide log-uniform / log-normal prior distributions
        reflecting genuine epistemic uncertainty (Sandberg, Drexler, & Ord 2018).
        Demonstrates that point estimates disguise enormous epistemic variance, explaining
        how the Fermi paradox naturally resolves into a substantial probability of humanity
        being alone in the Milky Way without requiring exotic mechanisms.
        """
        rng = random.Random(random_seed)
        n_values: List[float] = []
        alone_count = 0

        for _ in range(n_samples):
            # Astronomical parameters: well-constrained by observational astronomy
            r_star = rng.gauss(1.9, 0.4)
            r_star = max(0.5, r_star)

            f_p = rng.uniform(0.9, 1.0)
            n_e = rng.uniform(0.1, 0.4)

            # Epistemic parameters: span orders of magnitude
            # fl: log-uniform from 1e-5 to 1.0
            log_fl = rng.uniform(-5.0, 0.0)
            f_l = 10.0 ** log_fl

            # fi: log-uniform from 1e-4 to 0.5
            log_fi = rng.uniform(-4.0, math.log10(0.5))
            f_i = 10.0 ** log_fi

            # fc: log-uniform from 1e-2 to 0.5
            log_fc = rng.uniform(-2.0, math.log10(0.5))
            f_c = 10.0 ** log_fc

            # L: log-uniform from 1e2 years (100 yr) to 1e7 years (10 Myr)
            log_l = rng.uniform(2.0, 7.0)
            l_years = 10.0 ** log_l

            n_val = r_star * f_p * n_e * f_l * f_i * f_c * l_years
            n_values.append(n_val)

            if n_val < 1.0:
                alone_count += 1

        n_values.sort()
        p_alone = alone_count / n_samples
        p_multiple = 1.0 - p_alone
        median_n = n_values[n_samples // 2]
        mean_n = sum(n_values) / n_samples
        p5 = n_values[int(0.05 * n_samples)]
        p95 = n_values[int(0.95 * n_samples)]

        return DrakeEquationMonteCarlo(
            median_n=median_n,
            mean_n=mean_n,
            p_alone_in_galaxy=p_alone,
            p_multiple_civilizations=p_multiple,
            percentile_5=p5,
            percentile_95=p95,
            sample_size=n_samples
        )

    @staticmethod
    def cosmic_haystack_fraction(
        distance_searched_pc: float = 100.0,
        bandwidth_searched_hz: float = 1.0e9,
        eirp_detection_limit_w: float = 1.0e13,
        sky_fraction_searched: float = 0.05,
        duty_cycle_coverage: float = 1.0e-3
    ) -> CosmicHaystackFraction:
        """
        Quantifies the 8-dimensional SETI 'Cosmic Haystack' search volume fraction
        based on Wright et al. (2018).
        Total space includes:
          - Spatial volume (out to 10 kpc galactic scale)
          - Radio frequency (terrestrial microwave window: 1 - 10 GHz, or 0.1 - 100 GHz)
          - EIRP sensitivity (planetary radar ~1e13 W vs high-power beacon ~1e18 W)
          - Sky coverage (4*pi sr)
          - Temporal duty cycle and polarization.
        """
        galaxy_radius_pc = 10000.0
        total_volume = (4.0 / 3.0) * math.pi * (galaxy_radius_pc ** 3)
        volume_searched = (4.0 / 3.0) * math.pi * (distance_searched_pc ** 3) * sky_fraction_searched
        vol_frac = min(volume_searched / total_volume, 1.0)

        total_rf_bandwidth_hz = 100.0e9  # 0.1 to 100 GHz
        freq_frac = min(bandwidth_searched_hz / total_rf_bandwidth_hz, 1.0)

        # Sensitivity fraction: sensitivity down to 1e13 W relative to isotropic transmitter range
        # Parameterized across dynamic range of 10 orders of magnitude
        eirp_dynamic_range_decades = 10.0
        eirp_covered_decades = max(0.0, min(10.0, (18.0 - math.log10(max(eirp_detection_limit_w, 1.0)))))
        eirp_frac = eirp_covered_decades / eirp_dynamic_range_decades

        polarization_fraction = 0.5  # Typically linear only, missing circular/elliptical

        total_haystack_frac = vol_frac * freq_frac * (eirp_frac * 0.1) * polarization_fraction * duty_cycle_coverage
        total_haystack_frac = max(total_haystack_frac, 1e-30)
        log10_frac = math.log10(total_haystack_frac)

        return CosmicHaystackFraction(
            volume_searched_fraction=vol_frac,
            frequency_coverage_fraction=freq_frac,
            eirp_sensitivity_fraction=eirp_frac,
            polarization_fraction=polarization_fraction,
            repetition_fraction=duty_cycle_coverage,
            total_haystack_fraction_searched=total_haystack_frac,
            log10_haystack_fraction=log10_frac
        )

    @staticmethod
    def dyson_sphere_waste_heat(
        stellar_luminosity_w: float,
        interception_fraction_alpha: float,
        dyson_radius_m: float
    ) -> Tuple[float, float, float]:
        """
        Calculates thermodynamics of a partial/complete Dyson sphere (Kardashev Type II):
          - Total reradiated waste heat power P_waste = alpha * L_star
          - Equilibrium temperature T_eq = ( (alpha * L_star) / (4 * pi * R^2 * sigma_SB) )^(1/4)
          - Peak emission wavelength via Wien's Law: lambda_peak = b / T_eq
        Returns (P_waste_w, T_waste_k, lambda_peak_microns).
        """
        p_waste = interception_fraction_alpha * stellar_luminosity_w
        area = 4.0 * math.pi * (dyson_radius_m ** 2)
        t_waste = ((p_waste) / (area * SIGMA_SB)) ** 0.25
        lambda_peak_m = WIEN_B / max(t_waste, 1.0)
        lambda_peak_microns = lambda_peak_m * 1.0e6
        return p_waste, t_waste, lambda_peak_microns


# ==============================================================================
# QUESTION 3: HAS IT VISITED EARTH (RELATIVISTIC FLIGHT & PHYSICAL ARTEFACTS)
# ==============================================================================
class InterstellarVisitationModel:
    """
    Rigorous physical constraints on extraterrestrial interstellar travel,
    dust sputtering energetics, and Bayesian demarcation of purported visitation evidence.
    """

    @staticmethod
    def relativistic_kinematics(beta: float) -> RelativisticKinematicsResult:
        """
        Computes relativistic kinematics, ISM dust bombardment, and propellant requirements.
        beta = v / c (0 < beta < 1).
        """
        if beta <= 0.0 or beta >= 1.0:
            raise ValueError(f"Beta must be in range (0, 1), received {beta}")

        gamma = 1.0 / math.sqrt(1.0 - beta ** 2)
        kinetic_energy_per_kg = (gamma - 1.0) * (C ** 2)
        tnt_kilotons_per_kg = kinetic_energy_per_kg / 4.184e12
        tnt_megatons_per_kg = kinetic_energy_per_kg / 4.184e15

        # Distance to Proxima Centauri: 4.2465 light years
        dist_proxima_m = 4.2465 * LIGHT_YEAR
        velocity_m_s = beta * C
        travel_time_obs_s = dist_proxima_m / velocity_m_s
        travel_time_obs_yr = travel_time_obs_s / (365.25 * 86400.0)
        proper_time_ship_yr = travel_time_obs_yr / gamma

        # ISM interaction physics
        # Power flux P / A = 0.5 * rho_ISM * v^3 * gamma^2
        ism_power_flux = 0.5 * RHO_ISM * (velocity_m_s ** 3) * (gamma ** 2)
        ism_stagnation_pressure = RHO_ISM * (velocity_m_s ** 2) * gamma

        # 1-micron dust grain impact energy
        # Grain mass: radius = 1e-6 m, density = 2500 kg/m^3 -> m = (4/3)*pi*r^3*rho ~ 1.05e-14 kg
        grain_mass_kg = (4.0 / 3.0) * math.pi * ((1.0e-6) ** 3) * 2500.0
        grain_impact_energy_j = (gamma - 1.0) * grain_mass_kg * (C ** 2)

        # Relativistic rocket equation (Ackeret 1946):
        # M_0 / M_f = ((1 + beta)/(1 - beta))^(c / (2 * v_e))
        # 1. Fusion exhaust velocity ~ 0.05 c (Isp ~ 1.5e6 s)
        ve_fusion = 0.05 * C
        exponent_fusion = C / (2.0 * ve_fusion)
        fusion_mass_ratio = ((1.0 + beta) / (1.0 - beta)) ** exponent_fusion

        # 2. Ideal antimatter exhaust velocity = c (photonic rocket)
        exponent_antimatter = C / (2.0 * C)  # 0.5
        antimatter_mass_ratio = math.sqrt((1.0 + beta) / (1.0 - beta))

        return RelativisticKinematicsResult(
            beta=beta,
            gamma=gamma,
            kinetic_energy_per_kg=kinetic_energy_per_kg,
            tnt_kilotons_per_kg=tnt_kilotons_per_kg,
            tnt_megatons_per_kg=tnt_megatons_per_kg,
            travel_time_proxima_years=travel_time_obs_yr,
            proper_time_proxima_years=proper_time_ship_yr,
            ism_stagnation_pressure_pa=ism_stagnation_pressure,
            ism_power_flux_w_per_m2=ism_power_flux,
            micro_dust_impact_energy_j=grain_impact_energy_j,
            fusion_mass_ratio_one_way=fusion_mass_ratio,
            antimatter_mass_ratio_one_way=antimatter_mass_ratio,
        )

    @staticmethod
    def evaluate_visitation_claim_bayes(
        prior_p_visit: float = 1.0e-9,
        likelihood_data_given_et: float = 0.90,
        likelihood_data_given_mundane: float = 1.0e-3
    ) -> BayesianVisitationEvaluation:
        """
        Performs Bayesian hypothesis testing on purported extraterrestrial visitation evidence
        (UAP observations, alleged artefacts, radar tracks).
        P(ET | Data) = P(Data | ET) * P(ET) / [ P(Data | ET)*P(ET) + P(Data | Mundane)*P(Mundane) ].
        """
        p_mundane = 1.0 - prior_p_visit
        numerator = likelihood_data_given_et * prior_p_visit
        denominator = numerator + (likelihood_data_given_mundane * p_mundane)
        posterior = numerator / denominator if denominator > 0 else 0.0

        bayes_factor = likelihood_data_given_et / max(likelihood_data_given_mundane, 1e-15)

        if posterior > 0.95:
            conclusion = "Hypothesis of ET visitation supported by extraordinary, highly calibrated data."
        elif posterior > 0.05:
            conclusion = "Ambiguous: data warrants physical instrumentation follow-up but fails standard of proof."
        else:
            conclusion = "Unsubstantiated: data is overwhelmingly explained by terrestrial, optical, or sensor phenomena."

        return BayesianVisitationEvaluation(
            prior_probability=prior_p_visit,
            likelihood_evidence_given_et=likelihood_data_given_et,
            likelihood_evidence_given_null=likelihood_data_given_mundane,
            bayes_factor=bayes_factor,
            posterior_probability=posterior,
            epistemic_conclusion=conclusion
        )

    @staticmethod
    def isotopic_anomaly_sigma(
        measured_ratio: float,
        terrestrial_mean_ratio: float,
        terrestrial_std_dev: float
    ) -> Tuple[float, bool]:
        """
        Tests whether an alleged physical artefact exhibits non-terrestrial isotopic fractionation.
        Returns (sigma_deviation, is_anomalous_at_10_sigma).
        Standard: Non-terrestrial material requires >= 10 sigma deviation from terrestrial/solar lines.
        """
        if terrestrial_std_dev <= 0:
            raise ValueError("Standard deviation must be strictly positive.")
        deviation = abs(measured_ratio - terrestrial_mean_ratio) / terrestrial_std_dev
        return deviation, deviation >= 10.0


# ==============================================================================
# SYNTHESIS ENGINE: FALSIFIABLE PREDICTIONS & OBSERVATIONAL ROADMAP
# ==============================================================================
class ExtraterrestrialEpistemicEngine:
    """
    Master engine synthesizing the three questions, generating exact falsifiable
    predictions and defining the observational criteria required to settle each.
    """

    @classmethod
    def get_three_question_synthesis(cls) -> Dict[str, Any]:
        """Returns the structured scientific synthesis for the three distinct questions."""
        return {
            "question_1_life_elsewhere": {
                "question": "Does life exist elsewhere in the Universe?",
                "epistemic_status": "Plausible, empirically open, and actively investigable.",
                "established_ground_truth": [
                    "Over 5,500 confirmed exoplanets discovered (mid-2020s).",
                    "Rocky habitable-zone planet occurrence rate eta_Earth ~ 0.1 - 0.4 for FGK stars.",
                    "Prebiotic organic chemistry is ubiquitous across ISM, comets, and carbonaceous chondrites.",
                    "Active subsurface oceans exist in Solar System (Europa, Enceladus, Titan)."
                ],
                "falsifiable_prediction": (
                    "Within an observational survey of 30 temperate rocky exoplanets around quiet G/K dwarf stars "
                    "(via Habitable Worlds Observatory / ELT-ANDES direct spectroscopy), at least one planet will exhibit "
                    "a coupled O2/O3 and CH4 atmospheric absorption signature (mixing ratios f_O2 > 10^-2, f_CH4 > 10^-5) "
                    "with f_CO < 10^-4, exceeding abiotic photochemical steady-state ceilings by >= 5 sigma."
                ),
                "settling_observation": (
                    "Conclusive spectroscopic detection of simultaneous thermodynamic chemical disequilibrium "
                    "(coupled O2/O3 + CH4 in an N2-H2O atmosphere) on an exoplanet with abiotic photochemical pathways "
                    "(e.g., CO photolysis buildup, H2-escape desiccation) ruled out at >= 5 sigma; OR direct in situ "
                    "mass-spectrometric detection of homochiral biomolecules (L-amino acid enantiomeric excess > 20%) "
                    "in the plumes of Enceladus or Europa."
                ),
                "falsification_condition": (
                    "If an exhaustive spectroscopic census of >= 100 temperate rocky habitable-zone exoplanets "
                    "reveals purely abiotic equilibrium or photochemical runaways (high CO, desiccated atmospheres) "
                    "with zero confirmed biogenic disequilibria, the hypothesis that biogenesis is common (f_l >= 0.01) "
                    "is empirically falsified in the local stellar neighborhood."
                )
            },
            "question_2_intelligent_life": {
                "question": "Does intelligent life exist (The Fermi Paradox)?",
                "epistemic_status": "Structurally constrained by null technosignature results; currently undecidable.",
                "established_ground_truth": [
                    "The Milky Way galaxy is ~13.6 billion years old; stars and rocky planets formed billions of years before Earth.",
                    "No verified technosignature (radio narrowband, optical pulsed, Dyson megastructure) detected to date.",
                    "Less than 10^-16 of the multi-dimensional SETI 'Cosmic Haystack' parameter space has been surveyed.",
                    "WISE survey rules out Kardashev Type III megastructure civilizations (>50% galactic starlight intercepted) in 100,000 galaxies."
                ],
                "falsifiable_prediction": (
                    "If communicative technological civilizations exist with median communicative longevity L >= 10^5 years, "
                    "an all-sky radio survey across the 1.0 - 10.0 GHz window with EIRP sensitivity >= 10^12 W within 100 pc "
                    "will detect at least one persistent or periodic drifting narrowband signal (delta_nu < 5 Hz) with non-random modulation."
                ),
                "settling_observation": (
                    "Detection of an artificially modulated (Shannon entropy H < 1.0 or repetitive mathematical encoding), "
                    "drifting (Doppler acceleration consistent with planetary orbital motion) narrowband electromagnetic "
                    "transmission originating from a stationary sidereal celestial coordinate, confirmed independently by "
                    "two or more geographically separated observatories; OR discovery of an anomalous transit lightcurve "
                    "demonstrating geometric, non-spherical, wavelength-independent occultation characteristic of a Dyson swarm."
                ),
                "falsification_condition": (
                    "Completion of an exhaustive, all-sky survey of the 10^6 stars within 100 pc across 1 - 10 GHz down to "
                    "EIRP 10^12 W with null detections will empirically falsify the existence of any local civilization transmitting "
                    "at or above terrestrial planetary radar power, bounding local civilizational density to n_civ < 10^-6 pc^-3."
                )
            },
            "question_3_visitation": {
                "question": "Has extraterrestrial life or technology visited Earth?",
                "epistemic_status": "Empirically unsupported; rejected under standard scientific null hypothesis.",
                "established_ground_truth": [
                    "Interstellar transit is constrained by relativistic kinematics: v = 0.1c requires ~4.5e14 J/kg (108 kT TNT/kg).",
                    "ISM dust grain sputtering at relativistic velocities delivers catastrophic erosion and kinetic energy fluxes.",
                    "No recovered physical artefact, debris, or isotopic anomaly has demonstrated non-terrestrial synthetic origin.",
                    "NASA UAP Independent Study (2023) and DOD AARO confirmed zero calibrated, reproducible sensor evidence of extraterrestrial propulsion."
                ],
                "falsifiable_prediction": (
                    "If extraterrestrial technology has operated in terrestrial airspace or the Earth-Moon system, there exists "
                    "physical debris or an automated surveillance probe containing non-solar isotopic fractionation (> 10 sigma "
                    "from terrestrial fractionation lines in 17O/18O or 54Fe/56Fe) and atomic-scale engineered lattice tolerances."
                ),
                "settling_observation": (
                    "Laboratory mass spectrometry and transmission electron microscopy of an acquired physical material "
                    "demonstrating non-terrestrial stable isotope ratios (> 10 sigma deviation from solar system baseline) "
                    "coupled with synthetic microstructural architectures irreproducible by terrestrial chemistry; OR "
                    "multi-modal, calibrated, synchronized sensor data (optical, radar, thermal IR) demonstrating an object "
                    "executing sustained accelerations a > 100 g in atmosphere without acoustic shockwave, ionization plume, "
                    "or aerodynamic heating."
                ),
                "falsification_condition": (
                    "The hypothesis of extraterrestrial visitation stands rejected under Occam's razor and the null hypothesis "
                    "until such time as calibrated, peer-reviewed physical evidence is produced. Continued failure to find "
                    "non-terrestrial artefacts in comprehensive lunar surface mapping (0.5 m LRO resolution) and Lagrange "
                    "point surveys progressively tightens the empirical bound against historical Solar System visitation."
                )
            }
        }
