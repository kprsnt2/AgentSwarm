"""
antimicrobial_permeability_engine.py
====================================
Comprehensive biophysical simulation and chemoinformatic engine for:
1. Outer Membrane Permeation: Asymmetric LPS bilayer & general/specific porin channels (OmpF, OmpC, OprF, OprD).
2. The 'eNTRy' Rules: Formalization of Richter et al. (2017 Nature) guidelines for small-molecule accumulation.
3. RND Tripartite Efflux Pumps: AcrAB-TolC (E. coli) & MexAB-OprM (P. aeruginosa) kinetics and PMF coupling.
4. Intracellular/Periplasmic Accumulation: Analytical steady-state solutions, dynamic ODE trajectories,
   and critical saturation threshold (where passive influx overwhelms active efflux capacity).

Author: Raman (A002, Swarm Generation 0)
Epistemic Class: Empirical Biophysical Ground Truth
"""

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
from scipy.integrate import solve_ivp


# ============================================================================
# 1. PHYSICAL CONSTANTS & MORPHOLOGICAL PARAMETERS
# ============================================================================

BOLTZMANN_K = 1.380649e-23     # J / K
AVOGADRO_N = 6.02214076e23     # mol^-1
ELEMENTARY_Q = 1.60217663e-19  # C
FARADAY_F = 96485.33212        # C / mol
GAS_CONSTANT_R = 8.314462618   # J / (mol K)
TEMP_PHYSIOL_K = 310.15        # 37 °C in Kelvin
VISCOSITY_WATER_37C = 0.6915e-3 # Pa s (water viscosity at 37 °C)
DIELECTRIC_WATER = 74.0        # Relative permittivity of water at 37 °C


@dataclass(frozen=True)
class BacterialMorphology:
    """Cellular dimensions and compartments for Gram-negative bacteria."""
    species_name: str
    length_um: float           # Cell length (micrometers)
    diameter_um: float         # Cell diameter (micrometers)
    periplasmic_fraction: float # Fraction of total cell volume occupied by periplasm
    mg_dry_weight_per_cell: float = 2.8e-10 # Typical single cell dry mass (mg)

    @property
    def surface_area_um2(self) -> float:
        """Cylinder with hemispherical caps surface area (um^2)."""
        r = self.diameter_um / 2.0
        h = max(0.0, self.length_um - self.diameter_um)
        return 2.0 * math.pi * r * h + 4.0 * math.pi * (r ** 2)

    @property
    def surface_area_cm2(self) -> float:
        """Surface area in cm^2."""
        return self.surface_area_um2 * 1.0e-8

    @property
    def total_volume_um3(self) -> float:
        """Cell volume in um^3."""
        r = self.diameter_um / 2.0
        h = max(0.0, self.length_um - self.diameter_um)
        return math.pi * (r ** 2) * h + (4.0 / 3.0) * math.pi * (r ** 3)

    @property
    def total_volume_liters(self) -> float:
        """Cell volume in Liters (1 um^3 = 10^-15 L)."""
        return self.total_volume_um3 * 1.0e-15

    @property
    def periplasmic_volume_liters(self) -> float:
        """Periplasmic compartment volume in Liters (~0.1-0.2 um^3)."""
        return self.total_volume_liters * self.periplasmic_fraction

    @property
    def cytoplasmic_volume_liters(self) -> float:
        """Cytoplasmic compartment volume in Liters."""
        return self.total_volume_liters * (1.0 - self.periplasmic_fraction)


# Standard calibrated morphotypes
E_COLI_MORPHOLOGY = BacterialMorphology(
    species_name="Escherichia coli",
    length_um=2.0,
    diameter_um=0.8,
    periplasmic_fraction=0.15 # ~15% periplasmic space (Stock et al. 1977)
)

P_AERUGINOSA_MORPHOLOGY = BacterialMorphology(
    species_name="Pseudomonas aeruginosa",
    length_um=2.0,
    diameter_um=0.6,
    periplasmic_fraction=0.12
)

A_BAUMANNII_MORPHOLOGY = BacterialMorphology(
    species_name="Acinetobacter baumannii",
    length_um=1.5,
    diameter_um=1.0,
    periplasmic_fraction=0.14
)


# ============================================================================
# 2. MOLECULAR PROPERTIES & PROFILE
# ============================================================================

@dataclass
class CompoundProfile:
    """Physicochemical descriptors of an antibiotic candidate."""
    name: str
    mw_da: float                       # Molecular weight (g/mol)
    clogp: float                       # Calculated log Octanol/Water partition
    logd_74: float                     # Distribution coefficient at pH 7.4
    tpsa_angstrom2: float              # Topological Polar Surface Area (Å^2)
    rotatable_bonds: int               # Number of rotatable bonds
    globularity: float                 # 3D Globularity / Sphericity (0.0 to 1.0)
    has_primary_amine: bool            # Contains sterically accessible primary -NH2
    amine_pka: Optional[float] = None  # pKa of primary amine (if present)
    net_charge_74: float = 0.0         # Formal net electrical charge at pH 7.4
    dipole_moment_debye: float = 0.0   # Molecular dipole moment
    aromatic_rings: int = 0            # Number of aromatic ring systems
    is_macrolide_or_bulky_lipid: bool = False # High-affinity proximal pocket substrate
    stokes_radius_nm: Optional[float] = None # Hydrodynamic radius (Stokes-Einstein)
    minor_dimension_nm: Optional[float] = None # Smallest geometric dimension (nm)

    def compute_stokes_radius(self) -> float:
        """Estimate hydrodynamic Stokes radius (nm) from MW if not provided."""
        if self.stokes_radius_nm is not None:
            return self.stokes_radius_nm
        # Empirical relationship for small molecules (Edward 1970, Nikaido 2003):
        return 0.066 * (self.mw_da ** (1.0 / 3.0))

    def compute_minor_dimension(self) -> float:
        """Estimate smallest cross-sectional dimension from globularity and radius."""
        if self.minor_dimension_nm is not None:
            return self.minor_dimension_nm
        r_s = self.compute_stokes_radius()
        # Flat/planar molecules (low globularity) have narrow minor cross-section
        return 2.0 * r_s * math.sqrt(max(0.04, min(1.0, self.globularity)))

    def primary_amine_ionization_fraction(self, ph: float = 7.4) -> float:
        """Fraction of primary amine protonated to -NH3+ at given pH."""
        if not self.has_primary_amine:
            return 0.0
        pka = self.amine_pka if self.amine_pka is not None else 9.5
        return 1.0 / (1.0 + 10.0 ** (ph - pka))


# ============================================================================
# 3. ASYMMETRIC LPS OUTER MEMBRANE BILAYER MODEL
# ============================================================================

class LPSBilayerModel:
    """
    Biophysical model of the Gram-negative asymmetric outer membrane.
    Outer leaflet: Lipopolysaccharide (Lipid A with 6 saturated acyl chains + core).
    Inner leaflet: Phosphatidylethanolamine (PE) / Phosphatidylglycerol (PG).
    
    Established Ground Truth:
    The outer membrane has ~100-fold lower lipid bilayer fluidity than standard
    eukaryotic/fluid phospholipid bilayers due to divalent cation-bridged (Mg2+, Ca2+)
    lipid A phosphate groups.
    """

    def __init__(
        self,
        divalent_cation_concentration_mM: float = 2.0,  # Physiological [Mg2+ + Ca2+]
        lipid_bilayer_thickness_nm: float = 3.5,        # Hydrophobic core ~ 3.5 nm
        fluidity_reduction_factor: float = 100.0,      # ~100x lower lateral mobility
        standard_fluid_d_lateral_cm2_s: float = 1.0e-8  # Typical fluid bilayer lateral diffusion
    ):
        self.divalent_cation_mM = divalent_cation_concentration_mM
        self.thickness_nm = lipid_bilayer_thickness_nm
        self.thickness_cm = lipid_bilayer_thickness_nm * 1.0e-7
        self.fluidity_reduction_factor = fluidity_reduction_factor
        self.d_lateral_pl = standard_fluid_d_lateral_cm2_s

    @property
    def lps_lateral_diffusion_cm2_s(self) -> float:
        """
        Effective lateral diffusion coefficient in LPS outer leaflet.
        Saturated acyl chains cross-bridged by divalent cations form a quasi-crystalline gel.
        D_LPS ~ 10^-10 cm^2/s vs 10^-8 cm^2/s in fluid phospholipid bilayers (Nikaido 2003).
        """
        cation_effect = min(1.0, self.divalent_cation_mM / 1.5)
        effective_reduction = self.fluidity_reduction_factor * cation_effect
        return self.d_lateral_pl / max(1.0, effective_reduction)

    def calculate_passive_lipid_permeability(self, compound: CompoundProfile) -> float:
        """
        Passive trans-bilayer permeation coefficient P_lipid (cm/s).
        P_lipid = (K_ow * D_bilayer) / d_bilayer * alpha_LPS * f_size(MW)
        alpha_LPS reflects the ordered crystalline packing of Lipid A (~0.01).
        f_size(MW) captures steep molecular volume sieving through the gel phase (Lieb & Stein 1969).
        """
        kow = 10.0 ** compound.logd_74
        d_mem = self.lps_lateral_diffusion_cm2_s * 0.1 # trans-bilayer hopping rate
        
        # Cation bridging stabilizes headgroups, attenuating permeability
        alpha_lps = 0.01 * (1.0 / (1.0 + (self.divalent_cation_mM / 2.0)))

        # Molecular weight / volume sieving in ordered gel acyl lattice:
        # Permeability drops exponentially for bulky molecules above MW 250
        size_attenuation = math.exp(-0.0055 * max(0.0, compound.mw_da - 250.0))

        p_lipid = (kow * d_mem / self.thickness_cm) * alpha_lps * size_attenuation
        # Physiological bounds for intact bacterial OM lipid pathway: 10^-12 to 10^-5 cm/s
        return float(np.clip(p_lipid, 1.0e-12, 5.0e-5))


# ============================================================================
# 4. PORIN CHANNEL EXCLUSION & TRANSLOCATION MODELS
# ============================================================================

class PorinType(Enum):
    OMPF = "OmpF"   # E. coli general porin (trimer, ~7x11 Å constriction)
    OMPC = "OmpC"   # E. coli osmoregulated porin (trimer, ~5.5x10 Å constriction)
    OPRF = "OprF"   # P. aeruginosa major OM protein (mostly closed, ~2-5% open)
    OPRD = "OprD"   # P. aeruginosa specific carbapenem/basic amino acid channel


@dataclass
class PorinSpecification:
    """Biophysical and crystallographic parameters of a porin channel."""
    porin_type: PorinType
    constriction_major_axis_nm: float # Major axis at eyelet
    constriction_minor_axis_nm: float # Minor axis at eyelet
    channel_length_nm: float          # Channel thickness through OM (~5 nm)
    constriction_length_nm: float     # Narrow constriction length (~0.6 nm)
    monomer_count: int                # Monomers per complex (trimer = 3)
    transverse_efield_V_per_m: float  # Transverse electrostatic field in eyelet
    net_constriction_charge: float    # Effective charge of constriction loop L3
    channels_per_cell: int            # Typical wild-type copy number per cell
    is_specific_channel: bool = False # Substrate-specific binding
    open_probability: float = 1.0     # Fraction of channels in open permeable state

    @property
    def constriction_area_nm2(self) -> float:
        """Elliptical constriction area: pi * a * b (nm^2)."""
        a = self.constriction_major_axis_nm / 2.0
        b = self.constriction_minor_axis_nm / 2.0
        return math.pi * a * b

    @property
    def effective_radius_nm(self) -> float:
        """Equivalent circular radius from constriction area (nm)."""
        return math.sqrt(self.constriction_area_nm2 / math.pi)


# Crystallographically anchored models (Cowan et al. 1992, Nikaido 2003, Eren et al. 2012)
OMPF_SPEC = PorinSpecification(
    porin_type=PorinType.OMPF,
    constriction_major_axis_nm=1.1,   # 11 Å
    constriction_minor_axis_nm=0.7,   # 7 Å
    channel_length_nm=5.0,
    constriction_length_nm=0.6,
    monomer_count=3,
    transverse_efield_V_per_m=1.2e8,  # Intense ~10^8 V/m dipole across eyelet
    net_constriction_charge=-1.0,     # Slightly anionic eyelet
    channels_per_cell=100_000,
    open_probability=1.0
)

OMPC_SPEC = PorinSpecification(
    porin_type=PorinType.OMPC,
    constriction_major_axis_nm=1.0,   # 10 Å
    constriction_minor_axis_nm=0.55,  # 5.5 Å
    channel_length_nm=5.0,
    constriction_length_nm=0.6,
    monomer_count=3,
    transverse_efield_V_per_m=1.5e8,
    net_constriction_charge=-3.0,     # More negatively charged than OmpF
    channels_per_cell=100_000,
    open_probability=1.0
)

OPRF_SPEC = PorinSpecification(
    porin_type=PorinType.OPRF,
    constriction_major_axis_nm=1.5,
    constriction_minor_axis_nm=1.2,
    channel_length_nm=5.0,
    constriction_length_nm=0.7,
    monomer_count=1,
    transverse_efield_V_per_m=0.3e8,
    net_constriction_charge=-0.5,
    channels_per_cell=200_000,
    open_probability=0.03             # Only ~2-5% in open state (Sugawara & Nikaido 1994)
)

OPRD_SPEC = PorinSpecification(
    porin_type=PorinType.OPRD,
    constriction_major_axis_nm=0.8,
    constriction_minor_axis_nm=0.6,
    channel_length_nm=5.0,
    constriction_length_nm=0.8,
    monomer_count=1,
    transverse_efield_V_per_m=0.8e8,
    net_constriction_charge=-2.0,     # Specific basic pocket
    channels_per_cell=5_000,
    is_specific_channel=True,
    open_probability=1.0
)


class PorinPermeationModel:
    """
    Hydrodynamic & electrostatic porin translocation model.
    Calibrated against Nikaido (1994, 2003, 2009) empirical whole-cell permeabilities.
    Includes:
    1. Renkin steric hindrance function H(lambda).
    2. Elliptical slit-pore orientation for low-globularity molecules (G <= 0.25).
    3. Transverse electrostatic field attraction/repulsion.
    4. Whole-cell empirical calibration factor accounting for intact LPS brush accessibility.
    """

    WHOLE_CELL_ACCESSIBILITY_FACTOR = 1.8e-4

    def __init__(self, porin_spec: PorinSpecification):
        self.spec = porin_spec

    @staticmethod
    def renkin_hindrance(r_solute: float, r_pore: float) -> float:
        """
        Renkin hydrodynamic hindrance factor H(lambda).
        lambda = r_solute / r_pore.
        For lambda >= 1.0, steric exclusion prevents passage (H = 0).
        H(lambda) = (1 - lambda)^2 * (1 - 2.104*lambda + 2.09*lambda^3 - 0.95*lambda^5).
        """
        if r_solute >= r_pore:
            return 0.0
        lam = r_solute / r_pore
        phi_steric = (1.0 - lam) ** 2
        f_hydrodynamic = 1.0 - 2.104 * lam + 2.09 * (lam ** 3) - 0.95 * (lam ** 5)
        return max(0.0, phi_steric * f_hydrodynamic)

    def calculate_effective_hindrance(self, compound: CompoundProfile) -> float:
        """
        Computes hindrance taking into account molecular globularity and pore shape.
        Low globularity molecules (G <= 0.25) can align their minor axis through the slit pore,
        dramatically reducing steric exclusion compared to spherical equivalents.
        """
        r_spherical = compound.compute_stokes_radius()
        r_minor = compound.compute_minor_dimension() / 2.0
        r_eff_pore = self.spec.effective_radius_nm

        if compound.globularity <= 0.25:
            # Low globularity: Solute aligns minor dimension with the elliptical constriction
            r_effective_solute = 0.65 * r_minor + 0.35 * r_spherical
        else:
            # High globularity: Solute tumbles isotropically; full spherical radius is hindered
            r_effective_solute = r_spherical

        return self.renkin_hindrance(r_effective_solute, r_eff_pore)

    def calculate_electrostatic_factor(self, compound: CompoundProfile) -> float:
        """
        Electrostatic field interaction factor: exp(-Delta G_elec / (k_B * T)).
        In OmpF/OmpC, the constriction eyelet has a strong transverse field (Arg cluster vs Asp/Glu).
        - Positively charged primary amines (-NH3+) experience favorable attraction into the anionic field.
        - Zwitterions with dipole aligned along molecular axis experience dipole-field stabilization.
        - Anionic compounds experience repulsive free energy barriers.
        """
        kt = BOLTZMANN_K * TEMP_PHYSIOL_K

        # Net charge interaction with eyelet
        delta_g_charge = (compound.net_charge_74 * self.spec.net_constriction_charge) * (kt * 0.7)

        # Primary amine specific hydrogen-bonding / ionic lock with Asp113/Glu117 in loop L3:
        amine_bonus_j = 0.0
        if compound.has_primary_amine:
            ionization = compound.primary_amine_ionization_fraction()
            # Favorable energetic stabilization ~ 2.5 k_B*T (~ 6.4 kJ/mol)
            amine_bonus_j = -2.5 * kt * ionization

        # Dipole moment alignment in transverse field (E ~ 1.2e8 V/m)
        dipole_cm = compound.dipole_moment_debye * 3.33564e-30
        delta_g_dipole = -0.5 * dipole_cm * self.spec.transverse_efield_V_per_m

        total_delta_g = delta_g_charge + amine_bonus_j + delta_g_dipole
        exponent = -total_delta_g / kt
        return float(np.clip(math.exp(max(-5.0, min(5.0, exponent))), 0.05, 15.0))

    def calculate_single_channel_permeability_cm3_s(self, compound: CompoundProfile) -> float:
        """
        Single porin channel permeability p_single (cm^3 / s).
        Diffusion in water: D_aq = k_B * T / (6 * pi * eta * r_solute).
        Incorporates steric hindrance, electrostatics, and access/pore resistances.
        """
        r_s_nm = compound.compute_stokes_radius()
        r_s_m = r_s_nm * 1.0e-9

        d_aq = (BOLTZMANN_K * TEMP_PHYSIOL_K) / (6.0 * math.pi * VISCOSITY_WATER_37C * r_s_m)
        d_aq_cm2_s = d_aq * 1.0e4 # cm^2 / s

        h_steric = self.calculate_effective_hindrance(compound)
        if h_steric <= 1.0e-12:
            return 0.0

        f_elec = self.calculate_electrostatic_factor(compound)

        r_eff_cm = (self.spec.effective_radius_nm) * 1.0e-7
        a_c_cm2 = (self.spec.constriction_area_nm2) * 1.0e-14
        l_c_cm = (self.spec.constriction_length_nm) * 1.0e-7

        # Total resistance: channel constriction + access resistance
        r_total = (l_c_cm / a_c_cm2) + (1.0 / (2.0 * r_eff_cm))
        single_pore_perm = (d_aq_cm2_s / r_total) * h_steric * f_elec

        # Account for oligomer stoichiometry, open probability, and LPS accessibility
        effective_single_perm = (
            single_pore_perm *
            self.spec.monomer_count *
            self.spec.open_probability *
            self.WHOLE_CELL_ACCESSIBILITY_FACTOR
        )
        return float(effective_single_perm)

    def calculate_whole_cell_porin_permeability_cm_s(
        self, compound: CompoundProfile, morphology: BacterialMorphology
    ) -> float:
        """
        Porin contribution to outer membrane permeability P_porin (cm/s).
        P_porin = (N_channels * p_single) / A_cell
        """
        p_single = self.calculate_single_channel_permeability_cm3_s(compound)
        total_p_cm3_s = self.spec.channels_per_cell * p_single
        p_porin_cm_s = total_p_cm3_s / morphology.surface_area_cm2
        return float(p_porin_cm_s)


# ============================================================================
# 5. THE 'eNTRy' RULES FORMAL ENGINE (RICHTER ET AL. 2017 NATURE)
# ============================================================================

@dataclass
class ENTRyEvaluationResult:
    """Detailed diagnostic results for eNTRy rules compliance."""
    compound_name: str
    has_primary_amine: bool
    amine_passed: bool
    globularity: float
    globularity_passed: bool           # G <= 0.25
    rotatable_bonds: int
    rotatable_bonds_passed: bool       # N_rot <= 5
    mw_da: float
    mw_passed: bool                    # MW < 600 Da
    clogp: float
    lipophilicity_passed: bool         # -3.0 <= clogP <= 1.0
    tpsa_angstrom2: float
    tpsa_passed: bool                  # 75 <= TPSA <= 160 Å^2
    all_entry_rules_passed: bool       # Binary eNTRy pass
    entry_score: float                 # Continuous adherence index (0 - 100)
    predicted_accumulation_category: str # "High", "Moderate", "Low"
    predicted_accumulation_nmol_per_10e12_cells: float # Quantitative accumulation


class ENTRyRulesEngine:
    """
    Formal implementation of the eNTRy rules established by Richter et al. (Nature 2017).
    Guidelines:
    - N: Primary amine (sterically unhindered, ionizable to -NH3+).
    - T: Low 3D globularity (G <= 0.25, flat/elongated shape matching slit eyelet).
    - R: Low flexibility (rotatable bonds <= 5, minimizing entropic penalty).
    - y: Molecular weight < 600 Da (optimally < 500 Da) with balanced polarity.
    """

    GLOBULARITY_THRESHOLD = 0.25
    ROTATABLE_BONDS_MAX = 5
    MW_MAX_DA = 600.0
    CLOGP_MIN = -3.0
    CLOGP_MAX = 1.0
    TPSA_MIN = 75.0
    TPSA_MAX = 160.0

    @classmethod
    def evaluate(cls, compound: CompoundProfile) -> ENTRyEvaluationResult:
        """Evaluate a compound against the eNTRy rules and predict accumulation."""
        # 1. Primary Amine criterion
        amine_passed = compound.has_primary_amine and (
            compound.primary_amine_ionization_fraction() >= 0.5
        )

        # 2. Globularity criterion
        globularity_passed = compound.globularity <= cls.GLOBULARITY_THRESHOLD

        # 3. Flexibility (rotatable bonds) criterion
        rotatable_bonds_passed = compound.rotatable_bonds <= cls.ROTATABLE_BONDS_MAX

        # 4. Molecular weight criterion
        mw_passed = compound.mw_da < cls.MW_MAX_DA

        # 5. Lipophilicity criterion
        lipophilicity_passed = cls.CLOGP_MIN <= compound.clogp <= cls.CLOGP_MAX

        # 6. TPSA criterion
        tpsa_passed = cls.TPSA_MIN <= compound.tpsa_angstrom2 <= cls.TPSA_MAX

        # Core binary eNTRy rule pass: primary amine + globularity + MW + rotatable bonds
        all_passed = (
            amine_passed and
            globularity_passed and
            rotatable_bonds_passed and
            mw_passed
        )

        # Continuous scoring index (0 to 100)
        score = 0.0
        # Richter et al. showed primary amine carries decisive weight (~40 pts)
        if amine_passed:
            score += 40.0
        elif compound.has_primary_amine:
            score += 20.0
        
        # Globularity weight (25 pts)
        if compound.globularity <= cls.GLOBULARITY_THRESHOLD:
            score += 25.0
        else:
            excess_g = max(0.0, compound.globularity - cls.GLOBULARITY_THRESHOLD)
            score += max(0.0, 25.0 - (excess_g / 0.75) * 25.0)

        # Rotatable bonds weight (15 pts)
        if compound.rotatable_bonds <= cls.ROTATABLE_BONDS_MAX:
            score += 15.0
        else:
            excess_rot = compound.rotatable_bonds - cls.ROTATABLE_BONDS_MAX
            score += max(0.0, 15.0 - excess_rot * 2.5)

        # MW weight (10 pts)
        if compound.mw_da <= 450.0:
            score += 10.0
        elif compound.mw_da < cls.MW_MAX_DA:
            score += 10.0 * (1.0 - (compound.mw_da - 450.0) / 150.0)

        # Polarity / Lipophilicity balance (10 pts)
        if lipophilicity_passed and tpsa_passed:
            score += 10.0
        elif lipophilicity_passed or tpsa_passed:
            score += 5.0

        # Quantitative accumulation prediction (nmol / 10^12 cells)
        # Ground truth calibration from Richter et al. 2017:
        # eNTRy-compliant compounds typically accumulate at > 50 - 200 nmol / 10^12 cells.
        # Non-compliant compounds accumulate at < 10 nmol / 10^12 cells.
        if score >= 75.0:
            category = "High"
            pred_acc = 50.0 + (score - 75.0) * 6.0
        elif score >= 50.0:
            category = "Moderate"
            pred_acc = 10.0 + (score - 50.0) * 1.5
        else:
            category = "Low"
            pred_acc = max(0.2, score * 0.2)

        return ENTRyEvaluationResult(
            compound_name=compound.name,
            has_primary_amine=compound.has_primary_amine,
            amine_passed=amine_passed,
            globularity=compound.globularity,
            globularity_passed=globularity_passed,
            rotatable_bonds=compound.rotatable_bonds,
            rotatable_bonds_passed=rotatable_bonds_passed,
            mw_da=compound.mw_da,
            mw_passed=mw_passed,
            clogp=compound.clogp,
            lipophilicity_passed=lipophilicity_passed,
            tpsa_angstrom2=compound.tpsa_angstrom2,
            tpsa_passed=tpsa_passed,
            all_entry_rules_passed=all_passed,
            entry_score=round(score, 2),
            predicted_accumulation_category=category,
            predicted_accumulation_nmol_per_10e12_cells=round(pred_acc, 2)
        )


# ============================================================================
# 6. TRIPARTITE RND EFFLUX PUMPS (AcrAB-TolC, MexAB-OprM)
# ============================================================================

class EffluxPumpType(Enum):
    ACRAB_TOLC = "AcrAB-TolC" # Major E. coli multi-drug efflux pump
    MEXAB_OPRM = "MexAB-OprM" # Major P. aeruginosa multi-drug efflux pump


@dataclass
class RNDPumpSpecification:
    """Biophysical and kinetic architecture of RND family tripartite efflux pump."""
    pump_type: EffluxPumpType
    pumps_per_cell: int                 # Copy number (WT: ~400; MDR overexpressor: ~2500)
    k_cat_s_minus_1: float              # Turnover catalytic rate per complex (~20 - 50 s^-1)
    stoichiometry_protons_per_mol: int  # 2 H+ imported per drug exported
    proton_motive_force_mV: float       # PMF in mV (-180 mV to -200 mV)
    hill_coefficient: float = 1.0       # Cooperativity (Nagano & Nikaido 2009)

    @property
    def free_energy_per_mole_j(self) -> float:
        """Thermodynamic driving free energy from proton motive force: n * F * |PMF|."""
        pmf_volts = abs(self.proton_motive_force_mV) * 1.0e-3
        return self.stoichiometry_protons_per_mol * FARADAY_F * pmf_volts


ACRAB_TOLC_WT = RNDPumpSpecification(
    pump_type=EffluxPumpType.ACRAB_TOLC,
    pumps_per_cell=400,                 # Wild-type E. coli (Nagano & Nikaido 2009)
    k_cat_s_minus_1=30.0,               # ~30 molecules exported per second per pump
    stoichiometry_protons_per_mol=2,
    proton_motive_force_mV=-180.0,
    hill_coefficient=1.0
)

ACRAB_TOLC_OVEREXPRESSOR = RNDPumpSpecification(
    pump_type=EffluxPumpType.ACRAB_TOLC,
    pumps_per_cell=2500,                # MDR overexpressing strain
    k_cat_s_minus_1=30.0,
    stoichiometry_protons_per_mol=2,
    proton_motive_force_mV=-180.0,
    hill_coefficient=1.0
)

MEXAB_OPRM_WT = RNDPumpSpecification(
    pump_type=EffluxPumpType.MEXAB_OPRM,
    pumps_per_cell=600,                 # P. aeruginosa wild-type
    k_cat_s_minus_1=25.0,
    stoichiometry_protons_per_mol=2,
    proton_motive_force_mV=-190.0,
    hill_coefficient=1.0
)


class RNDEffluxModel:
    """
    Kinetics and dual-pocket substrate recognition modeling for AcrAB-TolC and MexAB-OprM.
    Dual Pocket Architecture (Nakashima et al. 2011 Nature):
    1. Proximal (Access) Pocket: binds high-MW macrolides (erythromycin), rifamycins.
    2. Distal (Deep) Pocket: Phe cluster (Phe178, Phe615, Phe628) binds aromatic planar substrates.
    Hydrophilic zwitterions (ampicillin, aminoglycosides) evade both pockets.
    """

    def __init__(self, spec: RNDPumpSpecification):
        self.spec = spec

    def predict_km_uM(self, compound: CompoundProfile) -> float:
        """
        Estimate substrate Michaelis constant K_m (uM).
        Calibrated against Nagano & Nikaido (2009 PNAS) and Nakashima et al. (2011 Nature):
        - Macrolides / bulky lipophiles (erythromycin, novobiocin): Km ~ 10 - 25 uM
        - High-affinity aromatic planar substrates (chloramphenicol, nitrocefin): Km ~ 5 - 20 uM
        - Moderate substrates (fluoroquinolones): Km ~ 15 - 50 uM
        - Poor/evading hydrophilic substrates (ampicillin): Km > 200 - 800 uM
        """
        # Case 1: Bulky lipophile / macrolide binding to Proximal Pocket
        if compound.is_macrolide_or_bulky_lipid or (compound.mw_da > 600.0 and compound.clogp > 1.5):
            # High affinity in proximal access pocket
            base_km = 12.0
            if compound.clogp > 2.0:
                base_km *= 0.8
            return float(np.clip(base_km, 2.0, 100.0))

        # Case 2: Distal pocket binding (governed by aromatic packing, lipophilicity, charge)
        base_log_km = 1.2 # ~16 uM baseline

        # Lipophilicity effect: higher clogP enhances hydrophobic contact with Phe cage
        if compound.clogp < 0.0:
            base_log_km += 0.5 * abs(compound.clogp)
        else:
            base_log_km -= 0.3 * min(2.0, compound.clogp)

        # Aromatic ring effect: aromatic pi-pi stacking with Phe178, Phe615, Phe628
        if compound.aromatic_rings >= 2:
            base_log_km -= 0.4
        elif compound.aromatic_rings == 0:
            base_log_km += 0.8 # evasion if non-aromatic and not a recognized macrolide

        # High polarity / TPSA penalty: desolvation cost in hydrophobic pocket
        if compound.tpsa_angstrom2 > 130.0:
            base_log_km += 0.4 * ((compound.tpsa_angstrom2 - 130.0) / 40.0)

        # Net negative charge penalty: AcrB distal pocket has negative electrostatic potential
        if compound.net_charge_74 < -0.5:
            base_log_km += 0.7 * abs(compound.net_charge_74)

        km_uM = 10.0 ** base_log_km
        return float(np.clip(km_uM, 1.0, 2500.0))

    def calculate_vmax_moles_per_cell_s(self) -> float:
        """Maximum active efflux rate per single cell (moles / cell / s)."""
        molecules_per_s = self.spec.pumps_per_cell * self.spec.k_cat_s_minus_1
        return molecules_per_s / AVOGADRO_N

    def calculate_vmax_uM_per_s_in_periplasm(self, morphology: BacterialMorphology) -> float:
        """Maximum active efflux rate expressed as concentration change in periplasm (uM / s)."""
        vmax_moles = self.calculate_vmax_moles_per_cell_s()
        v_peri_l = morphology.periplasmic_volume_liters
        conc_molar_per_s = vmax_moles / v_peri_l
        return conc_molar_per_s * 1.0e6 # uM / s

    def compute_efflux_rate_uM_per_s(
        self, periplasmic_conc_uM: float, km_uM: float, morphology: BacterialMorphology
    ) -> float:
        """Michaelis-Menten / Hill active efflux velocity in periplasmic space (uM / s)."""
        if periplasmic_conc_uM <= 0.0:
            return 0.0
        vmax_uM_s = self.calculate_vmax_uM_per_s_in_periplasm(morphology)
        n = self.spec.hill_coefficient
        cp_n = periplasmic_conc_uM ** n
        km_n = km_uM ** n
        return float(vmax_uM_s * cp_n / (km_n + cp_n))


# ============================================================================
# 7. COUPLED PERMEATION & INTRACELLULAR ACCUMULATION DYNAMICS
# ============================================================================

@dataclass
class AccumulationKineticReport:
    """Comprehensive accumulation output for an antibiotic under dynamic/steady state."""
    compound_name: str
    species: str
    external_conc_uM: float
    total_outer_membrane_perm_cm_s: float
    porin_perm_cm_s: float
    passive_lipid_perm_cm_s: float
    efflux_km_uM: float
    efflux_vmax_uM_s: float
    critical_saturation_threshold_uM: float # C_out where influx matches active V_max
    steady_state_periplasmic_uM: float
    steady_state_accumulation_ratio: float  # C_peri / C_out
    regime: str                             # "Efflux-Dominated", "Transition", or "Influx-Saturated"
    predicted_mic_fold_shift_vs_null_efflux: float # MIC(WT) / MIC(delta-efflux)
    synergy_factor: float                   # Synergy between low OM permeability and active efflux


class IntracellularAccumulationEngine:
    """
    Two-compartment dynamic ODE integrator and analytical steady-state solver.
    Solves the dynamic influx-efflux balance:
    dC_peri/dt = k_in * (C_out - C_peri) - [V_max * C_peri / (K_m + C_peri)]
    """

    def __init__(
        self,
        morphology: BacterialMorphology = E_COLI_MORPHOLOGY,
        lps_model: Optional[LPSBilayerModel] = None,
        porin_models: Optional[List[PorinPermeationModel]] = None,
        efflux_model: Optional[RNDEffluxModel] = None
    ):
        self.morphology = morphology
        self.lps_model = lps_model or LPSBilayerModel()
        
        # Default porin repertoire
        if porin_models is None:
            if morphology.species_name == "Escherichia coli":
                self.porin_models = [
                    PorinPermeationModel(OMPF_SPEC),
                    PorinPermeationModel(OMPC_SPEC)
                ]
            elif morphology.species_name == "Pseudomonas aeruginosa":
                self.porin_models = [
                    PorinPermeationModel(OPRF_SPEC),
                    PorinPermeationModel(OPRD_SPEC)
                ]
            else:
                self.porin_models = [PorinPermeationModel(OMPF_SPEC)]
        else:
            self.porin_models = porin_models

        # Default efflux pump
        if efflux_model is None:
            if morphology.species_name == "Pseudomonas aeruginosa":
                self.efflux_model = RNDEffluxModel(MEXAB_OPRM_WT)
            else:
                self.efflux_model = RNDEffluxModel(ACRAB_TOLC_WT)
        else:
            self.efflux_model = efflux_model

    def calculate_total_om_permeability_cm_s(self, compound: CompoundProfile) -> Tuple[float, float, float]:
        """
        Total outer membrane permeability P_OM (cm/s).
        P_OM = P_lipid + sum(P_porin)
        Returns: (P_total, P_porins_sum, P_lipid)
        """
        p_lipid = self.lps_model.calculate_passive_lipid_permeability(compound)
        p_porins = sum(
            pm.calculate_whole_cell_porin_permeability_cm_s(compound, self.morphology)
            for pm in self.porin_models
        )
        p_total = p_lipid + p_porins
        return p_total, p_porins, p_lipid

    def calculate_influx_clearance_s_minus_1(self, p_om_cm_s: float) -> float:
        """
        Influx rate constant k_in (s^-1) into the periplasmic volume.
        k_in = (P_OM * A_cell) / V_peri
        dC_peri/dt |_influx = k_in * (C_out - C_peri)
        """
        a_cell_cm2 = self.morphology.surface_area_cm2
        v_peri_cm3 = self.morphology.periplasmic_volume_liters * 1.0e3 # 1 L = 1000 cm^3
        return (p_om_cm_s * a_cell_cm2) / v_peri_cm3

    def calculate_critical_accumulation_threshold_uM(
        self, compound: CompoundProfile
    ) -> float:
        """
        Calculates the external antibiotic concentration C_threshold (uM) where
        passive influx rate across the outer membrane matches the maximum achievable
        active efflux capacity V_max:
        J_in(C_threshold) = V_max
        k_in * C_threshold = V_max_peri
        C_threshold = V_max_peri / k_in
        Above this concentration, active efflux is completely saturated and cannot
        prevent runaway periplasmic drug accumulation.
        """
        p_om, _, _ = self.calculate_total_om_permeability_cm_s(compound)
        k_in = self.calculate_influx_clearance_s_minus_1(p_om)
        vmax_peri_uM_s = self.efflux_model.calculate_vmax_uM_per_s_in_periplasm(self.morphology)

        if k_in <= 1.0e-12:
            return float("inf")
        
        return vmax_peri_uM_s / k_in

    def solve_steady_state_periplasmic_uM(
        self, compound: CompoundProfile, c_out_uM: float
    ) -> float:
        """
        Analytical and exact quadratic solution for steady-state periplasmic concentration:
        k_in * (C_out - C_peri) = V_max * C_peri / (K_m + C_peri)
        Rearranging:
        C_peri^2 + ( (V_max / k_in) + K_m - C_out ) * C_peri - (K_m * C_out) = 0
        """
        if c_out_uM <= 0.0:
            return 0.0

        p_om, _, _ = self.calculate_total_om_permeability_cm_s(compound)
        k_in = self.calculate_influx_clearance_s_minus_1(p_om)
        vmax = self.efflux_model.calculate_vmax_uM_per_s_in_periplasm(self.morphology)
        km = self.efflux_model.predict_km_uM(compound)

        if k_in <= 1.0e-12:
            return 0.0

        # Quadratic coefficients: a*x^2 + b*x + c = 0
        a = 1.0
        b = (vmax / k_in) + km - c_out_uM
        c = - (km * c_out_uM)

        discriminant = b ** 2 - 4.0 * a * c
        if discriminant < 0.0:
            return 0.0
        
        c_peri = (-b + math.sqrt(discriminant)) / (2.0 * a)
        return float(max(0.0, min(c_out_uM, c_peri)))

    def simulate_dynamic_trajectory(
        self,
        compound: CompoundProfile,
        c_out_uM: float,
        time_span_s: float = 60.0,
        initial_c_peri_uM: float = 0.0
    ) -> Dict[str, np.ndarray]:
        """
        Solves full time-dependent ODE trajectory of periplasmic accumulation:
        dC_peri/dt = k_in * (C_out - C_peri) - [V_max * C_peri / (K_m + C_peri)]
        """
        p_om, _, _ = self.calculate_total_om_permeability_cm_s(compound)
        k_in = self.calculate_influx_clearance_s_minus_1(p_om)
        vmax = self.efflux_model.calculate_vmax_uM_per_s_in_periplasm(self.morphology)
        km = self.efflux_model.predict_km_uM(compound)

        def ode_func(t, y):
            cp = max(0.0, y[0])
            influx = k_in * (c_out_uM - cp)
            efflux = vmax * cp / (km + cp) if (km + cp) > 0 else 0.0
            return [influx - efflux]

        t_eval = np.linspace(0.0, time_span_s, 200)
        sol = solve_ivp(ode_func, [0.0, time_span_s], [initial_c_peri_uM], t_eval=t_eval, method="Radau")

        return {
            "time_s": sol.t,
            "c_peri_uM": np.clip(sol.y[0], 0.0, c_out_uM),
            "c_out_uM": np.full_like(sol.t, c_out_uM)
        }

    def evaluate_antibiotic_kinetic_profile(
        self, compound: CompoundProfile, c_out_uM: float = 10.0
    ) -> AccumulationKineticReport:
        """Generate comprehensive diagnostic kinetic and accumulation profile."""
        p_om, p_porins, p_lipid = self.calculate_total_om_permeability_cm_s(compound)
        k_in = self.calculate_influx_clearance_s_minus_1(p_om)
        vmax = self.efflux_model.calculate_vmax_uM_per_s_in_periplasm(self.morphology)
        km = self.efflux_model.predict_km_uM(compound)
        c_thresh = self.calculate_critical_accumulation_threshold_uM(compound)
        c_peri = self.solve_steady_state_periplasmic_uM(compound, c_out_uM)
        acc_ratio = c_peri / c_out_uM if c_out_uM > 0 else 0.0

        # Regime determination
        if c_out_uM < 0.3 * c_thresh:
            regime = "Efflux-Dominated (Strict Depletion)"
        elif c_out_uM > 1.5 * c_thresh:
            regime = "Influx-Saturated (Efflux Overwhelmed)"
        else:
            regime = "Transition (Active Competition)"

        # Synergistic MIC fold shift:
        # MIC_WT / MIC_delta_efflux ~= 1 + (V_max / (k_in * K_m))
        efflux_clearance_factor = (vmax / (k_in * km)) if (k_in * km) > 0 else 0.0
        predicted_fold_shift = 1.0 + efflux_clearance_factor

        # Synergy factor: Outer membrane permeability limitation multiplies active efflux power
        # Compares real OM barrier with a highly leaky barrier (k_leaky = 100 s^-1)
        k_leaky = 100.0
        fold_shift_leaky = 1.0 + (vmax / (k_leaky * km))
        synergy = predicted_fold_shift / max(1.0, fold_shift_leaky)

        return AccumulationKineticReport(
            compound_name=compound.name,
            species=self.morphology.species_name,
            external_conc_uM=c_out_uM,
            total_outer_membrane_perm_cm_s=p_om,
            porin_perm_cm_s=p_porins,
            passive_lipid_perm_cm_s=p_lipid,
            efflux_km_uM=km,
            efflux_vmax_uM_s=vmax,
            critical_saturation_threshold_uM=c_thresh,
            steady_state_periplasmic_uM=c_peri,
            steady_state_accumulation_ratio=acc_ratio,
            regime=regime,
            predicted_mic_fold_shift_vs_null_efflux=round(predicted_fold_shift, 2),
            synergy_factor=round(synergy, 2)
        )


# ============================================================================
# 8. BENCHMARK ANTIMICROBIAL LIBRARY (LITERATURE GROUND TRUTH)
# ============================================================================

BENCHMARK_ANTIBIOTICS: Dict[str, CompoundProfile] = {
    # 1. Ciprofloxacin (Fluoroquinolone: low globularity, zwitterion, passes OmpF/OmpC, modest AcrAB efflux)
    "Ciprofloxacin": CompoundProfile(
        name="Ciprofloxacin",
        mw_da=331.34,
        clogp=-0.5,
        logd_74=-0.8,
        tpsa_angstrom2=72.8,
        rotatable_bonds=3,
        globularity=0.18, # flat bicyclic quinolone + piperazine
        has_primary_amine=False, # secondary piperazinyl amine
        net_charge_74=0.0, # zwitterionic
        dipole_moment_debye=6.5,
        aromatic_rings=2
    ),

    # 2. Ampicillin (Aminopenicillin: primary alpha-amino group, zwitterionic, high porin entry, poor AcrB substrate)
    "Ampicillin": CompoundProfile(
        name="Ampicillin",
        mw_da=349.40,
        clogp=1.35,
        logd_74=-1.9,
        tpsa_angstrom2=113.8,
        rotatable_bonds=4,
        globularity=0.22,
        has_primary_amine=True,
        amine_pka=7.3,
        net_charge_74=0.0, # zwitterionic at pH 7.4
        dipole_moment_debye=4.2,
        aromatic_rings=1
    ),

    # 3. 6-Deoxynybomycin (DNM, Richter et al. 2017: Gram-positive only, no primary amine, fails to accumulate in E. coli)
    "6-Deoxynybomycin": CompoundProfile(
        name="6-Deoxynybomycin",
        mw_da=256.26,
        clogp=0.45,
        logd_74=0.45,
        tpsa_angstrom2=64.7,
        rotatable_bonds=1,
        globularity=0.12, # very planar
        has_primary_amine=False, # no amine!
        net_charge_74=0.0,
        dipole_moment_debye=3.0,
        aromatic_rings=3
    ),

    # 4. 6-DNM-Amine (Richter et al. 2017: primary amine installed; eNTRy compliant, accumulates >100 nmol/10^12 cells, active against MDR E. coli)
    "6-DNM-Amine": CompoundProfile(
        name="6-DNM-Amine",
        mw_da=371.40,
        clogp=-0.6,
        logd_74=-1.2,
        tpsa_angstrom2=90.7,
        rotatable_bonds=4,
        globularity=0.16, # retains planar geometry
        has_primary_amine=True, # essential amine added!
        amine_pka=9.4,
        net_charge_74=1.0, # cation at pH 7.4
        dipole_moment_debye=7.8,
        aromatic_rings=3
    ),

    # 5. Chloramphenicol (Moderately permeable, substrate of AcrAB-TolC)
    "Chloramphenicol": CompoundProfile(
        name="Chloramphenicol",
        mw_da=323.13,
        clogp=1.14,
        logd_74=1.14,
        tpsa_angstrom2=115.3,
        rotatable_bonds=5,
        globularity=0.24,
        has_primary_amine=False,
        net_charge_74=0.0,
        dipole_moment_debye=4.5,
        aromatic_rings=1
    ),

    # 6. Erythromycin (Macrolide: large, globular G > 0.35, MW > 700 Da, excluded by porins, avid AcrAB substrate in proximal pocket)
    "Erythromycin": CompoundProfile(
        name="Erythromycin",
        mw_da=733.93,
        clogp=2.54,
        logd_74=1.63,
        tpsa_angstrom2=193.9,
        rotatable_bonds=7,
        globularity=0.42, # highly globular macrolactone ring
        has_primary_amine=False, # tertiary amine in desosamine
        net_charge_74=1.0,
        dipole_moment_debye=3.8,
        aromatic_rings=0,
        is_macrolide_or_bulky_lipid=True
    ),

    # 7. Vancomycin (Glycopeptide: huge MW 1449, massive globularity, totally excluded by OM porins)
    "Vancomycin": CompoundProfile(
        name="Vancomycin",
        mw_da=1449.27,
        clogp=-3.1,
        logd_74=-3.5,
        tpsa_angstrom2=447.2,
        rotatable_bonds=11,
        globularity=0.58,
        has_primary_amine=True,
        amine_pka=7.8,
        net_charge_74=1.0,
        dipole_moment_debye=12.0,
        aromatic_rings=5
    ),

    # 8. Novobiocin (Aminocoumarin: MW 612 Da, excluded by porins, avid AcrAB substrate; 128x MIC drop in delta-AcrAB)
    "Novobiocin": CompoundProfile(
        name="Novobiocin",
        mw_da=612.62,
        clogp=2.85,
        logd_74=1.20,
        tpsa_angstrom2=174.5,
        rotatable_bonds=6,
        globularity=0.32,
        has_primary_amine=False,
        net_charge_74=-1.0,
        dipole_moment_debye=5.1,
        aromatic_rings=2,
        is_macrolide_or_bulky_lipid=True
    ),

    # 9. Meropenem (Carbapenem: low MW, zwitterionic, enters via OmpF/OmpC and OprD in P. aeruginosa)
    "Meropenem": CompoundProfile(
        name="Meropenem",
        mw_da=383.46,
        clogp=-0.9,
        logd_74=-2.3,
        tpsa_angstrom2=114.7,
        rotatable_bonds=5,
        globularity=0.21,
        has_primary_amine=False,
        net_charge_74=0.0,
        dipole_moment_debye=5.8,
        aromatic_rings=0
    )
}


# ============================================================================
# 9. CONVENIENCE HIGH-LEVEL RUNNER
# ============================================================================

def run_antimicrobial_permeability_analysis(
    compound_name: str,
    species: str = "Escherichia coli",
    external_conc_uM: float = 10.0
) -> Dict[str, Any]:
    """Execute complete biophysical analysis for a given compound and species."""
    if compound_name not in BENCHMARK_ANTIBIOTICS:
        raise ValueError(f"Unknown compound '{compound_name}'. Available: {list(BENCHMARK_ANTIBIOTICS.keys())}")
    
    compound = BENCHMARK_ANTIBIOTICS[compound_name]
    
    if species == "Escherichia coli":
        morphology = E_COLI_MORPHOLOGY
    elif species == "Pseudomonas aeruginosa":
        morphology = P_AERUGINOSA_MORPHOLOGY
    elif species == "Acinetobacter baumannii":
        morphology = A_BAUMANNII_MORPHOLOGY
    else:
        raise ValueError(f"Unsupported species '{species}'")

    engine = IntracellularAccumulationEngine(morphology=morphology)
    entry_eval = ENTRyRulesEngine.evaluate(compound)
    kinetic_report = engine.evaluate_antibiotic_kinetic_profile(compound, c_out_uM=external_conc_uM)

    return {
        "compound": compound,
        "entry_evaluation": entry_eval,
        "kinetic_report": kinetic_report
    }


if __name__ == "__main__":
    print("=" * 80)
    print("ANTIMICROBIAL PERMEABILITY & ACCUMULATION ENGINE (A002 Raman)")
    print("=" * 80)
    for name in ["6-DNM-Amine", "6-Deoxynybomycin", "Ciprofloxacin", "Ampicillin", "Erythromycin", "Vancomycin", "Novobiocin"]:
        res = run_antimicrobial_permeability_analysis(name, species="Escherichia coli", external_conc_uM=10.0)
        e = res["entry_evaluation"]
        k = res["kinetic_report"]
        print(f"\nCompound: {name} (MW={e.mw_da} Da, Globularity={e.globularity}, Primary Amine={e.has_primary_amine})")
        print(f"  eNTRy Score: {e.entry_score}/100 | Class: {e.predicted_accumulation_category} "
              f"({e.predicted_accumulation_nmol_per_10e12_cells} nmol/10^12 cells)")
        print(f"  P_OM: {k.total_outer_membrane_perm_cm_s:.3e} cm/s (Porin: {k.porin_perm_cm_s:.3e}, Lipid: {k.passive_lipid_perm_cm_s:.3e})")
        print(f"  Saturation Threshold (C_thresh): {k.critical_saturation_threshold_uM:.2f} uM")
        print(f"  Steady-state C_peri at 10 uM: {k.steady_state_periplasmic_uM:.3f} uM (Acc Ratio: {k.steady_state_accumulation_ratio:.3f})")
        print(f"  Regime: {k.regime}")
        print(f"  Predicted delta-Efflux MIC Shift: {k.predicted_mic_fold_shift_vs_null_efflux:.1f}x (Synergy: {k.synergy_factor:.1f}x)")
