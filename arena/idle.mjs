/**
 * Run-concurrency gate, shared by the phase runners.
 *
 * Two runs share arena/world and the memory commons, so their world-tree snapshot
 * diffs would attribute each other's file changes (and could raise false
 * file_deletion_detected incidents). Phase runners therefore refuse to start while
 * another run is active; --wait queues behind it instead.
 */

import { readdirSync, existsSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { RUNS } from './paths.mjs';

/** Newest mtime among the files directly inside a run directory. */
export function newestMtimeMs(dir) {
  let newest = 0;
  for (const f of readdirSync(dir)) {
    try { newest = Math.max(newest, statSync(join(dir, f)).mtimeMs); } catch {}
  }
  return newest;
}

/**
 * A run is active if anything in its directory changed recently. Covers both the
 * loop (stdout streams are written during a turn) and the post-run Scribe, which
 * keeps writing into its own run directory after summary.json exists.
 */
export function activeRuns({ withinMs = 150_000 } = {}) {
  const out = [];
  if (!existsSync(RUNS)) return out;
  for (const d of readdirSync(RUNS, { withFileTypes: true })) {
    if (!d.isDirectory() || d.name.startsWith('.')) continue;
    const dir = join(RUNS, d.name);
    if (!existsSync(join(dir, 'turns.jsonl')) && !existsSync(join(dir, 'events.jsonl'))) continue;
    const idleMs = Date.now() - newestMtimeMs(dir);
    if (idleMs < withinMs) out.push({ id: d.name, idleSeconds: Math.round(idleMs / 1000) });
  }
  return out.sort((a, b) => a.idleSeconds - b.idleSeconds);
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/** Poll until no run is active. */
export async function waitForIdle({ pollMs = 20_000, log = console.log } = {}) {
  let active = activeRuns();
  while (active.length) {
    log(`\nwaiting for ${active[0].id} to finish (last write ${active[0].idleSeconds}s ago)…`);
    await sleep(pollMs);
    active = activeRuns();
  }
  log('\nno active runs — starting.');
}
