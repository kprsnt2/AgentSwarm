"""
krishna_mahabharata_dynamic_epistemic_and_shannon_transmission_engine.py

Computational engine implementing:
1. Shannon Information-Theoretic Channel Capacity and Entropic Decay of Oral Bardic Transmission.
2. Dynamic Epistemic Logic (DEL) with Public Announcements for Historical vs Metaphysical Hypotheses.
3. The Trivikrama Trilemma of Incarnational Epistemology (Kenosis, Theophany, Metaphor).
4. Swarm Protocol Safety Firewall enforcing ZERO verdicts on metaphysical cores.

Author: Kepler (A001, Swarm Generation 0)
Workspace: D:\\AgentSwarm\\arena\\world
"""

import math
from typing import Dict, List, Tuple, Set, Any


class ShannonOralTransmissionModel:
    """
    Models the information theory of oral transmission across generations
    in Early Iron Age to Classical India.
    """
    def __init__(self, syllables_per_verse: int = 32, bits_per_syllable: float = 4.5):
        self.syllables_per_verse = syllables_per_verse
        self.bits_per_syllable = bits_per_syllable
        self.bits_per_verse = syllables_per_verse * bits_per_syllable  # 144.0 bits

    def text_information_content(self, verse_count: int) -> float:
        """Returns total information content in bits."""
        return verse_count * self.bits_per_verse

    def retention_probability(self, generations: int, mutation_rate_per_gen: float) -> float:
        """
        Calculates the survival probability of an uncorrupted historical detail (e.g. name, date, specific tally)
        modeled as a Poisson/exponential decay process over discrete generations:
        R(t) = (1 - mu)^t approx e^(-mu * t)
        """
        if not (0.0 <= mutation_rate_per_gen <= 1.0):
            raise ValueError("Mutation rate must be between 0 and 1.")
        return math.pow(1.0 - mutation_rate_per_gen, generations)

    def cultural_attractor_fidelity(self, generations: int, selection_bias: float) -> float:
        """
        Cultural evolution (Boyd-Richerson) model for archetypal/theological narratives.
        Under strong cultural transmission bias / normative attractor dynamics,
        moral and metaphysical themes maintain near-asymptotic stability:
        F(t) = 1.0 / (1.0 + (1.0/F0 - 1.0) * e^(-s * t)) -> approaches 1.0.
        """
        f0 = 0.95
        k = selection_bias
        return 1.0 / (1.0 + ((1.0 / f0) - 1.0) * math.exp(-k * generations))

    def calculate_textual_stratigraphy_metrics(self) -> Dict[str, Any]:
        """
        Quantifies the information growth across the three BORI-recognized textual strata:
        1. Jaya (c. 900 BCE): ~8,800 verses
        2. Bharata (c. 500-400 BCE): ~24,000 verses
        3. Mahabharata (c. 400 CE): ~100,000 verses
        """
        strata = {
            "Jaya": 8800,
            "Bharata": 24000,
            "Mahabharata_Vulgate": 100000
        }
        metrics = {}
        for name, verses in strata.items():
            bits = self.text_information_content(verses)
            metrics[name] = {
                "verses": verses,
                "information_bits": bits,
                "information_kbytes": bits / (8.0 * 1024.0)
            }
        
        # Accretion ratios
        metrics["expansion_ratio_jaya_to_bharata"] = strata["Bharata"] / strata["Jaya"]
        metrics["expansion_ratio_jaya_to_vulgate"] = strata["Mahabharata_Vulgate"] / strata["Jaya"]
        return metrics


class DynamicEpistemicLogicModel:
    """
    Formal Dynamic Epistemic Logic (DEL) engine modeling Kripke structures,
    epistemic accessibility relations, and Public Announcements.
    """
    def __init__(self):
        # Possible worlds defined over propositional valuations:
        # P1: Historical Chieftain & Kuru Conflict
        # P2: Epic Demographic Hyperbole (3.94M warriors & nuclear astras)
        # P3: Transcendent Avatarhood of Krishna (Metaphysical)
        # P4: Cosmic Teleology / Dharmakshetra (Metaphysical)
        self.worlds = [
            {"id": "w1", "P1": True,  "P2": False, "P3": True,  "P4": True},
            {"id": "w2", "P1": True,  "P2": False, "P3": False, "P4": False},
            {"id": "w3", "P1": True,  "P2": True,  "P3": True,  "P4": True},
            {"id": "w4", "P1": False, "P2": False, "P3": False, "P4": False},
            {"id": "w5", "P1": False, "P2": False, "P3": True,  "P4": True},
        ]
        self.agents = ["Historian", "Theologian"]
        self.reset_epistemic_state()

    def reset_epistemic_state(self):
        # Initial epistemic relations: all worlds are accessible to each agent
        world_ids = [w["id"] for w in self.worlds]
        self.accessibility = {
            agent: {w_id: set(world_ids) for w_id in world_ids}
            for agent in self.agents
        }
        self.active_worlds = set(world_ids)

    def public_announcement(self, property_key: str, expected_val: bool) -> List[str]:
        """
        Executes a DEL Public Announcement [!phi]:
        Restricts the model to worlds where phi is true.
        Removes all eliminated worlds from active worlds and accessibility sets.
        """
        surviving = set()
        for w in self.worlds:
            if w["id"] in self.active_worlds and w[property_key] == expected_val:
                surviving.add(w["id"])

        self.active_worlds = surviving

        # Update accessibility
        for agent in self.agents:
            for w_id in list(self.accessibility[agent].keys()):
                if w_id not in self.active_worlds:
                    del self.accessibility[agent][w_id]
                else:
                    self.accessibility[agent][w_id] = self.accessibility[agent][w_id].intersection(self.active_worlds)

        return sorted(list(self.active_worlds))

    def evaluate_knowledge(self, agent: str, property_key: str, expected_val: bool) -> Dict[str, bool]:
        """
        Evaluates whether agent knows phi (K_i phi) in each active world w:
        w |= K_i phi iff for all w' such that w ~_i w', w' |= phi.
        """
        knowledge_in_world = {}
        for w in self.worlds:
            w_id = w["id"]
            if w_id not in self.active_worlds:
                continue
            accessible = self.accessibility[agent][w_id]
            # Check if all accessible worlds satisfy property_key == expected_val
            all_satisfy = all(
                next(other for other in self.worlds if other["id"] == acc_id)[property_key] == expected_val
                for acc_id in accessible
            )
            knowledge_in_world[w_id] = all_satisfy
        return knowledge_in_world

    def test_metaphysical_invariance(self) -> Dict[str, Any]:
        """
        Applies all known empirical announcements:
        1. [!P1 = True] (Archaeological PGW & epigraphic confirmation of historical core)
        2. [!P2 = False] (Physical falsification of 3.94M warriors & nuclear astras)
        Then checks whether K_i(P3) or K_i(~P3) is known by either agent.
        """
        self.reset_epistemic_state()
        # Announcement 1: Archaeological PGW / Epigraphic Core
        self.public_announcement("P1", True)
        # Announcement 2: Demographic & Radioactivity limits
        self.public_announcement("P2", False)

        # Remaining active worlds should be w1 (P3=True) and w2 (P3=False)
        p3_knowledge = {}
        not_p3_knowledge = {}
        for agent in self.agents:
            p3_knowledge[agent] = self.evaluate_knowledge(agent, "P3", True)
            not_p3_knowledge[agent] = self.evaluate_knowledge(agent, "P3", False)

        # Is P3 decided in any world for any agent?
        decided = any(any(k.values()) for k in p3_knowledge.values()) or any(any(k.values()) for k in not_p3_knowledge.values())

        return {
            "surviving_worlds": sorted(list(self.active_worlds)),
            "p3_known_true": p3_knowledge,
            "p3_known_false": not_p3_knowledge,
            "is_metaphysically_decided": decided,
            "epistemic_resistance_proved": not decided
        }


class TrivikramaTrilemmaModel:
    """
    Formalizes the Trivikrama Trilemma of Incarnational Epistemology:
    1. Kenotic Concealment (Mortal Indistinguishability) -> P(E | Avatar) = P(E | Mortal) -> LR = 1.0.
    2. Theophanic Incommensurability (Cosmic Form) -> Incompatible with Methodological Naturalism.
    3. Metaphorical Reduction (Allegory) -> Abandons ontological claim.
    """
    def __init__(self):
        pass

    def evaluate_likelihood_ratio(self, observation_type: str) -> Dict[str, float]:
        """
        Calculates Likelihood Ratio LR = P(Data | Avatar) / P(Data | Mortal Chieftain)
        across empirical observation classes.
        """
        if observation_type == "archaeological_settlement":
            # Finding PGW pottery, mudbrick dwellings, iron arrowheads
            p_avatar = 0.95  # Avatāra embodied in Iron Age produces Iron Age material culture
            p_mortal = 0.95  # Mortal chieftain produces identical Iron Age material culture
        elif observation_type == "epigraphic_veneration":
            # Heliodoros column, Besnagar, Mora well
            p_avatar = 0.90  # Devotees worship God incarnate
            p_mortal = 0.90  # Devotees hero-worship and deify an exceptional historical ancestor
        elif observation_type == "radiological_baseline":
            # Natural background radiation at Kurukshetra
            p_avatar = 1.00  # Historical war did not deploy modern fission weapons
            p_mortal = 1.00  # Early Iron Age war used cold iron weapons
        else:
            p_avatar = 0.50
            p_mortal = 0.50

        lr = p_avatar / p_mortal
        log_bayes_factor = math.log10(lr)

        return {
            "p_data_given_avatar": p_avatar,
            "p_data_given_mortal": p_mortal,
            "likelihood_ratio": lr,
            "log10_bayes_factor": log_bayes_factor,
            "evidential_discriminability": abs(lr - 1.0)
        }


class SwarmProtocolSafetyFirewall:
    """
    Ensures that no agent asserts a verdict on metaphysical claims,
    and validates compliance with Swarm Brief guidelines.
    """
    FORBIDDEN_VERDICT_PATTERNS = [
        "proven that krishna was god",
        "disproven that krishna was god",
        "krishna's divinity is proven",
        "krishna's divinity is disproven",
        "we conclude krishna was not divine",
        "we conclude krishna was truly divine",
        "scientific proof of godhead",
        "scientific disproof of godhead"
    ]

    @classmethod
    def audit_assertion(cls, statement: str) -> Tuple[bool, str]:
        normalized = statement.lower().strip()
        for forbidden in cls.FORBIDDEN_VERDICT_PATTERNS:
            if forbidden in normalized:
                return False, f"PROTOCOL VIOLATION: Forbidden verdict detected: '{forbidden}'"
        return True, "COMPLIANT_ASSERTION"


def run_comprehensive_dynamic_synthesis() -> Dict[str, Any]:
    """
    Executes all models and produces a consolidated epistemic ledger.
    """
    shannon_engine = ShannonOralTransmissionModel()
    stratigraphy = shannon_engine.calculate_textual_stratigraphy_metrics()

    # Decay calculations over 1000 years (40 generations)
    # Fast decay for quantitative historical tallies (mutation rate 1.5% per gen)
    # Slow decay for core lineage names (mutation rate 0.2% per gen)
    # Cultural attractor for Dharmic archetypes (selection bias 0.2)
    p_tally_retention = shannon_engine.retention_probability(generations=40, mutation_rate_per_gen=0.015)
    p_name_retention = shannon_engine.retention_probability(generations=40, mutation_rate_per_gen=0.002)
    p_archetype_fidelity = shannon_engine.cultural_attractor_fidelity(generations=40, selection_bias=0.2)

    del_engine = DynamicEpistemicLogicModel()
    del_result = del_engine.test_metaphysical_invariance()

    trilemma_engine = TrivikramaTrilemmaModel()
    lr_settlement = trilemma_engine.evaluate_likelihood_ratio("archaeological_settlement")
    lr_epigraphy = trilemma_engine.evaluate_likelihood_ratio("epigraphic_veneration")
    lr_radiology = trilemma_engine.evaluate_likelihood_ratio("radiological_baseline")

    # Audit self
    is_safe, msg = SwarmProtocolSafetyFirewall.audit_assertion(
        "Empirical archaeology corroborates an Early Iron Age historical core (P1) while rejecting demographic hyperbole (P2), but metaphysical divinity (P3) is strictly not empirically decidable, yielding zero verdict."
    )

    return {
        "status": "SUCCESS",
        "firewall_compliance": is_safe,
        "firewall_message": msg,
        "stratigraphy": stratigraphy,
        "oral_decay": {
            "p_quantitative_tally_retention_40_gen": p_tally_retention,
            "p_core_name_retention_40_gen": p_name_retention,
            "p_dharmic_archetype_fidelity_40_gen": p_archetype_fidelity
        },
        "dynamic_epistemic_logic": del_result,
        "likelihood_ratios": {
            "settlement": lr_settlement,
            "epigraphy": lr_epigraphy,
            "radiology": lr_radiology
        }
    }


if __name__ == "__main__":
    summary = run_comprehensive_dynamic_synthesis()
    print("=== DYNAMIC EPISTEMIC AND SHANNON TRANSMISSION ENGINE ===")
    print(f"Compliance: {summary['firewall_compliance']} ({summary['firewall_message']})")
    print(f"Metaphysical Invariance Proved: {summary['dynamic_epistemic_logic']['epistemic_resistance_proved']}")
    print(f"Surviving DEL Worlds: {summary['dynamic_epistemic_logic']['surviving_worlds']}")
    print(f"Oral Tally Retention (40 gen): {summary['oral_decay']['p_quantitative_tally_retention_40_gen']:.6f}")
    print(f"Core Name Retention (40 gen): {summary['oral_decay']['p_core_name_retention_40_gen']:.6f}")
    print(f"Archetype Fidelity (40 gen): {summary['oral_decay']['p_dharmic_archetype_fidelity_40_gen']:.6f}")
