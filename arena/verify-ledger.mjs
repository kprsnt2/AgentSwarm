/**
 * Verify every hash chain in the forensic ledgers. Exit non-zero on any break.
 *
 * The site claims the record is tamper-evident. This is the command that lets a
 * stranger check it without reading the engine: recompute every turn/event/incident
 * chain and every memory scope, and fail loudly if any record was edited.
 *
 * Usage:
 *   node verify-ledger.mjs            # every run + every memory scope
 *   node verify-ledger.mjs <runId>    # one run
 */

import { readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { ARENA, RUNS } from './paths.mjs';
import { ForensicLedger } from './ledger/forensic.mjs';
import { SharedMemory } from './ledger/memory.mjs';

const only = process.argv[2] || null;

const runIds = readdirSync(RUNS, { withFileTypes: true })
  .filter((d) => d.isDirectory() && !d.name.startsWith('.'))
  .map((d) => d.name)
  .filter((n) => existsSync(join(RUNS, n, 'turns.jsonl')))
  .filter((n) => !only || n === only)
  .sort();

if (only && !runIds.length) {
  console.error(`no run with a turns.jsonl ledger: ${only}`);
  process.exit(1);
}

let bad = 0;

for (const id of runIds) {
  const ledger = new ForensicLedger(ARENA, id);
  const res = ledger.verify();
  const ok = Object.values(res).every((v) => v.ok);
  const bits = Object.entries(res)
    .map(([k, v]) => `${k}:${v.ok ? 'ok' : `BROKEN@${v.brokenAt ?? '?'}`}(${v.count})`)
    .join('  ');
  if (!ok) bad += 1;
  console.log(`${ok ? 'OK  ' : 'FAIL'} ${id}  ${bits}`);
}

const memDir = join(ARENA, 'memory');
if (existsSync(memDir)) {
  const mem = new SharedMemory(ARENA);
  for (const f of readdirSync(memDir).filter((n) => n.endsWith('.jsonl')).sort()) {
    const scope = f.replace(/\.jsonl$/, '');
    const r = mem.verify(scope);
    if (!r.ok) { bad += 1; console.log(`FAIL memory/${f}  brokenAt:${r.brokenAt}`); }
    else console.log(`OK   memory/${f}  entries:${r.count}`);
  }
}

console.log(bad
  ? `\n${bad} chain(s) BROKEN — the record does not match its hashes.`
  : `\nall chains intact (${runIds.length} run${runIds.length === 1 ? '' : 's'}).`);
process.exit(bad ? 1 : 0);
