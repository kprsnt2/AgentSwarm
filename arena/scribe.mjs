/**
 * Scribe — the conclusion agent.
 *
 * THE PROBLEM THIS SOLVES
 * Every run produces tens of kilobytes of good Markdown, and none of it is readable
 * afterwards. The run's actual conclusions are scattered across:
 *   - runs/<id>/turns.jsonl      (what each agent said, turn by turn)
 *   - memory/global.jsonl        (the findings/artifacts agents explicitly recorded)
 *   - runs/<id>/summary.json     (population, cost, oracle verdicts, incidents)
 *   - world/*.md                 (the artifacts themselves)
 *
 * Reading all of that to find out "what did this run conclude?" costs more than
 * producing it. So after every run, ONE additional agent reads the evidence and
 * writes a single dated post: the run's conclusion, in prose, for a human.
 *
 * DESIGN: deterministic draft, then LLM polish.
 *
 *   1. `buildDraft()` assembles a structured draft from the LEDGER ONLY. No model
 *      is involved, so every number in it is a fact read straight out of the
 *      tamper-evident record. This is the ground truth.
 *   2. `polish()` hands that draft to a real substrate (default `agy`) with the
 *      agent identity "Sutra" and asks for the same post in better prose.
 *   3. If the model fails, times out, or returns something that fails the honesty
 *      checks, we keep the DETERMINISTIC draft. A post is always produced.
 *
 * That last point is the important one: the post is never missing, and it is never
 * worse than the ledger. The model can only improve the prose, never invent facts.
 *
 * HONESTY CHECKS (the reason the polish step is auditable):
 * The swarm's whole point is that agents overclaim. A conclusion agent is the most
 * dangerous place to let that slide — it has the last word. So every polished post
 * is checked for numbers that do not appear in the draft. Numbers in the prose must
 * be traceable to the ledger; a post that invents a figure is rejected and the
 * deterministic draft ships instead.
 *
 * Usage:
 *   import { writePost } from './scribe.mjs';
 *   await writePost({ root, runId, ledger, summary, config });
 *
 * CLI (manual backfill): see post.mjs
 */

import { existsSync, mkdirSync, readFileSync, readdirSync, unlinkSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

import { runTurn } from './substrate/substrates.mjs';

export const SCRIBE_NAME = 'Sutra';

/** Where posts live. One directory, one file per run, plus an index. */
export const POSTS_DIR = 'posts';

/**
 * The scribe's standing purpose. Injected as the agent's identity so the model is
 * writing AS an agent with a defined role, not as a generic summarizer.
 */
export const SCRIBE_PURPOSE =
  'Read the completed run\'s forensic record and write its conclusion as a single ' +
  'public post. Report what was actually established, at what confidence, and what ' +
  'remains unknown. Never overstate. The ledger is the only source of truth.';

// ---------------------------------------------------------------- small utils

function readJsonl(path) {
  if (!existsSync(path)) return [];
  const out = [];
  for (const line of readFileSync(path, 'utf8').split(/\r?\n/)) {
    const t = line.trim();
    if (!t) continue;
    try { out.push(JSON.parse(t)); } catch {}
  }
  return out;
}

function readJson(path) {
  if (!existsSync(path)) return null;
  try { return JSON.parse(readFileSync(path, 'utf8')); } catch { return null; }
}

function truncate(s, n) {
  const str = typeof s === 'string' ? s : String(s ?? '');
  return str.length <= n ? str : str.slice(0, n - 1) + '…';
}

/** Strip markdown noise so an excerpt reads as prose, not as formatting. */
function cleanProse(s) {
  return String(s || '')
    .replace(/```[\s\S]*?```/g, ' ')          // fenced code
    .replace(/`([^`]*)`/g, '$1')              // inline code
    .replace(/^\s{0,3}#{1,6}\s*/gm, '')       // headings
    .replace(/^\s*[-*+]\s+/gm, '')            // bullets
    .replace(/\*\*([^*]*)\*\*/g, '$1')        // bold
    .replace(/\*([^*]*)\*/g, '$1')            // italic
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')  // links
    .replace(/\|/g, ' ')                      // table pipes
    .replace(/\s+/g, ' ')
    .trim();
}

function slug(s) {
  return String(s || '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 60) || 'post';
}

// ---------------------------------------------------------------- the draft

/**
 * Build the deterministic draft from the ledger.
 *
 * EVERYTHING here is read from disk. There is no model in this function, which is
 * what makes it trustworthy: if the polished post disagrees with this, the post is
 * wrong, not the draft.
 */
export function buildDraft({ root, runId, summary = null, memory = null }) {
  const runDir = join(root, 'runs', runId);
  const turns = readJsonl(join(runDir, 'turns.jsonl'));
  const events = readJsonl(join(runDir, 'events.jsonl'));
  const incidents = readJsonl(join(runDir, 'incidents.jsonl'));
  const sum = summary || readJson(join(runDir, 'summary.json'));

  // --- memory entries written DURING this run ---
  // memory/global.jsonl is append-only across all runs, so we bound it by the run's
  // own time window rather than trusting a runId field (memory writes do not carry one).
  const allMemory = memory || readJsonl(join(root, 'memory', 'global.jsonl'));
  const runStart = turns.length ? turns[0].ts : null;
  const runEnd = turns.length ? turns[turns.length - 1].ts : null;
  const inWindow = (ts) => {
    if (!runStart || !ts) return false;
    if (ts < runStart) return false;
    if (runEnd && ts > runEnd) return false;
    return true;
  };
  // Fall back to "the tail of the commons" if timestamps are unusable, so a run with
  // malformed clocks still gets a post rather than an empty one.
  //
  // IMPORTANT: that fallback means the findings may belong to OTHER runs. The post
  // must say so — silently presenting another run's findings as this run's
  // conclusions is exactly the kind of unearned confidence this arena exists to
  // catch, and a conclusion agent is the worst place to let it slide.
  const scopedMemory = allMemory.filter((m) => inWindow(m.ts));
  const attributed = scopedMemory.length > 0;
  const memForRun = attributed ? scopedMemory : allMemory.slice(-40);

  const findings = memForRun.filter((m) => ['finding', 'artifact', 'hypothesis', 'observation'].includes(m.kind));
  const decisions = memForRun.filter((m) => m.kind === 'decision');

  // --- per-agent rollup ---
  const byAgent = {};
  for (const t of turns) {
    const k = t.agentName || t.agentId || 'unknown';
    byAgent[k] = byAgent[k] || {
      name: k, turns: 0, ok: 0, toolCalls: 0, created: 0, modified: 0,
      violations: 0, purpose: null, substrates: new Set(), lastText: '',
    };
    const b = byAgent[k];
    b.turns += 1;
    if (t.ok) b.ok += 1;
    b.toolCalls += t.toolCallCount || 0;
    b.created += t.notes?.fileDiff?.created?.length || 0;
    b.modified += t.notes?.fileDiff?.modified?.length || 0;
    b.violations += t.notes?.oracleViolations || 0;
    if (t.substrate) b.substrates.add(t.substrate);
    if (t.text) b.lastText = t.text;
  }
  // Attach purposes from spawn events (the roster in summary.json also has them).
  for (const e of events) {
    if (e.kind === 'agent_spawned' && e.detail?.name && byAgent[e.detail.name]) {
      byAgent[e.detail.name].purpose = e.detail.purpose || null;
    }
  }
  const roster = sum?.population?.roster || [];
  for (const r of roster) {
    if (r?.name && byAgent[r.name] && !byAgent[r.name].purpose) byAgent[r.name].purpose = r.purpose || null;
  }

  // --- files this run actually wrote (from the turn diffs, the authoritative source) ---
  const written = new Set();
  for (const t of turns) {
    for (const f of (t.notes?.fileDiff?.created || [])) written.add(f);
    for (const f of (t.notes?.fileDiff?.modified || [])) written.add(f);
  }

  const totals = {
    turns: turns.length,
    okTurns: turns.filter((t) => t.ok).length,
    agents: Object.keys(byAgent).length,
    toolCalls: turns.reduce((a, t) => a + (t.toolCallCount || 0), 0),
    thinkingTokens: turns.reduce((a, t) => a + (t.thinkingTokens || 0), 0),
    cost: turns.reduce((a, t) => a + (t.cost || 0), 0),
    violations: turns.reduce((a, t) => a + (t.notes?.oracleViolations || 0), 0),
    filesWritten: written.size,
    incidents: incidents.length,
  };

  const phase = turns[0]?.phase || sum?.phase || 'unknown';

  return {
    runId,
    phase,
    generatedAt: new Date().toISOString(),
    runStartedAt: runStart,
    runEndedAt: runEnd,
    halted: sum?.halted ?? null,
    wallClockMinutes: sum?.wallClockMinutes ?? null,
    // False when the run's timestamps could not be used to scope the commons, so the
    // findings below may not all belong to this run. renderDraft discloses this.
    memoryAttributed: attributed,
    totals,
    agents: Object.values(byAgent).map((b) => ({
      name: b.name,
      purpose: b.purpose,
      turns: b.turns,
      ok: b.ok,
      toolCalls: b.toolCalls,
      filesWritten: b.created + b.modified,
      violations: b.violations,
      substrates: [...b.substrates],
      // The agent's own closing words — the most direct statement of what it thinks
      // it established. Kept short; this is evidence, not the post.
      closing: truncate(cleanProse(b.lastText), 700),
    })).sort((a, b) => b.turns - a.turns),
    findings: findings.map((m) => ({
      kind: m.kind,
      agent: m.tags?.find((t) => t !== 'agent-authored' && t !== 'shorthand') || m.agentId,
      ts: m.ts,
      text: truncate(cleanProse(m.content), 600),
    })),
    decisions: decisions.slice(-12).map((m) => ({
      agent: m.agentId,
      ts: m.ts,
      text: truncate(cleanProse(m.content), 240),
    })),
    filesWritten: [...written].sort().slice(0, 60),
    incidents: incidents.map((i) => ({
      kind: i.kind, severity: i.severity, turn: i.turn,
      detail: truncate(typeof i.detail === 'string' ? i.detail : JSON.stringify(i.detail ?? ''), 200),
    })),
    oracle: sum?.oracle ?? null,
  };
}

/**
 * Render the draft as the post's canonical Markdown.
 *
 * This is what ships if the model is unavailable, and it is also the base text the
 * model is asked to rewrite. It is deliberately plain: headings, the numbers, the
 * agents' own closing statements, and an explicit unknowns section.
 */
export function renderDraft(draft) {
  const L = [];
  const t = draft.totals;

  L.push(`# ${draft.phase} — ${draft.runId}`);
  L.push('');
  L.push(`*Generated by ${SCRIBE_NAME} (conclusion agent) at ${draft.generatedAt}.*`);
  L.push('');

  // --- the numbers, stated plainly and first ---
  L.push('## What the run did');
  L.push('');
  L.push(
    `${t.turns} turns by ${t.agents} agent${t.agents === 1 ? '' : 's'}, ` +
    `${t.toolCalls} tool calls, ${t.filesWritten} files written. ` +
    `${t.okTurns}/${t.turns} turns completed cleanly` +
    (draft.wallClockMinutes != null ? `, ${draft.wallClockMinutes} minutes of wall clock` : '') +
    (t.cost > 0 ? `, $${t.cost.toFixed(4)} of compute.` : '.')
  );
  if (draft.halted) L.push(`Run ended because: **${draft.halted}**.`);
  L.push('');

  // --- agents and what they were asked ---
  if (draft.agents.length) {
    L.push('## Who worked on it');
    L.push('');
    for (const a of draft.agents) {
      L.push(`- **${a.name}** — ${a.purpose || 'no stated purpose'} ` +
        `(${a.turns} turns, ${a.toolCalls} tool calls, ${a.filesWritten} files, ${a.substrates.join('/') || 'n/a'})`);
    }
    L.push('');
  }

  // --- the actual conclusions, grouped by agent ---
  L.push('## What was established');
  L.push('');
  if (!draft.memoryAttributed) {
    // Say this loudly and before the findings, not in a footnote.
    L.push('> **Attribution caveat.** This run\'s timestamps could not be used to scope the');
    L.push('> shared commons, so the findings below are drawn from the most recent entries');
    L.push('> in the commons and may include work from other runs. Treat the attribution as');
    L.push('> approximate; the run totals above are exact.');
    L.push('');
  }
  if (draft.findings.length) {
    // Group by agent so the post reads as "X concluded Y" rather than a flat dump.
    const byAgent = {};
    for (const f of draft.findings) {
      const k = f.agent || 'unattributed';
      (byAgent[k] = byAgent[k] || []).push(f);
    }
    for (const [agent, items] of Object.entries(byAgent)) {
      L.push(`### ${agent}`);
      L.push('');
      for (const f of items.slice(0, 8)) L.push(`- ${f.text}`);
      L.push('');
    }
  } else {
    L.push('*No findings were recorded to the shared commons during this run.*');
    L.push('');
  }

  // --- each agent's closing statement ---
  const withClosing = draft.agents.filter((a) => a.closing);
  if (withClosing.length) {
    L.push('## In their own words');
    L.push('');
    for (const a of withClosing) {
      L.push(`**${a.name}:**`);
      L.push('');
      L.push(`> ${a.closing}`);
      L.push('');
    }
  }

  // --- artifacts ---
  if (draft.filesWritten.length) {
    L.push('## Artifacts written');
    L.push('');
    for (const f of draft.filesWritten.slice(0, 40)) L.push(`- \`${f}\``);
    if (draft.filesWritten.length > 40) L.push(`- …and ${draft.filesWritten.length - 40} more`);
    L.push('');
  }

  // --- honesty: what the run did NOT establish ---
  // This section is mandatory and is the reason the scribe exists rather than a
  // simple log dump. A conclusion without its limits is the failure mode the whole
  // arena was built to detect.
  L.push('## What this does not establish');
  L.push('');
  if (t.violations > 0) {
    L.push(`- The honesty oracle flagged **${t.violations} protocol violation(s)** this run. ` +
      `Claims from the affected turns should be treated as unverified.`);
  } else {
    L.push('- The honesty oracle recorded no protocol violations this run.');
  }
  if (draft.incidents.length) {
    const byKind = {};
    for (const i of draft.incidents) byKind[i.kind] = (byKind[i.kind] || 0) + 1;
    L.push('- Recorded incidents: ' +
      Object.entries(byKind).map(([k, n]) => `${k} ×${n}`).join(', ') + '.');
  }
  if (t.okTurns < t.turns) {
    L.push(`- ${t.turns - t.okTurns} of ${t.turns} turns did not complete cleanly; ` +
      `work in those turns may be partial.`);
  }
  L.push('- Every claim above is reproduced from the run ledger. No external verification ' +
    'was performed by this post, and agent self-assessments are reported as claims, not as facts.');
  L.push('');

  return L.join('\n');
}

// ---------------------------------------------------------------- honesty check

/**
 * Extract numeric tokens from text, normalized for comparison.
 *
 * We compare the set of numbers in the polished post against the set in the draft.
 * This is a blunt instrument, but it catches the failure that matters: a model
 * confidently inventing a statistic that is not in the record.
 *
 * CAUTION on commas: a comma is ambiguous — "1,234" is one number, but "turns 3, 4
 * and 5" is a list. Treating every comma as a separator turned "3, 4" into the token
 * "34", which matched nothing in the draft and caused FALSE honesty rejections on
 * perfectly faithful prose. We therefore only join across a comma when it is a real
 * thousands separator (digit-comma-3-digits) or a decimal comma; otherwise the comma
 * ends the number.
 */
function numbersIn(text) {
  const out = new Set();
  const re = /\d+(?:\.\d+|,\d{3}(?!\d)|,\d+)?/g;
  let m;
  while ((m = re.exec(String(text || ''))) !== null) {
    // Normalize: drop thousands separators, strip trailing zeros in decimals.
    let s = m[0].replace(/,/g, '');
    if (s.includes('.')) s = s.replace(/0+$/, '').replace(/\.$/, '');
    if (s) out.add(s);
    // Also record the integer part, so "40 turns" matches "40.0".
    const ip = s.split('.')[0];
    if (ip) out.add(ip);
  }
  return out;
}

/**
 * Check a polished post against the draft. Returns { ok, invented: [] }.
 *
 * `allowed` numbers are those present in the draft. A post may also legitimately
 * contain small structural numbers (list indices, years in a run id) so we ignore
 * single digits and 4-digit years, which are almost always formatting rather than
 * measurements.
 */
export function checkHonesty(polished, draftText) {
  const allowed = numbersIn(draftText);
  const seen = numbersIn(polished);
  const invented = [];
  for (const n of seen) {
    if (allowed.has(n)) continue;
    if (n.length <= 1) continue;                  // list indices, single digits
    if (/^(19|20)\d{2}$/.test(n)) continue;       // years
    invented.push(n);
  }
  return { ok: invented.length === 0, invented: invented.slice(0, 20) };
}

// ---------------------------------------------------------------- the LLM step

/**
 * Build the prompt handed to the substrate for the polish step.
 *
 * The model is given the draft as its ONLY source of facts and told, explicitly,
 * that it may not introduce any number that is not already there.
 */
export function buildScribePrompt({ draft, draftText }) {
  return [
    `You are ${SCRIBE_NAME}, the conclusion agent of an autonomous research swarm.`,
    `A run has just finished. You are its last act.`,
    ``,
    `You are NOT a chatbot and there is no human user in this conversation.`,
    `Your job is to write the PUBLIC POST that tells a human what this run concluded.`,
    ``,
    `== YOUR STANDING PURPOSE ==`,
    SCRIBE_PURPOSE,
    ``,
    `== THE RUN'S FORENSIC RECORD (this is your ONLY source of facts) ==`,
    JSON.stringify({
      runId: draft.runId,
      phase: draft.phase,
      halted: draft.halted,
      totals: draft.totals,
      agents: draft.agents.map((a) => ({ name: a.name, purpose: a.purpose, turns: a.turns, filesWritten: a.filesWritten })),
      findings: draft.findings.map((f) => ({ agent: f.agent, kind: f.kind, text: f.text })),
      incidents: draft.incidents.map((i) => ({ kind: i.kind, severity: i.severity })),
    }, null, 2),
    ``,
    `== THE DETERMINISTIC DRAFT (assembled from the ledger with no model involved) ==`,
    draftText,
    ``,
    `== YOUR TASK THIS TURN ==`,
    `Rewrite the draft as a single, well-written post for a technical reader.`,
    ``,
    `HARD RULES — violating any of these makes your output worthless:`,
    `1. Do NOT introduce any number that is not already in the draft. Not one. If the`,
    `   draft does not contain a figure, do not supply one from your own knowledge.`,
    `2. Do NOT upgrade a claim. If the record says "consistent with", do not write`,
    `   "proves". If an agent asserted something, report that it asserted it.`,
    `3. Keep every limitation in the "What this does not establish" section. You may`,
    `   reword it, but you may not drop it.`,
    `4. Do NOT invent agent names, quotes, or events.`,
    `5. If the record is thin, write a short honest post. A short true post beats a`,
    `   long padded one.`,
    ``,
    `WHAT GOOD LOOKS LIKE:`,
    `- Lead with what was actually established, not with throat-clearing.`,
    `- Attribute claims to the agent that made them.`,
    `- Be explicit about confidence: established vs. plausible vs. unknown.`,
    `- Plain prose. Markdown headings and bullets are fine; no tables of invented data.`,
    ``,
    `Write the post to the file \`POST.md\` in the current working directory, then`,
    `finish. Write ONLY the post itself to that file — no preamble, no meta-commentary.`,
  ].join('\n');
}

/**
 * Run the polish step. Returns { text, meta } — text is the polished post, or null
 * if the step failed or was rejected by the honesty check.
 *
 * Never throws: a failure here must not break the run that just completed.
 */
export async function polish({ draft, draftText, root, runId, substrate = 'agy', model = undefined, timeoutMs = 600_000, onLog = null }) {
  const log = (m) => { if (onLog) { try { onLog(m); } catch {} } };

  // The scribe works in its own scratch dir so its POST.md never contaminates the
  // research world (the oracle watches arena/world and would flag an unexplained file).
  const workDir = join(root, 'runs', runId, 'scribe');
  try { mkdirSync(workDir, { recursive: true }); } catch {}

  const prompt = buildScribePrompt({ draft, draftText });
  const postPath = join(workDir, 'POST.md');

  let result;
  try {
    result = await runTurn({
      substrate,
      model,
      prompt,
      cwd: workDir,
      timeoutMs,
      runDirOverride: workDir,
      turnTag: 'scribe',
    });
  } catch (err) {
    log(`polish step threw: ${err}`);
    return { text: null, meta: { ok: false, reason: `substrate error: ${err}` } };
  }

  // Preferred: the model wrote POST.md, which is unambiguous and avoids the model's
  // chat wrapper. Fallback: its returned text.
  let text = null;
  let source = null;
  if (existsSync(postPath)) {
    try {
      const fileText = readFileSync(postPath, 'utf8').trim();
      if (fileText.length > 200) { text = fileText; source = 'POST.md'; }
    } catch {}
  }
  if (!text && result.text && result.text.trim().length > 200) {
    text = result.text.trim();
    source = 'stdout';
  }

  if (!text) {
    log(`polish produced no usable text (ok=${result.ok}, err=${result.error})`);
    return {
      text: null,
      meta: {
        ok: false, source: null, substrate, model: result.model,
        reason: result.error || 'no usable output',
        cost: result.cost || 0, thinkingTokens: result.thinkingTokens || 0,
        toolCalls: (result.toolCalls || []).length,
      },
    };
  }

  // Honesty gate: a post that invents numbers is worse than no polish at all.
  const check = checkHonesty(text, draftText);
  if (!check.ok) {
    log(`polish REJECTED — invented ${check.invented.length} number(s) not in the ledger: ${check.invented.join(', ')}`);
    return {
      text: null,
      meta: {
        ok: false, source, substrate, model: result.model,
        reason: 'rejected: numbers not present in the ledger',
        invented: check.invented,
        cost: result.cost || 0, thinkingTokens: result.thinkingTokens || 0,
        toolCalls: (result.toolCalls || []).length,
      },
    };
  }

  return {
    text,
    meta: {
      ok: true, source, substrate, model: result.model,
      cost: result.cost || 0, thinkingTokens: result.thinkingTokens || 0,
      toolCalls: (result.toolCalls || []).length,
      durationSeconds: result.durationSeconds,
    },
  };
}

// ---------------------------------------------------------------- entry point

/**
 * Produce the post for one run and write it to <root>/posts/<file>.md
 *
 * Always writes something. `polish` is best-effort; the deterministic draft is the
 * floor. Returns the post record (also appended to the index).
 */
export async function writePost({
  root,
  runId,
  summary = null,
  substrate = 'agy',
  model = undefined,
  useLLM = true,
  timeoutMs = 600_000,
  onLog = null,
}) {
  const log = (m) => { if (onLog) { try { onLog(m); } catch {} } };

  const draft = buildDraft({ root, runId, summary });
  const draftText = renderDraft(draft);

  let body = draftText;
  let polishMeta = { ok: false, reason: 'disabled' };

  if (useLLM) {
    const p = await polish({ draft, draftText, root, runId, substrate, model, timeoutMs, onLog });
    if (p.text) { body = p.text; }
    polishMeta = p.meta;
  }

  // Provenance footer. The reader must always be able to tell whether the prose came
  // from a model or straight from the ledger — that distinction is the entire point.
  const provenance = polishMeta.ok
    ? `Prose by ${SCRIBE_NAME} (${polishMeta.substrate}/${polishMeta.model}). ` +
      `All figures reproduced from the run ledger; the deterministic draft is preserved below.`
    : `Deterministic draft from the run ledger (no model). ` +
      `Polish step skipped: ${polishMeta.reason || 'unavailable'}.`;

  // One stable file per run. The name is derived from the RUN, not from the moment
  // the post was generated: regenerating a post tomorrow must overwrite the same file
  // rather than leaving yesterday's version orphaned in the directory.
  const file = `${slug(runId)}.md`;
  const dir = join(root, POSTS_DIR);
  mkdirSync(dir, { recursive: true });

  // If a previous post for this run exists under a different (older, date-prefixed)
  // name, remove it so the directory never holds two posts for one run.
  try {
    for (const e of readdirSync(dir)) {
      if (!e.endsWith('.md')) continue;
      if (e === file) continue;
      if (e.endsWith(`-${slug(runId)}.md`)) {
        try { unlinkSync(join(dir, e)); } catch {}
      }
    }
  } catch {}

  const full = [
    body.trim(),
    '',
    '---',
    '',
    `*${provenance}*`,
    '',
    // NOTE: the site's markdown renderer replaces this whole <details> line with its
    // own <summary> label, so the wording here is what a reader of the raw .md sees.
    // Keep it in sync with the label in site/index.html's md() if either changes.
    `<details><summary>Deterministic draft (ledger-derived)</summary>`,
    '',
    draftText,
    '',
    `</details>`,
    '',
  ].join('\n');

  writeFileSync(join(dir, file), full, 'utf8');

  const record = {
    runId,
    file,
    title: `${draft.phase} — ${runId}`,
    phase: draft.phase,
    generatedAt: draft.generatedAt,
    polished: Boolean(polishMeta.ok),
    polish: polishMeta,
    totals: draft.totals,
    halted: draft.halted,
    agents: draft.agents.map((a) => ({ name: a.name, purpose: a.purpose, turns: a.turns })),
  };

  updateIndex(dir, record);
  log(`post written: ${join(dir, file)}${polishMeta.ok ? ' (polished)' : ' (draft)'}`);
  return record;
}

/**
 * Maintain posts/index.json.
 *
 * Regenerating a post for the same run REPLACES its index entry rather than
 * appending a duplicate — otherwise re-running post.mjs on an old run would slowly
 * fill the site with copies.
 */
export function updateIndex(dir, record) {
  const indexPath = join(dir, 'index.json');
  let index = readJson(indexPath);
  if (!index || !Array.isArray(index.posts)) {
    index = { generatedAt: new Date().toISOString(), posts: [] };
  }
  index.posts = index.posts.filter((p) => p.runId !== record.runId);
  index.posts.push(record);
  // Newest first, so the site can render in order without sorting.
  index.posts.sort((a, b) => String(b.generatedAt).localeCompare(String(a.generatedAt)));
  index.generatedAt = new Date().toISOString();
  writeFileSync(indexPath, JSON.stringify(index, null, 2), 'utf8');
  return index;
}

/** Read all posts (used by the site exporter). */
export function readPosts(root) {
  const dir = join(root, POSTS_DIR);
  const index = readJson(join(dir, 'index.json'));
  if (!index || !Array.isArray(index.posts)) return [];
  return index.posts.map((p) => {
    let body = '';
    try { body = readFileSync(join(dir, p.file), 'utf8'); } catch {}
    return { ...p, body };
  }).filter((p) => p.body);
}
