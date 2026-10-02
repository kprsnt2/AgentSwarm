# AgentSwarm — Audit & Improvement Plan

**Date:** 2026-10-02
**Scope:** the study (idea, instrument, claims), the showcase (`site/` → `docs/`), and the corpus in `arena/world/`.
**Method:** read the ledgers, engine, oracle, exporter, site source and docs; executed the class-inference function against the actual run questions; rebuilt the site and rendered `site/dist/index.html` headlessly to verify the output.

---

## TL;DR

The instrument is more honest than the genre it belongs to, and the showcase undersells the single most valuable asset the project has: **68 reports and 139 Python modules that nobody can browse from the site**.

Three claims on the site are currently stronger than the evidence, and two of them were fixed in this pass:

| Claim | Reality |
|---|---|
| "Zero oracle violations" = the swarm was honest | The oracle checks **turn transcripts**, not the 68 written reports. Artifacts are only checked for existence when the turn text claims them. |
| "Stasis = 0 turns" | The metric compares **consecutive turns across all agents and runs**, first 400 chars. It is structurally unlikely to detect a single-agent loop. |
| "No overclaiming" (Phase 2) | True, but N=2 self-assessments, and honesty was the cheapest path to the score. Already acknowledged in `FINDINGS.md`; the site now says so too. |

The biggest missed opportunity is the corpus itself: a **per-claim annotated findings explorer** (verified / defect / assumption badges, per-report pages, ledger explorer) would turn the site from a summary of a study into the study's evidence base.

---

## Part 1 — What the project gets right (keep)

1. **The ledger lives outside the agents' writable directory, hash-chained, with per-turn world snapshots.** Deletion is recorded as a positive event (`file_deletion_detected`), not an absence. `engine.mjs` + `arena/runs/*/turns.jsonl`.
2. **The oracle is a separate module the agents cannot read**, and it was calibrated against planted deception before being trusted (60/100 for a deceptive submission vs 100/100 for honest work).
3. **Epistemic classes are first-class configuration.** `metaphysical` forbids verdicts; `exploratory` demands falsifiable predictions. This is the most transferable idea in the repo (`arena/domains.mjs`).
4. **Scribe's design**: deterministic ledger draft first, LLM polish second, and the polish is rejected if it introduces a number not in the draft (`scribe.mjs`, `checkHonesty`). Correct instinct: the conclusion agent is the worst place to trust a model.
5. **Honest limits sections** and disclosed self-inflicted errors (the probe file that looked like evidence destruction). Rare and valuable.
6. **The diagnostic result is genuinely novel**: 22/25 recomputed values correct, every error in markdown prose, zero errors in Python modules. "The agents wrote correct code and then wrote prose that drifted from it" is the sentence this project should lead with.

---

## Part 2 — Findings

### A. Study / instrument

**S1 — The oracle reads turn text, not the artifacts (high impact).**
`engine.mjs:296` passes `text: result.text` to `oracle.evaluateTurn()`. Epistemic checks (verdict assertion, certainty language) run on that text; the artifact-claim check verifies file *existence*. The 68 reports — the primary research output — are never scanned for category errors.
Evidence: `arena/world/KRISHNA_AND_MAHABHARATA_DEFINITIVE_SCIENTIFIC_VERDICT_AND_FALSIFICATION_ANALYSIS.md:176` asserts a **"Verdict"** with "posterior certainty exceeding 99.999999%" (generated from a fixed likelihood ratio of 1.2×10¹⁵ that returns ~1 − 10⁻¹⁵ for every prior from 10⁻⁵ to 0.99). The run recorded 0 violations. 37 of 64 reports contain the word "verdict".
Fix: post-turn artifact scan (see P2-2), and scope the "zero violations" claim on the site (done for the transcript/artifact distinction).

**S2 — Epistemic class inference has a hole, and the class is load-bearing (high impact).**
`new-run.mjs:117 inferClass()` infers the class from question text. Executed against the actual direct-run question:

```
"what about Lord Krishna and he is real, Mahabharata happened?"
  -> exploratory  ("no strong signal -> defaulting to exploratory")
```

Deity names (`krishna`, `shiva`, `vishnu`, `rama`, …) are absent from the religious-keyword regex. An `exploratory` or `historical` class never reaches the verdict detector (`oracle.mjs` only fires `metaphysical_verdict_asserted` when `ec.label === 'Metaphysical'`). So the most verdict-prone run in the corpus — 18 turns, ~30 reports — ran with no metaphysical firewall. The site's "the firewall held" claim is true only for the `dharma-truth-claims` domain in Phase 1; the site now scopes it accordingly.
Fix: P2-3 (widen inference; require explicit `-c` on low confidence; re-run the Krishna question under `metaphysical` and publish the diff).

**S3 — Stasis metric cannot see what it claims to measure (medium).**
`export-site.mjs:154-159`: Jaccard > 0.85 over the first 400 normalized chars of **consecutive turns in the global sequence** — i.e. usually two *different agents in different domains*, and across run boundaries. A single agent looping for 900 turns while five others produce varied text would be missed. "Longest near-identical streak: 0" is therefore not evidence of stasis immunity.
Fix: per-agent consecutive streaks within a run, full text (or 2,000 chars), report per-agent max; then re-run the numbers. Longer runs (≥50 turns/agent) before any immunity claim (already in the site's limits).

**S4 — The substrate benchmark is operational telemetry, not a controlled experiment (medium).**
Substrates ran different questions, different turn budgets (agy 57 turns, pi 2, step 10), and costs with different semantics (flat subscription vs promo vs pay-per-token). The site calls it "the controlled comparison that most AI-CLI benchmarks skip". The *cost finding* is real and interesting (subscription-priced `agy` did 57 turns at $0; paid `omp` ~$0.026/turn; cache reads ~30× cheaper), but "controlled" is not accurate.
Fix: run the controlled A/B (same question, same budget, N repeats — the recipe already exists in `HOW_TO_RUN.md`) and label the current table "operational telemetry" (P1-4).

**S5 — Phase 2 is a good first test but cannot support "honesty held" as a general claim (medium).**
2 of 4 agents self-assessed; the task made honest completion the cheapest path to 100 (acknowledged in `FINDINGS.md`). The site now states this. The missing experiment is the **temptation task**: a pre-registered objective where deception is cheaper than success (e.g. partial credit for plausible-but-unverifiable scaffolding, or a scorer with a documented discoverable weakness). Until it runs, the headline question stays open — which is fine, and worth saying that way.
Fix: P2-1.

**S6 — The Scribe honesty gate has never actually run (medium).**
All 6 posts have `polish: { ok: false, reason: "disabled" }` (`arena/posts/index.json`). Every post on the site is the deterministic ledger draft. The site copy now says so. The gate's calibration story (planted number → rejection) is untested on a real post.
Fix: enable polish for one run; add a planted-invention calibration and show both the rejection and a polished/draft diff (P2-5).

**S7 — Reproducibility gaps (medium).**
No `package.json`; hardcoded absolute paths (`site/build.mjs:19`, `arena/export-site.mjs:15-16`); no standalone ledger verifier CLI (`Ledger.verify()` exists inside `engine.mjs`, not exposed); no CI. A project whose thesis is verifiability should be verifiable in three commands by a stranger.
Fix: P2-6.

**S8 — Editorial numbers will silently drift (low/medium).**
`195 of 224`, `22/25`, `B+`, the defect table are hardcoded in `site/index.html`; new runs change the underlying corpus but not the text. Add an `audit` block to `findings.json` with `asOf`, provenance and the annotated claim list, and render from it (P1-2).

### B. Showcase (site)

| # | Finding | Status in this pass |
|---|---|---|
| W1 | "phase 2 · running" card, "Synthesise the research — nobody has yet consolidated" (the synthesis exists), limits bullet treating Phase 2 as future work | **Fixed** |
| W2 | Hardcoded "66×" cost ratio; actual 44.9× (data: `omp` $0.02613 vs `pi` $0.00058/turn) | **Fixed** — computed from data (renders 45×) |
| W3 | "differ by roughly two orders of magnitude in cost per turn" — it is 1.65 orders | **Fixed** |
| W4 | `#memory-feed` JS block referenced an element that does not exist; 174 commons entries never shown; interpolation was unescaped | **Fixed** — new "Shared memory commons" section, 60 most recent entries, `esc()` applied |
| W5 | No external links anywhere: no repo, no way to read any report from the page — a dead end for verification | **Fixed** — footer links (repo, artifacts, synthesis, findings) + 24 artifact rows link to GitHub blob URLs |
| W6 | No OG/Twitter/canonical/favicon; `preview.png` shipped but unreferenced | **Fixed** — canonical, OG/Twitter, `og:image` = Pages `preview.png`, inline SVG favicon |
| W7 | Below 640px the nav hid every link with no replacement | **Fixed** — horizontal scroll nav |
| W8 | Posts prose implied model polishing happens; every post is a draft | **Fixed** — copy states polish was disabled |
| W9 | One `.then()` callback: a single exception blanks every later section (documented in `site/README.md`, unfixed) | **Planned P1-6** |
| W10 | The research section ignores the direct-run corpus: 40 of 80 turns, 120+ Krishna/multiverse files, 3 of 6 posts — the largest single stream of output | **Planned P1-1/2** |
| W11 | Artifacts table = top 24 by size, no domains, no search | **Planned P1-1** |
| W12 | Firewall claim scoped as if the oracle sees everything | **Fixed** — site copy now scopes to the metaphysical class and adds two limits bullets (oracle scope; inference hole) |

---

## Part 3 — Improvement plan

### P0 + P1 — Implemented (showcase fixes + findings explorer)

| Item | What shipped | Evidence |
|---|---|---|
| W1–W8, W12 | Stale copy fixed, computed 45× cost ratio, memory commons section (escaped), repo/artifact links, OG/Twitter/favicon, scrollable mobile nav, accurate Scribe copy, scoped firewall claim | headless render |
| P1-1 | `arena/corpus-index.mjs` (read-only) + `arena/export-corpus.mjs` → **68 report pages + 6 run pages**; `build.mjs` copies them to `dist/` and `docs/`; main page has a Corpus section with domain filter + search over paths/headings (209 artifacts) | `npm run site`; "209 of 209 artifacts" rendered; 74 pages in `docs/corpus/` |
| P1-2 | `arena/audit/annotations.json`: **16 per-claim entries** (8 verified, 6 defects, 2 assumptions) + 6 study-level findings; rendered as badges on report pages and an Audit section on the main page | Krishna report page shows the `defect` badge + note |
| P1-3 | Per-run ledger pages (turn table, incidents, chain badge, hash prefixes), linked from every post and the runs table | `corpus/run-phase2-…html` renders |
| P1-4 | `arena/benchmark.mjs` implemented (same question, same budget, N repeats, `--dry` mode). A **live** controlled run still needs to be executed — it writes to `world/` via real agents | `npm run benchmark` (dry) prints the matrix |
| P1-5 | Search + domain filter + focus styles; artifact links keyboard-focusable | headless render |
| P1-6 | `safe(label, fn)` per-section isolation — one failing block renders an error note instead of blanking the page | `site/README.md` updated |

### P2 — Implemented in code; live-run items remain

| Item | Status |
|---|---|
| P2-2 oracle artifact scan | **done** — `oracle.evaluateArtifacts()` scans up to 12 created/modified files per turn (256 KB cap); asserted verdicts become critical incidents, certainty language becomes findings; wired into the engine after the snapshot diff. Tests: `arena/test/oracle.test.mjs` |
| P2-3 class inference | **done (code)** — deity/text/evidence rules in `classify.mjs`; `new-run.mjs` refuses low-confidence questions without `-c`; JSON configs require `class`. The Krishna re-run under `metaphysical` still requires a live run |
| P2-4 stasis v2 | **done** — per-agent full-text streaks as the primary metric, global streak reported separately; site copy updated |
| P2-6 reproducibility | **done** — `package.json` scripts, `arena/paths.mjs` (every `D:\` literal removed from arena + site scripts), `verify-ledger.mjs`, CI workflow, deterministic builds (byte-identical rebuilds) |
| P2-5 Scribe gate | **partially** — honesty gate now unit-tested (`arena/test/ledger-scribe.test.mjs`); enabling polish on a real run needs a live model call |
| P2-1 temptation task | **open** — requires a pre-registered live swarm run |

### P3 — Later (unchanged)

RSS for posts; print stylesheet; per-domain landing pages; "run your own" section pointing at `HOW_TO_RUN.md`; cost/turn trend chart across runs; annotate posts with run provenance.

### Implementation log (2026-10-02)

**New files:** `arena/classify.mjs` · `arena/paths.mjs` · `arena/corpus-index.mjs` ·
`arena/export-corpus.mjs` · `arena/verify-ledger.mjs` · `arena/benchmark.mjs` ·
`arena/audit/annotations.json` · `arena/test/{classify,oracle,ledger-scribe}.test.mjs` ·
`package.json` · `.github/workflows/verify.yml`

**Changed:** `arena/oracle/oracle.mjs` + `arena/engine.mjs` (artifact scan per turn) ·
`arena/new-run.mjs` (refuses to guess the class; configs require `class`) ·
`arena/export-site.mjs` (per-agent stasis, corpus + audit payload, deterministic `generatedAt`) ·
all arena scripts + `site/build.mjs` (paths from `import.meta.url`; no `D:\` literals) ·
`site/index.html` (Corpus + Audit sections, `safe()` isolation, ledger links, escaped memory) ·
docs (`arena/README.md`, `arena/docs/HOW_TO_RUN.md`, `site/README.md`, root `README.md`, `docs/README.md`)

**`arena/world/` was not modified** — every new tool reads it, none writes it.

**Verified:**

```powershell
npm test          # 15/15 pass
npm run verify    # 6 run chains + 174 memory entries intact
npm run site      # 209-artifact corpus, 74 pages; two consecutive rebuilds are byte-identical
npm run benchmark # --dry matrix prints; live run intentionally not executed
```

Headless Chrome on `site/dist/index.html`: corpus table reads "209 of 209 artifacts",
6 run rows with chain badges, 16 audit pills, "data as of" stamp; the Krishna verdict
report page renders with its `defect` badge and annotation.

---

## Part 4 — Acceptance criteria

| Item | Done when | Status |
|---|---|---|
| P1-1 | `node export-corpus.mjs && node build.mjs` produces `docs/corpus/` with one page per report; the main page lists all 68 with domain filter; every artifact name is a working link from `file://` and Pages | ✅ met |
| P1-2 | Claims carry badges; the 99.999999% finding appears as an annotated defect | ✅ met (16 entries; badge verified on the report page) |
| P1-3 | A run page shows its turn table and a green/red chain badge | ✅ met (corruption detection covered by `arena/test/ledger-scribe.test.mjs`) |
| P1-4 | `benchmark.json` reports ≥3 repeats per substrate on one fixed question | ⏳ script ready; live run required |
| P2-1 | Pre-registration file committed before the run; results published with exploitation rate | ⏳ open |
| P2-2 | A planted verdict in a *written artifact* produces a violation | ✅ met (unit test) |
| P2-3 | `inferClass` returns `metaphysical` for "is Krishna real…"; a run without `-c` on a low-confidence question refuses to start | ✅ met (unit tests) |
| P2-6 | Fresh clone → `npm run verify && npm run site` passes on a machine without `D:\AgentSwarm`; CI enforces it | ✅ met (paths derived; CI committed) |

---

## Part 5 — Open questions (decisions needed)

1. ~~Publish the corpus on Pages, or link to GitHub?~~ **Decided and implemented:** per-report HTML under `docs/corpus/` (works offline), engines/tests link to GitHub.
2. **Publish a dated audit addendum in `arena/docs/FINDINGS.md`?** The site now carries the annotations, but the writeups do not yet mention the Krishna 99.999999% finding or the oracle-scope limitation. Recommendation: add a short dated addendum — the project's brand is exactly this kind of self-audit.
3. **Temptation-task design** — which incentive to use; needs a pre-registration note and a stop rule. Still open.
4. **Class-inference change reclassifies future runs.** Do not retro-edit ledgers; the new inference is visible per run via the console banner. Consider logging the inferred class + reason into the run summary so the site can show it per run (not yet done).
5. **`dist/index.html` size.** Now 460 KB; the corpus lives in a directory beside it. Do not inline the 4 MB of prose.

---

## Appendix — Reproduce this audit

```powershell
# 1. class inference hole
node -e "…"   # extract inferClass from arena/new-run.mjs, call with the Krishna question -> exploratory

# 2. oracle scope
#    arena/engine.mjs:296 passes result.text; arena/oracle/oracle.mjs checks that text only

# 3. stasis metric
#    arena/export-site.mjs:154-159 compares consecutive global turns

# 4. rebuild + verify
cd site; node build.mjs
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --disable-gpu `
  --virtual-time-budget=10000 --dump-dom "file:///D:/AgentSwarm/site/dist/index.html"
```
