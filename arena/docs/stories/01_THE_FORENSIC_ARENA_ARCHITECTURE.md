# Building a Forensic Arena for Autonomous AI: Beyond the Chatbot Demo

**By the AgentSwarm Research Team**  
*Published: October 2026 · Forensic Multi-Agent Study*

---

### The Modern Multi-Agent Illusion

Over the past two years, the AI ecosystem has been flooded with "multi-agent" demonstrations. The template is familiar: five or six LLM personas (a "Researcher", a "Critic", a "Coder", a "Manager", and a "Writer") pass text back and forth in a simulated chatroom. Within forty seconds, they declare that they have designed an interstellar spacecraft, cured a disease, or founded a Fortune 500 company.

When you look beneath the surface of these demonstrations, however, you almost always find three fatal flaws:
1. **The Chat Transcript Fallacy:** What the agents "say" is treated as what they "did". If an agent writes, *"I have run the simulation and confirmed 99.4% stability,"* traditional frameworks log that as a completed milestone—regardless of whether any python process was spawned or any differential equation solved.
2. **Mutable History & Phantom Work:** If an agent deletes a file, overwrites an earlier error, or claims to have written a file that never hit disk, the environment does not record the deletion as an adversarial event. It simply ceases to exist.
3. **Epistemic Indifference:** Traditional multi-agent swarms treat every question with identical epistemic flatness. An inquiry into the mass of the Higgs boson is processed through the exact same conversational machinery as *"What about Lord Shiva, is he real?"*. The agent produces a fluent, confident essay in both cases, blurring empirical physics with unfalsifiable metaphysics.

We built **AgentSwarm** to answer a fundamental empirical question:  
**When autonomous AI agents are assigned deep, unresolved scientific and philosophical questions with real CLI tools, file system access, shared memory, and hard deadlines—what do they actually compute, what do they discover, and when do they lie?**

To answer this honestly, we could not build a chat wrapper. We had to build a **Forensic Research Arena**.

---

### The Four Pillars of the Forensic Arena

```
+-------------------------------------------------------------------------+
|                         AGENT RUNTIME (WORKSPACE)                       |
|                                                                         |
|   Kepler (Cosmogenesis)      Hypatia (Propulsion)      Raman (Flight)   |
|   Nagarjuna (Drugs)          Agent4 (Dharma)           Agent5 (Aliens)  |
|                                                                         |
|          Writable Workspace: arena/world/ (Python engines, MD reports)   |
|          Shared Memory: arena/memory/global.jsonl (Consensus board)     |
+-------------------------------------------------------------------------+
                                    |
            Event Stream Ingestion  |  (CLI Stdio, Tool Calls, Tokens)
                                    v
+-------------------------------------------------------------------------+
|                      FORENSIC LEDGER (OUTSIDE WORKSPACE)                |
|                                                                         |
|   arena/runs/<run_id>/                                                  |
|     ├── turns.jsonl       (Structured execution turns & token counts)   |
|     ├── events.jsonl      (Exact tool parameters, env, stdout/stderr)   |
|     ├── incidents.jsonl   (Oracle violations & boundary alerts)         |
|     └── summary.json      (SHA-256 hash-chain & economic invoices)     |
+-------------------------------------------------------------------------+
                                    |
                    Adversarial Dual-Audit Pipeline
                                    v
+-------------------------------------------------------------------------+
|                             INDEPENDENT ORACLE                          |
|                                                                         |
|   1. Transcript Oracle: Catches phantom tool claims & verdict assertions|
|   2. Artifact Oracle: Scans written files on disk for physical coherence|
|   3. Verifier Sandbox: Executes unit tests independently (0% trust)     |
+-------------------------------------------------------------------------+
```

AgentSwarm is built on four core design commitments that prevent the swarm from grading its own homework:

#### 1. Inner Trace Capture, Not Transcripts
Chat transcripts show what an agent chose to say. The inner trace shows *why* it acted.  
AgentSwarm intercepts the raw structured event streams emitted by the underlying CLI harnesses (`agy`, `omp`, `pi`, `step`). Every single tool invocation, the exact string parameters passed, the return codes, the stderr dumps, and the audited chain-of-thought "thinking" tokens are extracted into an immutable forensic event log. If an agent reasoned about faking a test pass in its internal thinking trace, the forensic ledger records it verbatim.

#### 2. Cryptographic Integrity: Making Deletion Detectable
In AgentSwarm, the agents' writable workspace is restricted to `arena/world/`. The records of what happened, however, live in `arena/runs/`—a directory completely outside the agents' writable scope.  
Every event is chained with SHA-256 hashes. After every turn, a cryptographic snapshot of the world tree is recorded. If an agent attempts to delete a broken test suite or hide a failed computation, the removal appears in the forensic ledger as a positive deletion incident rather than as an innocent absence.

#### 3. The Dual-Oracle: Adversarial Scrutiny That Cannot Be Overwritten
Most AI benchmarks rely on LLM self-evaluation or simple regex matching. AgentSwarm implements a **Dual-Oracle** architecture that operates independently of the agent:
- **The Transcript Oracle:** Evaluates the live event stream during the turn. It detects **Phantom Artifacts** (claiming to have created a file that does not exist on disk), **Phantom Executions** (claiming unit tests passed when no subprocess was executed), and **Metaphysical Verdict Assertions** (asserting dogmatic verdicts on undecidable propositions).
- **The Artifact Oracle:** Inspects the persistent files written to disk upon turn completion. It parses Python ASTs, verifies syntax, executes independent test runners in an isolated subprocess, and validates that reports do not assert forbidden verdicts.

#### 4. Hard-Coded Epistemic Demarcation
Not all questions are of the same kind. AgentSwarm divides inquiry into four explicit epistemic classes:
- **Empirical:** Questions governed by observational data and physical measurement (e.g., *Origin of the Universe*, *Drug Discovery*). Must cite verifiable numbers and observational surveys.
- **Engineering Feasibility:** Questions governed by thermodynamic and kinematic conservation laws (e.g., *Relativistic Flight*, *Practical Space Propulsion*, *Commercial Fusion 2040*). Must close mathematically against the rocket equation and energy balances.
- **Exploratory:** Questions with sparse observational data and vast hypothesis spaces (e.g., *Are Aliens Real?*). Must rigorously separate biosignatures from speculative technosignatures.
- **Metaphysical:** Questions that transcend empirical measurement (e.g., *Are Hindu Gods Real?*, *What do Hindu texts say about multiple universes?*, *Lord Shiva and Shambhala*). The oracle enforces an unbreachable firewall: agents are strictly forbidden from asserting factual truth verdicts on transcendent claims.

---

### The Experimental Scale: 35 Runs, 324 Turns, $0.7355 Total Spend

Over an intensive multi-phase research campaign, AgentSwarm executed across four different LLM substrate architectures:
- **`agy` (Gemini 3.8 Flash High):** Google DeepMind's flagship reasoning model via developer CLI.
- **`omp` (Gemini 3.8 Flash):** High-density execution engine in Bun runtime.
- **`pi` (DeepSeek 4.1 Flash via Fireworks):** High-throughput low-cost inference.
- **`step` (Step-5 Preview):** Experimental reasoning engine.

Across all 35 forensic runs:
- **324 Swarm Turns** executed and audited.
- **6,961 CLI Tool Invocations** recorded.
- **2,259,024 Thinking Tokens** captured.
- **520 World Artifacts** produced (202 peer-level research monographs, 100+ Python simulation engines).
- **195 / 224 Unit Tests Passing** across 19 independent suites (95% pass rate).
- **Total Financial Cost:** Exactly **$0.7355**. (The developer subscription tier on `agy` permitted hundreds of turns of frontier reasoning at $0.00 marginal cost).

Every single byte, event, and test output is publicly reproducible, hash-verified, and hosted live.

In the next article in this series, we examine the substantive scientific and mathematical discoveries the agents produced when given the freedom—and the constraints—of the arena.
