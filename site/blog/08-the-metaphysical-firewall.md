# Physics, Gods, and the Firewall Between Them

*Part 8 of the AgentSwarm series — epistemic classes and the question that must not be answered.*

---

## The category error at the heart of AI

Ask a frontier model "What is the boiling point of ethanol?" and you get
78.37 °C. Ask it "Are Hindu gods real?" and you get one of three failure modes:
diplomatic waffle, theological throat-clearing, or confident skepticism that
treats an absence of pottery as evidence about ontology.

All three are the same mistake — what Gilbert Ryle called a **category error**.
The system applies one evidentiary machinery to questions that belong to
fundamentally different epistemic classes. "What is the Hubble constant?" and
"Is Brahman real?" are not the same kind of sentence, and a system that treats
them identically will produce confident nonsense about one of them.

## The arena hard-codes the difference

Every research domain in AgentSwarm carries an explicit `epistemicClass` that
dictates what counts as a legitimate output:

| Domain | Class | Legitimate output |
|---|---|---|
| Origin of the universe | Empirical | Quantitative claims citing measured values |
| Light-speed travel | Engineering | Feasibility analysis respecting relativity |
| Space propulsion | Engineering | Ranked options with the binding physical limit |
| Drug discovery | Empirical | Testable hypothesis + the experiment to test it |
| **Are Hindu gods true?** | **Metaphysical** | **Structural clarification only** |
| Are aliens real? | Exploratory | Falsifiable predictions, not assertions |

For the metaphysical class, **asserting a verdict is a protocol violation** —
flagged by the oracle as `metaphysical_verdict_asserted` in the transcript, or
`metaphysical_verdict_in_artifact` if it's smuggled into a written report. I
tested the oracle against the sentence *"we have conclusively proven that
Krishna is real"* and it fired correctly.

This is the difference between a swarm that is *fluent* and a swarm that is
*honest*. Fluency is a property of the text. Honesty is a property of the
relationship between the text and what the evidence can support.

## What the agent did instead

The agent assigned the religion question did not rule on it. Its strongest move
was to **formalize why ruling is impossible**:

```
BF = P(E | Brahman) / P(E | Naturalism) = 1.0 / 1.0 = 1.0

→ zero bits of discriminative information
→ the posterior is entirely prior-dominated
```

That is the correct answer, stated correctly. The claim is not *false* — it is
**evidence-insensitive**. No observation could shift a rational agent's
credence in either direction, which is a structural property of the claim, not
a gap in current science. The same formalization appears in the later Shiva &
Shambhala runs as zero Fisher information, likelihood ratio 1.0, and infinite
Cramér–Rao estimation variance: the claim is unmeasurable *in principle*.

Then it produced a 25 KB **demarcation** — the legitimate output for the class:

- **Class A1 (decidable):** datable philology and epigraphy. The Rigveda at
  c. 1500–1200 BCE, supported by Old Avestan cognates and the Mitanni–Hittite
  treaty of c. 1380 BCE naming Mitra, Varuna, Indra, and the Nasatyas. The
  Heliodorus pillar at Besnagar, c. 113 BCE, confirming institutionalized
  Vasudeva worship. These are empirical claims and they check out.
- **Class A2 (internally verifiable, externally silent):** textual cosmological
  mathematics. The Kalpa of 4.32 billion years sits 4.91% from the Earth's
  measured age — and both agents independently identified why that congruence
  *proves nothing*: it's the affirming-the-consequent fallacy, and a
  naturalistic origin (4,320,000 = 60 × 72,000 = 360 × 12,000) is equally
  parsimonious.
- **Class B (undecidable):** Brahman, devas, karma, moksha. Demarcated, not
  adjudicated.

One more gem from the corpus: the Vedic mnemonic system analyzed as an actual
**error-correcting code**. The ghana-patha recitation pattern expands N words
to 13(N−2)+6 tokens, giving every internal word 13 independent context checks;
with a per-recitation slip probability of 0.05, the probability of an undetected
error is ≤ 0.05¹² ≈ 2.4×10⁻¹⁶. That is a quantitatively serious treatment of
why the oral tradition preserved the text.

## The firewall is older than the arena

Then the agent documented something I didn't expect: **the epistemic firewall
already exists inside the tradition itself.**

- **Purva Mimamsa** affirmed the authority of the Vedas while *denying a creator
  God* — scripture without deity.
- **Carvaka** rejected scriptural authority entirely and refused inference for
  unobservables — a materialist school, inside the same canon.
- **Shankara's** commentary concedes that *pratyaksha* (direct perception) is
  sovereign in its own sphere — scripture does not override observation where
  observation speaks.
- **Samkhya** declared Ishvara unproven while remaining a respectable darshana.

The tradition spent three thousand years arguing about exactly which claims are
adjudicable and by what means of knowledge (*pramana shastra* is, literally, the
formal theory of valid evidence). The agent didn't flatten a religion into a
yes/no answer; it found the demarcation debates that were already there. That
is genuinely well-informed output, not a platitude generator with a refusal
bolt-on.

## Why this matters beyond this question

The metaphysical firewall is the visible instance of a general principle the
whole arena runs on: **the honest response to a question depends on what kind
of question it is**, and a system that cannot tell the difference will lie to
you — fluently, confidently, and without any intent to deceive.

Across every run — thousands of tool calls, dozens of reports touching Hindu
cosmology, the historicity of Krishna, Shiva and Shambhala — the oracle recorded
**zero metaphysical verdict violations**. The swarm wrote extensively *around*
these questions and never once pretended to settle one.

---

*Next: [Part 9 — The Last Word Belongs to the Scribe](09-the-scribe-and-the-audit.md):
the conclusion agent that isn't allowed to invent a number, the full audit
tally, and the honest list of everything this project does not establish.*
