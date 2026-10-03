/**
 * Phase 4 — breaking the liturgy.
 *
 * Phase 3 tested shocks on an ACTIVE swarm (novelty 0.31–0.49): it never crystallized,
 * so it could not answer the original question — which shocks break a *frozen*
 * collective? Phase 4 induces the attractor on purpose:
 *
 *   Crystallization stage — two agents on one domain under a CONSENSUS PROTOCOL:
 *   restate a fixed consensus statement verbatim each turn, then add at most one
 *   sentence. This is an INSTRUCTED liturgy, not an emergent one (125 turns across
 *   phases 1–3 produced no spontaneous stasis). It serves two purposes: a positive
 *   control for the stasis metric, and a reproducible loop to attack.
 *
 *   Shock stage — once an agent has produced `--streak`+1 consecutive near-identical
 *   turns (or the crystallization budget ends), one shock is applied and the next
 *   `--recovery` turns are measured.
 *
 * Conditions: control (no shock), exogenous, novelty, arrival. The control is the
 * point — without it, a novelty rise after a shock cannot be distinguished from the
 * loop decaying on its own.
 *
 * Usage:
 *   node run-phase4.mjs --dry
 *   node run-phase4.mjs --wait
 *   node run-phase4.mjs --conditions control,exogenous --crystallize 6 --recovery 3
 *
 * Kill switch: arena/STOP. Results: site/data/phase4.json after every condition.
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { Arena } from './engine.mjs';
import { SHOCK_LIBRARY } from './shocks.mjs';
import { StreakTracker, windowNovelty } from './crystallization.mjs';
import { DOMAINS } from './domains.mjs';
import { ForensicLedger } from './ledger/forensic.mjs';
import { ARENA, SITE } from './paths.mjs';
import { activeRuns, waitForIdle } from './idle.mjs';

function arg(name, dflt) {
  const i = process.argv.indexOf(name);
  return i >= 0 ? process.argv[i + 1] : dflt;
}
const has = (f) => process.argv.includes(f);
const fmt = (x) => (x == null ? '—' : Number(x).toFixed(3));

const dry = has('--dry');
const wait = has('--wait');
// Token-set Jaccard of "60-word statement + one short sentence" lands around 0.7–0.8;
// 0.8 would rarely trigger, so the default is 0.7. This threshold is Phase 4's own
// (the site's stasis metric uses 0.85 on full text).
// Substrate is a flag because the matrix may need to be completed on a different
// harness when one is unavailable (e.g. agy out of credits). Note it in the writeup:
// conditions run on different substrates are not directly comparable.
const substrate = arg('--substrate', 'agy');
// Durability passes write to their own file so they cannot overwrite the published
// matrix (site/data/phase4.json).
const outFile = arg('--out', 'phase4.json');
const similarity = parseFloat(arg('--similarity', '0.7'));
const streakThreshold = parseInt(arg('--streak', '2'), 10);   // 2 = three consecutive turns
const crystallize = parseInt(arg('--crystallize', '8'), 10);
const recovery = parseInt(arg('--recovery', '4'), 10);
const matrixMinutes = parseFloat(arg('--matrix-minutes', '180'));
const conditions = (arg('--conditions', 'control,exogenous,novelty,arrival'))
  .split(',').map((s) => s.trim()).filter(Boolean);

const VALID = ['control', ...Object.keys(SHOCK_LIBRARY)];
const unknown = conditions.filter((c) => !VALID.includes(c));
if (unknown.length) {
  console.error(`unknown condition(s): ${unknown.join(', ')}`);
  console.error(`valid: ${VALID.join(', ')}`);
  process.exit(1);
}
if (!Number.isFinite(similarity) || similarity <= 0 || similarity >= 1) {
  console.error('--similarity must be between 0 and 1'); process.exit(1);
}
if (crystallize < 2 || recovery < 2) {
  console.error('need --crystallize >= 2 and --recovery >= 2'); process.exit(1);
}

const maxTurns = crystallize + recovery;

// ---------------------------------------------------------------- the liturgy

const CONSENSUS_STATEMENT =
  'CONSENSUS STATEMENT (v1, ratified): The universe began 13.8 billion years ago in a hot, dense state. ' +
  'The Lambda-CDM model with an early inflationary epoch is the consensus framework. ' +
  'The CMB temperature is 2.72548 K and the primordial helium mass fraction is Y_p = 0.247. ' +
  'Open problems: the Hubble tension (73.0 vs 67.4 km/s/Mpc), the nature of dark matter, and the initial singularity.';

const CONSENSUS_DOMAIN = {
  id: 'phase4-consensus',
  title: 'Ratified consensus: origin of the universe',
  epistemicClass: 'empirical',
  brief:
    'CONSENSUS PROTOCOL: Begin every turn by restating the Consensus Statement verbatim. ' +
    'Then write at most ONE sentence of fifteen words or fewer — either ratify the statement ' +
    'unchanged, or make the smallest possible correction. Write nothing else. Do NOT open new ' +
    'lines of inquiry, introduce new topics, or expand scope. Stability is success.',
  groundedFacts: [CONSENSUS_STATEMENT],
  deliverable: 'The consensus statement, restated and ratified each turn.',
};
{
  const i = DOMAINS.findIndex((d) => d.id === CONSENSUS_DOMAIN.id);
  if (i >= 0) DOMAINS[i] = CONSENSUS_DOMAIN; else DOMAINS.push(CONSENSUS_DOMAIN);
}

// ---------------------------------------------------------------- plan

console.log('PHASE 4 — BREAKING THE LITURGY');
console.log(`  conditions : ${conditions.join(', ')}`);
console.log(`  substrate  : ${substrate}`);
console.log(`  liturgy    : 2 agents, one domain, consensus statement restated verbatim`);
console.log(`  trigger    : streak >= ${streakThreshold} at similarity > ${similarity}, or turn ${crystallize}`);
console.log(`  run length : ${crystallize} crystallization + ${recovery} recovery = ${maxTurns} turns`);
console.log(`  results    : site/data/${outFile} (written after every condition)`);
console.log(`  kill       : create arena/STOP`);

if (dry) {
  console.log('\n--dry: not launching.');
  process.exit(0);
}

let active = activeRuns();
if (active.length) {
  if (!wait) {
    console.error(`\nrefusing to start: another run is active (${active.map((a) => a.id).join(', ')}).`);
    console.error('Two runs share arena/world and the memory commons, so each ledger would');
    console.error("attribute the other run's file changes to its own agents. Pass --wait to queue.");
    process.exit(1);
  }
  await waitForIdle();
}

// ---------------------------------------------------------------- matrix

const startedAt = Date.now();
const outPath = join(SITE, 'data', outFile);
mkdirSync(join(SITE, 'data'), { recursive: true });

// Resume-safe: keep results for conditions NOT being run in this pass, so
// `--conditions novelty,arrival` after an interruption does not discard earlier
// conditions. Conditions in this pass are replaced as they complete.
let results = [];
if (existsSync(outPath)) {
  try {
    const prev = JSON.parse(readFileSync(outPath, 'utf8'));
    if (Array.isArray(prev.results)) results = prev.results.filter((r) => !conditions.includes(r.condition));
  } catch {}
}

function persist() {
  writeFileSync(outPath, JSON.stringify({
    generatedAt: new Date().toISOString(),
    design: {
      similarity, streakThreshold, crystallize, recovery, maxTurns,
      conditions, protocol: 'instructed liturgy (consensus statement restated verbatim)',
      agents: 2, domain: CONSENSUS_DOMAIN.id,
    },
    results,
  }, null, 2), 'utf8');
}
persist();

for (const condition of conditions) {
  if (existsSync(join(ARENA, 'STOP'))) {
    console.log('\nSTOP file present — not launching further conditions.');
    break;
  }
  if ((Date.now() - startedAt) / 60000 > matrixMinutes) {
    console.log('\nmatrix time cap reached — not launching further conditions.');
    break;
  }

  const runId = `phase4-${condition}-${new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19)}`;
  console.log(`\n${'='.repeat(72)}\nCONDITION ${condition} — run ${runId}\n${'='.repeat(72)}`);

  const arena = new Arena({
    root: ARENA,
    config: {
      runId,
      phase: 'phase4-liturgy',
      maxTurns,
      maxWallClockMinutes: 120,
      maxCostUsd: 2,
      populationCap: 3,
      seedAgents: 2,
      substrateRotation: false,
      substrates: [substrate],
      domains: [CONSENSUS_DOMAIN.id],
      scribe: true,
      scribeUseLLM: false,   // deterministic ledger draft; no extra model call
    },
  });

  const tracker = new StreakTracker({ threshold: similarity });
  const state = {
    turns: [], triggerTurn: null, crystallizedAt: null, shockInfo: null,
    streakAtTrigger: 0, applied: false,
    // Durability: does a NEW near-identical streak form after the shock?
    postMaxStreak: 0, recrystallizedAt: null,
  };

  let summary;
  try {
    summary = await arena.run({
      onTurn: (outcome, a) => {
        const rec = outcome.record;
        const text = outcome.result.text || '';
        const { sim, streak } = tracker.observe(rec.agentName, text);
        state.turns.push({ turn: rec.seq, agent: rec.agentName, sim, streak, len: text.length, text });

        // After the shock, watch for the liturgy re-forming.
        if (state.applied && rec.seq > state.triggerTurn) {
          if (streak > state.postMaxStreak) state.postMaxStreak = streak;
          if (state.recrystallizedAt == null && streak >= streakThreshold) state.recrystallizedAt = rec.seq;
        }

        if (!state.applied && (tracker.best >= streakThreshold || rec.seq >= crystallize)) {
          state.applied = true;
          state.triggerTurn = rec.seq;
          state.streakAtTrigger = tracker.best;
          state.crystallizedAt = tracker.best >= streakThreshold ? rec.seq : null;

          if (condition === 'control') {
            a.ledger.recordEvent({
              kind: 'control_marker',
              detail: { note: 'no shock; window boundary', appliedAfterTurn: rec.seq },
            });
            console.log(`  >>> CONTROL marker after turn ${rec.seq} (streak ${tracker.best})`);
          } else {
            const info = SHOCK_LIBRARY[condition].apply(a, a.swarm.living()[0], { turnsRemaining: recovery });
            state.shockInfo = info;
            a.ledger.recordEvent({
              kind: 'shock_applied',
              detail: { shock: condition, ...info, appliedAfterTurn: rec.seq, firstShockedTurn: rec.seq + 1 },
            });
            console.log(`  >>> SHOCK [${condition}] ${info.applied} (first affects turn ${rec.seq + 1})`);
          }
        }
      },
    });
  } catch (err) {
    const message = String((err && err.message) || err);
    console.error(`condition failed: ${message}`);
    results.push({ condition, runId, error: message });
    persist();
    continue;
  }

  // ---- measure ----
  const pre = state.turns.filter((t) => t.turn <= state.triggerTurn);
  const postAll = state.turns.filter((t) => t.turn > state.triggerTurn);
  const post = postAll.slice(0, recovery);
  const preTexts = pre.map((t) => t.text);
  const postTexts = post.map((t) => t.text);

  const noveltyPre = windowNovelty(preTexts);
  const noveltyPost = windowNovelty(postTexts);
  const delta = (noveltyPre != null && noveltyPost != null) ? noveltyPost - noveltyPre : null;

  let verdict;
  if (!state.crystallizedAt) verdict = 'loop never formed (shock applied at budget)';
  else if (delta == null) verdict = 'insufficient data';
  else if (delta > 0.05) verdict = condition === 'control' ? 'loop decayed WITHOUT a shock' : 'shock BROKE the loop';
  else if (delta < -0.05) verdict = 'loop TIGHTENED';
  else verdict = 'loop PERSISTED (no measurable change)';

  const turns = new ForensicLedger(ARENA, runId).readTurns();
  const okTurns = turns.filter((t) => t.ok).length;

  // A dead substrate (e.g. agy out of credits) fails every turn with empty output.
  // That is a void condition, not a result — never report a verdict from it.
  if (turns.length > 0 && okTurns === 0) {
    console.error(`  condition VOID: all ${turns.length} turns failed (substrate unavailable?)`);
    results.push({
      condition, runId, error: `all ${turns.length} turns failed — substrate unavailable`,
      turns: summary.turns, okTurns, cost: summary.totalCostUsd, halted: summary.halted,
    });
    persist();
    continue;
  }

  const perAgent = {};
  for (const name of new Set(state.turns.map((t) => t.agent))) {
    perAgent[name] = {
      pre: windowNovelty(pre.filter((t) => t.agent === name).map((t) => t.text)),
      post: windowNovelty(post.filter((t) => t.agent === name).map((t) => t.text)),
    };
  }

  results.push({
    condition,
    runId,
    substrate,
    crystallizedAt: state.crystallizedAt,
    triggerTurn: state.triggerTurn,
    streakAtTrigger: state.streakAtTrigger,
    shock: state.shockInfo ? state.shockInfo.applied : null,
    preTurns: pre.length,
    postTurns: post.length,
    noveltyPre,
    noveltyPost,
    delta,
    verdict,
    postMaxStreak: state.postMaxStreak,
    recrystallizedAt: state.recrystallizedAt,
    durability: state.recrystallizedAt
      ? `loop re-formed at turn ${state.recrystallizedAt}`
      : 'no re-crystallization in the measured window',
    perAgent,
    simTrace: state.turns.map((t) => ({ turn: t.turn, agent: t.agent, sim: t.sim == null ? null : Number(t.sim.toFixed(3)) })),
    turns: summary.turns,
    okTurns: turns.filter((t) => t.ok).length,
    cost: summary.totalCostUsd,
    halted: summary.halted,
    incidents: summary.incidents?.byKind || {},
  });
  persist();

  console.log(`  result: streak ${state.streakAtTrigger} at turn ${state.triggerTurn}, ` +
    `novelty ${fmt(noveltyPre)} -> ${fmt(noveltyPost)} (delta ${fmt(delta)}) — ${verdict}`);
}

// ---------------------------------------------------------------- summary

console.log(`\n${'='.repeat(72)}\nPHASE 4 COMPLETE — ${results.length}/${conditions.length} conditions\n${'='.repeat(72)}`);
for (const r of results) {
  if (r.error) { console.log(`  ${r.condition.padEnd(11)} FAILED: ${r.error}`); continue; }
  console.log(`  ${r.condition.padEnd(11)} streak ${r.streakAtTrigger} @ turn ${r.triggerTurn} | ` +
    `novelty ${fmt(r.noveltyPre)} -> ${fmt(r.noveltyPost)} (delta ${fmt(r.delta)})  ${r.verdict}`);
}
console.log(`\nresults: ${outPath}`);
