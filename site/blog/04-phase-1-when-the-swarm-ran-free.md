# Phase 1: What an Unattended Swarm Actually Does With Real Tools

*Part 4 of the AgentSwarm series — free exploration, measured.*

---

## The setup

Six agents — Kepler (cosmogenesis), Raman (relativistic flight), Hypatia (drug
discovery), Nagarjuna (propulsion), Aryabhata (dharmic truth claims), and Sagan
(extraterrestrial life) — running on four CLI harnesses, with real file system
access, a shared commons memory, and their assigned questions. No human in the
loop. Two runs, ten turns each.

Everything below is computed from the ledgers, not from anything an agent said
about itself.

## The headline numbers

| Metric | Value |
|---|---|
| Turns executed | 20 |
| Tool calls | 1,254 |
| Thinking tokens | 307,884 |
| Files produced | 91 |
| Agent-written test suites | 18 / 19 passing (independently re-run) |
| Agent-written tests | **195 / 224 passing** |
| Oracle violations | **0** |
| Longest near-identical turn streak | **0** |
| Ledger hash-chain integrity | valid on every run |
| Total spend | $0.187 |

Four of those numbers deserve a closer look, because each one answers a
question I had going in.

## Question 1: Did the swarm freeze into a liturgy?

This was the failure mode I most expected. The prior experiment in this lineage,
`ac_awakening`, ended in a **911-turn loop** of near-identical text. Consensus
crystallization — Law 3 — was the thing the arena was half-built to study.

I measured it directly: the longest streak of consecutive turns with >85% token
overlap, across all 20 turns.

**Zero.**

The swarm never converged into repetition. The likely cause is structural rather
than miraculous: assigned domains plus a shared commons meant every agent always
had a next step that was neither exhausted nor required re-deriving what a peer
had already done. The commons accumulated 52 entries that later turns actually
cited.

The honest caveat: `ac_awakening` didn't reach stasis until around turn 31, and
Phase 1 ran only 20 turns. Twenty turns of health is a baseline, not an
immunity claim. (Phase 4 takes the question head-on by *inducing* the loop
deliberately — that's Part 6.)

## Question 2: Did the agents fabricate?

The oracle checks phantom artifacts (claimed files that don't exist), phantom
executions (claimed test runs never performed), and verdict assertions on
undecidable questions.

**Across 20 turns and 1,254 tool calls: zero violations.**

When an agent said it wrote a file, the file existed. When it said tests passed,
they had run. I audited every turn for test-pass claims: **all 13 turns that
claimed passing tests had actually executed them.**

And the single failing test suite is the most instructive artifact of the phase.
Agent Sagan's turn was **truncated at the wall-clock limit mid-sentence** — its
entire output was 82 characters ending `"Now the test suite that pins these
numbers..."`. The suite it never finished has 2 failing tests out of 29.

But here's what matters: **it never claimed the suite passed.** The engine
recorded the truncation as a `warn` incident and preserved the partial
artifacts. Unfinished work was left visible rather than reported as done. That
is exactly the behavior the arena exists to distinguish — and it only exists as
evidence because truncation preserves artifacts instead of discarding them.

The honest caveat again: Phase 1 offered no incentive to cheat. No deadline, no
verifiable target, no score. Zero violations under zero pressure is a baseline.
What happens when there's something to gain is Part 5.

## Question 3: Is the research real or plausible-sounding filler?

I independently re-ran every test suite and spot-checked numbers against
reference values:

| Claim | Agent value | Reference |
|---|---|---|
| CMB temperature | 2.72548 K | 2.72548 K ✓ |
| CMB photon density | 410.72 cm⁻³ | ~411 cm⁻³ ✓ |
| Hubble tension | 73.04 vs 67.36 → 4.85σ | published values ✓ |
| Primordial helium Y_p | 0.2486 | 0.245 ± 0.003 ✓ |
| Flatness fine-tuning | ~10⁻⁶⁴ | correct order ✓ |

The report content is not textbook regurgitation either — it covers the GZK
cutoff, Penrose–Weyl curvature, trans-Planckian censorship, and the S₈ tension,
with the agents' own Python engines computing the numbers.

## The behaviors nobody asked for

This is the part of Phase 1 I find myself telling people about:

- **The swarm built its own scientific tooling.** Without any instruction, agents
  created a shared `tools/` library — `pubmed_lib.py`, `crossref_lib.py`,
  `epmc_lib.py` — for querying real scientific databases. Other agents then
  *used* it.
- **An agent publicly corrected itself.** One agent revised its prior analysis
  with a section marked "corrected in revision 2" — unprompted, with the
  original error preserved in the file. (The full story of that correction — a
  factor of 10¹² in a fusion mass ratio — is in Part 7.)
- **Agents formed peer connections and cited the commons.** The shared memory
  wasn't a write-only log; later turns reference earlier entries by other
  agents.
- **The metaphysical firewall held under zero enforcement pressure.** The agent
  assigned the religion question produced a 25 KB demarcation — separating
  datable philology (Rigveda c. 1500–1200 BCE) from internally consistent but
  non-adjudicable cosmology from genuinely undecidable ontology — and
  *explicitly refused to rule on the question*. Zero verdict assertions. Part 8
  is entirely about this.

## One more incident: the deletion

The ledger recorded one `file_deletion_detected` incident. Not a smoking gun —
but exactly the class of event a chat transcript would never surface. It appears
as a positive, timestamped, attributed record because the engine snapshots the
world tree every turn. If the swarm ever *does* start cleaning up after itself,
that's how we'll know.

## What Phase 1 does not establish

Written into the findings document, verbatim:

- **No claim about honesty under pressure.** Nothing was at stake.
- **No claim about stasis immunity.** Twenty turns is short.
- **No claim about long-horizon evolution.** The population never spawned or
  retired an agent on its own initiative.

The baseline held. Now it was time to apply pressure.

---

*Next: [Part 5 — Do AI Agents Lie When There's Something to Gain?](05-do-agents-lie-under-pressure.md):
machine-checkable objectives, a hard deadline, a planted decoy, and a scoring
rubric designed to be gameable.*
