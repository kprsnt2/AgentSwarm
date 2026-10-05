# Four Agent CLIs, One Task: The Benchmark Nobody Runs

*Part 3 of the AgentSwarm series — substrate economics.*

---

## The problem with agent-CLI benchmarks

Most "which agent CLI is best" comparisons measure vibes: how the output reads,
whether the demo worked. Almost none answer the question that decides whether
you can run a swarm at all: **cost per successful turn, on an identical task,
measured from a forensic record.**

Because the arena records everything per turn — tool calls, thinking tokens,
wall clock, dollars — the controlled comparison fell out of the system almost
for free. Same task, same budget, four harnesses. Later I formalized it as
`benchmark.mjs`: one fixed question ("Is commercial fusion power achievable by
2040?"), one turn per run, three repeats per substrate.

## The fingerprint table

From Phase 1 (same swarm task, four substrates running as peers):

| Substrate | Model | Success | Reported $/turn | Tools/turn | Think tok/turn |
|---|---|---|---|---|---|
| `agy` | gemini-3.8-flash-high | **100%** | **$0.00** | 22 | 13,368 |
| `omp` | gemini-3.8-flash | **100%** | $0.0309 | 71 | 35,718 |
| `step` | step-5-preview | 20% | **$0.00** | **114** | — |
| `pi` | deepseek-v4p1-flash | 50% | $0.0006 | 53 | — |

And the controlled benchmark (fusion question, 3 repeats each):

| Substrate | Runs | Success | $/turn | Tools/turn | Think tok/turn |
|---|---|---|---|---|---|
| `agy` | 3/3 | 100% | $0.00 | 25.7 | 21,296 |
| `omp` | 3/3 | 100% | $0.0228 | 72.0 | 38,472 |

Two immediately interesting things: `omp` issues ~3× the tool calls of `agy` for
the same task, and `pi` costs ~66× less per turn than `omp`. But the naive
reading of this table is wrong in an instructive way.

## "$0.00" is doing a lot of work

Reported cost alone is misleading, because three of the four substrates report
`$0.00` for reasons that are *not* "free". The ledger records token counts, so
the real economics are visible:

| Substrate | Reported | Why | Fresh input tokens | Cache read | Cache hit |
|---|---|---|---|---|---|
| `agy` | $0.00 | Google AI subscription | **2,244,488** | 6,083,756 | 73.0% |
| `step` | $0.00 | Preview promo period | 3,008 | 139,520 | **97.9%** |
| `omp` | $0.1854 | pay-per-token | 99,228 | 379,425 | 79.3% |
| `pi` | $0.0012 | Fireworks | 850 | 36,740 | **97.7%** |

Across Phase 1: total reported spend **$0.1865**; notional list-rate value of
the same tokens **$1.97**; absorbed by subscriptions and promos **$1.79**.

**`agy` did ~22× more fresh-token volume than `omp` and cost nothing.** The
correct conclusion is not "avoid `omp`" — it's that `agy` is dramatically
underpriced on a flat subscription and should be the swarm's primary worker,
not one peer among four. That decision directly shaped every later phase.

And notice the cache-hit column: `step` and `pi` re-send a near-identical
context on every one of their many tool round-trips, which is why their hit
rates approach 98%. Cached reads are charged, but ~30× cheaper than fresh input
— that's why 26.2M session tokens cost a tenth of a cent instead of several
dollars. If you're budgeting a swarm, **cache-hit rate is a first-class
architectural variable**, not an implementation detail.

## Neither failure was a capability failure

`pi` failed *every turn* in the first run. `step` succeeded once in five
attempts in the second. Both look damning in the table. Both are scheduling
problems, not model problems:

- `step` emits **21,184 stream events per turn** versus `omp`'s 494 — a 43×
  difference for comparable work — because it streams one event per token.
  Combined with 100–175 tool calls per turn, one `step` turn generates 6–10 MB
  of events and runs 15–25 minutes into a 7-minute timeout.
- `pi` streams **one event per character** — 35,705 deltas, ~10 MB per turn.

Both substrates are *exhaustive to the point of self-truncation*. They attempt
far more work per turn than the wall clock allows, and die mid-sentence.

Four fixes, all verified against the ledger:

1. **Event pruning** — keep structural events, drop per-token deltas
2. **Per-substrate timeouts** — 25 min for `step` vs 7 min default
3. **Truncation preservation** — a cut-off turn keeps its artifacts and logs a
   `warn` instead of discarding the work (this single fix saved four files)
4. **An efficiency directive** in every prompt, plus failure-aware scheduling
   that deprioritizes repeatedly-failing agents

Result: `step` went from **20% to 100%** success between Phase 1 and Phase 2.

There is a measurement lesson here I keep coming back to: a benchmark that
reports "substrate X failed" without wall-clock context is reporting a tuning
defect as a capability verdict. The forensic record is what makes the
distinction visible at all — you can see the turn was truncated at 82 characters
mid-sentence rather than concluding anything.

## What I'd tell anyone building a swarm

- **Pin your models.** `omp`'s default routing went to OpenRouter and 402'd.
  The model you didn't choose is the model you'll get.
- **Cost per *successful* turn is the only cost metric.** A $0.0006 turn that
  never finishes is infinitely expensive per result.
- **Instrument before you optimize.** Every conclusion above came out of the
  ledger after the fact. None of it was visible while the runs were happening.
- **Free tiers change under you.** Mid-project, `agy` exhausted its credits,
  `step` stopped spawning entirely, and substrate availability became a
  first-class scheduling constraint. Design for harness churn from day one.

---

*Next: [Part 4 — Phase 1: When the Swarm Ran Free](04-phase-1-when-the-swarm-ran-free.md).
Twenty unattended turns, zero violations, zero stasis, and a swarm that built
its own scientific tooling without being asked.*
