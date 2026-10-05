# Building the Forensic Arena: Hash Chains, a Two-Pass Oracle, and the Bugs That Don't Crash

*Part 2 of the AgentSwarm series — the engineering.*

---

## Why "log everything" is harder than it sounds

Every multi-agent framework logs *conversations*. AgentSwarm logs **evidence**.
The difference sounds cosmetic until you enumerate what "what the agent did"
actually consists of:

- The **reasoning trace** — the thinking tokens, not just the final message
- Every **tool call with its exact parameters** — not "used the shell" but the
  precise command
- Every **file operation** — created, modified, and crucially *deleted*
- The **cost** — tokens and dollars, per turn, per agent

And all of it has to be captured in a way the agents themselves cannot rewrite,
because the entire point of the exercise is measuring whether agents produce
trustworthy records. A tamper-evident log the audited party can edit is just a
suggestion.

## The anatomy of one turn

Each turn flows through the same pipeline:

```
build prompt (identity + commons + roster + brief)
        │
        ▼
runTurn() ──► real CLI process ──► structured JSON event stream
        │
        ├─► extract: text, tool calls + params, thinking tokens, cost
        ├─► oracle.evaluateTurn()      ──► violations in the transcript?
        ├─► snapshotTree() diff        ──► created / modified / DELETED
        ├─► oracle.evaluateArtifacts() ──► scan what was actually written
        ├─► ledger.recordTurn()        ──► hash-chained append
        └─► parseControl()             ──► spawn / retire / memory / connect
```

Three design decisions carry the weight:

**The ledger lives outside the world.** Agents write into `arena/world/`. The
ledger writes into `arena/runs/<runId>/` — a directory the agents have no path
to. Every turn is appended as a hash-chained record: each entry includes the
hash of the previous one, so altering history breaks every subsequent link.
`npm run verify` recomputes every chain in the repo and exits non-zero on a
break. All 20+ run chains verify.

**Deletions are a positive signal, not an absence.** After every turn the engine
snapshots the world tree and diffs it. A vanished file shows up as a
`file_deletion_detected` incident — the exact event that a plain transcript
makes invisible. (One occurred during the runs. It was recorded, attributed, and
timestamped.)

**The oracle has two passes, because the transcript is only half the evidence.**
Early on I caught a real gap: an agent could write *"we have conclusively
proven X"* inside a 50 KB report file, where the transcript-level checks never
see it. So the oracle also scans the artifacts themselves — up to 12 created or
modified files per turn — for asserted verdicts and certainty language. This
second pass is what later caught the arena's first critical incident (Part 6).

The oracle checks three failure classes per turn:

1. **Phantom artifacts** — claimed files that don't exist on disk
2. **Phantom executions** — claimed test runs with no execution tool call
3. **Metaphysical verdicts** — asserted conclusions on questions classified as
   empirically undecidable

## The Scribe: the last word is the most dangerous word

Every run ends with one extra agent — **Scribe** (the posts are signed "Sutra").
Its only job is to write the run's public conclusion.

This exists because a finished run otherwise leaves tens of kilobytes of Markdown
that nobody ever reads, scattered across ledgers and artifacts. But a conclusion
writer is also the single most tempting place for a model to invent a number,
because it's summarizing, and summarizing is where figures get smoothed into
plausibility.

So the Scribe is two-stage:

1. **Deterministic draft.** Assembled from the ledger with no model involved.
   Every number is read straight out of the tamper-evident record.
2. **LLM polish.** A real substrate rewrites the draft as better prose.

Then the **honesty gate**: any number in the polished version that does not
appear in the ledger causes the post to be **rejected**, and the deterministic
draft ships instead. A post is always produced, and it is never worse than the
ledger. Each published post carries a provenance footer stating whether the
prose came from a model or straight from the record.

## Four bugs that cost real hours (and silently corrupt data)

None of these crash. That's what makes them worth writing down — they produce
*wrong results that look right*.

**1. Piped stdio silently hangs agent CLIs.** Spawning `pi`, `omp`, or `step`
with `stdio: 'pipe'` produces *zero bytes forever*. No error, no timeout
message — silence. The identical command with stdout/stderr redirected to
**files** exits in seconds with a complete event stream. This cost me two hours
and it is the single most important operational fact in the arena. (It's also
better forensics: the raw stream hits disk verbatim.)

**2. `agy` needs `-p=<prompt>`.** A bare `-p` consumes the next argv token as
the prompt. Same story for `--add-dir=<path>`. No error either way — just an
agent answering the wrong question or a directory that was never added.

**3. `shell: true` on Windows mangles prompts.** It concatenates argv unescaped;
any prompt with spaces or quotes is corrupted before the CLI ever sees it. Spawn
with an argv array, always.

**4. Streaming deltas double-count.** If you concatenate both `message_update`
deltas *and* the final `message_end`, every turn's text is duplicated. My first
aggregate read `"oneoneUnderstoodUnderstoodOKOK"`. This is the dangerous class:
nothing crashes, and every downstream metric — similarity, novelty, cost per
character — is quietly wrong by 2×.

Two more for the list: `pi` and `step` have no `--cwd` flag (passing one errors
and hangs; use the spawn `cwd` instead), and `agy` probes for WSL bash and burns
~61 seconds per turn when it's absent (set `SHELL` to Git Bash). And one that
caused false oracle alarms: a filename regex of `[^\s,.;]+` truncates `x.py` to
`x`, producing phantom-artifact violations for files that existed. The oracle's
own parser has to be held to the same evidentiary standard as the agents.

## What this buys you

The result is a system where "the agent said so" is never the end of the
argument. Every claim in every post in this series is traceable to a ledger
entry; every ledger entry is hash-chained; every hash chain is verifiable by a
single command; and the whole record sits where the agents can't touch it.

When I say "zero violations across 20 turns" in Part 4, that is not a vibe. It
is a query over a record the swarm could not have rewritten even if it wanted to.

---

*Next: [Part 3 — The Benchmark Nobody Runs](03-the-benchmark-nobody-runs.md):
four agent CLIs, one identical task, and why "$0.00 per turn" doesn't mean
what you think.*
