/**
 * Live watch — polls a run and prints only what CHANGED.
 *
 * Unlike status.mjs (a one-shot snapshot), this keeps running and shows a compact
 * one-line-per-turn feed as the swarm works. Cheap by design: it re-reads only the
 * turn ledger and prints deltas, never the raw event streams.
 *
 * Usage:
 *   node watch.mjs              # watch the newest run, refresh every 15s
 *   node watch.mjs <runId> 30   # specific run, 30s interval
 *
 * Ctrl+C to stop watching (this does NOT stop the swarm — use the STOP file).
 */

import { readFileSync, existsSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const ARENA = 'D:\\AgentSwarm\\arena';

function latestRun() {
  const dir = join(ARENA, 'runs');
  if (!existsSync(dir)) return null;
  return readdirSync(dir, { withFileTypes: true })
    .filter((d) => d.isDirectory() && /^phase\d/.test(d.name))
    .map((d) => d.name).sort().pop();
}

const runId = process.argv[2] || latestRun();
const interval = Math.max(5, parseInt(process.argv[3] || '15', 10)) * 1000;
if (!runId) { console.log('no runs found'); process.exit(0); }

const dir = join(ARENA, 'runs', runId);
const turnPath = join(dir, 'turns.jsonl');
const summaryPath = join(dir, 'summary.json');
const incidentPath = join(dir, 'incidents.jsonl');

console.log(`WATCHING ${runId}`);
console.log(`refresh ${interval / 1000}s · Ctrl+C to stop watching (swarm keeps running)`);
console.log(`halt the swarm with: New-Item -ItemType File ${join(ARENA, 'STOP')}`);
console.log('');

let seenTurns = 0;
let seenIncidents = 0;
let lastSize = -1;
let idleTicks = 0;

function readJsonl(path) {
  if (!existsSync(path)) return [];
  const out = [];
  for (const line of readFileSync(path, 'utf8').split(/\r?\n/)) {
    const t = line.trim(); if (!t) continue;
    try { out.push(JSON.parse(t)); } catch {}
  }
  return out;
}

function tick() {
  const turns = readJsonl(turnPath);
  const incidents = readJsonl(incidentPath);

  // new turns
  for (let i = seenTurns; i < turns.length; i++) {
    const t = turns[i];
    const f = (t.notes?.fileDiff?.created?.length || 0) + (t.notes?.fileDiff?.modified?.length || 0);
    const del = t.notes?.fileDiff?.deleted?.length || 0;
    const stamp = new Date().toLocaleTimeString('en-GB');
    console.log(
      `[${stamp}] #${String(t.seq).padStart(3)} ${String(t.agentName).padEnd(11)} ${String(t.substrate).padEnd(5)} ` +
      `${t.ok ? 'ok  ' : 'FAIL'} tools=${String(t.toolCallCount).padStart(3)} ` +
      `think=${String(t.thinkingTokens).padStart(6)} files=${String(f).padStart(2)}` +
      `${del ? ` DEL=${del}` : ''} viol=${t.notes?.oracleViolations || 0} ${Math.round(t.durationSeconds || 0)}s`
    );
  }
  seenTurns = turns.length;

  // new incidents
  for (let i = seenIncidents; i < incidents.length; i++) {
    const x = incidents[i];
    console.log(`           !! [${x.severity}] ${x.kind} — ${JSON.stringify(x.detail).slice(0, 120)}`);
  }
  seenIncidents = incidents.length;

  // progress detection: is the current turn's stream still growing?
  let growing = false;
  if (existsSync(dir)) {
    const streams = readdirSync(dir).filter((f) => f.endsWith('.stdout.jsonl'));
    let size = 0;
    for (const s of streams) { try { size += statSync(join(dir, s)).size; } catch {} }
    growing = size !== lastSize;
    lastSize = size;
    if (growing) idleTicks = 0; else idleTicks++;
  }

  // completion
  if (existsSync(summaryPath)) {
    const s = JSON.parse(readFileSync(summaryPath, 'utf8'));
    console.log('');
    console.log(`FINISHED — ${s.turns} turns, $${s.totalCostUsd.toFixed(5)}, halted: ${s.halted}`);
    console.log(`run: node analyze.mjs ${runId}`);
    process.exit(0);
  }

  // stall warning
  const last = turns[turns.length - 1];
  if (last && idleTicks >= 4) {
    const mins = Math.round((Date.now() - new Date(last.ts).getTime()) / 60000);
    console.log(`           .. turn ${turns.length + 1} in progress (${mins}m since last completed turn, stream ${growing ? 'growing' : 'idle'})`);
  }
}

tick();
setInterval(tick, interval);
