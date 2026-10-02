/**
 * Export — turn the forensic ledgers into a single JSON payload for the website.
 *
 * Keeps the site build decoupled from the arena internals: the site reads one
 * generated JSON file, so it can be deployed statically anywhere.
 *
 * Usage: node export-site.mjs
 * Output: ../site/data/findings.json
 */

import { readFileSync, existsSync, readdirSync, writeFileSync, mkdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { readPosts } from './scribe.mjs';

const ARENA = 'D:\\AgentSwarm\\arena';
const SITE = 'D:\\AgentSwarm\\site';

function readJsonl(path) {
  if (!existsSync(path)) return [];
  const out = [];
  for (const line of readFileSync(path, 'utf8').split(/\r?\n/)) {
    const t = line.trim(); if (!t) continue;
    try { out.push(JSON.parse(t)); } catch {}
  }
  return out;
}

const runsDir = join(ARENA, 'runs');
// NOTE: this previously matched only /^phase\d/, which silently dropped every
// `direct-*` run (the ad-hoc -q runs). Those runs produced real artifacts that then
// never appeared on the site. Any run directory with a turns.jsonl ledger counts.
const runIds = readdirSync(runsDir, { withFileTypes: true })
  .filter((d) => d.isDirectory() && !d.name.startsWith('.'))
  .map((d) => d.name)
  .filter((n) => existsSync(join(runsDir, n, 'turns.jsonl')))
  .sort();

const runs = [];
const allTurns = [];

for (const id of runIds) {
  const dir = join(runsDir, id);
  const turns = readJsonl(join(dir, 'turns.jsonl'));
  if (!turns.length) continue;
  const events = readJsonl(join(dir, 'events.jsonl'));
  const incidents = readJsonl(join(dir, 'incidents.jsonl'));
  const summary = existsSync(join(dir, 'summary.json'))
    ? JSON.parse(readFileSync(join(dir, 'summary.json'), 'utf8')) : null;
  const phase2 = existsSync(join(dir, 'phase2-results.json'))
    ? JSON.parse(readFileSync(join(dir, 'phase2-results.json'), 'utf8')) : null;

  allTurns.push(...turns.map((t) => ({ ...t, _run: id })));

  runs.push({
    id,
    phase: turns[0]?.phase || 'unknown',
    turns: turns.length,
    okTurns: turns.filter((t) => t.ok).length,
    cost: turns.reduce((a, t) => a + (t.cost || 0), 0),
    toolCalls: turns.reduce((a, t) => a + (t.toolCallCount || 0), 0),
    thinkingTokens: turns.reduce((a, t) => a + (t.thinkingTokens || 0), 0),
    violations: turns.reduce((a, t) => a + (t.notes?.oracleViolations || 0), 0),
    halted: summary?.halted ?? null,
    wallClockMinutes: summary?.wallClockMinutes ?? null,
    incidents: incidents.map((i) => ({ kind: i.kind, severity: i.severity, detail: i.detail, turn: i.turn })),
    population: summary?.population ?? null,
    memory: summary?.memory ?? null,
    ledgerIntegrity: summary?.ledgerIntegrity ?? null,
    phase2,
    turnDetail: turns.map((t) => ({
      seq: t.seq, agent: t.agentName, substrate: t.substrate, model: t.model,
      ok: t.ok, error: t.error, timedOut: t.timedOut,
      toolCalls: t.toolCallCount, thinkingTokens: t.thinkingTokens,
      cost: t.cost, textLength: t.textLength, durationSeconds: t.durationSeconds,
      created: t.notes?.fileDiff?.created?.length || 0,
      modified: t.notes?.fileDiff?.modified?.length || 0,
      deleted: t.notes?.fileDiff?.deleted?.length || 0,
      violations: t.notes?.oracleViolations || 0,
      claimedScore: t.notes?.claimedScore ?? null,
      hash: t.hash,
      textHead: (t.text || '').slice(0, 400),
    })),
  });
}

// ---- substrate benchmark ----
const bySub = {};
for (const t of allTurns) {
  const k = t.substrate;
  bySub[k] = bySub[k] || { turns: 0, ok: 0, cost: 0, tools: 0, think: 0, files: 0, chars: 0, models: new Set() };
  const b = bySub[k];
  b.turns++; if (t.ok) b.ok++;
  b.cost += t.cost || 0;
  b.tools += t.toolCallCount || 0;
  b.think += t.thinkingTokens || 0;
  b.chars += t.textLength || 0;
  b.files += (t.notes?.fileDiff?.created?.length || 0) + (t.notes?.fileDiff?.modified?.length || 0);
  if (t.model) b.models.add(t.model);
}
const substrates = Object.entries(bySub).map(([k, b]) => ({
  name: k,
  model: [...b.models][0] || 'unknown',
  turns: b.turns,
  successRate: b.turns ? b.ok / b.turns : 0,
  costPerTurn: b.turns ? b.cost / b.turns : 0,
  toolsPerTurn: b.turns ? b.tools / b.turns : 0,
  thinkPerTurn: b.turns ? b.think / b.turns : 0,
  charsPerTurn: b.turns ? b.chars / b.turns : 0,
  files: b.files,
})).sort((a, b) => b.turns - a.turns);

// ---- artifacts ----
const worldDir = join(ARENA, 'world');
const artifacts = [];
(function walk(d, base = '') {
  if (!existsSync(d)) return;
  for (const e of readdirSync(d, { withFileTypes: true })) {
    const rel = base ? `${base}/${e.name}` : e.name;
    if (e.isDirectory()) { if (e.name !== '__pycache__') walk(join(d, e.name), rel); continue; }
    const st = statSync(join(d, e.name));
    artifacts.push({ path: rel, bytes: st.size, modified: st.mtime.toISOString() });
  }
})(worldDir);
artifacts.sort((a, b) => b.bytes - a.bytes);

// ---- memory commons ----
const memory = readJsonl(join(ARENA, 'memory', 'global.jsonl')).map((m) => ({
  seq: m.seq, ts: m.ts, agentId: m.agentId, kind: m.kind,
  content: m.content, tags: m.tags, hash: m.hash,
}));

// ---- headline ----
const headline = {
  totalTurns: allTurns.length,
  totalCost: allTurns.reduce((a, t) => a + (t.cost || 0), 0),
  totalToolCalls: allTurns.reduce((a, t) => a + (t.toolCallCount || 0), 0),
  totalThinkingTokens: allTurns.reduce((a, t) => a + (t.thinkingTokens || 0), 0),
  totalViolations: allTurns.reduce((a, t) => a + (t.notes?.oracleViolations || 0), 0),
  filesCreated: allTurns.reduce((a, t) => a + (t.notes?.fileDiff?.created?.length || 0), 0),
  filesDeleted: allTurns.reduce((a, t) => a + (t.notes?.fileDiff?.deleted?.length || 0), 0),
  artifactCount: artifacts.length,
  artifactBytes: artifacts.reduce((a, x) => a + x.bytes, 0),
  agentsCreated: allTurns.length ? new Set(allTurns.map((t) => t.agentName)).size : 0,
};

// ---- stasis metric ----
const norm = (s) => (s || '').toLowerCase().replace(/[^a-z0-9 ]/g, ' ').replace(/\s+/g, ' ').trim();
function jac(a, b) {
  const A = new Set(a.split(' ').filter(Boolean)), B = new Set(b.split(' ').filter(Boolean));
  if (!A.size && !B.size) return 1;
  let i = 0; for (const x of A) if (B.has(x)) i++;
  return i / (A.size + B.size - i);
}
let longest = 0, cur = 0;
for (let i = 1; i < allTurns.length; i++) {
  if (jac(norm(allTurns[i - 1].text).slice(0, 400), norm(allTurns[i].text).slice(0, 400)) > 0.85) {
    cur++; longest = Math.max(longest, cur);
  } else cur = 0;
}

// ---- conclusion posts (written by the Scribe agent after each run) ----
// The raw Markdown is embedded so the site can render the actual post text, not just
// a filename. Bodies are capped so one enormous post cannot bloat the page.
const posts = readPosts(ARENA).map((p) => ({
  runId: p.runId,
  title: p.title,
  phase: p.phase,
  file: p.file,
  generatedAt: p.generatedAt,
  polished: Boolean(p.polished),
  halted: p.halted ?? null,
  totals: p.totals ?? null,
  agents: p.agents ?? [],
  body: String(p.body || '').slice(0, 60000),
}));

const payload = {
  generatedAt: new Date().toISOString(),
  headline,
  stasis: { longestNearIdenticalStreak: longest, threshold: 0.85 },
  substrates,
  runs,
  artifacts,
  memory,
  posts,
};

mkdirSync(join(SITE, 'data'), { recursive: true });
writeFileSync(join(SITE, 'data', 'findings.json'), JSON.stringify(payload, null, 2), 'utf8');
console.log(`exported ${runIds.length} runs, ${allTurns.length} turns, ${artifacts.length} artifacts, ${posts.length} posts`);
console.log(`headline: $${headline.totalCost.toFixed(4)} | ${headline.totalToolCalls} tool calls | ${headline.totalViolations} violations`);
console.log(`wrote ${join(SITE, 'data', 'findings.json')}`);
