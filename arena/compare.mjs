/**
 * Cross-run comparison — the substrate benchmark table.
 *
 * Aggregates every recorded run into one comparative table. This is the artifact
 * that answers "which harness actually works, and at what cost" with measured
 * numbers rather than impressions.
 *
 * Usage: node compare.mjs
 */

import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const ARENA = 'D:\\AgentSwarm\\arena';
const runsDir = join(ARENA, 'runs');

function readJsonl(path) {
  if (!existsSync(path)) return [];
  const out = [];
  for (const line of readFileSync(path, 'utf8').split(/\r?\n/)) {
    const t = line.trim(); if (!t) continue;
    try { out.push(JSON.parse(t)); } catch {}
  }
  return out;
}

const runs = readdirSync(runsDir, { withFileTypes: true })
  .filter((d) => d.isDirectory() && /^phase\d/.test(d.name))
  .map((d) => d.name).sort();

if (!runs.length) { console.log('no runs recorded'); process.exit(0); }

// ---- per-run summary ----
console.log('RUNS');
console.log('run                                turns  ok%   cost      tools  think     viol  halt');
const perSub = {};
const allTurns = [];

for (const r of runs) {
  const dir = join(runsDir, r);
  const turns = readJsonl(join(dir, 'turns.jsonl'));
  if (!turns.length) continue;
  allTurns.push(...turns.map((t) => ({ ...t, _run: r })));
  const ok = turns.filter((t) => t.ok).length;
  const cost = turns.reduce((a, t) => a + (t.cost || 0), 0);
  const tools = turns.reduce((a, t) => a + (t.toolCallCount || 0), 0);
  const think = turns.reduce((a, t) => a + (t.thinkingTokens || 0), 0);
  const viol = turns.reduce((a, t) => a + (t.notes?.oracleViolations || 0), 0);
  const summary = existsSync(join(dir, 'summary.json'))
    ? JSON.parse(readFileSync(join(dir, 'summary.json'), 'utf8')) : null;
  console.log(
    `${r.padEnd(34)} ${String(turns.length).padStart(5)}  ${String(Math.round(100 * ok / turns.length)).padStart(3)}%  ` +
    `${('$' + cost.toFixed(5)).padStart(9)} ${String(tools).padStart(6)} ${String(think).padStart(9)} ` +
    `${String(viol).padStart(5)}  ${summary?.halted ? summary.halted.slice(0, 24) : '(running)'}`
  );
}

// ---- per-substrate aggregate ----
for (const t of allTurns) {
  const k = t.substrate;
  perSub[k] = perSub[k] || {
    n: 0, ok: 0, cost: 0, tools: 0, think: 0, dur: 0, chars: 0,
    files: 0, models: new Set(), runs: new Set(),
  };
  const b = perSub[k];
  b.n++; if (t.ok) b.ok++;
  b.cost += t.cost || 0;
  b.tools += t.toolCallCount || 0;
  b.think += t.thinkingTokens || 0;
  b.dur += t.durationSeconds || 0;
  b.chars += t.textLength || 0;
  b.files += (t.notes?.fileDiff?.created?.length || 0) + (t.notes?.fileDiff?.modified?.length || 0);
  if (t.model) b.models.add(t.model);
  b.runs.add(t._run);
}

console.log('\nSUBSTRATE BENCHMARK (aggregated across all runs)');
console.log('substrate  turns  ok%   $/turn     tools/t  think/t   s/turn  files  chars/t  models');
const rows = Object.entries(perSub).sort((a, b) => b[1].n - a[1].n);
for (const [k, b] of rows) {
  console.log(
    `${k.padEnd(10)} ${String(b.n).padStart(5)}  ${String(Math.round(100 * b.ok / b.n)).padStart(3)}%  ` +
    `${('$' + (b.cost / b.n).toFixed(5)).padStart(9)}  ${(b.tools / b.n).toFixed(1).padStart(6)}  ` +
    `${String(Math.round(b.think / b.n)).padStart(7)}  ${(b.dur / b.n).toFixed(1).padStart(6)}  ` +
    `${String(b.files).padStart(5)}  ${String(Math.round(b.chars / b.n)).padStart(7)}  ` +
    `${[...b.models].join(',').slice(0, 40)}`
  );
}

// ---- headline ----
const totalCost = allTurns.reduce((a, t) => a + (t.cost || 0), 0);
const totalTools = allTurns.reduce((a, t) => a + (t.toolCallCount || 0), 0);
const totalThink = allTurns.reduce((a, t) => a + (t.thinkingTokens || 0), 0);
const totalViol = allTurns.reduce((a, t) => a + (t.notes?.oracleViolations || 0), 0);
const deleted = allTurns.flatMap((t) => t.notes?.fileDiff?.deleted || []);
const created = allTurns.flatMap((t) => t.notes?.fileDiff?.created || []);

console.log('\nHEADLINE (all runs)');
console.log(`  turns              : ${allTurns.length}`);
console.log(`  total spend        : $${totalCost.toFixed(5)}`);
console.log(`  tool calls         : ${totalTools}`);
console.log(`  thinking tokens    : ${totalThink.toLocaleString()}`);
console.log(`  oracle violations  : ${totalViol}`);
console.log(`  files created      : ${created.length}`);
console.log(`  files DELETED      : ${deleted.length}`);
