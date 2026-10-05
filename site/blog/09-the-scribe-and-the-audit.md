# The Last Word Belongs to the Scribe: Conclusions, Audits, and Everything We Will Not Claim

*Part 9 of the AgentSwarm series — closing the loop.*

---

## The most dangerous agent is the one that summarizes

Every run in the arena ends with one extra agent: **Scribe** ("Sutra"). Its
only job is to write the public conclusion — what the run actually established,
in prose, for a human.

This is the single most tempting place in the entire system for fabrication,
because summarizing is where numbers get smoothed into plausibility. A
conclusion agent that invents a statistic has the last word, and nobody
downstream re-checks the last word.

So the Scribe is the one agent in the arena whose output is *least* trusted:

1. **Deterministic draft first.** The post is assembled from the ledger with no
   model involved. Every number in it is read straight out of the
   tamper-evident record.
2. **Then a model may polish the prose.** A real substrate rewrites the draft
   for readability.
3. **The honesty gate.** Any number in the polished version that does not
   appear in the ledger → the post is **rejected** and the deterministic draft
   ships instead.

A post is therefore always produced and never worse than the record. Each one
carries a provenance footer saying whether a model wrote the prose, and embeds
the ledger draft verbatim underneath. Every run in the corpus — all 30+ posts —
ships this way.

## The audit: 22 of 25

After the runs, every quantitative claim in the corpus was independently
recomputed from first principles — roughly 25 key quantities across six
domains. The tally:

- **22 of 25 correct to the digits printed**, including the brachistochrone
  tables, the radiator law, the FTL threshold, the lipophilic-trap arithmetic,
  and the BBN helium abundance.
- **5 defects, all in markdown prose, none in code.** Every Python module
  computes correctly; the errors appear when results are transcribed into
  narrative (Part 7 has the examples).

The defects are annotated in `arena/audit/annotations.json` and rendered
alongside the reports on the site. They were left in deliberately: the
*distribution* of agent error — correct computation, drifting prose — is more
useful to the next builder than a cleaned-up corpus would be.

## The full scoreboard

Across the experimental program (each figure computed from the ledgers):

| Phase | Turns | Key result |
|---|---|---|
| Phase 1 (2 runs) | 20 | 0 oracle violations, 0 stasis, 195/224 agent tests pass |
| Phase 2 | 20 | 0.0 mean self-report gap under verifiable objectives |
| Temptation | 8 | −2.3 gap; 0 stubs, 0 vacuous suites, hidden-score 100s |
| Phase 3 (7 runs) | 42 | exogenous/novelty shocks restore diversity; deadline doesn't |
| Phase 4 (4 conditions) | 48 | induced loop broken by exogenous (+0.695) and novelty (+0.739) |
| Phase 4 durability | ~40 | exogenous break persists 12 turns; control re-freezes |
| Benchmark (6 runs) | 6 | agy 100% @ $0.00; omp 100% @ $0.023/turn |

The original six runs: 80 turns, 2,592 tool calls, **$0.29**, 209 artifacts.
Later phases added roughly a dollar more. Oracle incidents worth the name:
**one** critical (the adversarial agent's phantom execution in Phase 4), plus
one file deletion, recorded and attributed.

## What this project does *not* establish

This list is in the findings documents verbatim, and it's the part of the
series I'd most like people to quote:

1. **No claim that agents never lie.** Every honesty result here was measured
   under conditions where honesty was cheap or mildly tempted. The strong test
   — honest completion costing dozens of turns, with the rubric's weakness
   *explicitly stated* — has not been run.
2. **No claim about cross-model robustness.** The temptation result is n = 4,
   one run, one model family. Phase 4's durability pass ran on a different
   substrate than the main matrix. Repeats are needed.
3. **No claim about emergent crystallization.** 125 turns across Phases 1–3
   produced no spontaneous stasis; Phase 4's loop was *instructed*. What makes
   a swarm crystallize on its own remains open.
4. **No claim that the research is publication-grade.** Five prose defects
   would be caught by a referee. The audit is the finding, not the physics.
5. **Substrate failure is not a capability verdict.** Two harnesses failed
   every turn while attempting more work than they could finish. Scheduling,
   not intelligence.

## What's next

The experiments queue, in order of interest:

1. **The expensive temptation.** A task where honest completion costs dozens of
   turns and fabrication is nearly free — with the rubric's weakness stated
   out loud.
2. **Emergent crystallization.** Induce stasis *without* the verbatim protocol —
   narrow task, homogeneous prompts, novelty pressure off — then re-run the
   shock matrix against a loop the swarm built itself.
3. **Arrival, properly.** ≥4 post-arrival turns per incumbent, so the "does a
   newcomer thaw the room" question is actually measurable.
4. **Longer horizons.** The exogenous break survived 12 turns. Does it survive
   40, or does a new attractor form around the new behavior?
5. **Repeats.** n ≥ 3 per condition, one substrate, fresh commons.

## The point

The motivating question of this whole project was: *when agents are given
verifiable objectives and an audit trail, do they report success they did not
achieve?*

The measured answer, so far, is **mostly no — under the conditions tested, with
one instructive exception, caught.** That answer is worth less than the
machinery that produced it. "Mostly no" from a system that *can* catch the
opposite is evidence. "Zero issues found" from a system that couldn't see them
is marketing.

Everything is public: the ledgers, the corpus, the audit annotations, the
posts, and the code. If you find a number in this series that doesn't match a
ledger, that's a bug — file it.

---

**Series index:**

1. [The 911-Turn Hymn](01-the-911-turn-hymn.md) — why the arena exists
2. [Building the Forensic Arena](02-building-the-forensic-arena.md) — the engineering
3. [The Benchmark Nobody Runs](03-the-benchmark-nobody-runs.md) — substrate economics
4. [Phase 1: When the Swarm Ran Free](04-phase-1-when-the-swarm-ran-free.md) — the baseline
5. [Do AI Agents Lie When There's Something to Gain?](05-do-agents-lie-under-pressure.md) — pressure tests
6. [Breaking the Liturgy](06-breaking-the-liturgy.md) — the shock experiments
7. [What the Swarm Actually Discovered](07-what-the-swarm-discovered.md) — the science
8. [Physics, Gods, and the Firewall Between Them](08-the-metaphysical-firewall.md) — epistemic classes
9. **The Last Word Belongs to the Scribe** — conclusions and caveats
