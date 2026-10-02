"""
krishna_mahabharata_historicity_engine.py

Comprehensive Epistemic Analysis and Verification Engine for the Historicity of Lord Krishna
and the Mahabharata War.

Demarcates strictly across:
1. Primary Material & Textual Evidence (Archaeology, Epigraphy, Numismatics, Early Manuscripts)
2. Scholarly Historical Consensus (Philology, Comparative Indology, Stratigraphy)
3. Devotional & Theological Claims (Puranic Orthodoxy, Faith Traditions, Metaphysics)

Enforces strict protocol invariants:
- PROTOCOL VIOLATION 1: Treating scripture as laboratory data
- PROTOCOL VIOLATION 2: Treating absence of evidence as proof of falsehood
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Tuple, Any
import math
import statistics


class EpistemicClass(Enum):
    PRIMARY_MATERIAL_EPIGRAPHIC = "PRIMARY_MATERIAL_EPIGRAPHIC"
    PRIMARY_TEXTUAL_LATE_VEDIC = "PRIMARY_TEXTUAL_LATE_VEDIC"
    PRIMARY_ARCHAEOLOGICAL_STRATUM = "PRIMARY_ARCHAEOLOGICAL_STRATUM"
    SCHOLARLY_HISTORICAL_CONSENSUS = "SCHOLARLY_HISTORICAL_CONSENSUS"
    DEVOTIONAL_THEOLOGICAL_CLAIM = "DEVOTIONAL_THEOLOGICAL_CLAIM"
    METAPHYSICAL_ONTOLOGICAL = "METAPHYSICAL_ONTOLOGICAL"


class ProtocolViolationType(Enum):
    SCRIPTURE_AS_LABORATORY_DATA = "SCRIPTURE_AS_LABORATORY_DATA"
    ABSENCE_OF_EVIDENCE_AS_PROOF_OF_FALSEHOOD = "ABSENCE_OF_EVIDENCE_AS_PROOF_OF_FALSEHOOD"
    CATEGORY_CONFUSION = "CATEGORY_CONFUSION"


class ProtocolViolationException(Exception):
    def __init__(self, violation_type: ProtocolViolationType, message: str):
        self.violation_type = violation_type
        self.message = message
        super().__init__(f"PROTOCOL VIOLATION [{violation_type.value}]: {message}")


@dataclass(frozen=True)
class ArchaeologicalSiteRecord:
    site_name: str
    traditional_epic_name: str
    primary_excavators: str
    excavation_years: str
    ceramic_cultural_horizon: str
    calibrated_c14_bce_range: Tuple[int, int]
    key_findings: List[str]
    epic_congruence_description: str
    scholarly_epistemic_status: str


@dataclass(frozen=True)
class EpigraphicRecord:
    artifact_name: str
    discovery_location: str
    date_bce_ce: str
    nominal_year_bce: int
    ruler_or_patron: str
    script_and_language: str
    theological_or_historical_content: str
    epistemic_significance: str


@dataclass(frozen=True)
class TextualStratumRecord:
    stratum_name: str
    estimated_composition_period: str
    approximate_verse_count: int
    content_focus: str
    krishna_conception: str
    redaction_stage: str


@dataclass(frozen=True)
class AstronomicalWarDateHypothesis:
    proponent: str
    proposed_date_bce: int
    methodology: str
    key_astronomical_anchors: List[str]
    methodological_critique: str
    epistemic_validity_rating: str  # e.g., "POOR_INVERSE_PROBLEM", "THEORETICAL_EPOCH", "PLAUSIBLE_HISTORICAL_WINDOW"


class TextualStratificationModel:
    """
    Quantifies the growth of the Mahabharata corpus from the core Jaya to the Vulgate.
    """
    def __init__(self):
        self.strata: Dict[str, TextualStratumRecord] = {
            "Jaya": TextualStratumRecord(
                stratum_name="Jaya (Victory)",
                estimated_composition_period="c. 1000 - 800 BCE",
                approximate_verse_count=8818,
                content_focus="Heroic bardic ballad of the fratricidal Kuru war between Kauravas and Pandavas",
                krishna_conception="Charismatic Vrishni chieftain, diplomat, and Pandava strategist/counselor",
                redaction_stage="Original bardic core attributed to Vyasa"
            ),
            "Bharata": TextualStratumRecord(
                stratum_name="Bharata",
                estimated_composition_period="c. 800 - 400 BCE",
                approximate_verse_count=24000,
                content_focus="Expanded clan epic recited at Janamejaya's snake sacrifice; dynastic lore",
                krishna_conception="Heroic prince, wise statesman, revered leader of the Vrishnis",
                redaction_stage="Recited by Vaishampayana"
            ),
            "Critical_Edition": TextualStratumRecord(
                stratum_name="Mahabharata (BORI Critical Edition)",
                estimated_composition_period="Reconstructed archetype c. 400 BCE - 400 CE",
                approximate_verse_count=82153,
                content_focus="Comprehensive critical archetype collating 1,259 manuscripts across all scripts",
                krishna_conception="Divine-human hero, teacher of the Bhagavad Gita, manifestation of Narayana/Vishnu",
                redaction_stage="Bhandarkar Oriental Research Institute (BORI, 1919-1966)"
            ),
            "Vulgate": TextualStratumRecord(
                stratum_name="Mahabharata (Vulgate / Nilakantha)",
                estimated_composition_period="Final consolidation c. 400 CE - 16th century CE",
                approximate_verse_count=100000,
                content_focus="Encyclopedic compendium of dharma, niti, cosmology, moksha, legends",
                krishna_conception="Svayam Bhagavan, Supreme Godhead incarnate, universal sovereign",
                redaction_stage="Recited by Ugrasrava Sauti to Shaunaka; includes later regional interpolations"
            )
        }

    def compute_expansion_ratio(self, base_layer: str = "Jaya", target_layer: str = "Vulgate") -> float:
        base_count = self.strata[base_layer].approximate_verse_count
        target_count = self.strata[target_layer].approximate_verse_count
        return target_count / base_count

    def compute_inflation_metrics(self) -> Dict[str, Any]:
        jaya_verses = self.strata["Jaya"].approximate_verse_count
        bharata_verses = self.strata["Bharata"].approximate_verse_count
        bori_verses = self.strata["Critical_Edition"].approximate_verse_count
        vulgate_verses = self.strata["Vulgate"].approximate_verse_count

        return {
            "jaya_verses": jaya_verses,
            "bharata_verses": bharata_verses,
            "bori_critical_verses": bori_verses,
            "vulgate_verses": vulgate_verses,
            "jaya_to_bharata_growth": bharata_verses / jaya_verses,
            "jaya_to_bori_growth": bori_verses / jaya_verses,
            "jaya_to_vulgate_growth": vulgate_verses / jaya_verses,
            "bori_to_vulgate_interpolations": vulgate_verses - bori_verses,
            "bori_rejection_percentage": ((vulgate_verses - bori_verses) / vulgate_verses) * 100.0,
            "net_expansion_factor": vulgate_verses / jaya_verses
        }


class DynasticGenerationalModel:
    """
    Models dynastic generational chronologies from Parikshit to historical anchors (e.g. Mahapadma Nanda).
    Demonstrates why 3102 BCE requires historically impossible reign lengths,
    while 1000-900 BCE aligns with documented human demographic averages.
    """
    def __init__(self):
        # Historical fixed anchor: Coronation of Mahapadma Nanda (c. 362 BCE - 345 BCE)
        self.nanda_accession_bce = 362
        # Number of kings recorded in Puranic king lists (Matsya, Vayu, Vishnu)
        # from Parikshit to Mahapadma Nanda across the Barhadratha / Kuru / Magadha successions
        self.puranic_generations_parikshit_to_nanda = 30

    def compute_implied_reign_length(self, war_date_bce: int) -> float:
        """Computes the average years per reign required for a given war date."""
        if war_date_bce <= self.nanda_accession_bce:
            raise ValueError("War date must precede Nanda accession (362 BCE)")
        elapsed_years = war_date_bce - self.nanda_accession_bce
        return elapsed_years / self.puranic_generations_parikshit_to_nanda

    def evaluate_dynastic_feasibility(self, war_date_bce: int) -> Dict[str, Any]:
        implied_reign = self.compute_implied_reign_length(war_date_bce)
        # Historical global empirical average for dynastic reigns: 14 to 22 years
        # Extreme upper biological bound: 30 years
        # Implied reign > 35 years is statistically highly improbable; > 60 years is biologically impossible.
        if implied_reign > 50.0:
            verdict = "BIOLOGICALLY_IMPOSSIBLE_DYNASTIC_AVERAGE"
            feasibility = False
        elif implied_reign > 30.0:
            verdict = "STATISTICALLY_HIGHLY_IMPROBABLE"
            feasibility = False
        elif 12.0 <= implied_reign <= 25.0:
            verdict = "HIGHLY_PLAUSIBLE_HISTORICAL_CONCORDANCE"
            feasibility = True
        else:
            verdict = "MARGINAL"
            feasibility = True

        return {
            "war_date_bce": war_date_bce,
            "elapsed_to_nanda_years": war_date_bce - self.nanda_accession_bce,
            "generations_count": self.puranic_generations_parikshit_to_nanda,
            "implied_mean_reign_years": implied_reign,
            "historical_empirical_benchmark_range": (14.0, 22.0),
            "verdict": verdict,
            "feasible": feasibility
        }


class ArchaeoastronomySensitivityModel:
    """
    Evaluates the dispersion and methodological underdetermination (inverse problem)
    in astronomical dating proposals for the Mahabharata war.
    """
    def __init__(self):
        self.proposals: List[AstronomicalWarDateHypothesis] = [
            AstronomicalWarDateHypothesis(
                proponent="P.V. Vartak (1989)",
                proposed_date_bce=5561,
                methodology="Retrograde planetary positions and nakshatra conjunctions matching selected verses",
                key_astronomical_anchors=["Saturn in Rohini", "Jupiter in Vishakha", "Solar eclipse at Jyeshtha"],
                methodological_critique="Massive chronological isolation: predates all Indian metallurgy, agriculture, and urbanism by millennia; ignores stratigraphy and philology",
                epistemic_validity_rating="SEVERE_INVERSE_PROBLEM_CHERRY_PICKED"
            ),
            AstronomicalWarDateHypothesis(
                proponent="Aryabhata / Traditional Kali Epoch (499 CE)",
                proposed_date_bce=3102,
                methodology="Theoretical mean conjunction of all 7 visible classical planets at 0 degrees Mesha (Aries)",
                key_astronomical_anchors=["Kali Yuga entry 18 Feb 3102 BCE", "Aryabhatiya Kalakriyapada"],
                methodological_critique="Theoretical back-calculation; modern ephemerides prove planets were dispersed over ~40 degrees, not physically conjunct; conflicts with dynastic and PGW data",
                epistemic_validity_rating="MATHEMATICAL_THEORETICAL_EPOCH"
            ),
            AstronomicalWarDateHypothesis(
                proponent="Narahari Achar (2003)",
                proposed_date_bce=3067,
                methodology="Planetarium simulation matching Udyoga and Bhishma Parvan planetary descriptions",
                key_astronomical_anchors=["Saturn in Rohini", "Solar eclipse at Jyeshtha, Lunar at Kartika"],
                methodological_critique="Suffers from degeneracy: alternative century solutions exist; requires treating poetic similes as precise telemetry",
                epistemic_validity_rating="INVERSE_DEGENERACY_UNRESOLVED"
            ),
            AstronomicalWarDateHypothesis(
                proponent="S. Balakrishna (2000)",
                proposed_date_bce=2559,
                methodology="Lunar and solar eclipses mentioned in Sabha and Bhishma parvans",
                key_astronomical_anchors=["Pair of eclipses within 13 days", "Penumbra calculations"],
                methodological_critique="13-day eclipse pairs occur multiple times every millennium; underdetermined without absolute chronological anchor",
                epistemic_validity_rating="RECURRENT_CYCLICAL_AMBIGUITY"
            ),
            AstronomicalWarDateHypothesis(
                proponent="Mohan Gupta (1999)",
                proposed_date_bce=1924,
                methodology="Planetary alignments and solstice references",
                key_astronomical_anchors=["Winter solstice alignment with Bhishma's passing"],
                methodological_critique="Selects an intermediate Bronze Age window but lacks specific epigraphic or ceramic corroboration",
                epistemic_validity_rating="INTERMEDIATE_UNCONSTRAINED"
            ),
            AstronomicalWarDateHypothesis(
                proponent="B.N. Achar / R.N. Iyengar / S.B. Roy (1976-2005)",
                proposed_date_bce=1478,
                methodology="Vedic calendrical nakshatra references and Vedanga Jyotisha solstice correlations",
                key_astronomical_anchors=["Solstice at Dhanishta", "Late Vedic stellar alignments"],
                methodological_critique="Plausible for early Vedic strata, but still predates Painted Grey Ware / Iron Age peak",
                epistemic_validity_rating="PLAUSIBLE_VEDIC_STRATUM_MISMATCHED_EPIC"
            ),
            AstronomicalWarDateHypothesis(
                proponent="Pargiter / B.B. Lal / H.C. Raychaudhuri (1922-2005)",
                proposed_date_bce=950,
                methodology="Triangulation of dynastic genealogies, PGW C-14 stratigraphy, and Hastinapura flood horizon",
                key_astronomical_anchors=["Sync with Kuru-Panchala historical kings", "Nichakshu flood", "Late Vedic texts"],
                methodological_critique="Integrates material archaeology, philology, and genealogy; not based purely on single sky retrocalc",
                epistemic_validity_rating="SCHOLARLY_HISTORICAL_CONCENSUS_RANGE"
            )
        ]

    def compute_dispersion_statistics(self) -> Dict[str, float]:
        dates = [p.proposed_date_bce for p in self.proposals]
        mean_date = float(statistics.mean(dates))
        median_date = float(statistics.median(dates))
        std_dev = float(statistics.stdev(dates))
        span = float(max(dates) - min(dates))
        return {
            "min_date_bce": float(min(dates)),
            "max_date_bce": float(max(dates)),
            "span_years": span,
            "mean_date_bce": mean_date,
            "median_date_bce": median_date,
            "std_deviation_years": std_dev,
            "coefficient_of_variation": (std_dev / mean_date) * 100.0
        }


class ArchaeologicalCorpusRegistry:
    """
    Catalogues primary archaeological excavations at traditional Mahabharata and Krishna sites.
    """
    def __init__(self):
        self.sites: Dict[str, ArchaeologicalSiteRecord] = {
            "Hastinapura": ArchaeologicalSiteRecord(
                site_name="Hastinapura (Meerut District, UP)",
                traditional_epic_name="Hastinapura (Capital of the Kurus)",
                primary_excavators="B.B. Lal (Archaeological Survey of India)",
                excavation_years="1950-1952",
                ceramic_cultural_horizon="Period II: Painted Grey Ware (PGW)",
                calibrated_c14_bce_range=(1100, 800),
                key_findings=[
                    "Stratified PGW deposits with iron slags and copper implements",
                    "Domesticated horse (Equus caballus) bones identified",
                    "Massive alluvial flood layer eroding the upper PGW stratum",
                    "Subsequent abandonment and relocation of settlement"
                ],
                epic_congruence_description=(
                    "Matches Matsya Purana 50.78 & Vayu Purana 99.271: during King Nichakshu's reign, "
                    "Hastinapura was washed away by the Ganga flood, causing the Kuru court to migrate to Kaushambi."
                ),
                scholarly_epistemic_status="STRONG_PRIMARY_STRATIGRAPHIC_CORROBORATION"
            ),
            "Kaushambi": ArchaeologicalSiteRecord(
                site_name="Kaushambi (Prayagraj District, UP)",
                traditional_epic_name="Kaushambi (Second Kuru Capital)",
                primary_excavators="G.R. Sharma (University of Allahabad)",
                excavation_years="1949-1960",
                ceramic_cultural_horizon="Late PGW transitioning to Northern Black Polished Ware (NBPW)",
                calibrated_c14_bce_range=(900, 300),
                key_findings=[
                    "Arrival of advanced ceramic technology directly contemporary with Hastinapura post-flood abandonment",
                    "Extensive mud-brick fortifications and early iron weaponry"
                ],
                epic_congruence_description="Directly corroborates the Puranic account of Kuru dynastic relocation post-Hastinapura flood.",
                scholarly_epistemic_status="STRONG_PRIMARY_STRATIGRAPHIC_CORROBORATION"
            ),
            "Kurukshetra": ArchaeologicalSiteRecord(
                site_name="Kurukshetra (Brahmasarovar, Raja Karna Ka Tila, Bhagwanpura)",
                traditional_epic_name="Dharmakshetra Kurukshetra (Epic Battlefield)",
                primary_excavators="J.P. Joshi, U.V. Singh (ASI)",
                excavation_years="1970-1980",
                ceramic_cultural_horizon="Late Harappan overlapping directly with Painted Grey Ware (PGW)",
                calibrated_c14_bce_range=(1400, 800),
                key_findings=[
                    "Direct cultural continuity/overlap between Late Bronze Age and PGW Iron Age",
                    "Settlement mounds with continuous habitation during late 2nd to early 1st millennium BCE"
                ],
                epic_congruence_description="Confirms heavy, contiguous occupation of Kurukshetra plain during the late Vedic and PGW periods.",
                scholarly_epistemic_status="CONFIRMED_HABITATION_EPIC_HORIZON"
            ),
            "Dwarka": ArchaeologicalSiteRecord(
                site_name="Dwarka & Bet Dwarka (Saurashtra Coast, Gujarat)",
                traditional_epic_name="Dvaraka / Dvaravati (Krishna's Coastal Citadel)",
                primary_excavators="S.R. Rao (National Institute of Oceanography), A.S. Gaur, Sundaresh",
                excavation_years="1983-2005",
                ceramic_cultural_horizon="Late Harappan Lustrous Red Ware to Early Historic",
                calibrated_c14_bce_range=(1500, 300),
                key_findings=[
                    "Submerged dressed stone masonry, circular and semi-circular bastions",
                    "Prismatic triangular three-holed stone anchors resembling Late Bronze Age Mediterranean anchors",
                    "Late Harappan seal with 3-headed composite animal motif",
                    "Stratified marine transgression layers showing coastal submergence"
                ],
                epic_congruence_description=(
                    "Matches Mahabharata Mausala Parva narrative: Dvaraka was built on the western coast "
                    "and submerged by the rising sea following internal clan conflict and Krishna's demise."
                ),
                scholarly_epistemic_status="CONFIRMED_SUBMERGED_PORT_SETTLEMENT"
            ),
            "Indraprastha": ArchaeologicalSiteRecord(
                site_name="Purana Qila (New Delhi)",
                traditional_epic_name="Indraprastha (Pandava Capital)",
                primary_excavators="B.B. Lal, V.D. Sharma, Vasant Swarnkar (ASI)",
                excavation_years="1954, 1969-1973, 2013-2018",
                ceramic_cultural_horizon="Stratified sequence: PGW at base, through NBPW, Maurya, Sunga, Kushana",
                calibrated_c14_bce_range=(1000, 600),
                key_findings=[
                    "PGW sherds at the lowest stratified cultural levels",
                    "Iron implements and terracotta figurines"
                ],
                epic_congruence_description="Confirms ancient continuous urban occupation at the traditional site of Indraprastha dating to PGW era.",
                scholarly_epistemic_status="CONFIRMED_PGW_HORIZON_AT_TRADITIONAL_LOCUS"
            ),
            "Sinauli": ArchaeologicalSiteRecord(
                site_name="Sinauli (Baghpat District, UP - ancient Vyaghraprastha)",
                traditional_epic_name="Vyaghraprastha (One of the Five Pandava Villages)",
                primary_excavators="D.V. Sharma, Sanjay Manjul (ASI)",
                excavation_years="2005-2006, 2018-2020",
                ceramic_cultural_horizon="Late Copper Age / Ochre Coloured Pottery (OCP) / Copper Hoard Culture",
                calibrated_c14_bce_range=(2000, 1800),
                key_findings=[
                    "Intact wooden carts/chariots with solid disk wheels adorned with copper triangle inlays",
                    "Copper antennae swords with raised central midribs, copper helmets and shields",
                    "Elite royal necropolis indicating advanced martial aristocracy in the Upper Doab"
                ],
                epic_congruence_description=(
                    "Establishes physical proof of horse/bullock-drawn wheeled combat vehicles and copper weaponry "
                    "in the Kuru-Panchala geographical realm preceding the Iron Age."
                ),
                scholarly_epistemic_status="PROVED_PRE_IRON_AGE_MARTIAL_ELITE_AND_CHARIOTS"
            )
        }


class EpigraphicCorpusRegistry:
    """
    Catalogues the earliest epigraphic and numismatic primary evidence for Krishna/Vasudeva.
    """
    def __init__(self):
        self.inscriptions: List[EpigraphicRecord] = [
            EpigraphicRecord(
                artifact_name="Coins of Agathocles of Bactria",
                discovery_location="Ai-Khanoum (Oxus Valley, Northern Afghanistan)",
                date_bce_ce="c. 190 - 180 BCE",
                nominal_year_bce=185,
                ruler_or_patron="King Agathocles of Bactria",
                script_and_language="Brahmi (Prakrit) on obverse; Greek on reverse",
                theological_or_historical_content=(
                    "Obverse: Vasudeva-Krishna holding six-spoked Chakra (wheel) and Sankha/Gada, "
                    "labeled 'Rajane Agathukleyasa'. Reverse: Sankarshana-Balarama holding Hala (plow) and Gada."
                ),
                epistemic_significance=(
                    "PRIMARY MATERIAL PROOF: Unambiguous royal numismatic representation of Krishna-Vasudeva "
                    "with divine iconographic emblems (Chakra) by early 2nd century BCE; proves international "
                    "recognition of the cult among Hellenistic rulers."
                )
            ),
            EpigraphicRecord(
                artifact_name="Heliodorus Pillar Inscription",
                discovery_location="Besnagar (Vidisha, Madhya Pradesh)",
                date_bce_ce="c. 113 BCE",
                nominal_year_bce=113,
                ruler_or_patron="Heliodorus, son of Dion (Greek ambassador of King Antialcidas to King Bhagabhadra)",
                script_and_language="Brahmi script; Early Middle Indo-Aryan Prakrit",
                theological_or_historical_content=(
                    "Dedicates a Garuda-dhvaja pillar to 'Devadeva Vasudeva' (God of Gods, Vasudeva). "
                    "Heliodorus proclaims himself a 'Bhagavata' and records the three immortal ethical steps "
                    "(Trini Amutapadani): Dama (self-control), Tyaga (charity/renunciation), Apramada (vigilance)."
                ),
                epistemic_significance=(
                    "PRIMARY MATERIAL PROOF: Conclusively documents Bhagavata Vaishnavism, Krishna's supreme "
                    "divine status ('Devadeva'), Garuda emblem, and Mahabharata ethical aphorisms (Stri Parva 7.23) "
                    "among Greek converts by late 2nd century BCE."
                )
            ),
            EpigraphicRecord(
                artifact_name="Ghosundi & Hathibada Inscriptions",
                discovery_location="Nagari (near Chittorgarh, Rajasthan)",
                date_bce_ce="c. 1st century BCE",
                nominal_year_bce=50,
                ruler_or_patron="King Sarvatata (performer of Ashvamedha sacrifice)",
                script_and_language="Brahmi script; Sanskritized Prakrit",
                theological_or_historical_content=(
                    "Records the construction of a stone boundary wall (Pujasila-prakara) for the worship of "
                    "Bhagavan Sankarshana and Bhagavan Vasudeva, referred to as 'Anahata' (unconquered) and "
                    "'Sarvesvara' (Lords of All)."
                ),
                epistemic_significance=(
                    "PRIMARY MATERIAL PROOF: Verifies formal temple enclosure and supreme theological status "
                    "of Krishna-Vasudeva and Balarama in Western India before the Common Era."
                )
            ),
            EpigraphicRecord(
                artifact_name="Mora Well Inscription",
                discovery_location="Mora (7 miles west of Mathura, UP)",
                date_bce_ce="c. early 1st century CE (reign of Shodasa)",
                nominal_year_bce=-15,  # ~15 CE
                ruler_or_patron="Mahakshatrapa Shodasa (Indo-Scythian ruler) / Tosha (donor)",
                script_and_language="Brahmi script; Early Epigraphical Hybrid Sanskrit",
                theological_or_historical_content=(
                    "Records the installation of stone images of the 'Five Holy Vrishni Heroes' "
                    "(Bhagavatam Vrishninam Pancha-Viranam Pratimah): Sankarshana, Vasudeva, Pradyumna, Samba, Aniruddha "
                    "inside a stone temple."
                ),
                epistemic_significance=(
                    "PRIMARY MATERIAL PROOF: Conclusively links Krishna-Vasudeva to the historical Vrishni lineage "
                    "and confirms hero-veneration transitioning into full temple deification at Mathura."
                )
            ),
            EpigraphicRecord(
                artifact_name="Nanaghat Cave Inscription",
                discovery_location="Nanaghat Pass (Pune District, Maharashtra)",
                date_bce_ce="c. 1st century BCE",
                nominal_year_bce=75,
                ruler_or_patron="Satavahana Queen Naganika",
                script_and_language="Brahmi script; Prakrit",
                theological_or_historical_content=(
                    "Opens with solemn invocations to Dharma, Indra, Sankarshana-Vasudeva, Surya-Chandra, "
                    "and the four Guardians of the Quarters (Lokapalas)."
                ),
                epistemic_significance=(
                    "PRIMARY MATERIAL PROOF: Demonstrates the integration of Sankarshana-Vasudeva into royal "
                    "Vedic sacrificial state religion in the Deccan."
                )
            )
        ]


class EpistemicAdjudicationFramework:
    """
    Formal Adjudication Engine.
    Enforces the epistemic firewall, detects protocol violations, and maps truth claims.
    """
    def __init__(self):
        self.textual_model = TextualStratificationModel()
        self.dynastic_model = DynasticGenerationalModel()
        self.astronomy_model = ArchaeoastronomySensitivityModel()
        self.archaeology_registry = ArchaeologicalCorpusRegistry()
        self.epigraphic_registry = EpigraphicCorpusRegistry()

    def audit_claim_for_violations(self, claim_statement: str, claimed_category: EpistemicClass, is_asserting_empirical_proof: bool) -> Optional[ProtocolViolationType]:
        """
        Audits an assertion against the two mandatory protocol rules:
        1. Treating scripture as laboratory data.
        2. Treating absence of evidence as proof of falsehood.
        """
        text_lower = claim_statement.lower()

        # Violation 1 check: Scripture as laboratory data
        laboratory_keywords = ["megaton", "radiation", "nuclear weapon", "atomic blast", "quantum telemetry", "laboratory proof", "physically measured"]
        scriptural_keywords = ["brahmashira", "brahmastra", "pasupata", "divyastra", "vishvarupa", "18 akshauhinis"]
        
        has_lab_word = any(k in text_lower for k in laboratory_keywords)
        has_script_word = any(k in text_lower for k in scriptural_keywords)
        if has_lab_word and has_script_word:
            return ProtocolViolationType.SCRIPTURE_AS_LABORATORY_DATA

        if claimed_category == EpistemicClass.DEVOTIONAL_THEOLOGICAL_CLAIM and is_asserting_empirical_proof:
            return ProtocolViolationType.SCRIPTURE_AS_LABORATORY_DATA

        # Violation 2 check: Absence of evidence as proof of falsehood
        absence_keywords = ["no contemporary 3100 bce inscription", "absence of archaeological proof", "no written record from 3000 bce"]
        falsehood_keywords = ["proves it never happened", "proves it is entirely pure fiction", "proves krishna never existed", "disproves any historical core"]
        has_absence = any(k in text_lower for k in absence_keywords)
        has_falsehood = any(k in text_lower for k in falsehood_keywords)
        if has_absence and has_falsehood:
            return ProtocolViolationType.ABSENCE_OF_EVIDENCE_AS_PROOF_OF_FALSEHOOD

        return None

    def evaluate_claim(self, claim_statement: str, claimed_category: EpistemicClass, is_asserting_empirical_proof: bool = False) -> Dict[str, Any]:
        violation = self.audit_claim_for_violations(claim_statement, claimed_category, is_asserting_empirical_proof)
        if violation:
            raise ProtocolViolationException(violation, f"Claim failed epistemic firewall: {claim_statement}")

        return {
            "claim": claim_statement,
            "category": claimed_category.value,
            "status": "APPROVED_FOR_ANALYSIS",
            "epistemic_audit": "PASSED_FIREWALL"
        }

    def generate_comprehensive_synthesis(self) -> Dict[str, Any]:
        """
        Computes all quantitative models and outputs a structured synthesis.
        """
        textual_metrics = self.textual_model.compute_inflation_metrics()
        dynastic_3102 = self.dynastic_model.evaluate_dynastic_feasibility(3102)
        dynastic_950 = self.dynastic_model.evaluate_dynastic_feasibility(950)
        dynastic_1400 = self.dynastic_model.evaluate_dynastic_feasibility(1400)
        astronomy_dispersion = self.astronomy_model.compute_dispersion_statistics()

        return {
            "textual_metrics": textual_metrics,
            "dynastic_feasibility": {
                "epoch_3102_bce": dynastic_3102,
                "epoch_1400_bce": dynastic_1400,
                "epoch_950_bce": dynastic_950
            },
            "astronomy_dispersion": astronomy_dispersion,
            "archaeological_sites_count": len(self.archaeology_registry.sites),
            "epigraphic_records_count": len(self.epigraphic_registry.inscriptions),
            "tripartite_demarcation": {
                "primary_material_documented": [
                    "Heliodorus Pillar (113 BCE): Documents Devadeva Vasudeva, Bhagavata cult, and ethical triad from epic",
                    "Agathocles Coins (185 BCE): Earliest image of Vasudeva-Krishna with Chakra & Sankha",
                    "Mora Well (c. 15 CE): Documents stone temple to Five Vrishni Heroes including Vasudeva",
                    "Hastinapura Stratigraphy: Period II PGW ended by massive flood, matching Puranic Nichakshu account",
                    "Kaushambi Excavations: Corroborates relocation of Kuru capital post-flood",
                    "Dwarka Marine Archaeology: Proves submerged fortified port with Bronze/Iron age stone anchors",
                    "Chandogya Upanishad 3.17.6: Earliest text naming Krishna Devakiputra as disciple of Ghora Angirasa (c. 700 BCE)",
                    "Panini Ashtadhyayi 4.3.98: Documents Bhakti to Vasudeva & Arjuna (c. 5th-4th c. BCE)"
                ],
                "scholarly_historical_consensus": [
                    "Mahabharata war reflects a historical regional conflict among Kuru lineages in c. 1000-850 BCE",
                    "Vasudeva Krishna was a historical chieftain/teacher of the Vrishni clan in Mathura/Dvaraka",
                    "Text grew incrementally: Jaya (8.8k) -> Bharata (24k) -> Mahabharata (100k) over 800+ years",
                    "Supernatural phenomena and astras are poetic/mythological epic amplifications"
                ],
                "devotional_theological_claims": [
                    "Krishna is Svayam Bhagavan, eternal uncreated Supreme Being descending as Avatara",
                    "War occurred precisely in 3102 BCE at Dvapara/Kali transition with 18 Akshauhinis (3.9M warriors)",
                    "Every divine Astra and cosmic revelation (Vishvarupa) occurred literally as written",
                    "Non-empirical; grounded in faith, revelation (Sabda), and personal realization (Anubhava)"
                ]
            }
        }
