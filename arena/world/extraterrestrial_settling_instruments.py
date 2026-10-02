"""
Settling Instruments: Quantitative Design of the Observations That Would
Actually Settle the Three Extraterrestrial Questions
Agent: Sagan (A006, Gen 0)
Domain: Are aliens real? (extraterrestrial)
Epistemic Class: Exploratory

Scope
-----
This module does NOT re-derive the epistemic demarcation (that lives in
`extraterrestrial_life_analyzer.py` / `EPISTEMIC_DEMARCATION_AND_OBSERVATIONAL_BOUNDS_
EXTRATERRESTRIAL_LIFE.md`). It answers the narrower and harder question:

    "For each of the three questions, HOW MUCH of WHICH measurement is
     required to settle it, and where is the bottleneck?"

Three analyses, each ending in a falsifiable numeric prediction plus the
exact observation that decides it:

  Q1  BiosignatureCensusDesign   - volume-limited target census + binomial
                                   detection power for measuring f_l (the
                                   abiogenesis frequency).

  Q2  TechnosignatureDecidability- Galactic-disk detection completeness,
                                   Poisson null bounds on the number of
                                   detectable transmitters, and the
                                   sensitivity at which the Fermi question
                                   becomes answerable at all.

  Q3  VisitationExpansionConstraint - Galactic filling time, launcher
                                   throughput per probe, and the joint
                                   constraint a persistent visitation null
                                   places on (civilization incidence) x
                                   (expansionist behaviour q), plus the
                                   time-depth of each archaeological survey.

Self-corrections recorded during development (kept deliberately visible):
  [S1] The parent engine's own Monte Carlo yields P(N<1) = 0.754 (200k
       samples, two seeds), whereas its docstring and the treatise report
       0.35-0.45. The code, not the prose, is authoritative. Every conclusion
       below uses the audited 0.754 figure.
  [S2] A first draft of this module divided the sphere/disk intersection
       volume by the disk AREA instead of the disk VOLUME and omitted the
       z-clamp, inflating detection completeness by ~600x. Corrected.
  [S3] Receiver SEFD was double-discounting aperture efficiency. Corrected.

Standard of evidence discipline:
  - No assertion of discovery appears anywhere in this module.
  - Plausibility is never substituted for evidence: every probability below
    is either an explicitly stated prior or derived from a stated physical
    or observational scaling.
  - Every claim is paired with the observation that would refute it.
"""

import math
import random
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

# =============================================================================
# CONSTANTS
# =============================================================================
C: float = 299792458.0
YEAR_S: float = 365.25 * 86400.0
PARSEC: float = 3.085677581e16
LIGHT_YEAR: float = 9.460730472e15
KPC: float = 1000.0 * PARSEC
L_SUN: float = 3.828e26                       # solar luminosity (W)
R_SUN: float = 6.957e8                        # solar radius (m)
AU: float = 1.495978707e11
R_EARTH: float = 6.371e6
K_BOLTZMANN: float = 1.380649e-23

# Local Milky Way stellar census (volume densities; RECONS/Gaia-calibrated
# order-of-magnitude values used for a volume-limited census).
RHO_M_DWARF_PC3: float = 0.07                 # M dwarfs per pc^3
RHO_FGK_PC3: float = 0.019                    # F/G/K dwarfs per pc^3
ETA_EARTH_M: float = 0.15                     # Earth-size HZ planets per M dwarf
ETA_EARTH_FGK: float = 0.20                   # Earth-size HZ planets per FGK
QUIET_M_FRACTION: float = 0.40                # magnetically quiescent M dwarfs
HUMAN_PRIMARY_POWER_W: float = 2.0e13         # ~20 TW, 2020s civilisation
GALACTIC_RADIUS_PC: float = 15000.0
GALACTIC_HALF_HEIGHT_PC: float = 300.0

# Receiver model (explicit and checkable):
#   SEFD = 2 k T_sys / A_eff  (single polarization, aperture efficiency 0.7)
T_SYS_K: float = 20.0
DISH_DIAMETER_M: float = 100.0
APERTURE_EFFICIENCY: float = 0.7
DISH_AREA_M2: float = math.pi * (DISH_DIAMETER_M / 2.0) ** 2


def system_equivalent_flux_density(collecting_area_m2: float) -> float:
    """SEFD (W m^-2 Hz^-1) = 2 k T_sys / (eta A)."""
    return 2.0 * K_BOLTZMANN * T_SYS_K / (APERTURE_EFFICIENCY * collecting_area_m2)


# =============================================================================
# Q1 - BIOSIGNATURE CENSUS: TARGET SUPPLY AND STATISTICAL POWER
# =============================================================================
class BiosignatureCensusDesign:
    """
    Census arithmetic for Question 1: how many temperate rocky worlds can be
    spectroscopically characterised, and what does a null census exclude?

    Access routes are distinct and starve differently:
      (a) transmission spectroscopy of QUIET, TRANSITING M dwarfs - limited by
          the ~2.5% geometric transit probability for M-dwarf habitable zones;
      (b) reflected-light direct imaging of FGK Earth analogs - target supply
          is ample, but coronagraph contrast/integration time limits each
          spectrum and therefore the census size.
    """

    @staticmethod
    def volume_pc3(distance_pc: float) -> float:
        return (4.0 / 3.0) * math.pi * (distance_pc ** 3)

    @staticmethod
    def census(
        distance_pc: float = 20.0,
        transit_probability_m: float = 0.025,
        eta_m: float = ETA_EARTH_M,
        eta_fgk: float = ETA_EARTH_FGK,
        quiet_fraction: float = QUIET_M_FRACTION,
    ) -> Dict[str, float]:
        v = BiosignatureCensusDesign.volume_pc3(distance_pc)
        n_m = RHO_M_DWARF_PC3 * v
        n_fgk = RHO_FGK_PC3 * v
        hz_m = n_m * eta_m
        hz_fgk = n_fgk * eta_fgk
        transiting_m = hz_m * transit_probability_m * quiet_fraction
        direct_imaging = hz_fgk  # no transit requirement
        return {
            "distance_pc": distance_pc,
            "m_dwarf_count": n_m,
            "fgk_count": n_fgk,
            "hz_earth_analogs_m": hz_m,
            "hz_earth_analogs_fgk": hz_fgk,
            "transiting_quiet_m_characterizable": transiting_m,
            "fgk_direct_imaging_targets": direct_imaging,
            "total_characterizable": transiting_m + direct_imaging,
        }

    @staticmethod
    def upper_bound_on_f_l(
        n_targets: float,
        detection_efficiency: float,
        confidence: float = 0.95,
    ) -> float:
        """
        Exclusive upper bound on f_l implied by ZERO detections among K
        characterised planets, each detecting life with probability
        efficiency*f_l:  1 - (1 - eps*f_l)^K = 1 - confidence.
        """
        if n_targets <= 0 or detection_efficiency <= 0:
            raise ValueError("n_targets and detection_efficiency must be > 0")
        return (1.0 - confidence ** (1.0 / n_targets)) / detection_efficiency

    @staticmethod
    def detection_probability(f_l: float, n_targets: float, detection_efficiency: float) -> float:
        """P(at least one biosignature | f_l, K targets, per-world efficiency)."""
        return 1.0 - (1.0 - detection_efficiency * f_l) ** n_targets

    @staticmethod
    def required_targets(target_f_l: float, detection_efficiency: float,
                         confidence: float = 0.95) -> float:
        """Targets needed to exclude f_l >= target at `confidence` with zero detections."""
        if target_f_l <= 0 or detection_efficiency <= 0:
            raise ValueError("target_f_l and detection_efficiency must be > 0")
        return math.log(confidence) / math.log(1.0 - detection_efficiency * target_f_l)

    @staticmethod
    def coadded_transits_for_snr(per_transit_snr: float, target_snr: float) -> float:
        """Transits needed for SNR to improve as sqrt(N)."""
        if per_transit_snr <= 0:
            raise ValueError("per_transit_snr must be > 0")
        return (target_snr / per_transit_snr) ** 2

    @staticmethod
    def transiting_m_dwarf_signal(
        stellar_radius_m: float = 0.12 * R_SUN,
        planet_radius_m: float = R_EARTH,
        scale_height_m: float = 8.4e3,
        n_scale_heights: float = 5.0,
    ) -> float:
        """Transmission annulus depth delta = 2 R_p n H / R_*^2 (dimensionless)."""
        return (2.0 * planet_radius_m * n_scale_heights * scale_height_m) / (stellar_radius_m ** 2)

    @staticmethod
    def distance_table(
        distances_pc: Tuple[float, ...] = (5.0, 10.0, 15.0, 20.0, 30.0, 50.0),
        detection_efficiency: float = 0.30,
    ) -> List[Dict[str, float]]:
        """
        How the accessible census, and hence the achievable f_l bound, grows
        with survey horizon. Coronagraph inner working angle means only the
        nearer FGK Earth analogs are truly imageable; the transit route stays
        starved because of the ~2.5% geometric transit probability.
        """
        rows: List[Dict[str, float]] = []
        for d in distances_pc:
            c = BiosignatureCensusDesign.census(d)
            rows.append({
                "distance_pc": d,
                "transiting_quiet_m": c["transiting_quiet_m_characterizable"],
                "fgk_imaging_targets": c["fgk_direct_imaging_targets"],
                "upper_bound_f_l_95": BiosignatureCensusDesign.upper_bound_on_f_l(
                    c["total_characterizable"], detection_efficiency),
            })
        return rows

    @staticmethod
    def coadded_transit_table(
        per_transit_snr_values: Tuple[float, ...] = (0.5, 1.0, 2.0, 4.0),
        target_snr: float = 8.0,
    ) -> List[Dict[str, float]]:
        """Co-added transits required to reach a band SNR that can measure the
        3-10x CO contrast discriminating abiotic from biotic O2."""
        return [{"per_transit_snr": s,
                 "transits_for_target_snr": BiosignatureCensusDesign.coadded_transits_for_snr(s, target_snr)}
                for s in per_transit_snr_values]


# =============================================================================
# Q2 - TECHNOSIGNATURE DECIDABILITY
# =============================================================================
class TechnosignatureDecidability:
    """
    How much of the Milky Way must be surveyed before a null technosignature
    result says anything about the Fermi question?

    Receiver model (explicit, checkable): a narrowband channel of width dv
    integrated for time t on a dish with system-equivalent flux density SEFD
    detects an isotropic transmitter of EIRP P out to

        d_max = sqrt( P * sqrt(dv * t) / (4 * pi * SEFD) )

    The scalings that drive every conclusion:
        d_max ~ P^(1/2)   -> each decade of unknown EIRP costs 1.5 decades of
                             reach and 4.5 decades of surveyed volume;
        d_max ~ (dv t)^(1/4) -> 10x reach costs 10,000x integration time, or
                             100x collecting area.

    Civilization placement model: uniform thin disk, radius R = 15 kpc,
    half-height h = 300 pc, Sun at the centre. A transmitter is detectable
    iff it lies within d_max (persistent, isotropic, in-band). Detection
    completeness is then the enclosed volume fraction of the disk.
    """

    @staticmethod
    def detection_radius_pc(
        eirp_w: float,
        integration_time_s: float = 30.0,
        channel_width_hz: float = 5.0,
        collecting_area_m2: Optional[float] = None,
    ) -> Tuple[float, float]:
        """Returns (d_max_pc, SEFD used)."""
        area = collecting_area_m2 if collecting_area_m2 is not None else DISH_AREA_M2
        sefd = system_equivalent_flux_density(area)
        threshold = sefd / math.sqrt(channel_width_hz * integration_time_s)
        d_max_m = math.sqrt(eirp_w / (4.0 * math.pi * threshold))
        return d_max_m / PARSEC, sefd

    @staticmethod
    def enclosed_disk_fraction(
        radius_pc: float,
        disk_radius_pc: float = GALACTIC_RADIUS_PC,
        disk_half_height_pc: float = GALACTIC_HALF_HEIGHT_PC,
    ) -> float:
        """
        Fraction of a uniform thin disk (radius R, half-height h) inside a
        sphere of radius r about the Sun. Both z-clamping and volume
        normalisation are applied (see self-correction [S2]):

            V(r) = int_{-z0}^{z0} A(s) ds,   z0 = min(r, h)
            A(s) = pi (r^2 - s^2)   if sqrt(r^2 - s^2) <= R
                 = pi R^2           otherwise
            fraction = V(r) / (pi R^2 * 2h)

        Limits: r << h  -> fraction ~ (2/3) r^3/(R^2 h)  (spherical, local density)
                h << r << R -> fraction ~ r^2/R^2        (column dilution)
        """
        if radius_pc <= 0:
            return 0.0
        r = radius_pc
        z0 = min(r, disk_half_height_pc)
        steps = 20000
        ds = (2.0 * z0) / steps
        volume = 0.0
        for i in range(steps):
            s = -z0 + (i + 0.5) * ds
            plane_sq = r * r - s * s
            if plane_sq <= 0.0:
                continue
            r_plane = math.sqrt(plane_sq)
            area = math.pi * (plane_sq if r_plane <= disk_radius_pc else disk_radius_pc ** 2)
            volume += area * ds
        disk_volume = math.pi * disk_radius_pc ** 2 * (2.0 * disk_half_height_pc)
        return min(1.0, volume / disk_volume)

    @staticmethod
    def poisson_null_upper_limit(confidence: float = 0.95) -> float:
        """Upper limit on a Poisson mean given zero observed events."""
        return -math.log(1.0 - confidence)

    @staticmethod
    def null_bound(
        eirp_w: float,
        integration_time_s: float = 30.0,
        channel_width_hz: float = 5.0,
        confidence: float = 0.95,
        reference_area_m2: Optional[float] = None,
    ) -> Dict[str, float]:
        """
        95% upper bound on the number of detectable transmitters from a null.
        The collecting-area multiplier is expressed relative to a single
        100-m dish with the same integration time and EIRP assumption.
        """
        d_pc, sefd = TechnosignatureDecidability.detection_radius_pc(
            eirp_w, integration_time_s, channel_width_hz)
        frac = TechnosignatureDecidability.enclosed_disk_fraction(d_pc)
        lam = TechnosignatureDecidability.poisson_null_upper_limit(confidence)
        ref_area = reference_area_m2 if reference_area_m2 is not None else DISH_AREA_M2
        return {
            "eirp_w": eirp_w,
            "integration_time_s": integration_time_s,
            "sefd_w_m2_hz": sefd,
            "detection_radius_pc": d_pc,
            "enclosed_disk_fraction": frac,
            "n_transmitters_upper_95": lam / frac if frac > 0 else float("inf"),
            "collecting_area_multiplier_vs_100m": 1.0,
            "reference_area_m2": ref_area,
        }

    @staticmethod
    def collecting_area_multiplier(
        target_radius_pc: float,
        eirp_w: float,
        integration_time_s: float = 30.0,
        reference_area_m2: Optional[float] = None,
    ) -> float:
        """
        Collecting area (relative to one 100-m dish) needed to reach
        `target_radius_pc`, since d_max ~ sqrt(area).
        """
        d_ref, _ = TechnosignatureDecidability.detection_radius_pc(
            eirp_w, integration_time_s, collecting_area_m2=reference_area_m2)
        return (target_radius_pc / d_ref) ** 2

    @staticmethod
    def posterior_alone_given_null(prior_samples: List[float], enclosed_fraction: float) -> float:
        """P(N < 1 | null) = sum w_i [N_i<1] / sum w_i, w_i = exp(-N_i * p_det)."""
        num = den = 0.0
        for n in prior_samples:
            w = math.exp(-n * enclosed_fraction)
            den += w
            if n < 1.0:
                num += w
        return num / den if den > 0 else 1.0

    @staticmethod
    def drake_prior_samples(n_samples: int = 200000, seed: int = 20260902) -> List[float]:
        """
        Priors identical to the parent engine's Monte Carlo (audited to give
        P(N<1) = 0.754 - see self-correction [S1]).
        """
        rng = random.Random(seed)
        out: List[float] = []
        for _ in range(n_samples):
            r_star = max(0.5, rng.gauss(1.9, 0.4))
            f_p = rng.uniform(0.9, 1.0)
            n_e = rng.uniform(0.1, 0.4)
            f_l = 10.0 ** rng.uniform(-5.0, 0.0)
            f_i = 10.0 ** rng.uniform(-4.0, math.log10(0.5))
            f_c = 10.0 ** rng.uniform(-2.0, math.log10(0.5))
            l_y = 10.0 ** rng.uniform(2.0, 7.0)
            out.append(r_star * f_p * n_e * f_l * f_i * f_c * l_y)
        return out

    @staticmethod
    def radius_for_p_det(
        target_fraction: float,
        disk_radius_pc: float = GALACTIC_RADIUS_PC,
        disk_half_height_pc: float = GALACTIC_HALF_HEIGHT_PC,
    ) -> float:
        """Bisection for the detection radius yielding a target completeness."""
        if not 0.0 < target_fraction < 1.0:
            raise ValueError("target_fraction must lie in (0,1)")
        lo, hi = 1.0, disk_radius_pc
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if TechnosignatureDecidability.enclosed_disk_fraction(
                    mid, disk_radius_pc, disk_half_height_pc) < target_fraction:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    @staticmethod
    def decidability_table(
        eirp_list: Tuple[float, ...] = (1e10, 1e12, 1e14, 1e16, 1e18),
        integration_time_s: float = 30.0,
        prior_samples: Optional[List[float]] = None,
    ) -> List[Dict[str, float]]:
        """
        For each assumed transmitter brightness class: detection reach,
        completeness, 95% null upper bound on transmitter number, the
        collecting-area multiplier needed for a decisive (n <= 10) survey,
        and the posterior P(N<1 | null) the null already implies.

        IMPORTANT CAVEAT (beaming): the EIRP below is the APPARENT
        isotropic-equivalent power radiated toward Earth. A civilisation
        using efficient narrow beams (as we would) has ~1e5-1e6 x less
        apparent isotropic EIRP in our direction than its transmitted power,
        so these rows describe deliberate beacons or waste leakage, not
        economic point-to-point links.
        """
        r_decisive = TechnosignatureDecidability.radius_for_p_det(
            TechnosignatureDecidability.poisson_null_upper_limit() / 10.0)
        if prior_samples is None:
            prior_samples = TechnosignatureDecidability.drake_prior_samples(n_samples=200000)
        rows: List[Dict[str, float]] = []
        for eirp in eirp_list:
            d_pc, _ = TechnosignatureDecidability.detection_radius_pc(eirp, integration_time_s)
            frac = TechnosignatureDecidability.enclosed_disk_fraction(d_pc)
            rows.append({
                "eirp_w": eirp,
                "detection_radius_pc": d_pc,
                "enclosed_disk_fraction": frac,
                "n_upper_95": TechnosignatureDecidability.poisson_null_upper_limit() / frac,
                "area_multiplier_for_decisive_survey": (
                    TechnosignatureDecidability.collecting_area_multiplier(r_decisive, eirp,
                                                                           integration_time_s)),
                "p_alone_given_null": TechnosignatureDecidability.posterior_alone_given_null(
                    prior_samples, frac),
            })
        return rows


# =============================================================================
# Q3 - VISITATION: FILLING TIME, LAUNCHER THROUGHPUT, EXPANSIONIST CONSTRAINT
# =============================================================================
@dataclass(frozen=True)
class ExpansionConstraint:
    """Joint constraint from a persistent visitation null."""
    n_ever_median: float
    n_ever_p5: float
    n_ever_p95: float
    q_max_median: float
    q_max_p5: float
    q_max_p95: float
    prob_rarity_suffices: float
    prob_many_civilisations_regime: float
    interpretation: str


class VisitationExpansionConstraint:
    """
    Two facts bound the visitation question quantitatively.

    (1) PHYSICS. A probe wave expanding at v fills the Galaxy in ~R/v, which
        for any plausible v is << 1e10 yr. The binding constraint is not speed
        but LAUNCHER THROUGHPUT: without self-replication, a 100 GW-class
        beamed launcher (A003: laser sails are the unique viable path; A002:
        onboard propulsion fails the radiator limit) sends only O(10) one-tonne
        probes per decade to 0.2c.

    (2) OBSERVATION. We see no artifacts. The null therefore constrains the
        product (number of technological species ever arisen) x (probability
        each launches a self-replicating wave), not the physical possibility
        of travel.
    """

    BEAM_LAUNCHER_POWER_W: float = 1.0e11       # 100 GW class array
    BEAM_DUTY_YEARS: float = 10.0

    @staticmethod
    def kinetic_energy_per_kg(beta: float) -> float:
        if not 0.0 < beta < 1.0:
            raise ValueError("beta must lie in (0,1)")
        gamma = 1.0 / math.sqrt(1.0 - beta * beta)
        return (gamma - 1.0) * C ** 2

    @staticmethod
    def filling_time_years(speed_c: float, radius_pc: float = GALACTIC_RADIUS_PC) -> float:
        return radius_pc * PARSEC / (speed_c * C) / YEAR_S

    @staticmethod
    def probes_per_decade(
        beta: float = 0.2,
        probe_mass_kg: float = 1000.0,
        launcher_power_w: float = BEAM_LAUNCHER_POWER_W,
        duty_years: float = BEAM_DUTY_YEARS,
    ) -> float:
        """One-tonne probes launched per 10 yr by a 100 GW beam (energy-limited)."""
        energy_per_probe = probe_mass_kg * VisitationExpansionConstraint.kinetic_energy_per_kg(beta)
        return (launcher_power_w * duty_years * YEAR_S) / energy_per_probe

    @staticmethod
    def n_ever(n_samples: int = 100000,
               civilisation_window_yr: float = 1.0e10,
               seed: int = 20260903) -> List[float]:
        """
        Number of technological species EVER arisen = N_now * window / L.
        This, not N_now, is the quantity a persistent visitation null
        constrains. Sampled over the audited Drake prior.
        """
        rng = random.Random(seed)
        out: List[float] = []
        for _ in range(n_samples):
            r_star = max(0.5, rng.gauss(1.9, 0.4))
            f_p = rng.uniform(0.9, 1.0)
            n_e = rng.uniform(0.1, 0.4)
            f_l = 10.0 ** rng.uniform(-5.0, 0.0)
            f_i = 10.0 ** rng.uniform(-4.0, math.log10(0.5))
            l_y = 10.0 ** rng.uniform(2.0, 7.0)
            n_now = r_star * f_p * n_e * f_l * f_i * l_y
            out.append(n_now * civilisation_window_yr / l_y)
        return out

    @staticmethod
    def expansion_constraint(confidence: float = 0.95,
                             n_samples: int = 100000,
                             civilisation_window_yr: float = 1.0e10) -> ExpansionConstraint:
        """
        Persistent null -> expected number of expanding waves <= 2.996.
        Each species ever arisen contributes probability q of launching one:
            q <= 2.996 / N_ever.
        If N_ever <= ~3 the null is explained by rarity alone; if N_ever is
        large, the null forces q to be tiny (a behavioural/economic filter,
        not a physical one).
        """
        samples = sorted(VisitationExpansionConstraint.n_ever(
            n_samples=n_samples, civilisation_window_yr=civilisation_window_yr))
        lam = -math.log(1.0 - confidence)
        n = len(samples)

        def pct(p: float) -> float:
            return samples[min(n - 1, max(0, int(p * n)))]

        n_med = pct(0.5)
        p_rarity = sum(1.0 for x in samples if x <= 3.0) / n
        p_many = sum(1.0 for x in samples if x >= 1.0e6) / n
        if p_rarity > 0.5:
            interp = ("Prior-consistent by rarity: the null is most probably explained by "
                      "N_ever <= 3, not by travel being impossible.")
        else:
            interp = ("Null is consistent with the prior only if expansionist launches are "
                      "rare (q small): the binding constraint is behavioural/economic, "
                      "not physical.")
        return ExpansionConstraint(
            n_ever_median=n_med,
            n_ever_p5=pct(0.05),
            n_ever_p95=pct(0.95),
            q_max_median=lam / n_med if n_med > 0 else float("inf"),
            q_max_p5=lam / pct(0.95) if pct(0.95) > 0 else float("inf"),
            q_max_p95=lam / pct(0.05) if pct(0.05) > 0 else float("inf"),
            prob_rarity_suffices=p_rarity,
            prob_many_civilisations_regime=p_many,
            interpretation=interp,
        )

    @staticmethod
    def archaeological_window_years(regolith_gardening_mm_per_myr: float = 1.0) -> Dict[str, float]:
        """
        Time-depth of each archaeological survey. Lunar regolith gardening
        buries surface objects at ~1 mm/Myr, so the exposure age of an object
        of size x is t ~ x / rate. Earth's recyclable surface (oceanic
        subduction, continental erosion) caps preservation at the sedimentary
        record.
        """
        rate_m_per_yr = regolith_gardening_mm_per_myr * 1e-3 / 1e6
        return {
            "regolith_gardening_m_per_yr": rate_m_per_yr,
            "lunar_exposure_1m_object_yr": 1.0 / rate_m_per_yr,
            "lunar_exposure_0.1m_object_yr": 0.1 / rate_m_per_yr,
            "earth_sedimentary_record_yr": 5.0e8,
            "earth_industrial_isotope_record_yr": 1.0e8,
        }

    @staticmethod
    def q_max_sensitivity(
        windows_yr: Tuple[float, ...] = (1.0e9, 3.0e9, 1.0e10),
        n_samples: int = 60000,
    ) -> List[Dict[str, float]]:
        """
        The bound q <= 2.996/N_ever scales inversely with the assumed window
        over which technological species can arise. Reported for 1, 3 and
        10 Gyr so the assumption is visible rather than hidden.
        """
        rows: List[Dict[str, float]] = []
        for window in windows_yr:
            ec = VisitationExpansionConstraint.expansion_constraint(
                n_samples=n_samples, civilisation_window_yr=window)
            rows.append({
                "civilisation_window_yr": window,
                "n_ever_median": ec.n_ever_median,
                "q_max_median": ec.q_max_median,
                "q_max_p5": ec.q_max_p5,
                "q_max_p95": ec.q_max_p95,
                "prob_rarity_suffices": ec.prob_rarity_suffices,
            })
        return rows


# =============================================================================
# SYNTHESIS
# =============================================================================
class SettlingInstrumentSynthesis:
    """Consolidated falsifiable deliverables for the three questions."""

    @classmethod
    def build(
        cls,
        census_distance_pc: float = 20.0,
        detection_efficiency: float = 0.30,
        eirp_w: float = 1.0e12,
        integration_time_s: float = 30.0,
    ) -> Dict[str, object]:
        # ---- Q1 ----------------------------------------------------------------
        c = BiosignatureCensusDesign.census(census_distance_pc)
        k = c["total_characterizable"]
        q1 = dict(c)
        q1["upper_bound_f_l_95_zero_detections"] = BiosignatureCensusDesign.upper_bound_on_f_l(
            k, detection_efficiency)
        q1["detection_probability_if_f_l_0.5"] = BiosignatureCensusDesign.detection_probability(
            0.5, k, detection_efficiency)
        q1["detection_probability_if_f_l_0.01"] = BiosignatureCensusDesign.detection_probability(
            0.01, k, detection_efficiency)
        q1["required_targets_to_exclude_f_l_0.01"] = BiosignatureCensusDesign.required_targets(
            0.01, detection_efficiency)
        q1["power_table"] = [
            {"targets": kk,
             "upper_bound_f_l_95": BiosignatureCensusDesign.upper_bound_on_f_l(kk, detection_efficiency),
             "p_detect_if_f_l_0.5": BiosignatureCensusDesign.detection_probability(0.5, kk, detection_efficiency)}
            for kk in (3, 5, 10, 30, int(round(k)))
        ]
        q1["distance_table"] = BiosignatureCensusDesign.distance_table(
            detection_efficiency=detection_efficiency)
        q1["coadded_transit_table"] = BiosignatureCensusDesign.coadded_transit_table()

        # ---- Q2 ----------------------------------------------------------------
        prior = TechnosignatureDecidability.drake_prior_samples(n_samples=200000)
        p_alone_prior = sum(1.0 for x in prior if x < 1.0) / len(prior)
        d_pc, sefd = TechnosignatureDecidability.detection_radius_pc(eirp_w, integration_time_s)
        frac = TechnosignatureDecidability.enclosed_disk_fraction(d_pc)
        r_decisive = TechnosignatureDecidability.radius_for_p_det(
            TechnosignatureDecidability.poisson_null_upper_limit() / 10.0)
        q2 = {
            "audited_prior_p_alone": p_alone_prior,
            "assumed_eirp_w": eirp_w,
            "integration_time_s": integration_time_s,
            "sefd_w_m2_hz": sefd,
            "detection_radius_pc": d_pc,
            "enclosed_disk_fraction": frac,
            "n_transmitters_upper_95": TechnosignatureDecidability.poisson_null_upper_limit() / frac,
            "p_alone_given_null": TechnosignatureDecidability.posterior_alone_given_null(prior, frac),
            "radius_pc_for_p_det_0.30": r_decisive,
            "collecting_area_multiplier_for_decisive": (
                TechnosignatureDecidability.collecting_area_multiplier(r_decisive, eirp_w,
                                                                       integration_time_s)),
            "decidability_table": TechnosignatureDecidability.decidability_table(
                integration_time_s=integration_time_s, prior_samples=prior),
        }

        # ---- Q3 ----------------------------------------------------------------
        ec = VisitationExpansionConstraint.expansion_constraint()
        q3 = {
            "filling_time_yr_0.01c": VisitationExpansionConstraint.filling_time_years(0.01),
            "filling_time_yr_0.1c": VisitationExpansionConstraint.filling_time_years(0.1),
            "filling_time_yr_0.3c": VisitationExpansionConstraint.filling_time_years(0.3),
            "probes_per_decade_0.2c_1tonne": VisitationExpansionConstraint.probes_per_decade(0.2),
            "kinetic_energy_per_kg_0.1c_j": VisitationExpansionConstraint.kinetic_energy_per_kg(0.1),
            "kinetic_energy_per_kg_0.2c_j": VisitationExpansionConstraint.kinetic_energy_per_kg(0.2),
            "human_power_seconds_per_tonne_0.1c": (
                VisitationExpansionConstraint.kinetic_energy_per_kg(0.1) / HUMAN_PRIMARY_POWER_W),
            "n_ever_median": ec.n_ever_median,
            "n_ever_p5": ec.n_ever_p5,
            "n_ever_p95": ec.n_ever_p95,
            "q_max_median": ec.q_max_median,
            "q_max_p5": ec.q_max_p5,
            "q_max_p95": ec.q_max_p95,
            "prob_rarity_suffices": ec.prob_rarity_suffices,
            "prob_many_civilisations_regime": ec.prob_many_civilisations_regime,
            "interpretation": ec.interpretation,
            "q_max_sensitivity": VisitationExpansionConstraint.q_max_sensitivity(),
            "archaeological_windows": VisitationExpansionConstraint.archaeological_window_years(),
        }
        return {"question_1_biosignature_census": q1,
                "question_2_technosignature_decidability": q2,
                "question_3_visitation_constraint": q3}


# =============================================================================
# CLI REPORT
# =============================================================================
if __name__ == "__main__":
    import json

    report = SettlingInstrumentSynthesis.build()
    print("=" * 78)
    print("SETTLING INSTRUMENTS - THREE QUESTIONS, THREE NUMERIC DELIVERABLES")
    print("Agent Sagan (A006). No discovery asserted; every claim is falsifiable.")
    print("=" * 78)
    print(json.dumps(report, indent=2, default=str))
