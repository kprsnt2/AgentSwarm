/**
 * Cost attribution — what each substrate actually cost, and what it WOULD have cost.
 *
 * Important nuance this script exists to capture: several substrates report $0.00
 * not because they are free, but because they are covered by a subscription or a
 * promotional period. Treating $0.00 as "free forever" would produce a badly wrong
 * recommendation. So we report two numbers:
 *
 *   reported  - what the CLI told us (may be 0 due to subscription/promo)
 *   notional  - what the tokens would cost at list API rates
 *
 * Usage: node cost.mjs
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
  .filter((d) => d.isDirectory() && /^phase1-/.test(d.name)).map((d) => d.name).sort();

const turns = [];
for (const r of runs) turns.push(...readJsonl(join(runsDir, r, 'turns.jsonl')));

const bySub = {};
for (const t of turns) {
  const k = t.substrate;
  bySub[k] = bySub[k] || {
    n: 0, ok: 0, reported: 0, freshIn: 0, cacheRead: 0, out: 0,
    think: 0, tools: 0, models: new Set(),
  };
  const b = bySub[k];
  b.n++; if (t.ok) b.ok++;
  b.reported += t.cost || 0;
  const u = t.usage || {};
  b.freshIn += u.input || u.input_tokens || 0;
  b.cacheRead += u.cacheRead || u.cache_read_tokens || 0;
  b.out += u.output || u.output_tokens || 0;
  b.think += t.thinkingTokens || 0;
  b.tools += t.toolCallCount || 0;
  if (t.model) b.models.add(t.model);
}

console.log('SUBSTRATE COST ATTRIBUTION');
console.log('(reported = what the CLI billed; tokens are the underlying volume)\n');
console.log('substrate  turns  ok%   reported$   fresh_in   cacheRead    output    cacheHit%');
for (const [k, b] of Object.entries(bySub)) {
  const totalIn = b.freshIn + b.cacheRead;
  const hit = totalIn ? (100 * b.cacheRead / totalIn).toFixed(1) : 'n/a';
  console.log(
    `${k.padEnd(10)} ${String(b.n).padStart(5)}  ${String(Math.round(100 * b.ok / b.n)).padStart(3)}%  ` +
    `${('$' + b.reported.toFixed(4)).padStart(10)}  ${String(b.freshIn).padStart(9)}  ` +
    `${String(b.cacheRead).padStart(10)}  ${String(b.out).padStart(9)}  ${String(hit).padStart(9)}%`
  );
}

const totalReported = turns.reduce((a, t) => a + (t.cost || 0), 0);
console.log(`\nTOTAL REPORTED SPEND: $${totalReported.toFixed(6)}`);

// ---- coverage notes: $0 does NOT always mean free ----
console.log('\nCOVERAGE STATUS (why a substrate may report $0.00)');
const notes = {
  agy: 'Google AI plan (subscription) — no per-token charge',
  omp: 'google-antigravity provider — billed per token in-harness',
  step: 'Step 5 Preview — promotional free usage period',
  pi: 'Fireworks — pay-per-token (very cheap + 97% cache hits)',
};
for (const k of Object.keys(bySub)) console.log(`  ${k.padEnd(6)} ${notes[k] || '(unknown)'}`);

// ---- notional list-rate estimate ----
// Rates are indicative public list prices per 1M tokens, used ONLY to show the
// order of magnitude of what the subscription/promo is absorbing.
const RATES = {
  // $/1M tokens: [fresh input, cached input, output]
  'gemini-3.8-flash-high': [0.30, 0.075, 2.50],
  'google-antigravity/gemini-3.8-flash': [0.30, 0.075, 2.50],
  'step/step-5-preview': [0.20, 0.05, 1.00],
  'fireworks/accounts/fireworks/models/deepseek-v4p1-flash': [0.15, 0.02, 0.60],
};

console.log('\nNOTIONAL LIST-RATE ESTIMATE (what these tokens would cost at API list prices)');
console.log('substrate  model                                    notional$');
let notionalTotal = 0;
for (const [k, b] of Object.entries(bySub)) {
  let cost = 0;
  for (const m of b.models) {
    const r = RATES[m];
    if (!r) continue;
    cost += (b.freshIn / 1e6) * r[0] + (b.cacheRead / 1e6) * r[1] + (b.out / 1e6) * r[2];
  }
  notionalTotal += cost;
  console.log(`${k.padEnd(10)} ${[...b.models].join(',').slice(0, 42).padEnd(42)} $${cost.toFixed(4)}`);
}
console.log(`\nTOTAL NOTIONAL: $${notionalTotal.toFixed(4)}`);
console.log(`Absorbed by subscription/promo: $${(notionalTotal - totalReported).toFixed(4)}`);
