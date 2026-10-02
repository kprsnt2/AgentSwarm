"""
hindu_multiverse_siddhantic_and_epistemic_synthesis_engine.py

Quantitative and Epistemic Engine for Siddhantic Astronomical Demarcation,
Puranic Multiverse Metrics, and Pan-Dharmic Cosmological Demarcation.

Author: Kepler (A001)
Domain: What do Hindu texts say about multiple universes (what-do-hindu-texts-say)
Epistemic Class: Historical / textual / astronomical
Standard of Evidence: Rigorous demarcation of Primary Text, Scholarly Consensus, Devotional Claim.
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import json


# Constants for Classical Indian Metrology and Modern Conversions
YOJANA_TO_KM_SIDDHANTA = 12.87  # Standard Siddhantic yojana (~8 miles / 12.87 km)
YOJANA_TO_KM_PURANA = 9.60      # Alternative classical Puranic yojana (~6 miles)
LIGHT_YEAR_KM = 9.460730472e12
AU_KM = 1.495978707e8

# Solar and Kalpa Time Scales (Surya Siddhanta & Siddhanta Siromani)
SOLAR_YEAR_DAYS = 365.258756481  # Siddhantic sidereal year (SS 1.34-39)
MAHAYUGA_YEARS = 4_320_000
KALPA_YEARS = 4_320_000_000      # 1,000 Mahayugas = 1 Day of Brahma
MAHAYUGA_CIVIL_DAYS = 1_577_917_828  # Surya Siddhanta 1.37
LUNAR_REVOLUTIONS_MAHAYUGA = 57_753_336  # Surya Siddhanta 1.30


@dataclass
class SiddhanticOrbitMetrics:
    """Mathematical derivation of planetary orbits and Brahmanda boundary in Surya Siddhanta."""
    body_name: str
    revolutions_per_mahayuga: float
    orbit_circumference_yojanas: float
    orbit_radius_yojanas: float
    orbit_radius_km: float
    orbit_radius_light_years: float


@dataclass
class PuranicSheathMetrics:
    """Metrics for the 7 concentric cosmic sheaths (Avaranas) enclosing the Brahmanda."""
    sheath_index: int
    name_sanskrit: str
    element_tattva: str
    thickness_factor: float
    radial_thickness_yojanas: float
    cumulative_radius_yojanas: float
    cumulative_radius_km: float
    cumulative_radius_light_years: float
    cumulative_volume_cubic_yojanas: float


@dataclass
class EpistemicStanceRecord:
    """Record defining an Indian school's epistemic stance on the multiverse."""
    school_name: str
    tradition: str
    primary_texts: List[str]
    representative_thinkers: List[str]
    epistemic_sources_accepted: List[str]  # Pramanas (Pratyaksha, Anumana, Sabda, etc.)
    multiverse_verdict: str  # AFFIRMED_PHYSICAL, AFFIRMED_MENTAL, AGNOSTIC_EMPIRICAL, STRICTLY_REJECTED, HARMONIZED_DUAL
    epistemic_class: str  # Primary Text / Scholarly Consensus / Devotional Claim
    core_thesis: str
    demarcation_analysis: str


class SiddhanticAndPuranicCosmologyEngine:
    """
    Engine implementing the mathematical, textual, and epistemic frameworks
    governing Hindu astronomical and Puranic multiverse models.
    """

    def __init__(self, yojana_km: float = YOJANA_TO_KM_SIDDHANTA):
        self.yojana_km = yojana_km

    def compute_siddhantic_kha_kaksha(self) -> Dict[str, Any]:
        """
        Derives the Brahmanda boundary (Kha-kaksha / Orbit of the Sky)
        according to the Surya Siddhanta (Chapter 12, vv. 80-90) and Siddhanta Siromani.
        
        Principle of Uniform Mean Motion (Sama-gati):
        All planets traverse equal linear distances in equal times.
        Hence, Orbit_Planetary = (Revolutions_Moon / Revolutions_Planet) * Orbit_Moon.
        
        The outer boundary of the Brahmanda (Kha-kaksha) is the orbit of a body
        completing exactly 1 revolution in a Kalpa (1,000 Mahayugas), or equivalently,
        the total linear distance traversed by any planet in a Kalpa.
        """
        # Base parameters from Surya Siddhanta 12.80-86
        moon_orbit_circumference = 324_000.0  # yojanas
        
        # Mean linear daily motion of any planet (yojanas/day)
        # In a Mahayuga, the Moon completes 57,753,336 revolutions
        total_distance_mahayuga = LUNAR_REVOLUTIONS_MAHAYUGA * moon_orbit_circumference
        mean_daily_motion_yojanas = total_distance_mahayuga / MAHAYUGA_CIVIL_DAYS
        
        # Total distance in a Kalpa (1,000 Mahayugas) = Circumference of Brahmanda (Kha-kaksha)
        kha_kaksha_circumference = total_distance_mahayuga * 1000.0
        
        # Exact radius of Brahmanda shell
        kha_kaksha_radius_yojanas = kha_kaksha_circumference / (2.0 * math.pi)
        kha_kaksha_radius_km = kha_kaksha_radius_yojanas * self.yojana_km
        kha_kaksha_radius_ly = kha_kaksha_radius_km / LIGHT_YEAR_KM
        
        # Planetary orbits derived from equal motion principle
        planetary_revs = {
            "Moon (Candra)": 57_753_336,
            "Mercury (Budha - sighra)": 17_937_060,
            "Venus (Sukra - sighra)": 7_022_376,
            "Sun (Surya)": 4_320_000,
            "Mars (Mangala)": 2_296_832,
            "Jupiter (Guru)": 364_220,
            "Saturn (Sani)": 146_568,
            "Asterisms (Naksatra-kaksha)": 60.0,
            "Brahmanda Boundary (Kha-kaksha)": 0.001  # 1 revolution in 1,000 Mahayugas (1 Kalpa)
        }
        
        orbits = []
        for name, revs in planetary_revs.items():
            circ = total_distance_mahayuga / revs if revs > 0.001 else kha_kaksha_circumference
            rad_yoj = circ / (2.0 * math.pi)
            rad_km = rad_yoj * self.yojana_km
            rad_ly = rad_km / LIGHT_YEAR_KM
            orbits.append(SiddhanticOrbitMetrics(
                body_name=name,
                revolutions_per_mahayuga=revs,
                orbit_circumference_yojanas=circ,
                orbit_radius_yojanas=rad_yoj,
                orbit_radius_km=rad_km,
                orbit_radius_light_years=rad_ly
            ))
            
        return {
            "moon_orbit_circumference_yojanas": moon_orbit_circumference,
            "mean_daily_motion_yojanas": mean_daily_motion_yojanas,
            "total_distance_mahayuga_yojanas": total_distance_mahayuga,
            "brahmanda_circumference_yojanas": kha_kaksha_circumference,
            "brahmanda_radius_yojanas": kha_kaksha_radius_yojanas,
            "brahmanda_radius_km": kha_kaksha_radius_km,
            "brahmanda_radius_light_years": kha_kaksha_radius_ly,
            "planetary_orbits": orbits
        }

    def compute_puranic_egg_and_sheath_metrics(self) -> Dict[str, Any]:
        """
        Computes the geometric and physical scale of the Puranic Brahmanda:
        - Inner Egg Core: Diameter = 500,000,000 yojanas (50 crore yojanas)
          (Bhagavata Purana 5.20.43, Vishnu Purana 2.7.22)
        - Seven Concentric Sheaths (Avaranas):
          Water, Fire, Air, Ether, Ahankara, Mahat, Pradhana.
          Each sheath is 10 times thicker than the preceding entity.
        """
        core_diameter_yojanas = 500_000_000.0  # 50 crore
        core_radius_yojanas = core_diameter_yojanas / 2.0
        core_radius_km = core_radius_yojanas * self.yojana_km
        core_radius_au = core_radius_km / AU_KM
        core_radius_ly = core_radius_km / LIGHT_YEAR_KM
        core_volume = (4.0 / 3.0) * math.pi * (core_radius_yojanas ** 3)

        sheath_names = [
            ("Ap (Water)", "Jala-tattva"),
            ("Tejas (Fire)", "Agni-tattva"),
            ("Vayu (Air)", "Vayu-tattva"),
            ("Akasa (Ether)", "Akasa-tattva"),
            ("Ahankara (Cosmic Ego)", "Ahankara-tattva"),
            ("Mahat (Cosmic Intellect)", "Buddhi/Mahat-tattva"),
            ("Pradhana (Unmanifest Prakriti)", "Avyakta-tattva")
        ]

        sheaths = []
        current_inner_radius = core_radius_yojanas
        cumulative_radius = core_radius_yojanas
        # Each sheath is 10 times thicker than preceding core / sheath
        # In Bhagavata Purana 3.11.40-41 and 2.5.35:
        # First sheath (water) thickness = 10 * core_diameter or 10 * previous entity
        thickness = core_diameter_yojanas * 10.0  # 5 * 10^9 yojanas

        for idx, (sanskrit_name, tattva) in enumerate(sheath_names, start=1):
            radial_thickness = thickness
            cumulative_radius += radial_thickness
            cum_km = cumulative_radius * self.yojana_km
            cum_ly = cum_km / LIGHT_YEAR_KM
            cum_vol = (4.0 / 3.0) * math.pi * (cumulative_radius ** 3)
            
            sheaths.append(PuranicSheathMetrics(
                sheath_index=idx,
                name_sanskrit=sanskrit_name,
                element_tattva=tattva,
                thickness_factor=10.0 ** idx,
                radial_thickness_yojanas=radial_thickness,
                cumulative_radius_yojanas=cumulative_radius,
                cumulative_radius_km=cum_km,
                cumulative_radius_light_years=cum_ly,
                cumulative_volume_cubic_yojanas=cum_vol
            ))
            # Next sheath is 10 times thicker than current
            thickness *= 10.0

        total_envelope_radius_yojanas = sheaths[-1].cumulative_radius_yojanas
        total_envelope_radius_km = sheaths[-1].cumulative_radius_km
        total_envelope_radius_ly = sheaths[-1].cumulative_radius_light_years
        total_envelope_volume = sheaths[-1].cumulative_volume_cubic_yojanas

        return {
            "core_diameter_yojanas": core_diameter_yojanas,
            "core_radius_yojanas": core_radius_yojanas,
            "core_radius_km": core_radius_km,
            "core_radius_au": core_radius_au,
            "core_radius_light_years": core_radius_ly,
            "core_volume_cubic_yojanas": core_volume,
            "sheaths": sheaths,
            "total_envelope_radius_yojanas": total_envelope_radius_yojanas,
            "total_envelope_radius_km": total_envelope_radius_km,
            "total_envelope_radius_light_years": total_envelope_radius_ly,
            "total_envelope_volume_cubic_yojanas": total_envelope_volume
        }

    def compare_siddhantic_and_puranic_scales(self) -> Dict[str, float]:
        """
        Computes the exact quantitative comparison between the Siddhantic
        astronomical boundary and the Puranic core and sheath envelopes.
        """
        siddhanta = self.compute_siddhantic_kha_kaksha()
        purana = self.compute_puranic_egg_and_sheath_metrics()

        r_sid_yoj = siddhanta["brahmanda_radius_yojanas"]
        r_pur_core_yoj = purana["core_radius_yojanas"]
        r_pur_env_yoj = purana["total_envelope_radius_yojanas"]

        radius_ratio_siddhanta_to_purana_core = r_sid_yoj / r_pur_core_yoj
        radius_ratio_purana_envelope_to_siddhanta = r_pur_env_yoj / r_sid_yoj
        
        vol_sid = (4.0 / 3.0) * math.pi * (r_sid_yoj ** 3)
        volume_ratio_siddhanta_to_purana_core = vol_sid / purana["core_volume_cubic_yojanas"]
        volume_ratio_purana_envelope_to_siddhanta = purana["total_envelope_volume_cubic_yojanas"] / vol_sid

        return {
            "siddhanta_radius_yojanas": r_sid_yoj,
            "purana_core_radius_yojanas": r_pur_core_yoj,
            "purana_envelope_radius_yojanas": r_pur_env_yoj,
            "radius_ratio_siddhanta_to_purana_core": radius_ratio_siddhanta_to_purana_core,
            "radius_ratio_purana_envelope_to_siddhanta": radius_ratio_purana_envelope_to_siddhanta,
            "volume_ratio_siddhanta_to_purana_core": volume_ratio_siddhanta_to_purana_core,
            "volume_ratio_purana_envelope_to_siddhanta": volume_ratio_purana_envelope_to_siddhanta
        }

    def build_pan_dharmic_epistemic_matrix(self) -> List[EpistemicStanceRecord]:
        """
        Builds the definitive 5-tradition Indian philosophical and astronomical
        epistemic taxonomy regarding multiple universes.
        """
        records = [
            EpistemicStanceRecord(
                school_name="Mathematical Astronomy (Jyotisa Siddhanta)",
                tradition="Siddhantic Jyotisa",
                primary_texts=[
                    "Aryabhatiya (Golapada 6-12)",
                    "Sisyadhivrddhida Tantra (Ch. 20 Mithyajnana-nirakarana)",
                    "Surya Siddhanta (Ch. 12.80-90)",
                    "Siddhanta Siromani (Bhuvanakosa 1-50, Vasanabhasya)"
                ],
                representative_thinkers=["Aryabhata", "Varahamihira", "Brahmagupta", "Lallacarya", "Bhaskara II", "Nilakantha Somayaji"],
                epistemic_sources_accepted=["Pratyaksa (Direct Observation)", "Anumana (Mathematical/Trigonometric Inference)"],
                multiverse_verdict="AGNOSTIC_EMPIRICAL",
                epistemic_class="Primary Text (Astronomical)",
                core_thesis="The Brahmanda is defined strictly by the operational limits of planetary motion and solar illumination (Kha-kaksha = 18.712e15 yojanas circumference). Multiple universes are unobservable and treated as theological allegory (arthavada). Flat-earth and Meru cosmography are mathematically disproven.",
                demarcation_analysis="Direct historical conflict with Puranas. Astronomers proved the Earth is an isolated sphere in empty space, calculating its circumference (~4,967 yojanas). They rejected physical parallel eggs because no observational deviation requires them."
            ),
            EpistemicStanceRecord(
                school_name="Puranic Realist Pluralism (Pauranika / Gaudiya / Vallabha)",
                tradition="Puranic Theism & Bhedabheda Vedānta",
                primary_texts=[
                    "Bhagavata Purana (2.5.35, 3.11.40-41, 6.16.37, 10.14.11)",
                    "Vishnu Purana (2.7.22-28)",
                    "Brahma Samhita (5.35, 5.40)",
                    "Tattva Sandarbha & Bhagavata Sandarbha of Jiva Gosvamin"
                ],
                representative_thinkers=["Veda Vyasa (trad.)", "Sridhara Svamin", "Jiva Gosvamin", "Sanatana Gosvamin", "Vallabhacarya"],
                epistemic_sources_accepted=["Sabda-Pramana (Scriptural Revelation as self-validating / svatah-pramana)"],
                multiverse_verdict="AFFIRMED_PHYSICAL",
                epistemic_class="Primary Text (Theological / Devotional)",
                core_thesis="Infinite universes (ananta-koti-brahmanda) exist objectively as isolated material bubbles nucleating continuously from the pores and exhalations of Maha-Visnu (Karanodakasayi Visnu) in the causal ocean. Each has 14 lokas, 7 sheaths, and a distinct Brahma.",
                demarcation_analysis="Cosmological pluralism is essential to demonstrating the limitless majesty (vibhati / aisvarya) of the Supreme Deity. Ontologically realist: universes are physically distinct external envelopes."
            ),
            EpistemicStanceRecord(
                school_name="Radical Phenomenological Idealism (Yoga-Vasistha / Advaita)",
                tradition="Monistic Idealism / Drsti-Srsti-Vada",
                primary_texts=[
                    "Yoga-Vasistha (Utpatti Prakarana 3.14, Nirvana Prakarana 6.2.82)",
                    "Mandukya Karika of Gaudapada (Vaitathya Prakarana)",
                    "Vedanta-Siddhanta-Muktavali of Prakasananda"
                ],
                representative_thinkers=["Vasistha (trad.)", "Gaudapada", "Prakasananda", "Madhusudana Sarasvati"],
                epistemic_sources_accepted=["Sabda (Scripture)", "Anumana (Logic)", "Aparoksanubhuti (Direct Non-dual Realization)"],
                multiverse_verdict="AFFIRMED_MENTAL",
                epistemic_class="Primary Text (Philosophical)",
                core_thesis="Universes are fractal subjective mental projections (citta-spanda). Infinite universes exist nested inside every atom, every rock, and every dream. Space and physical matter are cognitive illusions (maya); the multiverse is an epistemic manifold of consciousness.",
                demarcation_analysis="Rejects external objective multiverse realism. The multiverse is neither physical bubble nucleation nor parallel classical spaces, but infinite subjective reality-states coexisting without mutual physical interference."
            ),
            EpistemicStanceRecord(
                school_name="Purva Mimamsa Anti-Cosmogenic Steady-State",
                tradition="Orthodox Vedic Hermeneutics",
                primary_texts=[
                    "Mimamsa Sutras of Jaimini (1.1.1-5)",
                    "Sabara Bhasya",
                    "Slokavarttika of Kumarila Bhatta (Sambandhaksepa-parihara, vv. 40-115)",
                    "Tantravarttika"
                ],
                representative_thinkers=["Jaimini", "Sabara Svamin", "Kumarila Bhatta", "Prabhakara Misra"],
                epistemic_sources_accepted=["Pratyaksa", "Anumana", "Upamana", "Arthapatti", "Anupalabdhi", "Sabda"],
                multiverse_verdict="STRICTLY_REJECTED",
                epistemic_class="Primary Text (Orthodox Philosophy)",
                core_thesis="The physical universe was never created, will never be destroyed, and has no beginning or end ('na kadacid anidrsam jagat'). Rejects Mahapralaya (cosmic dissolution), Ishvara (creator God), and parallel Brahmandas as unprovable mythological fictions.",
                demarcation_analysis="Most rigorous orthodox Indian critique of multiverse cosmogony. Kumarila Bhatta proves that postulating a creator demiurge or multiple eggs leads to infinite regress (anavastha) and epistemic incoherence. Scripture consists of eternal injunctions (vidhi), not historical cosmologies."
            ),
            EpistemicStanceRecord(
                school_name="Commentarial Concordism / Dual-Sphere Reconciliation",
                tradition="Late Medieval Scholasticism",
                primary_texts=[
                    "Siddhanta Siromani Vasanabhasya (Bhaskara II)",
                    "Siddhanta Tattva-Viveka (Kamalakara Bhatta)",
                    "Siddhanta Darpana (Nilakantha Somayaji)",
                    "Yuktidipika"
                ],
                representative_thinkers=["Bhaskara II", "Kamalakara Bhatta", "Nilakantha Somayaji", "Vadiraja Tirtha"],
                epistemic_sources_accepted=["Samanvaya (Harmonization of Pratyaksa, Anumana, and Sabda)"],
                multiverse_verdict="HARMONIZED_DUAL",
                epistemic_class="Scholarly Consensus (Historical Commentarial)",
                core_thesis="Bifurcated reality: Siddhantic astronomy governs the physical terrestrial/planetary realm (adhibhautika/drsya), while Puranic Meru and multi-egg cosmography describe the subtle spiritual architecture (adhidaivika/adrsya) or laudatory metaphor (arthavada).",
                demarcation_analysis="Intellectual defense preserving both empirical science and sacred tradition. Bhaskara II explicitly states that Puranic statements are designed for meditation (upasana), not computational astronomy."
            )
        ]
        return records

    def build_concordism_demarcation_firewall(self) -> Dict[str, Any]:
        """
        Builds the Concordism Demarcation Firewall comparing modern theoretical
        physics multiverse models with ancient Hindu cosmologies, enforcing
        the protocol violations check.
        """
        comparisons = [
            {
                "modern_model": "Chaotic Inflation / Eternal Inflation (Linde, Guth, Vilenkin)",
                "hindu_concept": "Maha-Visnu Pore Bubble Nucleation (Bhagavata Purana 3.11, 2.5)",
                "superficial_similarity": "Bubbles continuously emerging from a vast background substrate (inflaton field vs Karanodaka causal ocean).",
                "ontological_difference": "Linde's model operates on quantum fluctuations of an inflaton scalar field driven by positive vacuum energy; Bhagavata operates on personal divine voluntary will (sankalpa) and karmic potential of unliberated jivas.",
                "mathematical_differential": "Modern: Scalar potential V(phi), slow-roll parameters epsilon, eta, tensor-to-scalar ratio r < 0.036. Hindu: Theological counts (koti-koti = 10^7, ananta = infinite), fixed yojana geometric expansions, moral causation.",
                "verifiability_status": "Modern: Potentially testable via cosmic microwave background (CMB) cold spot bubble collision signatures. Hindu: Untestable by empirical instruments; accepted via Sabda-pramana.",
                "protocol_verdict": "NON-EQUIVALENCE (Category Error if conflated; metaphorically resonant, physically distinct)."
            },
            {
                "modern_model": "Many-Worlds Interpretation of Quantum Mechanics (Everett III, DeWitt)",
                "hindu_concept": "Worlds Within Worlds / Mind-Worlds (Yoga-Vasistha, Nirvana Prakarana)",
                "superficial_similarity": "Infinite parallel realities co-existing simultaneously across orthogonal dimensions.",
                "ontological_difference": "Everett's branching occurs deterministically via unitary evolution of the universal wave function (|Psi>) in Hilbert space during decoherence; Yoga-Vasistha's worlds are subjective mental projections (citta-vrtti) in universal consciousness (Brahman/Cid-akasa).",
                "mathematical_differential": "Everett: Infinite-dimensional Hilbert space, projection operators, Born rule probability (P = |c_i|^2). Yoga-Vasistha: Radical idealism; matter is non-existent apart from perception (drsti-srsti).",
                "verifiability_status": "Modern: Debated in quantum foundations (decoherence experiments, quantum computing algorithms). Hindu: Experiential verification exclusively through samadhi and yogic meditation.",
                "protocol_verdict": "NON-EQUIVALENCE (Quantum linear superposition != Mental phenomenological idealism)."
            },
            {
                "modern_model": "String Theory Landscape & Calabi-Yau Compactification (Bousso-Polchinski, Susskind)",
                "hindu_concept": "36 Tattvas and 224 Bhuvanas (Saiva Siddhanta, Svacchanda Tantra)",
                "superficial_similarity": "Hierarchical multi-dimensional structure with hundreds of distinct ground states / worlds.",
                "ontological_difference": "String Landscape consists of ~10^500 flux vacua in 10/11 dimensions determined by geometry of compactified 6D Calabi-Yau manifolds; Tantric Bhuvanas are levels of conscious purity along the gradient from impure matter (asuddha) to pure Siva (suddha).",
                "mathematical_differential": "Modern: Topology, Hodge numbers (h^{1,1}, h^{2,1}), Euler characteristic, flux integrals. Tantra: Padadhvan, varnadhvan, tattvadhvan, karmic maturation levels.",
                "verifiability_status": "Modern: Particle physics LHC bounds, dark energy precision tests. Hindu: Esoteric ritual initiation (diksa) and internal Kundalini ascent.",
                "protocol_verdict": "NON-EQUIVALENCE (Mathematical flux compactification != Ontological hierarchy of divine energies)."
            }
        ]
        return {
            "firewall_rules": [
                "Rule 1: Prohibit retrofitting modern mathematical physics (tensors, Hilbert spaces, scalar fields) onto ancient Sanskrit poetic metaphors.",
                "Rule 2: Prohibit dismissing ancient cosmological models as primitive superstitions based on their lack of modern telescope data (avoid treating absence of evidence as proof of falsehood).",
                "Rule 3: Recognize that the Sanskrit texts formulated genuine, internally coherent concepts of spatial and temporal cosmic pluralism 1,500+ years before Western thought.",
                "Rule 4: Always cite whether a statement is a primary textual quote, an established scholarly Indological consensus, or a devotional apologetic claim."
            ],
            "demarcation_comparisons": comparisons
        }

    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """Runs all models and produces a consolidated master dictionary."""
        siddhanta = self.compute_siddhantic_kha_kaksha()
        purana = self.compute_puranic_egg_and_sheath_metrics()
        comparison = self.compare_siddhantic_and_puranic_scales()
        matrix = self.build_pan_dharmic_epistemic_matrix()
        firewall = self.build_concordism_demarcation_firewall()

        return {
            "siddhantic_cosmology": siddhanta,
            "puranic_cosmology": purana,
            "metric_comparison": comparison,
            "epistemic_matrix": [m.__dict__ for m in matrix],
            "concordism_firewall": firewall
        }


if __name__ == "__main__":
    engine = SiddhanticAndPuranicCosmologyEngine()
    results = engine.generate_comprehensive_report()
    print("=== SIDDHANTIC KHA-KAKSHA BOUNDARY ===")
    print(f"Circumference: {results['siddhantic_cosmology']['brahmanda_circumference_yojanas']:.4e} yojanas")
    print(f"Radius: {results['siddhantic_cosmology']['brahmanda_radius_yojanas']:.4e} yojanas")
    print(f"Radius in Light-Years: {results['siddhantic_cosmology']['brahmanda_radius_light_years']:.2f} ly")
    print("\n=== PURANIC 7-SHEATH ENVELOPE ===")
    print(f"Core Radius: {results['puranic_cosmology']['core_radius_yojanas']:.4e} yojanas ({results['puranic_cosmology']['core_radius_au']:.2f} AU)")
    print(f"Outer Sheath Radius: {results['puranic_cosmology']['total_envelope_radius_yojanas']:.4e} yojanas")
    print(f"Outer Sheath Radius in Light-Years: {results['puranic_cosmology']['total_envelope_radius_light_years']:.2f} ly")
    print("\n=== METRIC COMPARISON ===")
    print(f"Ratio of Siddhanta Radius to Purana Core: {results['metric_comparison']['radius_ratio_siddhanta_to_purana_core']:.2e}x")
    print(f"Ratio of Purana Outer Sheath to Siddhanta Radius: {results['metric_comparison']['radius_ratio_purana_envelope_to_siddhanta']:.2f}x")
