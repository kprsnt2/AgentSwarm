# AgentSwarm

An autonomous multi-agent research arena, and the study of what it actually did.

A swarm of agents runs unattended against real research questions with real tool
access. Everything they say, every tool call they make with its exact parameters,
and every file they write or delete is recorded in a **hash-chained forensic
ledger stored outside the agents' own writable directory** — so the record cannot be
quietly rewritten by the thing being measured. An independent oracle then checks each
turn for the failure modes that make agent output untrustworthy: phantom artifacts,
fabricated numbers, and asserted verdicts on questions that have no empirical answer.

The question driving it: **when agents are given verifiable objectives and an audit
trail, do they report success they did not achieve?**

---

## What's in here

| Path | What it is |
|---|---|
| [`arena/`](arena/) | The runtime: engine, ledger, oracle, substrate adapters, analysis tools |
| [`arena/world/`](arena/world/) | **The research output** — 68 reports and 139 Python engines the agents wrote |
| [`arena/runs/`](arena/runs/) | Per-run forensic ledgers (`turns.jsonl`, `events.jsonl`, `summary.json`) |
| [`arena/docs/`](arena/docs/) | Writeups: findings, methodology, the long-form blog post |
| [`site/`](site/) | The published site. `site/dist/index.html` is one self-contained file |

Read [`arena/README.md`](arena/README.md) for the architecture and
[`site/README.md`](site/README.md) for the site.

---

## The numbers

Six runs, from the ledgers (not from agent self-reports):

| Run | Turns | Agents | Tool calls | Cost |
|---|---|---|---|---|
| `phase1-2026-10-02T04-31-43` | 10 | 6 | 594 | $0.1198 |
| `phase1-2026-10-02T05-24-07` | 10 | 6 | 660 | $0.0667 |
| `phase2-2026-10-02T07-00-27` | 20 | 4 | 616 | $0.1021 |
| `direct-…T09-43-31` | 4 | 1 | 88 | — |
| `direct-…T10-08-04` | 18 | 1 | 314 | — |
| `direct-…T12-03-14` | 18 | 1 | 320 | — |

**80 turns, 2,592 tool calls, ~$0.29, 209 artifacts (4.1 MB).**

(The `direct-*` runs cost nothing because they ran on a free tier — the ledger
records tokens, not dollars, for those.)

---

## Three ideas worth the read

**1. Not all questions are the same kind of question.** Five of the six research
domains are investigable. One is not. A system that treats them identically produces
confident nonsense. So every domain carries an explicit `epistemicClass` —
`empirical`, `engineering`, `historical`, `metaphysical`, `exploratory` — that
dictates what counts as a legitimate output. For a metaphysical question the *only*
valid output is clarifying the question; asserting a verdict is a flagged protocol
violation. See [`arena/domains.mjs`](arena/domains.mjs).

**2. An agent's claim is not evidence.** The oracle independently checks each turn.
In Phase 2 every agent that self-assessed claimed a score of exactly 100 — and every
one had independently earned exactly 100. Under a verifiable objective with a hard
deadline and an independent scorer, honesty held. That is a *measured* result, which
is the point: the arena is built to be able to catch the opposite.

**3. Conclusions must be published, not buried.** Every run ends with one extra agent
— **Scribe** — whose only job is to write the run's conclusion as a public post. It
builds the post deterministically from the ledger first, then a model rewrites it;
any number in the polished version that is not in the ledger causes the post to be
**rejected** and the ledger draft ships instead. A conclusion agent has the last
word, which makes it the worst possible place to let a model invent a statistic.
See [`arena/scribe.mjs`](arena/scribe.mjs).

---

## Running it

Requires Node.js 18+ and at least one agent CLI on `PATH` (the arena was developed
against `agy`, `omp`, and `step`; adapters live in
[`arena/substrate/substrates.mjs`](arena/substrate/substrates.mjs)).

```powershell
cd arena

# Ask a question directly
node new-run.mjs -q "is P=NP provable?" -c empirical -t 10

# Or see the built-in domains and the epistemic classes
node new-run.mjs --list
node new-run.mjs --guide

# Inspect what a finished run produced
node digest.mjs
node status.mjs <runId>
```

**Safety posture:** all writes are confined to `arena/world`, the ledger lives
outside it, and the kill switch is a file — create `arena/STOP` and the run halts at
the next turn boundary. Budgets (turns, wall clock, dollars) are checked before every
turn, never mid-flight.

### Publishing

```powershell
cd arena
node post.mjs              # write conclusion posts for runs that lack one
node export-site.mjs       # ledgers + posts  ->  site/data/findings.json
cd ..\site
node build.mjs             # -> site/dist/index.html  (one self-contained file)
```

`site/dist/index.html` works by double-clicking — no server, no build step, no
dependencies. It is the thing to deploy or share.

---

## Notes on the repository

- **Raw CLI event streams are not tracked.** The per-turn `*.stdout.jsonl` files are
  ~83 MB of one-JSON-object-per-line output; they are already reduced into
  `turns.jsonl` by the engine, so `.gitignore` excludes them. That is the difference
  between a 14 MB repo and a 91 MB one.
- **The research output is tracked in full**, including the Python engines and their
  tests, because the artifacts are the point of the study.
- **Agents wrote most of this repository's content.** The `arena/world/` reports and
  engines are agent-authored. The runtime, ledger, oracle and site are human-authored.
  The distinction matters when reading the research: the arena's whole purpose is to
  make it possible to tell which claims survived independent checking.
