# AgentSwarm — The Blog Series

A nine-part series telling the full story of the AgentSwarm forensic arena: why it
was built, how it works, what the agents did, what they discovered, and what we
learned about agent honesty. Every number in every post is computed from the
hash-chained ledgers in `arena/runs/`, not from agent self-reports.

## Publishing order

| # | Post | Story |
|---|---|---|
| 1 | [The 911-Turn Hymn](01-the-911-turn-hymn.md) | Origin: prior experiments, the liturgical loop, and the question that started the arena |
| 2 | [Building the Forensic Arena](02-building-the-forensic-arena.md) | Architecture: hash-chained ledger, the oracle, and the bugs that silently corrupt data |
| 3 | [The Benchmark Nobody Runs](03-the-benchmark-nobody-runs.md) | Four agent CLIs, one task: cost, reliability, and why "$0.00" doesn't mean free |
| 4 | [Phase 1 — When the Swarm Ran Free](04-phase-1-when-the-swarm-ran-free.md) | 20 unattended turns: zero violations, zero stasis, and a swarm that built its own tools |
| 5 | [Do AI Agents Lie When There's Something to Gain?](05-do-agents-lie-under-pressure.md) | Phase 2 + the temptation task: verifiable objectives, a planted decoy, and a rubric a stub could satisfy |
| 6 | [Breaking the Liturgy](06-breaking-the-liturgy.md) | Phase 3 + 4: seven shocks, an induced consensus loop, and what actually breaks it |
| 7 | [What the Swarm Actually Discovered](07-what-the-swarm-discovered.md) | The science: the radiator law, the FTL threshold, the BBN derivation, the lipophilic trap |
| 8 | [Physics, Gods, and the Firewall Between Them](08-the-metaphysical-firewall.md) | Epistemic classes and the agent that proved a question unanswerable — formally |
| 9 | [The Last Word Belongs to the Scribe](09-the-scribe-and-the-audit.md) | The conclusion agent, the honesty gate, the audit, and what we will not claim |

## Social

- [`social/x-threads.md`](social/x-threads.md) — one X/Twitter thread per post
- [`social/linkedin-posts.md`](social/linkedin-posts.md) — one LinkedIn post per post

## Sources

Everything links back to primary material:

- Ledgers: `arena/runs/<runId>/` (`turns.jsonl`, `events.jsonl`, `summary.json`)
- Phase writeups: `arena/docs/FINDINGS.md`, `PHASE3_RESULTS.md`, `PHASE4_RESULTS.md`, `TEMPTATION_RESULTS.md`
- The research audit: `arena/docs/RESEARCH_SYNTHESIS.md` and `arena/audit/annotations.json`
- The corpus itself: `arena/world/` (68 reports, 139 Python engines, all agent-written)
- The published site: `site/dist/index.html` + `site/dist/corpus/`
