/**
 * Forensic ledger — the tamper-evident record of everything the swarm does.
 *
 * This is the direct answer to the user's research question ("understand what
 * agents are thinking and doing"). Two design commitments:
 *
 *  1. CAPTURE THE INNER TRACE, NOT JUST THE TRANSCRIPT.
 *     Every turn stores the full structured event stream emitted by the CLI,
 *     including reasoning/thinking tokens, the exact tool calls with parameters,
 *     and tool outputs. A chat transcript alone cannot show *why* an agent acted.
 *
 *  2. MAKE DELETION DETECTABLE.
 *     Records are hash-chained and appended to an immutable event log. The ledger
 *     also snapshots the world tree (path + sha256 + size) after every turn, so
 *     removing or rewriting a file is visible as a diff rather than an absence.
 *
 * The ledger is written OUTSIDE the agents' writable world directory so that an
 * agent cannot edit its own audit trail.
 */

import { appendFileSync, readFileSync, existsSync, mkdirSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { createHash } from 'node:crypto';
import { costOfTurn } from '../pricing.mjs';

export class ForensicLedger {
  constructor(root, runId) {
    this.root = root;
    this.runId = runId;
    this.dir = join(root, 'runs', runId);
    mkdirSync(this.dir, { recursive: true });
    this.turnPath = join(this.dir, 'turns.jsonl');
    this.eventPath = join(this.dir, 'events.jsonl');
    this.incidentPath = join(this.dir, 'incidents.jsonl');
    this.turnCount = 0;
  }

  _lastHash(path) {
    if (!existsSync(path)) return 'GENESIS';
    const lines = readFileSync(path, 'utf8').split(/\r?\n/).filter(Boolean);
    if (!lines.length) return 'GENESIS';
    try { return JSON.parse(lines[lines.length - 1]).hash; } catch { return 'GENESIS'; }
  }

  _append(path, record) {
    const prev = this._lastHash(path);
    const hash = createHash('sha256').update(prev + JSON.stringify(record)).digest('hex').slice(0, 20);
    appendFileSync(path, JSON.stringify({ ...record, prev, hash }) + '\n', 'utf8');
    return hash;
  }

  /**
   * Record one completed agent turn with its full forensic payload.
   * `result` is the object returned by runTurn().
   */
  recordTurn({ agent, turn, result, worldSnapshot, phase, notes = {} }) {
    this.turnCount += 1;

    // Price the turn from token counts at published list rates, so every substrate
    // is comparable even when it reports $0.00 due to a subscription or promo.
    const pricing = costOfTurn({
      model: result.model,
      usage: result.usage,
      reportedCost: result.cost || 0,
    });

    const record = {
      seq: this.turnCount,
      ts: new Date().toISOString(),
      phase,
      turn,
      agentId: agent.id,
      agentName: agent.name,
      substrate: result.substrate,
      model: result.model,
      ok: result.ok,
      error: result.error,
      timedOut: result.timedOut,

      // --- cognitive telemetry ---
      thinkingTokens: result.thinkingTokens,
      // The model's actual internal monologue, recovered from the streaming
      // thinking_delta events. This is the "what are they thinking" payload.
      reasoning: result.reasoning || '',
      reasoningChars: result.reasoningChars || 0,
      reasoningBlocks: result.reasoningBlocks || 0,
      usage: result.usage,
      cost: result.cost,
      pricing,

      // --- behaviour telemetry ---
      toolCallCount: result.toolCalls.length,
      toolCalls: result.toolCalls,
      textLength: (result.text || '').length,
      text: result.text,

      // --- integrity ---
      rawEventCount: result.rawEventCount,
      stdoutPath: result.stdoutPath ?? null,
      worldSnapshot,
      notes,
    };
    const hash = this._append(this.turnPath, record);
    return { ...record, hash };
  }

  /** Record a discrete behavioural event (spawn, retire, tamper attempt, ...). */
  recordEvent({ kind, agentId = null, detail = {}, phase = null, turn = null }) {
    return this._append(this.eventPath, {
      ts: new Date().toISOString(), phase, turn, kind, agentId, detail,
    });
  }

  /**
   * Record a detected integrity or safety incident.
   * Severity: info | warn | critical
   */
  recordIncident({ kind, severity = 'warn', agentId = null, detail = {}, phase = null, turn = null }) {
    return this._append(this.incidentPath, {
      ts: new Date().toISOString(), phase, turn, kind, severity, agentId, detail,
    });
  }

  readTurns() { return this._readJsonl(this.turnPath); }
  readEvents() { return this._readJsonl(this.eventPath); }
  readIncidents() { return this._readJsonl(this.incidentPath); }

  _readJsonl(path) {
    if (!existsSync(path)) return [];
    const out = [];
    for (const line of readFileSync(path, 'utf8').split(/\r?\n/)) {
      const t = line.trim();
      if (!t) continue;
      try { out.push(JSON.parse(t)); } catch {}
    }
    return out;
  }

  /** Verify the whole turn chain is intact. Detects any edit to history. */
  verify() {
    const results = {};
    for (const [name, path] of [['turns', this.turnPath], ['events', this.eventPath], ['incidents', this.incidentPath]]) {
      const entries = this._readJsonl(path);
      let prev = 'GENESIS';
      let ok = true;
      let brokenAt = null;
      for (const e of entries) {
        const { hash, prev: recPrev, ...body } = e;
        const expect = createHash('sha256').update(prev + JSON.stringify(body)).digest('hex').slice(0, 20);
        if (expect !== hash || recPrev !== prev) { ok = false; brokenAt = e.seq ?? null; break; }
        prev = hash;
      }
      results[name] = { ok, count: entries.length, brokenAt };
    }
    return results;
  }
}

/**
 * Snapshot a directory tree as { relPath: {sha256, size} }.
 * Used to detect file creation, modification, and DELETION between turns.
 */
export function snapshotTree(dir) {
  const out = {};
  if (!existsSync(dir)) return out;
  const walk = (d, base = '') => {
    let entries;
    try { entries = readdirSync(d, { withFileTypes: true }); } catch { return; }
    for (const ent of entries) {
      const full = join(d, ent.name);
      const rel = base ? `${base}/${ent.name}` : ent.name;
      if (ent.isDirectory()) { walk(full, rel); continue; }
      try {
        const buf = readFileSync(full);
        out[rel] = {
          sha256: createHash('sha256').update(buf).digest('hex').slice(0, 16),
          size: buf.length,
        };
      } catch {}
    }
  };
  walk(dir);
  return out;
}

/** Diff two snapshots into created/modified/deleted sets. */
export function diffSnapshots(before, after) {
  const created = [], modified = [], deleted = [];
  for (const [p, meta] of Object.entries(after)) {
    if (!(p in before)) created.push(p);
    else if (before[p].sha256 !== meta.sha256) modified.push(p);
  }
  for (const p of Object.keys(before)) if (!(p in after)) deleted.push(p);
  return { created, modified, deleted };
}
