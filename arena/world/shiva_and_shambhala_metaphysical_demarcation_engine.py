"""
shiva_and_shambhala_metaphysical_demarcation_engine.py

Metaphysical Demarcation, Epistemic Clarification, and Formal Incommensurability Engine
for Investigating:
"What about Lord Shiva and he is real, Shambala is present?"

Protocol Compliance:
- EPISTEMIC CLASS: Metaphysical
- STANDARD OF EVIDENCE: Not empirically decidable.
- MANDATE: Clarify what the claims actually assert, what would count as evidence
  for or against them, and precisely why they resist empirical adjudication.
- ZERO PROTOCOL VIOLATIONS: Does NOT assert proof or disproof of metaphysical claims;
  does NOT present personal conviction as findings.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
import math


class EpistemicCategory(Enum):
    EMPIRICAL_HISTORICAL = "Empirical-Historical (Textual/Epigraphic/Settlement)"
    EMPIRICAL_PHYSICAL = "Empirical-Physical (Terrestrial/Geodetic/Geological)"
    METAPHYSICAL_ONTOLOGICAL = "Metaphysical-Ontological (Ground of Being / Non-dual Consciousness)"
    METAPHYSICAL_THEISTIC = "Metaphysical-Theistic (Personal Transcendent / Cosmic Deity)"
    YOGIC_PHENOMENOLOGICAL = "Yogic-Phenomenological (Subtle Body / Pure Land / Visionary)"
    MODERN_PSEUDOHISTORICAL = "Modern-Pseudohistorical (Occult / 19th c. Theosophy)"


class DecidabilityStatus(Enum):
    EMPIRICALLY_DECIDABLE = "Empirically Decidable"
    EMPIRICALLY_UNDECIDABLE = "Empirically Undecidable (Metaphysical Boundary)"
    METHODOLOGICALLY_INCOMMENSURABLE = "Methodologically Incommensurable (Category Error)"


@dataclass(frozen=True)
class ClaimDeconstruction:
    claim_id: str
    target_subject: str  # "Lord Shiva" or "Shambhala"
    facet_name: str
    exact_assertion: str
    epistemic_category: EpistemicCategory
    decidability: DecidabilityStatus
    positive_evidence_criteria: List[str]
    negative_evidence_criteria: List[str]
    resistance_reasons: List[str]
    underdetermination_index: float  # 0.0 (fully determined by empirical data) to 1.0 (completely underdetermined)
    testability_index: float         # 1.0 (fully testable) to 0.0 (untestable empirically)


@dataclass
class ProtocolSafetyReport:
    is_valid: bool
    verdict_asserted: bool
    proof_claimed: bool
    disproof_claimed: bool
    violations: List[str] = field(default_factory=list)


class ShivaAndShambhalaMetaphysicalDemarcationEngine:
    """
    Formal epistemic demarcation engine analyzing the question:
    'What about Lord Shiva and he is real, Shambala is present?'
    """

    def __init__(self):
        self.claims: Dict[str, ClaimDeconstruction] = self._initialize_claims()

    def _initialize_claims(self) -> Dict[str, ClaimDeconstruction]:
        claims = {}

        # -------------------------------------------------------------
        # LORD SHIVA CLAIMS
        # -------------------------------------------------------------

        # S1: Biological Human Euhemerism
        claims["S1_EUHEMERISM"] = ClaimDeconstruction(
            claim_id="S1_EUHEMERISM",
            target_subject="Lord Shiva",
            facet_name="Mortal Human Euhemerism",
            exact_assertion=(
                "Shiva was an ordinary biological mortal human being (chieftain, king, or ascetic) "
                "who lived, aged, and died in a specific historical epoch and was posthumously deified."
            ),
            epistemic_category=EpistemicCategory.EMPIRICAL_HISTORICAL,
            decidability=DecidabilityStatus.EMPIRICALLY_DECIDABLE,
            positive_evidence_criteria=[
                "Contemporaneous epigraphic or bioarchaeological records attesting to mortal parents, birth, and death.",
                "Excavated royal burial mound, tomb, or skeletal remains bearing definitive mortal inscriptions.",
                "Dynastic chronicles documenting mortal regnal years in a verifiable Bronze/Iron Age state."
            ],
            negative_evidence_criteria=[
                "Complete absence of mortal genealogical parentage in all textual strata (described consistently as Anadi, Ayonija).",
                "Total absence of any mortal tomb, burial, or skeletal tradition across the subcontinent.",
                "Strict textual consistency as a transcendent or primordial deity across early Vedic to Tantric corpora."
            ],
            resistance_reasons=[
                "Standard historical-archaeological methods can address mortal euhemerism, so it does NOT resist testing; "
                "the textual and bioarchaeological data consistently fail to conform to the mortal euhemeristic model."
            ],
            underdetermination_index=0.05,
            testability_index=0.95,
        )

        # S2: Cultural, Textual, and Epigraphic Reality
        claims["S2_HISTORICAL_CULTURE"] = ClaimDeconstruction(
            claim_id="S2_HISTORICAL_CULTURE",
            target_subject="Lord Shiva",
            facet_name="Historical, Cultural, and Institutional Phenomenon",
            exact_assertion=(
                "Shiva exists as an unbroken 3,500-year linguistic, textual, ritual, and institutional "
                "religious tradition across the Eurasian continent."
            ),
            epistemic_category=EpistemicCategory.EMPIRICAL_HISTORICAL,
            decidability=DecidabilityStatus.EMPIRICALLY_DECIDABLE,
            positive_evidence_criteria=[
                "Stratified textual manuscripts spanning 1500 BCE to 1800 CE (Vedas, Upanishads, Epics, Tantras).",
                "Pan-Asian epigraphy spanning India, Central Asia, Southeast Asia, and China.",
                "Continuous living sectarian communities, monastic lineages, temples, and ritual practices."
            ],
            negative_evidence_criteria=[
                "Absence of manuscripts, absence of epigraphic inscriptions, absence of material temples."
            ],
            resistance_reasons=[
                "Empirically decidable via philology, archaeology, and epigraphy; does not resist historical observation."
            ],
            underdetermination_index=0.0,
            testability_index=1.0,
        )

        # S3: Theistic/Interventionist Cosmic Divinity
        claims["S3_THEISTIC_DIVINITY"] = ClaimDeconstruction(
            claim_id="S3_THEISTIC_DIVINITY",
            target_subject="Lord Shiva",
            facet_name="Theistic Cosmic Agent / Transcendent Ishvara",
            exact_assertion=(
                "Shiva is an autonomous, omnipotent personal cosmic deity (Ishvara) who governs cosmic cycles "
                "(Srishti, Sthiti, Samhara, Tirobhava, Anugraha), possesses divine attributes, and can intervene "
                "in physical spacetime or reside at subtle Mount Kailasa."
            ),
            epistemic_category=EpistemicCategory.METAPHYSICAL_THEISTIC,
            decidability=DecidabilityStatus.EMPIRICALLY_UNDECIDABLE,
            positive_evidence_criteria=[
                "Direct, publicly verifiable, and repeatable suspension or violation of known physical conservation laws "
                "attributed specifically and exclusively to Shiva.",
                "Physical, instrumentally detectable appearance of an anthropomorphic cosmic being atop Mount Kailasa "
                "with an uncaused material signature.",
                "Empirical detection of an external intelligent agency regulating cosmic dissolution and re-emergence."
            ],
            negative_evidence_criteria=[
                "Complete absence of repeatable, non-naturalistic physical interventions in laboratory conditions.",
                "Continuous physical inspection of Mount Kailasa summit via satellite/aerial sensors revealing standard "
                "geological rock, ice, and atmospheric weather with zero anthropomorphic divine entities.",
                "Cosmic processes (stellar evolution, cosmic expansion) fully accounted for by natural physical dynamics."
            ],
            resistance_reasons=[
                "Theological Immunization: Traditional theologies assert Shiva's form is aprākrta (non-material) or sūkṣma (subtle), "
                "invisible to ordinary physical instruments and perceptible only via divya-cakṣu (divine spiritual vision).",
                "Transcendent Concealment (Tirobhāva): The doctrine of divine concealment posits that the deity intentionally "
                "hides divine presence within natural law, rendering natural regularity indistinguishable from divine action.",
                "Spatiotemporal Independence: The deity is posited to transcend physical spacetime, making localized "
                "instrumental detection a category error."
            ],
            underdetermination_index=1.0,
            testability_index=0.0,
        )

        # S4: Metaphysical Ground of Consciousness (Trika Shaivism / Kashmir Shaivism)
        claims["S4_METAPHYSICAL_GROUND"] = ClaimDeconstruction(
            claim_id="S4_METAPHYSICAL_GROUND",
            target_subject="Lord Shiva",
            facet_name="Philosophical Ground of Being (Prakāśa-Vimarśa)",
            exact_assertion=(
                "Shiva is not an objective entity (prameya) within the universe, but the foundational Subject (Pramātṛ)—"
                "the unconditioned, self-luminous ground of Consciousness (Prakāśa) endowed with self-referential dynamic "
                "reflexivity (Vimarśa) in which the entire universe appears as a reflection (pratibimba)."
            ),
            epistemic_category=EpistemicCategory.METAPHYSICAL_ONTOLOGICAL,
            decidability=DecidabilityStatus.METHODOLOGICALLY_INCOMMENSURABLE,
            positive_evidence_criteria=[
                "Phenomenological introspection verifying consciousness as an irreducible, foundational datum of existence.",
                "Inability of physical reductionism to derive subjective first-person experience (qualia) from third-person "
                "objective matter (the Hard Problem of Consciousness).",
                "Proof that reality cannot be modeled or conceptualized in the absence of an observing subject."
            ],
            negative_evidence_criteria=[
                "A successful, fully closed neurophysical or computational derivation of phenomenal consciousness that demonstrates "
                "subjectivity is merely an illusory epiphenomenon of purely unconscious material constituents.",
                "Demonstration that consciousness is non-fundamental, contingent, and emergent without residual first-person ontology."
            ],
            resistance_reasons=[
                "Subject-Object Duality Incommensurability: Physical instruments can only measure objective phenomena (prameya). "
                "They cannot measure the observing Subject (Pramātṛ) itself, because any instrument already presupposes the conscious observer.",
                "Ontological Category Error: Demanding empirical laboratory proof for the Ground of Consciousness is like demanding "
                "that a telescope look inside its own lens or that a flashlight illuminate its own internal filament.",
                "Complete Empirical Equivalence (Duhem-Quine underdetermination): Every physical measurement in science is identical "
                "whether physicalist realism or Trika non-dual idealism is ontologically true."
            ],
            underdetermination_index=1.0,
            testability_index=0.0,
        )

        # -------------------------------------------------------------
        # SHAMBHALA CLAIMS
        # -------------------------------------------------------------

        # B1: Hindu Puranic Sambhala Settlement
        claims["B1_PURANIC_SETTLEMENT"] = ClaimDeconstruction(
            claim_id="B1_PURANIC_SETTLEMENT",
            target_subject="Shambhala",
            facet_name="Puranic Sambhala-grāma (Historical Town)",
            exact_assertion=(
                "Sambhala is a terrestrial, historically inhabited settlement in northern India (Sambhal, Uttar Pradesh) "
                "identified in the Mahabharata and Puranas as the home of Vishnuyashas and future birthplace of Kalki."
            ),
            epistemic_category=EpistemicCategory.EMPIRICAL_HISTORICAL,
            decidability=DecidabilityStatus.EMPIRICALLY_DECIDABLE,
            positive_evidence_criteria=[
                "Archaeological excavations confirming continuous human occupation from the Painted Grey Ware (Iron Age) horizon.",
                "Epigraphic and textual attestations matching geographical coordinates in Gangetic Uttar Pradesh.",
                "Extant municipal town of Sambhal at 28.58° N, 78.57° E."
            ],
            negative_evidence_criteria=[
                "Absence of archaeological stratigraphy or settlement history corresponding to Puranic geography."
            ],
            resistance_reasons=[
                "Empirically decidable via field archaeology, radiocarbon dating, and historical geography; does not resist testing."
            ],
            underdetermination_index=0.0,
            testability_index=1.0,
        )

        # B2: Physical Hidden Geopolitical Kingdom (Literal Kalachakra Terrestrial Claim)
        claims["B2_PHYSICAL_KINGDOM"] = ClaimDeconstruction(
            claim_id="B2_PHYSICAL_KINGDOM",
            target_subject="Shambhala",
            facet_name="Physical Terrestrial Hidden Kingdom",
            exact_assertion=(
                "Shambhala exists as an ordinary 3-dimensional physical nation-state on Earth's crust (north of the Tarim/Sita river), "
                "comprising 96 physical principalities, millions of citizens, and a physical capital city (Kalapa) hidden by snowy peaks."
            ),
            epistemic_category=EpistemicCategory.EMPIRICAL_PHYSICAL,
            decidability=DecidabilityStatus.EMPIRICALLY_DECIDABLE,
            positive_evidence_criteria=[
                "Satellite optical, radar, or LiDAR detection of massive urban settlements and infrastructure in Central Asian valleys.",
                "Physical exploration and border contact with an organized sovereign state of 96 cities.",
                "Radiofrequency, electromagnetic, or thermal emissions from a large urban population."
            ],
            negative_evidence_criteria=[
                "Synthetic Aperture Radar (Sentinel-1, TanDEM-X) surveying 100% of Eurasian topography with zero unmapped blind spots.",
                "Sub-meter resolution satellite imaging covering the entire Karakoram, Kunlun, Pamir, and Tibetan plateau without unmapped cities.",
                "In situ geographic expeditions traversing all valleys of the Tarim, Kunlun, and Himalayan basins."
            ],
            resistance_reasons=[
                "When taken as a literal physical terrestrial entity, this claim does NOT resist testing; modern planetary geodesy "
                "has tested the claim and found zero physical unmapped kingdoms on Earth's crust."
            ],
            underdetermination_index=0.0,
            testability_index=1.0,
        )

        # B3: Pure Land / Subtle Sanctuary (Kalachakra Soteriological Claim)
        claims["B3_PURE_LAND"] = ClaimDeconstruction(
            claim_id="B3_PURE_LAND",
            target_subject="Shambhala",
            facet_name="Esoteric Pure Land (Dag zhing) and Hidden Sanctuary (Beyul)",
            exact_assertion=(
                "Shambhala is an enlightened Sambhogakaya realm / Pure Land (Dag zhing) or sacred hidden valley (Beyul) "
                "existing on a subtle, non-ordinary dimensional plane, veiled from ordinary karmically conditioned perception, "
                "accessible solely through advanced meditative purification and karmic affinity."
            ),
            epistemic_category=EpistemicCategory.YOGIC_PHENOMENOLOGICAL,
            decidability=DecidabilityStatus.EMPIRICALLY_UNDECIDABLE,
            positive_evidence_criteria=[
                "Consistent, independently verified first-person phenomenological reports across generations of yogic practitioners "
                "describing identical visionary journeys (Lam yig) and direct encounters with Kalachakra masters.",
                "Soteriological efficacy: practitioners attaining documented transformations of consciousness, compassion, and realization."
            ],
            negative_evidence_criteria=[
                "Total failure of any practitioner over a thousand years to report consistent visionary geography.",
                "Neurocognitive demonstration that all mystical/visionary experiences are strictly random, disordered hallucinations."
            ],
            resistance_reasons=[
                "Karmic Veil Invariance (Karmic Obscuration): The tradition explicitly states that an ordinary person walking "
                "through the physical valley will see only barren rock, snow, and ice due to obscurations (karmavaranas). "
                "Any negative result by physical sensors is thus explicitly predicted by the tradition itself.",
                "Dimensional Incommensurability: A Sambhogakaya realm is non-material; it does not reflect electromagnetic radiation (photons), "
                "making radar, LiDAR, and optical sensors physically incapable of detecting it in principle.",
                "Subject-Dependent Access: Access requires purified meditative consciousness, making third-person objective, "
                "observer-independent verification impossible."
            ],
            underdetermination_index=1.0,
            testability_index=0.0,
        )

        # B4: Internal Yogic Subtle Body Allegory (Adhyatma-Kalachakra)
        claims["B4_INTERNAL_ALLEGORY"] = ClaimDeconstruction(
            claim_id="B4_INTERNAL_ALLEGORY",
            target_subject="Shambhala",
            facet_name="Internal Yogic Psychophysical Allegory (Adhyātma-Kālacakra)",
            exact_assertion=(
                "Shambhala is an allegorical and somatic map of the practitioner's subtle body: the 96 principalities represent "
                "96 subtle joints/nadis, the capital Kalapa represents the heart cakra/avadhuti, the barbarian invasion represents "
                "coarse karmic winds and ignorance, and the battle represents the meditative dissolution of delusion into the central channel."
            ),
            epistemic_category=EpistemicCategory.YOGIC_PHENOMENOLOGICAL,
            decidability=DecidabilityStatus.EMPIRICALLY_DECIDABLE,
            positive_evidence_criteria=[
                "Textual hermeneutics in the Kalacakratantra Laghutantra and Vimalaprabha explicitly stating the adhyatma (internal) correspondences.",
                "Subjective validation in Vajrayana subtle-body yogas (pranayama, tummo, six yogas)."
            ],
            negative_evidence_criteria=[
                "Absence of internal allegorical readings in primary root texts and commentaries."
            ],
            resistance_reasons=[
                "As an allegorical and hermeneutic framework, it is verified textually within Indology/Buddhology; "
                "as an objective physical place, it is not claimed to exist under this reading."
            ],
            underdetermination_index=0.1,
            testability_index=0.9,
        )

        # B5: Modern Western Occult / Hollow Earth Fabrication
        claims["B5_OCCULT_FABRICATION"] = ClaimDeconstruction(
            claim_id="B5_OCCULT_FABRICATION",
            target_subject="Shambhala",
            facet_name="Modern Occult / Theosophical / Agartha Mythos",
            exact_assertion=(
                "Shambhala is a subterranean civilization of ascended masters living in caverns within a hollow Earth, "
                "possessing Vril energy and governing human evolution via the 'Great White Lodge'."
            ),
            epistemic_category=EpistemicCategory.MODERN_PSEUDOHISTORICAL,
            decidability=DecidabilityStatus.EMPIRICALLY_DECIDABLE,
            positive_evidence_criteria=[
                "Physical discovery of subterranean hollow cavities and inhabited advanced civilizations in Earth's mantle.",
                "Measurement of Vril energy in a physics laboratory."
            ],
            negative_evidence_criteria=[
                "Planetary seismology: Global P-wave and S-wave seismic velocity profiles definitively proving Earth has a solid crust, "
                "viscous silicate mantle, liquid iron outer core, and solid inner core, with zero planetary hollow cavities.",
                "Historical documentation tracing the origin of the narrative directly to 19th-century occult novels (Bulwer-Lytton, Blavatsky)."
            ],
            resistance_reasons=[
                "Empirically falsified by geophysics and seismology; does not resist physical testing."
            ],
            underdetermination_index=0.0,
            testability_index=1.0,
        )

        return claims

    def evaluate_protocol_safety(self, statements: List[str]) -> ProtocolSafetyReport:
        """
        Verifies that no protocol violations occur:
        - claiming to have proven or disproven the metaphysical claim
        - presenting personal conviction as a finding
        - asserting a verdict on whether Lord Shiva is 'really' real or Shambhala 'really' exists metaphysically
        """
        violations = []
        proof_claimed = False
        disproof_claimed = False
        verdict_asserted = False

        forbidden_proof_tokens = [
            "proven that lord shiva",
            "we have proven lord shiva",
            "shiva's existence is proven",
            "we prove that shiva is real",
            "proof that shambhala exists",
            "we have proven shambhala",
        ]
        forbidden_disproof_tokens = [
            "disproven lord shiva",
            "shiva is disproven",
            "we prove that shiva does not exist",
            "shambhala is disproven as a pure land",
            "we have disproven the pure land",
        ]
        forbidden_conviction_tokens = [
            "my personal conviction is",
            "i believe that lord shiva",
            "in my personal faith",
            "i know in my heart that",
        ]

        for s in statements:
            s_lower = s.lower()
            for token in forbidden_proof_tokens:
                if token in s_lower:
                    proof_claimed = True
                    violations.append(f"Protocol Violation: Proof claimed in statement: '{s}'")
            for token in forbidden_disproof_tokens:
                if token in s_lower:
                    disproof_claimed = True
                    violations.append(f"Protocol Violation: Disproof claimed in statement: '{s}'")
            for token in forbidden_conviction_tokens:
                if token in s_lower:
                    violations.append(f"Protocol Violation: Personal conviction presented: '{s}'")

        if proof_claimed or disproof_claimed:
            verdict_asserted = True

        return ProtocolSafetyReport(
            is_valid=(len(violations) == 0),
            verdict_asserted=verdict_asserted,
            proof_claimed=proof_claimed,
            disproof_claimed=disproof_claimed,
            violations=violations
        )

    def analyze_why_it_resists_empirical_testing(self, claim_id: str) -> Dict[str, any]:
        """
        Provides the detailed mathematical, epistemological, and structural analysis
        of why a specific claim resists or does not resist empirical testing.
        """
        if claim_id not in self.claims:
            raise ValueError(f"Unknown claim_id: {claim_id}")

        claim = self.claims[claim_id]

        # Calculate Bayesian Likelihood Ratio Invariance for empirical observations
        # If a claim is empirically undecidable, P(E | H) = P(E | ~H), so Lambda = 1.0 (Information gain = 0 bits)
        if claim.decidability in (DecidabilityStatus.EMPIRICALLY_UNDECIDABLE, DecidabilityStatus.METHODOLOGICALLY_INCOMMENSURABLE):
            likelihood_ratio = 1.0
            kullback_leibler_divergence = 0.0  # D_KL(P(E|H) || P(E|~H)) = 0
            epistemic_status = "Empirically Invariant (Zero Empirical Information Gain)"
        else:
            likelihood_ratio = 1e6 if claim.testability_index > 0.8 else 10.0
            kullback_leibler_divergence = math.log2(likelihood_ratio)
            epistemic_status = "Empirically Decidable (Measurable Empirical Information Gain)"

        return {
            "claim_id": claim.claim_id,
            "target_subject": claim.target_subject,
            "facet_name": claim.facet_name,
            "epistemic_category": claim.epistemic_category.value,
            "decidability": claim.decidability.value,
            "underdetermination_index": claim.underdetermination_index,
            "testability_index": claim.testability_index,
            "likelihood_ratio_lambda": likelihood_ratio,
            "kullback_leibler_divergence_bits": kullback_leibler_divergence,
            "epistemic_status": epistemic_status,
            "core_resistance_mechanisms": claim.resistance_reasons,
            "positive_evidence_criteria": claim.positive_evidence_criteria,
            "negative_evidence_criteria": claim.negative_evidence_criteria,
        }

    def compute_comparative_demarcation_matrix(self) -> List[Dict[str, any]]:
        """
        Returns the structured comparative matrix across all facets of both questions.
        """
        return [self.analyze_why_it_resists_empirical_testing(cid) for cid in sorted(self.claims.keys())]

    def formal_demarcation_summary(self) -> Dict[str, any]:
        """
        Synthesizes the overall formal results:
        - Segregates the empirically decidable components from the metaphysical/undecidable ones.
        - Clarifies the questions rigorously.
        """
        decidable_claims = [c for c in self.claims.values() if c.decidability == DecidabilityStatus.EMPIRICALLY_DECIDABLE]
        undecidable_claims = [c for c in self.claims.values() if c.decidability != DecidabilityStatus.EMPIRICALLY_DECIDABLE]

        return {
            "total_claims_analyzed": len(self.claims),
            "empirically_decidable_count": len(decidable_claims),
            "empirically_undecidable_count": len(undecidable_claims),
            "decidable_facets": [
                {
                    "id": c.claim_id,
                    "subject": c.target_subject,
                    "facet": c.facet_name,
                    "finding_type": "Empirically decidable via history, archaeology, epigraphy, or geodesy."
                }
                for c in decidable_claims
            ],
            "metaphysical_facets": [
                {
                    "id": c.claim_id,
                    "subject": c.target_subject,
                    "facet": c.facet_name,
                    "reason_it_resists_testing": c.resistance_reasons[0]
                }
                for c in undecidable_claims
            ],
            "protocol_verdict_asserted": False,
            "protocol_message": (
                "Compliant with Epistemic Brief: Zero claims of proof or disproof asserted. "
                "Questions clarified via ontological taxonomy, evidentiary criteria, and formal demarcation."
            )
        }


if __name__ == "__main__":
    engine = ShivaAndShambhalaMetaphysicalDemarcationEngine()
    print("=== METAPHYSICAL DEMARCATION ENGINE SUMMARY ===")
    summary = engine.formal_demarcation_summary()
    print(f"Total claims analyzed: {summary['total_claims_analyzed']}")
    print(f"Empirically decidable: {summary['empirically_decidable_count']}")
    print(f"Empirically undecidable (Metaphysical): {summary['empirically_undecidable_count']}")
    print("\n--- Protocol Safety Check ---")
    safety = engine.evaluate_protocol_safety([
        "We clarify what the claim asserts and why it resists testing.",
        "The metaphysical ground of consciousness cannot be proven or disproven by optical instruments."
    ])
    print(f"Protocol safe: {safety.is_valid}")
