"""
epistemic_framework_analyzer.py

Formal Epistemological and Computational Analysis Framework for
Evaluating Dharmic Truth Claims, Cosmological Timescales, and Pramana Classification.

Standing Purpose: A002 (Raman) - Epistemic Class: Metaphysical
Protocol: Adjudication firewall. Distinguish investigable historical claims
from non-investigable metaphysical claims without asserting a metaphysical verdict.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional
import math


class EpistemicClass(Enum):
    HISTORICAL_TEXTUAL = "Historical/Philological/Archaeological"
    MATHEMATICAL_SPECIFICATION = "Internal Cosmological/Mathematical Specification"
    METAPHYSICAL_ONTOLOGICAL = "Metaphysical/Ontological/Transcendental"


class Pramana(Enum):
    PRATYAKSHA = "Pratyaksha (Direct Perception)"
    ANUMANA = "Anumana (Logical Inference)"
    UPAMANA = "Upamana (Analogy/Comparison)"
    ARTHAPATTI = "Arthapatti (Presumption/Postulation)"
    ANUPALABDHI = "Anupalabdhi (Non-perception/Negative proof)"
    SABDA = "Sabda (Verbal/Scriptural Testimony)"


class EmpiricalAdjudicability(Enum):
    DECIDABLE = "Decidable via empirical/historical methods"
    CONDITIONALLY_CONGRUENT = "Internally specific; congruence testable, metaphysical validity undecidable"
    UNDECIDABLE = "Resistant to empirical adjudication (metaphysically underdetermined)"


@dataclass
class ClaimRecord:
    claim_id: str
    description: str
    epistemic_class: EpistemicClass
    relevant_pramanas: List[Pramana]
    adjudicability: EmpiricalAdjudicability
    empirical_test: Optional[str]
    metaphysical_insulation_reason: Optional[str]
    disagreement_nature: str


class PuranicCosmologyCalculator:
    """
    Computes exact Puranic cosmological cycles and compares them
    with modern astrophysical and geological benchmarks.
    Demonstrates internal numerical specificity while maintaining the epistemic boundary.
    """

    # Base constants in solar years according to Surya Siddhanta and major Puranas (Vishnu Purana 1.3, etc.)
    KALI_YUGA = 432_000
    DVAPARA_YUGA = 2 * KALI_YUGA  # 864,000
    TRETA_YUGA = 3 * KALI_YUGA    # 1,296,000
    KRITA_YUGA = 4 * KALI_YUGA    # 1,728,000

    MAHAYUGA = KRITA_YUGA + TRETA_YUGA + DVAPARA_YUGA + KALI_YUGA  # 4,320,000

    MAHAYUGAS_PER_KALPA = 1_000
    KALPA_DURATION = MAHAYUGAS_PER_KALPA * MAHAYUGA  # 4,320,000,000 (4.32 Ga)

    # A full Day and Night of Brahma
    DAY_AND_NIGHT_OF_BRAHMA = 2 * KALPA_DURATION  # 8.64 Ga

    # Year of Brahma = 360 days and nights
    YEAR_OF_BRAHMA = 360 * DAY_AND_NIGHT_OF_BRAHMA  # 3.1104e12 solar years

    # 100 Years of Brahma (Maha-Kalpa / Life of Brahma)
    MAHA_KALPA = 100 * YEAR_OF_BRAHMA  # 3.1104e14 solar years (311.04 trillion years)

    # Modern scientific empirical benchmarks (for comparative contextualization)
    AGE_OF_EARTH_YEARS = 4.543e9       # Geochronological radiometric dating (Pb-Pb / meteorites)
    AGE_OF_UNIVERSE_YEARS = 13.787e9   # Lambda-CDM cosmological consensus (Planck 2018)
    SOLAR_MAIN_SEQUENCE_YEARS = 1.0e10 # Standard solar stellar evolution (~10 Ga)

    @classmethod
    def get_cycle_breakdown(cls) -> Dict[str, Any]:
        return {
            "kali_yuga_yr": cls.KALI_YUGA,
            "dvapara_yuga_yr": cls.DVAPARA_YUGA,
            "treta_yuga_yr": cls.TRETA_YUGA,
            "krita_yuga_yr": cls.KRITA_YUGA,
            "mahayuga_yr": cls.MAHAYUGA,
            "kalpa_day_yr": cls.KALPA_DURATION,
            "kalpa_night_pralaya_yr": cls.KALPA_DURATION,
            "brahma_nycthemeron_yr": cls.DAY_AND_NIGHT_OF_BRAHMA,
            "brahma_year_yr": cls.YEAR_OF_BRAHMA,
            "brahma_lifetime_yr": cls.MAHA_KALPA,
            "ratio": "4:3:2:1 (Krita:Treta:Dvapara:Kali)",
            "internal_consistency": True
        }

    @classmethod
    def compare_with_astrophysics(cls) -> Dict[str, Any]:
        kalpa_gyr = cls.KALPA_DURATION / 1e9
        earth_gyr = cls.AGE_OF_EARTH_YEARS / 1e9
        universe_gyr = cls.AGE_OF_UNIVERSE_YEARS / 1e9

        earth_diff_pct = abs(kalpa_gyr - earth_gyr) / earth_gyr * 100.0
        universe_ratio = universe_gyr / kalpa_gyr

        return {
            "kalpa_duration_gyr": kalpa_gyr,
            "earth_age_gyr": earth_gyr,
            "universe_age_gyr": universe_gyr,
            "delta_kalpa_earth_pct": round(earth_diff_pct, 2),
            "universe_to_kalpa_ratio": round(universe_ratio, 3),
            "epistemic_implication": (
                "Internal numerical specificity is verifiable within textual transmission. "
                "Order-of-magnitude proximity between Kalpa (4.32 Ga) and Earth's age (4.54 Ga) "
                "constitutes an interesting mathematical congruence, but logically CANNOT serve as "
                "an empirical proof of divine authorship without committing the fallacy of affirmation "
                "of the consequent. The text is an empirical historical object; its metaphysical claims "
                "remain underdetermined."
            )
        }


class EpistemicMatrix:
    """
    Formal registry separating investigable historical claims
    from non-investigable metaphysical claims.
    """

    def __init__(self):
        self.claims: List[ClaimRecord] = []
        self._populate_claims()

    def _populate_claims(self):
        # 1. Historical & Philological Claims (Investigable)
        self.claims.append(ClaimRecord(
            claim_id="HIST-001",
            description="The Rigveda Samhita was composed c. 1500-1200 BCE in the Greater Punjab region.",
            epistemic_class=EpistemicClass.HISTORICAL_TEXTUAL,
            relevant_pramanas=[Pramana.PRATYAKSHA, Pramana.ANUMANA],
            adjudicability=EmpiricalAdjudicability.DECIDABLE,
            empirical_test="Linguistic stratigraphy (Indo-Iranian cognates, Archaic Vedic Sanskrit meter), archaeological correspondence (Late Bronze/Early Iron Age, Painted Grey Ware), geographical references (Sapta Sindhu river systems).",
            metaphysical_insulation_reason=None,
            disagreement_nature="Philological and archaeological debate over absolute dating vs relative chronology; purely empirical and falsifiable."
        ))

        self.claims.append(ClaimRecord(
            claim_id="HIST-002",
            description="Vedic oral transmission preserved textual metrics and phonetics across millennia via formal mnemonic structures (Padapatha, Kramapatha, Jatapatha, Ghanapatha).",
            epistemic_class=EpistemicClass.HISTORICAL_TEXTUAL,
            relevant_pramanas=[Pramana.PRATYAKSHA, Pramana.ANUMANA],
            adjudicability=EmpiricalAdjudicability.DECIDABLE,
            empirical_test="Comparative analysis of surviving shakhas across geographically separated traditions (e.g., Nambudiri in Kerala vs Kashmiri vs Varanasi recensions) demonstrating near-zero variance in accent and syllable preservation.",
            metaphysical_insulation_reason=None,
            disagreement_nature="Linguistic, quantitative, and paleographical analysis of error rates and variant readings."
        ))

        self.claims.append(ClaimRecord(
            claim_id="HIST-003",
            description="The Principal Upanishads (e.g., Brihadaranyaka, Chandogya, Katha) date to the pre-Mauryan period (c. 800-500 BCE) preceding early Buddhism.",
            epistemic_class=EpistemicClass.HISTORICAL_TEXTUAL,
            relevant_pramanas=[Pramana.PRATYAKSHA, Pramana.ANUMANA],
            adjudicability=EmpiricalAdjudicability.DECIDABLE,
            empirical_test="Historical cross-references, linguistic syntax shifts from Brahmana prose to early Classical Sanskrit, allusions in early Buddhist (Pali Canon) and Jaina strata.",
            metaphysical_insulation_reason=None,
            disagreement_nature="Textual criticism, stratification, and comparative historiography."
        ))

        # 2. Internal Mathematical / Cosmological Specifications (Specific, Congruence-testable)
        self.claims.append(ClaimRecord(
            claim_id="COSMO-001",
            description="Puranic literature specifies cosmological cycles: 1 Mahayuga = 4.32 million years, 1 Kalpa = 4.32 billion years, following a 4:3:2:1 yuga ratio.",
            epistemic_class=EpistemicClass.MATHEMATICAL_SPECIFICATION,
            relevant_pramanas=[Pramana.PRATYAKSHA, Pramana.ANUMANA],
            adjudicability=EmpiricalAdjudicability.CONDITIONALLY_CONGRUENT,
            empirical_test="Textual verification across Vishnu Purana, Surya Siddhanta, and Bhagavata Purana confirms exact mathematical formulas. Comparison with physical geochronology evaluates numerical congruence.",
            metaphysical_insulation_reason="The existence of the textual specification is an empirical fact; the asserted cosmic recurring cycles (Pralaya, re-creation by Brahma) are transcendental and unobservable across cosmic epochs.",
            disagreement_nature="Historians treat it as an internally coherent ancient cosmological model with sexagesimal/astronomical numerology; believers or proponents may argue for ancient intuitive or divine knowledge; neither proves metaphysical divinity."
        ))

        # 3. Metaphysical / Ontological Claims (Resistant to Empirical Adjudication)
        self.claims.append(ClaimRecord(
            claim_id="META-001",
            description="Brahman is the non-dual ground of reality (Nirguna) or supreme omniscient, omnipotent personal deity (Saguna/Ishvara), from which spacetime emanates.",
            epistemic_class=EpistemicClass.METAPHYSICAL_ONTOLOGICAL,
            relevant_pramanas=[Pramana.SABDA, Pramana.ARTHAPATTI],
            adjudicability=EmpiricalAdjudicability.UNDECIDABLE,
            empirical_test=None,
            metaphysical_insulation_reason=(
                "Underdetermination: Any configuration of empirical physical laws (cosmic order, entropy, fine-tuning, or randomness) "
                "is compatible with both physicalist naturalism and Brahman as the ontological ground (either as non-dual conscious substratum "
                "or divine will). No sensory detector can measure pure metaphysical unmanifest consciousness (Avyakta/Cit)."
            ),
            disagreement_nature=(
                "Axiomatic dispute over ontological primitives: Believer posits Consciousness/Being as fundamental; "
                "Naturalist posits Mass-Energy/Spacetime fields as fundamental. Neither can construct an experiment to rule out the other's primitive."
            )
        ))

        self.claims.append(ClaimRecord(
            claim_id="META-002",
            description="The Law of Karma governs moral causality across trans-migratory lifecycles (Samsara), conserved across physical deaths.",
            epistemic_class=EpistemicClass.METAPHYSICAL_ONTOLOGICAL,
            relevant_pramanas=[Pramana.SABDA, Pramana.ARTHAPATTI],
            adjudicability=EmpiricalAdjudicability.UNDECIDABLE,
            empirical_test=None,
            metaphysical_insulation_reason=(
                "Causal insulation: The causal mechanism linking moral action in lifespan T1 to biological birth or circumstance in lifespan T2 "
                "is explicitly posited as unseen (Adrishta) and suprasensory (Atindriya). Because retroactive moral adjustment can explain any outcome "
                "(good fortune attributed to past unseen punya, suffering to unseen papa), the claim is unfalsifiable in empirical spacetime."
            ),
            disagreement_nature=(
                "Believer sees moral coherence and explanatory justice in cosmic suffering; non-believer applies Ockham's razor, noting zero empirical "
                "trace of non-physical causal conservation and explaining suffering via biological/sociological contingency."
            )
        ))

        self.claims.append(ClaimRecord(
            claim_id="META-003",
            description="The Vedas possess intrinsic authorless revelation (Apaurusheyatva) or divine revelation, providing infallible knowledge of Atindriya (suprasensory) truths.",
            epistemic_class=EpistemicClass.METAPHYSICAL_ONTOLOGICAL,
            relevant_pramanas=[Pramana.SABDA],
            adjudicability=EmpiricalAdjudicability.UNDECIDABLE,
            empirical_test=None,
            metaphysical_insulation_reason=(
                "Epistemic circularity: The claim that the texts are apaurusheya/divinely revealed is justified by scriptural self-testimony "
                "or transcendental deduction (Mimamsa epistemology). Empirical history documents manuscripts and human recensions, but cannot "
                "detect the metaphysical presence or absence of an authorless transcendental archetype (Sphota/Veda-Nityatva)."
            ),
            disagreement_nature=(
                "Disagreement over valid Pramanas (epistemic instruments): Mimamsa/Vedanta accept Sabda as an autonomous, self-validating pramana (Svatah-pramanya) "
                "for suprasensory realms; Carvaka and naturalism reject Sabda as independent pramana, reducing valid knowledge to Pratyaksha (perception) and strictly empirical Anumana."
            )
        ))

        self.claims.append(ClaimRecord(
            claim_id="META-004",
            description="Gods (Devas, e.g., Indra, Agni, Shiva, Vishnu) exist as actual ontological entities, cosmological intelligences, or conscious aspects of Brahman.",
            epistemic_class=EpistemicClass.METAPHYSICAL_ONTOLOGICAL,
            relevant_pramanas=[Pramana.SABDA, Pramana.ARTHAPATTI],
            adjudicability=EmpiricalAdjudicability.UNDECIDABLE,
            empirical_test=None,
            metaphysical_insulation_reason=(
                "Ontological flexibility: Depending on the school, Devas are understood literally as subtle-bodied cosmic beings (Puranic), "
                "metaphorically as cosmic forces/mantra powers (Mimamsa), or non-dual manifestations of the singular Saguna Brahman (Vedanta). "
                "No empirical observation (e.g., absence of celestial bodies on Mount Meru or lack of physical avatars in modern cities) "
                "can falsify subtle (sukshma) or transcendental dimensions defined as non-interacting with classical electromagnetic instrumentation."
            ),
            disagreement_nature=(
                "Believer operates within an enchanted, multi-layered cosmos with subjective experiential realization (Darshana, Anubhuti); "
                "non-believer demands reproducible physical measurement and attributes devas to anthropomorphic myth-making."
            )
        ))

    def get_claims_by_class(self, ep_class: EpistemicClass) -> List[ClaimRecord]:
        return [c for c in self.claims if c.epistemic_class == ep_class]

    def summary_stats(self) -> Dict[str, Any]:
        return {
            "total_claims_cataloged": len(self.claims),
            "historical_investigable": len(self.get_claims_by_class(EpistemicClass.HISTORICAL_TEXTUAL)),
            "cosmological_specified": len(self.get_claims_by_class(EpistemicClass.MATHEMATICAL_SPECIFICATION)),
            "metaphysical_undecidable": len(self.get_claims_by_class(EpistemicClass.METAPHYSICAL_ONTOLOGICAL)),
            "epistemic_firewall_enforced": True
        }


def run_formal_evaluation():
    calc = PuranicCosmologyCalculator()
    cycles = calc.get_cycle_breakdown()
    astro = calc.compare_with_astrophysics()
    matrix = EpistemicMatrix()
    stats = matrix.summary_stats()

    print("=" * 80)
    print("EPISTEMIC FRAMEWORK EVALUATION - DHARMIC TRUTH CLAIMS")
    print("=" * 80)
    print("\n[1] COSMOLOGICAL TIMESCALE SPECIFICITY ANALYSIS:")
    print(f"  - Mahayuga: {cycles['mahayuga_yr']:,} solar years")
    print(f"  - Kalpa (Day of Brahma): {cycles['kalpa_day_yr']:,} solar years ({cycles['kalpa_day_yr']/1e9:.2f} Ga)")
    print(f"  - Nycthemeron (Day + Night): {cycles['brahma_nycthemeron_yr']:,} solar years ({cycles['brahma_nycthemeron_yr']/1e9:.2f} Ga)")
    print(f"  - Brahma Lifetime (100 years): {cycles['brahma_lifetime_yr']:,} solar years ({cycles['brahma_lifetime_yr']/1e12:.2f} Trillion years)")
    print(f"  - Yuga Ratio: {cycles['ratio']}")
    print(f"\n  Astrophysical Comparison:")
    print(f"  - Modern Geochronology (Earth Age): {astro['earth_age_gyr']} Ga")
    print(f"  - Kalpa Duration: {astro['kalpa_duration_gyr']} Ga (Delta: {astro['delta_kalpa_earth_pct']:.2f}%)")
    print(f"  - Universe Age: {astro['universe_age_gyr']} Ga (Ratio to Kalpa: {astro['universe_to_kalpa_ratio']})")
    print(f"  Epistemic Note: {astro['epistemic_implication']}\n")

    print("[2] CLAIM CLASSIFICATION & ADJUDICABILITY MATRIX:")
    for claim in matrix.claims:
        print(f"  [{claim.claim_id}] {claim.description}")
        print(f"    Class: {claim.epistemic_class.value}")
        print(f"    Adjudicability: {claim.adjudicability.value}")
        if claim.empirical_test:
            print(f"    Empirical Test: {claim.empirical_test}")
        if claim.metaphysical_insulation_reason:
            print(f"    Insulation Reason: {claim.metaphysical_insulation_reason}")
        print(f"    Disagreement Root: {claim.disagreement_nature}")
        print("-" * 60)

    print(f"\n[3] EPISTEMIC FIREWALL AUDIT:")
    print(f"  Total claims analyzed: {stats['total_claims_cataloged']}")
    print(f"  Historical / Investigable: {stats['historical_investigable']}")
    print(f"  Mathematical / Specified: {stats['cosmological_specified']}")
    print(f"  Metaphysical / Undecidable: {stats['metaphysical_undecidable']}")
    print(f"  Firewall status: ENFORCED (Zero metaphysical verdicts asserted)")
    print("=" * 80)


if __name__ == "__main__":
    run_formal_evaluation()
