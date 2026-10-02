/**
 * Export the findings explorer — one HTML page per agent-authored report and one
 * per run ledger.
 *
 * READ-ONLY with respect to arena/world. The artifacts are the agents' output and
 * are never modified; pages are written to site/corpus/, and site/build.mjs copies
 * them to site/dist/corpus/ and docs/corpus/.
 *
 * Usage:
 *   node export-site.mjs      # findings.json first
 *   node export-corpus.mjs
 *   cd ../site && node build.mjs
 */

import { readFileSync, writeFileSync, mkdirSync, rmSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import {
  SITE, WORLD, listWorldFiles, loadAnnotations,
  renderMarkdown, pageHtml, escapeHtml, REPO_BLOB, REPO_URL,
} from './corpus-index.mjs';

const OUT = join(SITE, 'corpus');
const findingsPath = join(SITE, 'data', 'findings.json');

if (!existsSync(findingsPath)) {
  console.error('site/data/findings.json not found — run  node export-site.mjs  first.');
  process.exit(1);
}

const findings = JSON.parse(readFileSync(findingsPath, 'utf8'));
const annotations = loadAnnotations();
const files = listWorldFiles();

// Regenerate from scratch so a renamed artifact cannot leave a stale page behind.
rmSync(OUT, { recursive: true, force: true });
mkdirSync(OUT, { recursive: true });

const byFile = new Map();
for (const a of annotations.entries) {
  if (!a.file) continue;
  if (!byFile.has(a.file)) byFile.set(a.file, []);
  byFile.get(a.file).push(a);
}

function firstHeading(text, fallback) {
  const m = String(text).match(/^#\s+(.+)$/m);
  return m ? m[1].replace(/[*_`]/g, '').trim() : fallback;
}

let reportPages = 0;
let skipped = 0;

for (const f of files) {
  if (f.ext !== 'md') { skipped += 1; continue; }
  let text;
  try { text = readFileSync(join(WORLD, f.path), 'utf8'); }
  catch { continue; }

  const badges = byFile.get(f.path) || [];
  const title = firstHeading(text, f.path);
  const body = [
    `<h1>${escapeHtml(title)}</h1>`,
    `<p style="color:var(--fg3);font-family:var(--mono);font-size:12px">` +
      `${escapeHtml(f.domainLabel)} · ${(f.bytes / 1024).toFixed(1)} KB · ${escapeHtml(f.path)}</p>`,
    renderMarkdown(text),
  ].join('\n');

  const html = pageHtml({
    title,
    subtitle: f.domainLabel,
    badges,
    body,
    backHref: '../index.html#corpus',
    repoHref: `${REPO_BLOB}${encodeURI(f.path)}`,
    sha: f.sha1,
  });
  writeFileSync(join(OUT, `${f.slug}.html`), html, 'utf8');
  reportPages += 1;
}

// ---- run ledger pages ----
const postByRun = new Map((findings.posts || []).map((p) => [p.runId, p]));
let runPages = 0;

for (const run of findings.runs || []) {
  const integ = run.ledgerIntegrity || {};
  const integBadge = ['turns', 'events', 'incidents']
    .map((k) => integ[k] ? `<span class="b ${integ[k].ok ? 'verified' : 'defect'}">${k} chain ${integ[k].ok ? 'ok' : 'BROKEN'}</span>` : '')
    .join(' ');

  const rows = (run.turnDetail || []).map((t) => {
    const ok = t.ok ? '<span class="b verified">ok</span>' : `<span class="b defect">${escapeHtml(t.error || 'fail')}</span>`;
    const files = `+${t.created} ~${t.modified} -${t.deleted}`;
    return `<tr>
      <td>${t.seq}</td>
      <td>${escapeHtml(t.agent || '')}</td>
      <td><code>${escapeHtml(t.substrate || '')}</code></td>
      <td>${ok}</td>
      <td>${t.toolCalls ?? ''}</td>
      <td>${t.thinkingTokens ?? ''}</td>
      <td>$${(t.cost || 0).toFixed(4)}</td>
      <td>${files}</td>
      <td>${t.violations || 0}</td>
      <td><code>${escapeHtml(String(t.hash || '').slice(0, 10))}</code></td>
    </tr>`;
  }).join('');

  const incidents = (run.incidents || []).length
    ? `<h2>Incidents</h2><ul>${run.incidents.map((i) => `<li><code>${escapeHtml(i.kind)}</code> (${escapeHtml(i.severity || '')})${i.turn != null ? ` at turn ${i.turn}` : ''}</li>`).join('')}</ul>`
    : '<p>No incidents recorded.</p>';

  const post = postByRun.get(run.id);
  const body = [
    `<h1>Run ${escapeHtml(run.id)}</h1>`,
    `<p style="color:var(--fg3);font-family:var(--mono);font-size:12px">${escapeHtml(run.phase)} · ` +
      `${run.turns} turns · ${run.okTurns} ok · $${(run.cost || 0).toFixed(4)} · ${run.toolCalls} tool calls · ` +
      `${run.violations} violations · halted: ${escapeHtml(run.halted || 'unknown')}</p>`,
    `<div class="badges">${integBadge}</div>`,
    post ? `<p><a href="../index.html#posts">Conclusion post (${escapeHtml(post.polished ? 'polished' : 'ledger draft')})</a></p>` : '',
    `<h2>Turns</h2>`,
    `<div class="tw"><table><thead><tr><th>#</th><th>Agent</th><th>Harness</th><th>Status</th><th>Tools</th><th>Think tok</th><th>Cost</th><th>Files</th><th>Viol</th><th>Hash</th></tr></thead><tbody>${rows}</tbody></table></div>`,
    incidents,
    `<p style="color:var(--fg3);font-size:12px">Each hash is computed over the previous hash plus the record body; editing any turn breaks the chain and is detected by <code>node verify-ledger.mjs</code>.</p>`,
  ].join('\n');

  const html = pageHtml({
    title: `Run ${run.id}`,
    subtitle: run.phase,
    body,
    backHref: '../index.html#corpus',
    repoHref: `${REPO_URL}/tree/main/arena/runs/${encodeURI(run.id)}`,
  });
  writeFileSync(join(OUT, `run-${run.id}.html`), html, 'utf8');
  runPages += 1;
}

console.log(`wrote ${reportPages} report pages + ${runPages} run pages to site/corpus/`);
console.log(`${files.length - reportPages} non-markdown artifacts (engines, data) link to the repository instead`);
if (skipped !== files.length - reportPages) console.log(`(${skipped} skipped)`);
