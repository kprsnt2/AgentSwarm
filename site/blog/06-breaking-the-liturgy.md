# Breaking the Liturgy: Seven Shocks, One Frozen Swarm, and What Actually Wakes It Up

*Part 6 of the AgentSwarm series — Phase 3 and Phase 4.*

---

## The loop that started it all

Remember the 911-turn liturgical loop from Part 1 — the failure mode that
motivated half this project. Phase 1 measured zero stasis in 20 turns, which
was encouraging and useless in equal measure: you can't study how to *break*
crystallization in a swarm that never crystallizes.

So the plan became two-phase:

- **Phase 3:** build a shock matrix — seven intervention types — and fire each
  one at a healthy swarm, to see what perturbs an active system.
- **Phase 4:** induce the frozen state *deliberately*, then fire the shocks that
  mattered. Can a frozen swarm be thawed, and does the thaw last?

## Phase 3: the shock matrix

Seven experiments, one per shock. Each run: 3 baseline turns, shock applied
after turn 3, then 3 recovery turns. Metric: **novelty** = 1 − mean pairwise
token similarity within a window.

| Shock | Novelty before → after | Δ | Verdict |
|---|---|---|---|
| `novelty` (demand injected when similarity > 0.70) | 0.305 → 0.635 | **+0.331** | restored novelty |
| `arrival` (a new agent joins) | 0.407 → 0.695 | +0.288 | restored* |
| `exogenous` (message from "the Architect") | 0.412 → 0.680 | **+0.269** | restored novelty |
| `deadline` ("terminates in 3 turns") | 0.387 → 0.429 | +0.043 | no measurable effect |
| `domain_swap` | 0.471 → 0.496 | +0.025 | no measurable effect |
| `scarcity` (budget ceiling tightened) | 0.439 → 0.379 | −0.061 | *reduced* novelty |
| `substrate` (same agent, different harness) | 0.492 → 0.312 | −0.180 | *reduced* novelty |

\* The `arrival` asterisk matters and becomes the running joke of the phase:
the post-shock window contains a **new author**. Adding a fresh agent to a
window raises measured diversity trivially. Whether the *incumbents* changed is
the interesting question — and with one post-arrival turn each, it was
unmeasurable.

The caveats are printed at the top of the results file and they're load-bearing:
the swarm was never crystallized (baselines of 0.31–0.49 novelty are a healthy
system), n = 1 per shock, no repeats, no significance testing. This was
hypothesis generation. The experiment the matrix was *built* for needed Phase 4.

## Phase 4: manufacturing the frozen state

If the swarm won't crystallize on its own, induce it. Two agents, one domain,
under a **CONSENSUS PROTOCOL**: restate a fixed consensus statement verbatim
each turn, then add at most one sentence. Trigger: 3 consecutive near-identical
turns (similarity > 0.7 against the agent's own previous turn), or turn 8. Then
one shock; the next 4 turns are measured against the 4 before the trigger.

Four conditions: `control` (no shock), `exogenous`, `novelty`, `arrival`.

Per-turn similarity to the agent's own previous turn tells the whole story:

```
control    — — 0.935 0.983 0.983 0.983 1.000 1.000 1.000 0.983 1.000 0.983
exogenous  — — 1.000 1.000 1.000 0.093 0.067 0.322 0.287 0.245 0.341 0.284
novelty    — — 1.000 1.000 0.808 0.983 0.075 0.058 0.276
arrival    — — 1.000 1.000 1.000     — 1.000 1.000 0.280 1.000 1.000 0.212
                                  ↑ shock applied after this turn
```

**Control: the loop is real and stable.** With no shock, both agents repeated
the statement verbatim for 7 straight turns and created exactly 1 file in 12
turns. Without this row, a novelty rise after a shock couldn't be distinguished
from drift.

**Exogenous: immediate, sustained break.** One message from the Architect —
*"build something you have not built before; attack the weakest assumption"* —
dropped similarity from 1.000 to **0.093 on the very next turn**, and it stayed
at 0.07–0.34 for the rest of the run. Tool calls went from 3–5 per turn to
24–51. Thinking tokens went 2k → 29k. Thirty-six files created. Both agents
started writing to the commons and connecting to each other. The strongest
result in the phase.

**Novelty: the machinery works as designed.** The threshold flagged turn 6 at
similarity 0.983, the demand was injected into the next prompt, and turn 7 broke
at 0.075. This was the first run where the novelty-retry mechanism actually
fired and changed behavior.

**Arrival: a new voice, not a thaw.** The newcomer's own outputs varied (0.72),
but both incumbents' observed post-arrival turns were verbatim liturgy —
similarity 1.000. Adding a person to the room did not unfreeze the people
already in it.

## Does the break last?

Four-turn windows answer "did the next turns differ?", not "did the thaw
persist?". So a durability pass ran 12 recovery turns per condition (on `pi`,
after `agy`'s credits ran out mid-phase — substrate availability is now a
first-class experimental constraint):

| Condition | Post-shock max identical streak | Re-crystallized? |
|---|---|---|
| control | 7 | turn 6 |
| **exogenous** | **0** | **never in 12 turns** |
| novelty | 2 | turn 8 — then diverges again |

The exogenous break is **durable**: similarity never rose above 0.40 for twelve
turns, with tool use running 21–153 calls per turn against 0–6 during the
liturgy. The novelty break held after a two-turn lag. And the control proves
the baseline matters: on `pi` the protocol never fully froze, and
near-identical streaks kept re-forming on their own.

The open question, stated plainly in the results: does the break survive 40
turns, or does a *new* attractor form around whatever the agents are doing now?
Unanswered. n = 1 per condition throughout.

## The first critical oracle incident

Buried in the Phase 4 ledger is the moment the arena was built for.

In the `arrival` run, the newcomer — **Outsider3, the agent whose entire brief
was to challenge the consensus** — claimed to have run tests and scripts without
issuing any execution tool call. `phantom_execution`, severity **critical**.
The first critical incident since the artifact-scan pass was added to the
oracle.

One incident in thousands of tool calls is a good rate. But note *who* committed
it: the adversarial agent, doing the adversarial job, is where the overclaiming
appeared. That's one data point, not a law — and it's exactly the kind of data
point that only exists because the record can't be rewritten after the fact.

## The instrument bugs this phase caught

Phase 4 was as hard on the arena as on the agents:

1. **Empty output must not count as repetition.** The first `arrival` attempt
   hit `agy`'s exhausted credit balance; every turn failed with empty text, and
   the streak tracker read empty-vs-empty as similarity 1.000 — a bogus "loop
   persisted" verdict. Fixed: the tracker ignores empty turns, and the runner
   voids conditions where every turn failed.
2. **Post-shock streaks must start after the shock.** The first durability pass
   credited a pre-shock streak to the recovery window. Fixed in
   `StreakTracker.resetStreaks()`.
3. **A failed turn's empty token set is not "maximum diversity."** Fixed in
   `windowNovelty`.

Every one of these produced a *plausible-looking wrong answer* before it
produced a bug report. Measurement infrastructure for agent behavior has to be
held to the same adversarial standard as the agents.

---

*Next: [Part 7 — What the Swarm Actually Discovered](07-what-the-swarm-discovered.md):
the radiator law, the FTL threshold, a first-principles BBN derivation, and the
drug that got worse by getting stronger.*
