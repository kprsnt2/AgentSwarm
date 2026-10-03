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
import { spawnSync } from 'node:child_process';
import { RUNS } from './paths.mjs';

/**
 * Command lines of node processes running one of our runners.
 *
 * File mtimes alone are not enough: a substrate turn can be silent for 20+ minutes
 * (pi produced no output at all while a turn was in flight), so a recency window
 * shorter than the substrate timeout declares a live run idle. On 2026-10-03 that
 * let the queued temptation run overlap a stuck durability turn.
 */
export function runningRunners() {
  const re = /(run-phase\d|run-temptation|new-run\.mjs|phase\d\.mjs|benchmark\.mjs)/;
  try {
    if (process.platform === 'win32') {
      const r = spawnSync('powershell', ['-NoProfile', '-Command',
        "Get-CimInstance Win32_Process -Filter \"Name='node.exe'\" | ForEach-Object { \"$($_.ProcessId)|$($_.CommandLine)\" }",
      ], { encoding: 'utf8', timeout: 15_000, windowsHide: true });
      return (r.stdout || '').split(/\r?\n/).map((s) => s.trim()).filter((l) => l && re.test(l))
        .map((l) => { const i = l.indexOf('|'); return { pid: Number(l.slice(0, i)), cmd: l.slice(i + 1) }; });
    }
    const r = spawnSync('ps', ['-eo', 'pid,args'], { encoding: 'utf8', timeout: 15_000 });
    return (r.stdout || '').split('\n').map((s) => s.trim()).filter((l) => l && re.test(l))
      .map((l) => { const m = l.match(/^(\d+)\s+(.*)$/); return m ? { pid: Number(m[1]), cmd: m[2] } : null; })
      .filter(Boolean);
  } catch {
    return [];
  }
}

/** Live runners other than this process. */
export function otherRunners() {
  return runningRunners().filter((r) => r.pid !== process.pid);
}

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
  const others = otherRunners();
  for (const d of readdirSync(RUNS, { withFileTypes: true })) {
    if (!d.isDirectory() || d.name.startsWith('.')) continue;
    const dir = join(RUNS, d.name);
    const hasLedger = existsSync(join(dir, 'turns.jsonl')) || existsSync(join(dir, 'events.jsonl'));
    if (!hasLedger) continue;
    const finished = existsSync(join(dir, 'summary.json'));
    const idleMs = Date.now() - newestMtimeMs(dir);
    // ANOTHER runner process is alive and this run has no summary yet -> it is in
    // flight, even if its substrate has been silent past the recency window.
    // Scoped to other processes so stale runs from killed runners (no summary.json)
    // do not block the queue forever.
    const inFlight = !finished && others.length > 0;
    if (idleMs < withinMs || inFlight) {
      out.push({ id: d.name, idleSeconds: Math.round(idleMs / 1000), inFlight });
    }
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
