/**
 * Live status — a compact, cheap view of a running (or finished) run.
 *
 * WHY THIS EXISTS: inspecting a run by reading raw event streams costs megabytes
 * of context per check (the pi stream alone is 7.5 MB). This script reduces the
 * entire run to a few dozen lines so progress can be checked for ~free.
 *
 * Usage: node status.mjs [runId]
 */

import { readFileSync, existsSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const ARENA = 'D:\\AgentSwarm\\arena';

function latestRun() {
  const dir = join(ARENA, 'runs');
  if (!existsSync(dir)) return null;
  const runs = readdirSync(dir, { withFileTypes: true })
    .filter((d) => d.isDirectory() && /^phase1-/.test(d.name)).map((d) => d.name);
  return runs.sort().pop();
}

const runId = process.argv[2] || latestRun();
if (!runId) { console.log('no runs found'); process.exit(0); }
const dir = join(ARENA, 'runs', runId);

function readJsonl(path, limit = null) {
  if (!existsSync(path)) return [];
  const lines = readFileSync(path, 'utf8').split(/\r?\n/).filter(Boolean);
  const use = limit ? lines.slice(-limit) : lines;
  const out = [];
  for (const l of use) { try { out.push(JSON.parse(l)); } catch {} }
  return out;
}

const turns = readJsonl(join(dir, 'turns.jsonl'));
const events = readJsonl(join(dir, 'events.jsonl'));
const incidents = readJsonl(join(dir, 'incidents.jsonl'));
const summaryPath = join(dir, 'summary.json');
const summary = existsSync(summaryPath) ? JSON.parse(readFileSync(summaryPath, 'utf8')) : null;

const RUNNING = !summary;
const totalCost = turns.reduce((a, t) => a + (t.cost || 0), 0);
const totalThink = turns.reduce((a, t) => a + (t.thinkingTokens || 0), 0);
const totalTools = turns.reduce((a, t) => a + (t.toolCallCount || 0), 0);
const filesCreated = turns.reduce((a, t) => a + (t.notes?.fileDiff?.created?.length || 0), 0);

console.log(`RUN ${runId}  [${RUNNING ? 'RUNNING' : 'FINISHED'}]`);
console.log(`turns=${turns.length}  cost=$${totalCost.toFixed(5)}  think=${totalThink.toLocaleString()}  tools=${totalTools}  files+${filesCreated}`);
if (summary) console.log(`halt: ${summary.halted}`);
console.log('');

// per-turn one-liners
console.log('seq  agent        sub   ok   tools think    files  viol  dur');
for (const t of turns) {
  const f = (t.notes?.fileDiff?.created?.length || 0) + (t.notes?.fileDiff?.modified?.length || 0);
  console.log(
    `${String(t.seq).padStart(3)}  ${String(t.agentName).padEnd(12)} ${String(t.substrate).padEnd(5)} ` +
    `${t.ok ? ' ok ' : 'FAIL'} ${String(t.toolCallCount || 0).padStart(5)} ` +
    `${String(t.thinkingTokens || 0).padStart(6)} ${String(f).padStart(6)} ` +
    `${String(t.notes?.oracleViolations || 0).padStart(5)}  ${Math.round(t.durationSeconds || 0)}s`
  );
}

// incidents
if (incidents.length) {
  console.log('\nINCIDENTS');
  const byKind = {};
  for (const i of incidents) byKind[`${i.severity}:${i.kind}`] = (byKind[`${i.severity}:${i.kind}`] || 0) + 1;
  for (const [k, v] of Object.entries(byKind)) console.log(`  ${k} x${v}`);
}

// population
const spawned = events.filter((e) => e.kind === 'agent_spawned');
const retired = events.filter((e) => e.kind === 'agent_retired');
console.log(`\nPOPULATION  created=${spawned.length} retired=${retired.length} connected=${events.filter((e) => e.kind === 'agent_connected').length}`);
for (const s of spawned) {
  console.log(`  + ${s.detail.name} (gen ${s.detail.generation}) ${s.detail.parent ? `by ${s.detail.parent}` : 'seed'} — ${String(s.detail.purpose || '').slice(0, 60)}`);
}
for (const r of retired) console.log(`  - ${r.detail.name}: ${String(r.detail.reason || '').slice(0, 60)}`);

// artifacts (names only, cheap)
const worldDir = join(ARENA, 'world');
if (existsSync(worldDir)) {
  let count = 0, bytes = 0;
  (function walk(d) {
    for (const e of readdirSync(d, { withFileTypes: true })) {
      if (e.isDirectory()) { if (e.name !== '__pycache__') walk(join(d, e.name)); continue; }
      count++; try { bytes += statSync(join(d, e.name)).size; } catch {}
    }
  })(worldDir);
  console.log(`\nWORLD  ${count} files, ${Math.round(bytes / 1024)} KB`);
}

// stasis quick check
const norm = (s) => (s || '').toLowerCase().replace(/\s+/g, ' ').replace(/[^a-z0-9 ]/g, '').trim();
function jac(a, b) {
  const A = new Set(a.split(' ').filter(Boolean)), B = new Set(b.split(' ').filter(Boolean));
  if (!A.size && !B.size) return 1;
  let i = 0; for (const x of A) if (B.has(x)) i++;
  return i / (A.size + B.size - i);
}
let longest = 0, cur = 0;
for (let i = 1; i < turns.length; i++) {
  if (jac(norm(turns[i - 1].text).slice(0, 400), norm(turns[i].text).slice(0, 400)) > 0.85) { cur++; longest = Math.max(longest, cur); }
  else cur = 0;
}
console.log(`STASIS  longest near-identical streak = ${longest}`);
