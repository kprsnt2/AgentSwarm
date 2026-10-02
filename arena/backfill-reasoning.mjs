/**
 * Backfill reasoning for turns recorded before reasoning capture existed.
 *
 * The raw CLI streams on disk still contain the thinking_delta events, so the
 * internal monologue can be recovered retroactively without re-running anything.
 *
 * Writes runs/<id>/turns-priced.jsonl (preserving the hash-chained turns.jsonl).
 *
 * Usage: node backfill-reasoning.mjs [runId]
 */
import { readFileSync, writeFileSync, existsSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { costOfTurn } from './pricing.mjs';
import { ARENA } from './paths.mjs';


const RUNS = join(ARENA, 'runs');

function readJsonl(p) {
  if (!existsSync(p)) return [];
  const out = [];
  for (const l of readFileSync(p, 'utf8').split(/\r?\n/)) {
    const t = l.trim(); if (!t) continue;
    try { out.push(JSON.parse(t)); } catch {}
  }
  return out;
}

/** Recover reasoning from a raw CLI event stream file. */
function reasoningFromStream(path) {
  if (!existsSync(path)) return { text: '', blocks: 0 };
  let raw;
  try { raw = readFileSync(path, 'utf8'); } catch { return { text: '', blocks: 0 }; }

  const blocks = [];
  let current = null;
  let text = '';

  for (const line of raw.split(/\r?\n/)) {
    const t = line.trim();
    if (!t || t[0] !== '{') continue;
    let ev;
    try { ev = JSON.parse(t); } catch { continue; }
    const ame = ev.assistantMessageEvent;
    if (ame) {
      const type = ame.type || '';
      if (type === 'thinking_start') { current = { text: '' }; blocks.push(current); }
      else if (type === 'thinking_delta') {
        if (!current) { current = { text: '' }; blocks.push(current); }
        current.text += ame.delta || '';
      } else if (type === 'thinking_end') {
        if (current && ame.content != null) current.text = ame.content;
        if (current) { text += (text ? '\n\n' : '') + current.text; current = null; }
      }
    }
    // Fallback: whole thinking parts on final messages.
    const msg = ev.message;
    if (msg && msg.role === 'assistant' && Array.isArray(msg.content)) {
      for (const part of msg.content) {
        if (part.type === 'thinking' && part.thinking && !blocks.length) {
          blocks.push({ text: part.thinking });
          text += (text ? '\n\n' : '') + part.thinking;
        }
      }
    }
  }
  return { text: text.trim(), blocks: blocks.length };
}

const only = process.argv[2];
const runs = readdirSync(RUNS, { withFileTypes: true })
  .filter((d) => d.isDirectory() && (!only || d.name === only)).map((d) => d.name);

for (const r of runs) {
  const dir = join(RUNS, r);
  const basePath = join(dir, 'turns.jsonl');
  if (!existsSync(basePath)) continue;
  const base = readJsonl(basePath);
  if (!base.length) continue;

  let recovered = 0, chars = 0;
  const out = base.map((t) => {
    const pricing = t.pricing || costOfTurn({ model: t.model, usage: t.usage, reportedCost: t.cost || 0 });
    let reasoning = t.reasoning || '';
    let blocks = t.reasoningBlocks || 0;
    if (!reasoning && t.stdoutPath) {
      const rr = reasoningFromStream(t.stdoutPath);
      reasoning = rr.text;
      blocks = rr.blocks;
    }
    if (reasoning) { recovered++; chars += reasoning.length; }
    return {
      ...t,
      reasoning,
      reasoningChars: reasoning.length,
      reasoningBlocks: blocks,
      pricing,
    };
  });

  writeFileSync(join(dir, 'turns-priced.jsonl'), out.map((t) => JSON.stringify(t)).join('\n') + '\n', 'utf8');
  console.log(`${r}: recovered reasoning for ${recovered}/${base.length} turns (${chars.toLocaleString()} chars)`);
}
