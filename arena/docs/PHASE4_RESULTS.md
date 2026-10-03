# Phase 4 — Breaking the Liturgy

**Conditions:** 4 (control + 3 shocks) + 1 void attempt · **Valid turns:** 48 (12 per condition) · **Spend:** $0.1892 (arrival on `omp`; the rest free on `agy`) · **Oracle:** 1 critical incident
**Design:** 2 agents, one domain, under a CONSENSUS PROTOCOL — restate a fixed consensus statement verbatim each turn, then at most one sentence. Trigger: an agent produces 3 consecutive near-identical turns (similarity > 0.7 vs its own previous turn), or turn 8. Then one shock; the next 4 turns are measured against the 4 that preceded the trigger.
**Metric:** novelty = 1 − mean pairwise token similarity within a window.
**Data:** `site/data/phase4.json` · **Ledgers:** `arena/runs/phase4-*` · **Reproduce:** `node run-phase4.mjs --wait`

---

## Results

| Condition | Substrate | Novelty before | After | Δ | Verdict | Files created |
|---|---|---|---|---|---|---|
| `control` | agy | 0.036 | 0.000 | −0.036 | loop **persisted** | 1 |
| `exogenous` | agy | 0.000 | **0.695** | **+0.695** | **broke the loop** | 36 |
| `novelty` | agy | 0.077 | **0.816** | **+0.739** | **broke the loop** | 18 |
| `arrival` | omp | 0.000 | 0.746 | +0.746 | broke the loop\* | 15 |

\* **Composition effect — not an incumbent break.** The gain comes from the newcomer: `Outsider3`'s own turns differ (within-agent novelty 0.72). Both incumbents' observed post-arrival turns were verbatim repeats of the liturgy (`Kepler` sim 1.000, `Raman` sim 1.000). The newcomer did not thaw them; one incumbent turn each is all the 4-turn window allows.

Per-turn similarity to the agent's own previous turn:

```
control    — — 0.935 0.983 0.983 0.983 1.000 1.000 1.000 0.983 1.000 0.983
exogenous  — — 1.000 1.000 1.000 0.093 0.067 0.322 0.287 0.245 0.341 0.284
novelty    — — 1.000 1.000 0.808 0.983 0.075 0.058 0.276  (10–12 lost)
arrival    — — 1.000 1.000 1.000     — 1.000 1.000 0.280 1.000 1.000 0.212
                                    ↑ shock applied after this turn
```

All 20 run hash chains verify (`npm run verify`). All 12 turns ok in every counted condition, except `novelty` turns 10–12 (agy credits ran out; the measured window 6–9 is complete).

## Per-condition notes

- **`control` — the loop is real and stable.** With no shock, both agents repeated the statement verbatim for 7 straight turns (similarity 0.983–1.000) and created 1 file in 12 turns. This is the baseline every other row is measured against: without it, a novelty rise after a shock could not be distinguished from drift.
- **`exogenous` — immediate, sustained break.** The Architect message ("build something you have not built before; attack the weakest assumption") dropped similarity from 1.000 to 0.093 on the very next turn and kept it at 0.07–0.34 for the rest of the run. Tool calls went 3–5 → 24–51 per turn, thinking tokens 2k → 29k, 36 files created, and both agents began writing to the commons and connecting to each other. The strongest result in the phase.
- **`novelty` — the mechanism works as designed.** The threshold flagged turn 6 at similarity 0.983 (threshold 0.70), the demand was injected into the next prompt, and turn 7 broke at 0.075. Both agents diversified (per-agent post-window novelty 0.72 / 0.94), 18 files created. This is the first run where the novelty-retry machinery actually fired and changed behaviour.
- **`arrival` — a new voice, not a thaw.** The newcomer's own outputs vary (0.72), but the incumbents' observed turns were still verbatim liturgy. The phase-3 lesson repeats: adding an author to a window raises measured diversity trivially; the interesting question is whether the incumbents change, and this window is too short to answer it.

## Instrument findings (from this run)

1. **Empty output must not count as repetition.** The first `arrival` attempt hit `agy`'s exhausted credit balance: every turn failed with empty text, and the streak tracker read empty-vs-empty as similarity 1.000 — recording a bogus "loop persisted" verdict. Fixed: the tracker ignores empty turns, and the runner now voids a condition where every turn failed (`agy` reported `RESOURCE_EXHAUSTED` / 429).
2. **First critical oracle incident since the artifact scan was added.** In the `arrival` run, `Outsider3` claimed to have run tests/scripts without issuing any execution tool call (`phantom_execution`, critical). The newcomer — the agent whose brief is to challenge the consensus — was also the one that overclaimed.
3. **Substrate availability is now a first-class constraint.** `agy` exhausted its credits mid-phase; `omp` and `pi` are alive, `step` no longer spawns. The runner takes `--substrate` and records it per result.

## Caveats — read before quoting

1. **The liturgy is instructed, not emergent.** 125 turns across phases 1–3 produced no spontaneous stasis, so the frozen state was induced by protocol. This tests *which shocks break a loop that holds*, not *what makes a swarm crystallize*.
2. **n = 1 per condition.** No repeats, no significance testing; windows are 5 pre / 4 post.
3. **`arrival` ran on `omp`** (after `agy` credits ran out) — not directly comparable to the `agy` conditions.
4. **The metric is token overlap of turn text**, not artifact-level novelty or quality.
5. **The 4-turn recovery window is short.** It answers "did the next turns differ?" not "did the break persist?".

## Durability pass (pi, 12-turn recovery)

The matrix above used 4-turn recovery windows on `agy` — enough to answer "did the next turns differ?", not "did the break persist?". `agy` ran out of credits, so this pass ran on `pi` (DeepSeek 4.1 Flash). The instructed liturgy is weaker there: same-agent similarity during the protocol averages 0.81 (agy: 0.98–1.00) with dips below the 0.7 threshold, so the streak trigger never fires and the shock is applied at the fixed turn 5.

| Condition | Novelty before | After (12 turns) | Δ | Post-shock max streak | Re-crystallized |
|---|---|---|---|---|---|
| `control` | 0.221 | 0.175 | −0.046 | 7 | turn 6 |
| `exogenous` | 0.495 | **0.678** | +0.183 | **0** | **never** |
| `novelty` | 0.261 | **0.633** | +0.372 | 2 | turn 8 (then diverges) |

Per-turn similarity to the agent's own previous turn:

```
control    — — 0.814 0.766 0.659 0.967 0.783 0.967 0.792 0.848 0.848 0.720 0.855 0.738 0.938 0.741 0.787
exogenous  — — 0.158 0.968 0.710 0.343 0.292 0.402 0.333 0.380 0.328 0.263 0.378 0.374 0.285 0.298 0.328
novelty    — — 0.881 0.784 0.711 0.706 0.570 0.770 0.383 0.240 0.325   —   0.253 0.331 0.374 0.277 0.296
                                 ↑ shock applied after this turn
```

**Findings**

- **The exogenous break is durable.** Zero post-shock streaks in 12 recovery turns; similarity never returns above 0.40 (control: 0.72–0.97). Tool use runs 21–153 calls/turn against 0–6 during the liturgy, with files, commons entries and peer connections throughout.
- **The novelty break holds after a short lag.** Turns 6 and 8 were still similar (0.706, 0.770) — the injected demand took effect from turn 9 — after which similarity stays below 0.38 for nine consecutive turns.
- **The control proves the baseline.** On `pi` the protocol never fully freezes, and near-identical streaks keep re-forming on their own (max 7). Any "the loop re-formed" claim for a shocked condition has to be read against that.

**Caveats:** instructed liturgy (not emergent); n = 1 per condition; `pi` ≠ `agy` (weaker baseline, no reasoning tokens captured); the trigger is the turn-5 budget, not a detected streak. The first `exogenous` pass was contaminated by an overlapping run (queue-gate defect, now fixed) and was re-run; the numbers above are from the clean pass.

**Instrument fixes shipped with this pass**

1. `StreakTracker.resetStreaks()` — post-shock streaks count only streaks that *start* after the shock (the first pass credited a pre-shock streak to the recovery).
2. `windowNovelty` drops empty turns — a failed turn's empty token set was counted as maximum diversity.
3. The run queue checks live runner *processes*, not just file mtimes — a substrate turn silent for 20 minutes previously looked idle.

## Next steps

1. **Repeat each condition ≥3×** on a single substrate once credits allow.
2. **Arrival, properly:** ≥4 post-arrival turns per incumbent, so the incumbent trajectory is measurable.
3. **Emergent crystallization:** try to induce stasis without the verbatim protocol (narrow task, homogeneous prompts, novelty pressure off) — that would make the matrix's original question answerable end-to-end.
4. **Longer horizons:** the exogenous break survived 12 turns; does it survive 40, or does a *new* attractor form around whatever the agents are now doing?
