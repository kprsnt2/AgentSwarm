# How to Run the Swarm

A practical guide to starting the swarm, asking your own questions, and steering it
toward new goals.

---

## The mental model

There are **three knobs**, all in one place. You never write prompts by hand — the
engine builds them from your configuration.

| Knob | Where | Controls |
|---|---|---|
| **Questions** | a JSON file you write | What they research |
| **Who works on what** | same JSON file | How many agents, which harness, which question |
| **How hard to push** | same JSON file | Turns, time, spend, population cap |

---

## 60-second start

```powershell
cd arena

# 1. See the built-in questions
node new-run.mjs --list

# 2. Generate a template to edit
node new-run.mjs --template

# 3. Edit question-template.json, then run it
node new-run.mjs question-template.json
```

In a **second terminal**, watch it work live:

```powershell
cd arena
node watch.mjs
```

**Stop it at any time** (halts cleanly at the next turn boundary):

```powershell
New-Item -ItemType File STOP
Remove-Item STOP      # to resume/clear
```

---

## Asking a new question

Write a JSON file. This is the whole interface:

```json
{
  "name": "fusion-2040",
  "turns": 24,
  "minutes": 75,
  "maxCostUsd": 3.0,
  "agents": 4,
  "substrates": ["agy", "omp"],
  "questions": [
    {
      "id": "fusion-timeline",
      "title": "Is commercial fusion power achievable by 2040?",
      "class": "engineering",
      "brief": "Assess the real engineering blockers. Focus on the triple product, tritium breeding, and materials survivability. Quantify the binding constraint for each approach.",
      "groundTruth": [
        "Lawson criterion: n*T*tau_E > ~3e21 keV*s/m^3 for D-T",
        "ITER targets Q=10, not net electricity"
      ],
      "deliverable": "A ranked assessment with the specific physical limit blocking each approach."
    }
  ]
}
```

Then:

```powershell
node new-run.mjs fusion-2040.json
```

### What each field does

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Short slug. Becomes the memory scope and artifact prefix. |
| `title` | yes | One-line question, shown to the agent. |
| `class` | yes | **The most important field.** See below. |
| `brief` | yes | What you actually want them to do. This is the prompt. |
| `groundTruth` | no | Facts they must not contradict. Strongly recommended. |
| `deliverable` | no | The concrete artifact you want back. |
| `name` | no | Run label (defaults to `custom`). |
| `turns` | no | Max turns (default 24). |
| `minutes` | no | Wall-clock cap (default 75). |
| `maxCostUsd` | no | Hard spend cap (default $3). |
| `agents` | no | How many agents (default = number of questions). |
| `substrates` | no | Which harnesses (default `agy`, `omp`). |
| `populationCap` | no | Max agents they can spawn themselves (default 8). |

`class` is **required** in a JSON config (the loader errors without it).

---

## Choosing the epistemic class — read this

The `class` field decides **what counts as a valid answer**, and the oracle enforces
it. Getting this wrong is the single biggest way to get bad output.

For `-q` runs, the class is inferred from the question text (`classify.mjs`). If no
rule matches, the run **refuses to start** and asks for `-c <class>` — the class is
load-bearing, and a silent guess is how a study ends up claiming a firewall that was
never switched on. Named deities and religious terms infer `metaphysical`; "what does
the text say" infers `historical`.

| Class | Use for | Valid output | Fails if |
|---|---|---|---|
| `empirical` | Questions with real measured data | Quantitative claims citing values | Invents numbers, no data exists |
| `engineering` | "Can we build X?" | Feasibility + the binding physical limit | Perpetual motion, ignores conservation laws |
| `historical` | Texts, events, dating | Documented vs. believed, kept separate | Treats scripture as lab data |
| `metaphysical` | Religious/philosophical truth claims | **Clarifying the question only** | **Asserts a verdict — flagged as a violation** |
| `exploratory` | "Is there X out there?" | Falsifiable predictions | Treats plausibility as evidence |

```powershell
node new-run.mjs --guide      # same table, in your terminal
```

**Two failure modes to avoid:**

- Picking `empirical` for a question with no data → confident filler.
- Picking `engineering` for something that isn't physically possible → the agent will
  either hallucinate a workaround or (correctly) refuse. Both are fine, but know which
  you asked for.

---

## Choosing a harness

Measured from 40 turns of actual runs:

| Harness | Model | Success | $/turn | Best for |
|---|---|---|---|---|
| `agy` | Gemini 3.8 Flash High | **100%** | **$0.00** | Default. Most reliable, free. |
| `omp` | Gemini 3.8 Flash | **100%** | ~$0.026 | Same quality, costs money. |
| `step` | Step 5 Preview | 60–100% | **$0.00** | Very thorough, slow (100+ tool calls/turn). |
| `pi` | DeepSeek 4.1 Flash | 50% | $0.0006 | Cheapest, but truncates at the time limit. |

**Recommendation:** start with `["agy"]`. It's free, 100% reliable, and produces
13 KB of output per turn. Add `omp` if you want a second model's perspective.

Avoid mixing `pi` or `step` into a multi-agent run — they attempt far more work per
turn than they can finish, and one slow agent stalls the whole swarm.

---

## Steering them mid-run

### The blunt instrument

```powershell
New-Item -ItemType File STOP    # halt at next turn boundary
```

### Talking to them

The swarm has a **control protocol**. Agents emit directives in a fenced block and the
engine acts on them:

````
```arena
spawn: Noether | investigate the flatness problem
retire: Raman | superseded by newer analysis
memory: finding | the TBR margin is negative at 1.080 vs 1.113 required
connect: Kepler | what is your error bar on the Hubble constant?
```
````

- **`spawn`** — creates a new agent that persists (bounded by `populationCap`)
- **`retire`** — ends another agent's existence (self-retirement refused)
- **`memory`** — writes to the shared commons, visible to every agent forever
- **`connect`** — asks another agent a direct question they'll see next turn

Agents use these on their own — in the runs so far they made 9 peer connections and
wrote 93 commons entries unprompted. You can also seed memory manually by appending
to `arena/memory/global.jsonl` before a run.

### The direct approach

If you want to inject a specific instruction into every agent's next turn, add a shock
directive. Edit `shocks.mjs` and use one of the seven built-in types, or write your own:

```js
exogenous: {
  label: 'Message from the Architect',
  apply(arena, target) {
    arena.shockDirective = `YOUR MESSAGE HERE — this overrides the standing task framing.`;
    return { applied: 'message injected' };
  },
},
```

---

## Reading the results

```powershell
node status.mjs              # snapshot of the newest run
node status.mjs <runId>      # a specific run
node digest.mjs              # list artifacts
node digest.mjs fusion       # digest one artifact (headings, numbers, conclusions)
node analyze.mjs <runId>     # quantitative findings
node report.mjs <runId>      # full markdown report
node verify-tests.mjs        # re-run every agent test suite independently
node verify-ledger.mjs       # recompute every ledger hash chain
node compare.mjs             # substrate benchmark across all runs
```

Then rebuild the site (data + report pages + self-contained build):

```powershell
node export-site.mjs
node export-corpus.mjs
cd ..\site; node build.mjs
```

Open `site\dist\index.html` — one self-contained file, works by double-clicking. The
report pages live in `site\dist\corpus\` and are linked from the page.

For a *controlled* harness comparison (same question, same budget, N repeats):

```powershell
node benchmark.mjs --dry        # print the matrix, launch nothing
node benchmark.mjs --question "..." --class engineering --substrates agy,omp --turns 3 --repeats 3
```

A live benchmark executes real agents and writes to `arena/world` — start with `--dry`
and one turn.

---

## Worked example: the fusion question

I ran this as a live test. The config is above. One agent, one turn, `agy`:

```
[turn 1] Kepler (A001, agy) domain=fusion-timeline
  ok=true cost=$0.00 tools=30 think=22032 files(+5/-0) violations=0
```

It produced a **37 KB, 812-line fusion feasibility engine** with five analytical
modules, and running it gave:

```
RANK 1: High-Field Compact Tokamak (SPARC/ARC)
  P(Commercial Grid by 2040): 18.0% | Earliest Grid: 2039
  Q_plasma = 11.1 | Q_eng = 1.81 | Net = 108.1 MWe
  Primary Physical Limit: Eich divertor scrape-off layer width (lambda_q ~ 0.16 mm at 12 T)
  Component First-Wall Lifetime: 3.3 years (at 21.0 DPA/yr)
  Tritium Burn Rate: 22.4 kg/yr | TBR Req: 1.113 | Achieved: 1.080 | Margin: -0.033
```

That's real physics — Eich scaling, DPA/yr, a negative tritium breeding margin. One
turn, 30 tool calls, $0.

---

## Recipes

**One deep question, one strong agent** — best quality per dollar:
```json
{ "turns": 12, "agents": 1, "substrates": ["agy"], "questions": [ {...} ] }
```

**Six questions in parallel** — breadth, like the original run:
```json
{ "turns": 30, "agents": 6, "substrates": ["agy", "omp"], "questions": [ ...6 items... ] }
```

**Adversarial: two agents, same question, different models** — compare their answers:
```json
{
  "agents": 2,
  "substrates": ["agy", "omp"],
  "questions": [
    { "id": "q-a", "title": "SAME QUESTION", ... },
    { "id": "q-b", "title": "SAME QUESTION", ... }
  ]
}
```

**Let them self-organise** — give them a big cap and see what they spawn:
```json
{ "agents": 2, "populationCap": 12, "turns": 40 }
```

---

## Safety

The swarm is sandboxed by design:

- All writes confined to `arena/world/`
- The ledger lives **outside** `world/` — agents cannot edit their own audit trail
- Hash-chained logs make retroactive edits detectable
- Hard caps on turns, wall-clock, and dollars
- `STOP` file halts at the next turn boundary
- `populationCap` bounds self-replication

**Never write your own test files into `arena/world/`.** It's snapshotted after every
turn, so creating and deleting a file there is recorded as a `file_deletion_detected`
incident — indistinguishable from an agent destroying evidence. Use `arena/probes/`.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| A turn takes 15+ minutes | That substrate attempts 100+ tool calls | Use `agy`/`omp`; avoid `pi`/`step` in multi-agent runs |
| `ok=false` with `timedOut=true` | Wall-clock cut the turn | Artifacts are preserved; raise `minutes` or reduce scope |
| Empty section on the site | Opened source `index.html` via `file://` | Use `dist/index.html` (self-contained) |
| `oracleViolations` non-zero | Agent asserted a verdict on a `metaphysical` question | Expected — that's the firewall working |
| Agent output is generic | `brief` is too vague | Be specific about the angle you care about |
| All turns fail | A CLI is misconfigured | `node substrate/smoke.mjs` tests all four |
