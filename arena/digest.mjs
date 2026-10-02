/**
 * Digest — cheap, bounded summaries of what agents actually produced.
 *
 * WHY THIS EXISTS: the agents are writing 30-40 KB markdown reports each. Reading
 * them into a chat context to "see what happened" costs far more than producing
 * them. This script prints a bounded digest: headings, key numbers, and short
 * excerpts only.
 *
 * Usage:
 *   node digest.mjs                  # digest every artifact
 *   node digest.mjs <filename>       # digest one artifact
 *   node digest.mjs --list           # just list files
 */

import { readFileSync, existsSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { WORLD } from './paths.mjs';


const args = process.argv.slice(2);

function files() {
  const out = [];
  (function walk(d, base = '') {
    if (!existsSync(d)) return;
    for (const e of readdirSync(d, { withFileTypes: true })) {
      const rel = base ? `${base}/${e.name}` : e.name;
      if (e.isDirectory()) { if (e.name !== '__pycache__') walk(join(d, e.name), rel); continue; }
      out.push({ rel, full: join(d, e.name), size: statSync(join(d, e.name)).size });
    }
  })(WORLD);
  return out.sort((a, b) => b.size - a.size);
}

const all = files();

if (args[0] === '--list' || !args.length) {
  console.log(`${all.length} artifacts, ${Math.round(all.reduce((a, f) => a + f.size, 0) / 1024)} KB total\n`);
  for (const f of all) console.log(`${String(Math.round(f.size / 1024)).padStart(5)} KB  ${f.rel}`);
  if (!args.length) console.log('\n(pass a filename to digest it)');
  if (!args.length) process.exit(0);
}

const target = all.find((f) => f.rel.includes(args[0]));
if (!target) { console.log(`not found: ${args[0]}`); process.exit(1); }

const text = readFileSync(target.full, 'utf8');
const lines = text.split(/\r?\n/);
console.log(`\n${'='.repeat(70)}\n${target.rel}  (${Math.round(target.size / 1024)} KB, ${lines.length} lines)\n${'='.repeat(70)}\n`);

// headings
const headings = lines.filter((l) => /^#{1,3}\s/.test(l));
console.log(`## Structure (${headings.length} headings)`);
for (const h of headings.slice(0, 30)) console.log(`  ${h.slice(0, 100)}`);

// key quantitative lines: anything with a number + unit-ish token
const quant = lines.filter((l) =>
  /\d/.test(l) && /(km\/s|GeV|MeV|kg|years|yr|%|sigma|σ|Mpc|K\b|cm\^-?3|c\b|J\b|W\/m|eV|Ga|ly)/.test(l)
  && l.length < 160 && !/^\s*\|?\s*-{3,}/.test(l));
if (quant.length) {
  console.log(`\n## Quantitative claims (${quant.length} lines, first 18)`);
  for (const l of quant.slice(0, 18)) console.log(`  ${l.trim().slice(0, 130)}`);
}

// tables
const tableRows = lines.filter((l) => l.trim().startsWith('|') && l.split('|').length > 3);
if (tableRows.length) {
  console.log(`\n## Tables (${tableRows.length} rows, first 12)`);
  for (const l of tableRows.slice(0, 12)) console.log(`  ${l.trim().slice(0, 130)}`);
}

// conclusion-ish sections
const concl = [];
for (let i = 0; i < lines.length; i++) {
  if (/^#{2,3}\s*(conclusion|summary|finding|result|verdict|answer|implication)/i.test(lines[i])) {
    concl.push(lines.slice(i, i + 6).join('\n'));
  }
}
if (concl.length) {
  console.log(`\n## Conclusions (first ${Math.min(concl.length, 2)})`);
  for (const c of concl.slice(0, 2)) console.log(c.split('\n').map((l) => '  ' + l.slice(0, 130)).join('\n') + '\n');
}
