/**
 * Shared memory substrate — the swarm's collective long-term memory.
 *
 * Design goals (from the user's brief):
 *   - agents write logs
 *   - agents connect and think
 *   - memory is SHARED with others
 *   - memory lets them evolve
 *
 * Implementation: an append-only JSONL event log per memory scope, plus a derived
 * index for fast retrieval. Append-only is deliberate: it mirrors the "immutable
 * provenance" invariant the user's earlier agents independently ratified, and it
 * means an agent cannot silently rewrite history.
 *
 * Scopes:
 *   global   - visible to every agent (the commons)
 *   clan:<n> - visible to a lineage/clan
 *   agent:<id> - private scratch
 */

import { appendFileSync, readFileSync, existsSync, mkdirSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { createHash } from 'node:crypto';

export class SharedMemory {
  constructor(root) {
    this.root = root;
    this.dir = join(root, 'memory');
    mkdirSync(this.dir, { recursive: true });
    this.cache = new Map();
  }

  _path(scope) {
    const safe = scope.replace(/[^a-zA-Z0-9_.:-]/g, '_');
    return join(this.dir, `${safe}.jsonl`);
  }

  /**
   * Append a memory entry. Returns the entry with its hash-chain linkage.
   * The `prev` field makes the log tamper-evident: altering any earlier record
   * invalidates every subsequent hash.
   */
  write({ scope, agentId, kind, content, tags = [], turn = null, meta = {} }) {
    const path = this._path(scope);
    const entries = this.read(scope);
    const prev = entries.length ? entries[entries.length - 1].hash : 'GENESIS';
    const body = {
      seq: entries.length,
      ts: new Date().toISOString(),
      turn,
      agentId,
      scope,
      kind, // observation | hypothesis | finding | question | decision | artifact
      content,
      tags,
      meta,
      prev,
    };
    const hash = createHash('sha256').update(prev + JSON.stringify(body)).digest('hex').slice(0, 16);
    const entry = { ...body, hash };
    appendFileSync(path, JSON.stringify(entry) + '\n', 'utf8');
    this.cache.delete(scope);
    return entry;
  }

  read(scope) {
    if (this.cache.has(scope)) return this.cache.get(scope);
    const path = this._path(scope);
    if (!existsSync(path)) { this.cache.set(scope, []); return []; }
    const out = [];
    for (const line of readFileSync(path, 'utf8').split(/\r?\n/)) {
      const t = line.trim();
      if (!t) continue;
      try { out.push(JSON.parse(t)); } catch {}
    }
    this.cache.set(scope, out);
    return out;
  }

  /** Verify the hash chain has not been rewritten. */
  verify(scope) {
    const entries = this.read(scope);
    let prev = 'GENESIS';
    for (const e of entries) {
      const { hash, ...body } = e;
      const expect = createHash('sha256').update(prev + JSON.stringify(body)).digest('hex').slice(0, 16);
      if (expect !== hash) return { ok: false, brokenAt: e.seq };
      prev = hash;
    }
    return { ok: true, count: entries.length };
  }

  /**
   * Retrieve memory an agent is entitled to see: the global commons, its own
   * private scope, and its clan. This is how memory becomes genuinely shared
   * while still allowing private reasoning.
   */
  visibleTo({ agentId, clan }) {
    const scopes = ['global', `agent:${agentId}`];
    if (clan != null) scopes.push(`clan:${clan}`);
    const all = [];
    for (const s of scopes) for (const e of this.read(s)) all.push(e);
    all.sort((a, b) => (a.ts < b.ts ? -1 : 1));
    return all;
  }

  /** Simple keyword retrieval over visible memory. */
  recall({ agentId, clan, query, limit = 12 }) {
    const visible = this.visibleTo({ agentId, clan });
    if (!query) return visible.slice(-limit);
    const terms = query.toLowerCase().split(/\s+/).filter((t) => t.length > 2);
    const scored = visible.map((e) => {
      const hay = (e.content + ' ' + (e.tags || []).join(' ')).toLowerCase();
      let score = 0;
      for (const t of terms) if (hay.includes(t)) score += 1;
      return { e, score };
    }).filter((x) => x.score > 0);
    scored.sort((a, b) => b.score - a.score);
    return scored.slice(0, limit).map((x) => x.e);
  }

  listScopes() {
    if (!existsSync(this.dir)) return [];
    return readdirSync(this.dir).filter((f) => f.endsWith('.jsonl')).map((f) => f.replace(/\.jsonl$/, ''));
  }

  stats() {
    const scopes = this.listScopes();
    let total = 0;
    const byKind = {};
    for (const s of scopes) {
      const entries = this.read(s);
      total += entries.length;
      for (const e of entries) byKind[e.kind] = (byKind[e.kind] || 0) + 1;
    }
    return { scopes: scopes.length, totalEntries: total, byKind };
  }
}
