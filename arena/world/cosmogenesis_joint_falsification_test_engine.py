"""
cosmogenesis_joint_falsification_test_engine.py

Definitive Quantitative Falsification and Arbitration Engine:
Formalizing the joint Euclid + Nancy Grace Roman Space Telescope tomographic
bandpower observables that decisively arbitrate between:
  1. Decaying Cold Dark Matter (DCDM: f_dcdm ~ 3.5%, tau ~ 30 Gyr)
  2. Stable Cold Dark Matter with Enhanced AGN Baryonic Feedback (A_bary ~ 1.30, BAHAMAS)
  3. Fiducial Planck Lambda-CDM (Null Hypothesis: f_dcdm = 0, A_bary = 1.0)

Authored by Agent Raman (A002), Generation 0.
Collaborator: Agent Kepler (A001), Generation 0.
Domain: Ratified consensus: origin of the universe (phase4-consensus).
"""

import math
from dataclasses import dataclass
from typing import Dict, Any, List, Tuple


# Fundamental Physical Constants
C_LIGHT_KM_S: float = 299792.458               # km/s
MPC_TO_KM: float = 3.08567758149e19             # km per Mpc
SEC_PER_GYR: float = 3.15576e16                 # seconds per Gyr
SQ_DEG_IN_SKY: float = 41252.96                 # Total square degrees on celestial sphere
ARCMIN2_PER_STERADIAN: float = (180.0 * 60.0 / math.pi) ** 2  # ~ 1.1818e7 arcmin^2 / sr


@dataclass(frozen=True)
class BandpowerSpecification:
    """Bandpower bin definition in multipole space."""
    band_id: int
    ell_min: float
    ell_max: float
    ell_center: float
    survey: str  # 'Euclid', 'Roman', or 'Joint'


@dataclass(frozen=True)
class ArbitrationResult:
    """Result of the joint arbitration decision test."""
    verdict: str
    decision_quadrant: int
    s_curv_observed: float
    g_tomo_observed: float
    delta_stellar_observed: float
    y_tsz_observed: float
    delta_chi2_agn_vs_dcdm: float
    bayes_factor_ln_b: float
    sigma_separation: float
    p_dcdm: float
    p_agn: float


class CosmogenesisJointFalsificationEngine:
    """
    Formalizes the tomographic bandpower observables, covariance matrices,
    Fisher forecasting, and Bayesian arbitration framework for Euclid + Roman.
    """

    def __init__(self):
        # Cosmological baseline
        self.H0 = 67.36
        self.h = 0.6736
        self.Omega_m = 0.3138
        self.Omega_L = 1.0 - self.Omega_m

        # Survey parameters
        self.euclid_area_sqdeg = 15000.0
        self.euclid_f_sky = self.euclid_area_sqdeg / SQ_DEG_IN_SKY  # 0.3636
        self.euclid_n_eff = 30.0  # arcmin^-2
        self.euclid_sigma_eps = 0.28

        self.roman_area_sqdeg = 2000.0
        self.roman_f_sky = self.roman_area_sqdeg / SQ_DEG_IN_SKY    # 0.0485
        self.roman_n_eff = 51.0   # arcmin^-2
        self.roman_sigma_eps = 0.28

        # Tomographic redshift bins (5 bins)
        self.tomo_bins = [
            {"id": 1, "z_min": 0.2, "z_max": 0.5, "z_mean": 0.35, "chi_mpc": 1380.0},
            {"id": 2, "z_min": 0.5, "z_max": 0.8, "z_mean": 0.65, "chi_mpc": 2340.0},
            {"id": 3, "z_min": 0.8, "z_max": 1.1, "z_mean": 0.95, "chi_mpc": 3120.0},
            {"id": 4, "z_min": 1.1, "z_max": 1.5, "z_mean": 1.30, "chi_mpc": 3890.0},
            {"id": 5, "z_min": 1.5, "z_max": 2.2, "z_mean": 1.80, "chi_mpc": 4750.0},
        ]

        # Define 10 distinct bandpower intervals spanning linear to deep non-linear scales
        self.bandpowers = [
            # Euclid Linear & Intermediate Bands
            BandpowerSpecification(1, 100.0, 250.0, 158.1, "Euclid"),      # Band 1: Linear anchor
            BandpowerSpecification(2, 250.0, 600.0, 387.3, "Euclid"),      # Band 2: Intermediate linear
            BandpowerSpecification(3, 600.0, 1200.0, 848.5, "Euclid"),     # Band 3: Onset of non-linear
            BandpowerSpecification(4, 1200.0, 2000.0, 1549.2, "Joint"),    # Band 4: Degeneracy crossing zone
            BandpowerSpecification(5, 2000.0, 3200.0, 2529.8, "Joint"),    # Band 5: DCDM plateau vs AGN descent
            BandpowerSpecification(6, 3200.0, 5000.0, 4000.0, "Joint"),    # Band 6: Maximum AGN spoon dip
            # Roman High-Multipole Deep Bands (Space PSF stability)
            BandpowerSpecification(7, 5000.0, 6500.0, 5700.9, "Roman"),    # Band 7: Deep non-linear
            BandpowerSpecification(8, 6500.0, 8000.0, 7211.1, "Roman"),    # Band 8: AGN stellar core turnaround
            BandpowerSpecification(9, 8000.0, 10000.0, 8944.3, "Roman"),   # Band 9: Stellar core rebound
            BandpowerSpecification(10, 10000.0, 13000.0, 11401.8, "Roman"),# Band 10: Deep baryonic cusp
        ]

    def hubble_z(self, z: float) -> float:
        """H(z) in km/s/Mpc."""
        return self.H0 * math.sqrt(self.Omega_m * (1.0 + z) ** 3 + self.Omega_L)

    def cosmic_time_gyr(self, z: float) -> float:
        """Cosmic time in Gyr from Big Bang to redshift z."""
        n_steps = 150
        z_high = max(z + 50.0, 100.0)
        dz = (z_high - z) / n_steps
        t_int = 0.0
        for i in range(n_steps):
            z_mid = z + (i + 0.5) * dz
            h_mid = self.hubble_z(z_mid)
            t_int += dz / ((1.0 + z_mid) * h_mid)
        return t_int * (MPC_TO_KM / SEC_PER_GYR)

    def dcdm_transfer_ratio(self, k_h_mpc: float, z: float, f_dcdm: float = 0.035, tau_gyr: float = 30.0) -> float:
        """
        Suppression ratio P_dcdm / P_dmo.
        On scales k > 1 h/Mpc, suppression approaches a strictly scale-independent plateau:
        R(k) = 1 - 2.2 * f_decay(z)
        """
        t_z = self.cosmic_time_gyr(z)
        decay_frac = f_dcdm * (1.0 - math.exp(-t_z / tau_gyr))
        k_trans = 0.18  # h/Mpc
        transfer = (k_h_mpc / k_trans) ** 2 / (1.0 + (k_h_mpc / k_trans) ** 2)
        return max(0.01, 1.0 - 2.2 * decay_frac * transfer)

    def agn_baryonic_transfer_ratio(self, k_h_mpc: float, z: float, A_bary: float = 1.30) -> float:
        """
        Suppression ratio P_bary / P_dmo from halo gas ejection (BAHAMAS / HMcode).
        Features:
          - Gas conservation on linear scales (R -> 1 for k < 0.2 h/Mpc)
          - Pronounced spoon dip peaking around k ~ 4 - 8 h/Mpc
          - Stellar cusp recovery upturn for k > 10 h/Mpc
        """
        # Redshift evolution factor G(z)
        g_z = (1.0 + 0.6 * z) / (1.0 + 0.8 * (z ** 1.8))
        dip = (k_h_mpc / 1.0) ** 1.5 / (1.0 + (k_h_mpc / 1.0) ** 1.5 + 0.1 * (k_h_mpc / 6.0) ** 3)
        k_star = 10.0
        stellar = 0.20 * (k_h_mpc / k_star) ** 2 / (1.0 + (k_h_mpc / k_star) ** 2)
        return max(0.01, 1.0 - A_bary * 0.20 * g_z * dip + A_bary * stellar)

    def fiducial_convergence_spectrum(self, ell: float, bin_idx: int) -> float:
        """Fiducial C_ell^kappa for tomographic bin bin_idx under Dark Matter Only (DMO)."""
        z_mean = self.tomo_bins[bin_idx]["z_mean"]
        amp = 1.15e-4 * ((z_mean / 0.8) ** 1.35)
        return amp * ((ell / 100.0) ** (-1.18))

    def bandpower_convergence_spectrum(
        self, band: BandpowerSpecification, bin_idx: int, f_dcdm: float = 0.0, tau_gyr: float = 30.0, A_bary: float = 0.0
    ) -> float:
        """
        Computes the bandpower C_b^kappa at band.ell_center.
        Baseline DMO has f_dcdm = 0.0, A_bary = 0.0.
        Standard feedback has A_bary = 1.0.
        Enhanced AGN feedback has A_bary = 1.3.
        """
        c_fid = self.fiducial_convergence_spectrum(band.ell_center, bin_idx)
        b = self.tomo_bins[bin_idx]
        chi_eff = 0.5 * b["chi_mpc"] * self.h
        k_eff = band.ell_center / max(50.0, chi_eff)

        r_dcdm = self.dcdm_transfer_ratio(k_eff, b["z_mean"], f_dcdm, tau_gyr)
        r_bary = self.agn_baryonic_transfer_ratio(k_eff, b["z_mean"], A_bary) if A_bary > 0.0 else 1.0
        return c_fid * r_dcdm * r_bary

    def bandpower_variance(self, band: BandpowerSpecification, bin_idx: int, survey: str) -> float:
        """
        Computes the Gaussian variance of bandpower C_b^kappa:
        Var(C_b) = 2 / ((2*ell + 1) * f_sky * Delta_ell) * (C_b + N_b)^2
        """
        ell = band.ell_center
        delta_ell = band.ell_max - band.ell_min

        if survey.lower() == "euclid":
            f_sky = self.euclid_f_sky
            n_bin = (self.euclid_n_eff / 5.0) * ARCMIN2_PER_STERADIAN
            n_b = (self.euclid_sigma_eps ** 2) / n_bin
        elif survey.lower() == "roman":
            f_sky = self.roman_f_sky
            n_bin = (self.roman_n_eff / 5.0) * ARCMIN2_PER_STERADIAN
            n_b = (self.roman_sigma_eps ** 2) / n_bin
        else:  # Joint inverse-variance combination
            var_e = self.bandpower_variance(band, bin_idx, "euclid")
            var_r = self.bandpower_variance(band, bin_idx, "roman")
            return 1.0 / (1.0 / var_e + 1.0 / var_r)

        c_b = self.fiducial_convergence_spectrum(ell, bin_idx)
        prefactor = 2.0 / ((2.0 * ell + 1.0) * f_sky * delta_ell)
        return prefactor * ((c_b + n_b) ** 2)

    # -------------------------------------------------------------
    # THE FOUR FORMAL FALSIFICATION OBSERVABLES
    # -------------------------------------------------------------

    def observable_1_curvature_spoon_index(self, f_dcdm: float, tau_gyr: float, A_bary: float, bin_idx: int = 2) -> float:
        """
        Observable 1: High-ell Curvature / Spoon Index (S_curv).
        Measures the suppression ratio between Band 6 (ell ~ 4000, peak AGN spoon dip)
        and Band 1 (ell ~ 158, linear anchor), relative to DMO:
          S_curv = R(Band 6) / R(Band 1)
        - DCDM predicts S_curv ~ 0.992 (scale-invariant plateau across non-linear modes).
        - AGN feedback predicts S_curv ~ 0.836 (16.4% spoon dip deficit).
        """
        band1 = self.bandpowers[0]  # ell_center ~ 158.1
        band6 = self.bandpowers[5]  # ell_center ~ 4000.0

        c1_mod = self.bandpower_convergence_spectrum(band1, bin_idx, f_dcdm, tau_gyr, A_bary)
        c6_mod = self.bandpower_convergence_spectrum(band6, bin_idx, f_dcdm, tau_gyr, A_bary)

        c1_dmo = self.bandpower_convergence_spectrum(band1, bin_idx, 0.0, tau_gyr, 0.0)
        c6_dmo = self.bandpower_convergence_spectrum(band6, bin_idx, 0.0, tau_gyr, 0.0)

        r6 = c6_mod / c6_dmo
        r1 = c1_mod / c1_dmo
        return r6 / r1

    def observable_2_tomographic_growth_ratio(
        self, f_dcdm: float, tau_gyr: float, A_bary: float, match_physical_k: bool = True, k_fixed: float = 1.5, band_idx: int = 3
    ) -> float:
        """
        Observable 2: Tomographic Time-Evolution Gradient (G_tomo).
        Ratio of fractional power suppression in low-z Bin 1 (z_mean = 0.35, t = 9.8 Gyr)
        relative to high-z Bin 5 (z_mean = 1.80, t = 3.6 Gyr).
        When match_physical_k=True (3D cosmic shear reconstruction at fixed k = 1.5 h/Mpc):
          - DCDM predicts G_tomo = (1 - e^-t1/tau) / (1 - e^-t5/tau) ~ 2.43
          - AGN feedback scales with halo virial dynamics G(z), yielding G_tomo ~ 1.76.
        When fixed angular multipole band is used (match_physical_k=False):
          - Limber wavenumber shift k = ell / chi(z) shifts the effective scale between bins.
        """
        if match_physical_k:
            r1_dcdm = self.dcdm_transfer_ratio(k_fixed, 0.35, f_dcdm, tau_gyr)
            r1_bary = self.agn_baryonic_transfer_ratio(k_fixed, 0.35, A_bary) if A_bary > 0.0 else 1.0
            supp1 = max(1e-5, 1.0 - r1_dcdm * r1_bary)

            r5_dcdm = self.dcdm_transfer_ratio(k_fixed, 1.80, f_dcdm, tau_gyr)
            r5_bary = self.agn_baryonic_transfer_ratio(k_fixed, 1.80, A_bary) if A_bary > 0.0 else 1.0
            supp5 = max(1e-5, 1.0 - r5_dcdm * r5_bary)
            return supp1 / supp5

        band = self.bandpowers[band_idx]
        c1_mod = self.bandpower_convergence_spectrum(band, 0, f_dcdm, tau_gyr, A_bary)
        c1_dmo = self.bandpower_convergence_spectrum(band, 0, 0.0, tau_gyr, 0.0)
        supp1 = max(1e-5, 1.0 - (c1_mod / c1_dmo))

        c5_mod = self.bandpower_convergence_spectrum(band, 4, f_dcdm, tau_gyr, A_bary)
        c5_dmo = self.bandpower_convergence_spectrum(band, 4, 0.0, tau_gyr, 0.0)
        supp5 = max(1e-5, 1.0 - (c5_mod / c5_dmo))

        return supp1 / supp5

    def observable_3_stellar_rebound_cusp(self, f_dcdm: float, tau_gyr: float, A_bary: float, bin_idx: int = 2) -> float:
        """
        Observable 3: Roman Ultra-High-Multipole Stellar Rebound (Delta_stellar).
        Measures the relative rebound of Band 10 (ell ~ 11400) compared to Band 6 (ell ~ 4000):
          Delta_stellar = [R(Band 10) / R(Band 6)] - 1.0
        - DCDM predicts Delta_stellar ~ 0.00 (flat plateau continues out to ell = 13000).
        - AGN feedback predicts Delta_stellar ~ +0.108 (+10.8% rebound from cooled stellar cusp).
        """
        band6 = self.bandpowers[5]   # ell ~ 4000
        band10 = self.bandpowers[9]  # ell ~ 11400

        c6_mod = self.bandpower_convergence_spectrum(band6, bin_idx, f_dcdm, tau_gyr, A_bary)
        c10_mod = self.bandpower_convergence_spectrum(band10, bin_idx, f_dcdm, tau_gyr, A_bary)

        c6_dmo = self.bandpower_convergence_spectrum(band6, bin_idx, 0.0, tau_gyr, 0.0)
        c10_dmo = self.bandpower_convergence_spectrum(band10, bin_idx, 0.0, tau_gyr, 0.0)

        r6 = c6_mod / c6_dmo
        r10 = c10_mod / c10_dmo
        return (r10 / r6) - 1.0

    def observable_4_tsz_cross_correlation_amplitude(self, A_bary: float) -> float:
        """
        Observable 4: Orthogonal Thermal Sunyaev-Zel'dovich (tSZ) Pressure Amplitude (y_tsz).
        Normalized Compton-y cross-correlation amplitude from Simons Observatory / CMB-S4:
          y_tsz = <kappa * y> / <kappa * y>_fiducial
        - DCDM has no direct electromagnetic pressure signature: y_tsz = 1.00 +/- 0.02
        - AGN feedback ejects gas and alters cluster thermal profiles: y_tsz = 1.0 - 0.60 * (A_bary - 1.0)
        For A_bary = 1.30, y_tsz ~ 0.82.
        """
        if A_bary <= 0.0:
            return 1.00
        return max(0.2, 1.0 - 0.60 * (A_bary - 1.0))

    # -------------------------------------------------------------
    # JOINT SURVEY FISHER MATRIX & ARBITRATION TEST
    # -------------------------------------------------------------

    def compute_joint_bandpower_chi2(
        self, f_dcdm_test: float, tau_gyr_test: float, A_bary_test: float,
        f_dcdm_true: float, tau_gyr_true: float, A_bary_true: float
    ) -> float:
        """
        Evaluates the total chi^2 difference across all 10 bandpowers and 5 tomographic bins
        for the combined Euclid + Roman survey.
        """
        total_chi2 = 0.0
        for band in self.bandpowers:
            # Select optimal survey coverage per band
            if band.survey == "Euclid":
                survey = "euclid"
            elif band.survey == "Roman":
                survey = "roman"
            else:
                survey = "joint"

            for b_idx in range(len(self.tomo_bins)):
                c_test = self.bandpower_convergence_spectrum(band, b_idx, f_dcdm_test, tau_gyr_test, A_bary_test)
                c_true = self.bandpower_convergence_spectrum(band, b_idx, f_dcdm_true, tau_gyr_true, A_bary_true)
                var = self.bandpower_variance(band, b_idx, survey)
                delta = c_test - c_true
                total_chi2 += (delta ** 2) / var

        return total_chi2

    def compute_fisher_elements(self) -> Dict[str, float]:
        """
        Computes the Fisher Information Matrix elements for [f_dcdm, A_bary]
        evaluated around the fiducial cosmology, demonstrating parameter un-degeneracy.
        Includes cosmic shear across 10 bands and 5 bins, plus Simons Obs tSZ gas prior.
        """
        df = 0.005
        da = 0.05
        fid_f = 0.0
        fid_a = 1.0
        tau = 30.0

        f_ff = 0.0
        f_aa = 0.0
        f_fa = 0.0

        for band in self.bandpowers:
            survey = "joint" if band.survey == "Joint" else band.survey.lower()
            for b_idx in range(len(self.tomo_bins)):
                var = self.bandpower_variance(band, b_idx, survey)

                c_base = self.bandpower_convergence_spectrum(band, b_idx, fid_f, tau, fid_a)
                c_df = self.bandpower_convergence_spectrum(band, b_idx, fid_f + df, tau, fid_a)
                c_da = self.bandpower_convergence_spectrum(band, b_idx, fid_f, tau, fid_a + da)

                dc_df = (c_df - c_base) / df
                dc_da = (c_da - c_base) / da

                f_ff += (dc_df * dc_df) / var
                f_aa += (dc_da * dc_da) / var
                f_fa += (dc_df * dc_da) / var

        # Shear alone determinant proves non-singularity
        det_shear = f_ff * f_aa - (f_fa ** 2)

        # Joint analysis includes orthogonal tSZ cluster gas prior from Simons Observatory
        f_aa_prior = 1.0 / (0.04 ** 2)  # sigma_A_bary = 0.04 from tSZ
        f_aa_total = f_aa + f_aa_prior

        det_total = f_ff * f_aa_total - (f_fa ** 2)
        inv_ff = f_aa_total / det_total if det_total > 0 else 0.0
        inv_aa = f_ff / det_total if det_total > 0 else 0.0
        inv_fa = -f_fa / det_total if det_total > 0 else 0.0

        sigma_f = math.sqrt(max(0.0, inv_ff))
        sigma_a = math.sqrt(max(0.0, inv_aa))
        corr_param = inv_fa / math.sqrt(max(1e-10, inv_ff * inv_aa))

        return {
            "F_ff": f_ff,
            "F_aa": f_aa,
            "F_fa": f_fa,
            "det_shear": det_shear,
            "det_total": det_total,
            "sigma_f_dcdm": sigma_f,
            "sigma_A_bary": sigma_a,
            "parameter_correlation": corr_param,
        }

    def execute_arbitration_test(
        self, s_curv_obs: float, g_tomo_obs: float, delta_stellar_obs: float, y_tsz_obs: float
    ) -> ArbitrationResult:
        """
        Executes the formal 4-observable Bayesian arbitration test.
        Decision Quadrants:
          1: DCDM Confirmed, Stable CDM Falsified (S_curv > 0.96, y_tsz > 0.94, Delta_stellar < 0.02)
          2: Stable CDM + AGN Confirmed, DCDM Falsified (S_curv < 0.88, y_tsz < 0.88, Delta_stellar > 0.05)
          3: Hybrid Regime (both DCDM and AGN contribute)
          4: Vanilla Lambda-CDM Null Hypothesis Restored
        """
        # Quantitative separation between models in joint chi^2 space
        # True = DCDM (3.5%), Test = AGN (1.30)
        chi2_separation = self.compute_joint_bandpower_chi2(
            f_dcdm_test=0.0, tau_gyr_test=30.0, A_bary_test=1.30,
            f_dcdm_true=0.035, tau_gyr_true=30.0, A_bary_true=0.00
        )
        sigma_sep = math.sqrt(max(0.0, chi2_separation))
        bayes_factor = 0.5 * chi2_separation

        if s_curv_obs >= 0.96 and y_tsz_obs >= 0.94 and delta_stellar_obs <= 0.025:
            quadrant = 1
            verdict = "DCDM CONFIRMED; STABLE CDM + AGN FALSIFIED"
            p_dcdm = 1.0 / (1.0 + math.exp(-min(50.0, bayes_factor)))
            p_agn = 1.0 - p_dcdm
        elif s_curv_obs <= 0.88 and y_tsz_obs <= 0.88 and delta_stellar_obs >= 0.050:
            quadrant = 2
            verdict = "STABLE CDM + AGN CONFIRMED; DCDM FALSIFIED"
            p_agn = 1.0 / (1.0 + math.exp(-min(50.0, bayes_factor)))
            p_dcdm = 1.0 - p_agn
        elif 0.88 < s_curv_obs < 0.96 or 0.88 < y_tsz_obs < 0.94:
            quadrant = 3
            verdict = "HYBRID COEXISTENCE REGIME (DCDM + AGN JOINT CONTRIBUTION)"
            p_dcdm = 0.50
            p_agn = 0.50
        else:
            quadrant = 4
            verdict = "VANILLA LAMBDA-CDM RESTORED (NULL HYPOTHESIS)"
            p_dcdm = 0.01
            p_agn = 0.01

        return ArbitrationResult(
            verdict=verdict,
            decision_quadrant=quadrant,
            s_curv_observed=s_curv_obs,
            g_tomo_observed=g_tomo_obs,
            delta_stellar_observed=delta_stellar_obs,
            y_tsz_observed=y_tsz_obs,
            delta_chi2_agn_vs_dcdm=chi2_separation,
            bayes_factor_ln_b=bayes_factor,
            sigma_separation=sigma_sep,
            p_dcdm=p_dcdm,
            p_agn=p_agn,
        )
