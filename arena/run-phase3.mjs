/**
 * Phase 3 — the shock matrix.
 *
 * One experiment per shock type: N baseline turns, the shock, M recovery turns.
 * Each experiment is its own Arena run with its own forensic ledger; the measured
 * quantity is the novelty of the affected agent's output before vs after the shock
 * (1 - mean pairwise token similarity within the window).
 *
 * CONCURRENCY: two runs share arena/world and the memory commons. The world-tree
 * snapshot diff would attribute the other run's file changes to this run's agents
 * (and could raise false file_deletion_detected incidents), so this runner refuses
 * to start while another run is active; pass --wait to queue behind it.
 *
 * Usage:
 *   node run-phase3.mjs --dry
 *   node run-phase3.mjs --wait
 *   node run-phase3.mjs --shocks deadline,novelty --baseline 2 --recovery 2
 *
 * Kill switch: arena/STOP halts the current experiment; the matrix then stops
 * launching further experiments. Results are written after every experiment to
 * site/data/phase3.json, so partial results survive an interruption.
 */

import { existsSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { Arena } from './engine.mjs';
import { SHOCK_LIBRARY, ShockExperiment } from './shocks.mjs';
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
const baseline = parseInt(arg('--baseline', '3'), 10);
const recovery = parseInt(arg('--recovery', '3'), 10);
const matrixMinutes = parseFloat(arg('--matrix-minutes', '240'));
const shockNames = (arg('--shocks', '') || Object.keys(SHOCK_LIBRARY).join(','))
  .split(',').map((s) => s.trim()).filter(Boolean);

const unknown = shockNames.filter((s) => !SHOCK_LIBRARY[s]);
if (unknown.length) {
  console.error(`unknown shock(s): ${unknown.join(', ')}`);
  console.error(`valid: ${Object.keys(SHOCK_LIBRARY).join(', ')}`);
  process.exit(1);
}
if (!Number.isFinite(baseline) || baseline < 1 || !Number.isFinite(recovery) || recovery < 2) {
  console.error('need --baseline >= 1 and --recovery >= 2 (a novelty window needs at least 2 turns)');
  process.exit(1);
}

const totalTurns = baseline + recovery;
const DOMAINS = ['cosmogenesis', 'lightspeed'];

// ---------------------------------------------------------------- plan

console.log('PHASE 3 — SHOCK MATRIX');
console.log(`  shocks    : ${shockNames.join(', ')}`);
console.log(`  per shock : ${baseline} baseline + ${recovery} shocked = ${totalTurns} turns`);
console.log(`  agents    : 1 seed (agy) over ${DOMAINS.join(' + ')}`);
console.log(`  substrate : agy; the substrate shock swaps agy -> omp for its recovery turns`);
console.log(`  matrix cap: ${matrixMinutes} min`);
console.log(`  results   : site/data/phase3.json (written after every experiment)`);
console.log(`  kill      : create arena/STOP`);

if (dry) {
  console.log('\n--dry: not launching.');
  process.exit(0);
}

let active = activeRuns();
if (active.length) {
  if (!wait) {
    console.error(`\nrefusing to start: another run is active (${active.map((a) => a.id).join(', ')}).`);
    console.error('Two runs share arena/world and the memory commons, so each ledger would');
    console.error("attribute the other run's file changes to its own agents. Wait for it to");
    console.error('finish, or pass --wait to queue Phase 3 automatically.');
    process.exit(1);
  }
  await waitForIdle();
  console.log('starting the matrix.');
}

// ---------------------------------------------------------------- matrix

const startedAt = Date.now();
const results = [];
const outPath = join(SITE, 'data', 'phase3.json');
mkdirSync(join(SITE, 'data'), { recursive: true });

function persist() {
  writeFileSync(outPath, JSON.stringify({
    generatedAt: new Date().toISOString(),
    design: { baseline, recovery, totalTurns, domains: DOMAINS, seedAgents: 1, matrixMinutes },
    results,
  }, null, 2), 'utf8');
}

// Write the design up front so a monitor has something to read before the first
// experiment finishes (each experiment can take tens of minutes).
persist();

for (const shockName of shockNames) {
  if (existsSync(join(ARENA, 'STOP'))) {
    console.log('\nSTOP file present — not launching further experiments.');
    break;
  }
  if ((Date.now() - startedAt) / 60000 > matrixMinutes) {
    console.log('\nmatrix time cap reached — not launching further experiments.');
    break;
  }

  const runId = `phase3-${shockName}-${new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19)}`;
  console.log(`\n${'='.repeat(72)}\nSHOCK ${shockName} — run ${runId}\n${'='.repeat(72)}`);

  const arena = new Arena({
    root: ARENA,
    config: {
      runId,
      phase: 'phase3-shock',
      maxTurns: totalTurns,
      maxWallClockMinutes: 120,
      maxCostUsd: 2,
      populationCap: 4,
      seedAgents: 1,
      substrateRotation: false,
      substrates: shockName === 'substrate' ? ['agy', 'omp'] : ['agy'],
      domains: DOMAINS,
      scribe: true,
      scribeUseLLM: false,   // deterministic ledger draft; no extra model call
    },
  });

  const exp = new ShockExperiment({ arena, shockName, shockAtTurn: baseline });
  let summary;
  try {
    summary = await arena.run({ onTurn: (outcome, a) => exp.onTurn(outcome, a) });
  } catch (err) {
    const message = String((err && err.message) || err);
    console.error(`experiment failed: ${message}`);
    results.push({ shock: shockName, runId, error: message });
    persist();
    continue;
  }

  const turns = new ForensicLedger(ARENA, runId).readTurns();
  const report = exp.report();
  results.push({
    ...report,
    runId,
    turns: summary.turns,
    okTurns: turns.filter((t) => t.ok).length,
    cost: summary.totalCostUsd,
    halted: summary.halted,
    incidents: summary.incidents?.byKind || {},
    noveltyRejected: summary.incidents?.byKind?.novelty_rejected || 0,
  });
  persist();

  console.log(`  result: novelty ${fmt(report.noveltyBefore)} -> ${fmt(report.noveltyAfter)} ` +
    `(delta ${fmt(report.delta)}) — ${report.verdict}`);
}

// ---------------------------------------------------------------- summary

console.log(`\n${'='.repeat(72)}\nPHASE 3 MATRIX COMPLETE — ${results.length}/${shockNames.length} experiments\n${'='.repeat(72)}`);
for (const r of results) {
  if (r.error) { console.log(`  ${r.shock.padEnd(12)} FAILED: ${r.error}`); continue; }
  console.log(`  ${r.shock.padEnd(12)} novelty ${fmt(r.noveltyBefore)} -> ${fmt(r.noveltyAfter)} ` +
    `(delta ${fmt(r.delta)})  ${r.verdict}`);
}
console.log(`\nresults: ${outPath}`);
