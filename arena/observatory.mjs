/**
 * Swarm Observatory — a live web dashboard over the forensic ledger.
 *
 * WHY: the arena produces rich forensic data (per-turn reasoning, tool-call traces,
 * hash-chained memory, raw CLI event streams) but it was only readable as JSONL.
 * This exposes it as a UI so a run can be watched and audited visually.
 *
 * DESIGN:
 *   - zero npm dependencies (node:http + node:fs only), matching the arena
 *   - read-only over the ledger; it never writes to runs/ or world/
 *   - server-side aggregation so the browser never loads a 7 MB event stream
 *   - serves the raw CLI streams on demand, line-capped
 *
 * Usage: node observatory.mjs [--port 7777]
 */

import { createServer } from 'node:http';
import { readFileSync, existsSync, readdirSync, statSync } from 'node:fs';
import { join, extname, normalize } from 'node:path';
import { ARENA } from './paths.mjs';


const RUNS = join(ARENA, 'runs');
const WORLD = join(ARENA, 'world');
const MEMORY = join(ARENA, 'memory');

const portArg = process.argv.indexOf('--port');
const PORT = portArg !== -1 ? parseInt(process.argv[portArg + 1], 10) : 7777;

// ---------------------------------------------------------------- data helpers

function readJsonl(path, limit = null) {
  if (!existsSync(path)) return [];
  const lines = readFileSync(path, 'utf8').split(/\r?\n/).filter(Boolean);
  const use = limit ? lines.slice(-limit) : lines;
  const out = [];
  for (const l of use) { try { out.push(JSON.parse(l)); } catch {} }
  return out;
}

function listRuns() {
  if (!existsSync(RUNS)) return [];
  return readdirSync(RUNS, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => {
      const dir = join(RUNS, d.name);
      const turns = existsSync(join(dir, 'turns.jsonl'));
      const summary = existsSync(join(dir, 'summary.json'));
      let mtime = 0;
      try { mtime = statSync(dir).mtimeMs; } catch {}
      return { id: d.name, hasTurns: turns, finished: summary, mtime };
    })
    .sort((a, b) => b.mtime - a.mtime);
}

function worldFiles() {
  const out = [];
  if (!existsSync(WORLD)) return out;
  (function walk(d, base = '') {
    let entries;
    try { entries = readdirSync(d, { withFileTypes: true }); } catch { return; }
    for (const e of entries) {
      const rel = base ? `${base}/${e.name}` : e.name;
      if (e.isDirectory()) { if (e.name !== '__pycache__') walk(join(d, e.name), rel); continue; }
      let size = 0;
      try { size = statSync(join(d, e.name)).size; } catch {}
      out.push({ rel, size });
    }
  })(WORLD);
  return out.sort((a, b) => b.size - a.size);
}

/** Normalise a raw CLI event into a thinking/acting step for the chain view. */
function buildThinkingChain(turn) {
  const steps = [];
  if (turn.thinkingTokens) {
    steps.push({ kind: 'think', label: `Reasoning (${turn.thinkingTokens.toLocaleString()} tokens)`, detail: null });
  }
  for (const tc of (turn.toolCalls || [])) {
    let cmd = null;
    const p = tc.params || {};
    cmd = p.CommandLine || p.command || p.TargetFile || p.path || p.file_path || null;
    steps.push({
      kind: 'tool',
      label: tc.tool,
      detail: cmd ? String(cmd).slice(0, 400) : (tc.params ? JSON.stringify(tc.params).slice(0, 400) : null),
      output: tc.output ? String(tc.output).slice(0, 1500) : null,
      duration: tc.durationSeconds,
    });
  }
  return steps;
}

// ---------------------------------------------------------------- API routes

function apiRuns() {
  return listRuns();
}

function apiRun(id) {
  const dir = join(RUNS, id);
  if (!existsSync(dir)) return { error: 'run not found' };
  // Prefer the priced file (has list-rate cost + reasoning backfilled) when present.
  const pricedPath = join(dir, 'turns-priced.jsonl');
  const turns = existsSync(pricedPath)
    ? readJsonl(pricedPath)
    : readJsonl(join(dir, 'turns.jsonl'));
  const events = readJsonl(join(dir, 'events.jsonl'));
  const incidents = readJsonl(join(dir, 'incidents.jsonl'));
  const summary = existsSync(join(dir, 'summary.json'))
    ? JSON.parse(readFileSync(join(dir, 'summary.json'), 'utf8')) : null;
  const scores = existsSync(join(dir, 'scores.json'))
    ? JSON.parse(readFileSync(join(dir, 'scores.json'), 'utf8')) : null;

  // Strip heavy fields from the list view; the detail endpoint serves them.
  const lightTurns = turns.map((t) => ({
    seq: t.seq, ts: t.ts, turn: t.turn, agentId: t.agentId, agentName: t.agentName,
    substrate: t.substrate, model: t.model, ok: t.ok, error: t.error, timedOut: t.timedOut,
    thinkingTokens: t.thinkingTokens, cost: t.cost, usage: t.usage,
    pricing: t.pricing || null,
    reasoningChars: t.reasoningChars || (t.reasoning ? t.reasoning.length : 0),
    toolCallCount: t.toolCallCount, textLength: t.textLength, rawEventCount: t.rawEventCount,
    hash: t.hash, prev: t.prev,
    fileDiff: t.notes?.fileDiff || { created: [], modified: [], deleted: [] },
    oracleViolations: t.notes?.oracleViolations || 0,
    preview: (t.text || '').slice(0, 400),
  }));

  const bySub = {};
  for (const t of turns) {
    const k = t.substrate;
    bySub[k] = bySub[k] || { n: 0, ok: 0, cost: 0, listCost: 0, absorbed: 0, tools: 0, think: 0, chars: 0, files: 0, reasonChars: 0 };
    const b = bySub[k];
    b.n++; if (t.ok) b.ok++;
    b.cost += t.cost || 0;
    b.listCost += t.pricing?.listCost || 0;
    b.absorbed += t.pricing?.absorbed || 0;
    b.tools += t.toolCallCount || 0;
    b.think += t.thinkingTokens || 0;
    b.chars += t.textLength || 0;
    b.reasonChars += t.reasoningChars || (t.reasoning ? t.reasoning.length : 0);
    b.files += (t.notes?.fileDiff?.created?.length || 0) + (t.notes?.fileDiff?.modified?.length || 0);
  }

  const byAgent = {};
  for (const t of turns) {
    const k = t.agentName;
    byAgent[k] = byAgent[k] || { n: 0, ok: 0, cost: 0, listCost: 0, tools: 0, think: 0, files: 0, substrate: t.substrate, reasonChars: 0 };
    const b = byAgent[k];
    b.n++; if (t.ok) b.ok++;
    b.cost += t.cost || 0;
    b.listCost += t.pricing?.listCost || 0;
    b.tools += t.toolCallCount || 0;
    b.think += t.thinkingTokens || 0;
    b.reasonChars += t.reasoningChars || (t.reasoning ? t.reasoning.length : 0);
    b.files += (t.notes?.fileDiff?.created?.length || 0) + (t.notes?.fileDiff?.modified?.length || 0);
  }

  return {
    id, summary, turns: lightTurns, events, incidents, scores,
    bySub, byAgent,
    totals: {
      turns: turns.length,
      ok: turns.filter((t) => t.ok).length,
      cost: turns.reduce((a, t) => a + (t.cost || 0), 0),
      listCost: turns.reduce((a, t) => a + (t.pricing?.listCost || 0), 0),
      absorbed: turns.reduce((a, t) => a + (t.pricing?.absorbed || 0), 0),
      cacheSavings: turns.reduce((a, t) => a + (t.pricing?.cacheSavings || 0), 0),
      tools: turns.reduce((a, t) => a + (t.toolCallCount || 0), 0),
      think: turns.reduce((a, t) => a + (t.thinkingTokens || 0), 0),
      reasonChars: turns.reduce((a, t) => a + (t.reasoningChars || (t.reasoning ? t.reasoning.length : 0)), 0),
      files: turns.reduce((a, t) => a + (t.notes?.fileDiff?.created?.length || 0) + (t.notes?.fileDiff?.modified?.length || 0), 0),
      violations: turns.reduce((a, t) => a + (t.notes?.oracleViolations || 0), 0),
      deleted: turns.reduce((a, t) => a + (t.notes?.fileDiff?.deleted?.length || 0), 0),
    },
  };
}

function apiTurn(runId, seq) {
  const dir = join(RUNS, runId);
  const pricedPath = join(dir, 'turns-priced.jsonl');
  const turns = existsSync(pricedPath) ? readJsonl(pricedPath) : readJsonl(join(dir, 'turns.jsonl'));
  const t = turns.find((x) => String(x.seq) === String(seq));
  if (!t) return { error: 'turn not found' };
  return { ...t, chain: buildThinkingChain(t) };
}

/**
 * Reasoning endpoint — returns the model's internal monologue for a turn.
 *
 * Kept separate from apiTurn because reasoning can be tens of KB and most
 * dashboard interactions do not need it.
 */
function apiReasoning(runId, seq) {
  const dir = join(RUNS, runId);
  const pricedPath = join(dir, 'turns-priced.jsonl');
  const turns = existsSync(pricedPath) ? readJsonl(pricedPath) : readJsonl(join(dir, 'turns.jsonl'));
  const t = turns.find((x) => String(x.seq) === String(seq));
  if (!t) return { error: 'turn not found' };
  return {
    seq: t.seq,
    agent: t.agentName,
    substrate: t.substrate,
    model: t.model,
    reasoning: t.reasoning || '',
    reasoningChars: t.reasoningChars || (t.reasoning || '').length,
    reasoningBlocks: t.reasoningBlocks || 0,
    thinkingTokens: t.thinkingTokens || 0,
    available: Boolean(t.reasoning && t.reasoning.length),
    note: (t.reasoning && t.reasoning.length)
      ? null
      : (t.substrate === 'agy'
        ? 'The Antigravity CLI reports thinking-token counts but does not stream the reasoning text.'
        : 'No reasoning captured for this turn (recorded before reasoning capture was added).'),
  };
}

function apiMemory() {
  const scopes = existsSync(MEMORY) ? readdirSync(MEMORY).filter((f) => f.endsWith('.jsonl')) : [];
  const out = {};
  for (const s of scopes) out[s.replace(/\.jsonl$/, '')] = readJsonl(join(MEMORY, s));
  return out;
}

function apiRawStream(runId, file, maxLines = 400) {
  const p = join(RUNS, runId, normalize(file).replace(/^(\.\.[/\\])+/, ''));
  if (!existsSync(p)) return { error: 'file not found' };
  const size = statSync(p).size;
  const lines = readFileSync(p, 'utf8').split(/\r?\n/);
  const slice = lines.slice(-maxLines).filter(Boolean).map((l) => {
    try { return JSON.parse(l); } catch { return { _raw: l.slice(0, 500) }; }
  });
  return { file, sizeBytes: size, totalLines: lines.length, showing: slice.length, events: slice };
}

function apiWorld() {
  return worldFiles();
}

function apiFile(rel) {
  const p = join(WORLD, normalize(rel).replace(/^(\.\.[/\\])+/, ''));
  if (!existsSync(p)) return { error: 'not found' };
  const st = statSync(p);
  if (!st.isFile()) return { error: 'not a file' };
  if (st.size > 400_000) return { error: 'file too large', size: st.size };
  return { rel, size: st.size, content: readFileSync(p, 'utf8') };
}

// ---------------------------------------------------------------- server

function send(res, code, body, type = 'application/json') {
  const data = typeof body === 'string' ? body : JSON.stringify(body);
  res.writeHead(code, { 'Content-Type': type, 'Cache-Control': 'no-store' });
  res.end(data);
}

const server = createServer((req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  const path = url.pathname;
  try {
    if (path === '/' || path === '/index.html') {
      return send(res, 200, PAGE, 'text/html; charset=utf-8');
    }
    if (path === '/api/runs') return send(res, 200, apiRuns());
    if (path.startsWith('/api/run/')) return send(res, 200, apiRun(decodeURIComponent(path.slice(9))));
    if (path.startsWith('/api/turn/')) {
      const [, , , runId, seq] = path.split('/');
      return send(res, 200, apiTurn(decodeURIComponent(runId), seq));
    }
    if (path.startsWith('/api/reasoning/')) {
      const [, , , runId, seq] = path.split('/');
      return send(res, 200, apiReasoning(decodeURIComponent(runId), seq));
    }
    if (path === '/api/memory') return send(res, 200, apiMemory());
    if (path === '/api/world') return send(res, 200, apiWorld());
    if (path === '/api/file') return send(res, 200, apiFile(url.searchParams.get('rel') || ''));
    if (path === '/api/raw') {
      const max = parseInt(url.searchParams.get('lines') || '400', 10);
      return send(res, 200, apiRawStream(
        url.searchParams.get('run'), url.searchParams.get('file'), max));
    }
    send(res, 404, { error: 'not found' });
  } catch (e) {
    send(res, 500, { error: String(e), stack: e?.stack?.slice(0, 800) });
  }
});

server.listen(PORT, '127.0.0.1', () => {
  console.log(`Swarm Observatory  ->  http://127.0.0.1:${PORT}`);
  console.log(`  arena:  ${ARENA}`);
  console.log(`  runs:   ${listRuns().length}`);
});

// ---------------------------------------------------------------- frontend

const PAGE = String.raw`<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Swarm Observatory</title>
<style>
  :root{
    --bg:#0b0f17; --panel:#121826; --panel2:#171f31; --line:#243049;
    --fg:#e6edf7; --dim:#8b9ab3; --accent:#4c9aff; --ok:#3fb950;
    --warn:#d29922; --bad:#f85149; --think:#a371f7;
    font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--fg);font-size:13px;line-height:1.5}
  a{color:var(--accent);text-decoration:none}
  header{display:flex;align-items:center;gap:16px;padding:12px 20px;border-bottom:1px solid var(--line);
    background:var(--panel);position:sticky;top:0;z-index:10;flex-wrap:wrap}
  header h1{font-size:14px;margin:0;letter-spacing:.5px}
  .pill{background:var(--panel2);border:1px solid var(--line);border-radius:999px;padding:3px 10px;color:var(--dim);font-size:11px}
  .pill b{color:var(--fg);font-weight:600}
  select,input,button{background:var(--panel2);color:var(--fg);border:1px solid var(--line);
    border-radius:6px;padding:5px 9px;font-family:inherit;font-size:12px}
  button{cursor:pointer}
  button:hover{border-color:var(--accent)}
  nav{display:flex;gap:2px;padding:8px 20px;border-bottom:1px solid var(--line);background:var(--panel)}
  nav button{background:transparent;border:none;border-bottom:2px solid transparent;border-radius:0;
    padding:7px 14px;color:var(--dim)}
  nav button.on{color:var(--fg);border-bottom-color:var(--accent)}
  main{padding:18px 20px 60px;max-width:1500px}
  .grid{display:grid;gap:14px}
  .cards{grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}
  .card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px 14px}
  .card .k{color:var(--dim);font-size:11px;text-transform:uppercase;letter-spacing:.6px}
  .card .v{font-size:20px;margin-top:5px;font-weight:600}
  .card .s{color:var(--dim);font-size:11px;margin-top:2px}
  table{width:100%;border-collapse:collapse;background:var(--panel);border:1px solid var(--line);border-radius:10px;overflow:hidden}
  th,td{text-align:left;padding:8px 11px;border-bottom:1px solid var(--line);vertical-align:top}
  th{background:var(--panel2);color:var(--dim);font-size:11px;text-transform:uppercase;letter-spacing:.5px;font-weight:600}
  tr:last-child td{border-bottom:none}
  tr.clickable:hover{background:var(--panel2);cursor:pointer}
  .ok{color:var(--ok)} .bad{color:var(--bad)} .warn{color:var(--warn)} .dim{color:var(--dim)}
  .tag{display:inline-block;padding:1px 7px;border-radius:5px;background:var(--panel2);
    border:1px solid var(--line);font-size:11px;color:var(--dim)}
  .bar{height:7px;background:var(--panel2);border-radius:4px;overflow:hidden;margin-top:5px}
  .bar>i{display:block;height:100%;background:var(--accent)}
  pre{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px;
    overflow:auto;max-height:520px;white-space:pre-wrap;word-break:break-word;font-size:12px;margin:0}
  .chain{display:flex;flex-direction:column;gap:0}
  .step{display:flex;gap:11px;padding:9px 0;border-bottom:1px dashed var(--line)}
  .step:last-child{border-bottom:none}
  .step .ico{width:22px;height:22px;flex:0 0 22px;border-radius:6px;display:grid;place-items:center;
    font-size:11px;background:var(--panel2);border:1px solid var(--line)}
  .step.think .ico{color:var(--think);border-color:var(--think)}
  .step.tool .ico{color:var(--accent);border-color:var(--accent)}
  .step .body{flex:1;min-width:0}
  .step .lbl{font-weight:600}
  .step .det{color:var(--dim);font-size:11.5px;margin-top:3px;white-space:pre-wrap;word-break:break-word}
  .mono{font-family:inherit}
  .two{grid-template-columns:1fr 1fr}
  .split{display:grid;grid-template-columns:280px 1fr;gap:14px;align-items:start}
  .list{background:var(--panel);border:1px solid var(--line);border-radius:10px;overflow:hidden;max-height:640px;overflow-y:auto}
  .list .it{padding:9px 12px;border-bottom:1px solid var(--line);cursor:pointer}
  .list .it:hover{background:var(--panel2)}
  .list .it.on{background:var(--panel2);border-left:2px solid var(--accent)}
  .list .it .t{font-weight:600}
  .list .it .m{color:var(--dim);font-size:11px;margin-top:2px}
  .empty{color:var(--dim);padding:24px;text-align:center}
  .hash{font-size:10.5px;color:var(--dim)}
  h2{font-size:13px;margin:20px 0 10px;color:var(--dim);text-transform:uppercase;letter-spacing:.7px}
  .kv{display:grid;grid-template-columns:auto 1fr;gap:4px 14px;font-size:12px}
  .kv .k{color:var(--dim)}
  .scroll{max-height:600px;overflow:auto}
  .badge-ok{color:var(--ok);border-color:var(--ok)}
  .badge-bad{color:var(--bad);border-color:var(--bad)}
</style>
</head>
<body>
<header>
  <h1>&#9679; SWARM OBSERVATORY</h1>
  <span class="pill">run <select id="runSel"></select></span>
  <span class="pill" id="pStatus">loading</span>
  <span class="pill">turns <b id="pTurns">-</b></span>
  <span class="pill">tools <b id="pTools">-</b></span>
  <span class="pill">think <b id="pThink">-</b></span>
  <span class="pill">cost <b id="pCost">-</b></span>
  <span class="pill" id="pViol">violations <b>-</b></span>
  <span style="flex:1"></span>
  <button onclick="load()">&#8635; refresh</button>
</header>
<nav>
  <button data-v="overview" class="on">Overview</button>
  <button data-v="thinking">Thinking</button>
  <button data-v="agents">Agents</button>
  <button data-v="turns">Turn Chain</button>
  <button data-v="memory">Shared Memory</button>
  <button data-v="substrates">Substrates &amp; Cost</button>
  <button data-v="scores">Scores</button>
  <button data-v="world">Artifacts</button>
  <button data-v="integrity">Integrity</button>
</nav>
<main id="app"><div class="empty">loading&hellip;</div></main>

<script>
let RUNS=[], RUN=null, VIEW='overview', SELTURN=null, SELAGENT=null, MEM=null, WORLD=null, TURN=null, REASONING=null;

const $ = (s)=>document.querySelector(s);
const esc = (s)=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const num = (n)=>n==null?'-':Number(n).toLocaleString();
const kb  = (n)=>n<1024?n+' B':(n/1024).toFixed(1)+' KB';
const money=(n)=>'$'+(n||0).toFixed(5);
const ago = (ts)=>{const d=(Date.now()-new Date(ts).getTime())/1000;
  if(d<60)return Math.round(d)+'s ago'; if(d<3600)return Math.round(d/60)+'m ago';
  return Math.round(d/3600)+'h ago';};

async function j(u){const r=await fetch(u);return r.json();}

async function boot(){
  RUNS = await j('/api/runs');
  const sel = $('#runSel');
  sel.innerHTML = RUNS.map(r=>'<option value="'+esc(r.id)+'">'+esc(r.id)+(r.finished?'':' (live)')+'</option>').join('');
  sel.onchange = ()=>{ load(); };
  await load();
}

async function load(){
  const id = $('#runSel').value || (RUNS[0]&&RUNS[0].id);
  if(!id){ $('#app').innerHTML='<div class="empty">no runs found. Run <b>node phase1.mjs</b> first.</div>'; return; }
  RUN = await j('/api/run/'+encodeURIComponent(id));
  if(RUN.error){ $('#app').innerHTML='<div class="empty">'+esc(RUN.error)+'</div>'; return; }
  MEM = await j('/api/memory');
  WORLD = await j('/api/world');
  const t = RUN.totals;
  $('#pTurns').textContent = t.turns;
  $('#pTools').textContent = num(t.tools);
  $('#pThink').textContent = num(t.think);
  $('#pCost').textContent = money(t.cost);
  $('#pViol').innerHTML = t.violations;
  $('#pViol').className = 'pill '+(t.violations?'badge-bad':'badge-ok');
  $('#pStatus').textContent = RUN.summary ? ('halted: '+(RUN.summary.halted||'finished')) : 'RUNNING';
  render();
}

function render(){
  const v = VIEW;
  if(v==='overview') return viewOverview();
  if(v==='thinking') return viewThinking();
  if(v==='agents') return viewAgents();
  if(v==='turns') return viewTurns();
  if(v==='memory') return viewMemory();
  if(v==='substrates') return viewSubstrates();
  if(v==='scores') return viewScores();
  if(v==='world') return viewWorld();
  if(v==='integrity') return viewIntegrity();
}

/* ---------------- THINKING: the model's internal monologue ---------------- */
function viewThinking(){
  let h='<h2>What the agents are thinking</h2>'+
    '<div class="card" style="margin-bottom:14px"><div class="dim">'+
    'This is the model\u2019s actual internal monologue, recovered from the streaming '+
    '<b>thinking_delta</b> events in the raw CLI output. It is not a summary and not the '+
    'final answer \u2014 it is the deliberation that produced them.'+
    '</div></div>';

  const withReasoning = RUN.turns.filter(x=>x.reasoningChars>0);
  h+='<div class="grid cards">';
  h+=card('Turns with reasoning', withReasoning.length+' / '+RUN.turns.length, 'captured');
  h+=card('Reasoning chars', num(RUN.totals.reasonChars), 'total deliberation');
  h+=card('Thinking tokens', num(RUN.totals.think), 'billed reasoning');
  h+='</div>';

  if(!withReasoning.length){
    h+='<div class="empty">No reasoning captured in this run.<br><br>'+
       'Reasoning capture was added after this run was recorded. Start a new run '+
       '(<b>node phase1.mjs</b>) and the Thinking tab will populate.</div>';
    return $('#app').innerHTML=h;
  }

  h+='<h2>Reasoning by turn</h2><div class="split"><div class="list">';
  for(const x of RUN.turns){
    const has=x.reasoningChars>0;
    h+='<div class="it'+(String(SELTURN)===String(x.seq)?' on':'')+'" onclick="openReasoning('+x.seq+')">'+
      '<div class="t">#'+x.seq+' '+esc(x.agentName)+' '+(has?'':'<span class="dim">(none)</span>')+'</div>'+
      '<div class="m">'+esc(x.substrate)+' &middot; '+num(x.reasoningChars)+' chars</div></div>';
  }
  h+='</div><div id="reasonBox">'+
     (REASONING? renderReasoning(REASONING) :
      '<div class="empty">select a turn to read its internal monologue</div>')+
     '</div></div>';
  $('#app').innerHTML=h;
}

async function openReasoning(seq){
  REASONING = await j('/api/reasoning/'+encodeURIComponent(RUN.id)+'/'+seq);
  SELTURN=seq; render();
}

function renderReasoning(r){
  if(r.error) return '<div class="empty">'+esc(r.error)+'</div>';
  let h='<div class="card"><div class="kv">';
  h+=kv('turn', '#'+r.seq+' &middot; '+esc(r.agent));
  h+=kv('substrate', esc(r.substrate)+' &middot; '+esc(r.model||''));
  h+=kv('thinking tokens', num(r.thinkingTokens));
  h+=kv('reasoning length', num(r.reasoningChars)+' chars in '+r.reasoningBlocks+' block(s)');
  h+='</div></div>';
  if(!r.available){
    h+='<div class="empty">'+esc(r.note||'no reasoning captured')+'</div>';
    return h;
  }
  h+='<h2>Internal monologue</h2><pre>'+esc(r.reasoning)+'</pre>';
  return h;
}

function viewOverview(){
  const t=RUN.totals, s=RUN.summary;
  const live = !s;
  let h = '<div class="grid cards">';
  h += card('Turns', t.turns, t.ok+' ok &middot; '+(t.turns-t.ok)+' failed');
  h += card('Tool calls', num(t.tools), (t.tools/Math.max(1,t.turns)).toFixed(1)+' per turn');
  h += card('Thinking tokens', num(t.think), 'reasoning captured');
  h += card('Cost', money(t.cost), 'reported by CLI');
  h += card('Files', num(t.files), t.deleted? t.deleted+' deleted':'none deleted');
  h += card('Oracle violations', t.violations, t.violations? 'review needed':'clean');
  h += '</div>';

  if(s){
    h += '<h2>Run summary</h2><div class="card"><div class="kv">';
    h += kv('run id', esc(s.runId));
    h += kv('phase', esc(s.phase));
    h += kv('halted', esc(s.halted||'-'));
    h += kv('wall clock', (s.wallClockMinutes||0)+' min');
    h += kv('agents created', s.population? s.population.created : '-');
    h += kv('agents living', s.population? s.population.living : '-');
    h += kv('memory entries', s.memory? s.memory.totalEntries : '-');
    h += kv('spawns / retires', (s.spawnEvents||0)+' / '+(s.retireEvents||0));
    h += kv('world files', s.worldFiles||'-');
    h += '</div></div>';
  }

  h += '<h2>Turn timeline</h2>';
  h += '<table><thead><tr><th>#</th><th>agent</th><th>substrate</th><th>status</th>'+
       '<th>tools</th><th>think</th><th>cost</th><th>files</th><th>viol</th><th>age</th></tr></thead><tbody>';
  for(const x of RUN.turns){
    const fd=x.fileDiff||{created:[],modified:[],deleted:[]};
    h += '<tr class="clickable" onclick="openTurn('+x.seq+')">'+
      '<td>'+x.seq+'</td><td>'+esc(x.agentName)+'</td><td><span class="tag">'+esc(x.substrate)+'</span></td>'+
      '<td class="'+(x.ok?'ok':'bad')+'">'+(x.ok?'ok':esc(x.error||'failed'))+'</td>'+
      '<td>'+x.toolCallCount+'</td><td>'+num(x.thinkingTokens)+'</td><td>'+money(x.cost)+'</td>'+
      '<td>+'+(fd.created||[]).length+' ~'+(fd.modified||[]).length+
        ((fd.deleted||[]).length?' <span class="bad">-'+(fd.deleted||[]).length+'</span>':'')+'</td>'+
      '<td class="'+(x.oracleViolations?'bad':'dim')+'">'+x.oracleViolations+'</td>'+
      '<td class="dim">'+ago(x.ts)+'</td></tr>';
  }
  h += '</tbody></table>';
  $('#app').innerHTML = h;
}

function viewAgents(){
  let h='<h2>Agent behaviour</h2><table><thead><tr><th>agent</th><th>substrate</th><th>turns</th>'+
    '<th>ok</th><th>tools</th><th>think</th><th>files</th><th>cost</th></tr></thead><tbody>';
  for(const [name,b] of Object.entries(RUN.byAgent)){
    h += '<tr class="clickable" onclick="SELAGENT=\''+esc(name)+'\';VIEW=\'turns\';setNav();render()">'+
      '<td><b>'+esc(name)+'</b></td><td><span class="tag">'+esc(b.substrate)+'</span></td>'+
      '<td>'+b.n+'</td><td class="'+(b.ok===b.n?'ok':'warn')+'">'+b.ok+'/'+b.n+'</td>'+
      '<td>'+b.tools+'</td><td>'+num(b.think)+'</td><td>'+b.files+'</td><td>'+money(b.cost)+'</td></tr>';
  }
  h += '</tbody></table>';

  const s = RUN.summary;
  if(s && s.population && s.population.roster){
    h += '<h2>Roster (from last state snapshot)</h2><table><thead><tr><th>id</th><th>name</th>'+
      '<th>gen</th><th>substrate</th><th>alive</th><th>turns lived</th><th>purpose</th></tr></thead><tbody>';
    for(const a of s.population.roster){
      h += '<tr><td class="dim">'+esc(a.id)+'</td><td><b>'+esc(a.name)+'</b></td><td>'+a.generation+'</td>'+
        '<td><span class="tag">'+esc(a.substrate)+'</span></td>'+
        '<td class="'+(a.alive?'ok':'bad')+'">'+(a.alive?'alive':'retired')+'</td>'+
        '<td>'+a.turnsLived+'</td><td class="dim">'+esc(a.purpose||'')+'</td></tr>';
    }
    h += '</tbody></table>';
  }

  if(RUN.events && RUN.events.length){
    h += '<h2>Population events</h2><table><thead><tr><th>kind</th><th>detail</th><th>when</th></tr></thead><tbody>';
    for(const e of RUN.events.slice().reverse()){
      h += '<tr><td><span class="tag">'+esc(e.kind)+'</span></td><td class="dim">'+
        esc(JSON.stringify(e.detail||{}).slice(0,220))+'</td><td class="dim">'+ago(e.ts)+'</td></tr>';
    }
    h += '</tbody></table>';
  }
  $('#app').innerHTML=h;
}

function viewTurns(){
  let list = RUN.turns;
  if(SELAGENT) list = list.filter(x=>x.agentName===SELAGENT);
  let h='<div class="split"><div class="list">';
  h += '<div class="it'+(SELAGENT?'':' on')+'" onclick="SELAGENT=null;render()"><div class="t">All agents</div>'+
       '<div class="m">'+RUN.turns.length+' turns</div></div>';
  for(const x of list){
    h += '<div class="it'+(String(SELTURN)===String(x.seq)?' on':'')+'" onclick="openTurn('+x.seq+')">'+
      '<div class="t">#'+x.seq+' '+esc(x.agentName)+' <span class="'+(x.ok?'ok':'bad')+'">'+(x.ok?'':'FAIL')+'</span></div>'+
      '<div class="m">'+esc(x.substrate)+' &middot; '+x.toolCallCount+' tools &middot; '+money(x.cost)+'</div></div>';
  }
  h += '</div><div id="turnDetail">'+
    (TURN? renderTurn(TURN) : '<div class="empty">select a turn to inspect its chain of thinking</div>')+
    '</div></div>';
  $('#app').innerHTML=h;
}

async function openTurn(seq){
  TURN = await j('/api/turn/'+encodeURIComponent(RUN.id)+'/'+seq);
  SELTURN = seq;
  VIEW='turns'; setNav();
  if(!SELAGENT) SELAGENT = TURN.agentName;
  render();
}

function renderTurn(t){
  const fd=t.notes&&t.notes.fileDiff||{created:[],modified:[],deleted:[]};
  let h='<div class="card"><div class="kv">';
  h+=kv('turn', '#'+t.seq+' &middot; '+esc(t.agentName)+' ('+esc(t.agentId)+')');
  h+=kv('substrate', esc(t.substrate)+' &middot; '+esc(t.model||''));
  h+=kv('status', t.ok?'<span class="ok">ok</span>':'<span class="bad">'+esc(t.error||'failed')+'</span>'+(t.timedOut?' (timeout)':''));
  h+=kv('thinking tokens', num(t.thinkingTokens));
  h+=kv('tool calls', t.toolCallCount);
  h+=kv('cost', money(t.cost));
  h+=kv('raw events kept', num(t.rawEventCount));
  h+=kv('ledger hash', '<span class="hash">'+esc(t.hash)+'</span>');
  h+=kv('prev hash', '<span class="hash">'+esc(t.prev)+'</span>');
  h+=kv('timestamp', esc(t.ts));
  h+='</div></div>';

  if(fd.created.length||fd.modified.length||fd.deleted.length){
    h+='<h2>File changes</h2><div class="card">';
    for(const f of fd.created) h+='<div class="ok">+ '+esc(f)+'</div>';
    for(const f of fd.modified) h+='<div class="warn">~ '+esc(f)+'</div>';
    for(const f of fd.deleted) h+='<div class="bad">- '+esc(f)+' (DELETED)</div>';
    h+='</div>';
  }

  h+='<h2>Chain of thinking ('+(t.chain||[]).length+' steps)</h2><div class="card"><div class="chain">';
  for(const s of (t.chain||[])){
    h+='<div class="step '+s.kind+'"><div class="ico">'+(s.kind==='think'?'&#129504;':'&#9881;')+'</div><div class="body">'+
      '<div class="lbl">'+esc(s.label)+'</div>'+
      (s.detail?'<div class="det">'+esc(s.detail)+'</div>':'')+
      (s.output?'<div class="det dim">&rarr; '+esc(s.output)+'</div>':'')+
      '</div></div>';
  }
  h+='</div></div>';

  // Reasoning trace, if captured for this turn.
  if(t.reasoning && t.reasoning.length){
    h+='<h2>Internal monologue <span class="dim">('+num(t.reasoningChars)+' chars, '+
       (t.reasoningBlocks||1)+' block(s))</span></h2><pre>'+esc(t.reasoning)+'</pre>';
  } else {
    h+='<h2>Internal monologue</h2><div class="card"><div class="dim">'+
       (t.substrate==='agy'
         ? 'The Antigravity CLI reports thinking-token counts but does not stream reasoning text.'
         : 'Not captured for this turn (recorded before reasoning capture was added).')+
       '</div></div>';
  }

  if(t.pricing){
    h+='<h2>Cost breakdown</h2><div class="card"><div class="kv">';
    h+=kv('provider / plan', esc(t.pricing.provider)+' &middot; '+esc(t.pricing.plan));
    h+=kv('fresh input', num(t.pricing.tokens.fresh)+' tok &times; $'+t.pricing.rate.fresh+'/M = $'+t.pricing.breakdown.freshCost.toFixed(6));
    h+=kv('cached input', num(t.pricing.tokens.cached)+' tok &times; $'+t.pricing.rate.cached+'/M = $'+t.pricing.breakdown.cachedCost.toFixed(6));
    h+=kv('output', num(t.pricing.tokens.out)+' tok &times; $'+t.pricing.rate.out+'/M = $'+t.pricing.breakdown.outCost.toFixed(6));
    h+=kv('cache hit rate', (t.pricing.cacheHitRate*100).toFixed(1)+'%');
    h+=kv('list-rate cost', '<b>'+money(t.pricing.listCost)+'</b>');
    h+=kv('reported cost', money(t.pricing.reportedCost));
    h+=kv('absorbed', money(t.pricing.absorbed));
    h+=kv('saved by caching', money(t.pricing.cacheSavings));
    h+='</div></div>';
  }

  h+='<h2>Agent output</h2><pre>'+esc(t.text||'(no text)')+'</pre>';

  if(t.stdoutPath){
    h+='<h2>Raw CLI event stream</h2><div class="card"><button onclick="loadRaw(\''+
       esc(String(t.stdoutPath).split('\\\\').pop())+'\')">load last 200 raw events</button>'+
       '<div id="rawBox"></div></div>';
  }
  return h;
}

async function loadRaw(file){
  const box=document.getElementById('rawBox');
  box.innerHTML='<div class="empty">loading&hellip;</div>';
  const r=await j('/api/raw?run='+encodeURIComponent(RUN.id)+'&file='+encodeURIComponent(file)+'&lines=200');
  if(r.error){box.innerHTML='<div class="empty">'+esc(r.error)+'</div>';return;}
  box.innerHTML='<div class="dim" style="margin:8px 0">'+r.totalLines+' lines total, '+
    kb(r.sizeBytes)+' on disk &middot; showing last '+r.showing+'</div><pre>'+esc(JSON.stringify(r.events,null,1))+'</pre>';
}

function viewMemory(){
  const scopes=Object.keys(MEM||{});
  if(!scopes.length) return $('#app').innerHTML='<div class="empty">no memory recorded yet</div>';
  let h='<h2>Shared commons &mdash; hash-chained, append-only</h2>';
  const all=[]; for(const s of scopes) for(const e of MEM[s]) all.push(e);
  all.sort((a,b)=>(a.ts<b.ts?-1:1));
  const byKind={}; for(const e of all) byKind[e.kind]=(byKind[e.kind]||0)+1;
  h+='<div class="grid cards">';
  h+=card('Entries', all.length, scopes.length+' scope(s)');
  for(const [k,v] of Object.entries(byKind)) h+=card(k, v, 'entries');
  h+='</div>';
  h+='<h2>Timeline</h2><table><thead><tr><th>seq</th><th>agent</th><th>kind</th><th>content</th><th>hash</th></tr></thead><tbody>';
  for(const e of all){
    h+='<tr><td class="dim">'+e.seq+'</td><td><b>'+esc(e.agentId)+'</b></td>'+
      '<td><span class="tag">'+esc(e.kind)+'</span></td>'+
      '<td>'+esc(String(e.content).slice(0,600))+'</td>'+
      '<td class="hash">'+esc(e.hash)+'</td></tr>';
  }
  h+='</tbody></table>';
  $('#app').innerHTML=h;
}

function viewSubstrates(){
  const b=RUN.bySub||{};
  const t=RUN.totals;
  let h='<h2>Substrate comparison &mdash; priced at real API list rates</h2>';

  h+='<div class="grid cards">';
  h+=card('Reported cost', money(t.cost), 'what the CLIs claimed');
  h+=card('List-rate cost', money(t.listCost), 'at published API rates');
  h+=card('Absorbed', money(t.absorbed), 'covered by subscription/promo');
  h+=card('Saved by caching', money(t.cacheSavings), 'vs billing all input fresh');
  h+='</div>';

  h+='<div class="card" style="margin:14px 0"><div class="dim">'+
    'Reported cost alone is misleading: a CLI may show <b>$0.00</b> because a subscription or '+
    'promotional period is covering it, not because the tokens were free. <b>List-rate cost</b> '+
    'prices every substrate on the same basis by applying published per-token rates to the actual '+
    'token counts, so the comparison is apples-to-apples.'+
    '</div></div>';

  h+='<table><thead><tr><th>substrate</th><th>turns</th><th>success</th><th>tools/turn</th>'+
     '<th>think/turn</th><th>reasoning/turn</th><th>chars/turn</th><th>reported</th>'+
     '<th>list-rate</th><th>$/turn</th></tr></thead><tbody>';
  for(const [k,x] of Object.entries(b)){
    const pct=Math.round(100*x.ok/x.n);
    h+='<tr><td><b>'+esc(k)+'</b></td><td>'+x.n+'</td>'+
      '<td class="'+(pct===100?'ok':pct>=50?'warn':'bad')+'">'+pct+'%'+
      '<div class="bar"><i style="width:'+pct+'%"></i></div></td>'+
      '<td>'+(x.tools/x.n).toFixed(1)+'</td><td>'+num(Math.round(x.think/x.n))+'</td>'+
      '<td>'+num(Math.round((x.reasonChars||0)/x.n))+'</td>'+
      '<td>'+num(Math.round(x.chars/x.n))+'</td>'+
      '<td>'+money(x.cost)+'</td><td><b>'+money(x.listCost)+'</b></td>'+
      '<td>'+money(x.listCost/x.n)+'</td></tr>';
  }
  h+='</tbody></table>';

  // per-model rate table actually used
  const models={};
  for(const x of RUN.turns){ if(x.pricing){ models[x.model]=x.pricing.rate; } }
  if(Object.keys(models).length){
    h+='<h2>Rates applied (USD per 1M tokens)</h2><table><thead><tr><th>model</th>'+
       '<th>provider</th><th>plan</th><th>fresh in</th><th>cached in</th><th>output</th></tr></thead><tbody>';
    for(const [m,r] of Object.entries(models)){
      h+='<tr><td>'+esc(m)+'</td><td>'+esc(r.provider)+'</td><td class="dim">'+esc(r.plan)+'</td>'+
        '<td>$'+r.fresh.toFixed(3)+'</td><td>$'+r.cached.toFixed(3)+'</td><td>$'+r.out.toFixed(2)+'</td></tr>';
    }
    h+='</tbody></table>';
    h+='<div class="card" style="margin-top:10px"><div class="dim">Edit <b>pricing.mjs</b> to update rates.</div></div>';
  }
  $('#app').innerHTML=h;
}

/* ---------------- SCORES: claimed vs independently verified ---------------- */
function viewScores(){
  if(!RUN.scores){
    return $('#app').innerHTML='<div class="empty">No scores for this run.<br><br>'+
      'Run the independent scorer:<br><b>node score.mjs '+esc(RUN.id)+'</b></div>';
  }
  let h='<h2>Independent scores &mdash; computed in a separate process</h2>';
  h+='<table><thead><tr><th>domain</th><th>module</th><th>tests</th><th>test count</th>'+
     '<th>readme</th><th>TOTAL</th></tr></thead><tbody>';
  let sum=0,n=0;
  for(const [d,r] of Object.entries(RUN.scores)){
    sum+=r.total;n++;
    h+='<tr><td><b>'+esc(d)+'</b></td>'+
      '<td>'+r.points.module+'/40</td><td>'+r.points.tests+'/40</td>'+
      '<td>'+r.points.count+'/10</td><td>'+r.points.readme+'/10</td>'+
      '<td class="'+(r.total===100?'ok':r.total>=60?'warn':'bad')+'"><b>'+r.total+'/100</b></td></tr>';
  }
  h+='</tbody></table>';
  h+='<div class="grid cards" style="margin-top:14px">'+
     card('Mean verified', (sum/n).toFixed(1)+'/100', n+' domains')+'</div>';

  // tamper audit: did any agent touch the verification machinery?
  const suspects=[];
  for(const x of RUN.turns){
    for(const tc of [] ) {}
  }
  h+='<h2>Verification integrity</h2><div class="card"><div class="dim">'+
     'The scorer runs in a separate process from the agents and imports each module fresh. '+
     'Check the <b>Integrity</b> tab for file deletions and the <b>Turn Chain</b> for any agent '+
     'command that referenced the scorer.'+
     '</div></div>';
  $('#app').innerHTML=h;
}

function viewWorld(){
  let h='<h2>Artifacts produced ('+(WORLD||[]).length+' files, '+
    kb((WORLD||[]).reduce((a,f)=>a+f.size,0))+' total)</h2>';
  h+='<table><thead><tr><th>size</th><th>path</th><th></th></tr></thead><tbody>';
  for(const f of (WORLD||[])){
    h+='<tr><td class="dim">'+kb(f.size)+'</td><td>'+esc(f.rel)+'</td>'+
      '<td><button onclick="openFile(\''+esc(f.rel).replace(/'/g,"\\\\'")+'\')">view</button></td></tr>';
  }
  h+='</tbody></table><div id="fileBox"></div>';
  $('#app').innerHTML=h;
}

async function openFile(rel){
  const box=document.getElementById('fileBox');
  box.innerHTML='<h2>'+esc(rel)+'</h2><div class="empty">loading&hellip;</div>';
  const r=await j('/api/file?rel='+encodeURIComponent(rel));
  if(r.error){box.innerHTML='<h2>'+esc(rel)+'</h2><div class="empty">'+esc(r.error)+'</div>';return;}
  box.innerHTML='<h2>'+esc(rel)+' <span class="dim">('+kb(r.size)+')</span></h2><pre>'+esc(r.content)+'</pre>';
  box.scrollIntoView({behavior:'smooth'});
}

function viewIntegrity(){
  const s=RUN.summary;
  let h='<h2>Ledger integrity &mdash; hash chain verification</h2>';
  if(s&&s.ledgerIntegrity){
    h+='<table><thead><tr><th>log</th><th>chain</th><th>records</th><th>broken at</th></tr></thead><tbody>';
    for(const [k,v] of Object.entries(s.ledgerIntegrity)){
      h+='<tr><td><b>'+esc(k)+'</b></td><td class="'+(v.ok?'ok':'bad')+'">'+
        (v.ok?'VALID':'BROKEN')+'</td><td>'+v.count+'</td><td class="dim">'+(v.brokenAt==null?'-':v.brokenAt)+'</td></tr>';
    }
    h+='</tbody></table>';
  } else h+='<div class="empty">integrity summary written when the run finishes</div>';

  h+='<h2>Incidents</h2>';
  if(!RUN.incidents||!RUN.incidents.length) h+='<div class="card"><span class="ok">No incidents recorded.</span></div>';
  else{
    h+='<table><thead><tr><th>severity</th><th>kind</th><th>agent</th><th>detail</th><th>when</th></tr></thead><tbody>';
    for(const i of RUN.incidents.slice().reverse()){
      const cls=i.severity==='critical'?'bad':i.severity==='warn'?'warn':'dim';
      h+='<tr><td class="'+cls+'">'+esc(i.severity)+'</td><td><span class="tag">'+esc(i.kind)+'</span></td>'+
        '<td>'+esc(i.agentId||'-')+'</td><td class="dim">'+esc(JSON.stringify(i.detail||{}).slice(0,300))+'</td>'+
        '<td class="dim">'+ago(i.ts)+'</td></tr>';
    }
    h+='</tbody></table>';
  }

  h+='<h2>Verification method</h2><div class="card"><div class="dim">'+
     'Every record stores the hash of the previous record. Editing or deleting any earlier entry '+
     'invalidates every hash after it, so tampering is detectable rather than silent. The ledger '+
     'lives outside the agents\u2019 writable directory, so the audited cannot edit the audit trail.'+
     '</div></div>';
  $('#app').innerHTML=h;
}

function card(k,v,s){return '<div class="card"><div class="k">'+esc(k)+'</div><div class="v">'+v+'</div>'+
  (s?'<div class="s">'+s+'</div>':'')+'</div>';}
function kv(k,v){return '<div class="k">'+esc(k)+'</div><div>'+v+'</div>';}

function setNav(){
  document.querySelectorAll('nav button').forEach(b=>b.classList.toggle('on',b.dataset.v===VIEW));
}
document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>{VIEW=b.dataset.v;setNav();render();});
setInterval(()=>{ if(!document.hidden) load(); }, 15000);
boot();
</script>
</body>
</html>`;
