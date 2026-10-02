/**
 * Controlled substrate benchmark — one question, one budget, N repeats per harness.
 *
 * The site's substrate table is operational telemetry: harnesses ran different
 * questions, different turn budgets, and different pricing tiers. This script runs
 * the SAME question under the SAME cap on each harness, repeated, so the comparison
 * is actually controlled.
 *
 * Usage:
 *   node benchmark.mjs --question "Is commercial fusion power achievable by 2040?" \
 *                      --class engineering --substrates agy,omp --turns 3 --repeats 3
 *   node benchmark.mjs --dry          # print the matrix, launch nothing
 *
 * Output: ../site/data/benchmark.json
 *
 * NOTE: a live run executes real agents, which write artifacts under arena/world and
 * spend real money on pay-per-token harnesses. Start with --dry and --turns 1.
 */

import { writeFileSync, mkdirSync, readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { Arena } from './engine.mjs';
import { DOMAINS } from './domains.mjs';
import { inferClass } from './classify.mjs';
import { ARENA, SITE } from './paths.mjs';

function arg(name, dflt) {
  const i = process.argv.indexOf(name);
  return i >= 0 ? process.argv[i + 1] : dflt;
}

const dry = process.argv.includes('--dry');
const question = arg('--question', 'Is commercial fusion power achievable by 2040?');
const forcedClass = arg('--class', null);
const substrates = arg('--substrates', 'agy,omp').split(',').map((s) => s.trim()).filter(Boolean);
const turns = parseInt(arg('--turns', '3'), 10);
const repeats = parseInt(arg('--repeats', '3'), 10);
const minutes = parseFloat(arg('--minutes', '30'));

const inferred = forcedClass
  ? { cls: forcedClass, why: 'explicitly specified', confidence: 'high' }
  : inferClass(question);
if (inferred.confidence === 'low') {
  console.error(`could not infer a class for: "${question}"`);
  console.error('Pass --class <empirical|engineering|historical|metaphysical|exploratory>.');
  process.exit(1);
}

const domain = {
  id: 'benchmark',
  title: question,
  epistemicClass: inferred.cls,
  brief: question,
  groundedFacts: [],
  deliverable: 'A concrete written artifact saved to disk, with reasoning and quantitative claims.',
};
const existing = DOMAINS.findIndex((d) => d.id === 'benchmark');
if (existing >= 0) DOMAINS[existing] = domain; else DOMAINS.push(domain);

function readJsonl(path) {
  if (!existsSync(path)) return [];
  const out = [];
  for (const line of readFileSync(path, 'utf8').split(/\r?\n/)) {
    const t = line.trim(); if (!t) continue;
    try { out.push(JSON.parse(t)); } catch {}
  }
  return out;
}

console.log('CONTROLLED BENCHMARK');
console.log(`  question   : ${question}`);
console.log(`  class      : ${inferred.cls} (${inferred.why})`);
console.log(`  substrates : ${substrates.join(', ')}`);
console.log(`  per run    : ${turns} turns, ${minutes} min cap`);
console.log(`  repeats    : ${repeats} per substrate (${substrates.length * repeats} runs total)`);
console.log('  note       : live runs execute real agents and write to arena/world.');

if (dry) { console.log('\n--dry: not launching.'); process.exit(0); }

const results = [];
for (const sub of substrates) {
  for (let r = 1; r <= repeats; r++) {
    const runId = `bench-${sub}-r${r}-${new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19)}`;
    console.log(`\n== ${sub} repeat ${r}/${repeats} (${runId}) ==`);
    const arena = new Arena({
      root: ARENA,
      config: {
        runId,
        phase: 'benchmark',
        maxTurns: turns,
        maxWallClockMinutes: minutes,
        maxCostUsd: 2,
        substrateTimeouts: { agy: 900_000, omp: 900_000, step: 1_500_000, pi: 1_500_000 },
        populationCap: 1,
        seedAgents: 1,
        substrateRotation: false,
        substrates: [sub],
        domains: ['benchmark'],
      },
    });
    const summary = await arena.run({ onTurn: () => {} });
    const ledger = readJsonl(join(ARENA, 'runs', summary.runId, 'turns.jsonl'));
    results.push({
      substrate: sub,
      repeat: r,
      runId: summary.runId,
      turns: ledger.length,
      okTurns: ledger.filter((t) => t.ok).length,
      cost: summary.totalCostUsd,
      toolCalls: ledger.reduce((a, t) => a + (t.toolCallCount || 0), 0),
      thinkingTokens: ledger.reduce((a, t) => a + (t.thinkingTokens || 0), 0),
      wallClockMinutes: summary.wallClockMinutes,
      halted: summary.halted,
    });
    console.log(`   turns=${ledger.length} ok=${ledger.filter((t) => t.ok).length} cost=$${summary.totalCostUsd}`);
  }
}

const bySubstrate = substrates.map((s) => {
  const rs = results.filter((r) => r.substrate === s);
  const tt = rs.reduce((a, r) => a + r.turns, 0);
  const ok = rs.reduce((a, r) => a + r.okTurns, 0);
  return {
    name: s,
    runs: rs.length,
    turns: tt,
    successRate: tt ? ok / tt : 0,
    costPerTurn: tt ? rs.reduce((a, r) => a + r.cost, 0) / tt : 0,
    toolsPerTurn: tt ? rs.reduce((a, r) => a + r.toolCalls, 0) / tt : 0,
    thinkPerTurn: tt ? rs.reduce((a, r) => a + r.thinkingTokens, 0) / tt : 0,
  };
});

const payload = {
  generatedAt: new Date().toISOString(),
  question,
  class: inferred.cls,
  turnsPerRun: turns,
  repeats,
  substrates: bySubstrate,
  runs: results,
};

mkdirSync(join(SITE, 'data'), { recursive: true });
writeFileSync(join(SITE, 'data', 'benchmark.json'), JSON.stringify(payload, null, 2), 'utf8');
console.log(`\nwrote site/data/benchmark.json (${results.length} runs)`);
