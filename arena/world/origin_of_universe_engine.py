"""
origin_of_universe_engine.py
============================
Empirical Foundations and Open Problems of Cosmogenesis Engine.

A rigorous, quantitative, self-contained computational engine for modeling:
1. Empirical pillars of the Hot Big Bang (CMB blackbody thermodynamics, Standard Big Bang
   Nucleosynthesis, cosmological expansion, distance-redshift relations).
2. Quantitative analysis of the Hubble Tension and S8 tension.
3. Cosmic inflation dynamics, tensor-to-scalar ratio r, and Lyth bound.
4. Baryogenesis, Sakharov criteria, and Leptogenesis bounds.
5. Dark sector thermodynamics (Cosmological Constant problem, dynamical dark energy w(a),
   dark matter candidate parameter spaces and direct detection limits).
6. Programmatic registry of Open Problems in Cosmogenesis and their Decisive Resolving Observations.

References:
- Planck Collaboration (2018 / 2020), Cosmological parameters, A&A 641, A6.
- COBE/FIRAS (Fixsen 2009; Mather et al. 1994, 1999).
- BICEP/Keck Collaboration (Ade et al. 2021, Phys. Rev. Lett. 127, 151301).
- SH0ES Collaboration (Riess et al. 2022, ApJL 934, L7).
- DESI Collaboration (Adame et al. 2024, arXiv:2404.03002).
- Cooke et al. (2018, ApJ 855, 102) [Primordial Deuterium].
- Aver et al. (2015, 2021) [Primordial Helium-4].
- Sbordone et al. (2010, A&A 522, A26) [Spite Plateau Lithium-7].
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any, Optional


# ==============================================================================
# 1. PHYSICAL AND ASTRONOMICAL CONSTANTS (CODATA 2022 / IAU / PDG 2024)
# ==============================================================================

class PhysicalConstants:
    """Fundamental physical and astronomical constants in SI and natural units."""
    # Speed of light in vacuum (m/s)
    c: float = 299792458.0
    # Planck constant (J s)
    h: float = 6.62607015e-34
    # Reduced Planck constant (J s)
    hbar: float = 1.054571817e-34
    # Boltzmann constant (J/K)
    k_B: float = 1.380649e-23
    # Newtonian constant of gravitation (m^3 kg^-1 s^-2)
    G: float = 6.67430e-11
    # Elementary charge (C)
    e: float = 1.602176634e-19
    # Electron volt to Joule (J/eV)
    eV_to_J: float = 1.602176634e-19
    # Proton mass (kg)
    m_p: float = 1.67262192369e-27
    # Neutron mass (kg)
    m_n: float = 1.67492749804e-27
    # Electron mass (kg)
    m_e: float = 9.1093837015e-31
    # Neutron-proton mass difference (kg and MeV)
    delta_m_np_kg: float = 2.30557435e-30
    delta_m_np_MeV: float = 1.293332  # MeV
    # Free neutron lifetime (seconds, PDG 2024)
    tau_n: float = 879.4  # +/- 0.6 s
    # Radiation constant a_rad = 4 * sigma / c = (8 * pi^5 * k_B^4) / (15 * c^3 * h^3) (J m^-3 K^-4)
    a_rad: float = 7.5657e-16
    # Stefan-Boltzmann constant (W m^-2 K^-4)
    sigma_SB: float = 5.670374419e-8
    # Astronomical Unit (meters)
    AU: float = 1.495978707e11
    # Parsec (meters)
    pc: float = 3.085677581491367e16
    # Megaparsec (meters)
    Mpc: float = 3.085677581491367e22
    # Gigayear in seconds
    Gyr: float = 3.15576e16
    # Reduced Planck mass M_Pl = sqrt(hbar * c / (8 * pi * G)) in kg and GeV
    M_Pl_kg: float = 4.34136e-9
    M_Pl_GeV: float = 2.435e18
    # Full Planck mass m_Pl = sqrt(hbar * c / G) in kg and GeV
    m_Pl_kg: float = 2.17643e-8
    m_Pl_GeV: float = 1.2209e19
    # Planck length, time, and density
    l_Pl: float = 1.616255e-35  # m
    t_Pl: float = 5.391247e-44  # s
    rho_Pl_kg_m3: float = 5.155e96  # kg / m^3


# ==============================================================================
# 2. CANONICAL COSMOLOGICAL PARAMETERS (Planck 2018 / ACT / SH0ES)
# ==============================================================================

@dataclass
class CosmologicalParameters:
    """Cosmological parameters for flat Lambda-CDM model with observational uncertainties."""
    # Hubber constant H0 in km/s/Mpc
    H0_CMB: float = 67.36  # Planck 2018: 67.36 +/- 0.54
    H0_CMB_err: float = 0.54
    H0_local: float = 73.04  # SH0ES 2022: 73.04 +/- 1.04
    H0_local_err: float = 1.04
    H0_CCHP_TRGB: float = 69.8  # Freedman et al. (CCHP)
    H0_CCHP_err: float = 1.7
    
    # Baryon density parameter omega_b = Omega_b * h^2
    omega_b: float = 0.02237  # Planck 2018
    omega_b_err: float = 0.00015
    
    # Cold dark matter density parameter omega_c = Omega_c * h^2
    omega_c: float = 0.1200
    omega_c_err: float = 0.0012
    
    # CMB temperature at z=0 (K)
    T0_CMB: float = 2.72548  # Fixsen (2009)
    T0_CMB_err: float = 0.00057
    
    # Reionization optical depth tau
    tau_reion: float = 0.0544
    tau_reion_err: float = 0.0073
    
    # Scalar spectral index n_s
    n_s: float = 0.9649
    n_s_err: float = 0.0042
    
    # Primordial scalar amplitude ln(10^10 A_s)
    ln_10_As: float = 3.044
    ln_10_As_err: float = 0.014
    
    # Effective number of relativistic degrees of freedom
    N_eff: float = 3.046
    
    # Spatial curvature parameter Omega_k
    Omega_k: float = 0.0007
    Omega_k_err: float = 0.0019
    
    @property
    def h(self) -> float:
        """Dimensionless Hubble parameter h = H0 / 100."""
        return self.H0_CMB / 100.0

    @property
    def Omega_b(self) -> float:
        """Baryon density fraction Omega_b."""
        return self.omega_b / (self.h ** 2)

    @property
    def Omega_c(self) -> float:
        """Cold dark matter density fraction Omega_c."""
        return self.omega_c / (self.h ** 2)

    @property
    def Omega_m(self) -> float:
        """Total matter density fraction Omega_m = Omega_b + Omega_c."""
        return self.Omega_b + self.Omega_c

    @property
    def Omega_Lambda(self) -> float:
        """Dark energy density fraction Omega_Lambda in flat universe."""
        return 1.0 - self.Omega_m - self.Omega_k


# ==============================================================================
# 3. CMB THERMODYNAMICS AND BLACKBODY SPECTRAL FIDELITY
# ==============================================================================

class CMBBlackbodyThermodynamics:
    """
    Thermodynamic properties and spectral distortion limits of the Cosmic Microwave Background.
    Based on COBE/FIRAS precision measurements and high-redshift molecular tests.
    """
    def __init__(self, T0: float = 2.72548):
        self.T0 = T0
        self.k_B = PhysicalConstants.k_B
        self.h = PhysicalConstants.h
        self.c = PhysicalConstants.c
        self.hbar = PhysicalConstants.hbar

    def spectral_radiance_frequency(self, nu: float, T: Optional[float] = None) -> float:
        """
        Planck blackbody spectral radiance B_nu(T) in W / (m^2 sr Hz).
        B_nu(T) = (2 h nu^3 / c^2) / (exp(h nu / (k_B T)) - 1)
        """
        temp = T if T is not None else self.T0
        x = (self.h * nu) / (self.k_B * temp)
        if x > 700:
            return 0.0
        numerator = 2.0 * self.h * (nu ** 3) / (self.c ** 2)
        denominator = math.expm1(x)
        return numerator / denominator

    def peak_frequency(self, T: Optional[float] = None) -> float:
        """Wien displacement peak frequency in Hz: nu_max = 2.821439 * k_B * T / h."""
        temp = T if T is not None else self.T0
        return 2.821439372 * self.k_B * temp / self.h

    def peak_wavelength(self, T: Optional[float] = None) -> float:
        """Wien displacement peak wavelength in meters: lambda_max = 2.8977719e-3 / T."""
        temp = T if T is not None else self.T0
        return 2.897771955e-3 / temp

    def photon_number_density(self, T: Optional[float] = None) -> float:
        """
        Photon number density n_gamma in photons / m^3.
        n_gamma = (2 * zeta(3) / pi^2) * (k_B T / (hbar c))^3
        zeta(3) approx 1.202056903159594
        """
        temp = T if T is not None else self.T0
        zeta_3 = 1.202056903159594
        prefactor = 2.0 * zeta_3 / (math.pi ** 2)
        factor = (self.k_B * temp) / (self.hbar * self.c)
        return prefactor * (factor ** 3)

    def energy_density(self, T: Optional[float] = None) -> float:
        """Radiation energy density rho_gamma = a_rad * T^4 in J / m^3."""
        temp = T if T is not None else self.T0
        return PhysicalConstants.a_rad * (temp ** 4)

    def temperature_at_redshift(self, z: float) -> float:
        """Exact cosmological scaling of CMB temperature: T(z) = T0 * (1 + z)."""
        return self.T0 * (1.0 + z)

    def verify_firas_distortion_limits(self) -> Dict[str, Any]:
        """
        Returns empirical COBE/FIRAS constraints on spectral distortions.
        - Compton y-distortion (SZ effect from late energy injection)
        - Chemical potential mu-distortion (energy injection at 10^4 < z < 2e6)
        - Delta I / I_max upper bound
        """
        return {
            "T0_measured_K": self.T0,
            "T0_uncertainty_K": 0.00057,
            "y_distortion_limit": 1.5e-5,  # 95% CL (Fixsen et al. 1996)
            "mu_distortion_limit": 9.0e-5,  # 95% CL (Fixsen et al. 1996)
            "fractional_energy_deviation_limit": 6.0e-5,  # Delta rho / rho_gamma < 6e-5
            "spectral_departure_ppm": 50.0,  # departures < 50 parts per million
            "is_blackbody_within_firas_limits": True
        }

    def verify_high_redshift_measurements(self) -> List[Dict[str, Any]]:
        """
        Returns observational tests of T(z) from molecular/atomic transitions at high z.
        Demonstrates that T(z) = T0*(1+z), ruling out static/tired-light cosmologies.
        """
        observations = [
            {"z": 1.776, "T_obs": 7.58, "T_err": 0.35, "target": "PKS 1232+088 (C I)", "ref": "Srianand et al. 2000"},
            {"z": 2.418, "T_obs": 9.15, "T_err": 0.72, "target": "SDSS J143912+111740 (CO)", "ref": "Noterdaeme et al. 2011"},
            {"z": 3.025, "T_obs": 10.8, "T_err": 1.4, "target": "Q0347-383 (C II)", "ref": "Molaro et al. 2002"},
            {"z": 6.340, "T_obs": 20.0, "T_err": 2.0, "target": "HFLS3 (H2O absorption)", "ref": "Riechers et al. 2022"}
        ]
        for obs in observations:
            expected = self.temperature_at_redshift(obs["z"])
            pull = (obs["T_obs"] - expected) / obs["T_err"]
            obs["T_expected"] = round(expected, 2)
            obs["pull_sigma"] = round(pull, 2)
            obs["consistent_within_2sigma"] = abs(pull) <= 2.0
        return observations


# ==============================================================================
# 4. STANDARD BIG BANG NUCLEOSYNTHESIS (SBBN)
# ==============================================================================

class StandardBigBangNucleosynthesis:
    """
    Standard Big Bang Nucleosynthesis (SBBN) calculations:
    - n/p freeze-out thermodynamics
    - Neutron decay during deuterium bottleneck
    - Primordial 4He mass fraction Y_p
    - Primordial Deuterium (D/H)
    - Primordial Lithium-7 and the quantitative 'Lithium Problem'
    """
    def __init__(self, omega_b: float = 0.02237):
        self.omega_b = omega_b
        # Baryon-to-photon ratio eta = n_b / n_gamma = 2.7378e-8 * omega_b
        # eta_10 = 10^10 * eta
        self.eta = 2.7378e-8 * omega_b
        self.eta_10 = self.eta * 1e10  # typically ~ 6.12

    def calculate_freezeout_neutron_fraction(self, T_freeze_MeV: float = 0.80) -> float:
        """
        Calculates (n/p) ratio at weak freeze-out (T_freeze ~ 0.8 MeV):
        (n/p)_freeze = exp(-Delta m / T_freeze)
        where Delta m = 1.293332 MeV.
        """
        delta_m = PhysicalConstants.delta_m_np_MeV
        return math.exp(-delta_m / T_freeze_MeV)

    def calculate_bbn_neutron_fraction(self, T_freeze_MeV: float = 0.80, t_bottleneck_s: float = 300.0) -> float:
        """
        Calculates (n/p) ratio after neutron beta-decay during the deuterium bottleneck:
        (n/p)_BBN = (n/p)_freeze * exp(-t_bottleneck / tau_n)
        """
        np_freeze = self.calculate_freezeout_neutron_fraction(T_freeze_MeV)
        tau_n = PhysicalConstants.tau_n
        decay_factor = math.exp(-t_bottleneck_s / tau_n)
        return np_freeze * decay_factor

    def calculate_primordial_helium_mass_fraction(self, np_bbn: Optional[float] = None) -> float:
        """
        Calculates primordial 4He mass fraction Y_p:
        Y_p = (2 * (n/p)) / (1 + (n/p))
        Assuming virtually all neutrons are incorporated into 4He nuclei.
        """
        val_np = np_bbn if np_bbn is not None else self.calculate_bbn_neutron_fraction()
        return (2.0 * val_np) / (1.0 + val_np)

    def calculate_deuterium_abundance(self) -> float:
        """
        Theoretical primordial Deuterium-to-Hydrogen ratio (D/H)_p:
        Empirical scaling around Planck 2018 eta_10 = 6.12:
        (D/H)_p = 2.54e-5 * (eta_10 / 6.12)^(-1.60)
        """
        return 2.54e-5 * ((self.eta_10 / 6.12) ** (-1.60))

    def calculate_lithium7_abundance(self) -> float:
        """
        Theoretical primordial Lithium-to-Hydrogen ratio (7Li/H)_p from SBBN:
        Empirical scaling: (7Li/H)_p approx 4.68e-10 * (eta_10 / 6.12)^2.11
        """
        return 4.68e-10 * ((self.eta_10 / 6.12) ** 2.11)

    def evaluate_lithium_problem(self) -> Dict[str, Any]:
        """
        Quantitative quantification of the Primordial Lithium Problem:
        Compares theoretical SBBN prediction against observed Spite plateau value.
        """
        theo_7Li = self.calculate_lithium7_abundance()
        obs_7Li = 1.58e-10  # Sbordone et al. 2010 Spite plateau
        obs_7Li_err = 0.11e-10
        discrepancy_factor = theo_7Li / obs_7Li
        tension_sigma = (theo_7Li - obs_7Li) / math.sqrt(obs_7Li_err**2 + (0.32e-10)**2)

        return {
            "theoretical_7Li_over_H": theo_7Li,
            "theoretical_uncertainty": 0.32e-10,
            "observed_spite_plateau_7Li_over_H": obs_7Li,
            "observed_uncertainty": obs_7Li_err,
            "discrepancy_factor": round(discrepancy_factor, 2),
            "tension_sigma": round(tension_sigma, 2),
            "is_tension_severe": tension_sigma > 5.0,
            "potential_explanations": [
                "Stellar atmospheric depletion via turbulent diffusion and rotational mixing",
                "Beyond Standard Model particle decay (e.g., supersymmetric relics destroying Be-7 before decay to Li-7)",
                "Systematic errors in stellar temperature scales (largely ruled out by modern 3D non-LTE models)"
            ],
            "resolving_observation": "High-resolution spectroscopy of gas-phase lithium in pristine intergalactic/interstellar media outside stars (e.g. DLAs using ELT-HIRES)"
        }

    def comprehensive_bbn_comparison(self) -> Dict[str, Any]:
        """Compares calculated SBBN abundances with current observational benchmark measurements."""
        np_freeze = self.calculate_freezeout_neutron_fraction()
        np_bbn = self.calculate_bbn_neutron_fraction()
        Y_p_calc = self.calculate_primordial_helium_mass_fraction(np_bbn)
        DH_calc = self.calculate_deuterium_abundance()
        LiH_calc = self.calculate_lithium7_abundance()

        return {
            "baryon_density_omega_b": self.omega_b,
            "baryon_to_photon_ratio_eta": self.eta,
            "eta_10": round(self.eta_10, 3),
            "np_freezeout_ratio": round(np_freeze, 4),
            "np_bbn_ratio": round(np_bbn, 4),
            "helium4_mass_fraction": {
                "theoretical_predicted": round(Y_p_calc, 4),
                "observed_benchmark": 0.245,
                "observed_uncertainty": 0.003,
                "reference": "Aver et al. (2015, 2021); Peimbert et al. (2016)",
                "agreement_sigma": round(abs(Y_p_calc - 0.245) / 0.003, 2)
            },
            "deuterium_to_hydrogen": {
                "theoretical_predicted": DH_calc,
                "observed_benchmark": 2.547e-5,
                "observed_uncertainty": 0.025e-5,
                "reference": "Cooke et al. (2018)",
                "agreement_sigma": round(abs(DH_calc - 2.547e-5) / 0.025e-5, 2)
            },
            "lithium7_to_hydrogen": self.evaluate_lithium_problem()
        }


# ==============================================================================
# 5. COSMIC EXPANSION DYNAMICS & FRIEDMANN INTEGRATOR
# ==============================================================================

class CosmicExpansionDynamics:
    """
    Cosmic expansion dynamics for flat and curved Lambda-CDM universes.
    Computes Hubble parameter H(z), comoving distance, luminosity distance,
    angular diameter distance, and sound horizon.
    """
    def __init__(self, params: Optional[CosmologicalParameters] = None):
        self.params = params if params is not None else CosmologicalParameters()
        self.H0 = self.params.H0_CMB
        self.h = self.params.h
        self.Omega_m = self.params.Omega_m
        self.Omega_k = self.params.Omega_k
        self.Omega_Lambda = self.params.Omega_Lambda
        # Radiation density fraction Omega_r = Omega_gamma * (1 + 0.2271 * N_eff)
        # rho_gamma_0 = a_rad * T0^4, rho_crit_0 = 3 H0^2 / (8 pi G)
        c = PhysicalConstants.c
        G = PhysicalConstants.G
        H0_SI = (self.H0 * 1000.0) / PhysicalConstants.Mpc
        rho_crit_0 = (3.0 * (H0_SI ** 2)) / (8.0 * math.pi * G)
        rho_gamma_0 = PhysicalConstants.a_rad * (self.params.T0_CMB ** 4)
        Omega_gamma = rho_gamma_0 / (rho_crit_0 * (c ** 2))
        self.Omega_r = Omega_gamma * (1.0 + 0.227107 * self.params.N_eff)

    def E(self, z: float, w0: float = -1.0, wa: float = 0.0) -> float:
        """
        Dimensionless Friedmann expansion rate E(z) = H(z) / H0:
        Supports dynamical dark energy w(a) = w0 + wa * (1 - a) (CPL parametrization).
        """
        a = 1.0 / (1.0 + z)
        # Dark energy density scaling f_DE(z)
        if w0 == -1.0 and wa == 0.0:
            f_DE = 1.0
        else:
            f_DE = (a ** (-3.0 * (1.0 + w0 + wa))) * math.exp(-3.0 * wa * (1.0 - a))

        term_r = self.Omega_r * ((1.0 + z) ** 4)
        term_m = self.Omega_m * ((1.0 + z) ** 3)
        term_k = self.Omega_k * ((1.0 + z) ** 2)
        term_de = self.Omega_Lambda * f_DE

        total = term_r + term_m + term_k + term_de
        return math.sqrt(max(total, 1e-12))

    def hubble_parameter(self, z: float, w0: float = -1.0, wa: float = 0.0) -> float:
        """Hubble parameter H(z) in km/s/Mpc."""
        return self.H0 * self.E(z, w0, wa)

    def comoving_distance_Mpc(self, z: float, steps: int = 1000, w0: float = -1.0, wa: float = 0.0) -> float:
        """
        Comoving line-of-sight distance D_C(z) in Mpc:
        D_C(z) = (c / H0) * \int_0^z dz' / E(z')
        Computed via Simpson's composite rule.
        """
        if z <= 0.0:
            return 0.0
        n = steps if steps % 2 == 0 else steps + 1
        dz = z / n
        c_km_s = PhysicalConstants.c / 1000.0

        integral = 1.0 / self.E(0.0, w0, wa) + 1.0 / self.E(z, w0, wa)
        for i in range(1, n):
            zi = i * dz
            weight = 4.0 if i % 2 == 1 else 2.0
            integral += weight / self.E(zi, w0, wa)

        integral *= (dz / 3.0)
        return (c_km_s / self.H0) * integral

    def transverse_comoving_distance_Mpc(self, z: float, steps: int = 1000) -> float:
        """Transverse comoving distance D_M(z) in Mpc accounting for spatial curvature Omega_k."""
        dc = self.comoving_distance_Mpc(z, steps)
        if abs(self.Omega_k) < 1e-6:
            return dc
        c_km_s = PhysicalConstants.c / 1000.0
        dh = c_km_s / self.H0
        sqrt_k = math.sqrt(abs(self.Omega_k))
        if self.Omega_k > 0:  # Open
            return (dh / sqrt_k) * math.sinh(sqrt_k * dc / dh)
        else:  # Closed
            return (dh / sqrt_k) * math.sin(sqrt_k * dc / dh)

    def luminosity_distance_Mpc(self, z: float, steps: int = 1000) -> float:
        """Luminosity distance D_L(z) = (1 + z) * D_M(z) in Mpc."""
        return (1.0 + z) * self.transverse_comoving_distance_Mpc(z, steps)

    def angular_diameter_distance_Mpc(self, z: float, steps: int = 1000) -> float:
        """Angular diameter distance D_A(z) = D_M(z) / (1 + z) in Mpc."""
        return self.transverse_comoving_distance_Mpc(z, steps) / (1.0 + z)

    def sound_horizon_at_drag_epoch_Mpc(self) -> float:
        """
        Sound horizon r_s at drag epoch z_d approx 1060:
        Using standard Planck 2018 calibrated sound horizon r_s(z_d) = 147.21 +/- 0.23 Mpc.
        """
        return 147.21


# ==============================================================================
# 6. HUBBLE TENSION AND S8 TENSION QUANTIFICATION
# ==============================================================================

class TensionAnalyzer:
    """Quantitative statistical analysis of the Hubble Tension and Large-Scale Structure S8 Tension."""
    
    @staticmethod
    def calculate_gaussian_tension(val1: float, err1: float, val2: float, err2: float) -> Tuple[float, float]:
        """
        Calculates difference and statistical significance (number of standard deviations)
        between two independent Gaussian measurements:
        tension_sigma = |val1 - val2| / sqrt(err1^2 + err2^2)
        """
        diff = abs(val1 - val2)
        combined_err = math.sqrt(err1 ** 2 + err2 ** 2)
        sigma = diff / combined_err
        return diff, sigma

    def analyze_hubble_tension(self) -> Dict[str, Any]:
        """
        Comprehensive quantification of H0 measurements across early and late universe probes.
        """
        planck_H0, planck_err = 67.36, 0.54
        shoes_H0, shoes_err = 73.04, 1.04
        cchp_H0, cchp_err = 69.8, 1.7  # Freedman et al. TRGB
        act_H0, act_err = 67.9, 1.5  # ACT DR4 + WMAP
        desi_H0, desi_err = 67.97, 0.38  # DESI 2024 + CMB + BAO

        diff_shoes_planck, sigma_shoes_planck = self.calculate_gaussian_tension(shoes_H0, shoes_err, planck_H0, planck_err)
        diff_cchp_planck, sigma_cchp_planck = self.calculate_gaussian_tension(cchp_H0, cchp_err, planck_H0, planck_err)
        diff_shoes_cchp, sigma_shoes_cchp = self.calculate_gaussian_tension(shoes_H0, shoes_err, cchp_H0, cchp_err)

        return {
            "early_universe_probes": {
                "Planck_2018": {"H0": planck_H0, "err": planck_err, "method": "CMB primary TT,TE,EE + lensing"},
                "ACT_DR4_WMAP": {"H0": act_H0, "err": act_err, "method": "Ground-based CMB high-multipole"},
                "DESI_2024_BAO_CMB": {"H0": desi_H0, "err": desi_err, "method": "BAO + sound horizon calibration"}
            },
            "late_universe_probes": {
                "SH0ES_2022": {"H0": shoes_H0, "err": shoes_err, "method": "Cepheids + SNe Ia distance ladder"},
                "CCHP_TRGB": {"H0": cchp_H0, "err": cchp_err, "method": "Tip of Red Giant Branch (TRGB) + SNe Ia"},
                "Megamaser_Project": {"H0": 73.9, "err": 3.0, "method": "Geometric water megamasers in active galaxies"}
            },
            "shoes_vs_planck": {
                "delta_H0": round(diff_shoes_planck, 2),
                "tension_sigma": round(sigma_shoes_planck, 2),
                "is_tension_critical": sigma_shoes_planck >= 4.5
            },
            "cchp_vs_planck": {
                "delta_H0": round(diff_cchp_planck, 2),
                "tension_sigma": round(sigma_cchp_planck, 2)
            },
            "resolving_observations": [
                {
                    "probe": "Standard Siren Gravitational Waves",
                    "instrument": "LIGO/Virgo/KAGRA/Einstein Telescope",
                    "mechanism": "Direct luminosity distance from binary neutron star mergers without distance ladder",
                    "target_precision": "1-2% with ~50 detected events"
                },
                {
                    "probe": "JWST Cross-Calibration of Distance Anchors",
                    "instrument": "James Webb Space Telescope NIRCam",
                    "mechanism": "Simultaneous measurement of Cepheids, TRGB, and JAGB carbon stars in identical host galaxies",
                    "target_precision": "Eliminates crowding and metallicity systematic errors"
                },
                {
                    "probe": "High-Multipole CMB Polarization E-Modes",
                    "instrument": "Simons Observatory / CMB-S4",
                    "mechanism": "Detects or rules out Early Dark Energy (EDE) phase shifts at ell > 2500"
                }
            ]
        }

    def analyze_s8_tension(self) -> Dict[str, Any]:
        """Quantification of S8 = sigma_8 * sqrt(Omega_m / 0.3) tension between weak lensing and CMB."""
        planck_S8, planck_S8_err = 0.832, 0.013
        kids_S8, kids_S8_err = 0.759, 0.024
        des_y3_S8, des_y3_S8_err = 0.776, 0.017

        diff_kids, sigma_kids = self.calculate_gaussian_tension(kids_S8, kids_S8_err, planck_S8, planck_S8_err)
        diff_des, sigma_des = self.calculate_gaussian_tension(des_y3_S8, des_y3_S8_err, planck_S8, planck_S8_err)

        return {
            "CMB_Planck_S8": {"val": planck_S8, "err": planck_S8_err},
            "KiDS1000_S8": {"val": kids_S8, "err": kids_S8_err, "tension_sigma": round(sigma_kids, 2)},
            "DES_Y3_S8": {"val": des_y3_S8, "err": des_y3_S8_err, "tension_sigma": round(sigma_des, 2)},
            "resolving_observation": "Stage-IV cosmic shear surveys (Euclid space mission, Rubin Observatory LSST) mapping 3D matter clustering with sub-percent calibration of shear and photometric redshifts"
        }


# ==============================================================================
# 7. INFLATIONARY COSMOLOGY AND PRIMORDIAL GRAVITATIONAL WAVES
# ==============================================================================

class InflationaryCosmology:
    """
    Cosmic inflation models, slow-roll parameters, tensor-to-scalar ratio r,
    Lyth bound, and primordial gravitational wave predictions.
    """
    def __init__(self, N_efolds: float = 60.0):
        self.N = N_efolds
        self.M_Pl = PhysicalConstants.M_Pl_GeV  # Reduced Planck mass ~ 2.435e18 GeV

    def starobinsky_model(self) -> Dict[str, float]:
        """
        Starobinsky R^2 / Higgs inflation predictions:
        n_s = 1 - 2/N, r = 12 / N^2
        """
        ns = 1.0 - (2.0 / self.N)
        r = 12.0 / (self.N ** 2)
        return {
            "model": "Starobinsky R^2 / Higgs inflation",
            "N_efolds": self.N,
            "spectral_index_ns": round(ns, 4),
            "tensor_to_scalar_ratio_r": round(r, 5),
            "tensor_spectral_index_nT": round(-r / 8.0, 6)
        }

    def quadratic_chaotic_model(self) -> Dict[str, float]:
        """
        Linde quadratic chaotic inflation V(phi) = 1/2 m^2 phi^2 (Now ruled out by BK18):
        n_s = 1 - 2/N, r = 8 / N
        """
        ns = 1.0 - (2.0 / self.N)
        r = 8.0 / self.N
        return {
            "model": "Quadratic chaotic V(phi) = 1/2 m^2 phi^2",
            "N_efolds": self.N,
            "spectral_index_ns": round(ns, 4),
            "tensor_to_scalar_ratio_r": round(r, 4),
            "is_ruled_out_by_BK18": r > 0.036
        }

    def lyth_bound(self, r: float) -> float:
        """
        Lyth bound on inflaton field excursion Delta phi / M_Pl:
        Delta phi / M_Pl >= sqrt(r / 8) * N_efolds
        """
        return math.sqrt(r / 8.0) * self.N

    def inflation_energy_scale_GeV(self, r: float, A_s: float = 2.1e-9) -> float:
        """
        Inflationary energy scale V^(1/4) in GeV:
        V = (3 pi^2 / 2) * A_s * r * M_Pl^4
        V^(1/4) = (3 pi^2 / 2 * A_s * r)^(1/4) * M_Pl
        """
        prefactor = (1.5 * (math.pi ** 2) * A_s * r) ** 0.25
        return prefactor * self.M_Pl

    def current_status(self) -> Dict[str, Any]:
        """Observational status of primordial B-modes and future mission targets."""
        r_bk18_limit = 0.036  # BICEP/Keck 2021 95% CL upper limit
        v_scale_max = self.inflation_energy_scale_GeV(r_bk18_limit)
        starobinsky = self.starobinsky_model()

        return {
            "current_upper_limit_r_95CL": r_bk18_limit,
            "energy_scale_upper_limit_GeV": v_scale_max,
            "starobinsky_prediction_r": starobinsky["tensor_to_scalar_ratio_r"],
            "upcoming_observatories": [
                {
                    "mission": "LiteBIRD (JAXA/NASA/ESA, launch ~2032)",
                    "target_sensitivity": "sigma(r) < 0.001",
                    "capability": "Can detect r > 0.005 at > 5 sigma; tests Starobinsky model definitively"
                },
                {
                    "mission": "CMB-S4 (South Pole & Atacama)",
                    "target_sensitivity": "sigma(r) ~ 0.0005",
                    "capability": "Tests down to r ~ 0.001"
                }
            ],
            "resolving_power": "A detection of r confirms GUT-scale inflation and quantum origin of spacetime fluctuations. A non-detection with r < 10^-3 rules out all canonical plateau/large-field models and forces small-field or bounce cosmologies."
        }


# ==============================================================================
# 8. BARYOGENESIS AND SAKHAROV CONDITIONS
# ==============================================================================

class BaryogenesisAnalysis:
    """
    Theoretical requirements for cosmogenetic baryogenesis:
    Evaluation of the three Sakharov conditions in the Standard Model and Leptogenesis bounds.
    """
    def __init__(self):
        self.eta_obs = 6.12e-10  # Observed baryon asymmetry (n_b - n_antib) / n_gamma
        self.m_Higgs = 125.25  # GeV

    def evaluate_sakharov_conditions(self) -> Dict[str, Any]:
        """
        Evaluates why the Standard Model of Particle Physics fails to generate
        the observed baryon asymmetry.
        """
        # Condition 1: Baryon Number Violation
        # SM has electroweak sphaleron transitions at T > 100 GeV, violating B+L but conserving B-L.
        b_violation = {
            "status": "Partially satisfied",
            "mechanism": "Electroweak sphaleron transitions active at T > T_EW (~100-160 GeV)",
            "limitation": "Conserves (B - L); any primordial (B + L) asymmetry is washed out unless (B - L) != 0"
        }

        # Condition 2: C and CP Violation
        # SM has CP violation in CKM matrix quantified by Jarlskog invariant J ~ 3.08e-5
        # The dimensionless asymmetry d_CP ~ J * (m_t^2 - m_u^2)(m_t^2 - m_c^2)... / T_EW^12 ~ 10^-20
        jarlskog_J = 3.08e-5
        eta_SM_est = 1e-20
        cp_violation = {
            "status": "Failed in Standard Model",
            "jarlskog_invariant": jarlskog_J,
            "maximum_sm_baryon_asymmetry": eta_SM_est,
            "observed_asymmetry": self.eta_obs,
            "deficit_orders_of_magnitude": 10,
            "diagnosis": "Quark CKM CP violation is suppressed by 10 orders of magnitude; requires new BSM CP-violating phases in leptonic or extended Higgs sector"
        }

        # Condition 3: Departure from Thermal Equilibrium
        # First-order phase transition requires m_Higgs < 75 GeV in SM; observed m_Higgs = 125 GeV implies smooth crossover
        departure_equilibrium = {
            "status": "Failed in Standard Model",
            "observed_higgs_mass_GeV": self.m_Higgs,
            "critical_higgs_mass_for_first_order_GeV": 75.0,
            "phase_transition_nature": "Smooth crossover (no bubble nucleation, no departure from thermal equilibrium)",
            "diagnosis": "Electroweak phase transition cannot provide out-of-equilibrium environment needed to preserve generated asymmetry"
        }

        return {
            "b_violation": b_violation,
            "cp_violation": cp_violation,
            "departure_from_equilibrium": departure_equilibrium,
            "conclusion": "Standard Model cosmogenesis cannot explain baryon asymmetry of the universe; requires BSM physics (e.g. Leptogenesis, Electroweak Baryogenesis in 2HDM/NMSSM, or Affleck-Dine)."
        }

    def leptogenesis_bounds(self) -> Dict[str, Any]:
        """
        Davidson-Ibarra lower bound on lightest right-handed neutrino mass M_N1
        for thermal unflavored leptogenesis:
        M_N1 >= 10^9 GeV
        """
        m_N1_min_GeV = 1.0e9
        return {
            "mechanism": "Thermal Leptogenesis via heavy Majorana neutrino decays (N1 -> l + H, l_bar + H*)",
            "davidson_ibarra_bound_M_N1_GeV": m_N1_min_GeV,
            "implies_reheat_temperature_T_reh_GeV": m_N1_min_GeV,
            "resolving_observations": [
                {
                    "experiment": "Neutrinoless Double Beta Decay (0nu beta beta) [LEGEND-1000, nEXO]",
                    "goal": "Establish lepton number violation (Delta L = 2) and Majorana nature of neutrinos",
                    "sensitivity": "Effective Majorana mass m_bb down to 10-20 meV"
                },
                {
                    "experiment": "Long-Baseline Neutrino Oscillation [DUNE, Hyper-Kamiokande]",
                    "goal": "Measure Dirac CP-violating phase delta_CP in PMNS matrix at > 5 sigma",
                    "sensitivity": "Covers > 75% of delta_CP parameter space"
                },
                {
                    "experiment": "Permanent Electric Dipole Moments [ACME, JILA, PSI]",
                    "goal": "Detect new CP violation in electron or neutron EDM",
                    "current_bound_electron_e_cm": 4.1e-30
                }
            ]
        }


# ==============================================================================
# 9. DARK SECTOR THERMODYNAMICS & VACUUM ENERGY
# ==============================================================================

class DarkSectorAnalysis:
    """
    Thermodynamic analysis of the Dark Sector:
    - Cosmological Constant problem (QFT vacuum catastrophe)
    - Dynamical dark energy w(a) parametrization and DESI 2024 results
    - Dark Matter direct detection boundaries and candidate windows
    """
    def __init__(self, omega_Lambda: float = 0.6847, omega_c: float = 0.264):
        self.Omega_Lambda = omega_Lambda
        self.Omega_c = omega_c

    def cosmological_constant_discrepancy(self) -> Dict[str, Any]:
        """
        Quantifies the 121-order-of-magnitude mismatch between observed vacuum energy
        and Planck-scale quantum vacuum expectation value:
        rho_Lambda,obs approx (2.25 meV)^4 approx 2.5e-47 GeV^4
        rho_vac,Planck = M_Pl^4 approx 3.5e73 GeV^4
        """
        rho_obs_GeV4 = 2.5e-47  # GeV^4
        rho_Planck_GeV4 = 3.5e73  # GeV^4
        rho_EW_GeV4 = (100.0) ** 4  # 1e8 GeV^4 at electroweak scale
        rho_QCD_GeV4 = (0.2) ** 4  # 1.6e-3 GeV^4 at QCD scale

        log10_mismatch_planck = math.log10(rho_Planck_GeV4 / rho_obs_GeV4)
        log10_mismatch_ew = math.log10(rho_EW_GeV4 / rho_obs_GeV4)
        log10_mismatch_qcd = math.log10(rho_QCD_GeV4 / rho_obs_GeV4)

        return {
            "rho_obs_GeV4": rho_obs_GeV4,
            "rho_obs_J_m3": 5.9e-10,
            "equivalent_energy_scale_meV": 2.25,
            "log10_mismatch_vs_Planck": round(log10_mismatch_planck, 1),
            "log10_mismatch_vs_Electroweak": round(log10_mismatch_ew, 1),
            "log10_mismatch_vs_QCD": round(log10_mismatch_qcd, 1),
            "coincidence_ratio_today_rho_de_over_rho_m": round(self.Omega_Lambda / (1.0 - self.Omega_Lambda), 2),
            "coincidence_problem_description": "Why are dark energy and matter densities within an order of magnitude today (z=0), despite scaling as (1+z)^0 vs (1+z)^3?"
        }

    def desi_2024_dark_energy_results(self) -> Dict[str, Any]:
        """
        Summarizes DESI 2024 Year-1 BAO results combined with CMB and Type Ia Supernovae,
        showing tension with static cosmological constant (w0 = -1, wa = 0).
        """
        # DESI BAO + CMB + Pantheon+ / Union3
        w0 = -0.827
        w0_err = 0.063
        wa = -0.75
        wa_err_plus = 0.33
        wa_err_minus = 0.25

        # Statistical significance of deviation from LCDM (w0=-1, wa=0)
        # DESI Collaboration reports 2.5 sigma to 3.9 sigma tension depending on SNe sample
        return {
            "dataset": "DESI 2024 Year-1 BAO + Planck CMB + Pantheon+ SNe",
            "parametrization": "Chevallier-Polarski-Linder: w(a) = w0 + wa * (1 - a)",
            "w0": w0,
            "w0_err": w0_err,
            "wa": wa,
            "wa_err": f"+{wa_err_plus} / -{wa_err_minus}",
            "tension_with_static_LCDM_sigma": "2.5 - 3.9 sigma (sample dependent)",
            "physical_implications": "If validated at > 5 sigma by Euclid and Roman, dark energy is dynamical (quintessence / phantom crossing), definitively falsifying a bare cosmological constant."
        }

    def dark_matter_candidate_landscape(self) -> List[Dict[str, Any]]:
        """Registry of dark matter candidates and current experimental status."""
        return [
            {
                "candidate": "Weakly Interacting Massive Particles (WIMPs)",
                "mass_range": "10 GeV - 100 TeV",
                "current_limit": "LZ (2024) limit: sigma_SI < 6e-48 cm^2 at 30 GeV",
                "boundary": "Approaching coherent neutrino-nucleus scattering 'neutrino fog'",
                "resolving_observation": "Direct detection in DARWIN / XLZD (liquid xenon) or ARGO (liquid argon) above neutrino background"
            },
            {
                "candidate": "QCD Axions / Axion-Like Particles (ALPs)",
                "mass_range": "1 micro-eV to 1 meV (QCD window)",
                "current_limit": "ADMX excludes KSVZ/DFSZ coupling at 2.7 - 4.2 micro-eV",
                "boundary": "Exploring 1 - 100 GHz band",
                "resolving_observation": "Microwave resonant cavity detection in ADMX, DMRadio, BREAD, and ALPHA"
            },
            {
                "candidate": "Ultralight / Fuzzy Dark Matter",
                "mass_range": "1e-22 to 1e-19 eV",
                "current_limit": "Constrained by Lyman-alpha forest and dwarf galaxy core profiles",
                "resolving_observation": "High-redshift 21cm hydrogen power spectrum cutoff measured by HERA / SKA"
            },
            {
                "candidate": "Primordial Black Holes (PBHs)",
                "mass_range": "1e17 to 1e22 g (asteroid mass window)",
                "current_limit": "Sub-solar microlensing and Hawking evaporation bounds (M > 5e14 g required for survival)",
                "resolving_observation": "High-cadence optical microlensing (Subaru HSC) and sub-solar gravitational wave mergers (LIGO/ET)"
            }
        ]


# ==============================================================================
# 10. PROGRAMMATIC REGISTRY OF OPEN PROBLEMS AND RESOLVING OBSERVATIONS
# ==============================================================================

@dataclass
class CosmologicalOpenProblem:
    """Detailed structural representation of an open problem in cosmogenesis."""
    problem_id: str
    title: str
    theoretical_barrier: str
    what_theory_does_not_explain: str
    established_quantitative_values: Dict[str, Any]
    resolving_observation: str
    target_instruments: List[str]
    falsification_metric: str


class CosmogenesisOpenProblemsRegistry:
    """Compendium of open problems in cosmogenesis and their resolving observations."""

    def __init__(self):
        self.problems = self._build_registry()

    def _build_registry(self) -> List[CosmologicalOpenProblem]:
        return [
            CosmologicalOpenProblem(
                problem_id="OP-01",
                title="The Initial Singularity and Planck-Scale Incompleteness",
                theoretical_barrier="Penrose-Hawking singularity theorems show classical GR is geodesically incomplete at t -> 0, where curvature invariants diverge. GR is an effective field theory that breaks down at the Planck scale (t_Pl = 5.39e-44 s, rho_Pl = 5.16e96 kg/m^3).",
                what_theory_does_not_explain="Whether spacetime had a true physical beginning, emerged from a quantum bounce (Loop Quantum Cosmology), was preceded by a contracting phase (ekpyrotic/cyclic), or is an emergent macroscopic property of quantum entanglement.",
                established_quantitative_values={
                    "planck_time_s": PhysicalConstants.t_Pl,
                    "planck_density_kg_m3": PhysicalConstants.rho_Pl_kg_m3,
                    "planck_energy_GeV": PhysicalConstants.m_Pl_GeV
                },
                resolving_observation="Measurement of the Primordial Gravitational Wave (PGW) spectrum and tensor spectral index n_T across CMB B-modes (1e-17 Hz) and space interferometry (1e-4 - 100 Hz). A blue-tilted spectrum (n_T > 0) or specific high-frequency spectral cutoff would definitively rule out standard inflation and prove a quantum bounce or pre-Big Bang phase.",
                target_instruments=["LiteBIRD", "LISA", "DECIGO", "Big Bang Observer (BBO)", "Einstein Telescope"],
                falsification_metric="Measurement of tensor tilt n_T != -r/8, or detection of chiral gravitational wave modes, or cutoff at string/bounce scale."
            ),
            CosmologicalOpenProblem(
                problem_id="OP-02",
                title="Cosmic Inflation: Inflaton Identity, Initial Conditions, and Multiverse Measure",
                theoretical_barrier="Inflation requires exponential expansion (N >= 50-60 e-folds) driven by a negative-pressure scalar field potential V(phi) to explain the horizon and flatness problems, but the underlying field theory is unknown.",
                what_theory_does_not_explain="The particle identity of the inflaton, why the pre-inflationary patch was sufficiently homogeneous and flat to ignite inflation (initial conditions problem / low Weyl curvature), and whether eternal inflation generates an untestable multiverse with an intractable measure problem.",
                established_quantitative_values={
                    "current_bound_r_95CL": "< 0.036 (BICEP/Keck + Planck)",
                    "measured_scalar_tilt_ns": "0.9649 +/- 0.0042",
                    "spatial_flatness_Omega_k": "0.0007 +/- 0.0019"
                },
                resolving_observation="Precision measurement of CMB B-mode polarization tensor-to-scalar ratio r and non-Gaussianity f_NL. A detection of r in [0.003, 0.01] establishes GUT-scale single-field inflation and fixes the potential scale V^(1/4) ~ 10^16 GeV. Detection of |f_NL^local| > 1 rules out all single-field slow-roll inflation.",
                target_instruments=["LiteBIRD", "CMB-S4", "Simons Observatory", "SPHEREx", "Vera C. Rubin Observatory (LSST)"],
                falsification_metric="Upper limit r < 0.001 falsifies canonical large-field and Starobinsky/Higgs models; f_NL^local > 1 falsifies single-field inflation."
            ),
            CosmologicalOpenProblem(
                problem_id="OP-03",
                title="Baryon Asymmetry of the Universe (Baryogenesis)",
                theoretical_barrier="The Standard Model fails all three Sakharov conditions: EW sphalerons conserve (B - L); CKM CP violation is 10 orders of magnitude too small; and the Higgs transition at 125 GeV is a smooth crossover.",
                what_theory_does_not_explain="The physical mechanism that produced the observed net baryon-to-photon excess of 1 quark per billion in the primordial plasma.",
                established_quantitative_values={
                    "observed_eta": "6.12e-10",
                    "sm_jarlskog_asymmetry": "~ 1e-20",
                    "observed_higgs_mass_GeV": 125.25
                },
                resolving_observation="Detection of neutrinoless double beta decay (0nu beta beta) proving lepton number violation (Delta L = 2) and Majorana neutrinos; combined with measurement of leptonic CP-violating phase delta_CP in neutrino oscillations, validating thermal or resonant Leptogenesis.",
                target_instruments=["LEGEND-1000", "nEXO", "DUNE", "Hyper-Kamiokande", "ACME/JILA EDM"],
                falsification_metric="Discovery of 0nu beta beta with T_1/2 < 1e28 yr and nonzero delta_CP confirms the Leptogenesis paradigm; permanent EDM detection proves required BSM CP violation."
            ),
            CosmologicalOpenProblem(
                problem_id="OP-04",
                title="The Fundamental Nature of Dark Matter",
                theoretical_barrier="Dark matter accounts for ~84% of all matter, but has zero viable candidate in the Standard Model. Gravitational evidence is overwhelming across galaxies, clusters, lensing, and CMB, but non-gravitational interactions remain undetected.",
                what_theory_does_not_explain="The mass, spin, cross-section, self-interaction, and production mechanism of the dark matter particle across a 90-order-of-magnitude mass range.",
                established_quantitative_values={
                    "dark_matter_density_fraction_Omega_c": "0.264 +/- 0.003",
                    "wimp_limit_sigma_SI_cm2": "< 6e-48 at 30 GeV (LZ 2024)",
                    "measured_Omega_c_h2": "0.1200 +/- 0.0012"
                },
                resolving_observation="Non-gravitational detection via liquid noble target direct detection (WIMPs reaching the neutrino fog), resonant microwave cavity conversion (QCD axions in 1-100 micro-eV), or small-scale power spectrum cutoff in 21cm tomography (warm or fuzzy dark matter).",
                target_instruments=["LZ", "DARWIN / XLZD", "ADMX", "DMRadio", "HERA", "Square Kilometre Array (SKA)"],
                falsification_metric="Crossing the neutrino fog without nuclear recoil signal excludes thermal WIMPs; detection of resonant axion photon conversion definitively confirms QCD axion."
            ),
            CosmologicalOpenProblem(
                problem_id="OP-05",
                title="The Nature of Dark Energy and the Cosmological Constant Problem",
                theoretical_barrier="Dark energy accounts for ~68% of cosmic energy, yet quantum field theory predicts vacuum energy 121 orders of magnitude larger than observed. Furthermore, why rho_Lambda ~ rho_matter today is unexplained (coincidence problem).",
                what_theory_does_not_explain="Why the quantum vacuum does not gravitate at its natural cutoff scale, and whether dark energy is a static cosmological constant Lambda or dynamical field (quintessence).",
                established_quantitative_values={
                    "observed_rho_de_GeV4": "2.5e-47",
                    "planck_scale_rho_vac_GeV4": "3.5e73",
                    "mismatch_orders_of_magnitude": 121,
                    "desi_2024_hint": "w0 = -0.827, wa = -0.75 (2.5 - 3.9 sigma tension with LCDM)"
                },
                resolving_observation="High-precision measurement of the dark energy equation of state w(z) = w0 + wa(1-a) and growth rate of structure f*sigma_8(z). Detecting w(z) != -1 at > 5 sigma or growth rate deviations rules out a cosmological constant.",
                target_instruments=["Euclid Space Telescope", "Vera C. Rubin Observatory (LSST)", "Nancy Grace Roman Space Telescope", "DESI 5-Year"],
                falsification_metric="A measured equation of state w0 != -1 or wa != 0 at > 5 sigma falsifies Lambda-CDM; growth index gamma != 0.55 falsifies General Relativity on cosmological scales."
            ),
            CosmologicalOpenProblem(
                problem_id="OP-06",
                title="The Hubble Tension and Large-Scale Structure S8 Tension",
                theoretical_barrier="A persistent 4.9 - 5.3 sigma discrepancy exists between direct local measurements of H0 (SH0ES: 73.04 +/- 1.04 km/s/Mpc) and early-universe CMB + BAO inferences (Planck: 67.36 +/- 0.54 km/s/Mpc).",
                what_theory_does_not_explain="Whether the tension is due to unrecognized astrophysical systematic errors in the distance ladder or represents new physics (e.g., Early Dark Energy, decaying dark matter, primordial magnetic fields).",
                established_quantitative_values={
                    "planck_H0_km_s_Mpc": "67.36 +/- 0.54",
                    "shoes_H0_km_s_Mpc": "73.04 +/- 1.04",
                    "discrepancy_delta_H0": "5.68 km/s/Mpc",
                    "tension_significance": "4.90 sigma"
                },
                resolving_observation="Measurement of H0 via Gravitational Wave Standard Sirens (binary neutron star mergers with optical counterparts) independent of both the cosmic distance ladder and CMB sound horizon; combined with JWST cross-calibration of Cepheids, TRGB, and JAGB stars.",
                target_instruments=["LIGO/Virgo/KAGRA/Einstein Telescope", "JWST NIRCam", "Simons Observatory (high-ell polarization)"],
                falsification_metric="Standard siren H0 measurement achieving < 1% precision will definitively land on either 67.4 or 73.0 km/s/Mpc; high-multipole CMB polarization tests Early Dark Energy sound-horizon shrinking."
            ),
            CosmologicalOpenProblem(
                problem_id="OP-07",
                title="The Primordial Cosmological Lithium Problem",
                theoretical_barrier="Standard BBN using the Planck baryon density predicts an abundance of 7Li that is a factor of ~3 higher than observed in ancient halo stars (the Spite plateau).",
                what_theory_does_not_explain="Why low-metallicity Population II stars exhibit (7Li/H) = (1.58 +/- 0.11)e-10, whereas nuclear SBBN rigorously predicts (4.68 +/- 0.32)e-10 (> 5 sigma tension).",
                established_quantitative_values={
                    "theoretical_7Li_over_H": "4.68e-10",
                    "observed_spite_plateau_7Li_over_H": "1.58e-10",
                    "discrepancy_factor": 2.96,
                    "tension_significance": "> 5 sigma"
                },
                resolving_observation="Spectroscopic measurement of gas-phase 7Li in unevolved interstellar and intergalactic gas clouds outside stars (e.g. Damped Lyman-Alpha systems at high redshift) using next-generation ultra-high-resolution spectrographs.",
                target_instruments=["ELT-HIRES (Extremely Large Telescope)", "VLT-ESPRESSO", "Keck PEPSI"],
                falsification_metric="If pristine gas-phase (7Li/H) = 4.7e-10, stellar atmospheric depletion is proven and cosmology is saved. If gas-phase (7Li/H) = 1.6e-10, BSM nuclear destruction during BBN is established."
            ),
            CosmologicalOpenProblem(
                problem_id="OP-08",
                title="Cosmic Topology and Large-Angle CMB Anomalies",
                theoretical_barrier="Standard cosmology assumes an infinite, simply connected, statistically isotropic R^3 spatial geometry. However, large-angle CMB measurements show an absence of angular correlation above 60 degrees and multipole alignments (quadrupole-octopole alignment / 'Axis of Evil').",
                what_theory_does_not_explain="Whether large-angle anomalies are statistical flukes (cosmic variance) or reflect a multi-connected compact topology (e.g. 3-torus, Poincaré dodecahedral space) or anisotropic pre-inflationary initial conditions.",
                established_quantitative_values={
                    "two_point_correlation_above_60deg": "C(theta) ~ 0 (p-value < 0.1%)",
                    "quadrupole_octopole_alignment": "p-value < 0.1% - 0.5%",
                    "hemispherical_asymmetry": "~ 7% power discrepancy between hemispheres"
                },
                resolving_observation="Full-sky CMB polarization matched circles-in-the-sky search combined with 3D large-scale structure topology mapping using cosmic shear and galaxy clustering.",
                target_instruments=["LiteBIRD", "Euclid", "Vera C. Rubin Observatory (LSST)", "SPHEREx"],
                falsification_metric="Detection of identical temperature and polarization patterns in matched circle pairs proves compact multi-connected cosmic topology; 3D discrete power spectrum eigenmodes confirm topological boundary conditions."
            )
        ]

    def get_problem(self, problem_id: str) -> Optional[CosmologicalOpenProblem]:
        """Retrieves a specific open problem by ID."""
        for prob in self.problems:
            if prob.problem_id == problem_id:
                return prob
        return None

    def summarize_all(self) -> List[Dict[str, str]]:
        """Returns concise summary of all registered open problems and resolving observations."""
        return [
            {
                "id": p.problem_id,
                "problem": p.title,
                "resolving_observation": p.resolving_observation,
                "target_instruments": ", ".join(p.target_instruments),
                "falsification_metric": p.falsification_metric
            }
            for p in self.problems
        ]


# ==============================================================================
# 11. MAIN DEMONSTRATION & VERIFICATION ROUTINE
# ==============================================================================

def run_cosmogenesis_demonstration() -> Dict[str, Any]:
    """Executes complete demonstration of the cosmogenesis computational suite."""
    params = CosmologicalParameters()
    cmb = CMBBlackbodyThermodynamics(params.T0_CMB)
    bbn = StandardBigBangNucleosynthesis(params.omega_b)
    expansion = CosmicExpansionDynamics(params)
    tension = TensionAnalyzer()
    inflation = InflationaryCosmology()
    baryon = BaryogenesisAnalysis()
    dark = DarkSectorAnalysis(params.Omega_Lambda, params.Omega_c)
    registry = CosmogenesisOpenProblemsRegistry()

    return {
        "cosmological_parameters": {
            "H0_CMB": params.H0_CMB,
            "H0_local": params.H0_local,
            "T0_CMB": params.T0_CMB,
            "Omega_b": round(params.Omega_b, 4),
            "Omega_c": round(params.Omega_c, 4),
            "Omega_Lambda": round(params.Omega_Lambda, 4),
            "Omega_m": round(params.Omega_m, 4)
        },
        "cmb_thermodynamics": {
            "peak_frequency_GHz": round(cmb.peak_frequency() / 1e9, 2),
            "peak_wavelength_mm": round(cmb.peak_wavelength() * 1000.0, 3),
            "photon_density_cm3": round(cmb.photon_number_density() / 1e6, 2),
            "energy_density_eV_cm3": round((cmb.energy_density() / PhysicalConstants.eV_to_J) / 1e6, 4),
            "firas_limits": cmb.verify_firas_distortion_limits()
        },
        "bbn_results": bbn.comprehensive_bbn_comparison(),
        "expansion_distances_z1": {
            "comoving_distance_Mpc": round(expansion.comoving_distance_Mpc(1.0), 2),
            "luminosity_distance_Mpc": round(expansion.luminosity_distance_Mpc(1.0), 2),
            "angular_diameter_distance_Mpc": round(expansion.angular_diameter_distance_Mpc(1.0), 2)
        },
        "hubble_tension": tension.analyze_hubble_tension()["shoes_vs_planck"],
        "inflation_starobinsky": inflation.starobinsky_model(),
        "baryogenesis_evaluation": baryon.evaluate_sakharov_conditions(),
        "dark_energy_mismatch": dark.cosmological_constant_discrepancy(),
        "open_problems_count": len(registry.problems)
    }


if __name__ == "__main__":
    import json
    results = run_cosmogenesis_demonstration()
    print("=== COSMOGENESIS ENGINE DEMONSTRATION ===")
    print(json.dumps(results, indent=2))
