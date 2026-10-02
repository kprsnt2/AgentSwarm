/**
 * Backfill — recompute list-rate pricing for turns recorded before pricing.mjs
 * existed, so historical runs are cost-comparable without re-running them.
 *
 * Writes runs/<id>/turns-priced.jsonl (a NEW file) rather than mutating turns.jsonl,
 * because turns.jsonl is hash-chained: rewriting it would break the integrity
 * guarantee the whole forensic design depends on. The dashboard prefers the priced
 * file when present.
 *
 * Usage: node backfill-pricing.mjs [runId]
 */
import { readFileSync, writeFileSync, existsSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { costOfTurn } from './pricing.mjs';
import { ARENA } from './paths.mjs';


const RUNS = join(ARENA, 'runs');

function readJsonl(p) {
  if (!existsSync(p)) return [];
  const out = [];
  for (const l of readFileSync(p, 'utf8').split(/\r?\n/)) {
    const t = l.trim(); if (!t) continue;
    try { out.push(JSON.parse(t)); } catch {}
  }
  return out;
}

const only = process.argv[2];
const runs = readdirSync(RUNS, { withFileTypes: true })
  .filter((d) => d.isDirectory() && (!only || d.name === only))
  .map((d) => d.name);

for (const r of runs) {
  const src = join(RUNS, r, 'turns.jsonl');
  if (!existsSync(src)) continue;
  const turns = readJsonl(src);
  if (!turns.length) continue;

  let listTotal = 0, reportedTotal = 0, absorbed = 0, cacheSaved = 0;
  const priced = turns.map((t) => {
    const p = costOfTurn({ model: t.model, usage: t.usage, reportedCost: t.cost || 0 });
    listTotal += p.listCost;
    reportedTotal += p.reportedCost;
    absorbed += p.absorbed;
    cacheSaved += p.cacheSavings;
    return { ...t, pricing: p };
  });

  const outPath = join(RUNS, r, 'turns-priced.jsonl');
  writeFileSync(outPath, priced.map((t) => JSON.stringify(t)).join('\n') + '\n', 'utf8');

  console.log(`${r}`);
  console.log(`  turns           : ${turns.length}`);
  console.log(`  reported cost   : $${reportedTotal.toFixed(5)}`);
  console.log(`  list-rate cost  : $${listTotal.toFixed(5)}`);
  console.log(`  absorbed (sub/promo): $${absorbed.toFixed(5)}`);
  console.log(`  saved by caching    : $${cacheSaved.toFixed(5)}`);
  console.log(`  -> ${outPath}`);
}
