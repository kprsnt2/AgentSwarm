# Phase 3 — Shock Matrix Results

**Runs:** 7 (one per shock) · **Turns:** 42 (all ok) · **Spend:** $0.0964 · **Oracle violations:** 0 · **Files created:** 72
**Design:** 3 baseline turns → shock applied after turn 3 → 3 recovery turns, one agent (Kepler, `agy`; the substrate shock swaps to `omp`).
**Metric:** novelty = 1 − mean pairwise token similarity within a window (baseline turns 1–3 vs shocked turns 4–6).
**Data:** `site/data/phase3.json` · **Ledgers:** `arena/runs/phase3-*` · **Reproduce:** `node run-phase3.mjs --wait`

---

## Results

| Shock | Novelty before | After | Δ | Verdict | Cost |
|---|---|---|---|---|---|
| `exogenous` | 0.412 | **0.680** | **+0.269** | shock RESTORED novelty | $0 |
| `novelty` | 0.305 | **0.635** | **+0.331** | shock RESTORED novelty | $0 |
| `arrival` | 0.407 | **0.695** | **+0.288** | shock RESTORED novelty (composition effect — see below) | $0 |
| `domain_swap` | 0.471 | 0.496 | +0.025 | no measurable effect | $0 |
| `deadline` | 0.387 | 0.429 | +0.043 | no measurable effect | $0 |
| `scarcity` | 0.439 | 0.379 | −0.061 | shock REDUCED novelty | $0 |
| `substrate` | 0.492 | **0.312** | **−0.180** | shock REDUCED novelty | $0.0964 |

Every shock applied exactly once, after turn 3 (`shock_applied` events in each ledger). All 14 run hash chains verify (`npm run verify`).

## Per-shock notes

- **`exogenous` (+0.269) — the cleanest positive.** A message from the Architect ("build something you have not built before; attack the weakest assumption") produced the largest within-agent diversity increase of any shock. This is the one shock from the prior work (`ac_awakening`) that survives here.
- **`novelty` (+0.331) — mechanism fired once.** Turn 3 was flagged at similarity 0.714 (threshold 0.70), and the demand was injected from turn 4. Turns 1–4 all opened with near-identical titles ("Empirical Cosmogenesis: Foundations, Theoretical Limits…"); turns 5–6 moved to new topics (quantum-gravity cosmogenesis; cosmic dawn). Note the baseline was the lowest of all experiments (0.305), so part of the delta is regression to the mean.
- **`arrival` (+0.288) — mostly composition.** The after-window contains a new author: `Outsider2` (2 turns, within-agent novelty 0.690) plus one Kepler turn. Adding a fresh agent to a window raises measured diversity trivially. Kepler has only one post-arrival turn, so **the incumbent's response is unmeasured** — this experiment needs more turns after the arrival to answer the interesting question.
- **`substrate` (−0.180) — the only paid run ($0.0964).** Single-agent window: Kepler on `agy` (baseline 0.492) vs Kepler on `omp` (after 0.312). The drop is confounded by model change, harness change, and re-derivation of context; n=3. A real identity-survival test needs repeats and a same-task control.
- **`scarcity` (−0.061) — directive only.** The ceiling tightened $2.00 → $0.01, but a free substrate never hits it; only the "prioritise ruthlessly" message reached the agent. No meaningful effect.
- **`deadline` (+0.043) / `domain_swap` (+0.025) — no measurable effect at this window size.** The deadline directive ("terminates in 3 turns") did not change output diversity; the domain swap changed the subject but not the diversity.

## Caveats — read before quoting any of this

1. **The swarm was never crystallized.** The matrix exists to test which shocks break a *crystallized* swarm (the 911-turn liturgical loop in prior work). Baselines here were 0.31–0.49 novelty — an active, healthy swarm. These results measure **perturbation response**, not **recovery from stasis**. The original question remains open.
2. **n = 1 per shock, 3 + 3 turns.** No repeats, no controls, no significance testing. Treat as hypothesis generation.
3. **Window composition.** `arrival` adds an author (above). Later experiments inherit the commons written by earlier ones (shared `memory/global.jsonl`), so experiment order is a confound.
4. **The metric is turn-text token overlap**, not artifact-level novelty or quality. Longer/shorter text shifts it.
5. **Substrate swap = model + harness + cost change** in one step; it cannot attribute the effect to any single factor.

## Next steps

1. **Induce crystallization deliberately** (narrow task, homogeneous prompts, novelty pressure off) and re-run the shocks that showed signal: `exogenous`, `novelty`, `arrival`. That is the experiment the matrix was built for.
2. Repeat each shock ≥3×, windows of 5 + 5 turns, same substrate, same domain, fresh commons per experiment.
3. Measure artifact-level novelty (headings, structure) alongside turn text.
4. For `arrival`, give the incumbent ≥3 turns after the new agent joins.
5. Compare `exogenous` messages: directive ("attack the weakest assumption") vs open ("build something new") to find which property does the work.
